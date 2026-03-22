
# Import all our  modules
from load_dataset_module import MusicDataLoader
from statistics_module import MusicStatistics
from similarity_module import SimilarityCalculator
from user_interface_module import MusicApp

def main():
    print("--- Music Recommendation Engine Starting ---")
    
# load data & Create loader object and pass the CSV file name
    loader = MusicDataLoader('data.csv')
    # Execute the load function
    artist_music = loader.load()
    
    if not artist_music:
        print("Failed to load data. Exiting.")
        return

    # 2. SETUP ENGINES
    # Initialize the Statistics module (as per assignment requirements)
    stats_engine = MusicStatistics()
    # Initialize the Similarity module (handles the math)
    sim_engine = SimilarityCalculator()
    
    print("Engines initialized.")

    # 3. LAUNCH APP
    print("Launching User Interface...")
    # Pass the loaded data and the math engine to the UI class
    app = MusicApp(artist_music, sim_engine)
    # Start the visual application
    app.run()

# This line ensures the main() function only runs if you execute this file directly
if __name__ == "__main__":
    main()