password = input("Enter in a password: ")

lenCon = False
numCon = False
upperCon = False
lowerCon = False
sequence = False

alphabet = "0123456789abcdefghijklmnopqrstuvwxy"

if 6 < len(password) < 16:
    lenCon = True

# keeps track of how many numbers there are in the password
num_integers = 0
index_first_int = None

# enumerate allows us to use position as well as the character
for i, c in enumerate(password):
    print(i, c)
    if c.isnumeric():
        print("is number")
        numCon = True
        num_integers += 1
        if not index_first_int:
            index_first_int = i

    elif c.isupper():
        print("is upper")
        upperCon = True

    elif c.islower():
        print("is lower")
        lowerCon = True

if index_first_int:
    finished_loop = True
    for i in password[index_first_int:index_first_int+num_integers+1]:
        if not i.isdigit():
            finished_loop = False
            break
    if finished_loop:
        sequence = True
'''
for i in password:
    if i.isdigit():
        sequence = True
'''
if lenCon and numCon and upperCon and lowerCon and sequence:
    print("password accepted")
else:
    print("password rejected")
    print("LenCon: ", lenCon)
    print("NumCon: ", numCon)
    print("upperCon: ", upperCon)
    print("LowerCon: ", lowerCon)
    print("Sequence: ", sequence)
