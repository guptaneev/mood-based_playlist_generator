import json
import random
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk

# Mood-based colors
MOOD_COLORS = {
    "Happy": ("#FFD700", "Generate Happy Playlist", "Regenerate Happy Playlist"),
    "Sad": ("#4682B4", "Generate Sad Playlist", "Regenerate Sad Playlist"),
    "Relaxed": ("#98FB98", "Generate Relaxed Playlist", "Regenerate Relaxed Playlist"),
    "Energetic": ("#FF4500", "Generate Energetic Playlist", "Regenerate Energetic Playlist"),
    "Romantic": ("#FF69B4", "Generate Romantic Playlist", "Regenerate Romantic Playlist")
}

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


class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#D33232")  # Solid red background for the Home Page

        # Configure grid layout for central alignment
        self.grid_rowconfigure(0, weight=1)  # Top spacer
        self.grid_rowconfigure(1, weight=2)  # Title and button vertical space
        self.grid_rowconfigure(2, weight=1)  # Bottom spacer
        self.grid_columnconfigure(0, weight=2)  # Left side for Title
        self.grid_columnconfigure(1, weight=1)  # Right side for Button

        # Title Frame
        text_frame = ctk.CTkFrame(self, fg_color="#D33232")
        text_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(50, 0))  # Shifted down with top padding

        # Title text as three separate rows (centrally aligned)
        title1 = ctk.CTkLabel(
            text_frame,
            text="Mood-Based",
            font=ctk.CTkFont(size=72, weight="bold"),  # Much larger font size
            text_color="black",
        )
        title1.pack(anchor="center")

        title2 = ctk.CTkLabel(
            text_frame,
            text="Playlist",
            font=ctk.CTkFont(size=72, weight="bold"),  # Much larger font size
            text_color="black",
        )
        title2.pack(anchor="center")

        title3 = ctk.CTkLabel(
            text_frame,
            text="Generator",
            font=ctk.CTkFont(size=72, weight="bold"),  # Much larger font size
            text_color="black",
        )
        title3.pack(anchor="center")

        # Start Button
        start_button = ctk.CTkButton(
            self,
            text="Start",
            font=ctk.CTkFont(size=36, weight="bold"),  # Larger text for the button
            fg_color="white",
            hover_color="#F08080",  # Lighter red hover color
            text_color="black",
            corner_radius=40,  # Keeps it rounded but larger
            command=lambda: controller.show_frame("GeneratorPage"),
            width=250,  # Larger button width
            height=100,  # Larger button height
        )
        start_button.grid(
            row=1, column=1, sticky="n", padx=(20, 50), pady=(70, 0)
        )  # Shifted down with top padding


class GeneratorPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#D33232")

        # Title
        title_label = ctk.CTkLabel(
            self,
            text="Generate Your Playlist",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="white"
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=20)

        # Tutorial Button
        tutorial_button = ctk.CTkButton(
            self,
            text="Tutorial",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: controller.show_frame("TutorialPage"),
            width=100,
            fg_color="white",
            text_color="black",
            hover_color="#F0F0F0"
        )
        tutorial_button.grid(row=0, column=2, sticky="ne", pady=20, padx=20)

        # Mood Selection (Label and Dropdown combined as a sentence)
        mood_frame = ctk.CTkFrame(self, fg_color="#D33232")
        mood_frame.grid(row=1, column=0, columnspan=2, pady=10, padx=20, sticky="w")

        mood_label = ctk.CTkLabel(
            mood_frame,
            text="I'm feeling...",
            font=ctk.CTkFont(size=18),
            text_color="white"
        )
        mood_label.pack(side="left", padx=5)

        self.mood_var = ctk.StringVar(value="Happy")
        mood_options = list(MOOD_COLORS.keys())  # Dynamically fetch moods from MOOD_COLORS dictionary
        mood_dropdown = ctk.CTkOptionMenu(
            mood_frame,
            variable=self.mood_var,
            values=mood_options,
            font=ctk.CTkFont(size=14)
        )
        mood_dropdown.pack(side="left", padx=10)

        # Playlist Display
        playlist_frame = ctk.CTkFrame(self, width=600, height=300, fg_color="white")
        playlist_frame.grid(row=3, column=0, pady=20, padx=20, sticky="w")

        # Favorite Button (top right of the playlist box)
        favorite_button = ctk.CTkButton(
            playlist_frame,
            text="❤",
            font=ctk.CTkFont(size=16),
            fg_color="white",
            text_color="#FF0000",
            hover_color="#F0F0F0",
            command=self.save_favorite,
            width=40
        )
        favorite_button.pack(anchor="ne", padx=5, pady=5)

        self.playlist_textbox = ctk.CTkTextbox(
            playlist_frame,
            height=250,
            width=580,
            font=ctk.CTkFont(size=14)
        )
        self.playlist_textbox.pack(pady=(0, 10), padx=10)
        self.playlist_textbox.configure(state="disabled")  # Initially read-only

        # Generate and Regenerate Buttons
        button_frame = ctk.CTkFrame(self, fg_color="#D33232")
        button_frame.grid(row=3, column=1, pady=20, padx=10, sticky="n")

        self.generate_button = ctk.CTkButton(
            button_frame,
            text="Generate",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.generate_playlist,
            fg_color="white",
            text_color="black",
            hover_color="#F0F0F0",
            width=120
        )
        self.generate_button.pack(pady=10, padx=20)

        self.regenerate_button = ctk.CTkButton(
            button_frame,
            text="Regenerate",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.regenerate_playlist,
            fg_color="white",
            text_color="black",
            hover_color="#F0F0F0",
            width=120
        )
        self.regenerate_button.pack(pady=10, padx=20)
        
    def update_visuals(self, mood):
        """Updates the background color and button text based on the selected mood."""
        bg_color, generate_text, regenerate_text = MOOD_COLORS.get(mood, ("#D33232", "Generate", "Regenerate"))
    
        # Change background color
        self.configure(fg_color=bg_color)
    
        # Update button texts
        self.generate_button.configure(text=generate_text)
        self.regenerate_button.configure(text=regenerate_text)

    def generate_playlist(self):
        """Generates a playlist based on the selected mood."""
        self.update_visuals(self.mood_var.get())  # Update UI based on the selected mood
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

        self.current_playlist = random.sample(playlist, min(10, len(playlist)))
        self.update_playlist_display(
            f"{mood} Playlist:\n" +
            "\n".join(f"{song['song']} by {song['artist']}" for song in self.current_playlist)
        )

    def regenerate_playlist(self):
        """Regenerates the playlist with at least 50% difference in songs."""
        if not hasattr(self, "current_playlist") or not self.current_playlist:
            messagebox.showerror("Error", "No playlist exists to regenerate. Generate one first.")
            return

        mood = self.mood_var.get()
        try:
            with open("songs.json", "r") as f:
                song_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror("Error", "Unable to load songs.json file.")
            return

        playlist = song_data.get(mood, [])
        if not playlist:
            messagebox.showerror("Error", "No songs available for the selected mood.")
            return

        new_playlist = random.sample(playlist, min(10, len(playlist)))
        differences = len(set(song["song"] for song in new_playlist) -
                          set(song["song"] for song in self.current_playlist))

        if differences < len(new_playlist) / 2:
            messagebox.showerror(
                "Regenerate Warning",
                "Unable to ensure at least 50% difference in regenerated playlist."
            )

        self.current_playlist = new_playlist
        self.update_playlist_display(
            f"{mood} Playlist (Regenerated):\n" +
            "\n".join(f"{song['song']} by {song['artist']}" for song in self.current_playlist)
        )

    def save_favorite(self):
        """Save the current playlist as a favorite."""
        if not hasattr(self, "current_playlist") or not self.current_playlist:
            messagebox.showerror("Error", "No playlist to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        with open(file_path, "w") as file:
            file.write("\n".join(f"{song['song']} by {song['artist']}" for song in self.current_playlist))

        messagebox.showinfo("Success", f"Playlist saved as favorite at {file_path}")

    def update_playlist_display(self, text):
        """Updates the playlist display box with the specified text."""
        self.playlist_textbox.configure(state="normal")
        self.playlist_textbox.delete("1.0", tk.END)
        self.playlist_textbox.insert("1.0", text)
        self.playlist_textbox.configure(state="disabled")


class TutorialPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#D33232")

        # Step information
        self.steps = [
    "Step 1\n\n**Mood Selection:**\n"
    "The first step in using the Mood-Based Playlist Generator is selecting a mood. "
    "Click on the dropdown menu and choose from a variety of moods such as 'Happy', 'Sad', "
    "'Relaxed', 'Energetic', and more. This selection will determine the type of songs that appear in your playlist.\n\n"
    "**Why it matters:**\n"
    "Your mood choice directly affects the genre, tempo, and overall vibe of the generated playlist. "
    "This ensures a tailored music experience based on how you’re feeling.",

    "Step 2\n\n**Generate Button:**\n"
    "Once a mood is selected, press the 'Generate' button to create a playlist. "
    "The application will fetch a list of songs from its internal database based on the selected mood.\n\n"
    "**How it works:**\n"
    "- The system filters through a `.json` database containing categorized songs.\n"
    "- It selects a predefined number of tracks that best match the chosen mood.\n"
    "- The songs are displayed in a structured list format.\n\n"
    "**Expected Outcome:**\n"
    "A playlist of at least 10 songs (or as many as available in that mood category) will be displayed within seconds.",

    "Step 3\n\n**Regenerate Button:**\n"
    "If you are not satisfied with the generated playlist, press the 'Regenerate' button to get a new set of songs for the same mood.\n\n"
    "**How it works:**\n"
    "- The system ensures that at least 50% of the songs in the newly generated playlist are different from the previous selection.\n"
    "- It prevents excessive repetition by keeping track of the last generated playlist.\n\n"
    "**Why it’s useful:**\n"
    "This feature ensures variety, allowing you to explore different songs under the same mood category without manual selection.",

    "Step 4\n\n**Tutorial Button:**\n"
    "At any time, you can access this tutorial by clicking the 'Tutorial' button. "
    "This page provides a guided step-by-step breakdown of how to use the application effectively.\n\n"
    "**What’s included in the tutorial:**\n"
    "- How to select moods.\n"
    "- How to generate playlists.\n"
    "- How to regenerate a new playlist if needed.\n"
    "- Navigation controls (back and next buttons).\n\n"
    "**Why it’s important:**\n"
    "This tutorial ensures that first-time users, as well as returning users, can understand all features of the app with ease.",

    "Step 5\n\n**Navigation Between Tutorial Steps:**\n"
    "Use the '<' (previous) and '>' (next) buttons to navigate through the tutorial steps. "
    "Each step explains a different feature in detail.\n\n"
    "**How it works:**\n"
    "- The left arrow ('<') button takes you to the previous step.\n"
    "- The right arrow ('>') button moves forward to the next step.\n"
    "- The buttons are disabled when you reach the first or last step to prevent errors.\n\n"
    "**Best Practice:**\n"
    "Follow the tutorial in order to fully understand the application's functionalities.",

    "Step 6\n\n**Returning to the Generator Page:**\n"
    "Once you are familiar with the tutorial, you can return to the main Generator Page by clicking the 'Back' button at the top right of this page.\n\n"
    "**Why this matters:**\n"
    "The back button ensures smooth navigation and allows you to quickly return to the playlist generator without restarting the app.",

    "Step 7\n\n**Saving & Exporting Playlists:**\n"
    "After generating a playlist, you may want to save it for future listening. The application provides a save and export feature.\n\n"
    "**How it works:**\n"
    "- Click the heart icon next to the playlist to mark it as a favorite.\n"
    "- Press the 'Save' button to store the playlist in the app.\n"
    "- Use the 'Export' button to download the playlist as a `.txt` file to your device.\n\n"
    "**Why it’s useful:**\n"
    "This allows you to save your favorite music lists and share them with others easily.",

    "Step 8\n\n**Adaptive Theme & Visual Experience:**\n"
    "The app adapts its color scheme to match the selected mood, creating an immersive experience.\n\n"
    "**How it works:**\n"
    "- 'Happy' mood applies warm colors like yellow and orange.\n"
    "- 'Sad' mood uses cooler shades like blue or gray.\n"
    "- 'Energetic' mood shifts to bright reds and bold tones.\n\n"
    "**Why it’s important:**\n"
    "A visually adaptive UI enhances engagement and creates an emotionally resonant music selection process."
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

        # Navigation Buttons with Black Arrows
        self.prev_button = ctk.CTkButton(
            self,
            text="<",  # Black V-shaped arrow
            font=ctk.CTkFont(size=28, weight="bold"),  # Larger font for better visibility
            command=self.show_previous_step,
            fg_color="#D9D9D9",
            hover_color="#C0C0C0",
            text_color="black"
        )
        self.prev_button.grid(row=1, column=0, pady=10, padx=20, sticky="e")

        self.next_button = ctk.CTkButton(
            self,
            text=">",  # Black V-shaped arrow pointing right
            font=ctk.CTkFont(size=28, weight="bold"),  # Larger font for better visibility
            command=self.show_next_step,
            fg_color="#D9D9D9",
            hover_color="#C0C0C0",
            text_color="black"
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
            fg_color="#E57373",
            text_color="black",
            hover_color="#FFCCCC",
            width=150
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
