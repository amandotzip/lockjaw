# Lockjaw
Encrypts data into archives via facial recognition

# Overview
This program uses webcam video feed to register your face in its database, allowing you to encrypt files into an archive. You may use you face as a key to then decrypt your archives.

# Requirements
Runs on Python 3

pip install the folowing
- face_recognition (NOTE: requires Visual Studio C++)
- opencv-python
- numpy
- pyminizip
# How to start
```
py face.py
```
# Register
Register your face with option 1, your face will be scanned, a password will be generated alongside the scan, and you may encrypt files.

List out files you'd like to archive and encrypt For example

```
Choose files to encrypt:
images\potter.jpg images\granger.jpg images\weasley.jpg
```
Choose a name for the archive
```
Choose a snazzy name for the archive: 
yearbook
```

It is now stored in an encrypted archive.

# Accessing encrypted archives/decrypting
Select option 2 to decrypt archives]
Your face will now be scanned, and be matched with the database of stored face encodings. 

Once a registered user has their face scanned, they will be welcomed and may select to decrypt their files.


```
Scanning for your gorgeous face...
Welcome Master Dumbledore. What would you like to decrypt?
yearbook.zip
Uncompressing...
Uncompressing and decryption successful!
```

If you see the above success text, you should see the archive contents unzipped.
# Design
All face encodings, usernames, and passwords are stored in pickle files. Pickle files are able to store objects for use in another run of the program.

## clear_database() 
empties face encodings, username, and password pickle files.

## Face encodings
These are the meat of what is returned from the face recognition and openCV libraries. For our purposes, it merely is a face.

## Passwords
The password generated along with a face is 1000 characters with letters, numbers, caps, and special characters. A brute force would take several millenia to crack it. That said, the pickle file is not a safe means to save passwords. It would make sense to generate a one way hash on a smaller password, then compare the hash with the stored database one way hash. This is how most passwords are stored.

# Docs referenced
https://pypi.org/project/face-recognition/ 
https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py 
https://py7zr.readthedocs.io/en/latest/api.html

minizip used to encrypt zip folders with compress and uncompress
