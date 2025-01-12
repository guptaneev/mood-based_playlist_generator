import tkinter as tk
from tkinter import Tk, Frame, Label, Button, OptionMenu, StringVar, Text, Scrollbar, PhotoImage, messagebox, filedialog, DISABLED, NORMAL
import json
import random
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mood-Based Playlist Generator")
        self.geometry("600x400")
        
        # Store all frames in a dictionary
        self.frames = {}
        
        # Initialize all pages
        for PageClass in (HomePage, GeneratorPage, TutorialPage):
            frame = PageClass(parent=self, controller=self)
            self.frames[PageClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show the initial page (HomePage)
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        """Raise the frame with the given page name."""
        frame = self.frames[page_name]
        frame.tkraise()


# Home Page
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Set background color
        self.config(bg="#D33232")  # Updated red background

        # Configure grid layout for vertical alignment
        self.grid_rowconfigure([0, 1, 2], weight=1)  # For spacing
        self.grid_columnconfigure(0, weight=1)       # For left alignment
        self.grid_columnconfigure(1, weight=1)       # For button

        # Title labels in separate rows
        title_words = ["Mood-Based", "Playlist", "Generator"]
        for i, word in enumerate(title_words):
            label = tk.Label(
                self,
                text=word,
                font=("Arial", 36, "bold"),
                bg="#D33232",
                fg="black"
            )
            label.grid(row=i, column=0, sticky="w", padx=50)  # Align to left

        # Start button
        start_canvas = tk.Canvas(self, width=150, height=70, bg="#D33232", highlightthickness=0)
        start_button = start_canvas.create_oval(5, 5, 145, 65, fill="white", outline="black")
        start_text = start_canvas.create_text(75, 35, text="Start", font=("Arial", 18), fill="black")
        start_canvas.bind("<Button-1>", lambda event: controller.show_frame("GeneratorPage"))
        start_canvas.grid(row=1, column=1, sticky="e", padx=50)


class GeneratorPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Set background color
        self.config(bg="#D1E8E2")  # Soft pastel greenish-blue background

        # Title label
        label = tk.Label(
            self,
            text="Generate Your Playlist",
            font=("Helvetica", 28, "bold"),
            bg="#D1E8E2",
            fg="darkblue"
        )
        label.pack(pady=30)

        # Add "Tutorial" button in the top-right corner
        tutorial_button = tk.Button(
            self,
            text="Tutorial",
            font=("Helvetica", 12, "bold"),
            bg="#FFB347",  # Bright orange for emphasis
            fg="white",
            relief="flat",
            activebackground="#FFA07A",  # Light salmon for hover effect
            activeforeground="white",
            command=lambda: controller.show_frame("TutorialPage")
        )
        tutorial_button.place(x=500, y=15)  # Positioned at the top-right corner

        # Mood selection label
        mood_label = tk.Label(
            self,
            text="Select your mood:",
            font=("Helvetica", 16),
            bg="#D1E8E2",
            fg="black"
        )
        mood_label.pack(pady=10)

        # Mood dropdown menu
        self.mood_var = tk.StringVar(value="Happy")
        moods = ["Happy", "Sad", "Relaxed", "Energetic"]
        self.mood_menu = tk.OptionMenu(self, self.mood_var, *moods)
        self.mood_menu.config(
            font=("Helvetica", 14), 
            bg="white", 
            fg="black", 
            highlightthickness=1, 
            highlightbackground="darkblue"
        )
        self.mood_menu.pack(pady=15)

        # Generate button
        generate_button = tk.Button(
            self,
            text="Generate Playlist",
            font=("Helvetica", 16, "bold"),
            bg="#4CAF50",  # Green
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            activebackground="#81C784",  # Lighter green for hover effect
            activeforeground="white",
            command=self.generate_playlist
        )
        generate_button.pack(pady=20)

        # Regenerate button
        regenerate_button = tk.Button(
            self,
            text="Regenerate Playlist",
            font=("Helvetica", 16, "bold"),
            bg="#2196F3",  # Blue
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            activebackground="#64B5F6",  # Lighter blue for hover effect
            activeforeground="white",
            command=self.regenerate_playlist
        )
        regenerate_button.pack(pady=15)

        # Playlist display area in a scrollable text box
        self.playlist_frame = tk.Frame(self, bg="#D1E8E2")
        self.playlist_frame.pack(pady=20)
        self.playlist_label = tk.Text(
            self.playlist_frame,
            font=("Helvetica", 14),
            bg="#FFFFFF",
            fg="black",
            height=10,
            width=50,
            wrap="word",
            state="disabled",
            borderwidth=1,
            relief="groove"
        )
        self.playlist_label.pack(side="left", fill="y", padx=5)

        scrollbar = tk.Scrollbar(self.playlist_frame, command=self.playlist_label.yview)
        scrollbar.pack(side="right", fill="y")
        self.playlist_label["yscrollcommand"] = scrollbar.set

        # Save button
        save_button = tk.Button(
            self,
            text="Save Playlist",
            font=("Helvetica", 16, "bold"),
            bg="#FF5722",  # Red-orange
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            activebackground="#FF7043",  # Lighter red-orange for hover
            activeforeground="white",
            command=self.save_playlist
        )
        save_button.pack(pady=10)

        # Back button
        back_button = tk.Button(
            self,
            text="Back to Home",
            font=("Helvetica", 16, "bold"),
            bg="gray",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            activebackground="darkgray",
            activeforeground="white",
            command=lambda: controller.show_frame("HomePage")
        )
        back_button.pack(pady=10)

        # Initialize variables
        self.current_playlist = []  # To store the current playlist

    def generate_playlist(self):
        """Generate a playlist based on the selected mood."""
        mood = self.mood_var.get()
        with open("songs.json") as f:
            song_data = json.load(f)

        playlist = song_data.get(mood, [])
        if not playlist:
            self.update_playlist_display("No songs found for the selected mood.")
            return

        playlist = random.sample(playlist, min(10, len(playlist)))
        self.current_playlist = playlist
        playlist_text = f"Your '{mood}' Playlist:\n" + "\n".join(
            [f"{song['song']} by {song['artist']}" for song in playlist]
        )
        self.update_playlist_display(playlist_text)

        color_scheme = {
            "Happy": "#FF4B4B",
            "Sad": "#87CEEB",
            "Relaxed": "#F0E68C",
            "Energetic": "#FFA500"
        }
        self.config(bg=color_scheme.get(mood, "#D1E8E2"))

    def regenerate_playlist(self):
        """Regenerate the playlist with at least 50% different songs."""
        if len(self.current_playlist) < 10:
            messagebox.showerror("Error", "Not enough songs to regenerate a playlist with 50% difference.")
            return

        with open("songs.json") as f:
            song_data = json.load(f)

        mood = self.mood_var.get()
        playlist = song_data.get(mood, [])

        previous_songs = [song["song"] for song in self.current_playlist]
        available_songs = [song for song in playlist if song["song"] not in previous_songs]
        if len(available_songs) < len(self.current_playlist) // 2:
            messagebox.showerror("Error", "Not enough unique songs to create a playlist with 50% variation.")
            return

        new_playlist = random.sample(available_songs, len(self.current_playlist) // 2) + \
                       random.sample(self.current_playlist, len(self.current_playlist) // 2)
        random.shuffle(new_playlist)

        self.current_playlist = new_playlist
        playlist_text = f"Your regenerated '{mood}' Playlist:\n" + "\n".join(
            [f"{song['song']} by {song['artist']}" for song in new_playlist]
        )
        self.update_playlist_display(playlist_text)

    def save_playlist(self):
        """Save the current playlist as a text file."""
        if not self.current_playlist:
            messagebox.showerror("Error", "No playlist to save.")
            return

        file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "w") as f:
            for song in self.current_playlist:
                f.write(f"{song['song']} by {song['artist']}\n")

        messagebox.showinfo("Success", f"Playlist saved to {file_path}")

    def update_playlist_display(self, text):
        """Update the playlist display text box."""
        self.playlist_label.config(state="normal")
        self.playlist_label.delete(1.0, tk.END)
        self.playlist_label.insert(tk.END, text)
        self.playlist_label.config(state="disabled")


# Tutorial Page
class TutorialPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Set background color
        self.config(bg="#F0E68C")  # Light yellow background

        # Title label
        label = tk.Label(
            self,
            text="How to Use the App",
            font=("Arial", 24, "bold"),
            bg="#F0E68C",
            fg="black"
        )
        label.pack(pady=20)

        # Instructions
        tutorial_text = (
            "1. Select a mood and generate a playlist.\n"
            "2. You can regenerate a new playlist with a click on the 'Regenerate Playlist' button.\n"
            "3. You can save your playlist using the 'Save Playlist' button.\n"
            "4. If you are unsure, refer to this tutorial."
        )
        instructions = tk.Label(
            self,
            text=tutorial_text,
            font=("Arial", 14),
            bg="#F0E68C",
            fg="black",
            justify="left",
            wraplength=500
        )
        instructions.pack(pady=20)

        # Back button
        back_button = tk.Button(
            self,
            text="Back to Home",
            font=("Arial", 16),
            bg="white",
            fg="black",
            relief="flat",
            padx=20,
            pady=10,
            command=lambda: controller.show_frame("HomePage")
        )
        back_button.pack(pady=10)


# Main execution
if __name__ == "__main__":
    app = App()
    app.mainloop()