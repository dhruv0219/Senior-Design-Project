import pandas as pd
import os

def audit_transcript(file_name, track):
    
    # things we need to grab for audit report:
    # name, plan, student id, major, track
    # plan = masters, major = computer science

    core_hours = 0
    core_earned = 0     # required: 3.19

    elective_hours = 0
    elective_earned = 0 # required: 3.00

    total_hours = 0
    combined_earned = 0 # required: -

    required_elective_hours = 0
    required_core_hours = 0
    other_elective_hours = 0

    if track == "trad":
        required_elective_hours = 15
        required_core_hours = 15
        required_other_elective_hours = 3
    if track == "nat":
        required_elective_hours = 15
        required_core_hours = 15
        required_other_elective_hours = 3
    if track == "is":
        required_elective_hours = 15
        required_core_hours = 15
        required_other_elective_hours = 3
    if track == "ic":
        required_elective_hours = 15
        required_core_hours = 15
        required_other_elective_hours = 3
    if track == "sys":
        required_elective_hours = 15
        required_core_hours = 15
        required_other_elective_hours = 3
    if track == "ds":
        required_elective_hours = 15
        required_core_hours = 15
        required_other_elective_hours = 3
    if track == "cs":
        required_elective_hours = 15
        required_core_hours = 15
        required_other_elective_hours = 3

    # read in course catalog classes to 
    df = pd.read_excel("classes.xlsx")

    # get all core classes for the track
    core_classes = df.loc[ (df['Track'] == track) & (df['Core'] == "y") ]
    core_classes = core_classes['Number']

    core_classes_taken = list()
    elective_courses_taken = list()

    classes_completed = list()

    file = open(file_name)
    lines = file.readlines()

    for line in lines:
        line = line.strip("\n")

        if line.startswith("Name: "):
            name_arr = line.split(":")
            name = name_arr[1].lstrip()

        if line.startswith("Student ID: "):
            id_arr = line.split(":")
            student_id = id_arr[1].lstrip()

        line_arr = line.split(" ")

        if line.startswith("CS "):
            line_arr = line.split(" ")
            class_num = line_arr[1]


            if line_arr[len(line_arr) - 2] == '0.000':
                    continue

            # look up the class to see if it is a core class
            # if it is a core class for the corresponding track, add to core hours, otherwise add to elective
            #if df.loc[(df['Number'] == line_arr[1]) & (df['Track'] == track)].any().all():
            if core_classes[core_classes.isin([int(line_arr[1])])].any() and core_hours < required_core_hours:

                core_hours = core_hours + 3
                core_earned = core_earned + float(line_arr[len(line_arr) - 1])
                core_classes_taken.append(line_arr[1])
                
                # now all core classes left are what we need to print
                core_classes = core_classes.loc[core_classes != int(line_arr[1])]
                continue
            
            if elective_hours < required_elective_hours:
                elective_hours = elective_hours + 3
                elective_earned = elective_earned + float(line_arr[len(line_arr) - 1])
                classes_completed.append(line_arr[1])
                elective_courses_taken.append(line_arr[1])
                continue

            if other_elective_hours < required_other_elective_hours:
                other_elective_hours = other_elective_hours + 3
                combined_earned = combined_earned + float(line_arr[len(line_arr) - 1])
                classes_completed.append(line_arr[1])
                elective_courses_taken(line_arr[1])
                continue

        if line.startswith("ESCS ") and other_elective_hours < 3:
            classes_completed.append(line_arr[1])
            continue

    core_gpa = core_earned / float(core_hours)
    elective_gpa = elective_earned / float(elective_hours)
    combined_gpa = (elective_earned + core_earned + combined_earned) / (other_elective_hours + elective_hours + core_hours)

    core_gpa = round(core_gpa, 3)
    elective_gpa = round(elective_gpa, 3)
    combined_gpa = round(combined_gpa, 3)

    file.close()

    core_classes = core_classes.to_list()

    generate_audit_report(student_id, track, name, core_classes_taken, core_classes, core_gpa, elective_gpa, combined_gpa, elective_courses_taken)

    return 


def generate_audit_report(student_id, track, name, core_classes_taken, core_classes_left, core_gpa, elective_gpa, combined_gpa, elective_courses_taken):

    filename = 'audit_report_' + str(student_id) + ".txt"
    path = "/Users/wavyj/Documents/"
    path = os.path.join(path, filename)

    if track == "trad":
        track = "Traditional"
    if track == "nat":
        track = "Networks and Telecommunications"
    if track == "is":
        track = "Intelligent Systems"
    if track == "ic":
        track = "Interactive Computing"
    if track == "sys":
        track == "Systems"
    if track == "ds":
        track = "Data Science"
    if track == "cs":
        track = "Cybersecurity"

    elective_courses_taken = [str(i) for i in elective_courses_taken]
    elective_courses_taken_str = ", CS ".join(elective_courses_taken)
    elective_courses_taken_str = "CS " + elective_courses_taken_str

    core_classes_taken = [str(i) for i in core_classes_taken]
    core_classes_taken_str = ", CS ".join(core_classes_taken)
    core_classes_taken_str = "CS " + core_classes_taken_str

    core_classes_left = [str(i) for i in core_classes_taken]
    core_courses_left_str = ", CS".join(core_classes_left)
    core_courses_left_str = "CS " + core_courses_left_str

    with open(filename, 'w') as f:
        f.write("Audit Report\n\n")
        f.write("Name: " + name + "\n")
        f.write("Plan: Master\n\n")
        f.write("Major: Computer Science")
        f.write("Track: " + track + "\n\n")
        f.write("Core GPA: " + str(core_gpa) + "\n")
        f.write("Elective GPA: " + str(elective_gpa) + "\n")
        f.write("Combined GPA: " + str(combined_gpa) + "\n\n")
        f.write("Core Courses: " + core_classes_taken_str + "\n")
        f.write("Elective Courses: " + elective_courses_taken_str + "\n\n")
        f.write("Leveling Courses and Pre-requisites from Admission Letter: \n\n")
        f.write("Outstanding Requirements: \n\n")
        f.write("Core Courses Remaining: " + core_courses_left_str + "\n")

    return 

