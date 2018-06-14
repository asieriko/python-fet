import xml.etree.ElementTree as ET
from collections import defaultdict
import csv,sys,getopt

import random

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

class ebaluazioak():
    
    def __init__(self):
        self.tdic = {}
        self.gdic = defaultdict(list)
        self.allgroups = []
        self.sessions = 12
        self.days = 4
        self.indices = []
        self.groupspartition = []
        self.forbidden = []
        
    def set_forbidden(self,forbidden):
        '''
        Subjects that doesn't have evaluation sessions
        like meetings...
        '''
        self.forbidden = forbidden
        
    def set_sessions(self,sessions=12):
        '''
        sets the number of evaluation sessions in total.
        Then it has to be divided in days
        '''
        self.sessions = sessions
        return self.generateIndex()
    
    def set_days(self,days=3):
        '''
        in how many days would the sessions be
        '''
        self.days = days
        return self.generateIndexDay()
    
    def set_best_evs(self,best):
        '''
        once the beste session grouping have been determined
        in order to select the days for each session the best
        session distribution is taken into account
        '''
        self.groupspartition = best
    
    def read_data(self,file):
        '''
        gets the groups and teachers data from a fet teachers.xml file or a CSV file
        '''
        if file[-3:] == "xml":
            self.read_FET(file)
        elif file[-3:] == "csv":
            self.read_CSV(file)
        else:
            print("File format not accepted")
            
            
    def read_CSV(self,file,headers=False):
        '''
        CSV file must be a row for each group and a column for each teacher in the group
        1A;Teacher1;Teacher2;Teacher3
        1B;Teacher4;Teacher2;Teacher5
        '''
        with open(file,'r') as results:
                reader = csv.reader(results,delimiter=",")
                if headers:
                    next(reader,None)
                for row in reader:
                    group = row[0]
                    if group in self.forbidden:
                        print("forbidden: ",group)
                        continue
                    self.allgroups.append(group)
                    for teacher in row[1:]:
                        if teacher != '':
                            self.gdic[group].append(teacher)
                            if teacher in self.tdic.keys():
                                self.tdic[teacher].append(group)
                            else:
                                self.tdic[teacher] = [group]
        print(self.allgroups)
        
    def read_FET(self,file=None):
        '''
        gets the groups and teachers data from a fet teachers.xml file
        '''
        if file == None:
            file = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/EDUCA/teachers.xml"
        tree = ET.parse(file)
        root = tree.getroot()
        teachers = root.findall(".//Teacher")
        for teacher in teachers:
            groups=[]
            name=teacher.attrib.get('name')
            #print(name)
            students = teacher.findall(".//Students")
            for group in students:
                #print(group.attrib.get('name')[:3])
                if group.attrib.get('name')[0] in self.forbidden:
                    #print("FFFF:",group.attrib.get('name')[:3])
                    continue
                if group.attrib.get('name')[:3] not in groups:
                    groups.append(group.attrib.get('name')[:3])
                if group.attrib.get('name')[:3] not in self.allgroups:
                    self.allgroups.append(group.attrib.get('name')[:3])
                if name not in self.gdic[group.attrib.get('name')[:3]]:
                    self.gdic[group.attrib.get('name')[:3]].append(name)
            self.tdic[name] = groups
        with open('mycsvfile.csv','w') as f:
            w = csv.writer(f)
            for n in self.gdic.keys():
                row = n + ',' + ','.join(self.gdic[n])
                print(row)
                l = [n]
                for t in self.gdic[n]:
                    l.append(t)
                w.writerow(l)
        #
            #w = csv.writer(sys.stderr)
            #w.writerow(self.gdic.keys())
            #w.writerow(zip(*self.gdic.values()))
            

    
    def generateIndex(self):
        '''
        creates sessions partitions randomly with the same +/- 1 groups each
        Manuel Zubieta: http://stackoverflow.com/a/14861842/1246747
        '''
        q, r = divmod(len(self.allgroups), self.sessions)
        self.indices = [q*i + min(i, r) for i in range(self.sessions+1)] 

    def generateIndexDay(self):
        '''
        creates sessions partitions randomly with the same +/- 1 groups each
        Manuel Zubieta: http://stackoverflow.com/a/14861842/1246747
        '''
        q, r = divmod(len(self.groupspartition), self.days)
        self.indicesd = [q*i + min(i, r) for i in range(self.days+1)] 

    def permutationtogroups(self,partition):
        '''
        the algorithm works with numbers permutations and 
        we need to convert them to actual groups names
        '''
        partition2 = []
        for j in partition:
            partition2.append(self.allgroups[j])
        partitiongrouped = [partition2[self.indices[i]:self.indices[i+1]] for i in range(self.sessions)]
        partitione = []
        for i in partitiongrouped:
            partitione.append(i)
        return partitione

    def evaluateInd(self,partition):
        '''
        input a set of groups and the list with each group's teachers
        [['1A','1B'],['2A','2B'],['3A','3B']]
        {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"],'2A':["Teacher3","Teacher2"],'2B':["Teacher1","Teacher3"]},'3A':["Teacher1","Teacher2"],'3B':["Teacher1","Teacher4"]}
        ouput how many teachers repeat group for all partitions
        3
        '''
        partitione = self.permutationtogroups(partition)
        conf = 0
        for group in partitione:
            conf += self.evaluate(group)
        return (conf,)

    def evaluate(self,groups):
        '''
        input a set of groups and the list with each group's teachers
        ['1A','1B']
        {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"]}
        ouput how many teachers repeat group
        1
        '''
        t=[]
        conf = 0
        for g in groups:
            for teacher in self.gdic[g]:
                if teacher in t:
                    conf += 1
                else:
                    t.append(teacher)
        return conf
        

    def evaluateDay(self,groupspartition):
        '''
        input a set of groups organization and the list with each group's teachers
        [[['1A','1B'],['2A','2B']],[['3A','3B'],['4A','4B']]]
        {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"],'2A':["Teacher1","Teacher2"],'2B':["Teacher1","Teacher4"],
        '3A':["Teacher5","Teacher2"],'3B':["Teacher4","Teacher4"],'4A':["Teacher6","Teacher2"],'4B':["Teacher5","Teacher4"]}
        ouput how many teachers repeat day
        2
        '''
        t = []
        conf = 0
        part = []
        for j in groupspartition:
            part.append(self.allgroups[j])
        groupspartition = part
        partitiongrouped = [groupspartition[self.indicesd[i]:self.indicesd[i+1]] for i in range(self.days)]
        for groups in partitiongrouped:
            tp = []
            #groups = [item for sublist in p for item in sublist]
            for g in groups:
                for teacher in self.gdic[g]:
                    if teacher not in tp:
                        tp.append(teacher)
            #print(tp)
            t.append(tp)
        #print(t)
        for teacher in self.tdic.keys():
            tr = 0
            for i in range(len(t)):
                if teacher in t[i]:
                    tr += 1
            conf += tr
            #print(tr)
        #print(t)
        return (conf,)



def configure_deap(size,evfun):
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    IND_SIZE=size

    toolbox = base.Toolbox()
    toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
    toolbox.register("individual", tools.initIterate, creator.Individual,
                    toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxOrdered)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    toolbox.register("evaluate", evfun)
    
    return toolbox

def main(argv):
    inputfile = ''
    outputfile = ''
    sessions = 12
    days = 2
    population = 300
    generations = 400
    helptext= 'python3 evaluazioakdeap.py -s sessions_number -d days -p population -g generations'
    try:
      opts, args = getopt.getopt(argv,"hi:o:s:d:p:g:",["ifile=","ofile=","sessions=","days=","population=","generations="])
    except getopt.GetoptError:
      print(helptext)
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print(helptext)
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
      elif opt in ("-s", "--sessions"):
         sessions = int(arg)
      elif opt in ("-d", "--days"):
         days = int(arg)
      elif opt in ("-p", "--population"):
         sessions = int(arg)
      elif opt in ("-g", "--generations"):
         days = int(arg)
         
    ev = ebaluazioak()
    ev.set_forbidden(['B','M','6','1-Z','2-Z'])
    #/home/asier/Hezkuntza/python-hezkuntza/17-18/timetables/Horario1718-single/Horario1718_teachers.xml
    
    print(inputfile)
    
    if inputfile == '':
        inputfile = input("Enter the teachers.xml or .csv filepath: ")
        ev.read_data(inputfile)
        
    print(inputfile)
    
    data = {'sessions':sessions,'days':days,'population': population,'generations':generations}
    
    pop, stats, hof = best_ev_grouping(ev,data)
    
    print("best element: ")
    best = hof.items[0]
    bestg = ev.permutationtogroups(best)
    print(bestg,stats)
    
    partitiongrouped = [hof.items[0][ev.indices[i]:ev.indices[i+1]] for i in range(ev.sessions)]
    
    popd, statsd, hofd = best_ev_days(ev,partitiongrouped,data)
    
    dayg = []
    for e in hofd.items[0]:
        dayg.append(bestg[e])
    daygrouped = [dayg[ev.indicesd[i]:ev.indicesd[i+1]] for i in range(ev.days)]
    print("------------------------")
    print("best day distribution: ")
    #print(hofd.items[0])
    record = stats.compile(pop)
    print(record)
    recordd = statsd.compile(popd)
    print(recordd)
    for i,day in enumerate(daygrouped):
        print(i+1,"st day:")
        for j,hour in enumerate(day):
            print(j+1,": ",sorted(hour))
    #print(ev.tdic)
    #print(ev.gdic)
    
    
def best_ev_grouping(ev,data):    
    #ev.read_data()
    ev.set_sessions(data['sessions'])
    toolbox = configure_deap(len(ev.allgroups),ev.evaluateInd)
    pop = toolbox.population(n=data['population'])
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    #stats.register("Avg", tools.mean)
    #stats.register("Std", tools.std)
    stats.register("Min", min)
    stats.register("Max", max)
    
    algorithms.eaSimple(pop, toolbox, 0.5, 0.1, data['generations'], stats, halloffame=hof)
    return pop, stats, hof

def best_ev_days(ev,best,data):
    ev.set_best_evs(best)
    ev.set_days(data['days'])
    
    toolbox = configure_deap(len(best),ev.evaluateDay)
    
    pop = toolbox.population(n=data['population'])
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    #stats.register("Avg", tools.mean)
    #stats.register("Std", tools.std)
    stats.register("Min", min)
    stats.register("Max", max)
    
    algorithms.eaSimple(pop, toolbox, 0.5, 0.1, data['generations'], stats, halloffame=hof)
    return pop, stats, hof

if __name__ == "__main__":
   main(sys.argv[1:])
