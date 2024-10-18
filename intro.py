#Crea scena iniziale

import tkinter as tk

def show_intro():
   # Create the intro window
    intro_root = tk.Tk()
    intro_root.title("Intro")
    
    # Set the window size
    window_width = 500
    window_height = 300

    # Get screen width and height to center the window
    screen_width = intro_root.winfo_screenwidth()
    screen_height = intro_root.winfo_screenheight()

    # Calculate x and y coordinates for the window
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))

    # Set window geometry (position and size)
    intro_root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    # Disable resizing of the window
    intro_root.resizable(False, False)

    # Set background color to black
    intro_root.configure(bg='black')

    # Create the label with white text, centered in the window
    label = tk.Label(intro_root, text="SnapCore (A Ktech Program) \n - \n All the rights belong to the coder, \n Kujto Fetahi", font=("Arial", 20), fg="white", bg="black")
    label.pack(expand=True)

    # Automatically close the intro window after 5 seconds
    intro_root.after(5000, intro_root.destroy)

    # Start the intro window loop
    intro_root.mainloop()