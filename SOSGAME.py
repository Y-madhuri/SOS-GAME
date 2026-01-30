import tkinter as tk
from tkinter import PhotoImage
import subprocess

def start_button_click():
    subprocess.Popen(["python","MENUBAR.py"])  # Call create_main_menu function from menubar3

root = tk.Tk()

root.title("SOS GAME")

# New image path
image_path = r"C:\Users\ymsma\OneDrive\Documents\Downloads\image (1).png"

try:
    # Open the image
    background_image = PhotoImage(file=image_path)

    # Create a label to hold the background image
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=2, y=2, relwidth=1, relheight=2)  # Fill the whole window

    # Load the existing image
    existing_image_path = r"C:\Users\ymsma\OneDrive\Documents\Downloads\sos image3.png"
    existing_image = PhotoImage(file=existing_image_path)
    zoomed_image=existing_image.zoom(1,1)
    

    # Create a canvas widget with the same size as the existing image
    canvas = tk.Canvas(root, width=zoomed_image.width(), height=zoomed_image.height())
    canvas.place(relx=0.5, rely=0.5, anchor="center")  # Center the canvas in the window

    # Place the existing image on the canvas
    image_item = canvas.create_image(5, 5, anchor="nw", image=existing_image)

    # Create the "SOS GAME" label
    sos_label = tk.Label(root, text="SOS GAME", font=("Wide Latin", 30), pady=10, fg="Magenta")
    sos_label.place(relx=0.5, rely=0.1, anchor="center")  # Position the label in the center and slightly above

    # Create a next button
    next_button = tk.Button(root, text="start", command=start_button_click)
    next_button.place(relx=0.5, rely=0.9, anchor="center")  # Position the button in the center and slightly below

except FileNotFoundError:
    print("Error: File not found at the specified path.")
except tk.TclError as e:
    print("Error loading image:", e)

root.mainloop()
