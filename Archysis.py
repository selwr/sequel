# Archysis v3.4
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

separator = "─"

startTime = time.time()

print("\nStarting...")


# Getting current working directory and its contents
in_dir = os.path.dirname(os.path.realpath(__file__))

directory_contents = os.listdir(in_dir)


# Getting directory of font file
fontFile = 'Menlo-Regular.ttf'
fontFileDir = None

print("--> Searching for font file...")

for root, dirs, files in os.walk(r'/Users'):

    for name in files:

        if name == fontFile and "Mobile Documents" not in root and "Library" not in root:

            fontFileDir = os.path.abspath(os.path.join(root, name))[:-len(fontFile)]

            break

    if fontFileDir != None:

        break

if fontFileDir == None:

    print("--> No font file found!\n")
    exit()

else:

    print("--> Font file found!\n")


# Getting each of the theme names
themes = []

for folder in directory_contents:

    if (os.path.isdir(folder)) and ("." not in folder):

        subjects = []

        for subject in os.listdir(in_dir + "/" + folder):

            if (os.path.isdir(in_dir + "/" + folder + "/" + subject)) and ("." not in subject):

                subjects.append(subject)

        if subjects != []:

            themes.append([folder, subjects])

        else:

            themes.append(folder)

def theme_name_0(element):

    return element[0]

themes = sorted(themes, key=theme_name_0)
num_themes = len(themes)

for theme in themes:

    if isinstance(theme, list):

        themes[themes.index(theme)][1] = sorted(theme[1])


# Checking status of all files
corruptFiles = []

print("--> Checking files...")

for theme in themes:

    if not isinstance(theme, list):

        for filename in os.listdir(in_dir + "/" + theme):

            if ".pdf" in filename:

                try:

                    pdf = PdfFileReader(in_dir + "/" + theme + "/" + filename)

                except PyPDF2.errors.PdfReadError:

                    corruptFiles.append(subject + ": " + filename)
                    continue

                try:

                    temp = pdf.getNumPages()

                except PyPDF2.errors.PdfReadError:

                    corruptFiles.append(subject + ": " + filename)

                except ValueError:

                    corruptFiles.append(subject + ": " + filename)

    else:

        for subject in theme[1]:

            for filename in os.listdir(in_dir + "/" + theme[0] + "/" + subject):

                if ".pdf" in filename:

                    try:
                        
                        pdf = PdfFileReader(in_dir + "/" + theme[0] + "/" + subject + "/" + filename)

                    except PyPDF2.errors.PdfReadError:

                        corruptFiles.append(subject + ": " + filename)
                        continue
                    

                    try:

                        temp = pdf.getNumPages()

                    except PyPDF2.errors.PdfReadError:

                        corruptFiles.append(subject + ": " + filename)
                    
                    except ValueError:

                        corruptFiles.append(subject + ": " + filename)


# Writing list of corrupt files, if necessary
if corruptFiles != []:

    with open("Corruptions.txt", "w") as f:

        f.write("## Corrupt Files\n\n")

        for filename in corruptFiles:

            f.write("* " + filename + "\n")

    print("\n--> Fix files listed in 'Corruptions.txt'\n")

    exit()

else:

    print("--> File check complete!\n")


# Setting up the lists for the data
totalsData = [[f"Total", 0, 0, 0, 0, 0]]

overallData = []

themesData = []

topicsOverall = []

subjectPaperVals = []
subjectTopicVals = []
subjectPageVals = []
subjectSizeVals = []

print("\nReading files...")


# Getting all the data
for theme in themes:

    docs = 0
    topics = 0
    pages = 0
    size = 0
    subjects = 0

    running_subjects = ""


    # Getting data if theme has subjects
    if isinstance(theme, list):

        themeData = [theme[0], []]

        themeTopics = [theme[0], []]

        if themes.index(theme) == 0:

            print(f"--> Doing {theme[0]}...")

        else:

            print(f"\n--> Doing {theme[0]}...")

        for subject in theme[1]:

            topicsSubject = []

            subjectPapers = 0
            subjectTopics = 0
            subjectPages = 0
            subjectSize = 0

            subjects += 1
            totalsData[0][1] += 1

            running_subjects += subject + "\n"

            for filename in os.listdir(in_dir + "/" + theme[0] + "/" + subject):

                if ".pdf" in filename:
                    
                    # Getting papers data
                    totalsData[0][2] += 1
                    subjectPapers += 1
                    docs += 1


                    # Getting size data
                    totalsData[0][5] += os.path.getsize(in_dir + "/" + theme[0] + "/" + subject + "/" + filename)
                    subjectSize += os.path.getsize(in_dir + "/" + theme[0] + "/" + subject + "/" + filename)
                    size += os.path.getsize(in_dir + "/" + theme[0] + "/" + subject + "/" + filename)


                    # Getting pages data
                    with open(in_dir + "/" + theme[0] + "/" + subject + "/" + filename, "rb") as f:

                        pdf = PdfFileReader(f)

                        totalsData[0][4] += pdf.getNumPages()
                        subjectPages += pdf.getNumPages()
                        pages += pdf.getNumPages()


                    # Getting topics data
                    if "[" not in filename:

                        totalsData[0][3] += 1
                        subjectTopics += 1
                        topics += 1

                    if ("[" in filename) and ("[1]" in filename):

                        totalsData[0][3] += 1
                        subjectTopics += 1
                        topics += 1
                    

                    # Getting topics
                    topicsSubject.append(filename[:-4])
                

            # Appending all values to necessary lists
            subjectPaperVals.append(subjectPapers)
            subjectTopicVals.append(subjectTopics)
            subjectPageVals.append(subjectPages)
            subjectSizeVals.append(subjectSize)

            themeData[1].append([subject, str(subjectPapers), str(subjectTopics), str(subjectPages), humanize.naturalsize(subjectSize, binary=False, format="%.1f")])


            # Sorting out topics and flags
            topicsSubject = sorted(topicsSubject)

            for topic in topicsSubject:

                if "[" in topic:

                    topicsSubject[topicsSubject.index(topic)] = topicsSubject[topicsSubject.index(topic)][:topic.index("[")-1]

            topicsSubjectActual = []

            for topic in topicsSubject:

                if "(" in topic:

                    tempTopic = topic.split(" (")

                    if tempTopic[0] not in topicsSubjectActual:

                        topicsSubjectActual.append(tempTopic[0])
                else:
                    
                    topicsSubjectActual.append(topic)

            topicsSubjectActualSet = set(topicsSubjectActual)
            topicsSubjectActualList = list(topicsSubjectActualSet)

            topicsSubjectActual = sorted(topicsSubjectActualList)

            topicsForSubject = []
            for elem in topicsSubjectActual:

                topicsForSubject.append(elem)

            for name in topicsSubject:

                flags = []

                if "(" in name:

                    bracketIndex = name.index("(")
                    flag = name[bracketIndex+1:-1]
                    topicProper = name[:bracketIndex-1]


                    # One flag
                    if "," not in flag and " and " not in flag:

                        flags.append(flag)
                    

                    # Two flags
                    if "," not in flag and " and " in flag:

                        tempFlags = flag.split(" and ")

                        for f in tempFlags:

                            flags.append(f)
                

                    # No comma with 'and', three or more flags
                    if ", " in flag and " and " in flag and ", and " not in flag:

                        tempFlags = flag.split(", ")

                        tempFlags2 = []

                        for elem in tempFlags:

                            if " and " in elem:

                                splitAnd = elem.split(" and ")

                                for e in splitAnd:

                                    tempFlags2.append(e)
                            
                            else:

                                tempFlags2.append(elem)

                        for f in tempFlags2:

                            flags.append(f)


                    # Comma with 'and', three or more flags
                    if "," in flag and ", and " in flag:

                        tempFlags = flag.split(", ")

                        tempFlags2 = []

                        for elem in tempFlags:

                            if "and " in elem:

                                splitAnd = elem.split("and ")

                                for e in splitAnd:

                                    if e != "":

                                        tempFlags2.append(e)

                            else:
                                tempFlags2.append(elem)

                        for f in tempFlags2:

                            flags.append(f)

                    topicIndex = topicsForSubject.index(topicProper)

                    if topicsSubjectActual[topicIndex] == topicProper:

                        topicsSubjectActual[topicIndex] = [topicProper, flags]

                    elif topicsSubjectActual[topicIndex] != topicProper:

                        for f in flags:

                            topicsSubjectActual[topicIndex][1].append(f)

                if flags != [] and topicProper in topicsSubjectActual:

                    topicsSubjectActual.remove(topicProper)

            for flaggedTopic in topicsSubjectActual:
                
                if isinstance(flaggedTopic, list):
                    
                    for flag in flaggedTopic[1]:

                        countFlag = flaggedTopic[1].count(flag)

                        if countFlag == len(flaggedTopic[1]) and countFlag > 1:

                            topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)] = f"{flaggedTopic[0]} ({flag}) [{countFlag}]"

                            break

                        elif countFlag != len(flaggedTopic[1]) and countFlag > 1:

                            topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)][1][flaggedTopic[1].index(flag)] = f"{flag} [{countFlag}]"

                            while flag in topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)][1]:

                                topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)][1].remove(flag)

                        elif countFlag == len(flaggedTopic[1]) and countFlag == 1:

                            topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)] = f"{flaggedTopic[0]} ({flag})"
                            
                            break
                
            topicsSubjectDupes = []
            for topic in topicsSubject:

                if "(" in topic:

                    tempTopic = topic.split(" (")
                    topicsSubjectDupes.append(tempTopic[0])

                else:

                    topicsSubjectDupes.append(topic)

            for topic in topicsForSubject:

                count = topicsSubjectDupes.count(topic)
                index = topicsForSubject.index(topic)

                if count > 1:

                    if isinstance(topicsSubjectActual[index], list):

                        topicsSubjectActual[index][0] = topicsSubjectActual[index][0] + f" [{count}]"

                    elif not isinstance(topicsSubjectActual[index], list) and "[" not in topicsSubjectActual[index]:

                        topicsSubjectActual[index] = topicsSubjectActual[index] + f" [{count}]"

            themeTopics[1].append([subject, topicsSubjectActual])

            print(f"    ✓ {subject} done!")
        

        # Appending all necessary values
        themesData.append([theme[0], "("+ str(subjects) + ")\n" + running_subjects, str(docs), str(topics), str(pages), humanize.naturalsize(size, binary=False, format="%.1f")])

        overallData.append(themeData)
        topicsOverall.append(themeTopics)


    # Getting data if theme has subjects
    else:

        themeData = [theme]

        themeTopics = [theme]

        topicsSubject = []

        subjectPapers = 0
        subjectTopics = 0
        subjectPages = 0
        subjectSize = 0

        running_subjects += theme + "\n"

        totalsData[0][1] += 1

        if themes.index(theme) == 0:

            print(f"--> Doing {theme}...")

        else:

            print(f"\n--> Doing {theme}...")

        for filename in os.listdir(in_dir + "/" + theme):

            if ".pdf" in filename:

                # Getting papers data
                totalsData[0][2] += 1
                subjectPapers += 1
                docs += 1


                # Getting size data
                totalsData[0][5] += os.path.getsize(in_dir + "/" + theme + "/" + filename)
                subjectSize += os.path.getsize(in_dir + "/" + theme + "/" + filename)
                size += os.path.getsize(in_dir + "/" + theme + "/" + filename)


                # Getting pages data
                with open(in_dir + "/" + theme + "/" + filename, "rb") as f:

                    pdf = PdfFileReader(f)

                    totalsData[0][4] += pdf.getNumPages()
                    subjectPages += pdf.getNumPages()
                    pages += pdf.getNumPages()


                # Getting topics data
                if "[" not in filename:

                    totalsData[0][3] += 1
                    subjectTopics += 1
                    topics += 1

                if ("[" in filename) and ("[1]" in filename):

                    totalsData[0][3] += 1
                    subjectTopics += 1
                    topics += 1


                # Getting topics
                topicsSubject.append(filename[:-4])


        # Appending all values to necessary lists
        subjectPaperVals.append(subjectPapers)
        subjectTopicVals.append(subjectTopics)
        subjectPageVals.append(subjectPages)
        subjectSizeVals.append(subjectSize)

        themeData.append(str(subjectPapers))
        themeData.append(str(subjectTopics))
        themeData.append(str(subjectPages))
        themeData.append(humanize.naturalsize(subjectSize, binary=False, format="%.1f"))


        # Sorting out topics and flags
        topicsSubject = sorted(topicsSubject)

        for topic in topicsSubject:

            if "[" in topic:

                topicsSubject[topicsSubject.index(topic)] = topicsSubject[topicsSubject.index(topic)][:topic.index("[")-1]

        topicsSubjectActual = []

        for topic in topicsSubject:

            if "(" in topic:

                tempTopic = topic.split(" (")

                if tempTopic[0] not in topicsSubjectActual:

                    topicsSubjectActual.append(tempTopic[0])
            else:

                topicsSubjectActual.append(topic)

        topicsSubjectActualSet = set(topicsSubjectActual)
        topicsSubjectActualList = list(topicsSubjectActualSet)

        topicsSubjectActual = sorted(topicsSubjectActualList)

        topicsForSubject = []
        for elem in topicsSubjectActual:

            topicsForSubject.append(elem)

        for name in topicsSubject:

            flags = []

            if "(" in name:

                bracketIndex = name.index("(")
                flag = name[bracketIndex+1:-1]
                topicProper = name[:bracketIndex-1]


                # One flag
                if "," not in flag and " and " not in flag:

                    flags.append(flag)


                # Two flags
                if "," not in flag and " and " in flag:

                    tempFlags = flag.split(" and ")

                    for f in tempFlags:

                        flags.append(f)


                # No comma with 'and', three or more flags
                if ", " in flag and " and " in flag and ", and " not in flag:

                    tempFlags = flag.split(", ")

                    tempFlags2 = []

                    for elem in tempFlags:

                        if " and " in elem:

                            splitAnd = elem.split(" and ")

                            for e in splitAnd:

                                tempFlags2.append(e)

                        else:

                            tempFlags2.append(elem)

                    for f in tempFlags2:

                        flags.append(f)


                # Comma with 'and', three or more flags
                if "," in flag and ", and " in flag:

                    tempFlags = flag.split(", ")

                    tempFlags2 = []

                    for elem in tempFlags:

                        if "and " in elem:

                            splitAnd = elem.split("and ")

                            for e in splitAnd:

                                if e != "":

                                    tempFlags2.append(e)

                        else:
                            tempFlags2.append(elem)

                    for f in tempFlags2:

                        flags.append(f)

                topicIndex = topicsForSubject.index(topicProper)

                if topicsSubjectActual[topicIndex] == topicProper:

                    topicsSubjectActual[topicIndex] = [topicProper, flags]

                elif topicsSubjectActual[topicIndex] != topicProper:

                    for f in flags:

                        topicsSubjectActual[topicIndex][1].append(f)

            if flags != [] and topicProper in topicsSubjectActual:

                topicsSubjectActual.remove(topicProper)

        for flaggedTopic in topicsSubjectActual:

            if isinstance(flaggedTopic, list):

                for flag in flaggedTopic[1]:

                    countFlag = flaggedTopic[1].count(flag)

                    if countFlag == len(flaggedTopic[1]) and countFlag > 1:

                        topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)] = f"{flaggedTopic[0]} ({flag}) [{countFlag}]"

                        break

                    elif countFlag != len(flaggedTopic[1]) and countFlag > 1:

                        topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)][1][flaggedTopic[1].index(flag)] = f"{flag} [{countFlag}]"

                        while flag in topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)][1]:

                            topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)][1].remove(flag)

                    elif countFlag == len(flaggedTopic[1]) and countFlag == 1:

                        topicsSubjectActual[topicsSubjectActual.index(flaggedTopic)] = f"{flaggedTopic[0]} ({flag})"

                        break

        topicsSubjectDupes = []
        for topic in topicsSubject:

            if "(" in topic:

                tempTopic = topic.split(" (")
                topicsSubjectDupes.append(tempTopic[0])

            else:

                topicsSubjectDupes.append(topic)

        for topic in topicsForSubject:

            count = topicsSubjectDupes.count(topic)
            index = topicsForSubject.index(topic)

            if count > 1:

                if isinstance(topicsSubjectActual[index], list):

                    topicsSubjectActual[index][0] = topicsSubjectActual[index][0] + f" [{count}]"

                elif not isinstance(topicsSubjectActual[index], list) and "[" not in topicsSubjectActual[index]:

                    topicsSubjectActual[index] = topicsSubjectActual[index] + f" [{count}]"

        themeTopics.append(topicsSubjectActual)

        themesData.append([theme, "(1)\n" + running_subjects, str(docs), str(topics), str(pages), humanize.naturalsize(size, binary=False, format="%.1f")])

        overallData.append(themeData)
        topicsOverall.append(themeTopics)

        print(f"    ✓ {theme} done!")

print("\n--> Files read!\n\n")

print("Finishing up...")


# Getting lengths of theme names
themeLengths = []

for theme in themesData:

    themeLengths.append(len(theme[0]))

longestThemeNameLength = max(themeLengths)


# Formatting and tabulating the theme data
print("--> Formatting text...")

theme_headers = ["Theme", " Subjects ", " Documents ", " Topics ", " Pages ", " Size "]
theme_table = tabulate(themesData, theme_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center", "center"))
theme_table = theme_table.split("\n")

for line in theme_table:

    lineLength = len(line)
    extraBit = (88 - lineLength) / 2

    if extraBit % 2 == 0:

        theme_table[theme_table.index(line)] = (" " * int(extraBit)) + theme_table[theme_table.index(line)]

    else:

        theme_table[theme_table.index(line)] = (" " * int(np.floor(extraBit))) + theme_table[theme_table.index(line)]

barIndicies = []
for index in range(len(theme_table[1])):

    if theme_table[1][index] == "│":

        barIndicies.append(index)


# Formatting and tabulating the totals data
for x in range(1, len(totalsData[0]) - 1):

    totalsData[0][x] = str(totalsData[0][x])

totalsData[0][5] = humanize.naturalsize(totalsData[0][5], binary=False, format="%.2f")

totals_headers = [" " * (longestThemeNameLength - 2), " Subjects " + ((barIndicies[2] - barIndicies[1]) - 15) * " ", " Documents ", " Topics ", " Pages ", " Size "]
totals_table = tabulate(totalsData, totals_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center", "center"))
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


# Getting the maximum values and formatting them in their respective lists
maxPapers = max(subjectPaperVals)
maxTopics = max(subjectTopicVals)
maxPages = max(subjectPageVals)
maxSize = max(subjectSizeVals)

for theme in overallData:

    if isinstance(theme[1], list):

        for subject in theme[1]:

            if int(subject[1]) == maxPapers:

                overallData[overallData.index(theme)][1][theme[1].index(subject)][1] = "[ " + subject[1] + " ]"


            if int(subject[2]) == maxTopics:

                overallData[overallData.index(theme)][1][theme[1].index(subject)][2] = "[ " + subject[2] + " ]"


            if int(subject[3]) == maxPages:

                overallData[overallData.index(theme)][1][theme[1].index(subject)][3] = "[ " + subject[3] + " ]"


            if subject[4] == humanize.naturalsize(maxSize, binary=False, format="%.1f"):

                overallData[overallData.index(theme)][1][theme[1].index(subject)][4] = "[ " + subject[4] + " ]"
    
    else:

        if int(subject[1]) == maxPapers:

            overallData[overallData.index(theme)][1] = "[ " + subject[1] + " ]"


        if int(subject[2]) == maxTopics:

            overallData[overallData.index(theme)][2] = "[ " + subject[2] + " ]"


        if int(subject[3]) == maxPages:

            overallData[overallData.index(theme)][3] = "[ " + subject[3] + " ]"


        if subject[4] == humanize.naturalsize(maxSize, binary=False, format="%.1f"):

            overallData[overallData.index(theme)][4] = "[ " + subject[4] + " ]"


# Getting rows of subject table
subjectRows = []
for theme in overallData:

    if not isinstance(theme[1], list):

        subjectRows.append(theme)

    else:

        for subject in theme[1]:

            subjectRows.append(subject)

def subject_name(element):

    return element[0]

subjectRows = sorted(subjectRows, key=subject_name)


# Getting lengths of subject names
subjectLengths = []

for subject in subjectRows:

    subjectLengths.append(len(subject[0]))

longestSubjectNameLength = max(subjectLengths)


# Formatting and tabulating the subject data
subject_headers = [f"Subject", " Documents ", "  Topics  ", "  Pages  ", "   Size   "]
subjects_table = tabulate(subjectRows, subject_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center"))
subjects_table = subjects_table.split("\n")

for line in subjects_table:

    lineLength = len(line)
    extraBit = (88 - lineLength) / 2

    if extraBit % 2 == 0:

        subjects_table[subjects_table.index(line)] = (" " * int(extraBit)) + subjects_table[subjects_table.index(line)]

    else:

        subjects_table[subjects_table.index(line)] = (" " * int(np.floor(extraBit))) + subjects_table[subjects_table.index(line)]

print("--> Text formatted!\n")


# Getting date and time info
dateNow = str(dt.date.today())
dateNow = dateNow.split("-")[::-1]
now = dt.datetime.now()
timeNow = now.strftime("%H:%M:%S")


# Writing & formatting all the lines to the text list
print("--> Writing to PDF...")

text = []

text.append(separator * 88)
text.append("")
text.append(" " * 37 + "Almanac Report")
text.append("")
text.append(" " * 33 + f"{dateNow[0]}.{dateNow[1]}.{dateNow[2][2:]}  ❦  {timeNow}")
text.append("")
text.append(separator * 88)
text.append("")
text.append(" " * 18 + separator * 20 + "  Themes  " + separator * 20)
text.append("")

for line in theme_table:

    text.append(line)

text.append("")

for line in totals_table:

    text.append(line)

text.append(" " * 17 + separator * 20 + "  Subjects  " + separator * 20)
text.append("")

for line in subjects_table:

    text.append(line)

text.append("")
text.append("")
text.append(" " * 18 + separator * 20 + "  Index  " + separator * 20)
text.append("")
text.append(separator * 88)
text.append("")
text.append("• Atomic & Molecular - ")
text.append("• Biochemistry - ")
text.append("• Black Holes - ")
text.append("• Computing - ")
text.append("• Cosmology - ")
text.append("• Cryptography - ")
text.append("• Dark Matter - ")
text.append("• Earth - ")
text.append("• Energy - ")
text.append("• Extrasolar - ")
text.append("• Fluids - ")
text.append("• Galaxies - ")
text.append("• Gravity - ")
text.append("• Heliophysics - ")
text.append("• Humans - ")
text.append("• Inorganics - ")
text.append("• Jupiter - ")
text.append("• Life - ")
text.append("• Lunar - ")
text.append("• Mars - ")
text.append("• Materials - ")
text.append("• Mathematics - ")
text.append("• Medicine - ")
text.append("• Mercury - ")
text.append("• Nature - ")
text.append("• Neptune - ")
text.append("• Optics - ")
text.append("• Organics - ")
text.append("• Organometallics - ")
text.append("• Particle Physics - ")
text.append("• Photonics - ")
text.append("• Quantum Computing - ")
text.append("• Quantum Physics - ")
text.append("• Saturn - ")
text.append("• Solar System - ")
text.append("• Space - ")
text.append("• Spacecraft - ")
text.append("• Stars - ")
text.append("• Uranus - ")
text.append("• Venus - ")
text.append("")
text.append((separator * 88))

for x in range(4):
    
    text.append("")

text.append(" " * 17 + separator * 20 + "  Contents  " + separator * 20)
text.append("")
text.append(separator * 88)

for theme in topicsOverall:

    if not isinstance(theme[1][0][1], list):

        text.append("")

        subjectLength = len("- " + theme[0] + " -")
        extraBit = (88 - subjectLength) / 2

        if extraBit % 2 == 0:

            text.append(" " * int(extraBit) + f"- {theme[0]} -")

        else:
            
            text.append(" " * int(np.floor(extraBit)) + f"- {theme[0]} -")

        text.append("")
        text.append((separator * 88))
        text.append("")

        for topic in theme[1]:

            if isinstance(topic, list):

                text.append(f"• {topic[0]}")

                for flag in topic[1]:

                    text.append(f"    ‣ {flag}")

            else:
                text.append(f"• {topic}")
        
        text.append("")
        text.append(f"{separator * 88}")
    
    else:

        text.append("")

        themeLength = len("- " + theme[0] + " -")
        extraBit = (88 - themeLength) / 2

        if extraBit % 2 == 0:

            text.append(" " * int(extraBit) + f"- {theme[0]} -")

        else:

            text.append(" " * int(np.floor(extraBit)) + f"- {theme[0]} -")

        text.append("")
        text.append((separator * 88))

        subjects = []
        for item in theme:
            if isinstance(item, list):

                for subject in item:

                    subjects.append(subject)

        for subject in subjects:

            text.append("")

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

                if isinstance(topic, list):

                    text.append(f"• {topic[0]}")

                    for flag in topic[1]:

                        text.append(f"    ‣ {flag}")

                else:
                    text.append(f"• {topic}")

            text.append("")
            text.append(f"{separator * 88}")

text.append(f"{separator * 88}")      


# Replacing the colons
for line in text:

    if ":" in line and "❦" not in line:

        text[text.index(line)] = text[text.index(line)].replace(":", "/")


# Wrapping text
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


# Setting up the PDF
pdf = FPDF(orientation = "P", format = "A4")
pdf.add_page()
pdf.add_font("Menlo", "", fontFileDir + fontFile, uni=True)
pdf.set_font("Menlo", size = 10)
pdf.set_auto_page_break(auto = True, margin = 8.0)


# Writing to PDF
for index in range(len(textToWrite)):

    if index == 137 and "┼" in textToWrite[index]:

        oneReplaced = textToWrite[index].replace("┼", "┴")
        twoReplaced = oneReplaced.replace("├", "└")
        threeReplaced = twoReplaced.replace("┤", "┘")

        pdf.cell(0, 4, txt=threeReplaced, ln=1)

    elif index == 138 and "┼" in textToWrite[137]:

        oneReplaced = textToWrite[137].replace("┼", "┬")
        twoReplaced = oneReplaced.replace("├", "┌")
        threeReplaced = twoReplaced.replace("┤", "┐")

        pdf.cell(0, 4, txt=threeReplaced, ln=1)
        pdf.cell(0, 4, txt=textToWrite[index], ln=1)

    elif index == 136 and "┼" in textToWrite[index]:

        oneReplaced = textToWrite[index].replace("┼", "┴")
        twoReplaced = oneReplaced.replace("├", "└")
        threeReplaced = twoReplaced.replace("┤", "┘")

        pdf.cell(0, 4, txt=threeReplaced, ln=1)
        pdf.cell(0, 4, txt="", ln=1)

    elif index == 137 and "┼" in textToWrite[136]:

        oneReplaced = textToWrite[136].replace("┼", "┬")
        twoReplaced = oneReplaced.replace("├", "┌")
        threeReplaced = twoReplaced.replace("┤", "┐")

        pdf.cell(0, 4, txt=threeReplaced, ln=1)
        pdf.cell(0, 4, txt=textToWrite[index], ln=1)
        
    else:

        pdf.cell(0, 4, txt=textToWrite[index], ln=1)

pdf.output("Almanac Report.pdf")

print("--> PDF written!\n")


# Deleting temporary .pkl files
os.remove(fontFileDir + "Menlo-Regular.cw127.pkl")
os.remove(fontFileDir + "Menlo-Regular.pkl")


# End of program message
endTime = time.time()
runningTime = round(endTime - startTime, 2)

print(f"--> Finished in {runningTime}s!\n\n")
