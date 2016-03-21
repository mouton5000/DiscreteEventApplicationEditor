__author__ = 'mouton'

import os
import stateMachine
import shutil

exportMainFileName = 'exportMain.py'


def copyFiles(exportFolder, rootDir):
    if not os.path.exists(exportFolder):
        os.makedirs(exportFolder)
    for fileName in os.listdir(rootDir):
        if rootDir + '/' + fileName == exportFolder:
            continue

        if os.path.isdir(rootDir + '/' + fileName):
            try:
                shutil.copytree(rootDir + '/' + fileName, exportFolder + '/' + fileName)
            except OSError:
                shutil.rmtree(exportFolder + '/' + fileName)
                shutil.copytree(rootDir + '/' + fileName, exportFolder + '/' + fileName)
        else:
            shutil.copy2(rootDir + '/' + fileName, exportFolder + '/' + fileName)


def writeStaticInfos(exportFolder):
    exportFilesNames = ['stateMachine.py',
                        'database.py',
                        'utils/__init__.py',
                        'utils/dictSet.py',
                        'utils/mathutils.py',
                        'grammar/__init__.py',
                        'grammar/arithmeticExpressions.py',
                        'grammar/consequenceExpressions.py',
                        'grammar/keywords.py',
                        'grammar/triggerExpressions.py',
                        'game/__init__.py',
                        'game/gameWindow.py',
                        'game/Registeries/__init__.py',
                        'game/Registeries/LineRegistery.py',
                        'game/Registeries/OvalRegistery.py',
                        'game/Registeries/PolygonRegistery.py',
                        'game/Registeries/RectRegistery.py',
                        'game/Registeries/SoundRegistery.py',
                        'game/Registeries/SpriteRegistery.py',
                        'game/Registeries/TextRegistery.py']
    try:
        for exportFileName in exportFilesNames:
            path = os.path.dirname(exportFolder + '/' + exportFileName)
            if not os.path.exists(path):
                os.makedirs(path)
            importFileName = './' + exportFileName
            with open(exportFolder + '/' + exportFileName, 'w') as exportFile:
                with open(importFileName, 'r') as importFile:
                    export = True
                    for line in importFile:
                        if '# NO EXPORT' in line:
                            export = False
                            continue
                        if '# EXPORT' in line:
                            export = True
                            continue

                        if export:
                            exportFile.write(line)
                exportFile.write('\n\n')
    except IOError as e:
        print e


def writeImportInfos(exportFolderName):

    try:
        with open(exportFolderName + '/' + exportMainFileName, 'w') as exportMainFile:
            exportMainFile.write('import stateMachine\n')
            exportMainFile.write('from stateMachine import Transition\n')
            exportMainFile.write('import game.gameWindow as gameWindow\n')
            exportMainFile.write('from grammar.triggerExpressions import *\n')
            exportMainFile.write('from grammar.consequenceExpressions import *\n')
            exportMainFile.write('from grammar.arithmeticExpressions import *\n')
            exportMainFile.write('from grammar.keywords import *\n')
            exportMainFile.write('from utils.mathutils import sign\n')

            exportMainFile.write('from random import random, randint\n')
            exportMainFile.write('from math import cos, sin, tan, exp, log, floor, '
                                 'ceil, acos, asin, atan, cosh, sinh, tanh, acosh, atanh, asinh\n')

            exportMainFile.write('\n\n')
    except IOError as e:
        print e
        pass


def writeVariableInfos(exportFolderName):
    nodes = stateMachine.getNodes()

    try:
        with open(exportFolderName + '/' + exportMainFileName, 'a') as exportMainFile:

            exportMainFile.write('def _random(x):\n')
            exportMainFile.write('  return random() * x\n\n')

            exportMainFile.write('def _random(x):\n')
            exportMainFile.write('  return random() * x\n\n')

            exportMainFile.write('def _randint(x):\n')
            exportMainFile.write('  return randint(0, x - 1)\n\n')

            def printNode(n):
                exportMainFile.write('stateMachine.addNode(' + str(n.num) + ',\'' + n._name + '\')\n')

            def printArc(a):
                formula = arc.exportFormula()
                consequence = arc.exportConsequences()

                exportMainFile.write('Transition(stateMachine.getNodeByNum(' + str(a.n1.num) +
                                     '), stateMachine.getNodeByNum(' + str(a.n2.num) + '), '
                                     + formula + ', ' + consequence + ', False)\n')

            for node in nodes:
                printNode(node)

            exportMainFile.write('\n\n')

            for node in nodes:
                for arc in node.outputArcs:
                    printArc(arc)

            exportMainFile.write('\n\n')

            exportMainFile.write('\n\n')
    except IOError as e:
        print e
        pass


def writeLaunchInfos(exportFolderName, fps, maxTick, width, height, rootDir, initConsequences):

    try:
        with open(exportFolderName + '/' + exportMainFileName, 'a') as exportMainFile:
            exportMainFile.write('fps = ' + str(fps) + '\n')
            exportMainFile.write('maxTick = ' + str(maxTick) + '\n')
            exportMainFile.write('width = ' + str(width) + '\n')
            exportMainFile.write('height = ' + str(height) + '\n')
            exportMainFile.write('rootDir = \'' + rootDir + '/export\'' + '\n')

            exportMainFile.write('\n')

            exportMainFile.write('initConsequences = ' + stateMachine.exportInitConsequences(initConsequences) + '\n')

            exportMainFile.write('\n')

            runFile = open('./exporter/run', 'r')
            exportMainFile.write(runFile.read())

            exportMainFile.write('\n\n')
    except IOError as e:
        print e
        pass