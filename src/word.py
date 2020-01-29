'''
    word.py
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














