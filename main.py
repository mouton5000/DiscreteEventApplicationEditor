#!/usr/bin/env python

import sys
from PyQt4.QtGui import QApplication as QApp
from gui.EditorWindow import MainWindow


def main():

    hasToCompile = True

    if hasToCompile:
        print 'Compile grammar (0/3)'
        from grammar.grammar import BooleanExpressionParser
        BooleanExpressionParser.pre_compile_grammar()
        print 'Compile grammar (1/3)'
        from grammar.consequencesGrammar import ConsequencesParser
        ConsequencesParser.pre_compile_grammar()
        print 'Compile grammar (2/3)'
        from grammar.tokenGrammar import TokenParametersParser
        TokenParametersParser.pre_compile_grammar()
        print 'Compile grammar (3/3)'

    app = QApp(sys.argv)
    ex = MainWindow()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()