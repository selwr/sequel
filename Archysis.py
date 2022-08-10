# Archysis v3.2.5
# by Sam Wallis-Riches, 2022

import os
import time
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

startTime = time.time()

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
totalsData = [["Total", 0, 0, 0, 0]]

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
            totalsData[0][1] += 1
            subjectPapers += 1


            # Getting size data
            totalsData[0][4] += os.path.getsize(in_dir + "/" + subject + "/" + filename)
            subjectSize += os.path.getsize(in_dir + "/" + subject + "/" + filename)


            # Getting pages data
            with open(in_dir + "/" + subject + "/" + filename, "rb") as f:

                try:

                    pdf = PdfFileReader(f)

                except PyPDF2.errors.PdfReadError:

                    corruptFiles.append(subject + " : " + filename)
                

                try:

                    totalsData[0][3] += pdf.getNumPages()
                    subjectPages += pdf.getNumPages()

                except PyPDF2.errors.PdfReadError:

                    corruptFiles.append(subject + " : " + filename)
                
                except ValueError:

                    corruptFiles.append(subject + " : " + filename)


            # Getting topics data
            if "[" not in filename:

                totalsData[0][2] += 1
                subjectTopics += 1

            if ("[" in filename) and ("[1]" in filename):

                totalsData[0][2] += 1
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

    exit()


# Getting the maximum values and formatting them in their respective lists
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


# Getting lengths of subject names
subjectLengths = []

for subject in subjectData:

    subjectLengths.append(len(subject[0]))

longestSubjectNameLength = max(subjectLengths)


# Formatting and tabulating the subject data
subject_headers = ["Subject", "No. Documents", "No. Topics", "No. Pages", "   Size   "]
subjects_table = tabulate(subjectData, subject_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center"))
subjects_table = subjects_table.split("\n")

tIndex = subjects_table[0].index("╤")

firstLine = list(subjects_table[0])
firstLine[tIndex] = "╒"

for char in firstLine[:tIndex]:

    firstLine[firstLine.index(char)] = " "

subjects_table[0] = "".join(firstLine)

secondLine = list(subjects_table[1])
secondLine[0] = " "

subjects_table[1] = "".join(secondLine)
subjects_table[1] = subjects_table[1].replace("Subject", "       ")

thirdLine = list(subjects_table[2])
thirdLine[0] = "╒"

subjects_table[2] = "".join(thirdLine)

for line in subjects_table:

    lineLength = len(line)
    extraBit = (88 - lineLength) / 2

    if extraBit % 2 == 0:

        subjects_table[subjects_table.index(line)] = (" " * int(extraBit)) + subjects_table[subjects_table.index(line)]

    else:

        subjects_table[subjects_table.index(line)] = (" " * int(np.floor(extraBit))) + subjects_table[subjects_table.index(line)]


# Formatting and tabulating the totals data
for x in range(1, len(totalsData[0]) - 1):

    totalsData[0][x] = str(totalsData[0][x])

totalsData[0][4] = humanize.naturalsize(totalsData[0][4], binary=False, format="%.2f")

totals_headers = [" " * (longestSubjectNameLength - 2), "No. Documents", "No. Topics", "No. Pages", "   Size   "]
totals_table = tabulate(totalsData, totals_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center"))
totals_table = totals_table.split("\n")

totals_table = totals_table[2:]

totals_table[0] = totals_table[0].replace("╪", "╤")
totals_table[0] = totals_table[0].replace("╞", "╒")
totals_table[0] = totals_table[0].replace("╡", "╕")

for line in totals_table:

    lineLength = len(line)
    extraBit = (88 - lineLength) / 2

    if extraBit % 2 == 0:

        totals_table[totals_table.index(line)] = (" " * int(extraBit)) + totals_table[totals_table.index(line)]

    else:
        
        totals_table[totals_table.index(line)] = (" " * int(np.floor(extraBit))) + totals_table[totals_table.index(line)]


# Getting date and time info
dateNow = str(dt.date.today())
dateNow = dateNow.split("-")[::-1]
now = dt.datetime.now()
timeNow = now.strftime("%H:%M:%S")


# Writing & formatting all the lines to the text list
text = []

text.append(separator * 88)
text.append("")
text.append(" " * 37 + "Almanac Report")
text.append("")
text.append(" " * 33 + f"{dateNow[0]}.{dateNow[1]}.{dateNow[2][2:]}  ~  {timeNow}")
text.append("")
text.append(separator * 88)
text.append("")
text.append(" " * 38 + "- Metrics -")
text.append("")

for line in subjects_table:

    text.append(line)

text.append("")

for line in totals_table:

    text.append(line)

text.append(" " * 37 + "- Contents -")
text.append("")
text.append("")

for subject in topicsOverall:
    
    subjectLength = len("  " + subject[0] + "  ")
    extraBit = (88 - subjectLength) / 2

    if extraBit % 2 == 0:

        text.append(" " * int(extraBit) + f"  {subject[0]}  ")
        text.append(" " * int(extraBit) + "=" * len(f"  {subject[0]}  "))

    else:
        
        text.append(" " * int(np.floor(extraBit)) + f"  {subject[0]}  ")
        text.append(" " * int(np.floor(extraBit)) + "=" * len(f"  {subject[0]}  "))

    text.append("")

    for topic in subject[1]:

        text.append(f"* {topic}")

    if subject == topicsOverall[len(topicsOverall)-1]:

        text.append("")
        text.append(f"{separator * 88}")

    else:

        text.append("")
        text.append(f"{separator * 88}")
        text.append("")

text.append((separator * 88))

for line in text[:-2]:

    if ":" in line and "~" not in line:

        text[text.index(line)] = text[text.index(line)].replace(":", "/")


# Setting up the PDF
pdf = FPDF(orientation = "P", format = "A4")
pdf.add_page()
pdf.add_font("Menlo", "", fontFileDir + fontFile, uni=True)
pdf.set_font("Menlo", size = 10)
pdf.set_auto_page_break(auto = True, margin = 8.0)


# Writing to the PDF
textToWrite = []

for line in text:

    if len(line) > 88:

        wrappedText = textwrap.wrap(line, width = 88)

        for elem in wrappedText:

            if elem == wrappedText[0]:

                textToWrite.append(elem)

            else:

                textToWrite.append("  " + elem)

    else:

        textToWrite.append(line)

for line in textToWrite:

    pdf.cell(0, 4, txt=line, ln=1)

pdf.output("Almanac Report.pdf")


# Deleting temporary .pkl files
os.remove(fontFileDir + "Menlo-Regular.cw127.pkl")
os.remove(fontFileDir + "Menlo-Regular.pkl")


# End of program message
endTime = time.time()
runningTime = round(endTime - startTime, 2)

print(f"\n--> Finished in {runningTime}s!\n")
