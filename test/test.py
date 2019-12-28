l=[]
r = ("test", (1,2,3,4,),)
l.append(r)
r2 = ("test2", (4,2,5,4,),)
l.append(r2)
for a, (b,c,d,e) in l:
    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print("~~~~~~~~~")
