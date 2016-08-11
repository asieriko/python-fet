import csv

irakasleak = {}
with open('irakasleak.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        irakasleak[row[1]] = {'ABREV':row[0], 'DEPART':row[2]}


gelak = {}
with open('gelak.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        gelak[row[0]] = {'ABREV':row[0], 'EDIFICIO':row[1],'NOMBRE':row[0]}