# Archysis
# by Sam Wallis-Riches, 2022


import time
startTime = time.time()

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
from sys import exit

warnings.filterwarnings("ignore")




'''
INITIAL SETUP
'''


# Setting initial variables & starting the clock
version = "v3.19.1"

ext = ".pdf"

singleSep = "─"
boldSep = "━"
doubleSep = "═"

pageWidth = 88
pageLength = 69

doThemesTable = True
doGlossary = True



# Printing beginning verbose lines
startLine = f"Archysis {version}"

numSep = int(np.ceil((66 - len(f" {startLine} ")) / 2))
print(f"\n\n{singleSep * (numSep + 1)} {startLine} {singleSep * (numSep + 1)}\n")



# Getting archive directory and finding it
wantedDir = input("Enter directory of archive: ")

runFromDir = os.path.dirname(os.path.realpath(__file__))

print(f"\n──▶ Looking for {wantedDir} folder...")

if ":" in runFromDir:

    lookForDir = rf"C:{os.sep}Users"

else:

    lookForDir = rf"{os.sep}Users"

archDir = None


for root, dirs, files in os.walk(lookForDir):

    dirLength = len(root) - len(wantedDir)

    if root[dirLength:] == wantedDir:

        archDir = root

        break


if archDir == None:

    print(f"\n──▶ {wantedDir} folder not found!\n")
    exit()

else:

    # Getting archive name
    archive_name = archDir.split(os.sep)[-1]

    directory_contents = os.listdir(archDir)

    print(f"──▶ {wantedDir} folder found!\n")
    print(f"──▶ {archive_name} Report will be generated!\n")



# Getting directory of font file
fontFile = "archysis_font"
fontFileList = [f"{fontFile}.ttf", f"{fontFile}.otf"]
fontFileDir = None
fontExt = None

print("──▶ Looking for font file...")


for root, dirs, files in os.walk(lookForDir):

    
    for filename in files:

        if filename == fontFileList[0]:

            fontFileDir = os.path.abspath(os.path.join(root, filename))[:-len(fontFileList[0])]
            
            if "Trash" in fontFileDir or "Recycle.Bin" in fontFileDir:

                fontFileDir = None

                continue
            
            fontFile = fontFileList[0]

            break
        

        elif filename == fontFileList[1]:

            fontFileDir = os.path.abspath(os.path.join(root, filename))[:-len(fontFileList[1])]
            
            if "Trash" in fontFileDir or "Recycle.Bin" in fontFileDir:

                fontFileDir = None

                continue
            
            fontFile = fontFileList[1]

            break


    if fontFileDir != None:

        break



# Terminating if no font file can be found
if fontFileDir == None:

    print("──▶ No font file found!\n")
    exit()

else:

    print("──▶ Font file found!\n")



# Getting directory of glossary file
glossDir = None
glossName = f"{archive_name.lower()}_glossary.txt"

print("──▶ Looking for glossary file...")

for root, dirs, files in os.walk(lookForDir):

    for filename in files:

        if filename == glossName:

            glossDir = os.path.abspath(os.path.join(root, filename))[:-len(glossName)]

            if "Trash" in glossDir or "Recycle.Bin" in glossDir:

                glossDir = None

                continue

            break


    if glossDir != None:

        break



# Determining whether a glossary can/will be written
if glossDir == None:

    print("──▶ No glossary file found!\n")
    
    doGlossary = False

else:

    print("──▶ Glossary file found!\n")



# Getting each of the theme names
themes = []

subjectLikeThemeCount = 0

for folder in directory_contents:

    if (os.path.isdir(os.path.join(archDir, folder))) and ("." not in folder):

        subjects = []


        # Looping over subject subdirectories
        for subject in os.listdir(os.path.join(archDir, folder)):

            if (os.path.isdir(os.path.join(archDir, folder, subject))) and ("." not in subject):

                subjects.append(subject)


        if subjects != []:

            themes.append([folder, subjects])

        else:

            subjectLikeThemeCount += 1

            themes.append(folder)



# Terminating if no folders are found
if themes == []:

    print("\n──▶ No folders found to analyse!\n")

    exit()



# Establishing if all themes are subject-like
if subjectLikeThemeCount == len(themes):

    doThemesTable = False



# Sorting themes & subjects alphabetically
def get_theme_name(element):


    # If we have a theme with subjects
    if isinstance(element, list):

        return element[0]
    

    # If we have a subject-like theme
    else:

        return element


themes = sorted(themes, key=get_theme_name)
num_themes = len(themes)

for theme in themes:


    # Only need to sort the subjects if we have subjects
    if isinstance(theme, list):

        themes[themes.index(theme)][1] = sorted(theme[1])




'''
DATA EXTRACTION
'''


# Setting up the lists for the data
totalsData = [len(themes), 0, 0, 0, 0, 0]

overallData = []

themesData = []

topicsOverall = []

subjectTopicVals = []
subjectFileVals = []
subjectPageVals = []
subjectSizeVals = []

filesToFix = []



# Getting all the data
for theme in themes:

    subjects = 0
    topics = 0
    files = 0
    pages = 0
    size = 0

    running_subjects = ""



    # Getting data if theme has subjects
    if isinstance(theme, list):

        themeData = [theme[0], []]

        themeTopics = [theme[0], []]

        if themes.index(theme) == 0:

            print(f"──▶ Reading {theme[0]} folders...")

        else:

            print(f"\n──▶ Reading {theme[0]} folders...")



        # Running through all subjects
        for subject in theme[1]:

            topicsSubject = []

            subjectTopics = 0
            subjectFiles = 0
            subjectPages = 0
            subjectSize = 0

            subjects += 1
            totalsData[1] += 1

            running_subjects += "▪ " + subject + "\n"



            # Going through each of the files
            for filename in os.listdir(os.path.join(archDir, theme[0], subject)):


                # If we have a PDF
                if ext in filename:
                    


                    # Getting files data
                    totalsData[3] += 1
                    subjectFiles += 1
                    files += 1



                    # Getting size data
                    totalsData[5] += os.path.getsize(os.path.join(archDir, theme[0], subject, filename))
                    subjectSize += os.path.getsize(os.path.join(archDir, theme[0], subject, filename))
                    size += os.path.getsize(os.path.join(archDir, theme[0], subject, filename))



                    # Getting pages data & checking files
                    with open(os.path.join(archDir, theme[0], subject, filename), "rb") as f:

                        try:

                            pdf = PdfFileReader(f)

                        except PyPDF2.errors.PdfReadError:

                            filesToFix.append(f"{theme[0]} / {subject}: {filename} (Corrupted file)")

                            continue

                        except PyPDF2.errors.DependencyError:

                            filesToFix.append(f"{theme[0]} / {subject}: {filename} (Encryption error)")

                            continue


                        try:

                            totalsData[4] += pdf.getNumPages()
                            subjectPages += pdf.getNumPages()
                            pages += pdf.getNumPages()

                        except PyPDF2.errors.PdfReadError:

                            filesToFix.append(f"{theme[0]} / {subject}: {filename} (Corrupted file)")

                            continue

                        except ValueError:

                            filesToFix.append(f"{theme[0]} / {subject}: {filename} (Corrupted file)")

                            continue

                        

                    # Getting topics data
                    if "[" not in filename:

                        totalsData[2] += 1
                        subjectTopics += 1
                        topics += 1


                    if ("[" in filename) and ("[1]" in filename):

                        totalsData[2] += 1
                        subjectTopics += 1
                        topics += 1
                    


                    # Getting topics
                    topicsSubject.append(filename[:-4])



            # Appending all values to necessary lists
            subjectTopicVals.append(subjectTopics)
            subjectFileVals.append(subjectFiles)
            subjectPageVals.append(subjectPages)
            subjectSizeVals.append(subjectSize)

            themeData[1].append([subject,  str(subjectTopics), str(subjectFiles), str(subjectPages), humanize.naturalsize(subjectSize, binary=False, format="%.1f")])



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


            def get_topic(element):

                if element[0] == "'" or element[0] == "‘":

                    return element[1:].lower()
                

                else:

                    return element.lower()


            topicsSubjectActual = sorted(topicsSubjectActualList, key=get_topic)



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
                

                # If we have flags
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
                
            

            # Getting and adding counts for each topic
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

            print(f"    ▪ {subject} ✓")
        


        # Appending all necessary values
        themesData.append([theme[0], "["+ str(subjects) + "]\n\n" + running_subjects + "§", str(topics), str(files), str(pages), size])

        overallData.append(themeData)
        topicsOverall.append(themeTopics)



    # Getting data if theme has no subjects
    else:

        themeData = [theme]

        themeTopics = [theme]

        topicsSubject = []

        subjectTopics = 0
        subjectFiles = 0
        subjectPages = 0
        subjectSize = 0


        if themes.index(theme) == 0:

            print(f"──▶ Reading {theme} folder...")

        else:

            print(f"\n──▶ Reading {theme} folder...")



        # Going through all files
        for filename in os.listdir(os.path.join(archDir, theme)):


            # If we have a PDF
            if ext in filename:



                # Getting file data
                totalsData[3] += 1
                subjectFiles += 1
                files += 1



                # Getting size data
                totalsData[5] += os.path.getsize(os.path.join(archDir, theme, filename))
                subjectSize += os.path.getsize(os.path.join(archDir, theme, filename))
                size += os.path.getsize(os.path.join(archDir, theme, filename))



                # Getting pages data & checking files
                with open(os.path.join(archDir, theme, filename), "rb") as f:

                    try:

                        pdf = PdfFileReader(f)

                    except PyPDF2.errors.PdfReadError:

                        filesToFix.append(f"{theme}: {filename} (Corrupted file)")

                        continue

                    except PyPDF2.errors.DependencyError:

                        filesToFix.append(f"{theme}: {filename} (Encryption error)")

                        continue


                    try:

                        totalsData[4] += pdf.getNumPages()
                        subjectPages += pdf.getNumPages()
                        pages += pdf.getNumPages()

                    except PyPDF2.errors.PdfReadError:

                        filesToFix.append(f"{theme}: {filename} (Corrupted file)")

                        continue

                    except ValueError:

                        filesToFix.append(f"{theme}: {filename} (Corrupted file)")
                        
                        continue

                    

                # Getting topics data
                if "[" not in filename:

                    totalsData[2] += 1
                    subjectTopics += 1
                    topics += 1

                if ("[" in filename) and ("[1]" in filename):

                    totalsData[2] += 1
                    subjectTopics += 1
                    topics += 1



                # Getting topics
                topicsSubject.append(filename[:-4])



        # Appending all values to necessary lists
        if not doThemesTable:

            subjectTopicVals.append(subjectTopics)
            subjectFileVals.append(subjectFiles)
            subjectPageVals.append(subjectPages)
            subjectSizeVals.append(subjectSize)


        themeData.append(str(subjectTopics))
        themeData.append(str(subjectFiles))
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


        def get_topic(element):

                if element[0] == "'" or element[0] == "‘":

                    return element[1:].lower()
                

                else:

                    return element.lower()


        topicsSubjectActual = sorted(topicsSubjectActualList, key=get_topic)



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


            # If we have flags
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



        # Getting and adding counts for each topic
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



        # Appending all data to the lists
        themeTopics.append(topicsSubjectActual)

        themesData.append([theme, 3 * singleSep, str(topics), str(files), str(pages), size])

        overallData.append(themeData)
        topicsOverall.append(themeTopics)

        print(f"    ◆ {theme} ✓")



# Terminating if not PDFs found
if totalsData[3] == 0:

    print("\n──▶ No PDF files found!\n")

    exit()



# Writing list of files to fix, if necessary
if filesToFix != []:

    with open(f"{archDir + os.sep}Files to fix.txt", "w") as f:

        f.write("# Files to fix\n\n")

        for filename in filesToFix:

            f.write(f"* {filename}\n")
        
        f.write("\n\n(This plaintext file can be deleted once all files have been fixed!)\n")


    print("\n──▶ File check & read complete!\n")
    print("\n──▶ Fix files listed in 'Files to fix.txt'\n")

    exit()

else:

    print("\n──▶ File check & read complete!")
    print("──▶ All files OK!\n")




'''
DATA FORMATTING FOR REPORT
'''


print("──▶ Formatting data for writing...")



# Formatting and tabulating the theme data, if necessary
if doThemesTable:

    themeSubVals = []
    themeTopVals = []
    themeFileVals = []
    themePageVals = []
    themeSizeVals = []



    # Looping through the themes to find the highest values
    for theme in themesData:


        # Only doing this for non-subject-like themes
        if (3 * singleSep) not in theme[1]:
            
            endSubNum = theme[1].index("]")

            themeSubVals.append(int(theme[1][1:endSubNum]))

        themeTopVals.append(int(theme[2]))

        themeFileVals.append(int(theme[3]))

        themePageVals.append(int(theme[4]))

        themeSizeVals.append(int(theme[5]))

    

    # Finding the maxima
    maxThemesSubs = max(themeSubVals)
    maxThemesTops = max(themeTopVals)
    maxThemesFiles = max(themeFileVals)
    maxThemesPages = max(themePageVals)
    maxThemesSize = max(themeSizeVals)



    # Adding in the indicators, where necessary
    for theme in themesData:
        
        if (3 * singleSep) not in theme[1]:

            endSubNum = theme[1].index("]")

            if int(theme[1][1:endSubNum]) == maxThemesSubs:

                themesData[themesData.index(theme)][1] = "> [" + str(maxThemesSubs) + "] <" + theme[1][endSubNum + 1:]
        

        if int(theme[2]) == maxThemesTops:

            themesData[themesData.index(theme)][2] = "> " + str(maxThemesTops) + " <"


        if int(theme[3]) == maxThemesFiles:

            themesData[themesData.index(theme)][3] = "> " + str(maxThemesFiles) + " <"

        
        if int(theme[4]) == maxThemesPages:

            themesData[themesData.index(theme)][4] = "> " + str(maxThemesPages) + " <"

        
        if int(theme[5]) == maxThemesSize:

            themesData[themesData.index(theme)][5] = "> " + humanize.naturalsize(maxThemesSize, binary=False, format="%.1f") + " <"
        
        else:

            themesData[themesData.index(theme)][5] = humanize.naturalsize(theme[5], binary=False, format="%.1f")



    # Forming the table
    theme_headers = ["Theme", "Subjects", "Topics", "Files", "Pages", "Size"]
    theme_table = tabulate(themesData, theme_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center", "center"))
    theme_table = theme_table.replace("§", " ")
    theme_table = theme_table.split("\n")



    # Centring the themes table
    for line in theme_table:

        lineLength = len(line)
        extraBit = (pageWidth - lineLength) / 2

        theme_table[theme_table.index(line)] = (" " * int(np.ceil(extraBit))) + theme_table[theme_table.index(line)]



# Getting the highest values within subhect data and formatting them in their respective lists
maxTopics = max(subjectTopicVals)
maxFiles = max(subjectFileVals)
maxPages = max(subjectPageVals)
maxSize = max(subjectSizeVals)


for theme in overallData:


    # Non-subject-like theme
    if isinstance(theme[1], list):


        # Running through all subjects
        for subject in theme[1]:


            if int(subject[1]) == maxTopics:

                overallData[overallData.index(theme)][1][theme[1].index(subject)][1] = "> " + str(maxTopics) + " <"


            if int(subject[2]) == maxFiles:

                overallData[overallData.index(theme)][1][theme[1].index(subject)][2] = "> " + str(maxFiles) + " <"


            if int(subject[3]) == maxPages:

                overallData[overallData.index(theme)][1][theme[1].index(subject)][3] = "> " + str(maxPages) + " <"


            if subject[4] == humanize.naturalsize(maxSize, binary=False, format="%.1f"):

                overallData[overallData.index(theme)][1][theme[1].index(subject)][4] = "> " + humanize.naturalsize(maxSize, binary=False, format="%.1f") + " <"
    


    # Subject-like theme
    else:

        if int(theme[1]) == maxTopics:

            overallData[overallData.index(theme)][1] = "> " + str(maxTopics) + " <"


        if int(theme[2]) == maxFiles:

            overallData[overallData.index(theme)][2] = "> " + str(maxFiles) + " <"


        if int(theme[3]) == maxPages:

            overallData[overallData.index(theme)][3] = "> " + str(maxPages) + " <"


        if theme[4] == humanize.naturalsize(maxSize, binary=False, format="%.1f"):

            overallData[overallData.index(theme)][4] = "> " + humanize.naturalsize(maxSize, binary=False, format="%.1f") + " <"



# Getting rows of subject table & sorting them
subjectRows = []
for theme in overallData:


    # If we have a theme with subjects
    if isinstance(theme[1], list):

        for subject in theme[1]:

            subjectRows.append(subject)
    
    else:

        if not doThemesTable:

            subjectRows.append(theme)


def subject_name(element):

    return element[0]


subjectRows = sorted(subjectRows, key=subject_name)



# Formatting and tabulating the subject data
subject_headers = ["Subject", "  Topics  ", "  Files  ", "  Pages  ", "   Size   "]
subjects_table = tabulate(subjectRows, subject_headers, tablefmt="fancy_grid", colalign=("center", "center", "center", "center", "center"))
subjects_table = subjects_table.split("\n")



# Centring the subjects table
for line in subjects_table:

    lineLength = len(line)
    extraBit = (pageWidth - lineLength) / 2

    subjects_table[subjects_table.index(line)] = (" " * int(np.ceil(extraBit))) + subjects_table[subjects_table.index(line)]




'''
PDF LINE LIST WRITING
'''


# Writing & formatting all the lines to the text list
text = []



# Contents page
extraLines = 5

if doThemesTable == True:

    extraLines += 1


if doGlossary == True:

    extraLines += 3



# Finding and adding the maximum number of lines to 'centre' the contents page vertically
maxNumSubjectsForPush = pageLength - extraLines - subjectLikeThemeCount - 2 * (totalsData[0] - subjectLikeThemeCount)

blankLinesNum = int(np.ceil((maxNumSubjectsForPush - (totalsData[1] + subjectLikeThemeCount)) / 2)) - 1

for n in range(blankLinesNum):

    text.append("")



# Getting lengths of theme names
themeLengths = []

for theme in themesData:

    themeLengths.append(len(theme[0]))

longestThemeNameLength = max(themeLengths)



# Getting lengths of subject names
subjectLengths = []

for subject in subjectRows:

    subjectLengths.append(len(subject[0]))

longestSubjectNameLength = max(subjectLengths)


longestDirNameLength = max([longestSubjectNameLength, longestThemeNameLength])



# Sorting width of contents
if longestDirNameLength > 60 and longestDirNameLength < pageWidth:

    contentsWidth = longestDirNameLength

    gapWidth = int(np.ceil((pageWidth - contentsWidth) / 2))


elif longestDirNameLength > pageWidth:

    contentsWidth = pageWidth

    gapWidth = 0


else:

    contentsWidth = 60

    gapWidth = int(np.ceil((pageWidth - contentsWidth) / 2))



# Writing the contents line
contentsLine = " " * 28 + "╋" + boldSep * 10 + "  Contents  " + boldSep * 10 + "╋"
text.append(contentsLine)

text.append("")
text.append("")



# Writing the tables lines
if doThemesTable == True:

    dollarsNum = contentsWidth - (len("Themes") + 1)

    text.append(" " * gapWidth + "Themes" + " " + "$" * dollarsNum)


    dollarsNum = contentsWidth - (len("Subjects") + 1)

    text.append(" " * gapWidth + "Subjects" + " " + "$" * dollarsNum)

else:

    dollarsNum = contentsWidth - (len("Subjects") + 1)

    text.append(" " * gapWidth + "Subjects" + " " + "$" * dollarsNum)


text.append("")



# Adding each of the subjects' lines
for theme in themes:


    # If we have a subject-like theme
    if not isinstance(theme, list):

        lineModulo = len(text) % pageLength


        # Only want a new line if not at top of page
        if lineModulo != 0:

            text.append("")

        dollarsNum = contentsWidth - (len(theme) + 1)

        text.append(" " * gapWidth + theme + " " + "$" * dollarsNum)

    

    # If we have a theme with subjects
    else:

        lineModulo = len(text) % pageLength


        # Only want a new line if not at top of page
        if lineModulo != 0:

            text.append("")



        # Don't want to start new theme at bottom of page
        lineModulo = len(text) % pageLength

        if lineModulo != (pageLength - 1):

            text.append(" " * gapWidth + "╼ " + theme[0])

        elif lineModulo == (pageLength - 1):

            text.append("")
            text.append(" " * gapWidth + "╼ " + theme[0])
        


        # Running through all subjects
        for subject in theme[1]:

            dollarsNum = contentsWidth - (len(subject) + 1 + 2)

            text.append(" " * gapWidth + "▪ " + subject + " " + "$" * dollarsNum)
        


# Adding the glossary's line
if doGlossary == True:

    lineModulo = len(text) % pageLength

    # Only want a new line if not at top of page
    if lineModulo != 0:

        text.append("")


    lineModulo = len(text) % pageLength

    # Only want a new line if not at top of page
    if lineModulo != 0:

        text.append("")

    dollarsNum = contentsWidth - (len("Glossary") + 1)
    text.append(" " * gapWidth + "Glossary " + "$" * dollarsNum)



# Pushing themes/subject table onto the next page
currentIndex = len(text) - 1
currentIndexModulo = currentIndex % pageLength

push = (pageLength - 1) - currentIndexModulo

for x in range(push):

    text.append("")



# Themes table
if doThemesTable == True:

    themesLine = " " * 9 + "┣" + boldSep * 30 + "  Themes  " + boldSep * 30 + "┫"
    text.append(themesLine)

    text.append("")



    # Writing themes table
    for line in theme_table:

        text.append(line)

    text.append("")



    # Moving subject section onto a new page
    currentIndex = len(text) - 1
    currentIndexModulo = currentIndex % pageLength

    push = (pageLength - 1) - currentIndexModulo


    for x in range(push):

        text.append("")


else:

    themesLine = None



# Subjects table
subjectsLine = " " * 14 + "┣" + boldSep * 24 + "  Subjects  " + boldSep * 24 + "┫"
text.append(subjectsLine)
text.append("")



# Writing subjects table
for line in subjects_table:

    text.append(line)

text.append("")



# Writing topics line
topicsLine = " " * 19 + "┣" + boldSep * 19 + "  Topics  " + boldSep * 19 + "┫"
text.append(topicsLine)
text.append("")



# Topics list
for theme in topicsOverall:


    # Theme with no subjects
    if theme[0] in themes:


        # Adding the header
        text.append(doubleSep * pageWidth)
        text.append("")

        subjectLength = len("— " + theme[0] + " —")
        extraBit = (pageWidth - subjectLength) / 2

        text.append(" " * int(np.ceil(extraBit)) + f"— {theme[0]} —")

        text.append("")
        text.append(doubleSep * pageWidth)
        text.append("")



        # Giving a statement if the theme is empty
        if theme[1] == []:

            text.append("No PDF files found in this folder!")


        # Otherwise, writing the topics list
        else:

            for topic in theme[1]:


                # If we have flags
                if isinstance(topic, list):

                    text.append(f"• {topic[0]}")

                    for flag in topic[1]:

                        text.append(f"    ‣ {flag}")


                # If we have no flags
                else:
                    text.append(f"• {topic}")
    


    # Theme with subjects
    else:


        # Writing header
        text.append(doubleSep * pageWidth)
        text.append("")

        themeLength = len("- " + theme[0] + " -")
        extraBit = (pageWidth - themeLength) / 2

        if (pageWidth - themeLength) % 2 == 0:

            text.append(" " * int(np.ceil(extraBit) + 1) + f"╼ {theme[0]} ╾")

        else:

            text.append(" " * int(np.ceil(extraBit)) + f"╼ {theme[0]} ╾")

        text.append("")
        text.append(doubleSep * pageWidth)
        text.append("")



        # Getting subjects for current theme
        subjects = []

        for item in theme:

            if isinstance(item, list):

                for subject in item:

                    subjects.append(subject)



        # Looping over subjects
        for subject in subjects:



            # Writing 'header' for subject
            subjectLength = len(" " + subject[0] + " ")
            extraBit = (pageWidth - subjectLength) / 2

            if (pageWidth - subjectLength) % 2 == 0:

                text.append(" " * int(np.ceil(extraBit) + 1) + f" {subject[0]} ")
                text.append(" " * int(np.ceil(extraBit) + 1) +  singleSep * len(f" {subject[0]} "))

            else:

                text.append(" " * int(np.ceil(extraBit)) + f" {subject[0]} ")
                text.append(" " * int(np.ceil(extraBit)) +  singleSep * len(f" {subject[0]} "))
                

            text.append("")



            # Writing a statement if subject is empty
            if subject[1] == []:

                text.append("No PDF files found in this subfolder!")
            


            # Otherwise, writing the topics list
            else:

                for topic in subject[1]:


                    # If we have flags
                    if isinstance(topic, list):

                        text.append(f"• {topic[0]}")

                        for flag in topic[1]:

                            text.append(f"    ‣ {flag}")


                    # If we have no flags
                    else:
                        text.append(f"• {topic}")



# Appending glossary at the end of the report
if doGlossary == True:


    # Writing glossary line
    glossaryLine = " " * 19 + "┣" + boldSep * 19 + "  Glossary  " + boldSep * 19 + "┫"
    text.append(glossaryLine)
    text.append("")
    text.append("")



    # Reading from glossary file
    with open(glossDir + glossName, "r") as f:

        lines = f.readlines()



    # Establising the length of the glossary
    lengthGloss = (len(lines) - 3 + 1) / 2



    # Getting all the entries, and replacing their bullets
    glossEntries = []
    
    for line in lines:
        
        if "*" in line:

            endSubIndex = line.index(":")

            subName = line[2:endSubIndex]

            if subName not in themes:

                glossEntries.append([subName, line[:-1].replace("*", "▪")])
            
            else:

                glossEntries.append([subName, line[:-1].replace("*", "◆")])



    # Alphabetising the entries
    def get_subject(subject):

        return subject[0]
    

    glossEntries = sorted(glossEntries, key=get_subject)



    # Writing all the glossary entries
    for line in glossEntries:

        text.append(line[1])

        if line != glossEntries[-1]:

            text.append("")


else:

    glossaryLine = None




'''
PDF LINE FORMATTING
'''


# Replacing the colons
for line in text:

    if ":" in line and "▪" not in line and "◆" not in line:

        text[text.index(line)] = text[text.index(line)].replace(":", "/")



# Wrapping text
textWrapped = []
inGloss = False

for line in text:



    # Getting ready for a different case when we're in the glossary
    if line == glossaryLine:

        inGloss = True



    # If line is too long
    if len(line) > pageWidth:



        # 'Regular' wrapping
        if not inGloss:

            wrappedText = textwrap.wrap(line, width = pageWidth)

            for elem in wrappedText:


                # If no flag, add either no indent or a double-space indent, for alignment
                if "‣" not in line:

                    if elem == wrappedText[0]:

                        textWrapped.append(elem)

                    else:

                        textWrapped.append("  " + elem)
                

                # If we have a flag, add a four-space indent or a six-space indent, for alignment
                elif "‣" in line:

                    if elem == wrappedText[0]:

                        textWrapped.append("    " + elem)

                    else:

                        textWrapped.append("      " + elem)
        


        # If we're in the glossary
        else:

            
            # Finding how wide the subject of the line is, and then wrapping the line
            endSubject = line.index(":") + 2

            wrappedText = textwrap.wrap(line, width = pageWidth, subsequent_indent=(" " * endSubject))

            for elem in wrappedText:

                textWrapped.append(elem)



    # If no wrap is needed
    else:

        textWrapped.append(line)



# Formatting tables for PDF
textTablesDone = []

subjectsStartLine = textWrapped.index(subjectsLine)

if doThemesTable:
    
    themesStartLine = textWrapped.index(themesLine)

else:

    themesStartLine = subjectsStartLine


corrections = 0


# Looping through all lines to see if there are any strange cross-page formatting issues, and then correcting them
# Corrections count is to correct spacing later on
for index in range(len(textWrapped)):

    if index % pageLength == (pageLength - 1) and "┼" in textWrapped[index] and index > themesStartLine:

        threeReplaced = textWrapped[index].replace("┼", "┴").replace("├", "└").replace("┤", "┘")

        textTablesDone.append(threeReplaced)

    elif index % pageLength == 0 and "┼" in textWrapped[index - 1] and index > themesStartLine:

        threeReplaced = textWrapped[index - 1].replace("┼", "┬").replace("├", "┌").replace("┤", "┐")

        textTablesDone.append(threeReplaced)
        textTablesDone.append(textWrapped[index])

        if index < subjectsStartLine:
            
            corrections += 1

    elif index % pageLength == (pageLength - 2) and "┼" in textWrapped[index] and index > themesStartLine:

        threeReplaced = textWrapped[index].replace("┼", "┴").replace("├", "└").replace("┤", "┘")

        textTablesDone.append(threeReplaced)
        

        # Only themes table needs the extra blank line
        if index < subjectsStartLine:

            textTablesDone.append("")

            corrections += 1
        

    elif index % pageLength == (pageLength - 1) and "┼" in textWrapped[index - 1] and index > themesStartLine:

        threeReplaced = textWrapped[index - 1].replace("┼", "┬").replace("├", "┌").replace("┤", "┐")

        textTablesDone.append(threeReplaced)
        textTablesDone.append(textWrapped[index])

        if index < subjectsStartLine:

            corrections += 1
        

    else:

        textTablesDone.append(textWrapped[index])



# Now to remove any extra spaces which are no longer needed
# These are redundant now that the table has been effectively extended
textTablesReallyDone = []


# Finding the start of the subjects table
subjectsStartLine = textTablesDone.index(subjectsLine)


# Finding the bottom of the themes table
for x in range(len(textTablesDone)):

    line = textTablesDone[x]

    if "╘" in line:

        bottomThemesTableLine = textTablesDone.index(line)
        
        break



# Removing any of the excess lines
for y in range(len(textTablesDone)):

    if y < bottomThemesTableLine or y >= subjectsStartLine:

        textTablesReallyDone.append(textTablesDone[y])

    elif y > bottomThemesTableLine or y < subjectsStartLine:

        if textTablesDone[y] != "":

            textTablesReallyDone.append(textTablesDone[y])
        
        elif textTablesDone[y] == "":

            if corrections != 0:

                corrections -= 1

                continue
            
            else:

                textTablesReallyDone.append(textTablesDone[y])



# Correcting any cross-page topics/flags and moving all new sections/subjects/themes onto a new page
finalText = []

runningIndex = 0
finalIndex = len(textTablesReallyDone)


# While loop to only terminate once all lines have been fixed
while runningIndex < finalIndex:

    listToSort = []


    # Determining the list that needs fixing
    if runningIndex == 0:

        for line in textTablesReallyDone:

            listToSort.append(line)
        
    else:

        for line in finalText:

            listToSort.append(line)


    finalText = []


    # Finding the key lines
    subjectsStartLine = listToSort.index(subjectsLine)
    topicsStartLine = listToSort.index(topicsLine)

    if doGlossary == True:

        glossaryStartLine = listToSort.index(glossaryLine)



    # Looping over all the lines
    for x in range(len(listToSort)):

        line = listToSort[x]

        nextBulletIndex = None



        # If we don't currently have a topic or subject in the glossary
        if "•" not in line:



            # Fixing the cross-page formatting of the glossary
            if ("▪" in line or "◆" in line) and x > topicsStartLine:

                currentBulletIndex = listToSort.index(line)

                currentBulletModulo = currentBulletIndex % pageLength



                # Finding the next bullet point
                for part in listToSort[currentBulletIndex+1:]:

                    if "▪" in part or "◆" in part:

                        nextBulletIndex = listToSort.index(part)

                        break
                


                # Sorting out the last bullet point
                if nextBulletIndex == None:

                    finalText.append(line)

                    if x >= runningIndex:

                        runningIndex += 1

                    continue
                

                nextBulletModulo = nextBulletIndex % pageLength

                entryWidth = nextBulletIndex - currentBulletIndex - 1



                # Check if next bullet is on same page as current bullet or at very top of next page
                if (nextBulletModulo > currentBulletModulo):

                    finalText.append(line)

                    if x >= runningIndex:

                        runningIndex += 1

                    continue



                # This implies the next bullet is on the next page
                else:


                    # Forcing a lack of push
                    if entryWidth == 1 and currentBulletModulo == (pageLength - 1) and listToSort[x+1] == "":

                        finalText.append(line)

                        for rem in listToSort[currentBulletIndex + 2:]:

                            finalText.append(rem)

                        finalIndex = len(finalText)

                        break


                    else:

                        push = pageLength - currentBulletModulo



                        # Only correcting the bullet point position if not at top of next page
                        if nextBulletModulo != 0:

                            dividerCount = 0



                            # Finding the number of dividers between current bullet point and the next one
                            for part in listToSort[currentBulletIndex:nextBulletIndex+1]:

                                if "" in part:

                                    dividerCount += 1

                                    break



                            # Pushing the current bullet onto the next page if it won't fit on the current one
                            if dividerCount > 0:

                                for x in range(push):

                                    finalText.append("")


                                finalText.append(line)


                                for rem in listToSort[currentBulletIndex + 1:]:

                                    finalText.append(rem)

                                finalIndex = len(finalText)

                                break



                            # Appending the current line if it can fit on the current age
                            elif dividerCount == 0:

                                finalText.append(line)

                                if x >= runningIndex:

                                    runningIndex += 1

                                continue


                        # If no push is needed
                        else:

                            finalText.append(line)

                            if x >= runningIndex:

                                runningIndex += 1

                            continue



            # If not in glossary list
            else:



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
                elif "┣" in line and x % pageLength != 0 and x >= topicsStartLine:

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
                elif x > topicsStartLine and x % pageLength != 0 and x != (len(listToSort) - 1) and singleSep in listToSort[x+1] and (doubleSep not in listToSort[x-2]) and (("•" in listToSort[x+3]) or ("No PDF files found in this subfolder!" in listToSort[x+3])):

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
        elif "•" in line:

            currentBulletIndex = listToSort.index(line)

            currentBulletModulo = currentBulletIndex % pageLength



            # Finding the next bullet point
            for part in listToSort[currentBulletIndex+1:]:

                if "•" in part:

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



# Finding when topics line starts
topicsStartLine = finalText.index(topicsLine)

pageNums = []



# Looping over themes
for theme in themes:



    # If we have a subject-like theme
    if not isinstance(theme, list):


        # Looping over lines to find subject headers and thus calculate their page numbers
        for x in range(len(finalText)):


            # Only want to search topics list, so ignoring the glossary
            if doGlossary == True:

                if x < glossaryStartLine and x > topicsStartLine:

                    line = finalText[x]

                    if f" — {theme} —" in line:
                        
                        pageNum = (x // pageLength) + 2

                        pageNums.append([theme, pageNum])

                        break
            


            # Searching everywhere after topics list starts if no glossary
            else:

                if x > topicsStartLine:

                    line = finalText[x]

                    if f" — {theme} —" in line:

                        pageNum = (x // pageLength) + 2

                        pageNums.append([theme, pageNum])

                        break

    

    # If we do not have a subject-like theme
    elif isinstance(theme, list):


        # Looping over subjects
        for subject in theme[1]:


            # Looping over lines to find subject headers and thus calculate their page numbers
            for x in range(len(finalText)):


                # Only want to search topics list, so ignoring the glossary
                if doGlossary == True:

                    if x < glossaryStartLine and x > topicsStartLine:

                        line = finalText[x]
                        
                        if f"  {subject} " in line and singleSep in finalText[x+1]:

                            pageNum = (x // pageLength) + 2

                            pageNums.append([subject, pageNum])

                            break
                

                # Searching everywhere after topics list starts if no glossary
                else:

                    if x > topicsStartLine:

                        line = finalText[x]

                        if f"  {subject} " in line and singleSep in finalText[x+1]:

                            pageNum = (x // pageLength) + 2

                            pageNums.append([subject, pageNum])

                            break



# Finding the glossary          
if doGlossary == True:

    for x in range(len(finalText)):

        line = finalText[x]

        if line == glossaryLine:

            pageNum = (x // pageLength) + 2

            pageNums.append(["Glossary", pageNum])

            break



# Finding themes line
for x in range(len(finalText)):

    line = finalText[x]

    if line == themesLine:

        pageNum = (x // pageLength) + 2

        pageNums.append(["Themes", pageNum])

        break



# Finding subjects line
for x in range(len(finalText)):

    line = finalText[x]

    if line == subjectsLine:

        pageNum = (x // pageLength) + 2

        pageNums.append(["Subjects", pageNum])

        break



# Finding the key lines
if doThemesTable == True:

    themesStartLine = finalText.index(themesLine)

else:

    themesLine = subjectsLine
    themesStartLine = finalText.index(themesLine)

contentsStartLine = finalText.index(contentsLine)



# Adding page numbers back into the contents
for x in range(len(finalText)):

    line = finalText[x]


    # Only checking lines where entries need to be placed
    if "$" in line:



        # Finding position of subject name
        for char in line:

            if char != " " and char != "▪" and char != "—":

                subjectNameStart = line.index(char)

                break
        

        for char in line:

            if char == "—":

                continue


            if char == "$":

                subjectNameEnd = line.index(char) - 2

                break
        

        
        # Getting subject name
        subjectName = line[subjectNameStart:subjectNameEnd + 1]



        # Swapping out $ signs for the dots and the page numbers, and then aligning everything correctly too
        for subject in pageNums:

            if subjectName == subject[0]:

                
                # Subject-like theme
                if subjectName in themes:

                    numDots = (pageWidth - gapWidth) - 4 - gapWidth - len(subjectName) - len(str(subject[1]))

                    finalText[x] = " " * gapWidth + "— " + subjectName + " " + "." * numDots + " " + str(subject[1])
                

                # Glossary, themes table or subjects table
                elif subjectName == "Glossary" or subjectName == "Themes" or subjectName == "Subjects":

                    numDots = (pageWidth - gapWidth) - 2 - gapWidth - len(subjectName) - len(str(subject[1]))

                    finalText[x] = " " * gapWidth + subjectName + " " + "." * numDots + " " + str(subject[1])                    


                # Subjects
                else:

                    numDots = (pageWidth - gapWidth) - 2 - gapWidth - 2 - len(subjectName) - len(str(subject[1]))

                    finalText[x] = " " * gapWidth + "▪ " + subjectName + " " + "." * numDots + " " + str(subject[1])



    # Stopping when neccessary
    elif line == themesLine:

        break

    else:

        continue


print("──▶ Data formatted!\n")



# Warning the user if there is a mismatch between the glossary the subdirectories count
if doGlossary:

    if (totalsData[1] + subjectLikeThemeCount) > int(lengthGloss):

        print("──▶ Warning! Not all subjects have an entry in the glossary!\n")

    elif (totalsData[1] + subjectLikeThemeCount) < int(lengthGloss):

        print("──▶ Warning! Not all entries in the glossary have a directory!\n")




'''
WRITING TO PDF
'''


print("──▶ Writing to PDF...")



# Setting up the PDF
pdf = FPDF(orientation = "P", format = "A4")
pdf.add_page()
pdf.add_font(f"{fontFile[:-4]}", "", fontFileDir + fontFile, uni=True)
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
pdf.set_font(f"{fontFile[:-4]}", size = 10)

for i in range(14):

    pdf.cell(0, 4, txt="", ln=1)



# Writing title
pdf.set_font(f"{fontFile[:-4]}", size = 32)
titleLength = len(f"{archive_name} Report")
titleLine = int(np.ceil((27 - titleLength)/2)) * " " + f"{archive_name} Report"
pdf.cell(0, 4, txt=titleLine, ln=1)

pdf.set_font(f"{fontFile[:-4]}", size = 10)

for i in range(6):

    pdf.cell(0, 4, txt="", ln=1)



# Writing date and time
pdf.set_font(f"{fontFile[:-4]}", size = 18)
datetimeLength = len(timeNow + "  ❦  " + formattedDate)
dateLine = int(np.ceil((49 - datetimeLength)/2)) * " " + timeNow + "  ❦  " + formattedDate
pdf.cell(0, 4, txt=dateLine, ln=1)

pdf.set_font(f"{fontFile[:-4]}", size = 10)

for i in range(3):

    pdf.cell(0, 4, txt="", ln=1)



# Writing summary box
themesNum = str(totalsData[0])

if doThemesTable:

    subsNum = str(totalsData[1])

else:

    subsNum = str(totalsData[0])


topsNum = str(totalsData[2])
filesNum = str(totalsData[3])
pagesNum = str(totalsData[4])
sizeNum = humanize.naturalsize(totalsData[5], binary=False, format="%.2f")


# Getting lengths of numbers, and then the maximum
numLineLengths = [len(themesNum), len(subsNum), len(topsNum), len(filesNum), len(pagesNum), len(sizeNum)]

longestNum = max(numLineLengths)


# Determining box & centring parameters
boxWidth = longestNum + len("Subjects: ") + 7

leftWidth = int(np.ceil(boxWidth / 2))

rightWidth = int(np.floor(boxWidth / 2))

extraBitAll = int(np.ceil((63 - (boxWidth + 2)) / 2))



# Setting the lines depending on whether we have a themes table or not
if doThemesTable == True:

    summaryBoxLines = [["Themes: ", themesNum], ["Subjects: ", subsNum], ["Topics: ", topsNum], ["Files: ", filesNum], ["Pages: ", pagesNum], ["Size: ", sizeNum]]

else:

    summaryBoxLines = [["Subjects: ", subsNum], ["Topics: ", topsNum], ["Files: ", filesNum], ["Pages: ", pagesNum], ["Size: ", sizeNum]]



# Writing the box top
pdf.set_font(f"{fontFile[:-4]}", size = 14)

pdf.cell(0, 4, txt=(" " * extraBitAll + "╭" + "─" * boxWidth + "╮"), ln=1)
pdf.cell(0, 4, txt=(" " * extraBitAll + "│" + " " * boxWidth + "│"), ln=1)



# Writing the main box lines
for line in summaryBoxLines:

    leftBit = leftWidth - len(line[0])
    rightBit = rightWidth - len(line[1])

    pdf.cell(0, 4, txt=(" " * extraBitAll + "│" + " " * leftBit + line[0] + line[1] + " " * rightBit + "│"), ln=1)

    pdf.cell(0, 4, txt=(" " * extraBitAll + "│" + " " * boxWidth + "│"), ln=1)



# Writing the box bottom
pdf.cell(0, 4, txt=(" " * extraBitAll + "╰" + "─" * boxWidth + "╯"), ln=1)

pdf.set_font(f"{fontFile[:-4]}", size= 10)



# Final push lines before version number
if doThemesTable == True:

    for i in range(26):

        pdf.cell(0, 4, txt="", ln=1)

else:

    for i in range(28):

        pdf.cell(0, 4, txt="", ln=1)



# Writing version number
pdf.set_font(f"{fontFile[:-4]}", size = 18)
versionLength = len(version)
versionLine = int(np.ceil((49 - versionLength)/2)) * " " + version
pdf.cell(0, 4, txt=versionLine, ln=1)

pdf.set_font(f"{fontFile[:-4]}", size = 10)

for i in range(2):

    pdf.cell(0, 4, txt="", ln=1)



# Writing remainder of the lines
pdf.set_font(f"{fontFile[:-4]}", size = 10)

for x in range(len(finalText)):

    pdf.cell(0, 4, txt=finalText[x], ln=1)

pdf.output(f"{archDir + os.sep + archive_name} Report.pdf")

print("──▶ PDF written!\n")



# Deleting temporary .pkl files
try:

    os.remove(fontFileDir + f"{fontFile[:-4]}.cw127.pkl")

except FileNotFoundError:

    pass


os.remove(fontFileDir + f"{fontFile[:-4]}.pkl")



# End of program message
endTime = time.time()
runningTime = round(endTime - startTime, 2)

print(f"──▶ Finished in {runningTime}s!\n")

print(singleSep * (len(f"{singleSep * numSep} {startLine} {singleSep * numSep}") + 2) + "\n\n")
