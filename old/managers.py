'''
    managers.py
    Part of Softly Into the Night, a roguelike by Jacob Wharton.
    Copyright 2019.
'''

import math

from const import *
import rogue as rog
import components as cmp


'''
#
# abstract Manager class
#
# 
# A manager is an object that has functions for handling a complex task,
# which is carried out using its 'run()' function.
# give it some starting data, then call 'run()' inside a while loop.
# check the output of the manager with the property 'result'.
# finish the execution by calling 'close()'.
#
#     * Only the 'run', 'close', and 'result' functions should be called
    outside of the manager.
      * The manager only accesses its own functions through its 'run' method.
      * You can intercept the 'run' function at the end of each iteration
    in your while loop, simply by writing code following the 'run()' call.
    This is one of the useful things about managers.
#
'''
class Manager(object):
    
    def __init__(self):
        self._result=None
    def set_result(self,new):       self._result=new
    @property
    def result(self):           return self._result
    def run(self, *args,**kwargs):
        self.set_result(None)
    def close(self):
        pass
#

class GameStateManager(Manager):
    
    def __init__(self):
        super(GameStateManager,self).__init__()
        self._resume_game_state="normal"
    def close(self):
        super(GameStateManager,self).close()
        self.resume_game_state()
    def set_resume_state(self,new): self._resume_game_state=new
    def resume_game_state(self): rog.game_set_state(self._resume_game_state)
#






'''
    TODO: implement this Manager
'''
#
# Stat Modifier Effects
#

class Manager_Effects(Manager):
    ID = 0
    
    def __init__(self):
        super(Manager_Effects, self).__init__()

        self._statMods = {}
        
    def add(self, ent,mod): # create and add a new effect, return its ID
        Manager_Effects.ID = Manager_Effects.ID + 1
        newID = Manager_Effects.ID
        self._statMods.update( {newID : mod} )
        return newID

    def remove(self, modID): # remove an effect from the dict
        del self._statMods[modID]

    def get(self, modID):
        return self._statMods.get(modID, None)
        



#
# Events
#

class Manager_Events(Manager):
    
    def __init__(self):
        super(Manager_Events, self).__init__()
        
        self._sights={}
        self._sounds={}
        self._listeners_sights=set()
        self._listeners_sounds=set()
    
    def add_sight(self, x,y, text):
        for obj in self._listeners_sights:
            if rog.can_see(obj, x,y):
                lis=self.get_sights(obj)
                lis.append(Event_Sight(x,y, text))
                self._sights.update({obj : lis})
    
    def add_sound(self, x,y, text1,text2, volume):
        for obj in self._listeners_sounds:
            if rog.can_see(obj, x,y):
                continue
            data=rog.can_hear(obj, x,y, volume)
            if data:
                dx,dy,volHeard=data
                if volHeard <= 1:
                    dx=dy=0
            #   each entity gets its own Event object,
            #   specific to its own perception.
                text=text1 if obj.stats.get("hearing") >= SUPER_HEARING else text2
                lis=self.get_sounds(obj)
                lis.append(Event_Sound(dx,dy, text, volHeard))
                self._sounds.update({obj : lis})
    
    def get_sights(self,obj):       return  self._sights.get(obj,[])
    def get_sounds(self,obj):       return  self._sounds.get(obj,[])
    def add_listener_sights(self,obj):      self._listeners_sights.add(obj)
    def add_listener_sounds(self,obj):      self._listeners_sounds.add(obj)
    def remove_listener_sights(self,obj):
        if obj in self._listeners_sights:
            self._listeners_sights.remove(obj)
    def remove_listener_sounds(self,obj):
        if obj in self._listeners_sounds:
            self._listeners_sounds.remove(obj)
    def clear(self):
        self._sights={}
        self._sounds={}

class Event_Sight():
    def __init__(self, x,y, text):
        self.x=x
        self.y=y
        self.text=text
class Event_Sound():
    def __init__(self, dx,dy, text, volume):
        self.dx=dx
        self.dy=dy
        self.text=text
        self.volume=volume




    
#
# Sights Seen by player
#

class Manager_SightsSeen(Manager):
    # should run at end of turn (right before player turn begins)
    
    def __init__(self):
        super(Manager_SightsSeen,self).__init__()
        
        self.init_sights()
    
    def run(self):
        super(Manager_SightsSeen,self).run()
        
        atLeastOneMsg=False
        text=""
        for k,v in self.sights.items():
            if not v: continue
            atLeastOneMsg=True
            lis=v
            pc=rog.Ref.pc
            
            dirStr=DIRECTIONS_TERSE[k]
            if not dirStr == "self":
                text += "<{d}> ".format(d=dirStr)
            
            for strng in lis:
                text += "{}{} ".format(strng[0].upper(), strng[1:])

        if atLeastOneMsg:
            rog.msg(text)
            self.init_sights()
        
    def init_sights(self):
        self.sights={
        #   dir from: strings
            (0,0)   : [],
            (1,0)   : [],
            (1,-1)  : [],
            (0,-1)  : [],
            (-1,-1) : [],
            (-1,0)  : [],
            (-1,1)  : [],
            (0,1)   : [],
            (1,1)   : [],
        }
    
    def add(self, ev):
        k=self.get_direction(rog.Ref.pc, (ev.x,ev.y,))
        self.sights[k].append(ev.text)

    def get_direction(self, pc, coords):
        xf,yf=coords
        pos = rog.world().component_for_entity(pc, cmp.Position)
        if (pos.x == xf and pos.y == yf):
            return 0,0
        rads=maths.pdir(pos.x,pos.y,xf,yf)
        dx=round(math.cos(rads))
        dy=round(math.sin(rads))
        return dx,dy

#
# Sounds Heard by player
#

class Manager_SoundsHeard(Manager):
    #should run at end of turn (right before player turn begins)
    
    VOLCONST=400
    
    def __init__(self):
        super(Manager_SoundsHeard,self).__init__()
        
        self.init_sounds()
    
    def run(self):
        super(Manager_SoundsHeard,self).run()
        
        atLeastOneMsg=False
        text="You hear "
        for k,v in self.sounds.items():
            vol,lis=v
            if not vol: continue
            if vol > VOLUME_DEAFEN:
                rog.set_status(rog.pc(), DEAF)
            #super hearing
            if rog.pc().stats.get("hearing") >= SUPER_HEARING:
                volTxt=self.get_volume_name(vol)
                dirStr=DIRECTIONS_TERSE[k]
                if not dirStr == "self":
                    text += "<{d}>".format(d=dirStr)
                text += "({v}) ".format(v=volTxt)
            #combine strings with commas
            for strng in lis:
                text += "{s}, ".format(s=strng)
            #terminate with a period
            text=text[:-2] + "."
            atLeastOneMsg=True

        if atLeastOneMsg:
            rog.msg(text)
            self.init_sounds()
        
    def init_sounds(self):
        self.sounds={
        #   dir from: vol,strings
            (0,0)   : (0,[]),
            (1,0)   : (0,[]),
            (1,-1)  : (0,[]),
            (0,-1)  : (0,[]),
            (-1,-1) : (0,[]),
            (-1,0)  : (0,[]),
            (-1,1)  : (0,[]),
            (0,1)   : (0,[]),
            (1,1)   : (0,[]),
        }  
    
    def add(self, ev):
        
        k=(ev.dx,ev.dy,)
        data=self.sounds[k]
        cVol,lis=data

        if not ev.text in lis:
            lis.append(ev.text)
        maxVol=max(ev.volume, cVol)
        self.sounds.update({k : (maxVol, lis,)})
            
    def get_volume_name(self, perceivedVolume):
        pv=perceivedVolume
        vc=Manager_SoundsHeard.VOLCONST
        if pv >= vc:    return "fff"
        if pv >= vc/2:  return "ff"
        if pv >= vc/4:  return "f"
        if pv >= vc/8:  return "mf"
        if pv >= vc/16: return "mp"
        if pv >= vc/32: return "p"
        if pv >= vc/64: return "pp"
        else:           return "ppp"




#---------------------#
# game state managers #
#---------------------#


#
# Move View
#

class Manager_MoveView(GameStateManager):
    def __init__(self,view, con):
        super(Manager_MoveView, self).__init__()
        
        self.NUDGESPD   = 10
        self.view       = view
        self.con        = con
        self.refresh()
    
    def run(self, pcAct):
        super(Manager_MoveView, self).run(pcAct)
        
        for act,args in pcAct:
            if act=="target":   self.move(args)
            elif act=="select": self.set_result("select")
            elif act=="exit":   self.set_result("exit")
    
    def close(self):
        super(Manager_MoveView, self).close()
        
        rog.update_game()
        if self.result == "select":
            rog.view_center_player()
        
        
    def move(self,arg):
        dx,dy,dz = arg
        self.view.nudge(dx*self.NUDGESPD, dy*self.NUDGESPD)
        self.refresh()

    def refresh(self):
        libtcod.console_blit(self.con,
                             self.view.x, self.view.y, self.view.w, self.view.h,
                             rog.con_final(),
                             rog.view_port_x(), rog.view_port_y())
        rog.refresh()
    #
#




#
# Select Tile
#
# possible results:
#   - tuple of screen coordinates
#   - K_ESCAPE
#
# currently does nothing with its results. Used as a parent object...
#

class Manager_SelectTile(GameStateManager):
    
    def __init__(self, xs,ys, view, con):
        super(Manager_SelectTile, self).__init__()

        self.cursor     = IO.Cursor(0,0,rate=0.3)
        self.set_pos(rog.getx(xs), rog.gety(ys))
        self.view       = view
        self.con        = con
    
    def run(self, pcAct):
        super(Manager_SelectTile, self).run(pcAct)
        
        self.cursor_blink()
        for act,arg in pcAct:
            if act=='rclick':   self.rclick(arg)
            elif act=='lclick': self.lclick(arg)
            elif act=='target': self.nudge(arg)
            elif act=='select': self.select()
            elif act=="exit":   self.set_result('exit')
    
    def close(self):
        super(Manager_SelectTile, self).close()

        pass
    
    def cursor_blink(self):
        if self.cursor.blink():
            self.cursor.draw()
            libtcod.console_flush()
    
    def lclick(self,arg):
        xto,yto,zto = arg
        if (self.x==xto and self.y==yto):
            self.select(); return
        self.port(arg)
    
    def rclick(self,*args):
        self.port(*args)
        self.select()
        
    def port(self,tupl):
        xto,yto,zto = tupl
        self.set_pos(xto,yto)
        
    def nudge(self,tupl):
        dx,dy,dz = tupl
        if (self.is_shift_in_view_bounds(dx,dy)
                or self.is_cursor_by_edge_of_room(dx,dy) ):
            self.set_pos(self.x + dx, self.y + dy)
        else:
            self.view.nudge(dx,dy)
            self.refresh()
    
    def is_shift_in_view_bounds(self, dx,dy):
        if ( (dx == -1 and self.view.x == 0)
                or (dx == 1 and self.view.x == rog.view_max_x())
                or (dy == -1 and self.view.y == 0)
                or (dy == 1 and self.view.y == rog.view_max_y()) ):
             return True
        return False
    
    def is_cursor_by_edge_of_room(self, dx,dy):
        if ( (dx == 1 and self.x < self.view.w/2)
                or (dy == 1 and self.y < self.view.h/2)
                or (dx == -1 and self.x > self.view.w/2)
                or (dy == -1 and self.y > self.view.h/2) ):
             return True
        return False
            
    def set_pos(self,xto,yto):
        self.x=xto; self.y=yto
        self.restrict_pos()
        self.cursor.set_pos(self.x,self.y)
        self.cursor.blink_reset_timer_on()
        rog.refresh()
        
    def restrict_pos(self):
        x1 = rog.view_port_x()
        x2 = x1 + rog.view_w() - 1
        y1 = rog.view_port_y()
        y2 = y1 + rog.view_h() - 1
        self.x = maths.restrict(self.x, x1,x2)
        self.y = maths.restrict(self.y, y1,y2)
        
    def select(self):
        self.set_result( (rog.mapx(self.x), rog.mapy(self.y),) )
        
    def refresh(self):
        libtcod.console_blit(self.con,
                             self.view.x, self.view.y, self.view.w, self.view.h,
                             rog.con_final(),
                             rog.view_port_x(), rog.view_port_y())
        rog.refresh()
#




#
# Look Command
#
class Manager_Look(Manager_SelectTile):

    def __init__(self, *args,**kwargs):
        super(Manager_Look, self).__init__(*args,**kwargs)
    
    def run(self, *args,**kwargs):
        super(Manager_Look, self).run(*args,**kwargs)
    
    def close(self):
        super(Manager_Look, self).close()

        if (self.result and not self.result == "exit"):
            x,y = self.result
            rog.alert( rog.identify_symbol_at(x,y) )

        


#
# Print Vertically Scrollable Text
#
# possible results come from IO.Input()
#

class Manager_PrintScroll(GameStateManager):

    def __init__(self,con_mid,width,height, con_top,con_bot,h1=3,h2=4,maxy=0):
        super(Manager_PrintScroll, self).__init__()
        
        self.con_mid    = con_mid#dle
        self.con_top    = con_top
        self.con_bot    = con_bot#tom
        self.box1h      = h1
        self.box2h      = h2
        self.maxy       = maxy
        self.width      = width
        self.height     = height
        self.box2y      = self.height-self.box2h
        self.scrollspd  = 1
        self.pagescroll = self.height -(self.box1h +self.box2h +2)
        self.y          = 0
        self.update()
    
    def run(self, pcAct):
        super(Manager_PrintScroll, self).run(pcAct)
        
        self.user_input(pcAct)
    
    def close(self):
        super(Manager_PrintScroll, self).close()
        
        self.consoles_delete()
        rog.update_final()
    
    def user_input(self, pcAct):
        for act, arg in pcAct:
            if act=="target":
                self.y += arg[1]*self.scrollspd
                self.y=maths.restrict(self.y,0,self.maxy)
            elif act=="page up":    self.y = max(0,         self.y -int(self.pagescroll))
            elif act=="page down":  self.y = min(self.maxy, self.y +int(self.pagescroll))
            elif act=="home":       self.y = 0
            elif act=="end":        self.y = max(0,         self.maxy -self.pagescroll)
            elif (act=="select" or act=="exit"): self.set_result('exit')
            self.update()
    
    def update(self):
        rog.blit_to_final(self.con_mid, 0,self.y,  0,self.box1h)
        if self.con_top: rog.blit_to_final(self.con_top, 0,0, 0,0)
        if self.con_bot: rog.blit_to_final(self.con_bot, 0,0, 0,self.box2y)
        rog.refresh()
        
    def consoles_delete(self):
        libtcod.console_delete(self.con_mid)
        if self.con_top: libtcod.console_delete(self.con_top)
        if self.con_bot: libtcod.console_delete(self.con_bot)
#


'''
    Menu
    *bound_w and bound_h are the window dimensions
    *items is an iterable of strings
#   This manager's result is a selection from items
#   item in items can be a Thing() or a string
'''

class Manager_Menu(Manager): # TODO: Make into a GameStateManager ???
    
    def __init__(self, name, x,y, bound_w,bound_h, keysItems, autoItemize=True): 
        super(Manager_Menu, self).__init__()
        
    #   init from args      #
    #   - keysItems: {unique id : pointer to menu item}
    #   - keysItems can be manually created and passed in
    #   or automatically created if autoItemize == True
    #       (in which case you pass in an iterable)
    #       iterable can contain strings or an object with attr "name"
        self.name=name
        self.x=x
        self.y=y
        self.bound_w=bound_w    # limits of where the menu can be on screen
        self.bound_h=bound_h
        self.border_w=1
        self.border_h=1
        if autoItemize:
            new={}
            for k,v in misc.itemize(keysItems):
                new.update({k:v})
            self.keysItems=new
        else: self.keysItems=keysItems
    #   get width and height from items
        widest=0
        for k,v in self.keysItems.items():
            leni=len(self.get_name(v)) + 4
            if leni > widest:
                widest=leni
        lenTitlePadding=4
        borderPadding=2
        lenn=len(self.name) + borderPadding + lenTitlePadding
        if lenn > widest: widest=lenn
        self.w=widest
        self.h=len(self.keysItems)
        self.w += self.border_w*2
        self.h += self.border_h*2
    #   make sure it doesn't go off-screen
        self.x -= max(0, self.x + self.w - self.bound_w)
        self.y -= max(0, self.y + self.h - self.bound_h)
    #   draw
        self.con=libtcod.console_new(self.w, self.h)
        self.draw()
    #   clear buffer
        IO.get_raw_input()
    
    def run(self):
        super(Manager_Menu, self).run()
        
        libtcod.sys_sleep_milli(5)
        key,mouse=IO.get_raw_input()
        
    #   mouse
        if mouse.lbutton_pressed:
            self.refresh()
            index=mouse.cy - self.y - self.border_h
            if (index >= 0 and index < self.h - self.border_h*2):
                result=tuple(self.keysItems.values())[index]
                self.set_result(result)
        
    #   key
        if libtcod.console_is_key_pressed(key.vk):
            if key.vk == libtcod.KEY_ESCAPE:
                self.set_result(-1)
        if key.vk == libtcod.KEY_TEXT: # select
            self.refresh()
            n=self.keysItems.get(key.text,None) #.decode()
            if n: self.set_result(n)
    
    def close(self):
        super(Manager_Menu, self).close()
        
        libtcod.console_delete(self.con)
        rog.refresh()
        
    def draw(self):
        def sorter(val):
            k,v = val
            #if (ord(k) < (65+26) and ord(k) >= 65): #this code makes capital and lowercase appear in inconsistent orders in the list...
            #    k=chr(ord(k)+32) #offset CAPS chars to make capital and lowercase equal (with capital coming second)
            return k
        y=0
    #   draw title and box
        misc.rectangle(self.con, 0,0, self.w,self.h, 0)
        title="<{}>".format(self.name)
        tx=math.floor( (self.w - len(title)) /2)
        libtcod.console_print(self.con, tx, 0, title)
    #   draw options
        lis=list(self.keysItems.items())
        lis.sort(key=sorter)
        for key,item in lis:
            name=self.get_name(item)
            libtcod.console_print(
                self.con, 1, y + 1, '({i}) {nm}'.format(i=key, nm=name) )
            y += 1
        libtcod.console_blit(
            self.con, 0,0, self.w, self.h,
            0, self.x, self.y
        )
        libtcod.console_flush()

    def get_name(self,item):
        return item.name if hasattr(item,'name') else item
    def refresh(self):
        self.draw()










    


