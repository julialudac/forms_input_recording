import xml.etree.ElementTree as ET
import sys
import os
from pathlib import Path

def main_old():
    print('Welcome to the "Double your productivity by 5 P.M. tomorrow system!"')

    print("----------- Phase 1 - Planning -------------")

    dum = input("1/ What's your big goal (Month/Quarter/Year)? ")

    print("2/ Amplify your motivation for the Big Goal. Create a burning Desire.")
    dum = input("2/ a. Visualize (OK/KO): ")

def get_welcome_message(xml_root):
    title_element = list(xml_root)[0]
    return "Welcome to the " + title_element.text + " system!"


def read_and_fill(form_file):
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
                answer = input(el.text + " ")
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


def main():
    if True:
        """Read file"""
        filled_form = None
        while not filled_form:
            template_path = input("Which file should be open to read the template from? ")
            filled_form = read_and_fill(template_path)
        filled_form_str = ET.tostring(filled_form.getroot()).decode('utf8')
        print("Here is the filled form content:",  filled_form_str)

        
        """Potentially save file"""
        to_save = input("Would you like to save what you've filled? (Y/Anything)")
        if to_save == "Y":
            #  For now which file to write = hardcoded => TODO = ask user which file to read
            filename = input("Please specify the name of the file: ")
            dirpath = input("If you want to save at a specific directory path, please specify it: ")
            save_filled_form(filled_form, dirpath, filename)

    else:
        main_old()

if __name__ == "__main__":
    main()



