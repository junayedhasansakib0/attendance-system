import cv2
import face_recognition
import numpy as np
import os
import pandas as pd
import time
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
import pyttsx3

# Initialize TTS engine
engine = None
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Set speech rate
    # Optional: Set voice ID (uncomment and customize if specific voice is needed)
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voices[0].id)
    print("Text-to-Speech engine initialized.")
except Exception as e:
    print(f"Error initializing Text-to-Speech engine: {e}")
    engine = None


# Custom speak function
def speak(text):
    if engine:
        engine.say(text)
        engine.runAndWait()
    else:
        print(f"TTS Not Active: {text}")
    print(text)  # Keep print to console as fallback or for visibility


# Global variables
known_face_encodings = []
known_face_names = []
known_face_rolls = []
attendance_taken_today = set()


# Function to load known faces from 'known_faces' directory
def load_known_faces():
    global known_face_encodings, known_face_names, known_face_rolls
    known_face_encodings = []
    known_face_names = []
    known_face_rolls = []

    for filename in os.listdir("known_faces"):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            path = os.path.join("known_faces", filename)
            image = face_recognition.load_image_file(path)
            encodings = face_recognition.face_encodings(image)
            if encodings:
                face_encoding = encodings[0]
                known_face_encodings.append(face_encoding)
                # Extract name and roll from filename (e.g., Rakib_101.jpg)
                parts = os.path.splitext(filename)[0].split('_')
                if len(parts) >= 2:
                    name = parts[0]
                    roll = parts[1]
                else:
                    name = parts[0]
                    roll = "N/A"
                known_face_names.append(name)
                known_face_rolls.append(roll)
    speak(f"Loaded {len(known_face_encodings)} known faces.")


# Initially load known faces
load_known_faces()


# Function to enroll a new face
def enroll_new_face():
    root = tk.Tk()
    root.withdraw()  # Hide the main Tkinter window

    name = simpledialog.askstring("Enroll New Face", "Enter your Name:")
    if not name:
        messagebox.showinfo("Enrollment Cancelled", "Name cannot be empty. Enrollment cancelled.")
        return

    roll = simpledialog.askstring("Enroll New Face", "Enter your Roll Number:")
    if not roll:
        messagebox.showinfo("Enrollment Cancelled", "Roll Number cannot be empty. Enrollment cancelled.")
        return

    file_name = f"{name}_{roll}.jpg"
    save_path = os.path.join("known_faces", file_name)

    if os.path.exists(save_path):
        messagebox.showerror("Error",
                             "A face with this name and roll already exists. Please use a unique name/roll combination.")
        return

    messagebox.showinfo("Enrollment Ready", "Press 'q' to capture your face for enrollment.")
    speak("Enrollment ready. Please face the camera and press 'q' to capture your face.")

    video_capture = cv2.VideoCapture(0)  # 0 for default webcam

    while True:
        ret, frame = video_capture.read()
        if not ret:
            speak("Failed to grab camera frame.")
            break

        cv2.imshow('Enroll New Face - Press "q" to capture', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            face_locations = face_recognition.face_locations(frame)
            if face_locations:
                top, right, bottom, left = face_locations[0]
                face_image = frame[top:bottom, left:right]
                cv2.imwrite(save_path, face_image)
                messagebox.showinfo("Success", f"Face for {name} ({roll}) saved successfully!")
                speak(f"Face for {name}, roll {roll} saved successfully.")
                break
            else:
                messagebox.showwarning("No Face Detected", "No face detected. Please try again.")
                speak("No face detected. Please try again.")
                continue

    video_capture.release()
    cv2.destroyAllWindows()
    load_known_faces()  # Reload data after new face is added


# Function to mark attendance for a recognized person
def mark_attendance(name, roll):
    today = datetime.now().strftime("%Y-%m-%d")
    record_file = os.path.join("attendance_records", f"attendance_{today}.csv")

    current_time = datetime.now().strftime("%H:%M:%S")

    # Ensure attendance file exists
    if not os.path.exists(record_file):
        df = pd.DataFrame(columns=["Name", "Roll", "Time"])
        df.to_csv(record_file, index=False)

    # Check if attendance has already been taken for this person today
    if (name, roll) in attendance_taken_today:
        return

    df = pd.read_csv(record_file)
    new_record = pd.DataFrame([{"Name": name, "Roll": roll, "Time": current_time}])
    df = pd.concat([df, new_record], ignore_index=True)
    df.to_csv(record_file, index=False)
    attendance_taken_today.add((name, roll))
    speak(f"Attendance marked for {name}, roll {roll} at {current_time}.")


# NEW FUNCTION: Generate a summary report of present and absent students
def generate_attendance_summary():
    today = datetime.now().strftime("%Y-%m-%d")
    summary_file = os.path.join("attendance_records", f"summary_{today}.txt")

    present_students = attendance_taken_today
    absent_students = []

    # Determine who is absent
    for i in range(len(known_face_names)):
        name = known_face_names[i]
        roll = known_face_rolls[i]
        if (name, roll) not in present_students:
            absent_students.append((name, roll))

    # Sort for better readability
    present_list = sorted(list(present_students))
    absent_list = sorted(absent_students)

    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"--- Attendance Summary for {today} ---\n\n")

        f.write("--- PRESENT STUDENTS ---\n")
        if present_list:
            for name, roll in present_list:
                f.write(f"Name: {name}, Roll: {roll}\n")
        else:
            f.write("No students were marked present today.\n")

        f.write("\n--- ABSENT STUDENTS ---\n")
        if absent_list:
            for name, roll in absent_list:
                f.write(f"Name: {name}, Roll: {roll}\n")
        else:
            f.write("All known students were present today.\n")

    speak(f"Attendance summary report generated for {today}. Check {summary_file} for details.")
    print(f"Attendance summary report generated for {today} at {summary_file}")


# Function to start the attendance system
def take_attendance():
    global attendance_taken_today
    attendance_taken_today = set()  # Reset for a new day/session
    speak("Starting attendance system.")

    video_capture = cv2.VideoCapture(0)

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video_capture.read()
        if not ret:
            speak("Failed to grab camera frame. Exiting attendance system.")
            break

        # Process every other frame for better performance
        if process_this_frame:
            # Resize frame for faster face detection
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                roll = "Unknown"

                # Find the best match among known faces
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    roll = known_face_rolls[best_match_index]
                    mark_attendance(name, roll)

                face_names.append(f"{name} ({roll})")

        process_this_frame = not process_this_frame

        # Draw boxes and labels around detected faces
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video - Press "q" to quit, "e" to enroll new face', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            speak("Attendance system stopped. Generating summary report.")  # <--- Change here
            break
        elif key == ord('e'):
            speak("Enroll new face mode activated.")
            enroll_new_face()
            # Re-initialize camera after enrollment
            video_capture.release()
            cv2.destroyAllWindows()
            video_capture = cv2.VideoCapture(0)

    video_capture.release()
    cv2.destroyAllWindows()

    # NEW CALL: Generate summary report after attendance session ends
    generate_attendance_summary()

    speak("Attendance system session completed.")  # <--- Change here, updated message


# Main menu function
def main_menu():
    while True:
        speak("\n--- Attendance System Menu ---")
        speak("1. Enroll New Face")
        speak("2. Start Attendance")
        speak("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            speak("You chose to enroll a new face.")
            enroll_new_face()
        elif choice == '2':
            speak("You chose to start attendance.")
            take_attendance()
        elif choice == '3':
            speak("Exiting program. Goodbye!")
            break
        else:
            speak("Invalid choice. Please try again.")


# Entry point of the script
if __name__ == "__main__":
    # Ensure necessary folders exist
    if not os.path.exists("known_faces"):
        os.makedirs("known_faces")
    if not os.path.exists("attendance_records"):
        os.makedirs("attendance_records")

    main_menu()