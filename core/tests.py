import pytest
from .reply_factory import record_current_answer, generate_final_response, get_next_question
from .constants import PYTHON_QUESTION_LIST, BOT_WELCOME_MESSAGE

@pytest.fixture
def mock_session():
    # Mock session
    return {"user_answers": {}, "current_question_id":0}

def test_record_current_answer_correct(mock_session):
    current_question_id = 0
    answer = "7"

    success, error = record_current_answer(answer, current_question_id, mock_session)
    assert success is True
    assert mock_session["user_answers"][0]["user_answer"] == "7"
    assert mock_session["user_answers"][0]["is_correct"] is True

def test_record_current_answer_incorrect(mock_session):
    current_question_id = 0
    invalid_answer = "invalid answer"

    success, error = record_current_answer(invalid_answer, current_question_id, mock_session)
    assert success is False
    assert error == "Invalid answer" in error
    assert 0 not in mock_session["user_answers"]

def test_record_current_answer_wrong_answer(mock_session):
    current_question_id = 0
    wrong_answer = "52"  

    success, error = record_current_answer(wrong_answer, current_question_id, mock_session)

    assert success is True
    assert error == ""
    assert mock_session["user_answers"][0]["user_answer"] == "52"
    assert mock_session["user_answers"][0]["is_correct"] is False

def test_get_next_question_valid():
    
    current_question_id = 0
    next_question, next_question_id = get_next_question(current_question_id)

    assert next_question == PYTHON_QUESTION_LIST[1]["question_text"]
    assert next_question_id == 1

def test_get_next_question_end_of_list():
    
    current_question_id = len(PYTHON_QUESTION_LIST) - 1  # Last question
    next_question, next_question_id = get_next_question(current_question_id)

    assert next_question is None
    assert next_question_id is None

def test_generate_final_response_all_correct(mock_session):
    
    for i, question in enumerate(PYTHON_QUESTION_LIST):
        mock_session["user_answers"][i] = {"user_answer": question["answer"], "is_correct": True}

    response = generate_final_response(mock_session)

    assert f"Your Score: {len(PYTHON_QUESTION_LIST)}/{len(PYTHON_QUESTION_LIST)}" in response

def test_generate_final_response_partial_correct(mock_session):
    
    total_questions = len(PYTHON_QUESTION_LIST)
    for i in range(total_questions):
        is_correct = i % 2 == 0  # Mark even-indexed answers as correct
        mock_session["user_answers"][i] = {"user_answer": "dummy", "is_correct": is_correct}

    correct_answers = total_questions // 2 + (total_questions % 2)  # Half questions correct
    response = generate_final_response(mock_session)

    assert f"Your Score: {correct_answers}/{total_questions}" in response

def test_generate_final_response_no_correct(mock_session):
    
    for i in range(len(PYTHON_QUESTION_LIST)):
        mock_session["user_answers"][i] = {"user_answer": "wrong", "is_correct": False}

    response = generate_final_response(mock_session)

    assert f"Your Score: 0/{len(PYTHON_QUESTION_LIST)}" in response

