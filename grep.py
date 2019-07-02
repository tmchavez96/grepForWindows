#grep.py
#for those of us unforntuante to be on windows
#run "grep.py [keyword]" to search cwd and all child directories for keyword
#run "grep.py -t [keyword]" to search starting from user directory

import sys
import os
import re


def lineParse(dahline):
    word = ''
    words = []
    for char in dahline:
        if(char != " "):
            word += char
        else:
            if(len(word) > 0):
                words.append(word)
                word = ''
    words.append(word)
    return words

def trimToUserSpace(cwd):
    sp = "Users"
    i = cwd.find(sp)
    i += len(sp) + 1
    while(True):
        char = cwd[i]
        if(char == '\\'):
            return cwd[:i]
        i += 1

def goBack():
    cdstr = os.getcwd()
    cdstr += "\\.."
    os.chdir(cdstr)


class directory:
    def __init__(self,cwd,depth):
        os.chdir(cwd)
        tmp = os.popen("dir /a").read()
        #clean out lines not apart of listing
        nc = 0
        lines = []
        l = 0
        last = 0
        for char in tmp:
            if(char == '\n'):
                line = tmp[last:l]
                lines.append(line)
                last = l + 1
            l = l+1
        for _ in range(4):
            lines.pop(0)
        for _ in range(2):
            lines.pop()
        #with clean input, make a list of files and directoires
        folders = []
        files = []
        for line in lines:
            arr = lineParse(line)
            if(len(arr) < 5):
                pass
            else:
                type = arr[3]
                name = arr[4]
                c = 5
                while(c < len(arr)):
                    name = name + " " + arr[c]
                    c += 1
                if(type == "<DIR>"):
                    folders.append(name)
                elif(type == "<JUNCTION>"):
                    pass
                else:
                    files.append(name)
        self.files = files
        self.folders = folders
        self.cwd = cwd
        self.depth = depth
        #print(self.files)
        #print(self.folders)
        #print(self.depth)
        self.parent = None


    def check(self,expression):
        #print("new check call")
        #print("cwd = ",self.cwd)
        for file in self.files:
            if(file.find(expression) > -1):
                print("---------- on path: ", self.cwd)
                print("#### filename of " + file + " matched")
            fpath = self.cwd + '\\' + file
            f = open(fpath,"r")
            i = 1
            try:
                for l in f:
                    if(l.find(expression) > -1):
                        print("---------- on path: ",self.cwd)
                        print("### found key on line " + str(i) + " of file " + file)
                    i += 1
            except:
                pass
                #print("couldnt read non text file")
            f.close()
        while(len(self.folders) > 0):
            cur = self.folders.pop()
            if(cur == ".." or cur == '.'):
                pass
            else:
                if(cur.find(expression) > -1):
                    print("---------- on path: ", self.cwd)
                    print("## dir name of " + file + " matched")
                nextcwd = self.cwd + '\\' + cur
                nextDir = directory(nextcwd,self.depth + 1)
                nextDir.check(expression)
                #goBack()
        return

#get the current working directory and string form of ls
assert ('win' in sys.platform), "This code runs on windows only."
arglen = len(sys.argv)
assert(arglen > 1), "grep needs command line keyword"

key = sys.argv[arglen - 1]
cdstr = os.getcwd()

if(sys.argv[1] == '-t'):
    cdstr = trimToUserSpace(cdstr)


home = directory(cdstr,1)
home.check(key)
