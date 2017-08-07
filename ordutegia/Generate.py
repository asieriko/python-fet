import MendiFet as MF

a=MF.MendiFet()
#a.printm()
a.read_csv_data('/home/asier/Hezkuntza/python-hezkuntza/python-fet/ordutegia/data/1718.csv')
a.set_hours(['08:30-9:25','09:25-10:20', '10:20-11:15','11:45-12:40'])#,'11:15-11:45', '11:45-12:40','12:40-13:35', '13:35-14:30', '14:30-15:20' ])
a.set_days(['Astelehena', 'Asteartea', 'Asteazkena', 'Osteguna', 'Ostirala'])
a.set_name('Mendillorri BHI')
incompatibilities = {"1":{"Bio Geo P":["Bio Geo"],
                          "Gizarte P":["Gizarte","Gizarte Plur"],
                          "Bio Geo":["Bio Geo P"],
                          "Gizarte":["Gizarte P","Gizarte Plur"],
                          "Gizarte Plur":["Gizarte P","Gizarte"],
                          "Inglesa":["Inglesa Plur","Inglesa SSBB"],
                          "Inglesa Plur":["Inglesa","Inglesa SSBB"],
                          "Inglesa SSBB":["Inglesa Plur","Inglesa"],
                          "Erlijioa":["Balore Etikoak"],
                          "Balore Etikoak":["Erlijioa"],
                          },
                     "2":{"Inglesa":["Inglesa SSBB","Teknologia SSBB"],
                          "Inglesa SSBB":["Teknologia","Inglesa"],
                          "Teknologia":["Inglesa SSBB","Teknologia SSBB"],
                          "Teknologia SSBB":["Teknologia","Inglesa"],
                          "Erlijioa":["Balore Etikoak"],
                          "Balore Etikoak":["Erlijioa"],
                          },
                     "3":{"Inglesa":["Inglesa SSBB", "Fisika Kimika SSBB"],
                          "Inglesa SSBB":["Fisika Kimika","Inglesa"],
                          "Fisika Kimika":["Inglesa SSBB","Fisika Kimika SSBB"],
                          "Fisika Kimika SSBB":["Fisika Kimika","Inglesa"],
                          "Erlijioa":["Balore Etikoak"],
                          "Balore Etikoak":["Erlijioa"],
                          },
                     "4":{"Fisika Kimika":["Latina","Ekonomia","Teknologia", "Cien Apl","Ekintzailetza...","Matematika Aplikatuak","Taller Exp. Art"],
                          "Matematika Akademikoak":["Teknologia", "Cien Apl","Ekintzailetza...","Matematika Aplikatuak","Taller Exp. Art"],
                          "Latin":["Fisika Kimika","Teknologia", "Cien Apl","Ekintzailetza...","Matematika Aplikatuak","Laboratorio"],
                          "Ekonomia":["Fisika Kimika","Teknologia", "Cien Apl","Ekintzailetza...","Matematika Aplikatuak","Laboratorio"],
                          "Cien Apl":["Fisika Kimika","Ekonomia", "Latin","Taller Exp. Art","Matematika Akademikoak","Laboratorio"],
                          "Teknologia":["Fisika Kimika","Ekonomia", "Latin","Taller Exp. Art","Matematika Akademikoak","Laboratorio"],
                          "Laboratorio":["Teknologia","Cien Apl","Ekintzailetza...","Ekonomia", "Latina","Taller Exp. Art","Matematika Aplikatuak"],
                          "Ekintzailetza...":["Fisika Kimika","Ekonomia", "Latin","Taller Exp. Art","Matematika Akademikoak","Laboratorio"],
                          "Erlijioa":["Balore Etikoak"],
                          "Balore Etikoak":["Erlijioa"],
                          },
                     "5":{"IKT 2":["IKT 1"],"IKT 1":["IKT 2"],
                                  "Fisika Kimika 1":["Matematika 2","Fisika Kimika 2", "Historia 1", "Historia 2","Historia","Ekonomia","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Fisika Kimika 2":["Matematika 1","Fisika Kimika 1", "Historia 1", "Historia 2","Historia","Ekonomia","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Fisika Kimika":["Fisika Kimika 1", "Historia 1", "Historia 2","Historia","Ekonomia","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Bio Geo":["Tek Ind","Marrazketa Teknikoa","Historia 1", "Historia 2","Historia","Ekonomia","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I""Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Tek Ind":["Anatomia Ap.","Bio Geo","Historia 1", "Historia 2","Historia","Ekonomia","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I","Matematika GGZZ I 1", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Anatomia Ap.":["Tek Ind","Historia 1", "Historia 2","Historia","Ekonomia","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1","Matematika GGZZ I", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Marrazketa Teknikoa":["Historia 1", "Historia 2","Historia","Ekonomia","Bio Geo","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1","Matematika GGZZ I", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Matematika 1": ["Fisika Kimika 2","Matematika 2", "Historia 1", "Historia 2","Historia","Ekonomia","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1","Matematika GGZZ I", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Matematika 2": ["Fisika Kimika 1","Matematika 1","Historia 1", "Historia 2","Historia","Ekonomia","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1","Matematika GGZZ I", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                                  "Matematika": ["Matematika 1","Historia 1", "Historia 2","Historia","Ekonomia","Latina","Ekonomia 1", "Ekonomia 2","Matematika GGZZ I 1","Matematika GGZZ I", "Matematika GGZZ I 2","Marrazketa Artistikoa"],
                             "Historia 1":["Historia 2", "Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Historia 2":["Historia 1", "Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Historia":["Historia 1", "Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Latina":["Ekonomia","Matematika","Fisika Kimika","Ekonomia 1", "Ekonomia 2","Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Matematika GGZZ I 1":["Grekera","Matematika","Fisika Kimika","Matematika GGZZ I 2", "Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Matematika GGZZ I 2":["Grekera","Matematika","Fisika Kimika","Matematika GGZZ I 1", "Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Ekonomia 1":["Ekonomia","Matematika","Fisika Kimika","Ekonomia 2", "Latina","Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Ekonomia 2":["Ekonomia","Matematika","Fisika Kimika","Ekonomia 1", "Latina","Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"],
                             "Marrazketa Artistikoa":["Matematika","Fisika Kimika","Fisika Kimika 1","Fisika Kimika 2","Matematika 1", "Matematika 2","Tek Ind", "Bio Geo", "Anatomia Ap.","Marrazketa Teknikoa"]},
                     "6":{"Kimika 1":["Kimika 2","Latina","Grekera","Enp. Ekonomia","Filosofia 1", "Filosofia 2","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia"],
                          "Kimika 2":["Kimika 1","Latina","Grekera","Enp. Ekonomia","Filosofia 1", "Filosofia 2","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia"],
                          "Kimika":["Latina","Grekera","Enp. Ekonomia","Filosofia","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia"],
                          "Matematika 1":["Matematika 2","Latina","Grekera","Enp. Ekonomia","Filosofia 1", "Filosofia 2","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia"],
                          "Matematika 2":["Matematika 2","Latina","Grekera","Enp. Ekonomia","Filosofia 1", "Filosofia 2","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia"],
                          "Biologia 1":["Biologia 2","Latina","Grekera","Enp. Ekonomia","Filosofia 1", "Filosofia 2","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia","Marrazketa Teknikoa","Tek Ind"],
                          "Biologia 2":["Biologia 1","Latina","Grekera","Enp. Ekonomia","Filosofia 1", "Filosofia 2","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia","Marrazketa Teknikoa","Tek Ind"],
                          "Biologia":["Latina","Grekera","Enp. Ekonomia","Filosofia","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia","Marrazketa Teknikoa","Tek Ind"],
                          "Tek Ind":["Biologia 1","Biologia 2","Latina","Grekera","Enp. Ekonomia","Filosofia 1", "Filosofia 2","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia"],
                          "Marrazketa Teknikoa":["Biologia 1","Biologia 2","Latina","Grekera","Enp. Ekonomia","Filosofia 1", "Filosofia 2","Matematika GGZZ II","Marrazketa Artistikoa II","Kudeaketa Oin.","Geografia"],
                          "Filosofia 1":["Kimika 1","Kimika 2","Biologia 1","Biologia 2","Fisika","Marrazketa Teknikoa","Tek Ind"],
                          "Filosofia 2":["Kimika 1","Kimika 2","Biologia 1","Biologia 2","Fisika","Marrazketa Teknikoa","Tek Ind"],
                          "Filosofia":["Kimika","Biologia","Fisika","Marrazketa Teknikoa","Tek Ind"],
                          "Psicologia 1":["Tek Ind","Marrazketa Teknikoa"],
                          "Psicologia 2":["Tek Ind","Marrazketa Teknikoa"],
                          "Psicologia":["Tek Ind","Marrazketa Teknikoa"],
                          "Geografia":["Kimika 1","Kimika 2","Biologia 1","Biologia 2","Fisika","Marrazketa Teknikoa","Tek Ind","Matematika 1","Matematika 2"],
                          "Latina":["Kimika 1","Kimika 2","Biologia 1","Biologia 2","Fisika","Marrazketa Teknikoa","Tek Ind","Enp. Ekonomia","Matematika 1","Matematika 2"],
                          "Grekera":["Kimika 1","Kimika 2","Biologia 1","Biologia 2","Fisika","Marrazketa Teknikoa","Tek Ind","Matematika GGZZ II","Enp. Ekonomia","Matematika 1","Matematika 2"],}}
a.set_incompatibilities(incompatibilities)
print("Generate from raw data")
a.generate_from_raw_data()
#a.no_class_hours_mendillorri()
print("Generate teachers")
a.generate_teachers_from_activities()
print("Generate subjects")
a.generate_subjects_from_activities()
print("Generate rooms")
a.generate_rooms_from_activities()
print("Generate buildings")
a.generate_buildings_from_rooms()
print("Generate XML")
a.create_groups_XML(a.generate_groups_from_activities())
#a.printm()
print("Write")
a.write("testdata.fet")  
