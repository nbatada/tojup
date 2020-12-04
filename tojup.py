#!/usr/bin/env python3
# coding: utf-8
# 
# Please get in touch to report bugs or have a feature request
# Nizar Batada (firstname dot lastname @ gmail )
#

##%%
'''
This program will convert a script file into a jupyter notebook. 

Usage: ./convert_script_to_jupyter.py -f myprog.sh -l bash > myprog.ipynb

https://nbformat.readthedocs.io/en/latest/#:~:text=Jupyter%20(n%C3%A9%20IPython)%20notebook%20files,is%20stored%20in%20a%20cell.
'''

##%%
import sys
import argparse
import json

##%%
def cleanupMarkdownString(cell_txt):
    '''
    Helper function for *formatOneCell()*
    '''
    L=cell_txt.split('\\n') 
    L_stripped=[]
    for idx,s in enumerate(L):
        s_=s.lstrip('#') 
        if s_.startswith('!'): 
            s_=s_.lstrip('!') #!/usr/bin 
        if s_.strip()!='':
            L_stripped.append(s_)
    return(L_stripped)

##%%
def formatOneCell(cell_txt, count, language="python", cell_type="code"): 
    '''
    Helper function that is not meant to be called directly but instead by 
    *printJupyterFormat()* function

    Will format a string {cell_txt} into either a "code" or a "markdown" 
    jupyter notebook format so that it is seen as a single cell.

    Note:
    1) If the {cell_txt} starts with a "#" it would be considered to be a *markdown* cell.
    In this case, all the "#" prefixes in each string (after splitting on a new line) 
    will be removed (i.e. even if it is in markup)
   
    2) If stripped string is empty, it will not be printed

    3) If the {cell_txt} does not start with a "#", it is considered to be a *code* cell.
    
    4) A {cell_str} classified as *code* will be printed with a "%%bash" prefix if the {language}
    is defined as *bash* (bash,tsh,zsh or sh)


    '''
    if cell_txt.startswith('"') and cell_txt.endswith('"'): # input is json.dump formatted
        cell_txt=cell_txt[1:-1]


    CELL_TYPE="code"
    if cell_txt.startswith('#'):
        CELL_TYPE="markdown"
        L_stripped=cleanupMarkdownString(cell_txt)
        if len(L_stripped)==0: return(None)
        cell_txt='\\n'.join(L_stripped)


    out=['{']
    if CELL_TYPE=="markdown": 
        out.append('"cell_type": "%s",' % "markdown")
    else:
        out.append('"cell_type": "%s",' % "code")
        if language.lower()=="bash":
            cell_txt="%%%%bash\\n%s" % cell_txt
        out.append('"execution_count": %s,' % count)
        out.append('"outputs": [],')

    out.append('"metadata": {},')
    out.append('"source": ["%s"]' % cell_txt)
    out.append('}')

    return('\t\t\n'.join(out))

##%%
def convertToJupyterFormat(L, language):
    '''
    Given a list of strings, convert it to jupyter notebook format (ipynb)
    
    '''
    out=[]
    out.append('{')
    out.append(' "cells" : [')
    cells=[]
    for count,line in enumerate(L):
        if line.strip('# ')=="": continue # remove empty lines? This will messup the formating
        cell_type="code"
        #if line.startswith('#'):  cell_type="markdown"
        one_cell_formatted=formatOneCell(json.dumps(line),count+1, language, cell_type)
        if one_cell_formatted:
            cells.append( one_cell_formatted ) # json.dumps to escape quotes
    out.append(',\n'.join(cells))
    out.append(" ],")
    
    out.append(' "metadata": {')
    out.append('   \t"kernelspec": {')
    out.append('   \t"display_name": "%s",' % "python") #language)
    out.append('   \t"language": "%s",' % "python") #language)
    out.append('   \t"name": "%s"' % "python") #language)
    out.append('   \t}')
    out.append('  },')
    out.append(' "nbformat": 4,')
    out.append(' "nbformat_minor": 2')
    out.append('}')
    
    print('\n'.join(out))

##%%
def getCodeBlocks(fp, sep="\n"):
    code=[x.strip('\n\r') for x in fp.read().split(sep)]
    return(code)
##%%
if __name__ == '__main__':
    parser=argparse.ArgumentParser(description='''
This program will convert a script into a jupyter notebook. 
If the line starts with a "#", then that line will be considered to be a markdown cell.
Specify language as bash, if you like the cell to start with "%%bash".
Specify code blocks via *sep* argument. 
    ''')
    parser.add_argument('-f','--file',default='-',action='store',required=True,help='File name to read from. You can specify "-" to pipe the script file.')
    parser.add_argument('-l','--language',default='python',action='store',required=False,help='programming language of the input script. [Default: python] options:{python, bash}. If you specify *bash*, a prefix %%bash will be added to the cell block.')
    parser.add_argument('-s','--sep',default='\n', action='store',required=False,help='chunk seperator [Default: \n]. "\n": each line will be converted into a individual cell block]')
    args=parser.parse_args()
    if args.file=='-':
        fp=sys.stdin
    else:
        fp=open(args.file)
    
    code = getCodeBlocks(fp, sep=args.sep)

    convertToJupyterFormat(code, language=args.language.lower())





