import os
import json
import teachereval
from operator import itemgetter

rootdir = "/home/asier/Hezkuntza/python-hezkuntza/Asier-16-17/timetables/"

def recev():
    l = []
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if file[-12:] == "teachers.xml" and not "zaharrak" in subdir:
                #print(os.path.join(subdir, file))
                print(subdir)
                t,s,lab = teachereval.evaluate(os.path.join(subdir, file))
                if not 5 in s.keys():
                    s[5] = 0
                l.append([os.path.join(subdir, file),s[4]+s[5],s[0],lab[-3],s])
                #for k in s.keys():
                    #print(k,": ",s[k])
                #print(s)
    l.sort(key=itemgetter(1),reverse=True)
    for f in l:
        print(json.dumps(f[-1]), " - ",f[1], " Bad - ",f[2] ," Good - Hours/week: ",f[-2], " - File: ",f[0])
