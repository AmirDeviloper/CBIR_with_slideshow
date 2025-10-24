import tkinter as tk
from tkinter import filedialog, messagebox

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        messagebox.showinfo("Selected Directory", f"You selected: {directory}")

def select_image():
    image_file = filedialog.askopenfilename()
    if image_file:
        messagebox.showinfo("Selected Image", f"You selected: {image_file}")

def validate_number(value):
    if value.isdigit() or value == "":
        return True
    return False

def create_similar_slideshow():
    k = k_value.get()
    if k.isdigit() and int(k) > 0:
        messagebox.showinfo("Slideshow", f"Creating slideshow with {k} images.")
    else:
        messagebox.showerror("Error", "Please enter a valid number of images.")

root = tk.Tk()
root.title("Slideshow Creator")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

title_label = tk.Label(root, text="Welcome to Slideshow Creator", font=("Helvetica", 16, "bold"), bg="#f0f0f0", fg="#333")
title_label.pack(pady=10)

button1 = tk.Button(root, text="Select Directory", command=select_directory, bg="#4CAF50", fg="white", font=("Helvetica", 12), padx=10, pady=5)
button1.pack(pady=5)

button2 = tk.Button(root, text="Select Image", command=select_image, bg="#2196F3", fg="white", font=("Helvetica", 12), padx=10, pady=5)
button2.pack(pady=5)

label3 = tk.Label(root, text="K images you want:", font=("Helvetica", 12), bg="#f0f0f0", fg="#333")
label3.pack(pady=5)

validate_command = root.register(validate_number)
k_value = tk.Entry(root, validate="key", validatecommand=(validate_command, '%P'), font=("Helvetica", 12), width=5)
k_value.pack(pady=5)

button_final = tk.Button(root, text="Create Slideshow", command=create_similar_slideshow, bg="#FF5722", fg="white", font=("Helvetica", 12), padx=10, pady=5)
button_final.pack(pady=20)

root.mainloop()