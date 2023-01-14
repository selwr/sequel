# Archysis v3

Archysis is an archive analysis tool which will read a directory's PDF filenames & page counts to produce a report, detailing all themes, subjects, topics, flags and multiplicities. A contents page is automatically generated, and an optional glossary can be included too!

Archysis v1 and v2 can be found in selwr/poirot, but these are very much out of date with many oversights and problems, hence the v3 re-write.



## Report structure
The report will contain:
* a title page
* a contents page
* a themes table
* a subjects table
* a topic list (with any flags & multiplicities)
* a glossary

A summary of the archive, as well as the date & time of generation, is given on the title page.

The title of the report, and its filename, will be "archiveName Report", where archiveName is the name of the archive.

The page numbers given in the contents refer to the absolute page numbers of the report document.


### House style continuity
Throughout the report, a house style has been applied to aid the identification of different parts of the report at a glance.

Sections are indicated by bold separators, themes are indicated by double-line separators and subjects are indicated by single-line separators.

In the contents, themes are indicated by '╼ {theme}' and subject-like themes are indicated by '― {theme}' (see ***Directory structure*** subsection)

In headers, themes are indicated by '╼ {theme} ╾' and subject-like themes are indicated by '― {theme} ―'.

In tables, the highest value of a column's metric is enclosed by angle brackets.

The multiplicity of any metric (such as subjects, files and flags) is given in square brackets, and any lone flags are given in round brackets.

In lists, round bullets (•) indicate topics, triangular bullets (‣) indicate flags, square bullets (▪) indicate subjects and rhombus bullets (◆) indicate subject-like themes.



## Pre-requisites
Archysis runs on Python 3, but uses f-strings which were introduced in v3.6, so this is the minimum requirement. The latest version of Python 3 is, however, always recommended.

A number of external libraries are used, so these should be installed _before_ running Archysis:
* numpy
* textwrap
* humanize
* PyPDF2
* fpdf
* tabulate
* colorama


### Compilation into executable
The source code in the repo can be compiled into an executable file by running pyinstaller in the folder containing the Python file,

> pyinstaller --onefile Archysis.py

and then running the file created in the 'dist' subfolder to generate the report.

Note that all dependent libraries above, as well as pyinstaller, must be installed prior to compilation.



## Running Archysis
When run, Archysis will have a short boot-up before asking for the (case-sensitive) directory of the archive. The more information given, the better. It is recommended to give the parent folder and as well as the archive folder (parentDir/archiveDir) to ensure the correct archive is found. For example, if the archive folder is called 'Archive' and this folder is in the Documents folder, then an ideal input to Archysis would be:

> Documents/Archive

and then Archysis will find the folder called 'Archive' in the Documents folder, showing that the full path does not need to be given in this case. However, beware that if there are multiple folders of the same name and/or in the same location, your desired archive may not be found, and so further specification up the directory tree should be given.

NB: Neither the Python file, nor the executable needs to be put in the top-level of the archive in order to run it. These files can be put anywhere on the hard drive. The archive folder will be found from the above input!


### Files in the archive
Only PDF files will be analysed and their filenames should be formatted in the following way:

> {topic} (flags) [multiplicity].pdf

Topics are what the files are about. They needn't be written within curly braces - the above is just to illustrate their positioning within the filename. There should only be one topic per file, but hyphens can be included in the topic to give further clarity to the topic.

Flags are separate, optional 'classifiers' that allow differentiation between files on the same topic. They should all be in one set of round brackets and in the position shown above. Two flags should be separated using ' and '. Three or more flags should also be separated using commas. Use of an ampersand in the round brackets allows the whole flag to be printed onto a single line in the report, rather than being separated onto multiple ones for each of the different components.

The multiplicity in the square brackets should count from 1 up to however many files there are on that specific topic. However, if there is only one file on that topic, [1] is not required at the end of the filename. The multiplicity should be the final part of the filename before the extension.

The spaces shown in the filename above (between the end of the topic & the opening flag bracket, and between the closing flag bracket & the opening multiplicity bracket) must be in place.

Round and/or square brackets should not appear anywhere else in the filename, other than the positions shown above.

No box-drawing characters or bullets points (of any type) are permitted within filenames. Only single quotation marks (') may be used in filenames, not double quotation marks (").

When the files are read, they will be individually checked to see if they can be opened. If any corrupt/encrypted files are found, these will be added to a plaintext file and the program will be terminated so that the list of files can be repaired/decrypted before a full report can be generated.

NB: All files (the archive itself, Archysis (.py and/or executable) and the font & glossary files) must be on the C: drive on a Windows system, or all on the same hard drive on a Unix system.


### Directory structure
The archive should contain folders in which the PDF files reside. This highest-level of folder within the archive is denoted a 'theme', and can itself contain subfolders, which are denoted 'subjects'. No further recursive folders can be analysed.

Under normal circumstances, PDF files should be placed in the subject folders. However, theme folders can be 'subject-like', containing no subfolders, and instead containing PDF files. This is fine, and will be properly analysed even if all 'theme' folders are subject-like. However, if a theme is subject-like, it shouldn't contain any subfolders.

If all 'themes' are subject-like, then no themes table will be written in the report. In this case, the 'theme' folders are referred to as 'subjects' in the report.

Ideally, all theme and subject folder names should be under 50 characters in length.

NB: If not all themes are subject-like, any subject-like themes _will_ appear in the themes table to match their level of directory hierarchy, but _will not_ appear in the subjects table as, in effect, they are **themes** and not **subjects**. Furthermore, the total subjects count will _not_ include subject-like themes. However, given that they have no subdirectories, subject-like themes can (and should!) have glossary entries.


### Fonts
Due to the formatting of the report's tables, a monospaced Unicode TrueType or OpenType font must be used. This should allow for as large a range of glyphs possible, especially box-drawing characters as well as any other letter-like characters, such as letters with accents or Greek characters. To that end, the recommended font is DejaVu Sans Mono, which can be downloaded at https://dejavu-fonts.github.io. Once downloaded, provided that the font file is renamed from 'DejaVuSansMono.ttf' to 'archysis_font.ttf' and is _somewhere_ on the hard drive, it will be found.

Other fonts can be used, provided that they conform to the above requirements, that their filename is 'archysis_font' with a '.ttf' or '.otf' extension and that the file is _somewhere_ on the hard drive. Note that .otf files with Postscript Outlines are not supported.

The code will generate two .pkl files during its execution, but these will be automatically deleted.


### Glossary
A glossary can be included in the report, and will be automatically alphabetised by subject. Each entry in the glossary's plaintext file, on a new line, should be formatted as follows:

> \* SubjectName: Field1, Field2, Field3, ...

The glossary file must end with a blank line to prevent any fields from being cut off.

As with the font file, provided that the glossary file is _somewhere_ on the hard drive, and is named 'archiveName_glossary.txt', it will be found (where archiveName is the **lower case** name of the archive). If no glossary file is found, then one will not be written to the report.



## Future
A GUI-based version of Archysis (called P.A.G.E.) is in the works.