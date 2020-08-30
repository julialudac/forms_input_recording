import lxml.etree as etree
import sys
import os
from pathlib import Path

'''TODO maybe: put the free functions as class'method if it is only used once. '''


def is_a_template(root):
    ROOT_TEXT = "stepsdata"
    """TODO have a better check: The checks can be extracted into a function."""
    return root.tag == ROOT_TEXT


def get_welcome_message(xml_root):
    title_element = list(xml_root)[0]
    return "Welcome to the " + title_element.text + " system!"


def answer_exists(question_node):
    return "answer" in question_node.attrib and question_node.attrib.get("answer")


def create_form_instance_from(form_file):
    try:
        root = etree.parse(form_file).getroot()
        if not is_a_template(root):
            sys.stderr.write(
                "Content of the file doesn't seem to be a template.\n")
            return
        print(get_welcome_message(root))
        for el in root:
            if el.tag == "text":
                print(el.text)
            elif el.tag == "question":
                print(el.text + " ")
                if answer_exists(el):
                    print("Current answer:", el.attrib.get("answer"))
                    new_answer = input(
                        "Do you want to provide another one? (Y/other)")
                    if new_answer != "Y":
                        continue
                answer = input()
                el.set("answer", answer)
        return etree.ElementTree(root)
    except (FileNotFoundError, IOError):
        sys.stderr.write("File doesn't exist.\n")
    return


def save_filled_form(form, dirpath, filename):
    path = Path(dirpath)
    path.mkdir(parents=True, exist_ok=True)
    form.write(os.path.join(dirpath, filename))
    print("The form has been saved to " + dirpath +
          " with current name '" + filename + "'")


class ActionMenu:
    def __init__(self):
        self.execute()

    def execute(self):
        pass  # implemented into child classes


class FillFormMenu(ActionMenu):
    def execute(self):
        """Read file"""
        filled_form = None
        while not filled_form:
            template_path = input(
                "Which file should be open to read the template from? ")
            filled_form = create_form_instance_from(template_path)
        filled_form_str = etree.tostring(filled_form.getroot()).decode('utf8')
        print("Here is the filled form content:",  filled_form_str)

        """Potentially save file"""
        to_save = input(
            "Would you like to save what you've filled? (Y/Anything)")
        if to_save == "Y":
            filename = input("Please specify the name of the file: ")
            dirpath = input(
                "If you want to save at a specific directory path, please specify it: ")
            save_filled_form(filled_form, dirpath, filename)


def print_element_content(root):
    title = list(root)[0].text
    title = title.upper()
    print("\n")
    print("----------", title, "----------")
    print()
    for el in root:
        if el.tag == "text":
            print("\n" + el.text)
        elif el.tag == "question":
            print("Q:", el.text)
            if answer_exists(el):
                print("A:", el.attrib.get("answer"))
            else:
                print("No answer for this question")
    print()


def read_form(path_to_form):
    try:
        root = etree.parse(path_to_form).getroot()
        if not is_a_template(root):
            sys.stderr.write(
                "Content of the file doesn't seem to be a template.\n")
        print("Here is the content of the form:")
        print_element_content(root)
    except (FileNotFoundError, IOError):
        sys.stderr.write("File doesn't exist.\n")


class ReadFormMenu(ActionMenu):
    def execute(self):
        path_to_form = input("Please indicate the path to the form to read: ")
        read_form(path_to_form)


# TODO do defensive programming for this function... or not because the non-console part will be totally different
def create_answers_structure_from_similar_filled_forms(filled_forms, filled_forms_name):
    root = etree.Element("stepsdata")
    title = etree.SubElement(root, "title")
    title.text = filled_forms[0].findall("title")[0].text
    questions = filled_forms[0].findall("question")
    for i in range(len(questions)):
        question_text = etree.SubElement(root, "text")
        question_text.text = "Q: " + questions[i].text
        for j in range(len(filled_forms)):
            answer_text = etree.SubElement(root, "text")
            answer_text.text = "A from " + \
                filled_forms_name[j] + ": " + \
                filled_forms[j].findall("question")[i].attrib.get("answer")
    return etree.ElementTree(root)


def extract_filename_from_path(path):
    path_nodes = path.split("/")
    return path_nodes[-1]


class ReadFormsMenu(ActionMenu):
    def execute(self):
        # TODO defensive programming. Because here no verification at all
        forms_paths = [input("Form #1 to read: ")]
        open_others = "Y"
        next_instance_number = 2
        while open_others == "Y":
            # TODO a try-catch to handle invalid paths: In this case the path is not added and the next instance is not incrmented
            forms_paths.append(
                input("Form #" + str(next_instance_number) + " to read: "))
            next_instance_number += 1
            open_others = input(
                "Do you want to open other instances? (Y/other)")
        filled_forms = [etree.parse(forms_path) for forms_path in forms_paths]
        filled_forms_name = [extract_filename_from_path(
            forms_path) for forms_path in forms_paths]
        answers_structure = create_answers_structure_from_similar_filled_forms(
            filled_forms, filled_forms_name)
        print("Here are the answers from the collected forms for each questions:")
        print_element_content(answers_structure.getroot())
