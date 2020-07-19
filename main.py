import xml.etree.ElementTree as ET

def main_old():
    print('Welcome to the "Double your productivity by 5 P.M. tomorrow system!"')

    print("----------- Phase 1 - Planning -------------")

    dum = input("1/ What's your big goal (Month/Quarter/Year)? ")

    print("2/ Amplify your motivation for the Big Goal. Create a burning Desire.")
    dum = input("2/ a. Visualize (OK/KO): ")


def main():
    if True:
        root = ET.parse('double_your_productivity.xml').getroot()
        #for el in root.findall("text"):
        for el in root:
            print(el.text)
        #   print('Welcome to the "' + TODO + '" system!')
    else:
        main_old()

if __name__ == "__main__":
    main()
