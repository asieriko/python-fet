from ordutegia.MendiFet import MendiFet
from xml.etree import ElementTree as ET
import unittest


class TestMendiFet(unittest.TestCase):

    def test_generate_room(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        rg = mf.generate_room(1,"room1",1)
        rt = ET.fromstring("<ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom>")
        self.assertEqual(ET.tostring(rt), ET.tostring(rg[0]))
     
    def test_generate_room_2(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        rg = mf.generate_room(1,"room1",2)
        rt1 = ET.fromstring("<ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom>")
        rt2 = ET.fromstring("<ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom>")
        rt = [rt1,rt2]
        self.assertEqual(ET.tostring(rt[0]), ET.tostring(rg[0]))   
        self.assertEqual(ET.tostring(rt[1]), ET.tostring(rg[1]))
 
    def test_group_long_activities_3(self):
        mf = MendiFet()
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List></fet>")
        r = mf.group_long_activities(3)
        self.assertEqual([1,1,1,0,0], r)

    def test_group_long_activities_6(self):
        mf = MendiFet()
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List></fet>")
        r = mf.group_long_activities(6)
        self.assertEqual([2,2,2,0,0], r)

    def test_group_long_activities_6_notCompact(self):
        mf = MendiFet()
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List></fet>")
        r = mf.group_long_activities(6,False)
        self.assertEqual([2,1,1,1,1], r)

    def test_group_long_activities_8(self):
        mf = MendiFet()
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List></fet>")
        r = mf.group_long_activities(8)
        self.assertEqual([2,2,2,2,0], r)
    
    def test_group_long_activities_10(self):
        mf = MendiFet()
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List></fet>")
        r = mf.group_long_activities(10)
        self.assertEqual([2,2,2,2,2], r)
        
    def test_group_long_activities_13(self):
        mf = MendiFet()
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List></fet>")
        r = mf.group_long_activities(13)
        self.assertEqual([3,3,3,2,2], r)

    def test_group_long_activities_16(self):
        mf = MendiFet()
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List></fet>")
        r = mf.group_long_activities(16)
        self.assertEqual([4,3,3,3,3], r)
    
    def test_group_long_activities_22(self):
        mf = MendiFet()
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List></fet>")
        r = mf.group_long_activities(22)
        self.assertEqual([5,5,4,4,4], r)
        
    def test_generate_multiple_teachers(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.year = 2
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Time_Constraints_List /><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>7</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher2</Teacher><Teacher>Teacher3</Teacher><Teacher>Teacher4</Teacher><Subject>MB</Subject><Students>B</Students><Duration>1</Duration><Total_Duration>1</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        conexion = ['R', ['MB', 'B', '', 1, '7', '2', 'R', 'bilera'], ['Teacher2', 'Teacher3', 'Teacher4']]
        mf.generate_multiple_teachers(conexion, 1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)
       
    def test_generate_start_time(self):
        mf = MendiFet()
        Id = 1
        activitiesnumber = 2
        activitiesduration = 2
        r = mf.generate_start_time(Id, activitiesnumber, activitiesduration)
        o0 = b'<ConstraintActivitiesSameStartingTime><Weight_Percentage>100</Weight_Percentage><Number_of_Activities>2</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>3</Activity_Id><Active>true</Active><Comments> </Comments></ConstraintActivitiesSameStartingTime>'
        o1 = b'<ConstraintActivitiesSameStartingTime><Weight_Percentage>100</Weight_Percentage><Number_of_Activities>2</Number_of_Activities><Activity_Id>2</Activity_Id><Activity_Id>4</Activity_Id><Active>true</Active><Comments> </Comments></ConstraintActivitiesSameStartingTime>'
        self.assertEqual(o0, ET.tostring(r[0]))
        self.assertEqual(o1, ET.tostring(r[1]))
          
    def test_generate_min_days(self):
        mf = MendiFet()
        Id = 1
        number = 3
        r = ET.tostring(mf.generate_min_days(Id, number))
        o = b'<ConstraintMinDaysBetweenActivities><Weight_Percentage>100</Weight_Percentage><Consecutive_If_Same_Day>true</Consecutive_If_Same_Day><Number_of_Activities>3</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>2</Activity_Id><Activity_Id>3</Activity_Id><MinDays>1</MinDays><Active>true</Active><Comments> </Comments></ConstraintMinDaysBetweenActivities>'
        self.assertEqual(r,o)
        
    def test_generate_meetings_groups(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.year = 2
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 7
        mf.contype = 8
        activities = [['Teacher2', 'MB', 'B', '', 1, '7', '2', 'R', 'bilera'], ['Teacher3', 'MB', 'B', '', 1, '7', '2', 'R', 'bilera'],['Teacher4', 'MB', 'B','',  1, '7', '2', 'R', 'bilera']]
        o = [['R',['MB', 'B', '', 1, '7', '2', 'R', 'bilera'],['Teacher2', 'Teacher3', 'Teacher4']]]
        r = mf.generate_meetings_groups(activities)
        self.assertEqual(o,r)
        
    def test_generate_meetings_groups2(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.year = 2
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 7
        mf.contype = 8
        activities = [['Teacher2', 'MB', 'B', '', 1, '7', '2', 'R', 'bilera'], ['Teacher3', 'MB', 'B', '', 1, '7', '2', 'R', 'bilera'],['Teacher4', 'MB', 'B','',  1, '7', '2', 'R', 'bilera'],['Teacher5', 'MB', 'D', '', 1, '7', '2', 'S', 'bilera'], ['Teacher6', 'MB', 'D', '', 1, '7', '2', 'S', 'bilera'],['Teacher7', 'MB', 'D','',  1, '7', '2', 'S', 'bilera']]
        o = [['R',['MB', 'B', '', 1, '7', '2', 'R', 'bilera'],['Teacher2', 'Teacher3', 'Teacher4']],['S',['MB', 'D', '', 1, '7', '2', 'S', 'bilera'],['Teacher5', 'Teacher6', 'Teacher7']]]
        r = mf.generate_meetings_groups(activities)
        self.assertEqual(o,r)
        
    def test_generate_hautazkoak(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.year = 2
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 7
        mf.contype = 8
        activities = [['Teacher2', 'MB1', 'B', '', 1, '7', '2', 'R', 'h'], ['Teacher3', 'MB2', 'B', '', 1, '7', '2', 'R', 'h'],['Teacher4', 'MB3', 'B', '', 1, '7', '2', 'R', 'h']]
        o = [['R', ['Teacher2', 'MB1', 'B', '', 1, '7', '2', 'R', 'h'], ['Teacher3', 'MB2', 'B', '', 1, '7', '2', 'R', 'h'], ['Teacher4', 'MB3', 'B', '', 1, '7', '2', 'R', 'h']]]
        r = mf.generate_hautazkoak(activities)
        self.assertEqual(o,r)
        
    def test_incompatibilities_T(self):
        mf = MendiFet()
        i = mf.incompatiblegroups('5', 'Fisika Kimika', {'5', 'H', 'Historia'}, {"5":{"Fisika Kimika":["Historia","Latina","Ekonomia","Matematika GGZZ","Marrazketa Artistikoa"],"Matematika": ["Historia","Latina","Ekonomia","Matematika GGZZ","Marrazketa Artistikoa"]}})
        self.assertEqual(i, True)
    
    def test_incompatibilities_F(self):
        mf = MendiFet()
        i = mf.incompatiblegroups('5', 'Matematika', {'5', 'Fisika Kimika'}, {"5":{"Fisika Kimika":["Historia","Latina","Ekonomia","Matematika GGZZ","Marrazketa Artistikoa"],"Matematika": ["Historia","Latina","Ekonomia","Matematika GGZZ","Marrazketa Artistikoa"]}})
        self.assertEqual(i, False)
        
if __name__ == '__main__':
    unittest.main()