import tarfile
from tkinter.filedialog import askdirectory
import tkinter as tk
from tkinter import ttk
import os
import shutil
import threading
import pandas as pd
import re
import json
import google
from tkinter.messagebox import showwarning, showinfo

from utils.check_requirements import check_requirements

requirements_checked = check_requirements()
if requirements_checked == "bad_credentials":
    exit()

while requirements_checked == "not_internet":
    showwarning("Internet is disconnected", "The program is requiering internet connection, please check your internet connection and try again.")

from utils.gcp_utils import *


v3_v4_dir_entry = None
bacteria_data_entry = None
status_label = None
progress_var = None
percentage_label = None
select_v3_v4_dir_button = None
select_bacteria_data_button = None
submit_button = None



def upload_chatbot_data():
    v3_v4_dir = v3_v4_dir_entry.get()
    bacteria_dir = bacteria_data_entry.get()
    if not v3_v4_dir or not bacteria_dir:
        return
    
    select_v3_v4_dir_button.config(state=tk.DISABLED)
    select_bacteria_data_button.config(state=tk.DISABLED)
    submit_button.config(state=tk.DISABLED)
    bacteria_data_entry.config(state=tk.DISABLED)
    v3_v4_dir_entry.config(state=tk.DISABLED)

    os.makedirs("temp/v3_v4_data", exist_ok=True)

    # Extract the v3-v4 data
    status_label.config(text="Extracting v3-v4 data and copying...")
    total_files = 0
    progress_counter = 0
    for filename in os.listdir(v3_v4_dir):
        with tarfile.open(f"{v3_v4_dir}/{filename}") as tar:
            total_files += len(tar.getmembers())
    for filename in os.listdir(v3_v4_dir):
        with tarfile.open(f"{v3_v4_dir}/{filename}") as tar:
            for member in tar.getmembers():
                if member.isfile() and "dbBact" in member.name:
                    tar2 = tar.extractfile(member)
                    with open(member.name.split('/')[-1], 'wb') as f:
                        f.write(tar2.read())
                    shutil.copy2(member.name.split('/')[-1], f"temp/v3_v4_data/{member.name.split('/')[-1]}")
                    os.remove(member.name.split('/')[-1])
                    progress_counter += 1
                    progress = (progress_counter / total_files) * 100
                    progress_var.set(progress)
                    percentage_label.config(text=(('%.2f' % progress) + "%"))


    status_label.config(text="Copying bacteria data...")
    os.makedirs("temp/bacteria_data")

    progress_counter = 0
    total_files = sum([1 for _ in os.listdir(bacteria_dir)])
    for file in os.listdir(bacteria_dir):
        shutil.copy2(os.path.join(bacteria_dir, file), f"temp/bacteria_data/{file}")
        progress_counter += 1
        progress = (progress_counter / total_files) * 100
        progress_var.set(progress)
        percentage_label.config(text=(('%.2f' % progress) + "%"))

    
    # Organize sequences
    try:
        bacterias_data = read_data_from_cloud()
    except google.api_core.exceptions.NotFound:
        bacterias_data = {}
    status_label.config(text="Organizing sequences...")
    progress_counter = 0
    total_files = sum([1 for _ in os.listdir("temp/v3_v4_data")])
    for file in os.listdir("temp/v3_v4_data"):
        with open(f"temp/v3_v4_data/{file}", 'r') as f_fasta:
            fasta_content = f_fasta.readlines()
            for line in fasta_content:
                if line.startswith(">"):
                    try:
                        bacteria_id = str(line.replace('>', '').split(" ")[0].split(".")[0])
                    except ValueError:
                        print(f"ERROR: {file} has a bad entry.")
                    if bacteria_id not in bacterias_data.keys():
                        bacterias_data.setdefault(bacteria_id, {"sequences": [''], "kit_id": [], "Kingdom": "__", "Phylum": "__", "Class": "__", "Order": "__", "Family": "__", "Genus": "__", "Species": "__"})
                    else:
                        bacterias_data[bacteria_id]["sequences"].append('')
                else:
                    bacterias_data[bacteria_id]["sequences"][-1] += line.strip("\n")
        progress_counter += 1
        progress = (progress_counter / total_files) * 100
        progress_var.set(progress)
        percentage_label.config(text=(('%.2f' % progress) + "%"))
    

    status_label.config(text="Clearing duplicates...")
    total_records = len(bacterias_data.keys())
    progress_counter = 0
    progrss = (progress_counter / total_records) * 100
    progress_var.set(progress)
    percentage_label.config(text=(('%.2f ' % progrss) + '%'))
    for bacteria_id, data in bacterias_data.items():
        data["sequences"] = list(set(data["sequences"]))
        data["kit_id"] = list(set(data["kit_id"]))
        progress_counter += 1
        progress = (progress_counter / total_records) * 100
        progress_var.set(progress)
        percentage_label.config(text=(('%.2f ' % progress) + '%'))
    
    
    status_label.config(text="Merging data...")
    total_files = sum([1 for _ in os.listdir("temp/bacteria_data")])
    progress_counter = 0
    progress = (progress_counter / total_files) * 100
    progress_var.set(progress)
    percentage_label.config(text=(('%.2f ' % progress) + "%"))
    for file in os.listdir("temp/bacteria_data"):
        df = pd.read_csv(f"temp/bacteria_data/{file}")

        match = re.search(r'^S(\d+)_(Fr|R|S|F|L)(.*)', file)
        
        if not match:
            progress_counter += 1
            progress = (progress_counter / total_files)
            progress_var.set(progress)
            percentage_label.config(text=(('%.2f ' % progress) + '%'))
            continue

        kit_id = match.group(1)

        for index, row in df.iterrows():
            bacteria_id = str(row["id"])
            if bacteria_id in bacterias_data.keys():
                taxonomy = row["taxon"]
                if taxonomy == "No_Taxonomy":
                    continue
                taxonomy = ' '.join(taxonomy.split(' ')[1:]).split(';')
                bacterias_data[bacteria_id]["kit_id"].append(int(kit_id))
                try:
                    bacterias_data[bacteria_id]["Kingdom"] = taxonomy[0]
                except IndexError:
                    bacterias_data[bacteria_id]["Kingdom"] = "__"

                try:
                    bacterias_data[bacteria_id]["Phylum"] = taxonomy[1]
                except IndexError:
                    bacterias_data[bacteria_id]["Phylum"] = "__"

                try:
                    bacterias_data[bacteria_id]["Class"] = taxonomy[2]
                except IndexError:
                    bacterias_data[bacteria_id]["Class"] = "__"

                try:
                    bacterias_data[bacteria_id]["Order"] = taxonomy[3]
                except IndexError:
                    bacterias_data[bacteria_id]["Order"] = "__"

                try:
                    bacterias_data[bacteria_id]["Family"] = taxonomy[4]
                except IndexError:
                    bacterias_data[bacteria_id]["Family"] = "__"

                try:
                    bacterias_data[bacteria_id]["Genus"] = taxonomy[5]
                except IndexError:
                    bacterias_data[bacteria_id]["Genus"] = "__"

                try:
                    bacterias_data[bacteria_id]["Species"] = taxonomy[6]
                except IndexError:
                    bacterias_data[bacteria_id]["Species"] = "__"
        progress_counter += 1
        progress = (progress_counter / total_files) * 100
        progress_var.set(progress)
        percentage_label.config(text=(('%.2f' % progress) + "%"))

    with open("data.json", "w") as f:
        json.dump(bacterias_data, f)
    
    try:
        remove_data_from_cloud()
    except google.api_core.exceptions.NotFound:
        pass

    upload_data_to_cloud()

    os.remove("data.json")
    shutil.rmtree("temp")

    showinfo("Data has been saved in the cloud", "The data has been uploaded to the cloud and the chatbot knowladge updated.")

    select_v3_v4_dir_button.config(state=tk.NORMAL)
    select_bacteria_data_button.config(state=tk.NORMAL)
    submit_button.config(state=tk.NORMAL)
    bacteria_data_entry.config(state=tk.NORMAL)
    v3_v4_dir_entry.config(state=tk.NORMAL)
    status_label.config(text="")
    percentage_label.config(text="0.00 %")
    progress_var.set(0.0)

def select_dir(entry):
    # Ask for a directory and pasting the path in the field:
    dir_path = askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, dir_path)

def start_processing():
    threading.Thread(target=upload_chatbot_data).start()

def main():
    global v3_v4_dir_entry, bacteria_data_entry, status_label, progress_var, percentage_label, select_v3_v4_dir_button, select_bacteria_data_button, submit_button

    root = tk.Tk()
    root.title("Microbiome Chat Data Preperation")
    root.config(background="#dcdad5")
    icon = tk.PhotoImage(file="./static/icons/plant.ico")
    root.iconphoto(False, icon)

    # Set the window side to full screen
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

    root.state('zoomed')

    # Create a style
    style = ttk.Style()
    style.theme_use("clam")

    # Create a title for the application
    title_label = ttk.Label(root, text='Upload ChatBot Data', font=('Helvetica', 16, 'bold'), background="#dcdad5")
    title_label.pack(pady=10)

    # Create a label widget for the directory entry
    v3_v4_dir_label = ttk.Label(root, text='Select a directory of the v3-v4 data:', font=('Helvetica', 14), background="#dcdad5")
    v3_v4_dir_label.pack(pady=10)

    # Create an entry widget to display the selected directory path
    v3_v4_dir_entry = ttk.Entry(root, width=40, font=('Helvetica', 12))
    v3_v4_dir_entry.pack(pady=10)

    # Create a button to select a directory
    select_v3_v4_dir_button = tk.Button(root, text='Browse', command=lambda: select_dir(v3_v4_dir_entry), background='#007acc', fg='white',
                              font=('Helvetica', 12))
    select_v3_v4_dir_button.pack(pady=10)

    bacteria_data_label = ttk.Label(root, text='Select a bacteria data folder:', font=('Helvetica', 14), background="#dcdad5")
    bacteria_data_label.pack(pady=10)

    # Create an entry widget to display the selected file path
    bacteria_data_entry = ttk.Entry(root, width=40, font=('Helvetica', 12))
    bacteria_data_entry.pack(pady=10)

    # Create a button to select a file
    select_bacteria_data_button = tk.Button(root, text='Browse', command=lambda: select_dir(bacteria_data_entry), background='#007acc', fg='white', font=('Helvetica', 12))
    select_bacteria_data_button.pack(pady=10)


    # Create Submit button
    submit_button = tk.Button(root, text='Submit', command=start_processing, background='#4CAF50', fg='white',
                              font=('Helvetica', 12))
    submit_button.pack(pady=10)

    # Create a progress bar
    progress_var = tk.DoubleVar()
    progress_bar = ttk.Progressbar(root, length=300, variable=progress_var, mode='determinate')
    progress_bar.pack(pady=10)

    # Create a label to display the progress percentage
    percentage_label = ttk.Label(root, text='0%', font=('Helvetica', 12), background="#dcdad5")
    percentage_label.pack()

    # Create a label to display the status message
    status_label = ttk.Label(root, text='', font=('Helvetica', 12), background="#dcdad5")
    status_label.pack()

    root.mainloop()

if __name__ == '__main__':
    main()