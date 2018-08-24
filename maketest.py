#!/usr/bin/python

#------------------------------------------------------------------------------#
#                                                                              #
#                                                                              #
#                                 MAKETEST                                     #
#                            (Mac OS X version)                                #
#                               Antonio Ricco                                  #
#                                                                              #
#------------------------------------------------------------------------------#


import os
import sys
import fileinput
import shutil

import copy

# to add command line options
import argparse

# to use random.sample()
import random

from pdfrw import PdfReader, PdfWriter


#import logging
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.debug('This is a log message.')


def removeExtension(fileName):
    base=os.path.basename(fileName) # only filename without path
    removedExtensionFile = os.path.splitext(base)[0] # extension =  os.path.splitext(base)[1]
    return removedExtensionFile



# csvFileToMatrix opens a .csv file with tab as separator and converts it in a matrix list
def csvFileToMatrix(csvFileName, csvFilePath):
    outputMatrix = []

    for line in fileinput.input( csvFilePath + "/" + csvFileName ):
        outputMatrixLine = []
        for k in range(0,line.count("\t")+1):
            outputMatrixLine.append(line.split("\t")[k].rstrip())  # rstrip() removes \n, \r, etc.
        outputMatrix.append(outputMatrixLine)

    return outputMatrix



# it takes a matrix list composed by string elements
# and writes on a .csv file exactly as it is with columns separated by \t
# and rows separated by \n
def matrixToCsvFile(inputMatrix, csvFileName, csvFilePath):
    outputCsvFile = open( csvFilePath + "/" + csvFileName, 'w' )

    for j in range(0, len(inputMatrix)):
        for k in range(0, len(inputMatrix[j])-1):
            outputCsvFile.write ( inputMatrix[j][k] + "\t" )
        outputCsvFile.write ( inputMatrix[j][len(inputMatrix[j])-1] + "\n" )

    outputCsvFile.close()


# trasposition of matrices
# https://stackoverflow.com/questions/4937491/matrix-transpose-in-python#9622534
def transposed(lists):
   if not lists: return []
   return map(lambda *row: list(row), *lists)


# it deletes all the auxiliary files after creating the pdf file
# the command to delete the latex file is commented
def latexToPdf(latexFileName, latexFilePath):
    os.chdir(latexFilePath)
    # the LaTeX command is given twice in case LaTeX requires two passes
    os.system("pdflatex -interaction=batchmode " + latexFileName + " > log.log")
    os.system("pdflatex -interaction=batchmode " + latexFileName + " > log.log")
    # the following depends on the particular OS (in this case a Unix OS) - for Windows it has to be changed
    os.system("rm *.log \n rm *.aux")
    # os.system("rm " + latexFileName)
    os.chdir(mainpath)



# it takes a fileName, and a list of replacements,
# and replaces each element in the list with its replacement, producing a string
def replaceTag(fileName, filePath, replacementListMatrix):
    replacedString = ""
    #print len(replacementListMatrix)
    for line in fileinput.input( filePath + "/" + fileName ):
        newline = line

        for i in range(0,len(replacementListMatrix)):
            # print `replacementListMatrix[i][0]`
            newline = newline.replace(replacementListMatrix[i][0], replacementListMatrix[i][1] ) # ('a','b')

        replacedString = replacedString + newline

    return replacedString



# reorders the matrix of questions and adds more informations, namely the order of the answers,
# both in list form [1,2,3,4] and in string form 1234.
# TO BE ADDED: figures, as a number in the original questions
def reorderQuestionListMatrix(vNumber):

    #print `vNumber` + "\n"

    #print `vNumber == 0`

    # global questionListMatrix

    if vNumber == 0:
        order = range(1,questionNumber+1)
    else:
        order = random.sample(xrange(1,questionNumber+1), questionNumber)

    # this is done to avoid affecting the global variable
    #localQuestionListMatrix = [x[:] for x in questionListMatrix] # questionListMatrix.copy()
    localQuestionListMatrix = copy.deepcopy(questionListMatrix)

    #print localQuestionListMatrix

    reorderedQuestionListMatrix = []
    reorderedQuestionListMatrixLine = []


    for j in range(0,questionNumber):
        # questionListMatrixLine is each one of the lines forming reorderedQuestionListMatrix
        reorderedQuestionListMatrixLine = localQuestionListMatrix[order[j]-1]

        # print questionListMatrix[order[j]-1]

        qType = int(reorderedQuestionListMatrixLine[2])

        if vNumber == 0:
            answersOrderList = range(1,qType+1)
        else:
            answersOrderList = random.sample(xrange(1,qType+1), qType)

        reorderedQuestionListMatrixLine.append(answersOrderList)

        answersOrderString = ""
        for k in range(0,qType):
            answersOrderString = answersOrderString + `answersOrderList[k]`
        reorderedQuestionListMatrixLine.append(answersOrderString)

        answersKey = ""
        if not answersOrderList:
            answersKey = 'X'
        elif answersOrderList[0] == 1:
            answersKey = 'A'
        elif answersOrderList[1] == 1:
            answersKey = 'B'
        elif answersOrderList[2] == 1:
            answersKey = 'C'
        elif answersOrderList[3] == 1:
            answersKey = 'D'
        elif answersOrderList[4] == 1:
            answersKey = 'E'

        reorderedQuestionListMatrixLine.append(answersKey)

        # print questionListMatrixLine
        reorderedQuestionListMatrix.append(reorderedQuestionListMatrixLine)

    #print reorderedQuestionListMatrix
    #print "\n"

    return reorderedQuestionListMatrix




# it takes a questionCode, identifying a question, and produces a questionString, a string containing the question.
def makeQuestion(questionCode, questionType, answerOrder, figureNumber, tableNumber):
    if questionType == 0:
        questionType = int(questionCode[6])

    questionString = r'\item' + "\n"
    questionFile = open( mainpath + "/input/" + questionFolderName + "/" + "q" + questionCode + ".tex", 'r' )
    questionString = questionString + questionFile.read() + "\n"   #.decode('latin1')
    questionFile.close()

    if questionType != 0:
        questionString = questionString + "\t"
        questionString = questionString + r'\begin{enumerate}[label=\protect\squared{\Alph*}]'
        questionString = questionString + "\n"
        for k in range(1,questionType+1):
            l = answerOrder[k-1]
            questionString = questionString + "\t\t"
            questionString = questionString + r'\item '
            answerFile = open( mainpath + "/input/" + questionFolderName + "/" + "q" + questionCode + "a" + `l` + ".tex", 'r' )
            questionString = questionString + answerFile.read()
            questionString = questionString + "\n"
        questionString = questionString + "\t"
        questionString = questionString + r'\end{enumerate}'

    if projectType == "BES":
        questionString = questionString + "\n" r'\filbreak' + "\n"

    questionString = questionString +  "\n\n"

    if projectType == "INFO":
        questionString = questionString + r'\emph{' + questionCode + r'}' + "\n\n"

    if not figureNumber == '':
        questionString = questionString.replace('@FIGURA@', `figureNumber` )

    if not tableNumber == '':
        questionString = questionString.replace('@TABELLA@', `tableNumber` )

    return questionString



# it takes a questionCode, identifying the figure connected to a  question, and produces a figureString,
# a string containing the latex code for including the figure
def makeFigure(questionCode, figureNumber):


    if projectType == "BES":
        figureString = r'\noindent\begin{minipage}{\columnwidth}' + "\n"
        figureString = figureString + "\t" + r'\begin{center}' + "\n"
        figureString = figureString + "\t" + r'\includegraphics[width=7cm]{q' + questionCode + r'-fig.pdf}' +  "\n\n"
        figureString = figureString + "\t" + r'Figura ' + `figureNumber` +  "\n"
        figureString = figureString + "\t" + r'\end{center}' + "\n"
        figureString = figureString + r'\end{minipage}' + "\n\n\n" +r'\vspace{1cm}'
    else:
        figureString = r'\noindent\begin{minipage}{\columnwidth}' + "\n"
        figureString = figureString + "\t" + r'\begin{center}' + "\n"
        figureString = figureString + "\t" + r'\includegraphics[width=7cm]{q' + questionCode + r'-fig.pdf}' +  "\n\n"  #[width=4.4cm]
        figureString = figureString + "\t" + r'Figura ' + `figureNumber` +  "\n"
        figureString = figureString + "\t" + r'\end{center}' + "\n"
        figureString = figureString + r'\end{minipage}' + "\n\n\n"

    return figureString


# it takes a questionCode, identifying a question, and produces a questionString, a string containing the question.
def makeTable(questionCode, tableNumber):

    tableFile = open( mainpath + "/input/" + questionFolderName + "/" + "q" + questionCode + "-tab.tex", 'r' )
    tableString = tableFile.read() + "\n"
    tableFile.close()

    tableString = tableString.replace('@TABELLA@', `tableNumber` )

    return tableString



def makeLatexFile(latexOutputFileName, vNumber, transposedReorderedQuestionListMatrix):

    questionNumberList = transposedReorderedQuestionListMatrix[0]
    questionCodeList = transposedReorderedQuestionListMatrix[1]
    questionTypeList = transposedReorderedQuestionListMatrix[2]
    questionVersionNumberList = transposedReorderedQuestionListMatrix[3]
    questionFigureList = transposedReorderedQuestionListMatrix[4]
    questionTableList = transposedReorderedQuestionListMatrix[5]
    questionAnswerOrderList = transposedReorderedQuestionListMatrix[6]
    questionAnswerOrderString = transposedReorderedQuestionListMatrix[7]
    questionKeyList = transposedReorderedQuestionListMatrix[8]

    # qNumber = len(questionCodeList)

    # it creates a dictionary that to each figure associates its number
    # it creates a dictionary that to each table associates its number
    # it creates the strings of questions, figures and tables
    figureNumber = 0
    figureDictionary = {}
    figureDictionary['xxxxxxxxxxxx'] = ''

    tableNumber = 0
    tableDictionary = {}
    tableDictionary['xxxxxxxxxxxx'] = ''

    allQuestionString = ""
    allFigureString = ""
    allTableString = ""
    figureNumber = 0
    tableNumber = 0

    for j in range(0,questionNumber):
        if not questionFigureList[j] == 'xxxxxxxxxxxx' and not questionFigureList[j] in figureDictionary:
            figureNumber = figureNumber + 1
            #print figureNumber
            #print questionFigureList[j]
            figureDictionary[questionFigureList[j]] = figureNumber
            newFigureString = makeFigure(questionFigureList[j], figureNumber)
            allFigureString = allFigureString + newFigureString

        if not questionTableList[j] == 'xxxxxxxxxxxx' and not questionTableList[j] in tableDictionary:
            tableNumber = tableNumber + 1
            #print tableNumber
            #print questionTableList[j]
            tableDictionary[questionTableList[j]] = tableNumber
            newTableString = makeTable(questionTableList[j], tableNumber)
            allTableString = allTableString + newTableString

        newQuestionString = makeQuestion(questionCodeList[j], int(questionTypeList[j]), questionAnswerOrderList[j],
                                         figureDictionary[questionFigureList[j]], tableDictionary[questionTableList[j]] )
        allQuestionString = allQuestionString + newQuestionString    #encode('latin1')
    #print figureDictionary
    #print tableDictionary



    replacementListMatrix = [["@ver@",`vNumber`],["@QUESTIONS@", allQuestionString],
                             ["@FIGURES@", allFigureString],["@TABLES@", allTableString]]
    latexOutputFileString = replaceTag(latexInputFileName, mainpath + "/input/", replacementListMatrix)

    # print latexOutputFileString

    latexOutputFile = open( mainpath + "/output/latex/" + latexOutputFileName, 'w' )
    latexOutputFile.write(latexOutputFileString)    #.decode('latin1')



# it makes the latex and pdf files for the version and adds a line for all relevant files
def makeVersionFiles(vNumber):

    # print questionListMatrix

    reorderedQuestionListMatrix = reorderQuestionListMatrix(vNumber)
    # print reorderedQuestionListMatrix

    transposedReorderedQuestionListMatrix = transposed(reorderedQuestionListMatrix)
    # print transposedReorderedQuestionListMatrix

    questionNumberList, questionCodeList, questionTypeList, questionVersionNumberList, \
        questionFigureList, questionTableList, questionAnswerOrderList, questionAnswerOrderString, \
        questionKeyList = transposedReorderedQuestionListMatrix

    # questionNumberList = transposedReorderedQuestionListMatrix[0]
    # questionCodeList = transposedReorderedQuestionListMatrix[1]
    # questionTypeList = transposedReorderedQuestionListMatrix[2]
    # questionVersionNumberList = transposedReorderedQuestionListMatrix[3]
    # questionFigureList = transposedReorderedQuestionListMatrix[4]
    # questionTableList = transposedReorderedQuestionListMatrix[5]
    # questionAnswerOrderList = transposedReorderedQuestionListMatrix[6]
    # questionAnswerOrderString = transposedReorderedQuestionListMatrix[7]
    # questionKeyList = transposedReorderedQuestionListMatrix[8]


    # for version 0 adds the beginning to all the relevant output files

    if vNumber == 0:
        qNumberFile.write ( "Ordine delle domande \n versione \t" )
        qCodeFile.write ( "Lista delle domande \n versione \t" )
        qAnswerOrderFile.write ( "Ordine delle risposte \n versione \t" )
        qKeyFile.write ( "Lista delle soluzioni \n versione \t" )

        for k in range(0,questionNumber):
            qNumberFile.write ( "q" + `k+1` + "\t" )
            qCodeFile.write ( "q" + `k+1` + "\t" )
            qAnswerOrderFile.write ( "q" + `k+1` + "\t" )
            qKeyFile.write ( "q" + `k+1` + "\t" )

        qNumberFile.write ( "\n" )
        qCodeFile.write ( "\n" )
        qAnswerOrderFile.write ( "\n" )
        qKeyFile.write ( "\n" )


    # Adding a line for this version to all the relevant output files
    qNumberFile.write ( `vNumber` + "\t" )
    qCodeFile.write ( `vNumber` + "\t" )
    qAnswerOrderFile.write ( `vNumber` + "\t" )
    qKeyFile.write ( `vNumber` + "\t" )

    for k in range(0,questionNumber):
        qNumberFile.write ( questionNumberList[k] + "\t" )
        qCodeFile.write ( questionCodeList[k] + "\t" )
        qAnswerOrderFile.write ( questionAnswerOrderString[k] + "\t" )
        qKeyFile.write ( questionKeyList[k] + "\t" )

    qNumberFile.write ( "\n" )
    qCodeFile.write ( "\n" )
    qAnswerOrderFile.write ( "\n" )
    qKeyFile.write ( "\n" )

    latexOutputFileName = projectName + "-" + `vNumber` + ".tex"
    makeLatexFile(latexOutputFileName, vNumber, transposedReorderedQuestionListMatrix)
    latexToPdf(latexOutputFileName, mainpath+"/output/latex")
    # the latex file could be deleted by latexToPdf after creating the pdf file (commented now)
    # os.system("rm " + mainpath +  "/output/latex/" +  projectName + "-" + `vNumber` + ".tex")


    # USES pdfrw
    testWriter.addpages(PdfReader(mainpath + "/output/latex/" +  projectName + "-" + `vNumber` + ".pdf").pages)

    # all files in latex folder deleted after
    # os.system("rm " + mainpath + "/output/latex/" +  projectName + "-" + `vNumber` + ".pdf")



# it defines all the global variables associated to the project,
# such as projectMatrix, projectName, projectType, versionNumber, etc.
def readProject(projectFileName):

        #### LIST OF CONSTANTS ####

    global projectMatrix
    projectMatrix = csvFileToMatrix(projectFileName, mainpath)
    print "projectMatrix: \n" + `projectMatrix` + "\n\n"
    # sys.stdout
    #matrixToCsvFile(projectMatrix, `sys.stdout`, "")

    # PROJECT NAME, TYPE AND TOTAL NUMBER OF VERSIONS
    # TO DO: (da separare e verificare anche questionNumber, confrontando con il numero di domande in questionListMatrix )
    global projectName, projectType, versionNumber
    projectName = projectMatrix[0][1]
    projectType = projectMatrix[1][1]
    versionNumber = int(projectMatrix[2][1])

    # INPUT FILE NAMES
    global questionListFileName, latexInputFileName, questionFolderName
    questionListFileName = projectMatrix[5][1]
    latexInputFileName = projectMatrix[6][1]
    questionFolderName = projectMatrix[7][1]

    #OUTPUT FILE NAMES
    global qNumberFileName, qCodeFileName, qAnswerOrderFileName, qKeyFileName
    qNumberFileName = projectMatrix[11][1]
    qCodeFileName = projectMatrix[12][1]
    qAnswerOrderFileName = projectMatrix[13][1]
    qKeyFileName = projectMatrix[14][1]

    #OUTPUT FILE OBJECTS
    global qNumberFile, qCodeFile, qAnswerOrderFile, qKeyFile
    qNumberFile = open( mainpath + "/output/" + qNumberFileName, 'w' )
    qCodeFile = open( mainpath + "/output/" + qCodeFileName, 'w' )
    qAnswerOrderFile = open( mainpath + "/output/" + qAnswerOrderFileName, 'w' )
    qKeyFile = open( mainpath + "/output/" + qKeyFileName, 'w' )


    # using csvFileToMatrix(csvFileName, csvFilePath) to read the list of the questions from file and make a matrix
    global questionListMatrix
    questionListMatrix = csvFileToMatrix(questionListFileName, mainpath + "/input" )

    # NUMBER OF QUESTIONS
    global questionNumber
    questionNumber = len(questionListMatrix)
    #print qNumber

    #### END LIST OF CONSTANTS ####


def main():

    global mainpath
    mainpath = os.getcwd()

        #### COMMAND LINE OPTIONS ####
    parser = argparse.ArgumentParser()
    # parser.parse_args()
    parser.add_argument("project", help="the project filename")
    args = parser.parse_args()
    projectFileName = args.project
    # pprint args.project
    print "projectFileName: " + projectFileName + "\n"

    # readProject defines all the global variables associated to the project
    readProject(projectFileName)

    global testWriter
    testWriter = PdfWriter()

    # creating the latex folder that will be deleted on exiting
    if not os.path.exists(mainpath + "/output/latex/"):
        os.makedirs(mainpath + "/output/latex/")

    # copying the figures and eventually other files in the /output/latex directory
    # TO ADD: option to copy other files, like other figures
    # shutil.copyfile( mainpath + "/input/buon-compito.pdf",
    #                          mainpath + "/output/latex/buon-compito.pdf")
    for j in range(0,questionNumber):
        if os.path.exists( mainpath + "/input/" + questionFolderName + "/" + "q" + questionListMatrix[j][1] + "-fig.pdf" ):
            #print j+1
            shutil.copyfile( mainpath + "/input/" + questionFolderName + "/" + "q" + questionListMatrix[j][1] + "-fig.pdf" ,
                             mainpath + "/output/latex/" + "q" + questionListMatrix[j][1] + "-fig.pdf")

        #shutil.copyfile(src, dst)
        #newQuestionString = makeQuestion(questionCodeList[j], int(questionTypeList[j]), questionAnswerOrderList[j])
        #allQuestionString = allQuestionString + newQuestionString    #encode('latin1')


    for vNumber in range(0,versionNumber+1):
        print "Now preparing version " + `vNumber` + " (of " + `versionNumber` + "+1)..."
        makeVersionFiles(vNumber)

    print "Now binding together the .pdf files of the " + `versionNumber` + "+1 versions"

    # saving the pdf file
    os.chdir(mainpath+"/output")
    testWriter.write(projectName + ".pdf")
    os.chdir(mainpath)

    # the latex directory is deleted on exiting
    shutil.rmtree(mainpath + "/output/latex")

    qNumberFile.close()
    qCodeFile.close()
    qAnswerOrderFile.close()
    qKeyFile.close()


main()
