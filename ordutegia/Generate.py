import MendiFet as MF

a=MF.MendiFet()
#a.printm()
a.read_csv_data('/home/asier/Hezkuntza/fet/ordutegia/denagarbi15-16.csv')
a.set_hours(['08:30-9:25','09:25-10:20', '10:20-11:15','11:15-11:45', '11:45-12:40','12:40-13:35', '13:35-14:30', '14:30-15:20' ])
a.set_days(['Astelehena', 'Asteartea', 'Asteazkena', 'Osteguna', 'Ostirala'])
a.set_name('Mendillorri BHI')
print "Generate from raw data"
a.generate_from_raw_data()
#a.no_class_hours_mendillorri()
print "Generate teachers"
a.generate_teachers_from_activities()
print "Generate subjects"
a.generate_subjects_from_activities()
print "Generate rooms"
a.generate_rooms_from_activities()
print "Generate buildings"
a.generate_buildings_from_rooms()
print "Generate XML"
a.create_groups_XML(a.generate_groups_from_activities())
#a.printm()
print "Write"
a.write()