# Compilation Instructions

**CSCI262 Assignment #1 - Spring Session 2025**

**Part Two: Authentication and Access Control System**

**Jenamari P. Bathan, SN: 8565727**

This program is written in Python 3.

1. To initialise the FileSystem and create a new user:
```bash
$ python3 FileSystem.py -i
```

Example:
```bash
$ python3 FileSystem.py -i
Username: Bob
Password: CSCI262assignment1!
Confirm Password: CSCI262assignment1!
User clearance (0 or 1 or 2 or 3): 1
User Bob created successfully.
```

This will create, or append to:
- salt.txt
- shadow.txt

2. To run the FileSystem normally, and be able to do login and file operations:
```python
$ python3 FileSystem.py
```

Example: 
operations:
```python
$ python3 FileSystem.py
Username: Bob
Password: CSCI262assignment1!
Authentication for Bob complete.
The clearance for Bob is 1.
Options: (C)reate, (A)ppend, (R)ead, (W)rite, (L)ist, (S)ave or (E)xit.
```
## Reduction  Implementation Notes
- User Authentication is based on the traditional salt/shadow model.
- Users are created using a salt/hash/shadow system:
    - `salt.txt` stores the username and randomised 8-digit salt
    - `shadow.txt` stores the username, hashed password+salt, and security clearance
- Passwords must meet minimum strength requirements (length, uppercase, lowercase, digit, special character).
- Authentication is done by recomputing the salted hash and comparing it against shadow.txt.
- The internal file system allows creating, reading, writing, appending, listing, and saving files.
- Access is controlled according to the Bell–LaPadula model:
    - Users can only read files at or below their clearance
    - Users can only write/append files at or above their clearance
- Files are stored in memory and saved to Files.store for persistence.
- The program always reports a test MD5 hash: MD5("This is a test") at startup.

## CAPA Compatibility
- The program has been tested with Python 3 on CAPA.
- Ensure that the following files are present in the working directory:
  - FileSystem.py
  - salt.txt (initially empty)
  - shadow.txt (initially empty)
- The program does not rely on any external libraries other than the Python standard library.

## Demonstration
<img width="539" height="130" alt="1" src="https://github.com/user-attachments/assets/11ee4209-113e-40f8-a402-c84b225d74e2" />
<img width="563" height="417" alt="2" src="https://github.com/user-attachments/assets/1ef40111-69e8-41bb-aae8-a222e4ff0f73" />
<img width="563" height="251" alt="3" src="https://github.com/user-attachments/assets/75b21124-ceaf-4730-ab13-4459794a5c05" />



