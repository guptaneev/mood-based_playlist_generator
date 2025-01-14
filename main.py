import customtkinter as ctk
import tkinter as tk
import json
import random
from tkinter import messagebox, filedialog


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mood-Based Playlist Generator")
        self.geometry("800x600")  # Larger size for better layout
        ctk.set_appearance_mode("dark")  # Options: "light", "dark", "system"
        ctk.set_default_color_theme("green")  # Choose between "blue", "dark-blue", "green"

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


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(fg_color="gray25")  # Background color

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Mood-Based Playlist Generator",
            font=ctk.CTkFont(size=36, weight="bold"),
        )
        title_label.pack(pady=40)

        # Start Button
        start_button = ctk.CTkButton(
            self,
            text="Start",
            font=ctk.CTkFont(size=20, weight="bold"),
            command=lambda: controller.show_frame("GeneratorPage"),
        )
        start_button.pack(pady=20)


class GeneratorPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Generate Your Playlist",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title_label.pack(pady=20)

        # Mood Selection
        mood_label = ctk.CTkLabel(
            self,
            text="Select Your Mood",
            font=ctk.CTkFont(size=18),
        )
        mood_label.pack(pady=10)

        self.mood_var = ctk.StringVar(value="Happy")
        mood_options = ["Happy", "Sad", "Relaxed", "Energetic"]
        mood_dropdown = ctk.CTkOptionMenu(
            self,
            variable=self.mood_var,
            values=mood_options,
            font=ctk.CTkFont(size=14),
        )
        mood_dropdown.pack(pady=15)

        # Generate Playlist Button
        generate_button = ctk.CTkButton(
            self,
            text="Generate Playlist",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.generate_playlist,
        )
        generate_button.pack(pady=20)

        # Playlist Display
        self.playlist_textbox = ctk.CTkTextbox(self, height=200, width=400)
        self.playlist_textbox.configure(state="disabled")  # Initially read-only
        self.playlist_textbox.pack(pady=15)

        # Save Playlist Button
        save_button = ctk.CTkButton(
            self,
            text="Save Playlist",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.save_playlist,
        )
        save_button.pack(pady=10)

        # Back Button
        back_button = ctk.CTkButton(
            self,
            text="Back to Home",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: controller.show_frame("HomePage"),
        )
        back_button.pack(pady=10)

    def generate_playlist(self):
        mood = self.mood_var.get()
        try:
            with open("songs.json", "r") as f:
                song_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Unable to load songs.json file.")
            return

        playlist = song_data.get(mood, [])
        if not playlist:
            self.update_playlist_display("No songs found for the selected mood.")
            return

        playlist = random.sample(playlist, min(10, len(playlist)))
        self.update_playlist_display(
            f"{mood} Playlist:\n" +
            "\n".join(f"{song['song']} by {song['artist']}" for song in playlist)
        )

    def save_playlist(self):
        if not self.playlist_textbox.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "No playlist to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "w") as file:
            file.write(self.playlist_textbox.get("1.0", tk.END).strip())

        messagebox.showinfo("Success", f"Playlist saved to {file_path}")

    def update_playlist_display(self, text):
        self.playlist_textbox.configure(state="normal")
        self.playlist_textbox.delete("1.0", tk.END)
        self.playlist_textbox.insert(tk.END, text)
        self.playlist_textbox.configure(state="disabled")


class TutorialPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Title
        label = ctk.CTkLabel(
            self,
            text="How to Use the App",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        label.pack(pady=20)

        # Instructions
        instructions = (
            "1. Select a mood and generate a playlist.\n"
            "2. Click 'Regenerate Playlist' for more options.\n"
            "3. Save your playlist if desired.\n"
            "4. Go back to Home anytime."
        )
        instruction_label = ctk.CTkLabel(
            self,
            text=instructions,
            font=ctk.CTkFont(size=16),
            wraplength=600,
        )
        instruction_label.pack(pady=20)

        # Back Button
        back_button = ctk.CTkButton(
            self,
            text="Back to Home",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: controller.show_frame("HomePage"),
        )
        back_button.pack(pady=10)


if __name__ == "__main__":
    app = App()
    app.mainloop()