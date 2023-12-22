# Chatbot Microbiome data preparation

This project was built to upload data to Google Cloud so the chatbot knowledge will be updated.

## Setup for production
Download the latest release, and extract the files from the zip folder to a new folder. enter the folder and run "chat microbiome data preperation.exe" using double click

## Updating the program
Delete the current project folder from your PC and download the latest release.

## IMPORTANT
If you have downloaded a release zip folder, don't delete/move/rename any files. deleting/renaming/moving files can crash the program.

## Tip
Create a shortcut on your desktop to the "chat microbiome data preperation.exe" file

## Setup for development

### Navigate to the folder you want to download
```bash
cd MY_DIRECTORY
```
replace ```MY_DIRECTORY``` with a real path

### Download the project
```bash
git clone https://github.com/matan15/chat-microbiome-data-preperation
```

### Enter the project folder
```bash
cd chat-microbiome-data-preperation
```

### Create an environment and Activate
```bash
python -m venv env && cd env/Scripts && activate && cd ../..
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the project
```bash
python main.py
```