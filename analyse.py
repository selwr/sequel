import os
import warnings
import humanize
import PyPDF2
import datetime as dt

from PyPDF2 import PdfFileReader
from tabulate import tabulate

warnings.filterwarnings("ignore")

print("\nStarting...\n")

# Getting current working directory and its contents
in_dir = os.path.dirname(os.path.realpath(__file__))

directory_contents = os.listdir(in_dir)


# Getting each of the subject names
subjects = []

for folder in directory_contents:

    if (os.path.isdir(folder)) and ("." not in folder):

        subjects.append(folder)

subjects = sorted(subjects)


# Setting up the lists for the data
overallData = [[0, 0, 0, 0]]

subjectData = []

subjectPaperVals = []
subjectTopicVals = []
subjectPageVals = []
subjectSizeVals = []

corruptFiles = []

topicsOverall = []

# Getting all the data
for subject in subjects:

    topicsSubject = []

    subjectPapers = 0
    subjectTopics = 0
    subjectPages = 0
    subjectSize = 0

    for filename in os.listdir(in_dir + "/" + subject):

        if ".pdf" in filename:
            
            # Getting papers data
            overallData[0][0] += 1
            subjectPapers += 1


            # Getting size data
            overallData[0][3] += os.path.getsize(in_dir + "/" + subject + "/" + filename)
            subjectSize += os.path.getsize(in_dir + "/" + subject + "/" + filename)


            # Getting pages data
            with open(in_dir + "/" + subject + "/" + filename, "rb") as f:

                try:

                    pdf = PdfFileReader(f)

                except PyPDF2.errors.PdfReadError:

                    corruptFiles.append(filename)
                

                try:

                    overallData[0][2] += pdf.getNumPages()
                    subjectPages += pdf.getNumPages()

                except PyPDF2.errors.PdfReadError:

                    corruptFiles.append(subject + " : " + filename)
                
                except ValueError:

                    corruptFiles.append(subject + " : " + filename)


            # Getting topics data
            if "[" not in filename:

                overallData[0][1] += 1
                subjectTopics += 1

            if ("[" in filename) and ("[1]" in filename):

                overallData[0][1] += 1
                subjectTopics += 1
            

            # Getting topics
            topicsSubject.append(filename[:-4])
        

    # Appending all values to necessary lists
    subjectPaperVals.append(subjectPapers)
    subjectTopicVals.append(subjectTopics)
    subjectPageVals.append(subjectPages)
    subjectSizeVals.append(subjectSize)

    subjectData.append([subject, str(subjectPapers), str(subjectTopics), str(subjectPages), humanize.naturalsize(subjectSize, binary=False, format="%.1f")])


    # Sorting out topic names
    for topic in topicsSubject:

        if "[" in topic:

            topicsSubject[topicsSubject.index(topic)] = topicsSubject[topicsSubject.index(topic)][:topic.index("[")-1]
    

    topicsSubjectSet = set(topicsSubject)

    topicsSubjectList = list(topicsSubjectSet)


    for topic in topicsSubjectSet:

        count = topicsSubject.count(topic)

        if count > 1:

            topicsSubjectList[topicsSubjectList.index(topic)] = topicsSubjectList[topicsSubjectList.index(topic)] + f" [{count}]"


    topicsSubject = sorted(topicsSubjectList)

    topicsOverall.append([subject, topicsSubject])


    print(f"{subject} done!")


# Writing list of corrupt files, if necessary
if corruptFiles != []:

    with open("Corruptions.txt", "w") as f:

        f.write("## Corrupt Files\n\n")

        for filename in corruptFiles:

            f.write("* " + filename + "\n")

    print("\n--> Fix files listed in 'Corruptions.txt'\n")


# Getting the total size, maximum values and formatting them in their respective lists
totalSize = overallData[0][3]

maxPapers = max(subjectPaperVals)
maxTopics = max(subjectTopicVals)
maxPages = max(subjectPageVals)
maxSize = max(subjectSizeVals)

for subject in subjectData:

    if int(subject[1]) == maxPapers:

        subjectData[subjectData.index(subject)][1] = "[ " + subject[1] + " ]"


    if int(subject[2]) == maxTopics:

        subjectData[subjectData.index(subject)][2] = "[ " + subject[2] + " ]"


    if int(subject[3]) == maxPages:

        subjectData[subjectData.index(subject)][3] = "[ " + subject[3] + " ]"


    if humanize.naturalsize(maxSize, binary=False, format="%.1f") == subject[4]:

        subjectData[subjectData.index(subject)][4] = "[ " + subject[4] + " ]"


# Formatting and tabulating the overall data
for x in range(len(overallData[0]) - 1):

    overallData[0][x] = str(overallData[0][x])

overallData[0][3] = humanize.naturalsize(overallData[0][3], binary=False, format="%.2f")

overall_headers = ["Total papers", "Total topics", "Total pages", "Total size"]
overall_table = tabulate(overallData, overall_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center"))


# Tabulating subject data
subject_headers = ["Subject", "No. Papers", "No. Topics", "No. Pages", "   Size   "]
subjects_table = tabulate(subjectData, subject_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center"))


# Getting date and time info
dateNow = str(dt.date.today())
dateNow = dateNow.split("-")[::-1]
now = dt.datetime.now()
timeNow = now.strftime("%H:%M:%S")


# Writing all data to file
with open("Report.txt", "w") as f:

    f.write(f"""## Report

ID {totalSize * 8}

Last updated on {dateNow[0]}/{dateNow[1]}/{dateNow[2]} at {timeNow}


# Numerical Analysis

""")

    f.write(overall_table + "\n"*2)
    f.write(subjects_table + "\n"*4)

    f.write("# Contents\n\n\n")

    for subject in topicsOverall:

        f.write(f"~ {subject[0]} ~\n\n")

        for topic in subject[1]:

            f.write(f"* {topic}\n")


        f.write("\n\n\n")


print("\nDone!\n")
