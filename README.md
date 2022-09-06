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
A glossary can optionally be included in the report as well! Its plaintext file should be formatted as follows:

> \## Glossary\
> --- *blank line* ---\
> --- *blank line* ---\
> \* Subject1 - field1, field2, field3, ...\
> --- *blank line* ---\
> \* Subject2 - field1, field2, field3, ...\
> --- *blank line* ---\
> \* Subject3 - field1, field2, field3, ...\
> ...\
> etc.

The glossary file must end with a blank line to prevent any fields from being cut off.

As with the font file, provided the glossary file is named 'archive_glossary.txt' and is _somewhere_ on the hard drive, it will be found.


## Directory structure
The root of the archive should contain folders in which the PDF files reside. This highest-level of folder within the archive is denoted a 'theme', and can itself contain subfolders, which are denoted 'subjects'. No further recursive folders can be analysed.

Under normal circumstances, the PDF files will be placed in the subject folders. However, theme folders can be 'subject-like', containing no subfolders and instead PDF files themselves. This is fine, and will be properly analysed - even if all 'theme' folders are subject-like. However, if a theme is subject-like, it must not contain any subfolders.


### Limits to the analysis
Due to the formatting and nature of the report, if all themes are subject-like, then a maximum of 30 'themes' can be analysed - and these will be referred to as subjects in the report. However, if not **all** of the themes are subject-like, then the number depends on how many themes there are and how many are/aren't subject-like using the formula below:

> maxNumSubjects = p - (2r + s + 9)

where
* p is the number of lines per page (under the default settings - a paper size of A4 and a font size of 10 - this is 69)
* r is the remaining number of themes
* s is the number of themes that are subject-like
* 9 is the number of 'other' lines on the page.

These limits are only imposed to ensure the 'main table' and the totals table (and, separately, the contents page) of the report remain on the same page for clarity. A warning will be printed to the console if the number of subjects in an archive exceeds the maximum.

If the limit is exceeded, and all 'themes' are subject-like, proper theming is recommended. If the limit is exceeded and not all of the themes are subject-like, unfortunately there is no way around a strange-looking result!

The paper and font sizes can be changed towards the end of the code, and then the pageWidth and pageLength numbers can be corrected to match the new parameters, but this is a manual task to be performed if needed. Note though that the title page is written independently of the rest of the lines, so the value for pageWidth and pageLength do not apply to it and will need to be worked out independently for the title page to look correct after paper and/or font size adjustment!


## Files in the archive
Only PDF files will be analysed and their filenames must be formatted in the following way:
> "{topic} (flags) [multiplicity].pdf"

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
* a totals table
* a topic list with topic multiplicities, any flags as sub-lists, and any flags' multiplicities too
* a glossary (if one is found).

The date and time of generation is given on the title page for future reference.

The page numbers given in the contents refer to the absolute page number of the report, ***including all pages***.


## Future
A GUI-based version of Archysis is in the works.