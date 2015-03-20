__author__ = 'mouton'


def test_evaluation(unittest, expression, previousEvaluation, token, *expectedEvaluations):
    """
    Test if an expression that is True returns only one evaluation identical to the previous one.
    """

    evaluations = expression.eval(token, previousEvaluation)

    for evaluation, expected_evaluation in map(None, evaluations, expectedEvaluations):
        unittest.assertIsNotNone(evaluation)
        unittest.assertIsNotNone(expected_evaluation)
        unittest.assertEqual(evaluation, expected_evaluation)