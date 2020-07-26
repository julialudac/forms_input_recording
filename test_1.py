from unittest.mock import Mock
import interactive
import unittest.mock
import xml.etree.ElementTree as ET


"""Testing the behavior of the whole"""

def test_double_your_productivity_has_1_display_and_3_questions_to_fill():
    form = "double_your_productivity.xml"
    interactive.input = Mock()
    interactive.read_and_fill(form)
    assert interactive.input.call_count == 3 

def test_scrum_daily_has_1_display_and_3_questions_to_fill():
    form = "scrum_daily.xml"
    interactive.input = Mock()
    interactive.print = Mock()

    interactive.read_and_fill(form)

    assert interactive.input.call_count == 3 
    assert interactive.print.call_count == 1

#def test_print_and_ask_input_given_the_step_data:
#    with open("double_your_productivity.xml") as step_data:
#        ask_user_inputs(step_data)
            


#def test_register_questions_answers():
    

#def test_get_display_of_questions_answer():
#    SAME_ANSWER = "The answer"  # can only mock input() with one constant value
#    expected = ""
#    with open("display_of_questions_answer1.txt") as f:
#        expected = f.read()
#    with mock.patch("builtins.input", return_value=SAME_ANSWER):
#        questions_answers = main.get_display_of_questions_answer()
#        assert expected == questions_answers

"""Tests at a micro level"""

def test_get_welcome_message_for_scrum_daily_sheet():
    form = "scrum_daily.xml"
    root = ET.parse(form).getroot()

    welcome_message = interactive.get_welcome_message(root) 

    assert "Welcome to the Scrum Daily system!" == welcome_message
    
def test_get_scrum_daily_xml_with_answers():
    form = "scrum_daily.xml"
    SAME_ANSWER = "The answer"  # can only mock input() with one constant value
    form_with_answers = None
    with unittest.mock.patch("builtins.input", return_value=SAME_ANSWER):
        form_with_answers = interactive.read_and_fill(form)
        for qa in form_with_answers.getroot().findall("question"):
            assert qa.attrib.get("answer") == SAME_ANSWER

# Do I really need that:
#    """Collection of expected answers"""
#    expected_form = "scrum_daily_dummy_answers.xml"
#    root = ET.parse(expected_form).getroot()
#    for qa in root.findall("question"):
#        assert qa.attrib.get("answer") == SAME_ANSWER
