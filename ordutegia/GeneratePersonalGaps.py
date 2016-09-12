import csv
file = "/home/zuzendaria/Horario-16-17-ind_teachers.csv"
days = ''
week1 = ''
week2 = ''
week3 = ''
with open(file) as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
        #print(row['Teacher'], row['day'],row['week_min'],row['week_max'])
        day='''<ConstraintTeacherMaxGapsPerDay>
                <Weight_Percentage>100</Weight_Percentage>
                <Teacher_Name>{}</Teacher_Name>
                <Max_Gaps>{}</Max_Gaps>
                <Active>true</Active>
                <Comments></Comments>
        </ConstraintTeacherMaxGapsPerDay>
        '''.format(row['Teacher'],row['day'])
        days += day
        week='''<ConstraintTeacherMaxGapsPerWeek>
            <Weight_Percentage>100</Weight_Percentage>
            <Teacher_Name>{}</Teacher_Name>
            <Max_Gaps>{}</Max_Gaps>
            <Active>true</Active>
            <Comments></Comments>
        </ConstraintTeacherMaxGapsPerWeek>
        '''.format(row['Teacher'],row['week_min'])
        week1 += week
        week='''<ConstraintTeacherMaxGapsPerWeek>
            <Weight_Percentage>100</Weight_Percentage>
            <Teacher_Name>{}</Teacher_Name>
            <Max_Gaps>{}</Max_Gaps>
            <Active>true</Active>
            <Comments></Comments>
        </ConstraintTeacherMaxGapsPerWeek>
        '''.format(row['Teacher'],str((int(row['week_min'])+int(row['week_max']))//2))
        week2 += week
        week='''<ConstraintTeacherMaxGapsPerWeek>
            <Weight_Percentage>100</Weight_Percentage>
            <Teacher_Name>{}</Teacher_Name>
            <Max_Gaps>{}</Max_Gaps>
            <Active>true</Active>
            <Comments></Comments>
        </ConstraintTeacherMaxGapsPerWeek>
        '''.format(row['Teacher'],row['week_max'])
        week3 += week
#print(day,week)
    
#print("Days:")
#print(days)
#print("weekmin:")
#print(week1)
print("weekmed:")
print(week2)
#print("weekmax:")
#print(week3)