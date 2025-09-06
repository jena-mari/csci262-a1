# Compilation Instructions

**CSCI262 Assignment #1 - Spring Session 2025**

**Part Two: Authentication and Access Control System**

**Jenamari P. Bathan, SN: 8565727**

This program is written in Python 3.

1. To initialise the FileSystem and run the hash/salt/shadow based user/password creation system (make sure you are in the directory where these files are located):
```bash
$ python3 FileSystem.py -i
```

Example:
```bash
MD5 ("This is a test") = ce114e4501d2f4e2dcea3e17b546f339
Username (or 'exit' to cancel): Bob
Password: CSCI262assignment1!
Confirm Password: CSCI262assignment1!
User clearance (0 or 1 or 2 or 3): 1
User Bob created successfully!
```

This will create, or append to:
- salt.txt
- shadow.txt

2. To run the FileSystem normally with no arguments, and allow a user to try and log into the file system (again, make sure you are in the directory where these files are located):
```python
$ python3 FileSystem.py
```

Example: 
operations:
```python
MD5 ("This is a test") = ce114e4501d2f4e2dcea3e17b546f339
Username: Bob
Password: CSCI262assignment1!
Bob found in salt.txt
salt retrieved: 39213302
hashing ...
hash value: 3fdf6a53be3989dc5a12e8779306679c
Authentication for Bob complete.
The clearance for Bob is 1.

Options: (C)reate, (A)ppend, (R)ead, (W)rite, (L)ist, (S)ave, (E)xit
Pick an option:
```
After this step, the user will be able to do any of the mentioned options.

## Reduction Implementation Notes
- User Authentication is based on the traditional salt/shadow model.
- Users are created using a salt/hash/shadow system:
    - `salt.txt` stores the username and randomised 8-digit salt
    - `shadow.txt` stores the username, hashed password+salt, and security clearance
- Passwords must meet minimum requirements to ensure its strength.
- Authentication is done by recomputing the salted hash and comparing it against shadow.txt.
- The internal file system allows creating, reading, writing, appending, listing, and saving files.
- Access is controlled according to the Bell–LaPadula model:
    - Users can only read files at or below their clearance.
    - Users can only write/append files at or above their clearance.
- Files are stored in memory and saved to Files.store for persistence.
- The program always reports a test MD5 hash: MD5("This is a test") at the start.

## CAPA Compatibility
- The program has been tested with Python 3 on CAPA.
- Ensure that the following files are present (or made) in the working directory:
  - FileSystem.py
  - salt.txt (initially empty)
  - shadow.txt (initially empty)
- The program does not rely on any external libraries other than the Python standard library.

## Example of the Program
<img width="894" height="799" alt="Screenshot 2025-09-06 at 5 18 51 pm" src="https://github.com/user-attachments/assets/486d6c42-8cb7-40dc-8e43-ae5408ad1065" />
