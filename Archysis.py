# Archysis
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




'''
INITIAL SETUP
'''


# Setting initial variables
version = "v3.7.3"

ext = ".pdf"

singleSep = "─"
doubleSep = "═"
runningSep = "~"

pageWidth = 88
pageLength = 69

doThemesTable = True
doGlossary = True

startTime = time.time()



# Printing beginning verbose lines
startLine = f"Archysis {version}"

numSep = int(np.ceil((45 - len(f" {startLine} ")) / 2))
print(f"\n\n{runningSep * (numSep + 1)} {startLine} {runningSep * (numSep + 1)}")



# Getting current working directory and its contents
in_dir = os.path.dirname(os.path.realpath(__file__))

archive_name = in_dir.split(os.sep)[-1]

directory_contents = os.listdir(in_dir)

print(f"\n--> Report for '{archive_name}' will be generated!\n")



# Getting directory of font file
fontFile = "archysis_font.ttf"
fontFileDir = None

print("--> Searching for font file...")

for root, dirs, files in os.walk(r"/Users"):

    for name in files:

        if name == fontFile:

            fontFileDir = os.path.abspath(os.path.join(root, name))[:-len(fontFile)]

            break


    if fontFileDir != None:

        break


if fontFileDir == None:

    print("--> No font file found!\n")
    exit()

else:

    print("--> Font file found!\n")



# Getting directory of glossary file
glossDir = None
glossName = "archive_glossary.txt"

print("--> Searching for glossary file...")

for root, dirs, files in os.walk(r"/Users"):

    for name in files:

        if name == glossName:

            glossDir = os.path.abspath(os.path.join(root, name))[:-len(glossName)]

            break


    if glossDir != None:

        break


if glossDir == None:

    print("--> No glossary file found!\n")
    doGlossary = False

else:

    print("--> Glossary file found!\n")



# Getting each of the theme names
themes = []

subjectLikeThemeCount = 0

for folder in directory_contents:

    if (os.path.isdir(folder)) and ("." not in folder):

        subjects = []

        for subject in os.listdir(os.path.join(in_dir, folder)):

            if (os.path.isdir(os.path.join(in_dir, folder, subject))) and ("." not in subject):

                subjects.append(subject)


        if subjects != []:

            themes.append([folder, subjects])

        else:

            subjectLikeThemeCount += 1

            themes.append(folder)


if themes == []:

    print("\n--> No folders found to analyse!\n")

    exit()


def get_theme_name(element):

    if isinstance(element, list):

        return element[0]
    
    else:

        return element


themes = sorted(themes, key=get_theme_name)
num_themes = len(themes)

for theme in themes:

    if isinstance(theme, list):

        themes[themes.index(theme)][1] = sorted(theme[1])



# Checking status of all files
corruptFiles = []

print("--> Checking files...")
pdfCount = 0

for theme in themes:

    if not isinstance(theme, list):

        for filename in os.listdir(os.path.join(in_dir, theme)):

            if ext in filename:

                pdfCount += 1

                try:

                    pdf = PdfFileReader(os.path.join(in_dir, theme, filename))

                except PyPDF2.errors.PdfReadError:

                    corruptFiles.append(f"{subject}: {filename}")

                    continue


                try:

                    temp = pdf.getNumPages()

                except PyPDF2.errors.PdfReadError:

                    corruptFiles.append(f"{subject}: {filename}")

                except ValueError:

                    corruptFiles.append(f"{subject}: {filename}")


    else:

        for subject in theme[1]:

            for filename in os.listdir(os.path.join(in_dir, theme[0], subject)):

                if ext in filename:

                    pdfCount += 1

                    try:
                        
                        pdf = PdfFileReader(os.path.join(in_dir, theme[0], subject, filename))

                    except PyPDF2.errors.PdfReadError:

                        corruptFiles.append(f"{subject}: {filename}")

                        continue
                    

                    try:

                        temp = pdf.getNumPages()

                    except PyPDF2.errors.PdfReadError:

                        corruptFiles.append(f"{subject}: {filename}")
                    
                    except ValueError:

                        corruptFiles.append(f"{subject}: {filename}")


if pdfCount == 0:

    print("--> No PDF documents found\n")

    exit()


if subjectLikeThemeCount == len(themes):

    doThemesTable = False



# Writing list of corrupt files, if necessary
if corruptFiles != []:

    with open("Corruptions.txt", "w") as f:

        f.write("## Corrupt Files\n\n")

        for filename in corruptFiles:

            f.write(f"* {filename}\n")


    print("--> File check complete!\n")
    print("\n--> Fix files listed in 'Corruptions.txt'\n")

    exit()

else:

    print("--> File check complete!")
    print("--> All files OK!\n")




'''
DATA EXTRACTION
'''


# Setting up the lists for the data
totalsData = [[f"Total", 0, 0, 0, 0, 0]]

overallData = []

themesData = []

topicsOverall = []

subjectPaperVals = []
subjectTopicVals = []
subjectPageVals = []
subjectSizeVals = []



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



            # Going through each of the files
            for filename in os.listdir(os.path.join(in_dir, theme[0], subject)):

                if ext in filename:
                    


                    # Getting papers data
                    totalsData[0][2] += 1
                    subjectPapers += 1
                    docs += 1



                    # Getting size data
                    totalsData[0][5] += os.path.getsize(os.path.join(in_dir, theme[0], subject, filename))
                    subjectSize += os.path.getsize(os.path.join(in_dir, theme[0], subject, filename))
                    size += os.path.getsize(os.path.join(in_dir, theme[0], subject, filename))



                    # Getting pages data
                    with open(os.path.join(in_dir, theme[0], subject, filename), "rb") as f:

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


            # Removing square brackets
            for topic in topicsSubject:

                if "[" in topic:

                    topicsSubject[topicsSubject.index(topic)] = topicsSubject[topicsSubject.index(topic)][:topic.index("[")-1]

            topicsSubjectActual = []


            # Removing flags
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


            # Preserving the list with flags
            topicsForSubject = []

            for elem in topicsSubjectActual:

                topicsForSubject.append(elem)


            # Getting all flags per topic
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


                    # Adding flags to the data structures
                    topicIndex = topicsForSubject.index(topicProper)

                    if topicsSubjectActual[topicIndex] == topicProper:

                        topicsSubjectActual[topicIndex] = [topicProper, flags]

                    elif topicsSubjectActual[topicIndex] != topicProper:

                        for f in flags:

                            topicsSubjectActual[topicIndex][1].append(f)


                if flags != [] and topicProper in topicsSubjectActual:

                    topicsSubjectActual.remove(topicProper)


            # Getting counts of each flag
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
                
            
            # Getting counts for each topic
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



    # Getting data if theme has no subjects
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



        # Going through all files
        for filename in os.listdir(os.path.join(in_dir, theme)):

            if ext in filename:



                # Getting papers data
                totalsData[0][2] += 1
                subjectPapers += 1
                docs += 1



                # Getting size data
                totalsData[0][5] += os.path.getsize(os.path.join(in_dir, theme, filename))
                subjectSize += os.path.getsize(os.path.join(in_dir, theme, filename))
                size += os.path.getsize(os.path.join(in_dir, theme, filename))



                # Getting pages data
                with open(os.path.join(in_dir, theme, filename), "rb") as f:

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


        # Removing square brackets
        for topic in topicsSubject:

            if "[" in topic:

                topicsSubject[topicsSubject.index(topic)] = topicsSubject[topicsSubject.index(topic)][:topic.index("[")-1]


        # Removing flags
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


        # Preserving list with flags
        topicsForSubject = []

        for elem in topicsSubjectActual:

            topicsForSubject.append(elem)


        # Getting all flags per topic
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


                # Adding flags to data structures
                topicIndex = topicsForSubject.index(topicProper)

                if topicsSubjectActual[topicIndex] == topicProper:

                    topicsSubjectActual[topicIndex] = [topicProper, flags]

                elif topicsSubjectActual[topicIndex] != topicProper:

                    for f in flags:

                        topicsSubjectActual[topicIndex][1].append(f)


            if flags != [] and topicProper in topicsSubjectActual:

                topicsSubjectActual.remove(topicProper)


        # Getting counts for each flag
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


        # Getting counts for each topic
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

        themesData.append([theme, "N/A", str(docs), str(topics), str(pages), humanize.naturalsize(size, binary=False, format="%.1f")])

        overallData.append(themeData)
        topicsOverall.append(themeTopics)

print("\n--> Files read!\n")




'''
DATA FORMATTING FOR REPORT
'''


print("--> Preparing lines for writing...")


# Getting lengths of theme names
themeLengths = []

for theme in themesData:

    themeLengths.append(len(theme[0]))

longestThemeNameLength = max(themeLengths)



# Formatting and tabulating the theme data, if necessary

if doThemesTable:

    theme_headers = ["Theme", " Subjects ", " Documents ", " Topics ", " Pages ", " Size "]
    theme_table = tabulate(themesData, theme_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center", "center"))
    theme_table = theme_table.split("\n")



    # Centring the themes table
    for line in theme_table:

        lineLength = len(line)
        extraBit = (pageWidth - lineLength) / 2

        theme_table[theme_table.index(line)] = (" " * int(np.floor(extraBit))) + theme_table[theme_table.index(line)]



    # Getting positions of bars for totals table
    barIndicies = []

    for index in range(len(theme_table[1])):

        if theme_table[1][index] == "│":

            barIndicies.append(index)



# Getting the highest values and formatting them in their respective lists
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

        if int(theme[1]) == maxPapers:

            overallData[overallData.index(theme)][1] = "[ " + theme[1] + " ]"


        if int(theme[2]) == maxTopics:

            overallData[overallData.index(theme)][2] = "[ " + theme[2] + " ]"


        if int(theme[3]) == maxPages:

            overallData[overallData.index(theme)][3] = "[ " + theme[3] + " ]"


        if theme[4] == humanize.naturalsize(maxSize, binary=False, format="%.1f"):

            overallData[overallData.index(theme)][4] = "[ " + theme[4] + " ]"



# Getting rows of subject table & sorting them
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
subject_headers = ["Subject", " Documents ", "  Topics  ", "  Pages  ", "   Size   "]
subjects_table = tabulate(subjectRows, subject_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center"))
subjects_table = subjects_table.split("\n")



# Centring the subjects table
for line in subjects_table:

    lineLength = len(line)
    extraBit = (pageWidth - lineLength) / 2

    subjects_table[subjects_table.index(line)] = (" " * int(np.floor(extraBit))) + subjects_table[subjects_table.index(line)]



# Formatting and tabulating the totals data
if doThemesTable == True:

    for x in range(1, len(totalsData[0]) - 1):

        totalsData[0][x] = str(totalsData[0][x])

    totalsData[0][5] = humanize.naturalsize(totalsData[0][5], binary=False, format="%.2f")

    totals_headers = [" " * (longestThemeNameLength - 2), " Subjects " + ((barIndicies[2] - barIndicies[1]) - 15) * " ", " Documents ", " Topics ", " Pages ", " Size "]
    totals_table = tabulate(totalsData, totals_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center", "center"))


elif doThemesTable == False:

    totalsData = [["Total", totalsData[0][2], totalsData[0][3], totalsData[0][4], humanize.naturalsize(totalsData[0][5], binary=False, format="%.2f")]]

    totals_headers = [" " * (longestSubjectNameLength + 2), " Documents ", "  Topics  ", "  Pages  ", "   Size   "]
    totals_table = tabulate(totalsData, totals_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center"))

totals_table = totals_table.split("\n")

totals_table = totals_table[2:]

totals_table[0] = totals_table[0].replace("╪", "╤")
totals_table[0] = totals_table[0].replace("╞", "╒")
totals_table[0] = totals_table[0].replace("╡", "╕")



# Centring the totals table
for line in totals_table:

    lineLength = len(line)
    extraBit = (pageWidth - lineLength) / 2

    totals_table[totals_table.index(line)] = (" " * int(np.floor(extraBit))) + totals_table[totals_table.index(line)]




'''
PDF LINE LIST WRITING
'''


# Writing & formatting all the lines to the text list
text = []



# Contents page
maxNumSubjects = pageLength - 9 - subjectLikeThemeCount - 2 * (len(themes) - subjectLikeThemeCount)


if doThemesTable == True and len(subjectRows) > maxNumSubjects:

    print(f"Your report may have poor formatting as your number of subjects exceeds the maximum ({maxNumSubjects})!")

elif doThemesTable == False and len(subjectRows) > 30:

    print(f"Your report may have poor formatting as your number of subjects exceeds the maximum (30)!")


blankLinesNum = int(np.ceil((maxNumSubjects - int(len(subjectRows))) / 2)) - 1

for n in range(blankLinesNum):

    text.append("")

contentsLine = " " * 28 + "├" + singleSep * 10 + "  Contents  " + singleSep * 10 + "┤"
text.append(contentsLine)

text.append("")
text.append("")

if doThemesTable == True:

    text.append(" " * 14 + "Themes table ............................................. 3")
    text.append(" " * 14 + "Subjects table ........................................... 4")

else:

    text.append(" " * 14 + "Subjects table ........................................... 3")

text.append("")
text.append("")

for theme in themes:

    if not isinstance(theme, list):

        dollarsNum = 60 - (len(theme) + 1)

        text.append(" " * 14 + theme + " " + "$" * dollarsNum)
        text.append("")
    
    else:

        text.append(" " * 14 + theme[0])
        
        for subject in theme[1]:

            dollarsNum = 60 - (len(subject) + 1 + 2)

            text.append(" " * 14 + "- " + subject + " " + "$" * dollarsNum)
        
        text.append("")


if doGlossary == True:

    text.append("")

    dollarsNum = 60 - (len("Glossary") + 1)
    text.append(" " * 14 + "Glossary " + "$" * dollarsNum)



# Pushing themes/subject table onto the next page
currentIndex = len(text) - 1
currentIndexModulo = currentIndex % pageLength

push = (pageLength - 1) - currentIndexModulo

for x in range(push):

    text.append("")



# Themes table
if doThemesTable == True:

    themesLine = " " * 9 + "┌" + singleSep * 30 + "  Themes  " + singleSep * 30 + "┐"
    text.append(themesLine)

    text.append("")


    for line in theme_table:

        text.append(line)

    text.append("")


    for line in totals_table:

        text.append(line)



    # Moving subject section onto a new page
    currentIndex = len(text) - 1
    currentIndexModulo = currentIndex % pageLength

    push = (pageLength - 1) - currentIndexModulo


    for x in range(push):

        text.append("")



# Subjects table
subjectsLine = " " * 14 + "┌" + singleSep * 24 + "  Subjects  " + singleSep * 24 + "┐"
text.append(subjectsLine)
text.append("")


for line in subjects_table:

    text.append(line)

text.append("")


if doThemesTable == False:

    for line in totals_table:

        text.append(line)

topicsLine = " " * 19 + "┌" + singleSep * 19 + "  Topics  " + singleSep * 19 + "┐"
text.append(topicsLine)
text.append("")



# Topics list
for theme in topicsOverall:


    # Theme with no subjects
    if theme[0] in themes:

        text.append(doubleSep * pageWidth)
        text.append("")

        subjectLength = len("- " + theme[0] + " -")
        extraBit = (pageWidth - subjectLength) / 2

        text.append(" " * int(np.ceil(extraBit)) + f"- {theme[0]} -")

        text.append("")
        text.append(doubleSep * pageWidth)
        text.append("")

        if theme[1] == []:

            text.append("No PDF documents found in this folder")

        else:

            for topic in theme[1]:

                if isinstance(topic, list):

                    text.append(f"• {topic[0]}")

                    for flag in topic[1]:

                        text.append(f"    ‣ {flag}")


                else:
                    text.append(f"• {topic}")
    


    # Theme with subjects
    else:

        text.append(doubleSep * pageWidth)
        text.append("")

        themeLength = len("- " + theme[0] + " -")
        extraBit = (pageWidth - themeLength) / 2

        if (pageWidth - themeLength) % 2 == 0:

            text.append(" " * int(np.ceil(extraBit) + 1) + f"- {theme[0]} -")

        else:

            text.append(" " * int(np.ceil(extraBit)) + f"- {theme[0]} -")

        text.append("")
        text.append(doubleSep * pageWidth)
        text.append("")

        subjects = []

        for item in theme:

            if isinstance(item, list):

                for subject in item:

                    subjects.append(subject)


        for subject in subjects:

            subjectLength = len(" " + subject[0] + " ")
            extraBit = (pageWidth - subjectLength) / 2

            if (pageWidth - subjectLength) % 2 == 0:

                text.append(" " * int(np.ceil(extraBit) + 1) + f" {subject[0]} ")
                text.append(" " * int(np.ceil(extraBit) + 1) +  singleSep * len(f" {subject[0]} "))

            else:

                text.append(" " * int(np.ceil(extraBit)) + f" {subject[0]} ")
                text.append(" " * int(np.ceil(extraBit)) +  singleSep * len(f" {subject[0]} "))
                

            text.append("")

            if subject[1] == []:

                text.append("No PDF documents found in this subfolder")
            
            else:

                for topic in subject[1]:

                    if isinstance(topic, list):

                        text.append(f"• {topic[0]}")

                        for flag in topic[1]:

                            text.append(f"    ‣ {flag}")


                    else:
                        text.append(f"• {topic}")



# Appending glossary at the end of the document
if doGlossary == True:

    glossaryLine = " " * 19 + "┌" + singleSep * 19 + "  Glossary  " + singleSep * 19 + "┐"
    text.append(glossaryLine)
    text.append("")
    text.append("")

    with open(glossDir + glossName, "r") as f:

        lines = f.readlines()
        
        for line in lines[3:]:
            
            if "*" in line:

                text.append(line[:-1].replace("*", "▪"))
            
            else:

                text.append(line[:-1])

else:

    glossaryLine = None




'''
PDF LINE FORMATTING
'''


# Replacing the colons
for line in text:

    if ":" in line:

        text[text.index(line)] = text[text.index(line)].replace(":", "/")



# Wrapping text
textWrapped = []
inGloss = False

for line in text:

    if line == glossaryLine:

        inGloss = True


    if len(line) > pageWidth:

        if not inGloss:

            wrappedText = textwrap.wrap(line, width = pageWidth)

            for elem in wrappedText:

                if "‣" not in line:

                    if elem == wrappedText[0]:

                        textWrapped.append(elem)

                    else:

                        textWrapped.append("  " + elem)
                

                elif "‣" in line:

                    if elem == wrappedText[0]:

                        textWrapped.append("    " + elem)

                    else:

                        textWrapped.append("      " + elem)
        

        else:

            endSubject = line.index("-") + 2

            wrappedText = textwrap.wrap(line, width = (pageWidth - endSubject))

            for elem in wrappedText:

                if elem == wrappedText[0]:

                        textWrapped.append(elem)

                else:

                    textWrapped.append(" " * (endSubject) + elem)


    else:

        textWrapped.append(line)



# Formatting tables for PDF
textTablesDone = []

for index in range(len(textWrapped)):

    if index % pageLength == (pageLength - 1) and "┼" in textWrapped[index]:

        oneReplaced = textWrapped[index].replace("┼", "┴")
        twoReplaced = oneReplaced.replace("├", "└")
        threeReplaced = twoReplaced.replace("┤", "┘")

        textTablesDone.append(threeReplaced)


    elif index % pageLength == 0 and "┼" in textWrapped[index - 1]:

        oneReplaced = textWrapped[index - 1].replace("┼", "┬")
        twoReplaced = oneReplaced.replace("├", "┌")
        threeReplaced = twoReplaced.replace("┤", "┐")

        textTablesDone.append(threeReplaced)
        textTablesDone.append(textWrapped[index])


    elif index % pageLength == (pageLength - 2) and "┼" in textWrapped[index]:

        oneReplaced = textWrapped[index].replace("┼", "┴")
        twoReplaced = oneReplaced.replace("├", "└")
        threeReplaced = twoReplaced.replace("┤", "┘")

        textTablesDone.append(threeReplaced)
        textTablesDone.append(textWrapped[index])


    elif index % pageLength == (pageLength - 1) and "┼" in textWrapped[index - 1]:

        oneReplaced = textWrapped[index - 1].replace("┼", "┬")
        twoReplaced = oneReplaced.replace("├", "┌")
        threeReplaced = twoReplaced.replace("┤", "┐")

        textTablesDone.append(threeReplaced)
        textTablesDone.append(textWrapped[index])
        

    else:

        textTablesDone.append(textWrapped[index])



# Correcting any cross-page topics/flags and moving all new sections/subjects/themes onto a new page
finalText = []

runningIndex = 0
finalIndex = len(textTablesDone)

while runningIndex < finalIndex:

    listToSort = []

    if runningIndex == 0:

        for line in textTablesDone:

            listToSort.append(line)
        
    else:

        for line in finalText:

            listToSort.append(line)


    finalText = []

    subjectsStartLine = listToSort.index(subjectsLine)
    topicsStartLine = listToSort.index(topicsLine)

    if doGlossary == True:

        glossaryStartLine = listToSort.index(glossaryLine)


    for x in range(len(listToSort)):

        line = listToSort[x]

        nextBulletIndex = None


        # If we don't currently have a topic or subject in the glossary
        if "•" not in line and "▪" not in line:


            # Moving themes onto a new page
            if x > (topicsStartLine + 2) and (doubleSep in line) and x % pageLength != 0 and (doubleSep not in listToSort[x-4]):

                currentSepIndex = x

                currentSepModulo = currentSepIndex % pageLength

                push = pageLength - currentSepModulo

                for x in range(push):

                    finalText.append("")


                finalText.append(line)

                for rem in listToSort[currentSepIndex + 1:]:

                    finalText.append(rem)


                finalIndex = len(finalText)

                break
            


            # Moving sections onto new pages
            elif "┌" in line and x % pageLength != 0 and x >= topicsStartLine:

                currentStartIndex = x

                currentStartModulo = currentStartIndex % pageLength

                push = pageLength - currentStartModulo

                for x in range(push):

                    finalText.append("")


                finalText.append(line)


                for rem in listToSort[currentStartIndex + 1:]:

                    finalText.append(rem)


                finalIndex = len(finalText)

                break



            # Moving subjects onto new pages
            elif x > topicsStartLine and x % pageLength != 0 and singleSep in listToSort[x+1] and (doubleSep not in listToSort[x-2]) and (("•" in listToSort[x+3]) or ("No PDF documents found in this subfolder" in listToSort[x+3])):

                currentSubjectIndex = x

                currentSubjectModulo = currentSubjectIndex % pageLength

                push = pageLength - currentSubjectModulo


                for x in range(push):

                    finalText.append("")


                finalText.append(line)


                for rem in listToSort[currentSubjectIndex + 1:]:

                    finalText.append(rem)


                finalIndex = len(finalText)

                break



            # Adding the line if none of the above apply
            else:

                finalText.append(line)

                if x >= runningIndex:

                    runningIndex += 1

                continue



        # Checking and sorting out all the topics, and the glossary
        elif "•" in line or "▪" in line:

            currentBulletIndex = listToSort.index(line)

            currentBulletModulo = currentBulletIndex % pageLength


            # Finding the next bullet point
            for part in listToSort[currentBulletIndex+1:]:

                if "•" in part or "▪" in part:

                    nextBulletIndex = listToSort.index(part)

                    break



            # Sorting out the last bullet point
            if nextBulletIndex == None:

                finalText.append(line)

                if x >= runningIndex:

                    runningIndex += 1

                continue



            # Sorting out last topic in topics list
            if doGlossary == True:

                if nextBulletIndex > glossaryStartLine and currentBulletIndex < glossaryStartLine:

                    finalText.append(line)

                    if x >= runningIndex:

                        runningIndex += 1

                    continue

            nextBulletModulo = nextBulletIndex % pageLength

            

            # Check if next bullet is on same page as current bullet or at very top of next page
            if (nextBulletModulo > currentBulletModulo):

                finalText.append(line)

                if x >= runningIndex:

                    runningIndex += 1

                continue



            # This implies the next bullet is on the next page
            else:

                push = pageLength - currentBulletModulo


                # Only correcting the bullet point position if not at top of next page
                if nextBulletModulo != 0:

                    dividerCount = 0


                    # Finding the number of dividers between current bullet point and the next one
                    for part in listToSort[currentBulletIndex:nextBulletIndex+1]:

                        if singleSep in part or doubleSep in part:

                            dividerCount += 1

                            break



                    # Pushing the current bullet onto the next page if it won't fit on the current one
                    if dividerCount == 0:

                        for x in range(push):

                            finalText.append("")


                        finalText.append(line)


                        for rem in listToSort[currentBulletIndex + 1:]:

                            finalText.append(rem)

                        finalIndex = len(finalText)

                        break



                    # Appending the current line if it can fit on the current age
                    elif dividerCount > 0:

                        finalText.append(line)

                        if x >= runningIndex:

                            runningIndex += 1

                        continue



                # Appending bullet point if no problems
                else:

                    finalText.append(line)

                    if x >= runningIndex:

                        runningIndex += 1

                    continue



# Getting page numbers of subjects & glossary
if doGlossary == True:

    glossaryStartLine = finalText.index(glossaryLine)

topicsStartLine = finalText.index(topicsLine)

pageNums = []

for theme in themes:


    # If we have a subject-like theme
    if not isinstance(theme, list):

        for x in range(len(finalText)):

            if doGlossary == True:

                if x < glossaryStartLine and x > topicsStartLine:

                    line = finalText[x]

                    if f" - {theme} -" in line:
                        
                        pageNum = (x // 69) + 2

                        pageNums.append([theme, pageNum])

                        break
            
            else:

                if x > topicsStartLine:

                    line = finalText[x]

                    if f" - {theme} -" in line:

                        pageNum = (x // 69) + 2

                        pageNums.append([theme, pageNum])

                        break

    

    # If we do not have a subject-like theme
    elif isinstance(theme, list):

        for subject in theme[1]:

            for x in range(len(finalText)):

                if doGlossary == True:

                    if x < glossaryStartLine and x > topicsStartLine:

                        line = finalText[x]
                        
                        if f" {subject} " in line and singleSep in finalText[x+1]:

                            pageNum = (x // 69) + 2

                            pageNums.append([subject, pageNum])

                            break
                

                else:

                    if x > topicsStartLine:

                        line = finalText[x]

                        if f" {subject} " in line and singleSep in finalText[x+1]:

                            pageNum = (x // 69) + 2

                            pageNums.append([subject, pageNum])

                            break



# Finding the glossary          
if doGlossary == True:

    for x in range(len(finalText)):

        line = finalText[x]

        if line == glossaryLine:

            pageNum = (x // 69) + 2

            pageNums.append(["Glossary", pageNum])

            break



# Adding page numbers back into the glossary
if doThemesTable == True:

    themesStartLine = finalText.index(themesLine)

else:

    themesLine = subjectsLine
    themesStartLine = finalText.index(themesLine)

contentsStartLine = finalText.index(contentsLine)

for x in range(len(finalText)):

    line = finalText[x]

    if "$" in line:


        # Finding position of subject name
        for char in line:

            if char != " " and char != "-":

                subjectNameStart = line.index(char)

                break
        

        for char in line:

            if char == "$":

                subjectNameEnd = line.index(char) - 2

                break
        
        subjectName = line[subjectNameStart:subjectNameEnd + 1]



        # Swapping out $ signs for the dots and the page numbers
        for subject in pageNums:

            if subjectName == subject[0]:

                if subjectName in themes or subjectName == "Glossary":

                    numDots = 74 - 2 - 14 - len(subjectName) - len(str(subject[1]))

                    finalText[x] = " " * 14 + subjectName + " " + "." * numDots + " " + str(subject[1])


                else:

                    numDots = 74 - 2 - 14 - 2 - len(subjectName) - len(str(subject[1]))

                    finalText[x] = " " * 14 + "- " + subjectName + " " + "." * numDots + " " + str(subject[1])



    # Stopping when neccessary
    elif line == themesLine:

        break

    else:

        continue



# Fixing any potential blank lines at top of extra pages of glossary
textToWrite = []

for x in range(len(finalText)):

    if doGlossary == True:

        if x < glossaryStartLine:

            textToWrite.append(finalText[x])
        
        else:

            if x % pageLength == 0 and finalText[x] == "":

                continue

            else:

                textToWrite.append(finalText[x])
    

    else:

        textToWrite.append(finalText[x])

print("--> Lines prepared!\n")




'''
WRITING TO PDF
'''


print("--> Writing to PDF...")


# Setting up the PDF
pdf = FPDF(orientation = "P", format = "A4")
pdf.add_page()
pdf.add_font("Menlo", "", fontFileDir + fontFile, uni=True)
pdf.set_auto_page_break(auto = True, margin = 8.0)



# Getting date and time info
today = dt.date.today()
dateDay = today.day
dateMonth = today.month
dateYear = today.year

now = dt.datetime.now()
timeNow = now.strftime("%H:%M")

dateToday = dt.datetime(dateYear, dateMonth, dateDay)


def get_ending(dayNum):

    if "1" in dayNum[-1] and dayNum != "11":

        return "st"

    elif "2" in dayNum[-1] and dayNum != "12":

        return "nd"

    elif "3" in dayNum[-1] and dayNum != "13":

        return "rd"

    else:

        return "th"


formattedDate = dateToday.strftime(f"%d{get_ending(str(dateDay))} %b %Y")



# Writing title page
pdf.set_font("Menlo", size = 10)

for i in range(16):

    pdf.cell(0, 4, txt="", ln=1)



# Writing title
pdf.set_font("Menlo", size = 32)
titleLength = len(f"{archive_name} Report")
titleLine = int(np.ceil((27 - titleLength)/2)) * " " + f"{archive_name} Report"
pdf.cell(0, 4, txt=titleLine, ln=1)

pdf.set_font("Menlo", size = 10)

for i in range(6):

    pdf.cell(0, 4, txt="", ln=1)



# Writing date and time
pdf.set_font("Menlo", size = 18)
datetimeLength = len(timeNow + "  ~  " + formattedDate)
dateLine = int(np.ceil((49 - datetimeLength)/2)) * " " + timeNow + "  ~  " + formattedDate
pdf.cell(0, 4, txt=dateLine, ln=1)

pdf.set_font("Menlo", size = 10)

for i in range(41):

    pdf.cell(0, 4, txt="", ln=1)



# Writing version number
pdf.set_font("Menlo", size = 18)
versionLength = len(version)
versionLine = int(np.ceil((49 - versionLength)/2)) * " " + version
pdf.cell(0, 4, txt=versionLine, ln=1)

pdf.set_font("Menlo", size = 10)

for i in range(3):

    pdf.cell(0, 4, txt="", ln=1)



# Writing remainder of the lines
pdf.set_font("Menlo", size = 10)

for x in range(len(textToWrite)):

    pdf.cell(0, 4, txt=textToWrite[x], ln=1)

pdf.output(f"{archive_name} Report.pdf")

print("--> PDF written!\n")



# Deleting temporary .pkl files
try:

    os.remove(fontFileDir + f"{fontFile[:-4]}.cw127.pkl")

except FileNotFoundError:

    pass

os.remove(fontFileDir + f"{fontFile[:-4]}.pkl")



# End of program message
endTime = time.time()
runningTime = round(endTime - startTime, 2)

print(f"--> Finished in {runningTime}s!\n")

print(runningSep * (len(f"{runningSep * numSep} {startLine} {runningSep * numSep}") + 2) + "\n\n")
