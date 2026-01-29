def mock_evaluate_answer_sheet(answer_sheet_filename, answer_key_filename):
    """
    mock evaluation function
    Returns: score, weak_areas, feedback
    """

    return {
        'score': 42,
        'total_marks': 50,
        'percentage': 84.0,
        'weak_areas': ['Algebra', 'Geometry'],
        'feedback': 'Good effort! Focus more on Algebra and Geometry to improve your score.'
    }