# Archysis v3

## Introduction
Archysis is an archive analysis tool which will read in a directory's PDF files and produce a report, detailing all unique themes, subjects, topics, flags and multiplicities. A contents page is automatically generated, and an optional glossary can be included as well.

The report is automatically formatted to ensure a high level of readability.

Archysis v1 and v2 can be found in selwr/poirot, but these are very much out of date with many oversights and problems, hence the v3 re-write.

## Pre-requisites
The program runs on Python 3, but uses f-strings which were introduced in v3.6, so this is the minimum requirement.

A number of dependent libraries are also used, so these should be installed too:
* numpy
* textwrap
* humanize
* PyPDF2
* fpdf
* tabulate

Once the Archysis.py is placed in the root of the archive, it need only be run to generate the report.

### Fonts
Due to the formatting of the report's tables, a monospaced UTF-8 Unicode font must be used and one is included within this repo, Menlo. Once the repo has been downloaded, provided that the 'archysis_font.ttf' file is _somewhere_ on the hard drive, it will be found.

Other fonts can be used, provided that they conform to the above requirements and are renamed to be 'archysis_font.ttf'.

The code will generate two temporary .pkl files during its execution, but these will be automatically deleted.

### Glossary
A glossary can optionally be included in the report as well! Its plaintext file should be formatted as follows:

> \## Glossary\
> --- *blank line* ---\
> --- *blank line* ---\
> \* Subject 1 - field 1, field 2, field3\
> --- *blank line* ---\
> \* Subject 2 - field 1, field 2, field 3\
> ...\
> etc.

As with the font file, provided the glossary file is named 'archive_glossary.txt' and is somewhere on the hard drive, it will be found.


## Directory structure
The root of the archive should contain folders in which the PDF files reside. This highest-level of folder is denoted a 'theme', and can itself contain subfolders, which are denoted 'subjects'. No further recursive folders can be analysed.

Under normal circumstances, the PDF files will be placed in the subject folders, which are in the theme folders. However, theme folders can be 'subject-like', containing no subfolders but instead containing PDF files themselves. This is fine, and will be properly analysed - even if all 'theme' folders are subject-like.

However, if a theme _is_ subject-like, it cannot contain any subfolders.


### Limits to the analysis
Due to the formatting and nature of the report, if all themes are subject-like, then a maximum of 30 'themes' can be analysed. However, if not **all** themes are subject-like, then the number depends on how many themes _are_ subject-like and how many _aren't_ subject-like, using the below formula:

> maxNumSubjects = 69 - 9 - (2 x numRegThemes) - (numSubLikeThemes)

where
* 69 is the number of lines per page under the default settings (a paper size of A4 and a font size of 10)
* 9 is the number of 'other' lines on the page
* numSubLikeThemes is the number of themes that are subject-like
* numRegThemes is the remaining number of themes.

These limits are only imposed to ensure the 'main table' and the totals table (and, independently, the contents page) of the report remain on the same page for clarity. A warning will be printed to the console if the number of subjects in an archive exceeds the maximum.

If the limit is exceeded, and all 'themes' are subject-like, proper theming is recommended. If the limit is exceeded and not all of the themes are subject-like, unfortunately there is no way around a strange-looking result!


## Files in the archive
Only PDF files will be analysed and must be formatted in the following way:
> "{topic} (flags) [multiplicity].pdf"

The topic is essentially what the file is about. It shouldn't be written within curly brackets - the above is just to illustrate its positioning within the filename.

The optional flags are separate 'classifiers' that allow differentiation between files on the same topic. They should all be in one set of round brackets and in the position shown above. Two flags should be separated by ' and ', but three flags can be separated using commas _as well_.

The multiplicity in the square brackets should count from 1 up to however many files there are on that specific topic - however, if there is only one file on that topic, [1] is not required at the end of the filename. The multiplicity should be the final part of the filename before the extension.

Round and/or square brackets should not appear anywhere else in the filename, other than the positions shown above.


## Report structure
The report will contain a title page, a contents page, a themes table (if not all themes are subject-like), a subjects table, a totals table, a topic list (with multiplicities, the flags as sub-lists, and the flags' multiplicities too), and a glossary (if one is found).

The date and time of generation is given on the title page.

The page numbers given in the glossary refer to the absolute page number of the report, **including the title page and all table-containing pages**.


## Future
A GUI-based version of Archysis is in the works.