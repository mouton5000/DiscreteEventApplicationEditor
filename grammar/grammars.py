__author__ = 'mouton'


def compileGrammars():
    print 'Compile grammar (0/3)'

    from grammar.triggerGrammar import TriggerParser
    from grammar.preCompiledBooleanExpressionGrammar import preCompiledBooleanExpressionGrammar
    newCompiledBooleanExpressionGrammar = \
        TriggerParser.pre_compile_grammar(preCompiledBooleanExpressionGrammar)
    if newCompiledBooleanExpressionGrammar is not None:
        print 'New Boolean Expression Grammar'
        with open('grammar/preCompiledBooleanExpressionGrammar.py', 'w') as f:
            f.write('__author__ = \'mouton\'\n\n')
            f.write('preCompiledBooleanExpressionGrammar = ')
            f.write(newCompiledBooleanExpressionGrammar)
    print 'Compile grammar (1/3)'

    from grammar.consequenceGrammar import ConsequenceParser
    from grammar.preCompiledConsequenceGrammar import preCompiledConsequenceGrammar
    newCompiledConsequenceGrammar = \
        ConsequenceParser.pre_compile_grammar(preCompiledConsequenceGrammar)
    if newCompiledConsequenceGrammar is not None:
        print 'New Consequence Grammar'
        with open('grammar/preCompiledConsequenceGrammar.py', 'w') as f:
            f.write('__author__ = \'mouton\'\n\n')
            f.write('preCompiledConsequenceGrammar = ')
            f.write(newCompiledConsequenceGrammar)
    print 'Compile grammar (2/3)'

    from grammar.tokenGrammar import TokenParametersParser
    from grammar.preCompiledTokenGrammar import preCompiledTokenGrammar
    newCompiledTokenGrammar = TokenParametersParser.pre_compile_grammar(preCompiledTokenGrammar)
    if newCompiledTokenGrammar is not None:
        print 'New Token Grammar'
        with open('grammar/preCompiledTokenGrammar.py', 'w') as f:
            f.write('__author__ = \'mouton\'\n\n')
            f.write('preCompiledTokenGrammar = ')
            f.write(newCompiledTokenGrammar)
    print 'Compile grammar (3/3)'