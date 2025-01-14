import json
import random
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk


# App Configuration
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Mood-Based Playlist Generator")
        self.geometry("600x400")
        self.state("zoomed")  # Start in fullscreen mode
        self.configure(fg_color="#D33232")  # Background color of the app
        
        # Configure grid weights for the main window
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
                
        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, sticky="nsew")
                
        # Navigate to HomePage initially
        self.frames = {}
        for Page in (HomePage, GeneratorPage, TutorialPage):
            frame = Page(parent=self, controller=self)
            self.frames[Page.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

# Home Page
class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#D33232")  # Background color for the Home Page

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)  # Title Column
        self.grid_columnconfigure(1, weight=1)  # Button Column
        self.grid_rowconfigure(0, weight=1)  # Align items vertically

        # Frame for the vertical text title
        text_frame = ctk.CTkFrame(self, fg_color="#D33232")
        text_frame.grid(row=0, column=0, sticky="nsew", padx=20)

        # Title text as three separate rows
        title1 = ctk.CTkLabel(
            text_frame,
            text="Mood-Based",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="black",
        )
        title1.pack(anchor="w")

        title2 = ctk.CTkLabel(
            text_frame,
            text="Playlist",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="black",
        )
        title2.pack(anchor="w")

        title3 = ctk.CTkLabel(
            text_frame,
            text="Generator",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="black",
        )
        title3.pack(anchor="w")

        # Oval Start Button
        start_button = ctk.CTkButton(
            self,
            text="Start",
            font=ctk.CTkFont(size=18),
            fg_color="white",
            text_color="black",
            corner_radius=35,  # Oval shape
            command=lambda: controller.show_frame("GeneratorPage"),
            width=120,
            height=60,
        )
        start_button.grid(row=0, column=1, sticky="n", padx=(10, 50))


class GeneratorPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#D33232")  # Background color for Generator Page

        # Configure grid layout for fullscreen
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # (1) Mood Selection Dropdown
        mood_label = ctk.CTkLabel(
            self,
            text="I'm feeling...",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white",
        )
        mood_label.grid(row=0, column=0, sticky="e", padx=(0, 15), pady=(20, 0))

        self.mood_var = ctk.StringVar(value="Happy")
        mood_options = ["Happy", "Sad", "Relaxed", "Energetic"]
        mood_dropdown = ctk.CTkOptionMenu(
            self,
            variable=self.mood_var,
            values=mood_options,
            fg_color="white",
            text_color="black",
            font=ctk.CTkFont(size=16),
        )
        mood_dropdown.grid(row=0, column=1, sticky="w", padx=(15, 0), pady=(20, 0))

        # (4) Tutorial Button
        tutorial_button = ctk.CTkButton(
            self,
            text="Tutorial",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="white",
            text_color="black",
            width=120,
            command=lambda: controller.show_frame("TutorialPage"),
        )
        tutorial_button.grid(row=0, column=1, sticky="ne", padx=(0, 20), pady=10)

        # (2) Playlist Display
        playlist_frame = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        playlist_frame.grid(
            row=1, column=0, columnspan=2, sticky="nsew", padx=40, pady=10
        )

        playlist_label = ctk.CTkLabel(
            playlist_frame,
            text="Generated Playlist:",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="black",
        )
        playlist_label.pack(pady=(10, 5), anchor="w", padx=10)

        self.playlist_textbox = ctk.CTkTextbox(
            playlist_frame,
            font=ctk.CTkFont(size=16),
            text_color="black",
            wrap="word",
            state="disabled",
        )
        self.playlist_textbox.pack(fill="both", expand=True, padx=10, pady=10)

        # (3) Save Playlist Button (Heart Icon)
        save_button = ctk.CTkButton(
            self,
            text="♥ Save",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="white",
            text_color="red",
            command=self.save_playlist,
        )
        save_button.grid(row=1, column=1, sticky="ne", padx=20, pady=20)

        # (5) Generate Button
        generate_button = ctk.CTkButton(
            self,
            text="Generate",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="white",
            text_color="black",
            corner_radius=30,
            width=180,
            height=50,
            command=self.generate_playlist,
        )
        generate_button.grid(row=2, column=0, sticky="e", padx=(0, 30), pady=20)

        # (6) Regenerate Button
        regenerate_button = ctk.CTkButton(
            self,
            text="Regenerate",
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="white",
            text_color="black",
            corner_radius=30,
            width=180,
            height=50,
            command=self.regenerate_playlist,
        )
        regenerate_button.grid(row=2, column=1, sticky="w", padx=(30, 0), pady=20)

    def generate_playlist(self):
        """Generate a playlist based on the selected mood."""
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
        """Save the displayed playlist to a text file."""
        if not self.playlist_textbox.get("1.0", tk.END).strip():
            messagebox.showerror("Error", "No playlist to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "w") as file:
            file.write(self.playlist_textbox.get("1.0", tk.END).strip())

        messagebox.showinfo("Success", f"Playlist saved to {file_path}")

    def regenerate_playlist(self):
        """Regenerate the playlist for the currently selected mood."""
        self.generate_playlist()

    def update_playlist_display(self, text):
        """Update the playlist display textbox with given text."""
        self.playlist_textbox.configure(state="normal")
        self.playlist_textbox.delete("1.0", tk.END)
        self.playlist_textbox.insert(tk.END, text)
        self.playlist_textbox.configure(state="disabled")


class TutorialPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#D33232")

        # Step information
        self.steps = [
            "Step 1\n\n**Mood Selection:**\nSelect a mood from the dropdown to start generating playlists.",
            "Step 2\n\n**Generate Button:**\nClick 'Generate' to create a playlist based on the selected mood.",
            "Step 3\n\n**Regenerate Button:**\nUse 'Regenerate' to refresh your playlist with different songs for the same mood.",
        ]
        self.current_step = 0

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Tutorial",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky="w")

        # Navigation Buttons
        self.prev_button = ctk.CTkButton(
            self,
            text="◀",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_previous_step
        )
        self.prev_button.grid(row=1, column=0, pady=10, padx=20, sticky="e")

        self.next_button = ctk.CTkButton(
            self,
            text="▶",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_next_step
        )
        self.next_button.grid(row=1, column=2, pady=10, padx=20, sticky="w")

        # Textbox
        self.textbox = ctk.CTkTextbox(
            self,
            height=300,
            width=600,
            font=ctk.CTkFont(size=16)
        )
        self.textbox.grid(row=1, column=1, padx=20)
        self.textbox.insert("1.0", self.steps[self.current_step])
        self.textbox.configure(state="disabled")

        # Back Button
        back_button = ctk.CTkButton(
            self,
            text="Back",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=lambda: controller.show_frame("GeneratorPage"),
        )
        back_button.grid(row=0, column=2, pady=20, padx=20, sticky="e")

        self.update_navigation_buttons()

    def show_previous_step(self):
        """Show the previous tutorial step."""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_tutorial_text()
            self.update_navigation_buttons()

    def show_next_step(self):
        """Show the next tutorial step."""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.update_tutorial_text()
            self.update_navigation_buttons()

    def update_tutorial_text(self):
        """Update the tutorial textbox with the current step's content."""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", tk.END)
        self.textbox.insert("1.0", self.steps[self.current_step])
        self.textbox.configure(state="disabled")

    def update_navigation_buttons(self):
        """Enable or disable navigation buttons based on the current step."""
        self.prev_button.configure(state="normal" if self.current_step > 0 else "disabled")
        self.next_button.configure(state="normal" if self.current_step < len(self.steps) - 1 else "disabled")


if __name__ == "__main__":
    app = App()
    app.mainloop()