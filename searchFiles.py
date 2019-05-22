#search a directory's files looking for a particular string

import os

#get str and directory
print('''Welcome. This script allows you to search a directory's
readable files for a particular string.''')

while(True):
    print("Current directory:\n\n", os.path.dirname(__file__), sep="")
    searchdir=input("\nEnter directory to search in.\n>>")
    find=input("Enter string to search for.\n>>")
    #search each (readable) file in directory for string
    for filename in os.listdir(searchdir):
        try:
            with open( os.path.join(searchdir,filename)) as file:
                lineNum = 1
                for line in file.readlines():
                    if find in line:
                        print(filename, "| Line", lineNum)
                    lineNum +=1
        except Exception as err:
            pass
    print("End of report.\n------------------------------------------")
