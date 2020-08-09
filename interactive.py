import xml.etree.ElementTree as ET
import sys
import os
from pathlib import Path


def get_welcome_message(xml_root):
    title_element = list(xml_root)[0]
    return "Welcome to the " + title_element.text + " system!"

def is_a_template(root):
    ROOT_TEXT = "stepsdata"
    """TODO have a better check: The checks can be extracted into a function."""
    return root.tag == ROOT_TEXT


def create_form_instance_from(form_file):
    try:
        root = ET.parse(form_file).getroot()
        if not is_a_template(root):
            sys.stderr.write("Content of the file doesn't seem to be a template.\n")
            return
        print(get_welcome_message(root))
        for el in root:
            if el.tag == "text":
                print(el.text)
            elif el.tag == "question":
                print(el.text + " ")
                if __answer_exists__(el):
                    print("Current answer:", el.attrib.get("answer"))
                    new_answer = input("Do you want to provide another one? (Y/other)")
                    if new_answer != "Y":
                        continue
                answer = input()
                el.set("answer", answer)
        return ET.ElementTree(root)
    except (FileNotFoundError, IOError):
        sys.stderr.write("File doesn't exist.\n")
    return 

def save_filled_form(form, dirpath, filename):
    path = Path(dirpath)
    path.mkdir(parents=True, exist_ok=True)
    form.write(os.path.join(dirpath, filename))
    print("The form has been saved to " + dirpath + " with current name '" + filename + "'")

def __answer_exists__(question_node):
    return "answer" in question_node.attrib and question_node.attrib.get("answer")

def fill_form_menu():
    """Read file"""
    filled_form = None
    while not filled_form:
        template_path = input("Which file should be open to read the template from? ")
        filled_form = create_form_instance_from(template_path)
    filled_form_str = ET.tostring(filled_form.getroot()).decode('utf8')
    print("Here is the filled form content:",  filled_form_str)

    
    """Potentially save file"""
    to_save = input("Would you like to save what you've filled? (Y/Anything)")
    if to_save == "Y":
        filename = input("Please specify the name of the file: ")
        dirpath = input("If you want to save at a specific directory path, please specify it: ")
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
            if __answer_exists__(el):
                print("A:", el.attrib.get("answer"))
            else:
                print("No answer for this question")
    print()




def read_form(path_to_form):
    try:
        root = ET.parse(path_to_form).getroot()
        if not is_a_template(root):
            sys.stderr.write("Content of the file doesn't seem to be a template.\n")
        print("Here is the content of the form:")
        print_element_content(root)
    except (FileNotFoundError, IOError):
        sys.stderr.write("File doesn't exist.\n")
    

def read_form_menu():
    path_to_form = input("Please indicate the path to the form to read: ")
    read_form(path_to_form)


def main():
    print("Welcome to form input recording program.")
    option = ""
    while option not in ["1","2"]:
        option = input("What would you like to do?\n1. Fill a form\n2. Read form\n")
        if option == "1":
            fill_form_menu()
        elif option == "2":
            read_form_menu()

if __name__ == "__main__":
    main()



