import xml.etree.ElementTree as ET

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
    root = ET.parse(form_file).getroot()
    print(get_welcome_message(root))

    for el in root:
        if el.tag == "text":
            print(el.text)
        elif el.tag == "question":
            answer = input(el.text + " ")
            el.set("answer", answer)

    return ET.ElementTree(root)

def save_filled_form(form, filename):
    form.write(filename)
    print("The form has been saved with current name '" + filename + "'")


def main():
    if True:
        #  For now which file to read = hardcoded => TODO = ask user which file to read
        filled_form = read_and_fill("scrum_daily.xml")
        to_save = input("Would you like to save what you've filled? (Y/Anything)")
        if to_save == "Y":
            #  For now which file to write = hardcoded => TODO = ask user which file to read
            save_filled_form(filled_form, "scrum_daily_filled.xml")
    else:
        main_old()

if __name__ == "__main__":
    main()



