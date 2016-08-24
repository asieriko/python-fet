import os
import teachereval
from operator import itemgetter

rootdir = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/"

def recev():
    l = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file[-12:] == "teachers.xml":
                #print(os.path.join(subdir, file))
                t,s,lab = teachereval.evaluate(os.path.join(subdir, file))
                if not 5 in s.keys():
                    s[5] = 0
                l.append([os.path.join(subdir, file),s[4]+s[5],s[0],lab[-2]])
                #for k in s.keys():
                    #print(k,": ",s[k])
                #print(s)
    l.sort(key=itemgetter(1),reverse=True)
    for f in l:
        print(f[1], " Bad - ",f[2] ," Good - Hours/week: ",f[-1], " - File: ",f[0])
