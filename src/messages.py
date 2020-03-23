'''
    messages.py
    Softly Into the Night, a sci-fi/Lovecraftian roguelike
    Copyright (C) 2020 Jacob Wharton.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

'''
    tags in {} are substituted with the following.
    tag   - substituted with:
    pct     PC title
    pcn     PC name
    pcc     PC class
    pcgg    PC gender - generic ("man", "woman")
    pcgp    PC gender - polite ("sir", "madam")
    pcgo    PC gender - object ("him", "her")
    npct    NPC title
    npcn    NPC name
    npcc    NPC class
    npcgg   NPC gender - generic
    nc      name calling
    ncs     name calling plural
    slur    curse
    slurs   slur plural
    flirt   flirt word ("baby", "cutie", "hot stuff", "",)
    tod     time of day
    tof     term of friendship
    toe     term of endearment
    gcomp   generic compliment
    comp    compliment
    wcomp   whacky over the top compliment
    icomp   item of a compliment (something you are wearing or holding or carrying)
    insult  generic 
    
    
    * capitalized first letter indicates the need to capitalize the word
        that is substituted.
'''

TERM_OF_FRIENDSHIP={
    "male" : ("bro","dude","man",),
    "female" : ("girl","babe","woman",),
}

TERM_OF_ENDEARMENT=(
    "darling", "dear", "love", "dear friend",
)

TERM_OF_ATTRACTION=(
    "sweety", "honey", "darling",
)

SLUR=(
    # singular
    ("jackass", "cuntface", "dick", "bitch", "motherfucker", "human trash",
     "wretch", "cur", "devil", "douchebag",),
    # plural
    ("jackasses", "cuntfaces", "dicks", "bitches", "motherfuckers", "human trash",
     "wretches", "curs", "devils", "douchebags",),
)

NAMECALLING=(
    # singular
    ("ninny", "twit", "loser", "asshole", "jerk", "imbecile", "simp",
     "simpleton", "fool", "ass", "asshat", "cunt", "donkey",),
    # plural
    ("ninnies", "twits", "losers", "assholes", "jerks", "imbeciles", "simps",
     "simpletons", "fools", "asses", "asshats", "cunts", "donkeys",),
)

COMPLIMENT=(
    "you have beautiful eyes",
    "I dig your style",
)

COMPLIMENT_GENERIC=(
    "I like your hair",
    "lookin' good",
    "nice outfit",
    "looking sharp",
)

COMPLIMENT_WHACKY=(
    "what a splendid day it is that I should stumble upon the likes of your glorious person",
    "well aren't you a sight for sore eyes",
    "your presence is divine, like the rays of the Sun",
    "my, what a beautiful face you have",
)

PHRASE_QUIRKY=(
    "well slap me sideways and call me Sally",
    "",
)

PHRASE_WHY=(
    "well kick me in the gut and pull my intestines out from my prolapsed anus",
)

INSULT=(
    "you reek of codfish and your mother speaks Cantonese",
)

    #----------#
    # messages #
    #----------#

# Introductions -- on first meeting someone #

INTRODUCTION={
"generic" : {
    0: ("I don't care who you are. Just leave me alone.",),
    0.1:("Whoever you are, just mind your own business.",),
    0.2:("Good to meet you.",),
    0.3:("Nice to meet you. The name's {npcn}.",),
    0.4:("{npcn}. Nice to meet you.",),
    0.5:("Pleased to meet you, {pcn}. I'm {npcn}.",),
    0.6:("So very nice to meet you, {pcn}. My name is {npcn}.",),
    0.7:("I feel like we've met before.",),
    0.8:("You remind me of an old friend. I think we'll get along very well.",),
    0.9:("Oh, yes, {pcn}, I am very pleased to make your acquaintance. My name is {npcn}. I hope we will be seeing a lot more of each other.",),
    },
}

# Greetings #

REJECTION={ # conversation rejection
"generic" : {
    0  :("I'm sick of you. Go away, and don't ever come back.",
         "I hate you.",
         "Leave. Now.",
         "Piss off.",
         "*no response*",),
    0.1:("Get lost.",
         "Go away.",
         "Shut up.",
         "Stop.",
         "Stop it.",),
    0.2:("I'm busy.",
         "I'm sorry, I can't help you.",
         "I'm sorry, I'm too busy right now. Come back later.",),
    0.3:("Sorry, I've got a lot of work to do. I can't help you now.",
         "Unfortunately, I've got my hands full. Sorry.",),
    0.4:("I'd like to help you, {pcn}, but I'm very busy.",),
    0.5:("As much as I'd like to help, I'm afraid I can't right now. I'll make it up to you.",),
    0.6:("Hey, {pcn}. I wish I had time to chat, but I have to concentate. See you later.",),
    0.7:("Oh, hey, {pcn}! I'm sorry, I can't talk with you right now, but come back again sometime soon.",),
    0.8:("Hello, sweet {pcn}. I'm sorry, I have a lot of work to do at the moment.",),
    0.9:("As much as it pains me to say it, dear {pcn}, I'm too busy to talk at the moment.",),
    },
"motivated" : {
    0  :("I don't have time for you. Now or ever.",
         "No, no time. Not for you.",),
    0.1:("Nope.",),
    0.2:("Excuse me, I'm busy; please let me finish my work.",),
    0.3:("I'm sorry, {pcgg}{pcc}, I'm very busy at the moment, but come back shortly.",),
    },
"outgoing" : {
    100 : ("Forgive me. I must be going.",),
    },
"proactive" : {
    100 : ("I'm sorry, I don't talk to {slurs} like you.",),
    },
}

GREETING={ # conversation acceptance
"generic" : {
    0  :("I wish you would be quiet.",
         "Please just go away.",
         "You again? What do you want?",),
    0.1:("Yea? What?",
         "Not you again.",
         "What? What do you want from me?",),
    0.2:("Yea?",
         "Yes, {pcc}?",
         "Yes, {pcc}? What do you want?",
         "What do you want?",),
    0.3:("Mm-hmm?",
         "Yes, {pct}{pcn}?",
         "What can I do for you?",
         "Can I help you?",),
    0.4:("Yes, {pcn}?",
         "Hello.",
         "What's up?",
         "What is it, {pcn}?",
         "How can I help, {pcc}?",),
    0.5:("Hello again.",
         "Hello again, {pcn}.",
         "Hello, friend.",
         "Nice to see you again.",
         "What are you up to today?",
         "What is it, dear {pcn}?",),
    0.6:("Yes, sweet {pcn}?",
         "It's nice to see you, {pcn}.",
         "Hey {tof}, what are your plans for the weekend?",
         "Hello again {pcn}, I pray you're doing well. What's on your mind?",),
    0.7:("Great to see you again.",
         "It's always good to see you, {pcn}.",
         "Hello again, {toe}."),
    0.8:("Hello, love.",
         "Hello, darling, what can I do you for?",
         "Is there something I can do to help? Anything at all, just ask.",
         "It's great to see you again.",),
    0.9:("And for what purpose am I blessed to be in your presence?",
         "Hey {pcn}! It's so great to see you.",
         "I've missed you, {pcn}.",
         "Hello, my love.",
         "Hello again, my darling.",),
    1.0:("Hello, my dearest {pcn}.",
         "I've missed you -- you should come around more often.",
         "I've really missed you a lot.",),
    },
"proud" : {
    0  :("What is it, person who is inferior to me in every way?",
         "Just walk away, you miserable dog.",
         "Piss off, you wretched creature.",),
    0.1:("Hey, {pcc}, is it true you pissed your bed until you were eight?",
         "Horrible creature.",
         "I saw a muckrat the other day.",),
    0.2:("What do *you* want?",
         "Well if it isn't you again.",
         "I suppose I could spare a moment or two for someone less fortunate than myself.",),
    0.3:("Hey, good to see you.",
         "Hello, {pcc}. I hope you won't take up too much of my time.",
         "Have you come to bask in my glorious presence? Can't say I blame you.",),
    0.4:("Hey, {pcn}, good to see you.",
         "What can I do for you, {pcc}?",
         "It's your lucky day! It appears I've got a moment to spare for you.",),
    0.5:("I'd be glad to help.",
         "It would be my pleasure.",
         "I'm glad you're still alive.",),
    0.6:("Let me know if there's anything I can do to help. I'd be glad to do what I can.",
         "It's so good to see you. Anything I can do, just say the word.",
         "Great to see you're doing all right.",),
    0.7:("Hello {pcn}. You know, I'm proud to call you my friend. What can I do for you?",
         "What a nice thing to say. It's good to see you, friend.",),
    0.8:("Hello, my dear {pcn}. Anything you need, don't hesitate to ask.",
         "Oh, please, you're too kind.",),
    0.9:("I'm so glad to see you.",
         "Oh, it's good to see you're all right. Us upperclassmen have got to stick together.",),
    1.0:("Oh, {pcn}, how I've missed you! It's so good to see you're still in one piece.",),
    },
"low-self-esteem" : {
    0  :("Great, just what I deserved. It's you.",
         "Just when things were starting to look slightly less shitty. You show up.",),
    0.1:("Not you again. Just my luck.",
         "I may deserve every ounce of pain you're going to cause me, but I beg you, have mercy.",),
    0.2:("...Yes?",
         "Hello there.",
         "Yo.",),
    0.3:("Hi.",
         "Oh, it's you again. Hello.",
         "Whassup?",
         "Yo, whassup?",
         "'Sup?",),
    0.4:("Yo, what's hangin'.",
         "Hope you've been doin' better than I have.",
         "What's shakin'?",),
    0.5:("How've you been? Better than me, I hope.",
         "Well, they say the grass is always greener...",),
    0.6:("Hi, {pcn}!",
         "I'm glad you're doing OK.",),
    0.7:("To what do I owe the pleasure?",),
    0.8:("Hello there, {pcn}, I'm so glad to see you.",),
    0.9:("I've been looking forward to you coming to visit, {pcn}.",),
    1.0:("You're so wonderful... I don't deserve you.",),
    },
"argumentative" : {
    0  :("Hey, {slur}.",
         "Yea, I know your mother gives free handies, and like I told you before, I'm straight.",
         "Go fall in a hole and die.",
         "Not you. Anyone but you, please, for the love of God.",
         "Hello again, {slur}. It's so great to see you. Oh no, please, feel free to be an absolute fucking {slur}. Be my guest.",),
    0.1:("Looking for a fight?",
        "Hey, ...you.",
         "Whassup, {slur}.",
         "Ugh.",
         "Not you. Get lost or hit me like a {pcgg}, {slur}.",
         "Whatever you're looking for, I'm sure I don't know how to find it.",),
    0.2:("You're not the person I was hoping to see.",
         "Can I *help* you?",),
    0.3:("Hey {pcn}, you agree that socialism is the same thing as naziism, right?",
         "Yea? Can I help you?",),
    0.4:("George Hepburn is the stupidest god-damn president of all time. Try to change my mind.",
         "Wow, I still can't believe he said that. *laughs*",),
    0.5:("What do you think of the illuminati?",
         "I'm telling you, mountain stew is, bar-none, the best MRE in the history of mankind.",),
    0.6:("Where do you think we go when we die?",
         "UFOs are real. I've seen one with my own eyes. They're real. Aliens are real.",),
    0.7:("Hello my friend. Looking for a right beating in a good ol' game of fless?",
         "Oh no, not you again. *chuckles* Good to see you, you son of a bitch. How've you been?",),
    0.8:("Hey, I need you to break a tie. No matter which way you shake it, The Shobbit films are just *so* vastly much better produced than the Lord of the Kings. Right?",),
    0.9:("There's no-one I'd rather see. What's new?",),
    1.0:("There's my {pcn}. No-one could ever beat you in a fight!",),
    },
"non-confrontational" : {
    0  :("*no response*",
         "*exasperated expression*",),
    0.1:("I'd really rather you not.",
         "Could you just... not?",
         "*annoyed expression*",),
    0.2:("Hm.",
         "*sharp exhale*",
         "Well, what is it?",),
    0.3:("Yep?",
         "Yes? Do you need something?",),
    0.4:("Uh-huh?",
         "Oh, it's just you. Hello.",),
    0.5:("Hi, how are you?",),
    0.6:("*smiles*",),
    0.7:("Hello friend, lovely weather we're having.",),
    0.8:("Great to see you again. Is there anything I can do for you?",),
    0.9:("Oh, hello, sweet {pcn}. How have you been?",),
    1.0:("Will I get to see you tomorrow, {pcn}?",),
    },
"outgoing" : {
    0  :("No!!! God. No! God, please, no. No! No! Noooo!!!!!",
         "What the hell do you want?",
         "What do you want, {slur}?",
         "God, just go. Go away, and don't come back.",),
    0.1:("Make it quick or hit the road.",
         "I don't like you.",),
    0.2:("I'm sure there's someone else you can bother.",),
    0.3:("Hey, {pcn}. {Gcomp}.",
         "Yo, {tof}, what's up.",
         "Hey, buddy.",),
    0.4:("Yea, {pcc}? Do you have a question?",
         "{Gcomp}, {pcn}. What's up?",
         "What's up, {tof}?",
         "Hey, buddy!",),
    0.5:("What's happenin'?",
         "What's shakin', bacon?",
         "What's cookin', my shooken?",
         "Niiice {icomp}, {tof}.",
         "Heya, pal.",),
    0.6:("What's up, brohammer?",
         "{pcn}! Yo, I love that {icomp}!",
         "Heya, pal!",),
    0.7:("'Sup, {pcn}! Sick {icomp}!",
         "Hey there, {pcn}! {Comp}.",
         "Hey! Good on ya, {tof}!",
         "Hey, friend.",),
    0.8:("Hey, {tof}! {Comp}.",
         "What's up, {tof}? Great to see you! {Comp}.",
         "Hello, sweet {toe}. What can I do for you on this fine day?",
         "Oh, {tof}, it's good to see you! Put 'er there!",
         "Hey, friend!",),
    0.9:("I'm so glad to see you again, {pcn}! I hope you've been well. Is there anything I can do for you? Anything at all?",
         "Friend!",),
    1.0:("Oh, my dear {pcn}, how are you?",
         "Oh! {pcn}, what a surprise! I'm so happy to see you. How have you been?",),
    },
"shy" : {
    0  :("Um... so, I would appreciate it if you would leave.",),
    0.1:("Oh, hello...",),
    0.2:("Hi, {pcn}.",
         "Hello, {pcn}.",
         "Hello...",
         "Yea.",),
    0.3:("Hello {pcn}.",
         "Hello.",
         "Yea?",),
    0.4:("Hi, {pcn}!",
         "Oh! Hi, {pcn}.",
         "Yes.",),
    0.5:("*smiles*",
         "Yes?",),
    0.6:("Uh! Well, it's...! Oh, nevermind.",
         "*grins*",
         "Mm-hmm.",),
    0.7:("Mm-hmm...?",
         "Nice to see you!",),
    0.8:("Mm-hmm!",
         "Hello!",
         "Hi again!",),
    0.9:("Hey, {pcn}. How are you doing? I've missed you! *hugs*",
         "*glances at you coyly*",),
    1.0:("Hello, {toe}! I love you! *hugs*",
         "*smiles coyly*",),
    },
"independent" : {
    0  :("I don't want whatever you're selling.",
         "Just leave me and my family alone.",
         "Whatever you're after, leave me out of it.",),
    0.1:("I'm fine, thanks.",
         "Hey?",
         "*silently looks you in the eyes*",),
    0.2:("Hey, there, {pcc}.",
         "Hey, you.",),
    0.3:("No, thank you. Oh -- it's just you; I thought you were a vendor. *shudders*",),
    0.4:("Hello, {pcn}. {Gcomp}.",),
    0.5:("Hello you.",),
    0.6:("Hi {pcn}!",
         "Hi!",),
    0.7:("Hey, you!",),
    0.8:("Hey you!",),
    0.9:("Hey you! *smiles*",
         "How are you! *smiles*",),
    1.0:("Hey, you! *grins*",
         "*cute smile*",
         "Dear {toe}, how have you been?",),
    },
"codependent" : {
    0  :("I don't want you. I don't need you. Just get out of my life.",
         "Go away, and don't ever come back.",),
    0.1:("You again? What is it this time?",),
    0.2:("Hey there, {pcgp} {pcc}.",),
    0.3:("Hey, {pcn}. What's up?",),
    0.4:("Maybe we can help each other.",),
    0.5:("I'm looking forward to dealing more with you in the future.",
         "Can I help?"),
    0.6:("What do you need?",
         "Yes, dear {pcn}? What can I do for you?",),
    0.7:("Dear {pcn}, is there something I can do for you?",
         "Hello, my sweet {pcn}, how can I serve you?",
         "It's always good to see you, dear {pcn}. What do you need?",),
    0.8:("Hello {toe}, {comp}. What's new?",
         "{Gcomp}, {pcn}! Need something?",
         "Sweet {pcn}, can I help with something?",),
    0.9:("Oh, dearest {pcn}! {Wcomp}.",
         "How can I assist you my love?",
         "Hey, {pcn}! Boy, do I have a lot to tell you!",),
    1.0:("Lovely {pcn}, {wcomp}.",
         "*big smile*",
         "Hello best friend!",
         "How are you my {toe}?",),
    },
"bubbly" : {
    0  :("Just get it over with, {slur}!",
         "Hey, {slur}! {Gcomp}.",
         "Oh, hi, {slur}. I always love when you come, because I get to look forward to you leaving.",
         "Ooh, I love that {icomp}. It really highlights what a {slur} you are.",),
    0.1:("Sorry, but not sorry.",
         "Gross. It's {pcn}.",
         "Ew.",),
    0.2:("Hey, it's {pcn} again!",),
    0.3:("Hey again!",
         "Hey, {gcomp}, {pcgg}."),
    0.4:("Hello again {pcn}! Good {tod}.",
         "Hey {pcn}, {gcomp}.",),
    0.5:("Hey there! *punches you in the arm*",
         "Hi!!",
         "Hey! Nice {icomp}.",),
    0.6:("Well, hi again, {pcn}. So nice to see you.",
         "Yo! *high-fives*",
         "Hi, {pcn}! I love that {icomp}!",),
    0.7:("Heya! *does a little dance*",
         "Yao! {pcn}! Did I ever tell you {comp}?",),
    0.8:("Squee! It's {pcn}...! *smiles*",
         "Well if it isn't my {toe}, {pcn}. Don't hesitate to ask if there's anything I can do for you.",),
    0.9:("Hey!! Guess what? I love you!",
         "*freaks out in excited delight*",
         "Wow! That {icomp} looks so good on you! *hugs*",),
    1.0:("*big smile*",
         "Aw, {pcn}! How lucky can I be?",
         "It's {pcn}!! {Comp}. I can't get over it.",
         "Hey! *smiles, hugs*",),
    },
"low-energy" : {
    0  :("*long, exasperated sigh*",
         "Eat shit, {slur}.",),
    0.1:("They don't pay me enough to deal with {slur}s like you.",),
    0.2:("Oh. It's only you. What?",),
    0.3:("Yea? Something you need?",),
    0.4:("Hm? What is it?",
         "Warm day to you.",),
    0.5:("Hey. Good to see you.",
         "Warm day to you, friend.",),
    0.6:("Hey, how are you doin'?",
         "Live long and prosper.",),
    0.7:("What's goin' on?",
         "Heeeeyyy.",),
    0.8:("Yo, good to see you!",
         "*smiles with love*",),
    0.9:("Hi there, how are you doing?",
         "Love. *hugs*",),
    1.0:("Hey... How are you?",
         "*hugs*",),
    },
"motivated" : {
    0  :("What could possibly be worth my time, coming from a {slur} like you?",
         "Suck my dick, you fuckhead.",),
    0.1:("What do you want? I'm very busy.",
         "Just one more, and make it quick.",),
    0.2:("Yes? If it's nothing important, I'll be going now.",
         "What is it now?",),
    0.3:("Good {tod}.",
         "Yes, {pcgp}? Make it quick, I'm very busy.",
         "Is there something I can do for you? If not, please leave me to my work.",
         "Yes, {pcn}. {Gcomp}.",),
    0.4:("Good day, {pcgp}.",
         "Hello, {pcn}. {Gcomp}.",),
    0.5:("Good day, {pcgp}!",
         "Good {tod}. {Comp}.",),
    0.6:("Great {pcgp}, what can I do for you?"
         "Hello again, great {pcgp}!",
         "Great {pcgp}. So wonderful to see you.",),
    0.7:("Great {pcgp}, it is wonderful to see you again. I'd quite like to do so more often, but I'm afraid time is not on my side, you see.",
         "Hello, {pcn}. {Comp}.",
         "Well, {pcn}! I can always make time for you. What can I do you for?",),
    0.8:("Hello, {pcn}. {Wcomp}.",
         "{pcn}! So great to see you! {Gcomp}, as always!",
         "Salutations, {toe}.",),
    0.9:("Hello, beautiful.",
         "You're looking wonderful this {tod}.",),
    1.0:("I'm very glad to see you, {toe}. *hugs*",
         "{pcn}! I've missed you. *hugs*",),
    },
"unmotivated" : {
    0  :("Oof. Not you again.",
         "*sighs*",),
    0.1:("Ooohh... *groans*",
         "*sighs* Yea?",),
    0.2:("I don't have the energy for you today.",),
    0.3:("Hey.",
         "'Sup.",
         "*nods head in greeting*",),
    0.4:("Well if it isn't {pcn}.",
         "*raises head in greeting*",),
    0.5:("Hi, trusted {pcn}.",
         "*smiles slightly*",
         "Hey-yo.",),
    0.6:("*singing badly* What's goin' on?",
         "All-right.",),
    0.7:("*finger guns*",
         "All-right!",),
    0.8:("Hey there, {pcn}. I'm glad you're all right.",
         "*singing badly* Hello, hello! I don't know why you say goodbye, I say hello.",
         "Arright!",),
    0.9:("Well it's very nice to see you, {pcn}.",
         "Arrigght!!",),
    1.0:("Hello, {toe}.",
         "{Toe}, hello again.",),
    },
"relaxed" : {
    0  :("Listen, you need to leave me alone.",
         "Listen, {slur}. You're ruining my {tod}.",
         "You are scum.",
         "God have mercy.",
         "{Slur}.",),
    0.1:("Dang, what a drag.",
         "Oh. {pcn}. I thought it was something important. *picks nose*",
         "Not you.",
         "I fart in your general direction.",),
    0.2:("Huh. Oh, it's only {pcn} again. Yea?",
         "Mm-hmm? What is it now, {pcc}?",
         "Oh. You.",),
    0.3:("Uh-huh? What is it?",
         "Oh, hey {pcn}. What's up?",
         "Oh, it's {pcn}.",),
    0.4:("Heyy.",
         "Hey, {pcgg}. What's hangin'? I mean -- how's it hangin'?",),
    0.5:("Yo, {pcn}. {Gcomp}.",
         "Dude, you're never going to believe this, but I saw a UFO the other day.",),
    0.6:("Hey, {pcn}. Good to see you, {pcgg}. What have you been up to?",
         "I promise you there are aliens out there, somewhere. It's just logical. I mean, think about it. Space is so vast, and there are so many planets with the necessary conditions for life.",),
    0.7:("Aw, yea. It's my friend, {pcn}.",
         "Yo, {pcgg}. You want a beer?",
         "What's up, {pcgg}? You feelin' cool?",),
    0.8:("'Eyyy, how've you been, {pcgg}?",
         "Hey! So good to see you! *hugs*",),
    0.9:("{pcn}! Just the person I was hoping to see.",
         "Hello again, {toe}. *hugs*",
         "Hey, {pcn}. *smiles*",),
    1.0:("Heyyyy... how's it goin', my {toe}?",
         "Friend...! How nice you could come by. *hugs*",
         "*small but sincere smile*",),
    },
"uptight" : {
    0  :("God will punish you.",
         "Jesus help you.",
         "Burn in hell, you wretched cur.",
         "You are the worst type of person.",
         "Yea, I know, you're a {slur}; everybody already knows, so you can just go home now. Bye.",),
    0.1:("Nobody likes you; nobody needs you.",
         "What is it? Can't you go bother someone else?",
         "I don't have the time nor the energy for you right now, {pcn}.",
         "I don't care for you. I don't know why I should help you, except that I'm just a saint.",),
    0.2:("Hmm. What is it? I do hope it will be quick.",
         "Yes, {pcc}?",
         "What is it, {pcgg}?",
         "Yes, {pct}{pcn}?",),
    0.3:("Yes, {pct}{pcn}? Is there something you need?",
         "Great {pcgp}.",
         "Oh, {pcn}. How are you.",),
    0.4:("What do you need?",
         "Great {pcgp}, are you in need of my assistance?",),
    0.5:("Greetings!",
         "Bonjour, great {pcgp}.",
         "A pleasure.",
         "Hello, {pcn}. So nice to see you on this fine {tod}.",),
    0.6:("Salutations.",
         "Greetings and salutations!",
         "An honor to be sure.",),
    0.7:("I am most honored, {pcn}. Please, the pleasure is mine.",
         "A pleasure to serve you.",),
    0.8:("How very nice to see you. I do hope that everything is all right.",
         "Most excellent.",),
    0.9:("Dear {pcn}, what a lovely encounter.",
         "Hello, {toe}. What brings you this way on this fine {tod}?",),
    1.0:("Hello, my lovely {pcn}. It's so wonderful to see you. {Comp}.",
         "Oh, hi, sweet {toe}. What a lovely visit. You can stay as long as you like.",
         "Oh, please, stay a while. I do ever so love when you come to visit.",),
    },
"proactive" : {
    0  :("People like you are the reason this country has gone to shit.",
         "Go back to kissing the president's ass, ass-kisser.",
         "I don't have time for anything else from you.",
         "You're a piece of shit human being.",
         "I'm sorry you had a shitty childhood, {pcgg}, but that's no excuse for being a complete {slur} all the time.",),
    0.1:("What gives you the right?",
         "What the hell is it now?",
         "Yes? I'm busy.",),
    0.2:("What is it, {pct}{pcn}?",
         "Mmm?",
         "Got something for me?",),
    0.3:("Mm? What is it, {pcn}?",
         "Oh, {pcn}. How are you this {tod}?",
         "Learn anything new?",),
    0.4:("What's goin' on? Any news?",
         "Hey {pcn}! What's new?",
         "Got anything new for me?",),
    0.5:("Hey, {pcgg}. Anything new?",
         "What's the news?",),
    0.6:("Hey, friend! How've you been lately?",
         "Hey {pcn}, what's new with you?",),
    0.7:("Hello, {toe}. Heard anything interesting lately?",
         "What's going on, {pcn}? *high fives*",),
    0.8:("Yo, {pcn}! I love your {icomp}. Where did you get it?",
         "What's new, {toe}?",
         "Hey there, {pcn}, what's the news?",),
    0.9:("Any news, {toe}? No? You just came to chat? That's OK. I've got time.",
         "Yay, it's my friend, {pcn}! *hugs*",),
    1.0:("Hi!! *hugs*",
         "It's so good to see you again, {pcn}! What have you been up to lately?",),
    },
"apathetic" : {
    0  :("*scowls in digust*",
         "*gives you the finger*",
         "Eat dogshit!",
         "What the fuck do you want?",
         "Fuck you.",),
    0.1:("What? What?",
         "What do *you* want? *scowls*",
         "What?",
         "*glances at you, then looks away*",),
    0.2:("Huh?",
         "Yea?",
         "Uh-huh?",
         "Yep?",),
    0.3:("Yea, {pcn}?",
         "Hey, {pcn}.",
         "Hey.",),
    0.4:("Yes?",
         "What is it?",
         "Hello.",),
    0.5:("Hey!",
         "Hello, {pcn}.",
         "'Sup, {pcgg}?",),
    0.6:("Hello!",
         "Hello, {pcn}!",
         "Hey, {pcn}!",
         "Yo, what's up?",
         "Hey, {pcgg}. What's going on?",),
    0.7:("Hey. Anything new?",
         "Hello, there.",
         "Hi. *smiles*",),
    0.8:("Hi, {pcn}!",
         "Hello! *smiles*",),
    0.9:("Heya, {pcn}. Good to see you.",
         "Yo, what's up, {pcgg}? *fist bumps*",),
    1.0:("Heya, {pcn}! Good to see you.",
         "How've you been?",
         "*fist bumps*",),
    },
}


    #------------#
    # Persuasion #
    #------------#

# small talk -- idle chit-chat between two people, generally acquaintances rather than close friends #

SMALLTALK_SUCCESS={ # could work differently than other messages:
            # all options are always available as long as you have >= the disposition requirement
"generic" : {
    0  :("That was strange.",
         "Oh, yeah. Right. That's good.",),
    0.1:("Yes, it's not bad.",
         "Good. And you?",),
    0.2:("MREs used to be a lot better.",
         "We live in strange times.",
         "Arright.",),
    0.3:("Nice weather we're having.",
         "I'm doing well, thanks. And you?",
         "Cool.",),
    0.4:("Water keeps getting more and more expensive.",
         "That's weird, I thought I left it right here...",
         "Great.",),
    0.5:("This is going to be a bad year for crops.",
         "Oh, good to hear.",),
    0.6:("It's a good day today.",
         "I didn't know that, that is something.",),
    0.7:("What a lovely day it's turned out to be.",
         "The weather's been feeling better these days, hm?",),
    0.8:("It's shaping up to be a wonderful {tod}.",
         "Well, that's very interesting.",),
    0.9:("I'm glad you came to chat. I've been looking forward to it.",
         "That's great to hear. I'm doing well, thank you.",),
    1.0:("Oh, I do enjoy our conversations. Please stay a while.",
         "So nice to hear it, {toe}. I've been doing well.",
         "Thanks for the update, {toe}.",
         "Oh, how nice.",),
    },
"proud" : {
    0  :("Reeeally.",),
    0.2:("Yes, I'm fine. Thanks.",
         "Yes, I'm doing very well. Thanks for your concern.",),
    0.4:("Good to hear. Yes, I'm doing well, as always.",),
    0.6:("Look at this picture of my dog. Isn't {she} so precious?",),
    0.8:("Look at this picture of my daughter. Isn't she so precious?",
         "Look at this picture of my newborn son. Isn't he so precious?",),
    1.0:("Look at this picture of my family. Aren't they just so precious?",),
    },
"low-self-esteem" : {
    0  :("Shitty day as usual.",),
    0.2:("Another day another nickel.",),
    0.4:("Yep, shitty weather as always.",),
    0.6:("I've been through the ringer this year, but I'm feeling a little better lately.",),
    0.8:("Shitty day. I'm feeling all right now, though.",),
    1.0:("I'm feeling a lot better now that you're here.",),
    },
"argumentative" : {
    0.2:("Nah, it's definitely the complete opposite. But you have a right to your wrong opinion.",),
    0.4:("Oh no way. No way. *laughs*",),
    0.6:("I disagree, but that's an interesting opinion.",),
    0.8:("Yeah, today is all right, but you should have seen yesterday.",),         
    },
"non-confrontational" : {
    0  :("Ah..",
         "Yeah, that's right, all right.",),
    0.2:("Oh... I see, I see.",
         "Oh, for sure.",),
    0.4:("Hm... Interesting...",
         "Oh, absolutely.",
         "Indeed.",),
    0.6:("Indubitably.",),
    0.8:("You're absolutely right about that, {pcgg}.",),
    },
"outgoing" : {
    0.2:("Huh! That's something, all right.",),
    0.4:("Yes, I agree. It is nice.",
         "Oh yeah, I am excited about it.",),
    0.6:("Oh, how nice to hear, {pcn}.",),
    },
"shy" : {
    0  :("Oh, OK...",),
    0.2:("Oh, that's... nice.",),
    0.6:("I do enjoy the rain.",),
    1.0:("Yesterday I saw a deer.",),
    },
"independent" : {
    0.8:("",),
    },
"codependent" : {
    0.8:("",),
    },
"bubbly" : {
    0.8:("",),
    },
"low-energy" : {
    0.4:("Lovely weather.",),
    0.6:("Indeed, {pcn}.",),
    0.8:("",),
    },
"motivated" : {
    0.2:("I'm hype.",),
    0.4:("Corn stocks are *still* dropping. Can you believe it?",),
    0.6:("This is going to be a good decade for entrepreneurs.",),
    0.8:("I might be on to something.",),
    },
"unmotivated" : {
    0.8:("",),
    },
"relaxed" : {
    0.8:("",),
    },
"uptight" : {
    0.8:("",),
    },
"proactive" : {
    0.4:("Well, more and more rivers are running dry these days. It's because the mega-corporations keep building more and more dams. It's terrible.",),
    0.6:("That's good news.",),
    },
"apathetic" : {
    0.8:("",),
    },
}

SMALLTALK_FAILURE={
"generic" : {
    0  :("I don't want to talk to you.",
         "You're bothering me.",),
    0.2:("Let's just be quiet for a while.",
         "Ok.",),
    0.3:("Oh. Yea.",
         "Ah, hm.",),
    0.4:("Mm...hm.",
         "Ah. I see.",),
    0.6:("Oh. Wow.",
         "Hmmm. Is that right.",),
    0.8:("Huh. That's pretty cool.",),
    1.0:("Oh, that's super interesting.",),
    },
"argumentative" : {
    0  :("Who gives a shit?",),
    0.2:("No. Wrong.",),
    0.4:("No disrespect, but that's demonstrably false.",),
    0.6:("That's... not quite right.",
         "Aliens are definitely real, {pcgg}.",),
    0.8:("",),
    },
"motivated" : {
    0  :("Shoo, fly.",
         "Shoo, fly, before I swat you.",
         "Shoo, shoo.",),
    0.2:("Who's got the time for that?",),
    },
"proactive" : {
    0.2:("Well, it'd be much nicer of a day if our own government didn't poison our air with mind-control gas.",),
    0.4:("",),
    },
}

# gossip -- like small talk, but slightly more intense and friendly #

GOSSIP_SUCCESS={
"generic" : {
    0  :("Ha. That's a good one.",
         "I'll remember that.",),
    0.2:("Mm, is that so?",
         "Well, that's pretty interesting.",),
    0.4:("Huh. Very interesting.",
         "Wow, I didn't know that.",),
    0.6:("Oh, really? *laughs*",
         "Ooh, that's juicy.",),
    0.8:("Oh my God, you're kidding!",
         "Oh, no...",),
    1.0:("What? She did what?!",),
    },
"uptight" : {
    0.2:("What has this country come to?",),
    0.4:("Well, I can't say I'm surprised.",),
    },
}

GOSSIP_FAILURE={
"generic" : {
    0  :("Everybody already knows that, {slur}.",
         "Who gives a damn?",),
    0.2:("Nobody cares, {pcn}.",
         "That's none of my concern, nor yours for that matter.",),
    0.4:("What are you talking about?",
         "That's disgusting!",
         "Oh, {pcgg}, I heard an even better one just the other {tod}.",),
    0.6:("Wow. I didn't know you would stoop so low.",
         "Gross, {pcn}.",
         "That's nobody's business but their own.",),
    0.8:("You should just mind your own business.",
         "Oh, sorry, I don't like to talk about people behind their backs.",),
    },
"proactive" : {
    0  :("You ape.",
         "Barbarian.",),
    0.2:("What two grown men do in their own home is none of your business!",
         "I don't wanna hear about that. Not from you, anyway.",),
    0.4:("Oh, {pcgg}. That's just messed up.",),
    0.6:("How... how do you even know about that?",),
    0.8:("That's my sister you're talking about, {pcgg}.",),
    },
"relaxed" : {
    0.2:("Just keep your nose out of other people's shit!",),
    },
}

# ask question -- try to gain information about location, entity, entity class, etc. #

QUESTION_SUCCESS={
"generic" : {
    0  :("Fine, I'll tell you, {slur}.",),
    0.2:("I guess it wouldn't hurt to tell you.",),
    0.4:("OK, I'll tell you just this once.",),
    0.6:("No problem, I'd be glad to answer any questions you have.",),
    0.8:("Any more questions? Ask away.",),
    1.0:("Anything else, dear {pcn}?",),
    },
}

QUESTION_FAILURE={
"generic" : {
    0  :("Why on earth should I tell you that?",
         "I'll never tell, you {slur}.",
         "Give it up.",),
    0.2:("I'm not going to tell you that.",
         "Sorry, I can't tell you that.",),
    0.4:("Sorry, that's really not my place to say.",
         "I'm afraid I don't know the answer.",),
    0.6:("No, I can't tell you. I'm sorry.",),
    0.8:("I'm sorry, {pcn}. It's just something I can't say.",),
    1.0:("I'm terribly sorry, {toe}. I promised I wouldn't tell.",),
    },
}

# interrogate -- like questioning but more intense, more serious #

INTERROGATE_SUCCESS={
"generic" : {
    0  :("Fine! Fine! I'll sing!",),
    0.2:("All right, you got me.",),
    0.4:("I'll tell you whatever you need to know.",),
    0.6:("I'll tell you. You don't need to make such a big deal about it.",),
    0.8:("Calm down, {pcgg}. I'll answer your questions.",),
    1.0:("Oh, {pcn}, I wish you would ask nicely.",),
    },
}

INTERROGATE_FAILURE={
"generic" : {
    0  :("I'll never tell you in a million years.",
         "Get fucked.",
         "*spits on you*",),
    0.2:("No, I'm not gonna talk.",
         "You're gonna have to do a lot better than that.",),
    0.4:("Forget it, {pcc}.",
         "No, it's not going to happen.",),
    0.6:("I won't spill it.",),
    0.8:("I'm sorry, I just can't.",),
    1.0:("You're making me upset, {pcn}. Just calm down and let's think about this rationally.",),
    },
}

# torture -- threaten pain to get information or get them to do what you want #

TORTURE_SUCCESS={
"generic" : {
    0  :("*crying* Fine... I'll tell you. Just please, stop. I can't take it anymore.",
         "I'll tell you everything. Just don't hurt my family.",),
    0.2:("Yes! OK! I'll tell you, just promise you'll leave me alone if I do!",),
    0.4:("I can't believe you'd go to such measures. I'll tell you. Just stop.",),
    0.6:("I'll tell! I'll tell! Christ!",),
    0.8:("I can't take it anymore. Whatever you need me to do, I'll do it.",),
    },
}

TORTURE_FAILURE={
"generic" : {
    0  :("*sobbing* I don't know.",
         "Just please, stop.",
         "I can't take it.",
         "I think my heart is going to give out.",),
    0.2:("Never. I'll never tell.",
         "I'm not going to rat my friends out.",),
    0.4:("I can't tell you, so just give up.",
         "No. I won't tell you; not now or ever.",),
    0.6:("Why would you do this?",),
    0.8:("How could you do this to me?",),
    },
"motivated" : {
    0  :("You'll give out before I do.",),
    },
}

# ask favor -- ask someone to do something for you #

ASKFAVOR_SUCCESS={
"generic" : {
    0  :("I'll do it. But then I don't ever want to see you again.",),
    0.1:("This is the last time I'll ever help you.",),
    0.2:("Don't make me regret helping you.",
         "OK, but I'm not happy about it.",),
    0.3:("OK, I'll do it.",
         "Fine.",),
    0.4:("All right.",
         "Sure.",
         "Yep.",),
    0.5:("Sure, that's fine.",
         "Yes, I can do that.",),
    0.6:("OK, friend.",),
    0.7:("Yes.",),
    0.8:("I'll get it done right away.",),
    0.9:("That'll be easy.",),
    1.0:("I'll do it as soon as I can.",),
    },
"proud" : {
    0.2:("Don't make me regret taking pity on you.",),
    },
"unmotivated" : {
    0  :("What a drag.",),
    0.2:("Ugh, fine. Hold on...",),
    0.4:("Fine...",),
    },
"relaxed" : {
    0.2:("Eh, all right. Give me a second.",),
    0.4:("Yeah, no problem.",
         "Yeah.",),
    },
"bubbly" : {
    0.6:("Absofruitly.",),
    },
         
}

ASKFAVOR_FAILURE={
"generic" : {
    0  :("No. I won't do that.",
         "Not for you. Get lost.",),
    0.1:("Why would I do that for you?",
         "Come again? Who are you now?",),
    0.2:("You want me to do what?",),
    0.3:("No, I'm not going to do that for you.",
         "No. Sorry, but that's kind of innappropriate of you.",),
    0.4:("No, I won't do that.",
         "Sorry, that's something I'm not going to do.",),
    0.5:("Sorry, I can't do that for you.",),
    0.6:("No, sorry, {pcn}.",),
    0.7:("Oh, I'm sorry, I can't help you with that, {pcn}.",),
    0.8:("Oh, I can't. I'm really sorry...",
         "For my own sake, I can't help you with that.",),
    0.9:("Well I would love to help, but I really can't. Please forgive me.",
         "I care deeply for you, {pcn}, but I can't do that for you.",),
    1.0:("I don't think you could ever get me to do that, no matter what you did.",
         "I'm truly sorry, {pcn}. I can't.",),
    },
}

# beg -- like asking favor, but much more intense and needy #

BEG_SUCCESS={
"generic" : {
    0  :("Oh, what a pitiful creature. Get yourself some clean clothes.",),
    0.1:("*hands you a gift, avoiding eye contact*",),
    0.2:("Very well, you poor thing.",),
    0.3:("All right, I can see you are in desperate need.",),
    0.4:("OK, then. I can tell you're really out and out.",),
    0.5:("Damn, {pcgg}, you've had a rough {tod}, haven't you?",),
    0.6:("All right, all right. It's not a big deal.",),
    0.7:("Yes, I'll lend you a hand, {pcn}.",),
    0.8:("Yes, {pcn}, I can help you out.",),
    0.9:("OK, I'll do what I can.",),
    1.0:("Very well, dear {toe}.",),
    },
"motivated" : {
    0.5:("Sure, I can give you a loan if you need it.",),
    },
"codependent" : {
    0.5:("Hey, hey. You didn't have to beg.",),
    },
}

BEG_FAILURE={
"generic" : {
    0  :("Absolutely not.",),
    0.1:("No.",),
    0.2:("Sorry, no.",),
    0.3:("Sorry.",),
    0.4:("I can't, sorry.",),
    0.5:("Sorry, {pcgg}.",),
    0.6:("I'm afraid I can't swing it.",),
    0.7:("No, I can't do that, sorry, {pcn}. I pray you'll get through this.",),
    0.8:("I have faith that you can get out of this yourself.",),
    0.9:("I can't, {pcn}. I care about you, but I can't give you that.",),
    1.0:("I'm really sorry.",),
    },
"independent" : {
    0  :("Ugh, how very pathetic.",),
    0.2:("Get your own.",
         "Why? So you can buy another hit of morphine off the street?",),
    0.4:("I worked hard for this! I'm not just going to give it to you.",),
    },
"proud" : {
    0  :("Pitiful. Just pitiful.",),
    0.2:("Poor cretin, what a terrible hand the world has dealt you.",),
    0.4:("How sad, that you would stoop to begging.",),
    },
"uptight" : {
    0  :("Oh, how incredibly sad. Look at {pcgo}.",),
    0.2:("I will pray for you.",),
    0.4:("I pray your situation improves, {pcn}.",),
    0.6:("It pains me to say it, but I have to decline.",),
    },
}

# barter -- buy / sell / trade / ask for gift #

BARTER_SUCCESS={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

BARTER_FAILURE={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

# charm -- temporarily increase disposition #

CHARM_SUCCESS={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

CHARM_FAILURE={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

# boast -- temporarily increase disposition #

BOAST_SUCCESS={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

BOAST_FAILURE={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

# bribe -- offer a gift in exchange for improved disposition #

BRIBERY_SUCCESS={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

BRIBERY_FAILURE={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

# intimidate -- scare using IDN stat to raise disposition,
# but also gives the Mistreated component,
#   which makes them quick to turn on you if given the opportunity.

INTIMIDATION_SUCCESS={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

INTIMIDATION_FAILURE={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

# debate -- argue; talk about something possibly intense to try and raise disposition #

DEBATE_SUCCESS={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

DEBATE_FAILURE={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

# pester -- annoy someone in an effort to make them mad or dislike you #

PESTER_SUCCESS={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

PESTER_FAILURE={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

# taunt -- try to make them really mad so they will fight you #

TAUNT_SUCCESS={
"generic" : {
    0  :("Let's take this outside.",
         "I'll make you regret this!",
         "Do you want to die, {slur}?",
         "{Slur}!",),
    0.2:("You {slur}!",),
    0.4:("If you're looking for a fight, you've found one.",),
    0.6:("Sure, I'll kick your ass for you.",),
    0.8:("You're asking for it.",),
    },
"proud" : {
    0:  ("Die!",),
    0.2:("That's it. I'm gonna knock your teeth in.",),
    },
"low-self-esteem" : {
    0.2:("",),
    },
"argumentative" : {
    0  :("I'll kill you!",),
    0.2:("I'll teach you a lesson you won't forget, little kid.",),
    0.4:("I'm going to kick your ass.",),
    },
"non-confrontational" : {
    0.2:("I'm not going to enjoy kicking your ass.",),
    0.4:("I take no pleasure in this.",),
    0.6:("*sighs* you total {nc}.",),
    },
"outgoing" : {
    0.2:("Let's go. You ready, {slur}?",),
    },
"shy" : {
    0  :("*quietly enters a combat stance*",),
    },
"independent" : {
    0  :("Argh! That's it, I'm going to destroy you!",),
    },
"codependent" : {
    0.2:("So, you want a fight, huh? I'll abide.",),
    },
"bubbly" : {
    0.2:("*grinding teeth* You're going to raise my blood pressure!",),
    0.4:("Aghh! You {slur}!",),
    0.6:("I'm so going to hurt you!",),
    },
"low-energy" : {
    0.2:("",),
    },
"motivated" : {
    0  :("You've crossed the line, {pcgp}.",),
    0.2:("I'll kick you in time to resume my studies!",),
    0.4:("I'm always ready for a friendly tussle, my great {pcgp}. *unrolling sleeves gesture*",),
    },
"unmotivated" : {
    0.2:("",),
    },
"relaxed" : {
    0  :("*sighs, enters combat stance* All right, let's make this quick.",),
    0.2:("That's the line, {pcgg}.",),
    0.4:("",),
    },
"uptight" : {
    0  :("All right then. Have at you, {slur}!",),
    0.2:("Well then, great {pcgp}, prepare yourself!",),
    0.4:("I'll not pull my punches!",),
    0.6:("By jove, you've gone mad. I'll knock some sense into you.",),
    },
"proactive" : {
    0.2:("",),
    },
"apathetic" : {
    0.2:("",),
    },
}

TAUNT_FAILURE={
"generic" : {
    0  :("What a {slur}.",
         "*ignoring you*",),
    0.2:("Stop it. Now.",
         "Please stop.",),
    0.4:("*annoyed expression*",
         "Ugh. Leave me alone, {pcgg}.",
         "Stop it!",),
    0.6:("Leave me alone, {pcn}.",
         "Quit it!",),
    0.8:("Quit, {pcn}!",
         "*angry expression*",
         "Why are you like this?",),
    },
"proud" : {
    0  :("*laughs* Wow, you're such a {nc}.",
         "*scoffs*",),
    0.2:("*laughs* Look at you. {Nc}.",),
    0.4:("You're embarassing yourself.",),
    },
"low-self-esteem" : {
    0  :("Thanks for making my {tod} even worse.",
         "{Slur}.",),
    0.2:("You're mean.",
         "I know you are but what am I?",),
    0.4:("I know, but you don't have to be such a {slur} about it.",),
    },
"argumentative" : {
    0  :("Are you running for the biggest {slur} of the year award? You've got my vote.",),
    },
"non-confrontational" : {
    0  :("*ignoring you agressively*",),
    },
"outgoing" : {
    0  :("Piss off.",),
    0.2:("",),
    },
"shy" : {
    0.2:("",),
    },
"independent" : {
    0.2:("",),
    },
"codependent" : {
    0.2:("",),
    },
"bubbly" : {
    0.2:("",),
    },
"low-energy" : {
    0.2:("",),
    },
"motivated" : {
    0.2:("",),
    },
"unmotivated" : {
    0.2:("",),
    },
"relaxed" : {
    0.2:("",),
    },
"uptight" : {
    0  :("Buzz off, bothersome pest.",),
    0.2:("Do you kiss your mother with that mouth?",),
    },
"proactive" : {
    0.2:("",),
    },
"apathetic" : {
    0.2:("",),
    },
}

_={
"generic" : {
    0  :("",),
    0.1:("",),
    0.2:("",),
    0.3:("",),
    0.4:("",),
    0.5:("",),
    0.6:("",),
    0.7:("",),
    0.8:("",),
    0.9:("",),
    1.0:("",),
    },
}

# Flattery -- admiring, complimenting, etc. #

FLATTERY_SUCCESS={
"generic" : {
    0  :("Thanks.",
         "Mm-hm.",
         "Yep.",),
    0.1:("You're too kind.",
         "Thanks, {pct}",
         "That's nice.",),
    0.2:("Thanks, that's really nice.",
         "Thank you, {pcc}.",
         "Thank you.",
         "Thanks.",),
    0.3:("Well, thanks!",
         "How nice.",
         "Thanks!",),
    0.4:("Why, thank you!",
         "That's so nice, thanks.",
         "How nice! Thanks.",
         "Thank you.",),
    0.5:("You're such a sweetheart.",
         "That's very nice.",
         "Thanks, that means a lot.",
         "Oh, thank you! How very nice.",
         "Thank you!",),
    0.6:("Oh, I'm glad you think so.",
         "How nice. Thank you, {pcn}.",
         "Yes, I worked hard on it. Thanks for noticing.",),
    0.7:("Thanks, {toe}.",
         "Wow, thanks, {pcn}! You're looking good, too!",
         "I'm glad you think so.",),
    0.8:("What a wonderful compliment. Thank you, {pcn}.",
         "Thank you, my dear {pcn}.",
         "Thanks, {toe}. You're too kind.",),
    0.9:("Aw, thanks, {toe}!",
         "That's wonderful. Thank you, sweet {pcn}.",),
    1.0:("That means so much coming from you. Thank you, dearest {pcn}.",
         "I'm so happy you like it.",),
    },
"proud" : {
    0.2:("Well, it's about time someone noticed.",),
    },
"low-self-esteem" : {
    0  :("Are you my own personal hell manifest?",),
    0.1:("Yea, right. Don't make me laugh...",),
    0.2:("That's not true. But thank you.",),
    0.3:("No, I'm not that great. Thanks anyway.",
         "Oh, please. Give me a break.",),
    0.4:("Stop, you're exaggerating.",
         "No, really -- you're too much.",),
    0.5:("No, I don't deserve that praise. But thanks.",
         "Really, you're too much.",),
    0.6:("*weak smile*",
         "Thanks...",),
    0.7:("*starts, then pauses* Oh... thanks.",
         "It's too much, {pcn}. Thanks for the thought, though.",),
    0.8:("Thanks, that means a lot coming from you.",
         "I'm glad you like it!",),
    0.9:("I'm really glad you see it that way. I just wish I felt the same way about it.",),
    1.0:("What a lovely thing to say.",
         "Oh, thank you, {pcn}. Thanks so much.",),
    },
"motivated" : {
    0  :("Coming from you, that means nothing.",),
    0.1:("Yes, you're right. I am fabulous.",),
    },
}

FLATTERY_FAILURE={
"generic" : {
    0  :("Just quit it.",
          "*scowl*",
          "Ugh!",
          "Enough!",
          "I've had enough! Get lost!",),
    0.1:("Cool.",
          "Good for you.",
          "I don't care.",
          "*raises, then lowers eyebrows*",
          "Enough.",
          "Uh...",
          "I don't want to hear that from you.",),
    0.2:("Thanks but I don't need to hear that coming from you.",
          "*false smile*",
          "Ok, that's enough.",
          "I don't need to hear that from you.",),
    0.3:("Well, that's nice of you.",
          "Oh... thanks.",
          "Stop. You're too much, really.",
          "*grimaces*",
          "That's enough, now.",),
    0.4:("*frowns*",
          "Oh. Well, I can't say I agree with you on that one.",
          "I know you mean well, but now you're making me uncomfortable.",
          "Ok, you've said your fill. Let's change the subject.",),
    0.5:("I don't want to talk about this.",
          "Ok. Let's change the subject.",
          "*confused / upset expression*",),
    0.6:("*uncomfortable, forced smile*",
          "All right, {pcn}.",
          "K. Thanks.",
          "Well that's very nice, {pcn}. Anyway, is there something else you needed?",),
    0.7:("Hm. Ok.",
          "Ok, that's enough, please, let's talk about something different now.",
          "I have to disagree with you about that.",
          "I'm really not that great.",),
    0.8:("That's nice of you, {pcn}. But I'd rather you didn't say things like that.",
          "Right. Anyways.",),
    0.9:("Well I'm glad you like it, but let's get back to what we were talking about before.",),
    1.0:("Oh. Thank you... {pcn}.",),
    },
"low-self-esteem" : {
    0  :("*crying* I can't take any more of your lies.",
         "*crying* You're so mean!",
         "*sobbing*",
         "You're just evil.",),
    0.1:("Don't try to make me laugh.",
         "No. That's never been true.",),
    0.2:("Yeah, right. You just made that up.",
         "Hm. I wish.",),
    0.3:("You're just saying that.",
         "I know you're full of it.",),
    0.4:("You're lying.",
         "You're a liar.",
         "That's just ridiculous.",),
    0.5:("You liar!",
         "Yea, right. Come on, {tof}.",
         "I wish...",),
    0.6:("Stop it! I wish that were true.",),
    0.7:("Not that I don't think you're being sincere, but I just can't see it that way.",),
    0.8:("That's really nice of you to say, but... I can't believe you. It's not you, it's me...",),
    },
}

# flirtation -- making a pass, complimenting in a romantic or sexual way, suggestive language (flirting) #

FLIRTATION_SUCCESS={
"generic" : {
    0  :("*laughs nervously*",),
    0.4:("*giggles*",
         "*smiles, glances down*",),
    0.5:("*glances suggestively*",),
    0.6:("Hey... *smiles*",),
    0.7:("Hey, {flirt}.",
         "*bites lip*",),
    0.8:("Hey there, {flirt}. Are you free this Friday?",
         "You're not too bad, yourself.",
         "*flutters eyes*",),
    0.9:("*suggestive smile*",
         "*opens mouth in horniness*",),
    1.0:("*looks suggestively at your lips*",
         "*shows tounge*",),
    },
}

FLIRTATION_FAILURE={
"generic" : {
    0  :("Help, help! I'm being sexually assaulted!",
         "I'm extremely uncomfortable right now.",),
    0.1:("Oh -- sorry, I can't.",
         "Not with you. No.",
         "Please, stop. You're making me so uncomfortable.",
         "Don't make me call the cops.",),
    0.2:("Oh, I'm actually seeing someone.",
         "It's too much. Too sudden.",
         "You're making me very uncomfortable...",
         "*no response*",),
    0.3:("You're making me uncomfortable.",
         "*smiles, glances away*",
         "*ignoring you*",),
    0.4:("*stares at you*",
         "*looks away*",),
    0.5:("*tries to look busy*",),
    0.6:("*shuffles nervously*",),
    0.7:("*grumbles uncomfortably*",),
    0.8:("Sorry... I can't.",),
    0.9:("I'm sorry, {pcn}. You're very nice, but I just don't think of you in that way.",),
    1.0:("Oh, {pcn}. You're too much. Really.",),
    },
}

# anger -- brought near the point of violent outbreak #

ANGRY={
"generic" : {
    0  :("I'm going to kick your ass.",
         "You're such a {nc}.",
         "{Slur}.",
         "{Nc}.",
         "{Insult}.",
         "*no response*",),
    0.2:("Hey. Shut up.",),
    0.4:("Who would do something like that?",
         "What a {nc}.",
         "What a {slur} you are.",
         "You absolute {nc}.",),
    0.6:("You're being a real {nc}.",
         "Stop being such a {slur}.",
         "You {nc}!",
         "Are you trying to piss me off?",),
    0.8:("You {nc}! I hate you! I can't believe you would do this!",
         "You absolute {nc}! What are you thinking?",
         "What's gotten into you?",
         "Quit trying to piss me off, {pcn}.",
         "Have you gone mad, {pcgg}?",
         "You complete {nc} of a {pcc}. I'm going to smash your face.",),
    },
"outgoing" : {
    0  :("Are you ready to fight, {slur}?",),
    },
"argumentative" : {
    0  :("I'm about to curb-stomp your ass.",
         "Fucking {nc}, {insult}.",
         "*laughs* Look at this fuckin' {nc}.",),
    0.2:("You've made me really fuckin' mad.",
         "I will bury you.",
         "I'm not scared, you {nc}. Come at me, {tof}.",
         "You made a mistake, kiddo.",),
    },
"bubbly" : {
    0.4:("You {nc}, I'll eat you for breakfast!",),
    },
}





'''

"proud" : {
    },
"low-self-esteem" : {
    },
"argumentative" : {
    },
"non-confrontational" : {
    },
"outgoing" : {
    },
"shy" : {
    },
"independent" : {
    },
"codependent" : {
    },
"bubbly" : {
    },
"low-energy" : {
    },
"motivated" : {
    },
"unmotivated" : {
    },
"relaxed" : {
    },
"uptight" : {
    },
"proactive" : {
    },
"apathetic" : {
    },
    '''













