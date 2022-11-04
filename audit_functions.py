import PyPDF2
import pandas as pd

def audit_transcript(file_name, track):
    
    # things we need to grab for audit report:
    # name, plan, student id, major, track
    # plan = masters, major = computer science

    pdf_file = open(file_name, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    num_pages = pdf_reader.numPages
    

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

    classes_completed = list()

    for page_num in range(num_pages):
        page = pdf_reader.getPage(page_num)
        text_file = page.extract_text()

        for line in text_file:
            if line.startswith("CS"):
                line_arr = line.split(" ")
                class_num = line_arr[1]

                # look up the class to see if it is a core class
                # if it is a core class for the corresponding track, add to core hours, otherwise add to elective
                if ((df['Number'] == line_arr[1]) and (df['Track'] == track).any()):
                    core_hours += 3
                    core_earned += line_arr[len(line_arr) - 1]
                    classes_completed.append(line_arr[1])
                    continue
                
                if elective_hours < required_elective_hours:
                    elective_hours += 3
                    elective_earned += line_arr[len(line_arr) - 1]
                    classes_completed.append(line_arr[1])
                    continue

                if other_elective_hours < required_elective_hours:
                    other_elective_hours += 3
                    combined_earned += line_arr[len(line_arr) - 1]
                    classes_completed.append(line_arr[1])
                    continue

            if line.startswith("ESCS"):
                other_elective_hours += 3
                combined_earned += line_arr[len(line_arr) - 1]
                classes_completed.append(line_arr[1])
                continue



    pdf_file.close()
    return 


def generate_audit_report():
    return 