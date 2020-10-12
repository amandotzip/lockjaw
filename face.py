def clear_database():
    with open('face_encodings.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump([], f, pickle.HIGHEST_PROTOCOL)

    with open('face_names.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump([], f, pickle.HIGHEST_PROTOCOL)
    
    with open('passwords.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump([], f, pickle.HIGHEST_PROTOCOL)


import face_recognition
import cv2
import numpy as np
import secrets
import string
import pickle
import pyminizip


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.
print("   ///////\n  LOCKJAW \n ///////")


# clear_database()
# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

known_face_encodings = []
known_face_names = []
passwords = []

with open('face_encodings.pickle', 'rb') as f:
    known_face_encodings = pickle.load(f)

with open('face_names.pickle', 'rb') as f:
    known_face_names = pickle.load(f)

with open('passwords.pickle', 'rb') as f:
    passwords = pickle.load(f)


#Choose option to register your face or open encrypted files
option = input("Select an option below:\nRegister: \t\t1\nDecrypt archives: \t2\n")

if option == "1":
    username = input("Please enter a username\n")
    # Initialize some variables
    face_locations = []
    face_encodings = [] 
    face_names = []
    process_this_frame = True


    registered = False
    print("Scanning for your gorgeous face...")
    #As soon as the first face is found, you are registered and we will stop scanning video feed
    while not registered:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=.25, fy=.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                #will take the first face it sees, can restrict it to only allow 1 later
                #store in file of registered users
               
                
                #add to registered names and encodings 
                #append to lists, then update the pickle file
                known_face_encodings.append(face_encoding)
                known_face_names.append(username)

                with open('face_encodings.pickle', 'wb') as f:
                    # Pickle the 'data' dictionary using the highest protocol available.
                    pickle.dump(known_face_encodings, f, pickle.HIGHEST_PROTOCOL)

                with open('face_names.pickle', 'wb') as f:
                    # Pickle the 'data' dictionary using the highest protocol available.
                    pickle.dump(known_face_names, f, pickle.HIGHEST_PROTOCOL)


                #A face was found so add name into system, 
                # then declare registerd to stop looking at video
                registered = True


                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    
       
    print("Registration successful!")
    # going to have to make this more friendly than literall wrtiing a list
    src_files = input("Welcome " + username + ". Choose files to encrypt:\n").split(" ")
    archive_name = input("Choose a snazzy name for the archive:\n")

    src_paths = []

    for files in src_files:
        src_paths.append(archive_name)
    
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(2000))
    print("*************")
    print("Key generated")
    print("*************")
    print(password + "\n")
    passwords.append(password)
    with open('passwords.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(passwords, f, pickle.HIGHEST_PROTOCOL) 

    print("Compressing...")
    #minizip encryption
    compression_level = 5 # 1-9
    pyminizip.compress_multiple(src_files, src_paths, ".\\" + archive_name + ".zip", password, compression_level)

    print("Compressing and encryption successful!")



elif option == "2":
    # Initialize some variables
    face_locations = []
    face_encodings = [] 
    face_names = []
    process_this_frame = True

    current_person = ""
    current_password = ""
    userfound = False
    print("Scanning for your gorgeous face...")

    #As soon as the first face is found, you are registered and we will stop scanning video feed
    while not userfound:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            
            #face_encodings = all faces in current frame
            face_names = []
            for face_encoding in face_encodings:
                
                
                #will take the first face it sees, can restrict it to only allow 1 later
                #store in file of registered users

                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    current_person = name

                    current_password = passwords[best_match_index]
                    userfound = True

                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()


    target = input("Welcome Master " + current_person +". What would you like to decrypt?\n")
    print("Uncompressing...")
    pyminizip.uncompress(target, current_password, None, 0)
    print("Uncompressing and decryption successful!")