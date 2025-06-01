# Facial Attendance System

A Python-based facial recognition attendance system that uses `face_recognition` and OpenCV to detect and recognize faces, mark attendance, and provide text-to-speech feedback. The system allows users to enroll new faces, take attendance, and store records in CSV files.

## Features
- **Face Enrollment**: Register new users by capturing their face via webcam and saving it with their name and roll number.
- **Attendance Marking**: Automatically detect and recognize faces in a live video feed, marking attendance in a daily CSV file.
- **Text-to-Speech Feedback**: Uses `pyttsx3` to provide voice feedback for actions like enrollment, attendance marking, and system navigation.
- **User-Friendly Interface**: A simple command-line menu with Tkinter dialogs for user input.
- **Real-Time Face Detection**: Displays recognized faces with names and roll numbers on the video feed.

## Prerequisites
- **Python**: Version 3.10 or 3.11 (Python 3.13 is not supported due to compatibility issues with `face_recognition`).
- **Operating System**: Tested on Windows 10/11. Should work on Linux and macOS with minor adjustments.
- **Webcam**: A working webcam is required for face enrollment and attendance.
- **Dependencies**: See the [Dependencies](#dependencies) section for required Python packages.

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/facial-attendance-system.git
cd facial-attendance-system
```

### 2. Set Up Python and Virtual Environment
Install Python 3.10 if not already installed:
- Download from [python.org](https://www.python.org/downloads/release/python-31013/).
- During installation, check "Add Python to PATH".

Create and activate a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # On Windows
# source .venv/bin/activate  # On Linux/macOS
```

### 3. Install Dependencies
Install the required Python packages:
```bash
pip install --upgrade pip
pip install face_recognition opencv-python numpy pandas pyttsx3
```

**Note on `dlib` Installation (Required by `face_recognition`)**:
- On Windows, `dlib` may fail to install due to compilation requirements. Use a prebuilt wheel:
  ```bash
  pip install dlib-19.24.2-cp310-cp310-win_amd64.whl
  ```
  Download the wheel for your Python version from a trusted source like PyPI or https://github.com/ageitgey/face_recognition#installing-on-windows.

**Fallback for `face_recognition_models`**:
If `face_recognition` does not automatically install its models, run:
```bash
pip install git+https://github.com/ageitgey/face_recognition_models
```

### 4. Verify Installation
Test that all packages are installed:
```bash
python -c "import face_recognition, cv2, numpy, pandas, pyttsx3; print('All packages imported successfully')"
```

## Usage

### 1. Prepare the Directory Structure
The script automatically creates the following directories if they don’t exist:
- `known_faces/`: Store images of known faces (e.g., `Rakib_101.jpg`).
- `attendance_records/`: Store attendance CSV files (e.g., `attendance_2025-06-01.csv`).

### 2. Run the Script
```bash
python attendance_system.py
```

### 3. Navigate the Menu
- **Enroll New Face (Option 1)**: Enter a name and roll number, then press 'q' to capture your face via webcam.
- **Start Attendance (Option 2)**:
  - The system will open your webcam and start detecting faces.
  - Recognized faces will have their attendance marked in a CSV file.
  - Press 'e' to enroll a new face during attendance, or 'q' to quit.
- **Exit (Option 3)**: Exit the program.

### 4. Attendance Records
- Attendance is recorded in `attendance_records/attendance_YYYY-MM-DD.csv` with columns: `Name`, `Roll`, and `Time`.
- The system ensures duplicate attendance entries are not recorded for the same person in a session.

## Dependencies
- `face_recognition`: For face detection and recognition.
- `opencv-python`: For webcam access and video processing.
- `numpy`: For numerical operations.
- `pandas`: For handling attendance records in CSV format.
- `pyttsx3`: For text-to-speech feedback.
- `tkinter`: For GUI dialogs (included with Python).

## Troubleshooting

### Common Issues
1. **Error: Could not find platform independent libraries <prefix>**:
   - Ensure `face_recognition_models` is installed:
     ```bash
     pip install git+https://github.com/ageitgey/face_recognition_models
     ```
2. **Error: Failed to install `dlib`**:
   - Use a prebuilt wheel or install Visual Studio Build Tools with C++ workload.
3. **No Sound from `pyttsx3`**:
   - Ensure your system has working audio drivers.
   - Test with a simple script:
     ```python
     import pyttsx3
     engine = pyttsx3.init()
     engine.say("Hello, world!")
     engine.runAndWait()
     ```
4. **Webcam Not Working**:
   - Ensure your webcam is connected and not in use by another application.
   - Test with:
     ```python
     import cv2
     cap = cv2.VideoCapture(0)
     print(cap.isOpened())
     ```

### Performance Tips
- The `face_recognition` library can be slow with many faces. Process fewer frames by adjusting the `process_this_frame` logic in `take_attendance`.
- Lower the webcam resolution if performance is an issue.

## Contributing
Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. For major changes, open an issue first to discuss your ideas.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with [face_recognition](https://github.com/ageitgey/face_recognition) by Adam Geitgey.
- Uses [OpenCV](https://opencv.org/) for video processing.
- Text-to-speech powered by [pyttsx3](https://github.com/nateshmbhat/pyttsx3).