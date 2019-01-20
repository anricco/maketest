



# import os
# import sys
import fileinput
# import shutil

# import copy

# to add command line options
# import argparse

# to use random.sample()
# import random

# from pdfrw import PdfReader, PdfWriter



# csvFileToMatrix opens a .csv file with tab as separator and converts it in a matrix list
def csvFileToMatrix(csvFileName, csvFilePath):
    outputMatrix = []

    for line in fileinput.input( csvFilePath + "/" + csvFileName ):
        outputMatrixLine = []
        for k in range(0,line.count("\t")+1):
            outputMatrixLine.append(line.split("\t")[k].rstrip())  # rstrip() removes \n, \r, etc.
        outputMatrix.append(outputMatrixLine)

    return outputMatrix
