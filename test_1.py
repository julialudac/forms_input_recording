from unittest.mock import Mock
import interactive
import unittest.mock
import xml.etree.ElementTree as ET
import mock
import os
import lxml.etree as etree

#TODO replace ET uses by etree

"""Testing the behavior of the whole"""


def test_save_filled_form():
    form_file = "data/scrum_daily.xml"
    SAME_ANSWER = "The answer"  # can only mock input() with one constant value
    form_with_answers = None
    expected_form_file = "data/scrum_daily_dummy_answers.xml"
    expected_form_str = None
    actual_form_str = None
    with open(expected_form_file) as f:
        expected_form_str = f.read()
    with unittest.mock.patch("builtins.input", return_value=SAME_ANSWER):
        form_with_answers = interactive.create_form_instance_from(form_file)
        actual_form_str = ET.tostring(form_with_answers.getroot()).decode('utf-8')
    assert " ".join(expected_form_str.split()) == " ".join(actual_form_str.split())
    

def test_save_filled_form2():
    form_file = "data/scrum_daily.xml"
    SAME_ANSWER = "The answer 2"  # can only mock input() with one constant value
    form_with_answers = None
    expected_form_file = "data/scrum_daily_dummy_answers2.xml"
    expected_form_str = None
    actual_form_str = None
    with open(expected_form_file) as f:
        expected_form_str = f.read()
    with unittest.mock.patch("builtins.input", return_value=SAME_ANSWER):
        form_with_answers = interactive.create_form_instance_from(form_file)
        actual_form_str = ET.tostring(form_with_answers.getroot()).decode('utf-8')
    assert " ".join(expected_form_str.split()) == " ".join(actual_form_str.split())


"""Tests at a micro level"""

def test_get_welcome_message_for_scrum_daily_sheet():
    form = "data/scrum_daily.xml"
    root = ET.parse(form).getroot()

    welcome_message = interactive.get_welcome_message(root) 

    assert "Welcome to the Scrum Daily system!" == welcome_message
    
def test_get_scrum_daily_xml_with_answers():
    form = "data/scrum_daily.xml"
    SAME_ANSWER = "The answer"  # can only mock input() with one constant value
    form_with_answers = None
    with unittest.mock.patch("builtins.input", return_value=SAME_ANSWER):
        form_with_answers = interactive.create_form_instance_from(form)
        for qa in form_with_answers.getroot().findall("question"):
            assert qa.attrib.get("answer") == SAME_ANSWER

def test_do_not_stop_when_file_does_not_exist():
    form_file = "data/scrum_dailyy.xml"
    with unittest.mock.patch("builtins.input", return_value="Whatever"):
        interactive.create_form_instance_from(form_file)

def test_when_file_is_not_a_template_dont_return_an_ElementTree():
    form_file = "data/scrum_daily_impostor.xml"
    with unittest.mock.patch("builtins.input", return_value="Whatever"):
        nothing = interactive.create_form_instance_from(form_file)
        assert nothing == None

def test_write_saved_file_to_indicated_place():

    person_root = ET.Element("person")
    name = ET.SubElement(person_root, "name")
    name.text = "Toto Novi"
    address = ET.SubElement(person_root, "address")
    street_number = ET.SubElement(address, "number")
    street_number.text = "117"
    street_name = ET.SubElement(address, "name")
    street_name.text = "Vaalser Strasse"
    person = ET.ElementTree(person_root)

    target_dir = "data/test_forms"
    target_filename = "toto_txt.xml"
    target = os.path.join(target_dir, target_filename)
    if os.path.exists(target):
        os.remove(target)
    interactive.save_filled_form(person, target_dir, target_filename)

    assert os.path.exists(target)

     
def test_question_node_has_an_answer():
    question = ET.Element("question")
    question.set("answer", "data/An Answer")
    assert interactive.__answer_exists__(question)

def test_question_node_has_no_answer():
    question = ET.Element("question")
    assert not interactive.__answer_exists__(question)

    question.set("answer", "")
    assert not interactive.__answer_exists__(question)

def test_create_answers_structure_from_similar_filled_forms():
   expected_answers_structure = ET.parse("data/dailies/daily_answers.xml")
   filled_forms_paths = ["data/dailies/daily_julia.xml", "data/dailies/daily_thomas.xml", "data/dailies/daily_paul.xml"] 
   filled_forms_name = ["Julia", "Thomas", "Paul"]
   filled_forms = [ET.parse(path) for path in filled_forms_paths] 

   actual_answers_structure = interactive.create_answers_structure_from_similar_filled_forms(filled_forms, filled_forms_name)
   actual_answers_structure_root = etree.fromstring(ET.tostring(actual_answers_structure.getroot()).decode('utf8'))

   """ There is no real way to compare 2 elements, so the trick is to convert them into strings. There is the trap
   of whitespaces, which make the test break with the alignment of the elements in the string is not the
   same => The trick is to make the actual and expected elements have the same format using pretty print from etree
   and 2 whitespaces indentation in the expected file. This is an ugly test, but so far I don't know other possiblities
   that work."""
   expected_answers_structure_root_str = ET.tostring(expected_answers_structure.getroot()).decode() 
   actual_answers_structure_root_str = etree.tostring(actual_answers_structure_root, pretty_print=True).decode()
   actual_answers_structure_root_str = actual_answers_structure_root_str[:len(actual_answers_structure_root_str)-1] # -1 because of an extra \n to throw away
   assert expected_answers_structure_root_str == actual_answers_structure_root_str 
