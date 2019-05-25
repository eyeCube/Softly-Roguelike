'''
    word.py
    by Jacob Wharton
'''



#
# split stanza
#
# take a string, return list of strings each no longer than nlines lines
#
# - string must already have '\n' newlines in place;
#       this function does not wrap text or add newlines!
#
def split_stanza(text,nlines):
    boxes = []
    count = start = i = 0
    for ch in text:
        i+=1
        if ch == '\n':
            count +=1
        if count >= nlines:
            boxes.append(text[start:i])
            start = i
            count = 0
    boxes.append(text[start:])  # get the remaining lines in one box
    return boxes

#remove_blankspace
#take a string and return it without any spaces
def remove_blankspace(text):
    newStr=[]
    for i in text:
        if i != " ": newStr.append(i)
    return "".join(newStr)














