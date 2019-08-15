import csv
from collections import defaultdict

#FIXME: It works for normal option subjects, but it fails for small groups, when students from H, and I are split into 3 gropus H,HI and I, same subject name.
#['GAZTE', '1H', 'Yolanda', '4', '1A2', 'z']
#['GAZTE', '1HI', 'Ana', '4', '1A3', 'z']
#['GAZTE', '1I', 'JuanRamón', '4', '1A4', 'z']
#['BE', '1HI', 'Marilen', '2', '1A2', 'x']
#['ERL', '1HI', 'Yolanda', '2', '1A3', 'x']
#Combine input:  [['1-H'], ['GAZTE', 'GAZTE'], ['BE', 'ERL']]
#Combine input:  [['1-I'], ['GAZTE', 'GAZTE'], ['BE', 'ERL']]
#('1-H', ['1-H-GAZTE-BE', '1-H-GAZTE-ERL', '1-H-GAZTE-BE', '1-H-GAZTE-ERL'])
#('1-I', ['1-I-GAZTE-BE', '1-I-GAZTE-ERL', '1-I-GAZTE-BE', '1-I-GAZTE-ERL'])

#FIXME: Impossible combinations are generates (maybe it doesn't affect at all)
#5-H-Latin-tekno-ORA
#5-H-Latin-tekno-ERL
#5-H-Latin-FRA-ORA
#Tekno and latin are on different hours, but students can't do both



def getgroups(activity,sg):
    '''
    activity = ['BE', '1HI', 'Marilen', '2', '1A2', 'x']
    sg = {'1-H': ['1-H-BE', '1-H-ERL'], '1-I': ['1-I-BE', '1-I-ERL']}
    returns ['1-H-BE', '1-I-BE']
    
    Last if...
    activity = ['tekno', '1H', 'Asier', '3', '1A1', '']
    sg = {'1-H': ['1-H-BE', '1-H-ERL'], '1-I': ['1-I-BE', '1-I-ERL']}
    returns ['1-H-BE', '1-H-ERL']
    
    activity = ['Luisa', 'CCSS', '1DBH', '1I', '4', '1A4', 'z']
    sg = {'1-I': ['1-I-BE-Natur', '1-I-BE-CCSS', '1-I-ERL-Natur', '1-I-ERL-CCSS']}
    returns ['1-I-BE-CCSS', '1-I-ERL-CCSS']
    '''
    groups = []
    subgroups = []
    for groupleter in activity[3][1:]:
        groups.append(activity[3][0]+"-"+groupleter)
    for group in groups:
        for subgroup in sg[group]:
            if ("-"+activity[1] in subgroup) or (activity[-1]==''):
                # second par of the or
                #It's not connected so all subgroups of the group
                subgroups.append(subgroup)
    return(subgroups)

def combine(groups):
    '''
    Creates all combinations from two or more lists
    combine ([['h'],['erl','be'],['plas','fra','ale']])  
    ['h-erl-plas', 'h-erl-fra', 'h-erl-ale', 'h-be-plas', 'h-be-fra', 'h-be-ale']
    '''
    l = len(groups)
    if l < 1:
        raise ValueError()
    if l == 1:
        return groups[0]
    c = []
    l1 = groups[0]
    for l2 in groups[1:]:
        for e1 in l1:
            for e2 in l2:
                c.append(str(e1)+"-"+str(e2))
        l1 = c
        c = []
    return l1


def extract(activities):
    '''
    Takes connected subjects and returns a dict with the group and the subjects
    activities = [['Teacher6', 'MT', '1BATX', '5HIJ', '4', '1A4', 't'], ['Teacher8', 'BG', '1BATX', '5HIJ', '4', '1A4', 't'], ['Teacher4', 'Latin', '1BATX', '5HIJ', '4', '1A4', 't'], ['Teacher7', 'Ekonomia', '1BATX', '5HIJ', '4', '1A4', 't']]
    extract(b)
    {'5-J': ['MT', 'BG', 'Latin', 'Ekonomia'], '5-H': ['MT', 'BG', 'Latin', 'Ekonomia'], '5-I': ['MT', 'BG', 'Latin', 'Ekonomia']}

    '''
    groups = defaultdict(list)
    for activity in activities:
        if activity[-1] != '':
            for leter in activity[3][1:]:
                groups[activity[3][0]+"-"+leter].append(activity[1])
    return groups
            
            
def conexions(activities):
    '''
    takes all subjects and generates conexions
    activities = [['Teacher1','tekno','1DBH', '1H',  '3', '1A1', ''], ['BE', '1HI', 'Teacher2', '2', '1A2', 'x'], ['ERL', '1HI', 'Teacher3', '2', '1A3', 'x']]
    {'x': [['BE', '1HI', 'Teacher2', '2', '1A2', 'x'],['ERL', '1HI', 'Teacher3', '2', '1A3', 'x']]}
    '''
    con = defaultdict(list)
    for activity in activities:
        if activity[-1] != '':
            if any(activity[1] in i[1] for i in  con[activity[-1]]):
                raise NameError("Same subject ({}) in a connection ({})".format(activity[1],activity[-1]))
                #If this is not checked you get duplicates, for grupos pequeños...
                #['Begoña', 'Natur', '1DBH', ['1-H-BE-Natur', '1-H-BE-Natur', '1-H-ERL-Natur', '1-H-ERL-Natur'], '4', '1A2', 'z']
                #['Juanjo', 'Natur', '1DBH', ['1-H-BE-Natur', '1-H-BE-Natur', '1-H-ERL-Natur', '1-H-ERL-Natur', '1-I-BE-Natur', '1-I-ERL-Natur'], '4', '1A3', 'z']
            if any(activity[0] in i[0] for i in  con[activity[-1]]):
                raise NameError("Same teacher ({}) in a connection ({})".format(activity[0],activity[-1]))
            if any(activity[5] in i[5] for i in  con[activity[-1]]):
                raise NameError("Same room ({}) in a connection ({})".format(activity[5],activity[-1]))     
            con[activity[-1]].append(activity)
    return con

def mergedics(d1,d2):
    '''
    Merges two dictionaries
    d1 = {}
    d2 = {'5-I': ['IKT', 'ORAT', 'KulZ'], '5-J': ['IKT', 'ORAT', 'KulZ']}
    newsubgroups.mergedics(d1,d2)
    {'5-I': [['IKT', 'ORAT', 'KulZ']], '5-J': [['IKT', 'ORAT', 'KulZ']]}

    d1 = {'5-I': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']], '5-J': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']]}
    d2 = {'5-H': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR'], '5-J': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR'], '5-I': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']}
    newsubgroups.mergedics(d1,d2)
    {'5-H': [['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']], '5-I': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']], '5-J': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']]}
    '''
    if d2 == {}:
        d1,d2 = d2,d1
    k1 = d1.keys()
    k2 = d2.keys()
    d=defaultdict(list)
    for k in k1:
        d[k] = d1[k]
    for k in k2:
        if k not in k1:
            d[k] = [d2[k]]
        elif d2[k] not in d[k]:
            d[k].append(d2[k])
    return d

def generatesubgroups(cl):
    c = conexions(cl)
    d = {}
    for l in c.values():
        d2 = extract(l)
        d = mergedics(d,d2)
    sg = {}
    for k,v in d.items():
        a = v  #[['BE', 'ERL'], ['Natur', 'CCSS']]
        a.insert(0,[k]) #[['1-I'], ['BE', 'ERL'], ['Natur', 'CCSS']]
        sg[k] = combine(a) # { '1-I': ['1-I-BE-Natur', '1-I-BE-CCSS', '1-I-ERL-Natur', '1-I-ERL-CCSS']}
    return sg

def options(a):
    a = [['Teacher2', 'Subject2', '1DBH', '1HI', '2', '1', 'A'], ['Teacher3', 'Subject3', '1DBH', '1HI', '2', '2', 'A'], ['Teacher5', 'Subject5', '1DBH', '1HIJ', '3', '1', 'B'], ['Teacher7', 'Subject7', '1DBH', '1HIJ', '3', '2', 'B'], ['Teacher8', 'Subject8', '1DBH', '1HIJ', '3', '3', 'B']]
    o = [['A', ['Teacher2', 'Subject2', '2', '1', ['1DBH-1-Subject2', '1DBH-H-Subject2', '1DBH-I-Subject2']], ['Teacher3', 'Subject3', '2', '2', ['1DBH-1-Subject3', '1DBH-H-Subject3', '1DBH-I-Subject3']]], 
             ['B', ['Teacher5', 'Subject5', '3', '1', ['1DBH-1-Subject5', '1DBH-H-Subject5', '1DBH-I-Subject5', '1DBH-J-Subject5']], ['Teacher7', 'Subject7', '3', '2', ['1DBH-1-Subject7', '1DBH-H-Subject7', '1DBH-I-Subject7', '1DBH-J-Subject7']], ['Teacher8', 'Subject8', '3', '3', ['1DBH-1-Subject8', '1DBH-H-Subject8', '1DBH-I-Subject8', '1DBH-J-Subject8']]]]
    #options(a,sg),o
    return o

if __name__=="__main__":
        
#[['Teacher2', 'Subject2', 'GRADE', 'GROUPs', 'HOURS', 'ROOM', 'CON']        
        
    a=["Asier,tekno,1DBH,1H,3,1A1,","Idoia,musika,1DBH,1H,3,1A2,"]
    b=["Asier,tekno,1DBH,1H,3,1A1,","Marilen,BE,1DBH,1HI,2,1A2,x","Yolanda,ERL,1DBH,1HI,2,1A3,x"]
    c=["Asier,tekno,1DBH,1H,3,1A1,","Marilen,BE,1DBH,1HI,2,1A2,x","Yolanda,ERL,1DBH,1HI,2,1A3,x","Karol,TPLAS,1DBH,1HIJ,2,1A2,y","Bidane,FRA,1DBH,1HIJ,2,1A3,y","Make,ALE,1DBH,1HIJ,2,1A4,y"]
    d=["Asier,tekno,1DBH,1H,3,1A1,","Marilen,BE,1DBH,1HI,2,1A2,x","Yolanda,ERL,1DBH,1HI,2,1A3,x","Karol,TPLAS,1DBH,1HIJ,2,1A2,y","Bidane,FRA,1DBH,1HIJ,2,1A3,y","Make,ALE,1DBH,1HIJ,2,1A4,y","Maider,MAT1,1DBH,1JK,4,1A3,z","Uxue,MATE2,1BDH,1JK,4,1A4,z"]
    e=["Asier,tekno,1DBH,1H,3,1A1,","Marilen,BE,1DBH,1HI,2,1A2,x","Yolanda,ERL,1DBH,1HI,2,1A3,x","Yolanda,GAZTE,1DBH,1H,4,1A2,z","Ana,GAZTE,1DBH,1HI,4,1A3,z","JuanRamón,GAZTE,1DBH,1I,4,1A4,z"]
    e=["Asier,tekno,1DBH,1H,3,1A1,","Marilen,BE,1DBH,1HI,2,1A2,x","Yolanda,ERL,1DBH,1HI,2,1A3,x","Begoña,Natur,1DBH,1H,4,1A2,z","Juanjo,Natur1,1DBH,1HI,4,1A3,z","Luisa,CCSS,1DBH,1I,4,1A4,z"]
    d=["Asier,tekno,1BATX,5HIJ,3,1A1,x","Marilen,FRA,1BATX,5HIJ,2,1A4,x","Yolanda,ALE,1BAT,5HIJ,2,1A7,x","Karol,MART,1BATX,5HIJ,2,1A2,x","Asun,NAFAR,1BATX,5HIJ,2,1A3,x","Amaia,ORA,1BATX,5H,2,1A9,r","Yolanda,ERL,1BATX,5H,2,1A8,r","Asier,IKT,1BATX,5IJ,4,1A3,z","Amaia,ORAT,1BATX,5IJ,4,1A9,z","Arantza,KulZ,1BATX,5IJ,4,1A4,z","Karol,MT,1BATX,5HIJ,4,1A4,t","Arantza,BG,1BATX,5HIJ,4,1A8,t","Amaia,Latin,1BATX,5HIJ,4,1A9,t","Mikel,Ekonomia,1BATX,5HIJ,4,1A1,t"]

    al = list(csv.reader(a))
    bl = list(csv.reader(b))
    cl = list(csv.reader(c))
    dl = list(csv.reader(d))
    el = list(csv.reader(e))
    with open('/home/asier/Hezkuntza/python-hezkuntza/python-fet/testdata.csv') as csvfile:
        rl = list(csv.reader(csvfile))
    
    courses = rl
    
    sg = generatesubgroups(courses)
    #for s in sg.items():
        #print(s)
    print(sg)
    for j in courses:
        #print("gg: ",getgroups(j,sg))    
        nl = j[:3] + list([getgroups(j,sg)]) + j[4:]
        print(nl)
