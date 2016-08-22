import xml.etree.ElementTree as ET
from collections import defaultdict

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
    
    def read_data(self):
        '''
        gets the groups and teachers data from a fet teachers.xml file
        '''
        tree = ET.parse("/home/asier/Hezkuntza/python-hezkuntza/python-fet/EDUCA/teachers.xml")
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

def main():
    ev = ebaluazioak()
    ev.set_forbidden(['B','M','6'])
    pop, stats, hof = best_ev_grouping(ev)
    print("best element: ")
    best = hof.items[0]
    bestg = ev.permutationtogroups(best)
    print(bestg)
    partitiongrouped = [hof.items[0][ev.indices[i]:ev.indices[i+1]] for i in range(ev.sessions)]
    pop, stats, hof = best_ev_days(ev,partitiongrouped)
    dayg = []
    for e in hof.items[0]:
        dayg.append(bestg[e])
    daygrouped = [dayg[ev.indicesd[i]:ev.indicesd[i+1]] for i in range(ev.sessions_d)]
    print("------------------------")
    print("best day distribution: ")
    print(hof.items[0])
    print(daygrouped)
    
    
def best_ev_grouping(ev):    
    ev.read_data()
    ev.set_sessions(12)
    toolbox = configure_deap(len(ev.allgroups),ev.evaluateInd)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    #stats.register("Avg", tools.mean)
    #stats.register("Std", tools.std)
    stats.register("Min", min)
    stats.register("Max", max)
    
    algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 4000, stats, halloffame=hof)
    return pop, stats, hof

def best_ev_days(ev,best):
    ev.set_best_evs(best)
    ev.set_days(2)
    
    toolbox = configure_deap(len(best),ev.evaluateDay)
    
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    #stats.register("Avg", tools.mean)
    #stats.register("Std", tools.std)
    stats.register("Min", min)
    stats.register("Max", max)
    
    algorithms.eaSimple(pop, toolbox, 0.5, 0.1, 4000, stats, halloffame=hof)
    return pop, stats, hof

if __name__ == "__main__":
    main()