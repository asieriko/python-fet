from lxml import etree

def doit():
    xmlfile = input("Enter file path: ")
    #"/home/asier/Hezkuntza/SGCC-Erregistroak-16-17/PR01 Matriculacion y planificacion docente y servicios complementarios/PR0102 Planificacion/Horarios/Horario-16-17-indw3JuantoNaira.fet"
    tree = etree.parse(xmlfile)

    for elem in tree.findall('.//Activity'):
        students = elem.findall('.//Students')
        if students != [] and students[0].text[:2] != 'MB':
            #print("Stud ", students[0].text)
            withstudents = etree.SubElement(elem,"Activity_Tag")
            withstudents.text = "WithStudents"
            students.append( withstudents )
        elif students != [] and students[0].text[:2] == 'MB':
            #print("M1 ", subject[0].text[:2])
            meeting = etree.SubElement(elem,"Activity_Tag")
            meeting.text = "Bilera"
            students.append( meeting )
        else:
            subject = elem.findall('.//Subject')
            if subject[0].text == "Zaintza":
                guard = etree.SubElement(elem,"Activity_Tag")
                guard.text = "Zaintza"
                students.append( guard )
            else:#if subject[0].text[:2] in ["MB","BC","BZ","DA","KP"]:
                #print("M2 ", subject[0].text)
                meeting = etree.SubElement(elem,"Activity_Tag")
                meeting.text = "Bilera"
                students.append( meeting )
                
    atl = tree.find('.//Activity_Tags_List')
    for tag in ["WithStudents","Zaintza","Bilera"]:
        at = etree.SubElement(atl,"Activity_Tag")
        atn = etree.SubElement(at,"Name")
        atn.text = tag
    
    tree.write(xmlfile[:-4] + "-Tags.fet", encoding="utf-8", method="xml", pretty_print=True)
    #print(etree.tostring(tree, pretty_print=True))


doit()