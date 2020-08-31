from lxml import etree
import csv

def addComplementary(fetfile,csvfile):
    #"/home/asier/Hezkuntza/SGCC-Erregistroak-16-17/PR01 Matriculacion y planificacion docente y servicios complementarios/PR0102 Planificacion/Horarios/Horario-16-17-indw3JuantoNaira.fet"
    tree = etree.parse(xmlfile)
    activities_list = tree.find('.//Activities_List')
    maxid = max_activity_id(tree)
        
    with open(csvfile, newline='') as csvfile1:
     reader = csv.DictReader(csvfile1)
     for row in reader:
         teachername = row["Irakaslea"]
         for k in row.keys():
             if row[k] != '' and k != 'Irakaslea':
                 for hours in range(int(row[k])):
                    activity = etree.SubElement(activities_list,"Activity")
                    
                    teacher = etree.SubElement(activity,"Teacher")
                    teacher.text = teachername
                    subject = etree.SubElement(activity,"Subject")
                    subject.text = k
                    activitytag = etree.SubElement(activity,"Activity_Tag")
                    activitytag.text = "Complementarias"
                    duration = etree.SubElement(activity,"Duration")
                    duration.text = "1"
                    totalduration = etree.SubElement(activity,"Total_Duration")
                    totalduration.text = "1"
                    aid = etree.SubElement(activity,"Id")
                    aid.text = str(maxid)
                    activitygroupid = etree.SubElement(activity,"Activity_Group_Id")
                    activitygroupid.text = str(maxid)
                    active = etree.SubElement(activity,"Active")
                    active.text = "true"
                    comments = etree.SubElement(activity,"Comments")
                    
                    activities_list.append( activity )
                    
                    maxid += 1
       
                
    atl = tree.find('.//Activity_Tags_List')
    at = etree.SubElement(atl,"Activity_Tag")
    atn = etree.SubElement(at,"Name")
    atn.text = "Complementarias"
    
    subjectslist = tree.find('.//Subjects_List')
    for newsubject in ["MintegiBurutzaOrduak","TutoretzaLektiboOrduak","TutoretzaOsagarriOrduak","KalitateOrduak","AdinMurrizketaOrduak","TTBB","EOIDNA","ZuzendaritzaLektibo","ZuzendaritzaOsagarri","Ibiltaritza","EskolaKontseilua","Konpentsazioa","Elkarbizitza","Koordinazioa","Proiektuak"]:
         subject = etree.SubElement(subjectslist,"Subject")
         subjectName = etree.SubElement(subject,"Name")
         subjectName.text = newsubject
         subjectC = etree.SubElement(subject,"Comments")
         subjectslist.append(subject)
    
    tree.write(xmlfile[:-4] + "-Comp.fet", encoding="utf-8", method="xml", pretty_print=True)
    #print(etree.tostring(tree, pretty_print=True))
    print("REMEMEBER: Remove unnecesary constraints...")


def max_activity_id(tree):
      """
      Returns the max_activity_id that the fet xml has
      """
      try:
         return int(max([int(b.text) for b in tree.findall(".//Activity/Id")]))+1
      except:
         return 1

if __name__ == "__main__":
    #csvfile = input("Enter csv file path: ")
    #xmlfile = input("Enter fet file path: ")
    xmlfile = "/home/asier/Hezkuntza/2020-2021/ZUZ/Horario-20-21 Base 18 E2 - 1094.fet"
    csvfile = "/home/asier/Hezkuntza/python-hezkuntza/python-fet/20-21-data/complementarias.csv"
    
    addComplementary(xmlfile,csvfile)

    #Zuzendaritza-MikelB-Begoña 5 días-span7
    #Poner no complementarias 0-r-7
