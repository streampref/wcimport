**Table of Contents**

- [Introduction](#introduction)
- [Generators](#generators)
- [Command Line](#command-line)

# Introduction

WCImport is a tool for importation of data of 2014 Soccer World Cup and prepare this data for experiments with StreamPref DSMS.

# Data Importing

The first step is to run the tool **wcimport.py** to download and convert the data.
Next, you can use the appropriated generator to create the environment for experiments.

# Generators

WCImport has individual dataset generators for evaluation of specific StreamPref operators.

- **SEQGen**: generator for evaluation of SEQ operator (sequence extraction);
- **CONSEQGen**: generator for evaluation of CONSEQ operator (subsequences with consecutive timestamp);
- **ENDSEQGen**: generator for evaluation of ENDSEQ operator (subsequences with end position);
- **MINSEQGen**: generator for evaluation of MINSEQ operator (filtering sequences by minimum length);
- **MAXSEQGen**: generator for evaluation of MAXSEQ operator (filtering sequences by maximum length);
- **BESTSEQGen**: generator for evaluation of BESTSEQ operator (dominant sequences according to temporal conditional preferences);
- **CompGen**: Generator for evaluation of the number of comparisons unsing different combinations of operators. 

# Command Line

All generators share the same command line options:
- -h/--help: Show the help message
- -g/--gen: Generate files
- -o/--output: Configure files to generate query results
- -r/--run: Run experiments
- -s/--summarize: Summarize experiments results
