# Archysis v3

## Introduction
Archysis is an archive analysis tool which will read a directory's PDF files and produce a report, detailing all unique themes, subjects, topics, flags and multiplicities. A contents page is automatically generated, and an optional glossary can be included too!

The report is automatically formatted to ensure a high level of readability.

Archysis v1 and v2 can be found in selwr/poirot, but these are very much out of date with many oversights and problems, hence the v3 re-write.

## Pre-requisites
The program runs on Python 3, but uses f-strings which were introduced in v3.6, so this is the minimum requirement. However, the latest version of Python 3 that is available is always recommended.

A number of dependent libraries are also used, so these should be installed too:
* numpy
* textwrap
* humanize
* PyPDF2
* fpdf
* tabulate

Once the Archysis.py file is placed in the root of the archive, it need only be run to generate the report.

### Fonts
Due to the formatting of the report's tables, a monospaced UTF-8 Unicode font must be used and the default font (Menlo) is included within this repo. Once the repo has been downloaded, provided that the 'archysis_font.ttf' file is _somewhere_ on the hard drive, it will be found.

Other fonts can be used, provided that they conform to the above requirements and are renamed to be 'archysis_font.ttf'.

The code will generate two .pkl files during its execution, but these will be automatically deleted.

### Glossary
A glossary can optionally be included in the report as well! Each entry in the plaintext file should be formatted as follows:

> \* SubjectName - Field1, Field2, Field3, ...

The glossary file must end with a blank line to prevent any fields from being cut off.

The glossary will be automatically alphabetised in the report.

As with the font file, provided the glossary file is named 'archive_glossary.txt' and is _somewhere_ on the hard drive, it will be found.


## Directory structure
The root of the archive should contain folders in which the PDF files reside. This highest-level of folder within the archive is denoted a 'theme', and can itself contain subfolders, which are denoted 'subjects'. No further recursive folders can be analysed.

Under normal circumstances, the PDF files will be placed in the subject folders. However, theme folders can be 'subject-like', containing no subfolders and instead PDF files themselves. This is fine, and will be properly analysed - even if all 'theme' folders are subject-like. However, if a theme is subject-like, it must not contain any subfolders.


## Files in the archive
Only PDF files will be analysed and their filenames must be formatted in the following way:
> {topic} (flags) [multiplicity].pdf

The topic is essentially what the file is about. It needn't be written within curly brackets - the above is just to illustrate its positioning within the filename.

The optional flags are separate 'classifiers' that allow differentiation between files on the same topic. They should all be in one set of round brackets and in the position shown above. Two flags should be separated by ' and ', but three or more flags can be separated using commas too.

The multiplicity in the square brackets should count from 1 up to however many files there are on that specific topic - however, if there is only one file on that topic, [1] is not required at the end of the filename. The multiplicity should be the final part of the filename before the extension.

Round and/or square brackets should not appear anywhere else in the filename, other than the positions shown above.


## Report structure
The report will contain:
* a title page
* a contents page
* a themes table (if not all themes are subject-like)
* a subjects table
* a topic list with topic multiplicities, any flags as sub-lists, and any flags' multiplicities too
* a glossary (if one is found).

The date and time of generation is given on the title page for future reference.

A summary of the report, and thus of the archive itself too, is given on the title page.

The page numbers given in the contents refer to the absolute page number of the report, ***including all pages***.

The highest value of a particular metric in each column is surrounded with curly braces to illustrate its size.


## Future
A GUI-based version of Archysis (called P.A.G.E.) is in the works.