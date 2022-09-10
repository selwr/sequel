# Archysis v3

Archysis is an archive analysis tool which will read a directory's PDF files and produce a report, detailing all themes, subjects, topics, flags and multiplicities. A contents page is automatically generated, and an optional glossary can be included too!

Archysis v1 and v2 can be found in selwr/poirot, but these are very much out of date with many oversights and problems, hence the v3 re-write.



## Report structure
The report will contain:
* a title page
* a contents page
* a themes table
* a subjects table
* a topic list (with any flags & multiplicities)
* a glossary

A summary of the archive as well as the date & time of generation are given on the title page.

The title of the report, and its filename, will be "{archive_name} Report", where archive_name is the name of the root of the archive.

The page numbers given in the contents refer to the absolute page numbers of the report document.

The highest value of a particular metric in each column is surrounded by curly braces to illustrate its size.

The report is automatically formatted to ensure a high level of readability.



## Pre-requisites
The program runs on Python 3, but uses f-strings which were introduced in v3.6, so this is the minimum requirement. However, the latest version of Python 3 is always recommended.

A number of external libraries are used, so these should be installed:
* numpy
* textwrap
* humanize
* PyPDF2
* fpdf
* tabulate

Once the Archysis.py file is placed in the root of the archive, it need only be run to generate the report.


### Files in the archive
Only PDF files will be analysed and their filenames should be formatted in the following way:

> {topic} (flags) [multiplicity].pdf

Topics are what the files are about. They needn't be written within curly braces - the above is just to illustrate their positioning within the filename. There should only be one topic per file, but hyphens can be included in the filename to give further clarity to the topic.

Flags are separate, optional 'classifiers' that allow differentiation between files on the same topic. They should all be in one set of round brackets and in the position shown above. Two flags should be separated using ' and ', and three or more flags can be separated using commas too.

The multiplicity in the square brackets should count from 1 up to however many files there are on that specific topic. However, if there is only one file on that topic, [1] is not required at the end of the filename. The multiplicity should be the final part of the filename before the extension.

The spaces shown in the filename above (between the end of the topic & the opening flag bracket, and between the closing flag bracket & the opening multiplicity bracket) must be in place.

Round and/or square brackets should not appear anywhere else in the filename, other than the positions shown above.


### Directory structure
The root of the archive should contain folders in which the PDF files reside. This highest-level of folder within the archive is denoted a 'theme', and can itself contain subfolders, which are denoted 'subjects'. No further recursive folders can be analysed.

Under normal circumstances, PDF files should be placed in the subject folders. However, theme folders can be 'subject-like', containing no subfolders, and instead containing PDF files. This is fine, and will be properly analysed even if all 'theme' folders are subject-like. However, if a theme is subject-like, it shouldn't contain any subfolders.

If all 'themes' are subject-like, then no themes table will be written in the report.


### Fonts
Due to the formatting of the report's tables, a monospaced UTF-8 Unicode font must be used. The default font (Menlo) is included within this repo. Once the repo has been downloaded, provided that the 'archysis_font.ttf' file is _somewhere_ on the hard drive, it will be found.

Other fonts can be used, provided that they conform to the above requirements and their file is renamed to be 'archysis_font.ttf'.

The code will generate two .pkl files during its execution, but these will be automatically deleted.

### Glossary
A glossary can be included in the report, and will be automatically alphabetised by subject. Each entry in its plaintext file, on a new line, should be formatted as follows:

> \* SubjectName - Field1, Field2, Field3, ...

The glossary file must end with a blank line to prevent any fields from being cut off.

As with the font file, provided the glossary file is named '{archive_name}\_glossary.txt', where archive_name is the name of the root of the archive, and is _somewhere_ on the hard drive, it will be found. If no glossary is found, then one will not be written to the report.



## Future
A GUI-based version of Archysis (called P.A.G.E.) is in the works.