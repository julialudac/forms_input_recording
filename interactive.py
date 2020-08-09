import xml.etree.ElementTree as ET
import sys
import os
from pathlib import Path


def get_welcome_message(xml_root):
    title_element = list(xml_root)[0]
    return "Welcome to the " + title_element.text + " system!"


def create_form_instance_from(form_file):
    try:
        root = ET.parse(form_file).getroot()
        ROOT_TEXT = "stepsdata"
        """TODO have a better check: The checks can be extracted into a function."""
        if root.tag != ROOT_TEXT:
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

def main():
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
        #  For now which file to write = hardcoded => TODO = ask user which file to read
        filename = input("Please specify the name of the file: ")
        dirpath = input("If you want to save at a specific directory path, please specify it: ")
        save_filled_form(filled_form, dirpath, filename)

if __name__ == "__main__":
    main()



