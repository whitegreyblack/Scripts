# help.py
# Help Database of different language syntaxes
import getopt
import sys

def main(argv):
    def usage():
        return "Usage:\n  python help.py -h | -u | -lang [arg] ]\n\t lang:[ sql | py | c#"

    languages = {"python": {"py", "python"}, "sql": {"sql", "sqlite", "mysql"}}
    try:
        opts, args = getopt.getopt(argv, "hul:", ["lang="])
    except getopt.GetoptError:
        print("Incorrect usage")
        exit(usage())

    if not opts and not args:
        print("No arguments specified")
        exit(usage())
    elif opts:
        for opt, arg in opts:
            if opt in ("-h", "u"):
                exit(usage())
            elif opt in ("-l", "--lang"):
                valid = False
                for language in languages:
                    if arg in languages[language]:
                        print("Language syntax for {}".format(language))
                        valid = True
                        break
                if not valid:
                    exit("Syntax help for input language not implemented")

if __name__ == "__main__":
    main(sys.argv[1:])