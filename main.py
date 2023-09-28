from PIL import Image
import imagehash
import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def get_image_hash(image_path):
    with Image.open(image_path) as img:
        return imagehash.average_hash(img)

def find_duplicates(directory):
    hash_dict = {}
    duplicates = []

    for filename in os.listdir(directory):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            file_path = os.path.join(directory, filename)
            file_size = os.path.getsize(file_path)
            image_hash = get_image_hash(file_path)
            if (file_size, image_hash) in hash_dict:
                duplicates.append((filename, hash_dict[(file_size, image_hash)]))
            else:
                hash_dict[(file_size, image_hash)] = filename

    return duplicates

def remove_duplicates(duplicates, directory):
    for duplicate in duplicates:
        duplicate_path = os.path.join(directory, duplicate[0])
        os.remove(duplicate_path)

def count_duplicates(directory):
    duplicates = find_duplicates(directory)
    return len(duplicates)

def show_duplicates_graph(directory):
    duplicates = find_duplicates(directory)
    hashes = [hash(int(d[1], 16)) for d in duplicates]

    plt.hist(hashes, bins=20, alpha=0.7, color='blue', edgecolor='black')
    plt.title('Duplicate Image Distribution')
    plt.xlabel('Image Hashes')
    plt.ylabel('Frequency')
    plt.show()

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        # Remove duplicates using image hash
        count = count_duplicates(folder_path)
        if count > 0:
            duplicates = find_duplicates(folder_path)
            remove_duplicates(duplicates, folder_path)
            print(f"{count} duplicates removed.")
        else:
            print("No duplicates found.")
        
        # Show Matplotlib graph
        show_duplicates_graph(folder_path)

# Create GUI window
root = tk.Tk()
root.title("Duplicate Image Checker")

# Create button to select folder
button = tk.Button(root, text="Select Folder", command=select_folder)
button.pack(pady=20)

# Start GUI loop
root.mainloop()
