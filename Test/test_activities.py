from ordutegia.MendiFet import MendiFet
from xml.etree import ElementTree as ET
import unittest


class TestMendiFet(unittest.TestCase):

    def test_generate_activity_one_group(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.totalduration = 4
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        activity = ["Teacher","Subject","Year",["Group"],"Total_Duration","Room","Building","Conexion","ConType"] 
        ag = mf.generate_activity(activity,1,1,1)
        at = ET.fromstring("<Activity><Teacher>Teacher</Teacher><Subject>Subject</Subject><Students>Group</Students><Duration>1</Duration><Total_Duration>Total_Duration</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity>")
        self.assertEqual(ET.tostring(at), ET.tostring(ag))

    def test_generate_activity_two_groups(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.totalduration = 4
        mf.group = 3
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        activity = ["Teacher","Subject","Year",["Group1","Group2"],"Total_Duration","Room","Building","Conexion","ConType"] 
        ag = mf.generate_activity(activity,1,1,1)
        at = ET.fromstring("<Activity><Teacher>Teacher</Teacher><Subject>Subject</Subject><Students>Group1</Students><Students>Group2</Students><Duration>1</Duration><Total_Duration>Total_Duration</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity>")
        self.assertEqual(ET.tostring(at), ET.tostring(ag))

    def test_generate_simultaneous_activities_duration1(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Time_Constraints_List><ConstraintActivitiesSameStartingTime><Weight_Percentage>100</Weight_Percentage><Number_of_Activities>2</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>2</Activity_Id><Active>true</Active><Comments> </Comments></ConstraintActivitiesSameStartingTime></Time_Constraints_List><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room2</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>1</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher2</Teacher><Subject>Subject</Subject><Students>Group2</Students><Duration>1</Duration><Total_Duration>1</Total_Duration><Id>2</Id><Activity_Group_Id>2</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= [["Teacher1","Subject","Year",["Group1"],1,"Room1","Building","Conexion","ConType"],["Teacher2","Subject","Year",["Group2"],1,"Room2","Building","Conexion","ConType"]]
        mf.generate_simultaneous_activities(activities, 1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)

    def test_generate_simultaneous_activities_duration2(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Time_Constraints_List><ConstraintMinDaysBetweenActivities><Weight_Percentage>100</Weight_Percentage><Consecutive_If_Same_Day>true</Consecutive_If_Same_Day><Number_of_Activities>2</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>2</Activity_Id><MinDays>1</MinDays><Active>true</Active><Comments> </Comments></ConstraintMinDaysBetweenActivities><ConstraintActivitiesSameStartingTime><Weight_Percentage>100</Weight_Percentage><Number_of_Activities>2</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>3</Activity_Id><Active>true</Active><Comments> </Comments></ConstraintActivitiesSameStartingTime><ConstraintActivitiesSameStartingTime><Weight_Percentage>100</Weight_Percentage><Number_of_Activities>2</Number_of_Activities><Activity_Id>2</Activity_Id><Activity_Id>4</Activity_Id><Active>true</Active><Comments> </Comments></ConstraintActivitiesSameStartingTime></Time_Constraints_List><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>3</Activity_Id><Room>Room2</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>4</Activity_Id><Room>Room2</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>2</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher2</Teacher><Subject>Subject</Subject><Students>Group2</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>3</Id><Activity_Group_Id>3</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher2</Teacher><Subject>Subject</Subject><Students>Group2</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>4</Id><Activity_Group_Id>3</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= [["Teacher1","Subject","Year",["Group1"],2,"Room1","Building","Conexion","ConType"],["Teacher2","Subject","Year",["Group2"],2,"Room2","Building","Conexion","ConType"]]
        mf.generate_simultaneous_activities(activities, 1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)
        
    def test_generate_simultaneous_activities_exclusive_duration1(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Time_Constraints_List /><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room2</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>1</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher2</Teacher><Subject>Subject</Subject><Students>Group2</Students><Duration>1</Duration><Total_Duration>1</Total_Duration><Id>2</Id><Activity_Group_Id>2</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= [["Teacher1","Subject","Year",["Group1"],1,"Room1","Building","Conexion","ConType"],["Teacher2","Subject","Year",["Group2"],1,"Room2","Building","Conexion","ConType"]]
        mf.generate_simultaneous_activities(activities, 1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)

    def test_generate_simultaneous_activities_exclusive_duration2(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Time_Constraints_List><ConstraintMinDaysBetweenActivities><Weight_Percentage>100</Weight_Percentage><Consecutive_If_Same_Day>true</Consecutive_If_Same_Day><Number_of_Activities>2</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>2</Activity_Id><MinDays>1</MinDays><Active>true</Active><Comments> </Comments></ConstraintMinDaysBetweenActivities></Time_Constraints_List><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>3</Activity_Id><Room>Room2</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>4</Activity_Id><Room>Room2</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>2</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher2</Teacher><Subject>Subject</Subject><Students>Group2</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>3</Id><Activity_Group_Id>3</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher2</Teacher><Subject>Subject</Subject><Students>Group2</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>4</Id><Activity_Group_Id>3</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= [["Teacher1","Subject","Year",["Group1"],2,"Room1","Building","Conexion","ConType"],["Teacher2","Subject","Year",["Group2"],2,"Room2","Building","Conexion","ConType"]]
        mf.generate_simultaneous_activities(activities, 1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)
        
    def test_generate_independent_activities_duration1(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List /><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>1</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= ["Teacher1","Subject","Year",["Group1"],1,"Room1","Building","","ConType"]
        mf.generate_independent_activities(activities,1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)     
        
    def test_generate_independent_activities_duration2(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List><ConstraintMinDaysBetweenActivities><Weight_Percentage>100</Weight_Percentage><Consecutive_If_Same_Day>true</Consecutive_If_Same_Day><Number_of_Activities>2</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>2</Activity_Id><MinDays>1</MinDays><Active>true</Active><Comments> </Comments></ConstraintMinDaysBetweenActivities></Time_Constraints_List><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>2</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= ["Teacher1","Subject","Year",["Group1"],2,"Room1","Building","","ConType"]
        mf.generate_independent_activities(activities,1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)
    
    def test_generate_independent_activities_duration2_trinkete(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List /><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Trinkete</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>2</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= ["Teacher1","Subject","Year",["Group1"],2,"Trinkete","Building","","ConType"]
        mf.generate_independent_activities(activities,1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)
            
    def test_generate_independent_activities_duration7(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List><ConstraintMinDaysBetweenActivities><Weight_Percentage>100</Weight_Percentage><Consecutive_If_Same_Day>true</Consecutive_If_Same_Day><Number_of_Activities>4</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>2</Activity_Id><Activity_Id>3</Activity_Id><Activity_Id>4</Activity_Id><MinDays>1</MinDays><Active>true</Active><Comments> </Comments></ConstraintMinDaysBetweenActivities></Time_Constraints_List><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>3</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>4</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>7</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>7</Total_Duration><Id>2</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>7</Total_Duration><Id>3</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>7</Total_Duration><Id>4</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= ["Teacher1","Subject","Year",["Group1"],7,"Room1","Building","","ConType"]
        mf.generate_independent_activities(activities,1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)    
        
    def test_generate_independent_activities_duration8(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List><ConstraintMinDaysBetweenActivities><Weight_Percentage>100</Weight_Percentage><Consecutive_If_Same_Day>true</Consecutive_If_Same_Day><Number_of_Activities>4</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>2</Activity_Id><Activity_Id>3</Activity_Id><Activity_Id>4</Activity_Id><MinDays>1</MinDays><Active>true</Active><Comments> </Comments></ConstraintMinDaysBetweenActivities></Time_Constraints_List><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>3</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>4</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>8</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>8</Total_Duration><Id>2</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>8</Total_Duration><Id>3</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>8</Total_Duration><Id>4</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= ["Teacher1","Subject","Year",["Group1"],8,"Room1","Building","","ConType"]
        mf.generate_independent_activities(activities,1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)  
        
    def test_generate_independent_activities_duration9(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List><ConstraintMinDaysBetweenActivities><Weight_Percentage>100</Weight_Percentage><Consecutive_If_Same_Day>true</Consecutive_If_Same_Day><Number_of_Activities>5</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>2</Activity_Id><Activity_Id>3</Activity_Id><Activity_Id>4</Activity_Id><Activity_Id>5</Activity_Id><MinDays>1</MinDays><Active>true</Active><Comments> </Comments></ConstraintMinDaysBetweenActivities></Time_Constraints_List><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>3</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>4</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>5</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>9</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>9</Total_Duration><Id>2</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>9</Total_Duration><Id>3</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>9</Total_Duration><Id>4</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>9</Total_Duration><Id>5</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activities= ["Teacher1","Subject","Year",["Group1"],9,"Room1","Building","","ConType"]
        mf.generate_independent_activities(activities,1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)  
        
    def test_generate_independent_activities_duration10(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List><ConstraintMinDaysBetweenActivities><Weight_Percentage>100</Weight_Percentage><Consecutive_If_Same_Day>true</Consecutive_If_Same_Day><Number_of_Activities>5</Number_of_Activities><Activity_Id>1</Activity_Id><Activity_Id>2</Activity_Id><Activity_Id>3</Activity_Id><Activity_Id>4</Activity_Id><Activity_Id>5</Activity_Id><MinDays>1</MinDays><Active>true</Active><Comments> </Comments></ConstraintMinDaysBetweenActivities></Time_Constraints_List><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>3</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>4</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>5</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>10</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>10</Total_Duration><Id>2</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>10</Total_Duration><Id>3</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>10</Total_Duration><Id>4</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>10</Total_Duration><Id>5</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activity= ["Teacher1","Subject","Year",["Group1"],10,"Room1","Building","","ConType"]
        mf.generate_independent_activities(activity,1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)  
        
    def test_generate_independent_activities_duration16(self):
        mf = MendiFet()
        mf.teacher = 0
        mf.subject = 1
        mf.group = 3
        mf.totalduration = 4
        mf.room = 5
        mf.con = 6
        mf.contype = 7
        mf.fetxml = ET.fromstring("<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List/><Space_Constraints_List/><Activities_List/></fet>")
        rt = b'<fet><Days_List><Name>A</Name><Name>B</Name><Name>C</Name><Name>D</Name><Name>E</Name></Days_List><Time_Constraints_List /><Space_Constraints_List><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>1</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>2</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>3</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>4</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>5</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>6</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>7</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom><ConstraintActivityPreferredRoom><Weight_Percentage>100</Weight_Percentage><Activity_Id>8</Activity_Id><Room>Room1</Room><Permanently_Locked>true</Permanently_Locked><Active>true</Active><Comments> </Comments></ConstraintActivityPreferredRoom></Space_Constraints_List><Activities_List><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>2</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>2</Total_Duration><Id>2</Id><Activity_Group_Id>2</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>2</Total_Duration><Id>3</Id><Activity_Group_Id>3</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>2</Total_Duration><Id>4</Id><Activity_Group_Id>4</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>2</Total_Duration><Id>5</Id><Activity_Group_Id>5</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>2</Total_Duration><Id>6</Id><Activity_Group_Id>6</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>2</Total_Duration><Id>7</Id><Activity_Group_Id>7</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity><Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>2</Duration><Total_Duration>2</Total_Duration><Id>8</Id><Activity_Group_Id>8</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity></Activities_List></fet>'
        activity= ["Teacher1","Subject","Year",["Group1"],16,"Room1","Building","","ConType"]
        mf.generate_independent_activities(activity,1)
        ot = ET.tostring(mf.fetxml)
        self.assertEqual(rt,ot)  
       
    def test_generate_activity_1Group(self):
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
        rt = b'<Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity>'
        activity= ["Teacher1","Subject","Year",["Group1"],2,"Room1","Building","","ConType"]
        ot = ET.tostring(mf.generate_activity(activity, 1, 1, duration='1'))
        self.assertEqual(rt,ot)
        
    def test_generate_activity_2Group(self):
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
        rt = b'<Activity><Teacher>Teacher1</Teacher><Subject>Subject</Subject><Students>Group1</Students><Students>Group2</Students><Duration>1</Duration><Total_Duration>2</Total_Duration><Id>1</Id><Activity_Group_Id>1</Activity_Group_Id><Active>true</Active><Comments> </Comments></Activity>'
        activity= ["Teacher1","Subject","Year",["Group1","Group2"],2,"Room1","Building","","ConType"]
        ot = ET.tostring(mf.generate_activity(activity, 1, 1, duration='1'))
        self.assertEqual(rt,ot)
        
        
if __name__ == '__main__':
    unittest.main()