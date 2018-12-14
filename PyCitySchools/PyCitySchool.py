# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset
school_data_complete = pd.merge(student_data, school_data, 
how="left", on=["school_name", "school_name"])

#District Summary
schools = school_data["school_name"]
students = student_data["student_name"]
total_budget = school_data["budget"].sum()
avg_math = student_data["math_score"].mean()
avg_reading = student_data["reading_score"].mean()

math_score = student_data.loc[(student_data["math_score"] >= 70), :]
pass_math = len(math_score)    
percent_math = (pass_math/(len(students)))*100

reading_score = student_data.loc[(student_data["reading_score"] >= 70), :]
pass_reading = len(reading_score)   
percent_reading = (pass_reading/(len(students)))*100

overall_pass = (avg_math +avg_reading)/2

schoolandstudent_summary = pd.DataFrame(
    [{"Total Schools": len(schools),"Total Students": len(students), "Total Budget": total_budget, 
      "Average Math Score": avg_math, "Average Reading Score": avg_reading, "% Passing Math": percent_math, 
      "% Passing Reading": percent_reading, "% Overall Passing Rate": overall_pass}])

schoolandstudent_summary

#Top Performing Schools (By Passing Rate)
merge_schoolsummary = pd.merge(student_data, school_data, on="school_name", how = "outer")

del merge_schoolsummary['Student ID']
del merge_schoolsummary['gender']
del merge_schoolsummary['grade']

#start_point1 = pd.DataFrame(merge_schoolsummary.set_index('type').groupby(['school_name']).count())

start_point = pd.DataFrame(merge_schoolsummary.groupby(['school_name', 'type']).count())

total_budget_school = pd.DataFrame(merge_schoolsummary).groupby(['school_name', 'type']).mean()['budget']
total_students = pd.DataFrame(merge_schoolsummary).groupby(['school_name', 'type']).count()['student_name']
avg_math_school = pd.DataFrame(merge_schoolsummary.groupby(['school_name', 'type']).mean()['math_score'])
avg_reading_school = pd.DataFrame(merge_schoolsummary.groupby(['school_name', 'type']).mean()['reading_score'])
budget_per_student = pd.DataFrame(total_budget_school/total_students)

pass_math = merge_schoolsummary.loc[(merge_schoolsummary["math_score"] == 70)|(merge_schoolsummary["math_score"] > 70), 
                                    ["school_name", 'type', "math_score"]]
pass_reading = merge_schoolsummary.loc[(merge_schoolsummary["reading_score"] == 70)|(merge_schoolsummary["reading_score"] > 70), 
                                    ["school_name", 'type', "reading_score"]]

pass_math_df = pd.DataFrame(pass_math).groupby(['school_name', 'type']).count()['math_score']
pass_reading_df = pd.DataFrame(pass_reading).groupby(['school_name', 'type']).count()['reading_score']

percent_math_school = pd.DataFrame((pass_math_df/total_student)*100)
percent_reading_school = pd.DataFrame((pass_reading_df/total_student)*100)

overall_pass_school = pd.DataFrame((percent_math_school + percent_reading_school)/2)


del start_point['student_name']
del start_point['School ID']
del start_point['reading_score']
del start_point['math_score']
del start_point['size']
del start_point['budget']

#start_point['School Type'] = 
start_point['Total Students'] = total_students
start_point['Total School Budget'] = total_budget_school
start_point['Per Student Budget'] = budget_per_student
start_point['Average Math Score'] = avg_math_school
start_point['Average Reading Score'] = avg_reading_school
start_point['% Passing Math'] = percent_math_school
start_point['% Passing Reading'] = percent_reading_school
start_point['% Overall Passing Rate'] = overall_pass_school

initial_summary = start_point


top_summary = initial_summary.sort_values ("% Overall Passing Rate", ascending = False).head()

top_summary


#Bottom Performing Schools (By Passing Rate)
bottom_summary = initial_summary.sort_values ("% Overall Passing Rate", ascending = True).head()

bottom_summary


#Math Scores by Grade
merge_schoolgrade = pd.merge(student_data, school_data, on="school_name", how = "outer")

del merge_schoolgrade['Student ID']
del merge_schoolgrade['School ID']
del merge_schoolgrade['student_name']
del merge_schoolgrade['gender']
del merge_schoolgrade['budget']
del merge_schoolgrade['size']
del merge_schoolgrade['type']
del merge_schoolgrade['reading_score']

math_9 = merge_schoolsummary.loc[(merge_schoolgrade["grade"] == '9th'), ["school_name", "math_score"]]
math_10 = merge_schoolsummary.loc[(merge_schoolgrade["grade"] == '10th'), ["school_name", "math_score"]]
math_11 = merge_schoolsummary.loc[(merge_schoolgrade["grade"] == '11th'), ["school_name", "math_score"]]
math_12 = merge_schoolsummary.loc[(merge_schoolgrade["grade"] == '12th'), ["school_name", "math_score"]]

math_9_df = pd.DataFrame(math_9.groupby(['school_name']).mean()['math_score'])
math_10_df = pd.DataFrame(math_10.groupby(['school_name']).mean()['math_score'])
math_11_df = pd.DataFrame(math_11.groupby(['school_name']).mean()['math_score'])
math_12_df = pd.DataFrame(math_12.groupby(['school_name']).mean()['math_score'])

merge1 = pd.merge(math_9_df, math_10_df, on=['school_name'], how ='outer', suffixes = (' 9th', ' 10th'))
merge2 = pd.merge(merge1, math_11_df, on=['school_name'], how ='outer')
merge3 = pd.merge(merge2, math_12_df, on=['school_name'], how ='outer', suffixes = (' 11th', ' 12th'))

mathscore_summary  = merge3.rename(columns={'math_score 9th': '9th', 'math_score 10th': '10th',
                                           'math_score 11th': '11th', 'math_score 12th': '12th'})

mathscore_summary


#Reading Score by Grade
read_9 = merge_schoolsummary.loc[(merge_schoolgrade["grade"] == '9th'), ["school_name", "reading_score"]]
read_10 = merge_schoolsummary.loc[(merge_schoolgrade["grade"] == '10th'), ["school_name", "reading_score"]]
read_11 = merge_schoolsummary.loc[(merge_schoolgrade["grade"] == '11th'), ["school_name", "reading_score"]]
read_12 = merge_schoolsummary.loc[(merge_schoolgrade["grade"] == '12th'), ["school_name", "reading_score"]]

read_9_df = pd.DataFrame(read_9.groupby(['school_name']).mean()['reading_score'])
read_10_df = pd.DataFrame(read_10.groupby(['school_name']).mean()['reading_score'])
read_11_df = pd.DataFrame(read_11.groupby(['school_name']).mean()['reading_score'])
read_12_df = pd.DataFrame(read_12.groupby(['school_name']).mean()['reading_score'])

merge1 = pd.merge(read_9_df, read_10_df, on=['school_name'], how ='outer', suffixes = (' 9th', ' 10th'))
merge2 = pd.merge(merge1, read_11_df, on=['school_name'], how ='outer')
merge3 = pd.merge(merge2, read_12_df, on=['school_name'], how ='outer', suffixes = (' 11th', ' 12th'))

readscore_summary  = merge3.rename(columns={'reading_score 9th': '9th', 'reading_score 10th': '10th',
                                           'reading_score 11th': '11th', 'reading_score 12th': '12th'})

readscore_summary


#Scores by School Spending
# Sample bins. Feel free to create your own bins.
spending_bins = [0, 585, 615, 645, 675]
group_names = ["<$585", "$585-615", "$615-645", "$645-675"]

spending_analysis = pd.DataFrame(initial_summary )

spending_analysis["Spending Ranges (Per Student)"] = pd.cut(score_analysis["Per Student Budget"], spending_bins, labels=group_names)

del spending_analysis['Per Student Budget']
del spending_analysis['Total Students']
del spending_analysis['Total School Budget']

spending_analysis


Scores by School Size
# Sample bins. Feel free to create your own bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

size_analysis = pd.DataFrame(initial_summary)

size_analysis["School Size"] = pd.cut(size_analysis["Total Students"], size_bins, labels=group_names)

del size_analysis['Per Student Budget']
del size_analysis['Total Students']
del size_analysis['Total School Budget']

size_analysis.groupby('School Size').head()


#Scores by School Type
type_analysis = pd.DataFrame(initial_summary)

del type_analysis['Per Student Budget']
del type_analysis['Total Students']
del type_analysis['Total School Budget']

type_analysis.groupby('School Type').head()