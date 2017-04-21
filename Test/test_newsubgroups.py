import unittest
from ordutegia.MendiFet import MendiFet
from unittest.case import expectedFailure


class TestMendiFet(unittest.TestCase):

    def test_combine1(self):
        a = [['h'],['erl','be'],['plas','fra','ale']]
        MF = MendiFet()
        self.assertEqual(MF.combine(a), ['h-erl-plas', 'h-erl-fra', 'h-erl-ale', 'h-be-plas', 'h-be-fra', 'h-be-ale'])

    def test_combine2(self):
        a = [['erl','be'],['plas','fra','ale']]
        self.assertEqual(MendiFet().combine(a), ['erl-plas', 'erl-fra', 'erl-ale', 'be-plas', 'be-fra', 'be-ale'])

    def test_combine3(self):
        a = [['plas','fra','ale']]
        self.assertEqual(MendiFet().combine(a), ['plas','fra','ale'])
    
    def test_conexions1(self):
        b = [['Teacher2','BE','1DBH', '1HI',  '2', '1A2', 'x','h'], ['Teacher3','ERL','1DBH', '1HI',  '2', '1A3', 'x','h']]
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        self.assertDictEqual(mf.conexions(b),{'x': [['Teacher2','BE','1DBH' ,'1HI',  '2', '1A2', 'x','h'],['Teacher3','ERL','1DBH', '1HI', '2', '1A3', 'x','h']]})

    def test_conexions2(self):
        b = [['Teacher1','tekno','1DBH', '1H',  '3', '1A1', '','independiente'], ['Teacher2','BE', '1DBH','1HI',  '2', '1A2', 'x','h'], ['Teacher3','ERL','1DBH', '1HI',  '2', '1A3', 'x','h']]
        bo = {'x': [['Teacher2','BE','1DBH', '1HI',  '2', '1A2', 'x','h'],[ 'Teacher3','ERL', '1DBH','1HI', '2', '1A3', 'x','h']]}
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        self.assertDictEqual(mf.conexions(b),bo)

    def test_conexions3(self):
        b = [['Teacher1','tekno', '1BATX','5HIJ',  '3', '1A1', 'x','h'], ['Teacher2','FRA','1BATX', '5HIJ',  '2', '1A2', 'x','h'], ['Teacher3','ALE','1BATX', '5HIJ', '2', '1A3', 'x','h'], ['Teacher6','MART','1BATX', '5HIJ', '2', '1A6', 'x','h'], ['Teacher5','NAFAR','1BATX', '5HIJ', '2', '1A5', 'x','h'], ['Teacher4','ORA','1BATX', '5H', '2', '1A4', 'r','h'], ['Teacher3','ERL', '1BATX','5H', '2', '1A3', 'r','h'], ['Teacher1','IKT','1BATX', '5IJ',  '4', '1A1', 'z','h'], ['Teacher4','ORAT', '1BATX','5IJ', '4', '1A4', 'z','h'], ['Teacher7','KulZ','1BATX', '5IJ', '4', '1A7', 'z','h'], ['Teacher6','MT', '1BATX','5HIJ',  '4', '1A6', 't','h'], ['Teacher7','BG','1BATX', '5HIJ', '4', '1A7', 't','h'], ['Teacher4','Latin', '1BATX','5HIJ', '4', '1A4', 't','h'], ['Teacher8','Ekonomia','1BATX', '5HIJ', '4', '1A8', 't','h']]
        bo = {'x': [['Teacher1', 'tekno', '1BATX', '5HIJ', '3', '1A1', 'x','h'], ['Teacher2', 'FRA', '1BATX', '5HIJ', '2', '1A2', 'x','h'], ['Teacher3', 'ALE', '1BATX', '5HIJ', '2', '1A3', 'x','h'], ['Teacher6', 'MART', '1BATX', '5HIJ', '2', '1A6', 'x','h'], ['Teacher5', 'NAFAR', '1BATX', '5HIJ', '2', '1A5', 'x','h']],
              'r': [['Teacher4', 'ORA', '1BATX', '5H', '2', '1A4', 'r','h'], ['Teacher3', 'ERL', '1BATX', '5H', '2', '1A3', 'r','h']], 
              't': [['Teacher6', 'MT', '1BATX', '5HIJ', '4', '1A6', 't','h'], ['Teacher7', 'BG', '1BATX', '5HIJ', '4', '1A7', 't','h'], ['Teacher4', 'Latin', '1BATX', '5HIJ', '4', '1A4', 't','h'], ['Teacher8', 'Ekonomia', '1BATX', '5HIJ', '4', '1A8', 't','h']], 
              'z': [['Teacher1', 'IKT', '1BATX', '5IJ', '4', '1A1', 'z','h'], ['Teacher4', 'ORAT', '1BATX', '5IJ', '4', '1A4', 'z','h'], ['Teacher7', 'KulZ', '1BATX', '5IJ', '4', '1A7', 'z','h']]}
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        r = mf.conexions(b)
        self.assertEqual(r.keys(), bo.keys())
        for k in r.keys():
            self.assertEqual(r[k], bo[k])
        #self.assertDictEqual(r,bo)

    def test_extract1(self):
        b = [[ 'Teacher1', 'IKT', '1BATX' ,'5IJ','4', '1A3', 'z'], ['Teacher4','ORAT', '1BATX', '5IJ',  '4', '1A4', 'z'], ['Teacher7','KulZ', '1BATX', '5IJ', '4', '1A4', 'z']]
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        self.assertDictEqual(mf.extract(b),{'5-J': ['IKT', 'ORAT', 'KulZ'], '5-I': ['IKT', 'ORAT', 'KulZ']})
        
    def test_extract2(self):
        b = [['Teacher6', 'MT', '1BATX', '5HIJ',  '4', '1A4', 't'], ['Teacher8','BG', '1BATX', '5HIJ', '4', '1A4', 't'], ['Teacher4','Latin', '1BATX', '5HIJ',  '4', '1A4', 't'], ['Teacher7','Ekonomia', '1BATX', '5HIJ',  '4', '1A4', 't']]
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        self.assertDictEqual(mf.extract(b),{'5-J': ['MT', 'BG', 'Latin', 'Ekonomia'], '5-H': ['MT', 'BG', 'Latin', 'Ekonomia'], '5-I': ['MT', 'BG', 'Latin', 'Ekonomia']})
        
    def test_extract3(self):
        b = [['Teacher1','tekno', '1BATX', '5HIJ',  '3', '1A1', 'x'], ['Teacher2','FRA', '1BATX', '5HIJ',  '2', '1A2', 'x'], ['Teacher3', 'ALE', '1BATX', '5HIJ', '2', '1A3', 'x'], [ 'Teacher6','MART', '1BATX', '5HIJ', '2', '1A2', 'x'], ['Teacher5','NAFAR', '1BATX', '5HIJ',  '2', '1A3', 'x']]
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        self.assertDictEqual(mf.extract(b),{'5-J': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR'], '5-H': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR'], '5-I': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']})
        
    def test_mergedicts1(self):
        d1 = {}
        d2 = {'5-I': ['IKT', 'ORAT', 'KulZ'], '5-J': ['IKT', 'ORAT', 'KulZ']}
        self.assertDictEqual(MendiFet().mergedics(d1,d2),{'5-I': [['IKT', 'ORAT', 'KulZ']], '5-J': [['IKT', 'ORAT', 'KulZ']]})

    def test_mergedicts2(self):
        d1 = {'5-I': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']], '5-J': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']]}
        d2 = {'5-H': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR'], '5-J': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR'], '5-I': ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']}
        self.assertDictEqual(MendiFet().mergedics(d1,d2),{'5-H': [['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']], '5-I': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']], '5-J': [['IKT', 'ORAT', 'KulZ'], ['tekno', 'FRA', 'ALE', 'MART', 'NAFAR']]})

    def test_mergedicts3(self):
        d1 = {'5-I': ['IKT', 'ORAT', 'KulZ'], '5-J': ['IKT', 'ORAT', 'KulZ']}
        d2 = {}
        self.assertDictEqual(MendiFet().mergedics(d1,d2),{'5-J': [['IKT', 'ORAT', 'KulZ']], '5-I': [['IKT', 'ORAT', 'KulZ']]})

    def test_generatesubgroups1(self):
        a = [['Teacher1','tekno','1DBH', '1H',  '3', '1A1', '','independiente'], [ 'Teacher2','BE','1DBH','1HI', '2', '1A2', 'x','h'], ['Teacher3','ERL','1DBH', '1HI',  '2', '1A3', 'x','h']]
        o = {'1-I': ['1-I-BE', '1-I-ERL'], '1-H': ['1-H-BE', '1-H-ERL']}
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        self.assertDictEqual(mf.generatesubgroups(a),o)
    
    @expectedFailure
    def test_generatesubgroups2(self):
        #FIXME: Sometimes it works some it doesn't it changes the order of elements¿?
        a = [['Teacher1','tekno','1BATX', '5HIJ',  '3', '1A1', 'x','h'], ['Teacher2','FRA','1BATX', '5HIJ',  '2', '1A2', 'x','h'], ['Teacher3','ALE','1BATX', '5HIJ',  '2', '1A3', 'x','h'], ['Teacher6','MART','1BATX', '5HIJ',  '2', '1A4', 'x','h'], ['Teacher5','NAFAR','1BATX', '5HIJ',  '2', '1A5', 'x','h'], ['Teacher4','ORA','1BATX', '5H',  '2', '1A4', 'r','h'], ['Teacher3','ERL','1BATX', '5H',  '2', '1A2', 'r','h'], [ 'Teacher1','IKT','1BATX', '5IJ', '4', '1A3', 'z','h'], ['Teacher4','ORAT','1BATX', '5IJ',  '4', '1A4', 'z','h'], ['Teacher7','KulZ','1BATX', '5IJ',  '4', '1A2', 'z','h'], ['Teacher6','MT','1BATX', '5HIJ',  '4', '1A4', 't','h'], ['Teacher7','BG','1BATX', '5HIJ',  '4', '1A2', 't','h'], ['Teacher4','Latin','1BATX', '5HIJ',  '4', '1A1', 't','h'], ['Teacher8','Ekonomia', '1BATX','5HIJ',  '4', '1A5', 't','h']]
        o = {'5-I': ['5-I-MT-IKT-tekno', '5-I-MT-IKT-FRA', '5-I-MT-IKT-ALE', '5-I-MT-IKT-MART', '5-I-MT-IKT-NAFAR', '5-I-MT-ORAT-tekno', '5-I-MT-ORAT-FRA', '5-I-MT-ORAT-ALE', '5-I-MT-ORAT-MART', '5-I-MT-ORAT-NAFAR', '5-I-MT-KulZ-tekno', '5-I-MT-KulZ-FRA', '5-I-MT-KulZ-ALE', '5-I-MT-KulZ-MART', '5-I-MT-KulZ-NAFAR', '5-I-BG-IKT-tekno', '5-I-BG-IKT-FRA', '5-I-BG-IKT-ALE', '5-I-BG-IKT-MART', '5-I-BG-IKT-NAFAR', '5-I-BG-ORAT-tekno', '5-I-BG-ORAT-FRA', '5-I-BG-ORAT-ALE', '5-I-BG-ORAT-MART', '5-I-BG-ORAT-NAFAR', '5-I-BG-KulZ-tekno', '5-I-BG-KulZ-FRA', '5-I-BG-KulZ-ALE', '5-I-BG-KulZ-MART', '5-I-BG-KulZ-NAFAR', '5-I-Latin-IKT-tekno', '5-I-Latin-IKT-FRA', '5-I-Latin-IKT-ALE', '5-I-Latin-IKT-MART', '5-I-Latin-IKT-NAFAR', '5-I-Latin-ORAT-tekno', '5-I-Latin-ORAT-FRA', '5-I-Latin-ORAT-ALE', '5-I-Latin-ORAT-MART', '5-I-Latin-ORAT-NAFAR', '5-I-Latin-KulZ-tekno', '5-I-Latin-KulZ-FRA', '5-I-Latin-KulZ-ALE', '5-I-Latin-KulZ-MART', '5-I-Latin-KulZ-NAFAR', '5-I-Ekonomia-IKT-tekno', '5-I-Ekonomia-IKT-FRA', '5-I-Ekonomia-IKT-ALE', '5-I-Ekonomia-IKT-MART', '5-I-Ekonomia-IKT-NAFAR', '5-I-Ekonomia-ORAT-tekno', '5-I-Ekonomia-ORAT-FRA', '5-I-Ekonomia-ORAT-ALE', '5-I-Ekonomia-ORAT-MART', '5-I-Ekonomia-ORAT-NAFAR', '5-I-Ekonomia-KulZ-tekno', '5-I-Ekonomia-KulZ-FRA', '5-I-Ekonomia-KulZ-ALE', '5-I-Ekonomia-KulZ-MART', '5-I-Ekonomia-KulZ-NAFAR'], '5-H': ['5-H-MT-ORA-tekno', '5-H-MT-ORA-FRA', '5-H-MT-ORA-ALE', '5-H-MT-ORA-MART', '5-H-MT-ORA-NAFAR', '5-H-MT-ERL-tekno', '5-H-MT-ERL-FRA', '5-H-MT-ERL-ALE', '5-H-MT-ERL-MART', '5-H-MT-ERL-NAFAR', '5-H-BG-ORA-tekno', '5-H-BG-ORA-FRA', '5-H-BG-ORA-ALE', '5-H-BG-ORA-MART', '5-H-BG-ORA-NAFAR', '5-H-BG-ERL-tekno', '5-H-BG-ERL-FRA', '5-H-BG-ERL-ALE', '5-H-BG-ERL-MART', '5-H-BG-ERL-NAFAR', '5-H-Latin-ORA-tekno', '5-H-Latin-ORA-FRA', '5-H-Latin-ORA-ALE', '5-H-Latin-ORA-MART', '5-H-Latin-ORA-NAFAR', '5-H-Latin-ERL-tekno', '5-H-Latin-ERL-FRA', '5-H-Latin-ERL-ALE', '5-H-Latin-ERL-MART', '5-H-Latin-ERL-NAFAR', '5-H-Ekonomia-ORA-tekno', '5-H-Ekonomia-ORA-FRA', '5-H-Ekonomia-ORA-ALE', '5-H-Ekonomia-ORA-MART', '5-H-Ekonomia-ORA-NAFAR', '5-H-Ekonomia-ERL-tekno', '5-H-Ekonomia-ERL-FRA', '5-H-Ekonomia-ERL-ALE', '5-H-Ekonomia-ERL-MART', '5-H-Ekonomia-ERL-NAFAR'], '5-J': ['5-J-MT-IKT-tekno', '5-J-MT-IKT-FRA', '5-J-MT-IKT-ALE', '5-J-MT-IKT-MART', '5-J-MT-IKT-NAFAR', '5-J-MT-ORAT-tekno', '5-J-MT-ORAT-FRA', '5-J-MT-ORAT-ALE', '5-J-MT-ORAT-MART', '5-J-MT-ORAT-NAFAR', '5-J-MT-KulZ-tekno', '5-J-MT-KulZ-FRA', '5-J-MT-KulZ-ALE', '5-J-MT-KulZ-MART', '5-J-MT-KulZ-NAFAR', '5-J-BG-IKT-tekno', '5-J-BG-IKT-FRA', '5-J-BG-IKT-ALE', '5-J-BG-IKT-MART', '5-J-BG-IKT-NAFAR', '5-J-BG-ORAT-tekno', '5-J-BG-ORAT-FRA', '5-J-BG-ORAT-ALE', '5-J-BG-ORAT-MART', '5-J-BG-ORAT-NAFAR', '5-J-BG-KulZ-tekno', '5-J-BG-KulZ-FRA', '5-J-BG-KulZ-ALE', '5-J-BG-KulZ-MART', '5-J-BG-KulZ-NAFAR', '5-J-Latin-IKT-tekno', '5-J-Latin-IKT-FRA', '5-J-Latin-IKT-ALE', '5-J-Latin-IKT-MART', '5-J-Latin-IKT-NAFAR', '5-J-Latin-ORAT-tekno', '5-J-Latin-ORAT-FRA', '5-J-Latin-ORAT-ALE', '5-J-Latin-ORAT-MART', '5-J-Latin-ORAT-NAFAR', '5-J-Latin-KulZ-tekno', '5-J-Latin-KulZ-FRA', '5-J-Latin-KulZ-ALE', '5-J-Latin-KulZ-MART', '5-J-Latin-KulZ-NAFAR', '5-J-Ekonomia-IKT-tekno', '5-J-Ekonomia-IKT-FRA', '5-J-Ekonomia-IKT-ALE', '5-J-Ekonomia-IKT-MART', '5-J-Ekonomia-IKT-NAFAR', '5-J-Ekonomia-ORAT-tekno', '5-J-Ekonomia-ORAT-FRA', '5-J-Ekonomia-ORAT-ALE', '5-J-Ekonomia-ORAT-MART', '5-J-Ekonomia-ORAT-NAFAR', '5-J-Ekonomia-KulZ-tekno', '5-J-Ekonomia-KulZ-FRA', '5-J-Ekonomia-KulZ-ALE', '5-J-Ekonomia-KulZ-MART', '5-J-Ekonomia-KulZ-NAFAR']}
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7 
        r = mf.generatesubgroups(a)
        self.assertEqual(r.keys(), o.keys())
        for k in r.keys():
            self.assertEqual(r[k], o[k])
        self.assertDictEqual(mf.generatesubgroups(a),o)

    def test_getgroups1(self):
        a = [ 'Teacher1','tekno','1DBH', '1H', '3', '1A1', '']
        sg = {'1-H': ['1-H-BE', '1-H-ERL'], '1-I': ['1-I-BE', '1-I-ERL']}
        o = ['1-H-BE', '1-H-ERL']
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        self.assertEqual(mf.getgroups(a,sg),o)    

    def test_getgroups2(self):
        a = ['Teacher2','BE', '1DBH','1HI',  '2', '1A2', 'x']
        sg = {'1-H': ['1-H-BE', '1-H-ERL'], '1-I': ['1-I-BE', '1-I-ERL']}
        o = ['1-H-BE','1-I-BE']
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        self.assertEqual(mf.getgroups(a,sg),o)    

    @expectedFailure
    def test_options(self):
        a = [['Teacher2', 'Subject2', '1DBH', '1HI', '2', '1', 'A'], ['Teacher3', 'Subject3', '1DBH', '1HI', '2', '2', 'A'], ['Teacher5', 'Subject5', '1DBH', '1HIJ', '3', '1', 'B'], ['Teacher7', 'Subject7', '1DBH', '1HIJ', '3', '2', 'B'], ['Teacher8', 'Subject8', '1DBH', '1HIJ', '3', '3', 'B']]
        o = [['A', ['Teacher2', 'Subject2', '2', '1', ['1DBH-1-Subject2', '1DBH-H-Subject2', '1DBH-I-Subject2']], ['Teacher3', 'Subject3', '2', '2', ['1DBH-1-Subject3', '1DBH-H-Subject3', '1DBH-I-Subject3']]], 
             ['B', ['Teacher5', 'Subject5', '3', '1', ['1DBH-1-Subject5', '1DBH-H-Subject5', '1DBH-I-Subject5', '1DBH-J-Subject5']], ['Teacher7', 'Subject7', '3', '2', ['1DBH-1-Subject7', '1DBH-H-Subject7', '1DBH-I-Subject7', '1DBH-J-Subject7']], ['Teacher8', 'Subject8', '3', '3', ['1DBH-1-Subject8', '1DBH-H-Subject8', '1DBH-I-Subject8', '1DBH-J-Subject8']]]]
        self.assertEqual(MendiFet().options(a),o)    


if __name__ == '__main__':
    unittest.main()
