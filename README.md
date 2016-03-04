# Course-Page-Downloader (beta)
Downloads contents of VIT Academics Course Page and organizes them nicely

## Features
1. Auto Captca Entry -- thanks to Karthik Balakrishnan
2. All details are cached for later use
3. Automatically organizes each course into a folder as `[Course-Code]-[Faculty-Name]`.
4. Strips off the redundant content in each file -- thanks to Lalit Umbarkar
5. Automaticaly resumes from the previous downloaded content. Only latest uploaded material is downloaded

## Working
![cmd-prompt](https://raw.githubusercontent.com/kp96/Course-Page-Downloader/master/screenshots/cmd.PNG?token=AIj1ZtvibbI1CwGPtnB3Y9aCx9Nr7s9Fks5W4l3dwA%3D%3D)
![directories](https://raw.githubusercontent.com/kp96/Course-Page-Downloader/master/screenshots/direct.PNG?token=AIj1Zm0-faKz3OYlNB4rrjPrr5e6Ue7Rks5W4l5cwA%3D%3D)
![files](https://raw.githubusercontent.com/kp96/Course-Page-Downloader/master/screenshots/contents.PNG?token=AIj1Zhms694lA94W-3HvrjPzupm6egdgks5W4l52wA%3D%3D)

## Setup
1. Clone the repository `git clone https://github.com/kp96/Course-Page-Downloader.git`
2. Download and Install `python 2.7`
3. `cd Course-Page-Downloader`
4. `pip install -r requirements.txt`
5. `python main.py`

To clear cached data remove `course.db` file.
