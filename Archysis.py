# Archysis v3.2.1
# by Sam Wallis-Riches, 2022

import os
import warnings
import textwrap
import humanize
import PyPDF2
import datetime as dt
import numpy as np

from PyPDF2 import PdfFileReader
from fpdf import FPDF
from tabulate import tabulate

warnings.filterwarnings("ignore")

separator = "-"

print("\nStarting...\n")


# Getting current working directory and its contents
in_dir = os.path.dirname(os.path.realpath(__file__))

directory_contents = os.listdir(in_dir)


# Getting directory of font file
fontFile = 'Menlo-Regular.ttf'
fontFileDir = None

for root, dirs, files in os.walk(r'/Users'):

    for name in files:

        if name == fontFile and "Mobile Documents" not in root and "Library" not in root:

            fontFileDir = os.path.abspath(os.path.join(root, name))[:-len(fontFile)]

            break

    if fontFileDir != None:

        break


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

                    corruptFiles.append(subject + " : " + filename)
                

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

        text.append("## Corrupt Files\n\n")

        for filename in corruptFiles:

            text.append("* " + filename + "\n")

    print("\n--> Fix files listed in 'Corruptions.txt'\n")

    exit()


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
overall_table = overall_table.split("\n")


# Formatting and tabulating the subject data
subject_headers = ["Subject", "No. Papers", "No. Topics", "No. Pages", "   Size   "]
subjects_table = tabulate(subjectData, subject_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center"))
subjects_table = subjects_table.split("\n")


# Getting date and time info
dateNow = str(dt.date.today())
dateNow = dateNow.split("-")[::-1]
now = dt.datetime.now()
timeNow = now.strftime("%H:%M:%S")


# Writing & formatting all the lines to the text list
text = []

text.append("## Report")
text.append("")
text.append(f"Date:   {dateNow[0]}/{dateNow[1]}/{dateNow[2]}")
text.append(f"Time:   {timeNow}")
text.append("")
text.append("")
text.append("")
text.append("# Numerical Analysis")
text.append("")

for line in overall_table:

    text.append(line)

text.append("")

for line in subjects_table:

    text.append(line)

text.append("# Contents")
text.append("")
text.append("")

for subject in topicsOverall:

    text.append(f"~ {subject[0]} ~")
    text.append("=" * len(text[-1]))
    text.append("")

    for topic in subject[1]:

        text.append(f"* {topic}")


    if subject == topicsOverall[len(topicsOverall)-1]:

        text.append("")
        text.append(f"{separator * 85}")

    else:

        text.append("")
        text.append(f"{separator * 85}")
        text.append("")
        text.append("")

text.append((separator * 85))
text.append("")

text.append(f"ID {totalSize * 8}")

for line in text[4:]:

    if ":" in line:

        text[text.index(line)] = text[text.index(line)].replace(":", "/")


# Setting up the PDF
pdf = FPDF(orientation = "P", format = "A4")
pdf.add_page()
pdf.add_font("Menlo", "", fontFileDir + fontFile, uni=True)
pdf.set_font("Menlo", size = 10)


# Writing to the PDF
textToWrite = []

for line in text:

    if len(line) > 85:

        wrappedText = textwrap.wrap(line, width = 85)

        for elem in wrappedText:

            if elem == wrappedText[0]:

                textToWrite.append(elem)

            else:

                textToWrite.append("  " + elem)

    else:

        textToWrite.append(line)

for line in textToWrite:

    pdf.cell(0, 4, txt=line, ln=1)

pdf.output("Report.pdf")


# Deleting temporary .pkl files
os.remove(fontFileDir + "Menlo-Regular.cw127.pkl")
os.remove(fontFileDir + "Menlo-Regular.pkl")


# Informing the user of completion
print("\n--> Finished!\n")
