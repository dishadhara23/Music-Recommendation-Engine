
import pandas as pd
import ast
import os

# will create a generic template for loading the data 
class DataLoader:
  
    def __init__(self, file_path):
# will create a path to store the file
        self.file_path = file_path
# After storing, will initialise a variable to hold the data for later use 
        self.data = None

    def load(self):
        
        raise NotImplementedError("Subclass must implement the load method")

class MusicDataLoader(DataLoader):

    def __init__(self, file_path):
        super().__init__(file_path) 
    
    def load(self):
    
        print(f"Attempting to load data from: {self.file_path}")
        
# here will perform error handling for exception handling 
        try:
            # Checking if the file exists
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"The file {self.file_path} was not found.")

# Read the dataset file into a pandas DataFrame
            df = pd.read_csv(self.file_path)
# Fetching exactly the columns which were needed
            req_columns = [
                "acousticness", "artists", "danceability", "energy", "id", 
                "liveness", "loudness", "name", "popularity", "speechiness", 
                "tempo", "valence"
            ]
            
# will check if the dataset file actually has all these columns
            if not set(req_columns).issubset(df.columns):
                raise ValueError("Dataset is missing required columns.")
            
# here will create a copy with only the columns we need
            music_data = df[req_columns].copy()
            
           
# We will now convert the data to a real Python list so we can use it later.
         #   music_data['artists'] = music_data['artists'].apply(ast.literal_eval)
            music_data['artists'] = music_data['artists'].apply( lambda artists: [a.strip().lower() for a in ast.literal_eval(artists)])

            
# after creating the list, will create a key named id to convert the dataframe to a dictionary 
   
            artist_music = music_data.set_index('id').to_dict(orient='index')
            
           
            self.data = artist_music
            print("Data loaded and parsed successfully.")
            return self.data

        except FileNotFoundError as e:
# If any missing file error is noticed, it will return it
            print(f"Error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None