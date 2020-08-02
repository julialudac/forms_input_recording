from unittest.mock import Mock
import interactive
import unittest.mock
import xml.etree.ElementTree as ET
import mock


"""Testing the behavior of the whole"""


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
        actual_form_str = ET.tostring(form_with_answers.getroot()).decode('utf-8')
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
        actual_form_str = ET.tostring(form_with_answers.getroot()).decode('utf-8')
    assert " ".join(expected_form_str.split()) == " ".join(actual_form_str.split())


def test_do_not_stop_when_file_does_not_exist():
    form_file = "scrum_dailyy.xml"
    with unittest.mock.patch("builtins.input", return_value="Whatever"):
        interactive.read_and_fill(form_file)


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

