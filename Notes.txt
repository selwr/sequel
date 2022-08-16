## Notes


# General
* The program will search through all subfolders of the folder in which the .py file is placed and ran from
* The files to search for must be PDFs
* The formatting currently allows up to 40 subjects. This can be reduced to give the desired formatting by removing some of the ‘text.append(“”)’ line breaks towards the beginning of the append statements, or by reducing the argument in the for loop which appends these breaks en masse.

# Fonts
* Must be a monospaced Unicode (UTF-8 encoded) font (eg. Menlo, as included)
* The .ttf file must be somewhere on the hard drive, but not in /Library or (explicitly) /'Mobile Documents'
* The code will generate two .pkl files in the directory of the file's .ttf; the exact names of these files need to be put in the code (towards the end) so that they are deleted once the program has been executed

# Protected characters
* No ~ or > can appear in a file name
* Square brackets can only be used to show multiplicity of a topic at the end of a file name, eg. [n]
* Round brackets can only be used for 'flags' at the end of the file, before the multiplicity
* There must only be one set of square or round brackets per filename