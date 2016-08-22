import xml.etree.ElementTree as ET
from collections import defaultdict

tree = ET.parse("/home/asier/Hezkuntza/python-hezkuntza/python-fet/EDUCA/teachers.xml")
root = tree.getroot()
teachers = root.findall(".//Teacher")
tdic={}
gdic= defaultdict(list)
allgroups=[]
for teacher in teachers:
    groups=[]
    name=teacher.attrib.get('name')
    #print(name)
    students = teacher.findall(".//Students")
    for group in students:
        #print(group.attrib.get('name')[:3])
        if group.attrib.get('name')[0] in ['M','B','6']:
            #print("FFFF:",group.attrib.get('name')[:3])
            continue
        if group.attrib.get('name')[:3] not in groups:
            groups.append(group.attrib.get('name')[:3])
        if group.attrib.get('name')[:3] not in allgroups:
            allgroups.append(group.attrib.get('name')[:3])
        if name not in gdic[group.attrib.get('name')[:3]]:
            gdic[group.attrib.get('name')[:3]].append(name)
    tdic[name] = groups

sessions=12    
def generateIndex(sessions):
    '''
    creates sessions partitions randomly with the same +/- 1 groups each
    Manuel Zubieta: http://stackoverflow.com/a/14861842/1246747
    '''
    q, r = divmod(len(allgroups), sessions)
    indices = [q*i + min(i, r) for i in range(sessions+1)] 
    return indices    

partitionIndex = generateIndex(sessions)

def permutationtogroups(partition):
    #groups = list(gdic.keys())
    #print(groups)
    partition2 = []
    for j in partition:
        partition2.append(allgroups[j])
    partitiongrouped = [partition2[partitionIndex[i]:partitionIndex[i+1]] for i in range(sessions)]
    partitione = []
    for i in partitiongrouped:
        partitione.append(i)
    return partitione

def evaluateInd(partition):
    '''
    input a set of groups and the list with each group's teachers
    [['1A','1B'],['2A','2B'],['3A','3B']]
    {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"],'2A':["Teacher3","Teacher2"],'2B':["Teacher1","Teacher3"]},'3A':["Teacher1","Teacher2"],'3B':["Teacher1","Teacher4"]}
    ouput how many teachers repeat group for all partitions
    3
    '''
    partitione = permutationtogroups(partition)
    conf = 0
    for group in partitione:
        conf += evaluate(group)
    return (conf,)

def evaluate(groups):
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
        for teacher in gdic[g]:
            if teacher in t:
                conf += 1
            else:
                t.append(teacher)
    return conf
    

def evaluateDay(groupspartition):
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
    for p in groupspartition:
        tp = []
        groups = [item for sublist in p for item in sublist]
        for g in groups:
            for teacher in gdic[g]:
                if teacher not in tp:
                    tp.append(teacher)
        #print(tp)
        t.append(tp)
    #print(t)
    for teacher in teachers.keys():
        tr = 0
        for i in range(len(t)):
            if teacher in t[i]:
                tr += 1
        conf += tr
        #print(tr)
    #print(t)
    return conf

import random

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

IND_SIZE=41

toolbox = base.Toolbox()
toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
toolbox.register("individual", tools.initIterate, creator.Individual,
                 toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluateInd)

def main():
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