import sys
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

# Main class that controls the UI 
class MusicApp:
# constructor method   
    def __init__(self, data_dict, sim_engine):
# Store the music data 
        self.data = data_dict
# store similar calculation
        self.sim_engine = sim_engine
        self.root = tk.Tk()
        self.root.title("HARMONY")
        self.root.geometry("800x850")
        self.root.configure(bg="#f0f0f0") # Light grey background

# Setup Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
# Define Fonts
        self.main_font = ("Helvetica", 11)
        self.header_font = ("Helvetica", 12, "bold")
        self.title_font = ("Helvetica", 24, "bold")
        
# Build the UI
        self.setup_ui()
        self.root.bind("<Escape>", lambda e: self.force_quit())


    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg="#f0f0f0")
        header_frame.pack(pady=(40, 20))
        tk.Label(header_frame, text="Music Recommender", font=self.title_font, bg="#f0f0f0").pack()
        
# Input Card 
        input_card = tk.Frame(self.root, bg="white", padx=30, pady=30, relief="flat")
        input_card.pack(fill="x", padx=50, pady=10)
        
# Mode Selection (Track vs Artist)
        ttk.Label(input_card, text="Mode", background="white", font=("Helvetica", 10, "bold")).grid(row=0, column=0, sticky="w")
        self.comp_type = tk.StringVar(value="track")
        mode_frame = tk.Frame(input_card, bg="white")
        mode_frame.grid(row=1, column=0, sticky="w", pady=(0, 15))
        ttk.Radiobutton(mode_frame, text="Track", variable=self.comp_type, value="track").pack(side="left")
        ttk.Radiobutton(mode_frame, text="Artist", variable=self.comp_type, value="artist").pack(side="left")
        
# Metric Selection
        ttk.Label(input_card, text="Algorithm", background="white", font=("Helvetica", 10, "bold")).grid(row=0, column=1, sticky="w")
        self.metric_var = tk.StringVar(value="Cosine")
        metrics = ["Cosine", "Euclidean", "Pearson", "Manhattan"]
        self.metric_dropdown = ttk.Combobox(input_card, textvariable=self.metric_var, values=metrics, state="readonly")
        self.metric_dropdown.grid(row=1, column=1, sticky="w", pady=(0, 15))

# Text Entries
        ttk.Label(input_card, text="Item 1", background="white").grid(row=2, column=0, sticky="w")
        self.entry1 = ttk.Entry(input_card, width=35)
        self.entry1.grid(row=3, column=0, sticky="ew", pady=(5, 15), padx=(0, 10))
        
        ttk.Label(input_card, text="Item 2", background="white").grid(row=2, column=1, sticky="w")
        self.entry2 = ttk.Entry(input_card, width=35)
        self.entry2.grid(row=3, column=1, sticky="ew", pady=(5, 15))

# Analyze Button
        tk.Button(input_card, text="Analyze", bg="#4CAF50", fg="white", font=("Helvetica", 11, "bold"), 
                  relief="flat", pady=10, command=self.run_comparison).grid(row=4, column=0, columnspan=2, sticky="ew")

        self.result_area = scrolledtext.ScrolledText(self.root, width=80, height=20, font=("Consolas", 10), padx=15, pady=15)
        self.result_area.pack(fill="both", expand=True, padx=50, pady=(20, 30))
        self.result_area.tag_config("HEADER", font=("Helvetica", 11, "bold"))
        
        tk.Button( 
            input_card, 
            text="Quit",
            bg="#f44336",
            fg="white",
            font=("Helvetica", 11, "bold"),
            relief="flat",
            pady=10,
            command=self.force_quit
            ).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        
        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)


        
    def run_comparison(self):
# trigger setting when user clicks
        item1 = self.entry1.get().strip().lower()
        item2 = self.entry2.get().strip().lower()

        mode = self.comp_type.get()
        metric_name = self.metric_var.get()
        
        if not item1 or not item2:
            messagebox.showwarning("Missing Input", "Enter both items.")
            return

# Map string selection to actual function
        metric_map = {
            "Cosine": self.sim_engine.cosine_similarity,
            "Euclidean": self.sim_engine.euclidean_similarity,
            "Pearson": self.sim_engine.pearson_similarity,
            "Manhattan": self.sim_engine.manhattan_similarity
        }
        selected_metric = metric_map[metric_name]

# Reset Result Screen
        self.result_area.delete(1.0, tk.END)
        self.result_area.insert(tk.END, f"Processing {mode} comparison...\n\n", "HEADER")

        try:
            is_artist = (mode == "artist")
            
            if is_artist:
                score = self.sim_engine.compare_artists(self.data, item1, item2, selected_metric)
            else:
                score = self.sim_engine.compare_tracks(self.data, item1, item2, selected_metric)

            self.result_area.insert(tk.END, f"Similarity Score: {score}\n\n")
            
# Get Recommendations for both inputs
            self._display_recs(item1, selected_metric, is_artist)
            self.result_area.insert(tk.END, "\n" + "-"*40 + "\n\n")
            self._display_recs(item2, selected_metric, is_artist)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _display_recs(self, item, metric, is_artist):
        display_name = item.title()
        self.result_area.insert(tk.END, f"Top 5 Recommendations for '{display_name}':\n", "HEADER")

        recs = self.sim_engine.get_recommendations(self.data, item, metric, by_artist=is_artist)
        if isinstance(recs, list):
            for i, (name, val) in enumerate(recs, 1):
                self.result_area.insert(tk.END, f"   {i}. {name} ({val:.4f})\n")
        else:
            self.result_area.insert(tk.END, f"   Error: {recs}\n")
            
    def force_quit(self):
        self.root.destroy()   # Close window

    
    def run(self):
        self.root.mainloop()


    def quit_app(self):
        if messagebox.askyesno("Quit", "Do you want to exit the application?"):
            self.force_quit()


