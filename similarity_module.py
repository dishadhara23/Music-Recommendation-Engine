

import numpy as np
from scipy.stats import pearsonr
from statistics_module import MusicStatistics

class SimilarityCalculator:
# to calculate the similarity between songs and rank them accordingly will be defining init function
   
    def __init__(self):
# Will take the numeric features and compare them 
        self.numeric_features = [
            "acousticness", "danceability", "energy", "liveness", 
            "loudness", "speechiness", "tempo", "valence"
        ]
        self.stats = MusicStatistics()
# after comparing will extract the numbers for single tracks 
    def _get_features(self, data, item_id):
#if the track ID does not exist return none
        if item_id not in data: return None
#  list of features values for the track 
        vector = [data[item_id][feature] for feature in self.numeric_features]

        return np.array(vector, dtype=float)
# to find track id using either track name or track id 
    def _get_id_by_name(self, data, name_or_id):
# if the input given is a valid ID will return it 
        if name_or_id in data: return name_or_id
        
# Otherwise, search all tracks for a matching name
        for pid, track in data.items():
            if track['name'].lower() == name_or_id.lower():
                return pid
        return None

    def _get_artist_vector(self, data, artist_name):
       
        vectors = []
        for track in data.values():
# Check if the name of artist is in this track's artist list
            if any(artist_name.lower() == a.lower() for a in track['artists']):
                v = [track[f] for f in self.numeric_features]
                vectors.append(v)
        
        if not vectors: return None
            
        
        means = []
        for i in range(len(self.numeric_features)):
            feature_values = [v[i] for v in vectors]
            mean_val = self.stats.compute_mean(feature_values)
            means.append(mean_val)
            return np.array(means)
    
    def euclidean_similarity(self, v1, v2):
        return np.linalg.norm(v1 - v2)

    def manhattan_similarity(self, v1, v2):
        return np.sum(np.abs(v1 - v2))

    def cosine_similarity(self, v1, v2):
        dot = np.dot(v1, v2)
        norm_a = np.linalg.norm(v1)
        norm_b = np.linalg.norm(v2)
        return 0.0 if norm_a == 0 or norm_b == 0 else dot / (norm_a * norm_b)

    def pearson_similarity(self, v1, v2):
        if len(v1) < 2: return 0
        return pearsonr(v1, v2)[0]

#  will compare the two individual track    
    def compare_tracks(self, data, track1_input, track2_input, metric_func):
        try:
            id1 = self._get_id_by_name(data, track1_input)
            id2 = self._get_id_by_name(data, track2_input)
            
            if not id1 or not id2:
                return f"Error: One or both tracks not found."

            v1 = self._get_features(data, id1)
            v2 = self._get_features(data, id2)
            
            return metric_func(v1, v2)
        except Exception as e:
            return f"Error comparing tracks: {e}"
# comparing two artist using average song feature 
    
    def compare_artists(self, data, artist1_name, artist2_name, metric_func):
        try:
            v1 = self._get_artist_vector(data, artist1_name)
            v2 = self._get_artist_vector(data, artist2_name)
            
            if v1 is None or v2 is None: return "Error: Artist not found."
            
            return metric_func(v1, v2)
        except Exception as e:
            return f"Error comparing artists: {e}"

# after comparing, finding the top 5 similar songs 
    def rank_items(self, data, query, metric_func, by_artist=False, limit=5):
        results = []
        is_distance = metric_func.__name__ in ['euclidean_similarity', 'manhattan_similarity']
        
        try:
            if not by_artist:
                query_id = self._get_id_by_name(data, query)
                if not query_id: return f"Track '{query}' not found."
                query_vec = self._get_features(data, query_id)
                
                count = 0
                for tid, track in data.items():
                    if tid == query_id: continue
                    count += 1
# Stop after 3000 to prevent freezing while refreshing 
                    if count > 3000: break 
                    
                    cand_vec = self._get_features(data, tid)
                    raw_score = metric_func(query_vec, cand_vec)
                    if is_distance:
                        score = 1 / (1 + raw_score)
                    else:
                        score = raw_score
                    
                    results.append((track['name'], score))
                    
            else:
                query_vec = self._get_artist_vector(data, query)
                if query_vec is None: return f"Artist '{query}' not found."
                
                seen_artists = {query.lower()}
                for track in data.values():
                    art_name = track['artists'][0]
                    if art_name.lower() not in seen_artists:
                        seen_artists.add(art_name.lower())
    
                        cand_vec = self._get_artist_vector(data, art_name)
                        if cand_vec is not None:
                            raw_score = metric_func(query_vec, cand_vec)
                        
                            if is_distance:
                                score = 1 / (1 + raw_score)
                            else:
                                score = raw_score
                        
                            results.append((art_name, score))

                        
                        if len(results) >= 50: break # Stop after 50 artists

            results.sort(key=lambda x: x[1], reverse=not is_distance)
            return results[:limit]
        
        except Exception as e:
            return f"Error during ranking: {e}"

    def get_recommendations(self, data, query, metric_func, by_artist=False, limit=5):
        return self.rank_items(data, query, metric_func, by_artist, limit)

