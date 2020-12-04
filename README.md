# tojup
Utility to convert scripts to Jupyter Notebook (ipynb) format


usage: tojup.py [-h] -f FILE [-l LANGUAGE] [-s SEP]

This program will convert a script into a jupyter notebook. If the line starts with a "#", then that line will be
considered to be a markdown cell. Specify language as bash, if you like the cell to start with "%%bash". Specify code
blocks via *sep* argument.

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  File name to read from. You can specify "-" to pipe the script file.
  -l LANGUAGE, --language LANGUAGE
                        programming language of the input script. [Default: python] options:{python, bash}. If you specify
                        *bash*, a prefix %bash will be added to the cell block.
  -s SEP, --sep SEP     chunk seperator [Default: ]. " ": each line will be converted into a individual cell block]





Example
usage: tojup.py -f tojup.py --sep '##%%' > tojup.ipynb

Will convert the file *tojupy.py* in which each code block has been demarcated by "##%%" into ipynb format.

