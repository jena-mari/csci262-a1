"""
Part Two: Authentication and Access Control System

1. Construct a hash/salt/shadow based user/password creation system
2. Construct a hash/salt/shadow based user authentication system.
3. Construct an associated file system, into which a user can log. Files can be created, read from,
   written to, but only in accordance with a four–level access control model.
4. The levels of the four–level access control model are 0, 1, 2 and 3. 0 is dominated by 1, 2 and 3; 
   and 1 and 2 are dominated by 3; and 1 is dominated by 2.
"""
# ---- IMPORT ----

import os
import hashlib
import random
import re
import sys

# ---- FILES ----
salt_file = "salt.txt"
shadow_file = "shadow.txt"
files_store = "Files.store"

# ---- HELPER FUNCTIONS ----

def md5_hash(text):
    return hashlib.md5(text.encode()).hexdigest()

def report_md5_test():
    # return this for every test
    print(f'MD5 ("This is a test") = {md5_hash("This is a test")}')

# ---- INITIALISATION ----
def initialisation():
    report_md5_test()

    # create blank files if missing
    for f in [salt_file, shadow_file]:
        if not os.path.exists(f):
            open(f, "w").close()

    while True:
        username = input("Username (or 'exit' to cancel): ").strip()
        if username.lower() == "exit":
            print("Cancelled.")
            return

        exists = False
        with open(salt_file, "r") as sf:
            for line in sf:
                if line.startswith(username + ":"):
                    exists = True
                    break
        if exists:
            print("User already exists. Try again.")
            continue
        break

    # create a password for entered username
    while True:
        password = input("Password: ")
        confirm = input("Confirm Password: ")
        if password != confirm:
            # confirm if passwords match
            print("Passwords do not match, try again.")
            continue
        # create password checks to meet standard requirements
        if len(password) < 6 or not re.search(r"[A-Za-z]", password) or not re.search(r"[0-9]", password):
            print("Password must be at least 6 characters and contain at least one letter and one number.")
            continue
        break

    # clearance
    while True:
        try:
            clearance = int(input("User clearance (0 or 1 or 2 or 3): "))
            if clearance not in [0,1,2,3]:
                print("Invalid clearance.")
                continue
            break
        except ValueError:
            print("Enter a number 0-3.")

    # generate salt and hash
    salt = str(random.randint(10000000, 99999999))
    pass_hash = md5_hash(password + salt)

    # add example lines if missing
    with open(salt_file, "r") as sf:
        lines = sf.read().splitlines()
    if "Username:Salt" not in lines:
        with open(salt_file, "a") as sf:
            sf.write("Username:Salt\n")
    with open(shadow_file, "r") as sh:
        lines = sh.read().splitlines()
    if "Username:PassSaltHash:SecurityClearance" not in lines:
        with open(shadow_file, "a") as sh:
            sh.write("Username:PassSaltHash:SecurityClearance\n")

    # append added username and necessary details
    with open(salt_file, "a") as sf:
        sf.write(f"{username}:{salt}\n")
    with open(shadow_file, "a") as sh:
        sh.write(f"{username}:{pass_hash}:{clearance}\n")

    # inform user that their username has been created
    print(f"User {username} created successfully!")

# ---- LOGIN ----
def logging_in():
    # report the test
    report_md5_test()

    # initial requirements
    salts = {}
    shadows = {}

    # load salts
    if os.path.exists(salt_file):
        with open(salt_file, "r") as sf:
            for line in sf:
                line = line.strip()
                if not line or line.startswith("Username:"):
                    continue  # skip blank lines or header
                try:
                    user, s = line.split(":")
                    salts[user] = s
                except ValueError:
                    print(f"Skipping malformed line in {salt_file}: {line}")

    # load shadows
    if os.path.exists(shadow_file):
        with open(shadow_file, "r") as sh:
            for line in sh:
                line = line.strip()
                if not line or line.startswith("Username:"):
                    continue  # skip blank lines or header
                try:
                    user, h, c = line.split(":")
                    shadows[user] = (h, int(c))
                except ValueError:
                    print(f"Skipping malformed line in {shadow_file}: {line}")

    # enter username
    username = input("Username: ").strip()
    if username not in salts:
        print("Authentication failed.")
        return None

    # verify password
    password = input("Password: ")
    salt = salts[username]
    hash_attempt = md5_hash(password + salt)

    if hash_attempt == shadows[username][0]:
        print(f"Authentication for {username} complete.")
        print(f"The clearance for {username} is {shadows[username][1]}.")
        return username, shadows[username][1]
    else:
        print("Authentication failed.")
        return None


    # print all necessary information
    print(f"{username} found in salt.txt")
    print(f"salt retrieved: {salt}")
    print("hashing ...")
    print(f"hash value: {hash_attempt}")

    if hash_attempt == shadows[username][0]:
        print(f"Authentication for {username} complete.")
        print(f"The clearance for {username} is {shadows[username][1]}.")
        return username, shadows[username][1]
    else:
        print("Incorrect password.")
        return None


# ---- ACCESS CONTROL (Bell-LaPadula) ----
# dominance rules:
# 0 < 1 < 2 < 3

dominance = {
    0: [1, 2, 3],
    1: [2, 3],
    2: [3],
    3: []
}

def can_read(user_level, file_level):
    # no read up: user can read if the file is at or below their clearance
    return file_level == user_level or file_level in dominance.get(user_level, [])

def can_write(user_level, file_level):
    # no write down: user can write if their clearance is at or below the file’s level
    return user_level == file_level or user_level in dominance.get(file_level, [])


# ---- FILESYSTEM MENU ----
def main_menu(user, clearance):
    files = {}

    # load Files.store if exists
    if os.path.exists(files_store):
        with open(files_store,"r") as fs:
            current_file = None
            for line in fs:
                line = line.strip()
                if not line: continue
                if line.startswith("---"): 
                    current_file = None
                    continue
                if "(" in line and "Owner:" in line and "Level:" in line:
                    parts = line.split("(")
                    fname = parts[0].strip()
                    details = parts[1].rstrip(")")
                    owner = details.split(",")[0].split(":")[1].strip()
                    level = int(details.split(",")[1].split(":")[1].strip())
                    files[fname] = {"owner": owner,"level":level,"content":""}
                    current_file = fname
                elif line.startswith("Content:") and current_file:
                    files[current_file]["content"] = line.replace("Content:","",1).strip()

    # use while loop to print out options
    while True:
        print("\nOptions: (C)reate, (A)ppend, (R)ead, (W)rite, (L)ist, (S)ave, (E)xit")
        choice = input("Pick an option: ").strip().upper()

        # creating a file
        if choice == "C":
            fname = input("Filename: ").strip()
            if fname in files:
                print("File already exists.")
            else:
                files[fname] = {"owner": user, "level": clearance, "content": ""}
                print(f"{fname} created!")

        # appending to an existing file
        elif choice == "A":
            fname = input("Filename: ").strip()
            if fname not in files:
                print("File doesn't exist.")
            else:
                if can_write(clearance, files[fname]["level"]):
                    print("Access granted (append).")
                    data = input("Text to append: ")
                    files[fname]["content"] += data
                    print("Appended!")
                else:
                    print("Access denied (can't write down).")

        # reading an existing file
        elif choice == "R":
            fname = input("Filename: ").strip()
            if fname not in files:
                print("File doesn't exist.")
            else:
                if can_read(clearance, files[fname]["level"]):
                    print("Access granted (read).")
                    print(f"Contents of {fname}:\n{files[fname]['content']}")
                else:
                    print("Access denied (can't read up).")

        # writing to an existing file (overwrite)
        elif choice == "W":
            fname = input("Filename: ").strip()
            if fname not in files:
                print("File doesn't exist.")
            else:
                if can_write(clearance, files[fname]["level"]):
                    print("Access granted (write).")
                    data = input("New content: ")
                    files[fname]["content"] = data
                    print("File overwritten!")
                else:
                    print("Access denied (can't write down).")


        # listing existing files and their content
        elif choice == "L":
            if files:
                for fname, info in files.items():
                    print(f"{fname} (Owner: {info['owner']}, Level: {info['level']})")
            else:
                print("No files yet.")

        # saving files
        elif choice == "S":
            with open(files_store,"w") as fs:
                for fname, info in files.items():
                    fs.write(f"{fname} (Owner: {info['owner']}, Level: {info['level']})\n")
                    fs.write(f"Content: {info['content']}\n")
                    fs.write("---\n")
            print("Files saved!")

        # exiting the file system
        elif choice == "E":
            confirm = input("Shut down the FileSystem? (Y)es or (N)o: ").strip().upper()
            if confirm == "Y":
                print("Goodbye!")
                break

        else:
            print("Invalid option, try again.")

# ---- MAIN ----
if __name__ == "__main__":
    # use initialisation if user states -i
    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        initialisation()
    else:
        # otherwise, do a regular log in
        creds = logging_in()
        if creds:
            main_menu(*creds)

