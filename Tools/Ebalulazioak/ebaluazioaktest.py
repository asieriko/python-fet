import ebaluazioak
import unittest

class KnownValues(unittest.TestCase):            
    
    
    
    def test_evaluate1(self):
        groups = ['1A','1B']
        gdic = {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"]}
        expected = 1
        a = ebaluazioak.evaluation()
        result = a.evaluate(groups,gdic)
        self.assertEqual(expected, result)
    
    
    def test_evaluate0(self):
        groups = ['1A','1B']
        gdic = {'1A':["Teacher1","Teacher2"],'1B':["Teacher3","Teacher4"]}
        expected = 0
        a = ebaluazioak.evaluation()
        result = a.evaluate(groups,gdic)
        self.assertEqual(expected, result)
    
    
    #def test_evaluateN(self):
        #groups = ['2A','2B']
        #gdic = {'1A':["Teacher1","Teacher2"],'1B':["Teacher3","Teacher4"]}
        #expected = 0
        #a = ebaluazioak.evaluation()
        #result = a.evaluate(groups,gdic)
        #self.assertEqual(expected, result)
    
    
    def test_evpart0(self):
        partition = [['1A','1B'],['2A','2B'],['3A','3B']]
        gdic = {'1A':["Teacher1","Teacher2"],'1B':["Teacher3","Teacher4"],'2A':["Teacher4","Teacher2"],'2B':["Teacher1","Teacher3"],'3A':["Teacher3","Teacher2"],'3B':["Teacher1","Teacher4"]}
        expected = 0
        a = ebaluazioak.evaluation()
        result = a.evaluatePartition(partition,gdic)
        self.assertEqual(expected, result)
    
    def test_evpart3(self):
        partition = [['1A','1B'],['2A','2B'],['3A','3B']]
        gdic = {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"],'2A':["Teacher3","Teacher2"],'2B':["Teacher1","Teacher3"],'3A':["Teacher1","Teacher2"],'3B':["Teacher1","Teacher4"]}
        expected = 3
        a = ebaluazioak.evaluation()
        result = a.evaluatePartition(partition,gdic)
        self.assertEqual(expected, result)
        
        
        
    def test_evaluateDay7(self):
        partition = [[['1A','1B'],['2A','2B']],[['3A','3B'],['4A','4B']]]
        gdic = {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher4"],'2A':["Teacher1","Teacher2"],'2B':["Teacher1","Teacher4"],
        '3A':["Teacher5","Teacher2"],'3B':["Teacher4","Teacher6"],'4A':["Teacher6","Teacher2"],'4B':["Teacher5","Teacher4"]}
        teachers = {"Teacher1": ['1A','1B','2A','2B'],"Teacher2": ['1A','2A','3A','4A'],"Teacher4": ['1B','2B','3B','4B'],"Teacher5": ['3A','4B'],"Teacher6": ['3B','4A']}
        expected = 7
        a = ebaluazioak.evaluation()
        result = a.evaluateDay(partition,gdic,teachers)
        self.assertEqual(expected, result)

    def test_evaluateDay10(self):
        partition = [[['1A','1B'],['2A','2B']],[['3A','3B'],['4A','4B']]]
        gdic = {'1A':["Teacher1","Teacher2","Teacher5"],'1B':["Teacher1","Teacher4"],'2A':["Teacher1","Teacher6"],'2B':["Teacher2","Teacher4"],
        '3A':["Teacher2"],'3B':["Teacher1","Teacher4","Teacher6"],'4A':["Teacher2"],'4B':["Teacher5","Teacher4"]}
        teachers = {"Teacher1": ['1A','1B','2A','3B'],"Teacher2": ['1A','2B','3A','4A'],"Teacher4": ['1B','2B','3B','4B'],"Teacher5": ['1A','4B'],"Teacher6": ['3B','2A']}
        expected = 10
        a = ebaluazioak.evaluation()
        result = a.evaluateDay(partition,gdic,teachers)
        self.assertEqual(expected, result)

    def test_evaluateDay5(self):
        partition = [[['1A','1B'],['2A','2B']],[['3A','3B'],['4A','4B']]]
        gdic = {'1A':["Teacher1","Teacher2"],'1B':["Teacher1","Teacher2"],'2A':["Teacher1","Teacher2"],'2B':["Teacher1","Teacher2"],
        '3A':["Teacher4"],'3B':["Teacher4","Teacher6"],'4A':["Teacher6"],'4B':["Teacher5","Teacher4"]}
        teachers = {"Teacher1": ['1A','1B','2A','2B'],"Teacher2": ['1A','1B','2A','2B'],"Teacher4": ['3A','3B','4B'],"Teacher5": ['4B'],"Teacher6": ['3B','4A']}
        expected = 5
        a = ebaluazioak.evaluation()
        result = a.evaluateDay(partition,gdic,teachers)
        self.assertEqual(expected, result)
   
    def test_mix_1(self):
        allgroups = ['1-A','1-B','2-A','2-B']
        expected = 4
        a = ebaluazioak.evaluation()
        print(a.mix(allgroups,simultaneous=1))
        result = len(a.mix(allgroups,simultaneous=1))
        self.assertEqual(expected, result)

    def test_mix_2(self):
        allgroups = ['1-A','1-B','2-A','2-B']
        expected = 2
        a = ebaluazioak.evaluation()
        print(a.mix(allgroups,simultaneous=2))
        result = len(a.mix(allgroups,simultaneous=2))
        self.assertEqual(expected, result)
    
    def test_mix_4(self):
        allgroups = ['1-A','1-B','2-A','2-B']
        expected = 1
        a = ebaluazioak.evaluation()
        print(a.mix(allgroups,simultaneous=4))
        result = len(a.mix(allgroups,simultaneous=4))
        self.assertEqual(expected, result)
        
    def test_mix_12(self):    
        allgroups = ['1-A','1-B','2-A','2-B','3-A','3-B','4-A','4-B','4-C','4-D','5-A','5-B','5-C','5-D']
        expected = 3
        a = ebaluazioak.evaluation()
        print(a.mix(allgroups,simultaneous=5))
        result = len(a.mix(allgroups,simultaneous=5))
        self.assertEqual(expected, result)
        
    def test_mix2_2(self):
        allgroups = ['1-A','1-B','2-A','2-B']
        expected = 2
        a = ebaluazioak.evaluation()
        result = len(a.mix2(allgroups,sessions=2))
        self.assertEqual(expected, result)
    
    
    def test_mix2_1(self):
        allgroups = ['1-A','1-B','2-A','2-B']
        expected = 1
        a = ebaluazioak.evaluation()
        result = len(a.mix2(allgroups,sessions=1))
        self.assertEqual(expected, result)

    def test_mix2_3(self):
        allgroups = ['1-A','1-B','2-A','2-B']
        expected = 3
        a = ebaluazioak.evaluation()
        result = len(a.mix2(allgroups,sessions=3))
        self.assertEqual(expected, result)

    
    def test_mix2_4(self):
        allgroups = ['1-A','1-B','2-A','2-B']
        expected = 4
        a = ebaluazioak.evaluation()
        result = len(a.mix2(allgroups,sessions=4))
        self.assertEqual(expected, result)

    def test_mix2_12_5(self):
        allgroups = ['1-A','1-B','2-A','2-B','3-A','3-B','4-A','4-B','5-A','5-B','5-C','5-D']
        expected = 5
        a = ebaluazioak.evaluation()
        result = a.mix2(allgroups,sessions=5)
        self.assertEqual(expected, len(result))


    def test_mix2_12_5_2(self):
        allgroups = ['1-A','1-B','2-A','2-B','3-A','3-B','4-A','4-B','5-A','5-B','5-C','5-D']
        expected = 5
        a = ebaluazioak.evaluation()
        result = a.mix2(allgroups,sessions=5)
        
        e = {1:0,2:3,3:2,4:0}
        r = {1:0,2:0,3:0,4:0}
        for r1 in result:
            r[len(r1)] += 1
        self.assertEqual(e,r)

if __name__ == '__main__':
    unittest.main()