# Lockjaw
Encrypts data into archives via facial recognition

# Overview
This program uses webcam video feed to register your face in its database, allowing you to encrypt files into an archive. You may use you face as a key to then decrypt your archives.

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

clear_database: empties face encodings, username, and password pickle files.

# Docs referenced
https://pypi.org/project/face-recognition/ 
https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py 
https://py7zr.readthedocs.io/en/latest/api.html

minizip used to encrypt zip folders with compress and uncompress
