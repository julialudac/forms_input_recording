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
            a = input(el.text + " ")
            el.set("answer", "The answer")

    return ET.ElementTree(root)


def main():
    if True:
        read_and_fill("scrum_daily.xml")
    else:
        main_old

if __name__ == "__main__":
    main()



