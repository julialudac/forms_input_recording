from unittest.mock import Mock
import interactive
import unittest.mock
import xml.etree.ElementTree as ET
import mock


"""Testing the behavior of the whole"""


# Do we really write the file while running the unit test or is there another softer way?
# TODO find a better way
def test_save_filled_form():
    form_file = "scrum_daily.xml"
    SAME_ANSWER = "The answer"  # can only mock input() with one constant value
    form_with_answers = None
    expected_form_file = "scrum_daily_dummy_answers.xml"
    expected_form_str = None
    actual_form_str = None
    with open(expected_form_file) as f:
        expected_form_str = f.read()

    with unittest.mock.patch("builtins.input", return_value=SAME_ANSWER):
        form_with_answers = interactive.read_and_fill(form_file)
        actual_form_file = "test_form_with_answers.xml"
        form_with_answers.write(actual_form_file)
        with open(actual_form_file) as f:
            actual_form_str = f.read()

    assert " ".join(expected_form_str.split()) == " ".join(actual_form_str.split())
    

def test_save_filled_form2():
    form_file = "scrum_daily.xml"
    SAME_ANSWER = "The answer 2"  # can only mock input() with one constant value
    form_with_answers = None
    expected_form_file = "scrum_daily_dummy_answers2.xml"
    expected_form_str = None
    actual_form_str = None
    with open(expected_form_file) as f:
        expected_form_str = f.read()

    with unittest.mock.patch("builtins.input", return_value=SAME_ANSWER):
        form_with_answers = interactive.read_and_fill(form_file)
        actual_form_file = "test_form_with_answers2.xml"
        form_with_answers.write(actual_form_file)
        with open(actual_form_file) as f:
            actual_form_str = f.read()

    assert " ".join(expected_form_str.split()) == " ".join(actual_form_str.split())



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

