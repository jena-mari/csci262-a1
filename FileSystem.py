"""
Part Two: Authentication and Access Control System

1. Construct a hash/salt/shadow based user/password creation system
2. Construct a hash/salt/shadow based user authentication system.
3. Construct an associated file system, into which a user can log. Files can be created, read from,
written to, but only in accordance with a four–level access control model.
4. The levels of the four–level access control model are 0, 1, 2 and 3. 0 is dominated by 1, 2 and 3; and
1 and 2 are dominated by 3; and 1 is dominated by 2.

"""

# ---- INITIAL REQUIREMENTS ----

# import all needed modules
import os
import hashlib
import json
import random
import re
import sys

# state blank files
salt_file = "salt.txt" # for initialisation
shadow_file = "shadow.txt" # for initialisation
files_store = "Files.store" # for logging in

def md5_hash(text):
    # call MD5 with text for reporting test output
    return hashlib.md5(text.encode()).hexdigest()

# report test output of the MD5
def report_output():
    print(f'MD5 ("This is a test") = {md5_hash("This is a test")}')


# ---- INITIALISATION FUNCTION ----
def initialisation():

    # report output
    report_output()

    # prompt for a username
    username = input("Username: ").strip()
    # check if this username exists in the salt.txt file
    if os.path.exists(salt_file):
        with open(salt_file) as a: # open salt file as "a" (placeholder name)
            for line in a:
                if line.startswith(username + ":"): # follows the format of usernames in salt.txt file
                    print("User already exists.") # say if user exists
                    return

    # prompt for a password and confirm
    password = input("Password: ")
    confirm_password = input("Confirm Password: ")

    if password != confirm_password: # if both passwords don't match
        print("Passwords do not match. Please try again.")
        return
    
    # add appropriate checks for a strong password and stronger entropy
    if len(password) < 8:
        print("Password must be at least 8 characters long. Please try again.")
        return
    if not re.search(r"[A-Z]", password):
        print("Password must contain at least one uppercase letter (A–Z). Please try again.")
        return
    if not re.search(r"[a-z]", password):
        print("Password must contain at least one lowercase letter (a–z). Please try again.")
        return
    if not re.search(r"[0-9]", password):
        print("Password must contain at least one digit (0–9). Please try again.")
        return
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print("Password must contain at least one special character (!@#$%^&* etc.). Please try again.")
        return
    
    # clearance input (final request of the user)
    try:
        security_clearance = int(input("User clearance (0 or 1 or 2 or 3): "))
    except ValueError:
        print("Invalid input. User clearance must be a number.") # if input was not a number
        return
    if security_clearance not in [0, 1, 2, 3]:
        print("Invalid input. Please choose only from numbers 0-3.") # if input was not among the list
        return

    # if all of this passes, we can proceed to modifying salt.txt and shadow.txt to include the user

    # create salt = randomly chosen string of 8 digits
    salt = str(random.randint(10000000, 99999999))
    # create salted hash using md5
    pass_salt_hash = md5_hash(password + salt)

    # append to salt.txt and shadow.txt
    with open(salt_file, "a") as sf:
        sf.write(f"{username}:{salt}\n")
    with open(shadow_file, "a") as sh:
        sh.write(f"{username}:{pass_salt_hash}:{security_clearance}\n")

    print(f"User {username} created successfully.")


# ---- LOGGING IN ----
def logging_in():
    
    # report output
    report_output()

    # load salts and shadows into memory
    salts = {}
    shadows = {}

    # locate salt and user in salt_file
    if os.path.exists(salt_file):
        with open(salt_file, "r") as sf:
            for line in sf:
                if ":" in line:
                    user, s = line.strip().split(":")
                    salts[user] = s
    if os.path.exists(shadow_file):
        with open(shadow_file, "r") as sh:
            for line in sh:
                if ":" in line:
                    user, pass_salt_hash, security_clearance = line.strip().split(":")
                    shadows[user] = (pass_salt_hash, security_clearance)

    # prompt for a username
    username = input("Username: ").strip()
    # check if the username exists
    if username not in salts:
        print("This user does not exist.") # if user does not exist
        return None
        
    # prompt for a password
    password = input("Password: ")

    # retrieve salt and hash
    salt = salts[username]
    print(f"{username} found in salt.txt")
    print(f"salt retrieved: {salt}")
    print("hashing ...")
    pass_salt_hash = md5_hash(password + salt)
    print(f"hash value: {pass_salt_hash}")

    # check if hash matches shadow
    if username in shadows and pass_salt_hash == shadows[username][0]:
        security_clearance = shadows[username][1] # obtain security clearance
        print(f"Authentication for {username} complete.") # report authentication 
        print(f"The clearance for {username} is {security_clearance}.") # report clearance
        return username, security_clearance
    else:
        print("Incorrect password.")
        return None
    
# ---- ONCE LOGGED IN ----

def main_menu(user, security_clearance):

    # load files into memory
    files = {}

    # open files_store
    if os.path.exists(files_store):
        with open(files_store) as fs:
            current_file = None
            for line in fs:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("---"):
                    current_file = None
                    continue
                if "(" in line and "Owner:" in line and "Level:" in line:
                    # Parse filename, owner, level
                    parts = line.split("(")
                    fname = parts[0].strip()
                    details = parts[1].rstrip(")")
                    owner = details.split(",")[0].split(":")[1].strip()
                    level = int(details.split(",")[1].split(":")[1].strip())
                    files[fname] = {"owner": owner, "level": level, "content": ""}
                    current_file = fname
                elif line.startswith("Content:") and current_file:
                    files[current_file]["content"] = line.replace("Content:", "", 1).strip()

    # create a while loop for the main menu
    while True:
        # create a list of options
        print("Options: (C)reate, (A)ppend, (R)ead, (W)rite, (L)ist, (S)ave or (E)xit.\n ")
        # ask for user's choice 
        choice = input("Choose one of the options: ").strip().upper()

        # if choice is (c)reate
        if choice == "C":
            filename = input("Filename: ").strip()
            if filename in files:
                print("File already exists.")
            else:
                files[filename] = {
                    "owner": user,
                    "level": int(security_clearance),
                    "content": ""
                }
                print(f"File {filename} created.")

        elif choice == "A":
            filename = input("Filename: ").strip()
            if filename not in files:
                print("File does not exist.")
            else:
                if int(security_clearance) <= files[filename]["level"]:
                    data = input("Enter text to append: ")
                    files[filename]["content"] += data
                    print("Data appended.")
                else:
                    print("Access denied: insufficient clearance to append.")

        elif choice == "R":
            filename = input("Filename: ").strip()
            if filename not in files:
                print("File does not exist.") 
            else:
                if int(security_clearance) >= files[filename]["level"]:
                    print(f"Contents of {filename}: {files[filename]['content']}")
                else:
                    print("Access denied: insufficient clearance to read.")

        elif choice == "W":
            filename = input("Filename: ").strip()
            if filename not in files:
                print("File does not exist.") 
            else:
                if int(security_clearance) <= files[filename]["level"]:
                    data = input("Enter new content: ")
                    files[filename]["content"] = data
                    print("File overwritten.")
                else:
                    print("Access denied: insufficient clearance to write.")

        elif choice == "L":
            if files:
                for fname, info in files.items():
                    print(f"{fname} (Owner: {info['owner']}, Level: {info['level']})")
            else:
                print("No files created yet.")

        elif choice == "S":
            with open(files_store, "w") as fs:
                for fname, info in files.items():
                    fs.write(f"{fname} (Owner: {info['owner']}, Level: {info['level']})\n")
                    fs.write(f"Content: {info['content']}\n")
                    fs.write("---\n")
            print("Files saved.")

        elif choice == "E":
            confirm = input("Shut down the FileSystem? (Y)es or (N)o: ").strip().upper()
            if confirm == "Y":
                break
        else:
            print("Invalid choice. Please select a valid option.")

# ---- MAIN FUNCTION ----
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        initialisation()
    else:
        creds = logging_in()
        if creds:
            main_menu(*creds)
