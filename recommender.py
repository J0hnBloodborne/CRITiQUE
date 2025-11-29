# recommender.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class ContentRecommender:
    def __init__(self, places_data):
        """
        places_data: List of dicts containing 'id', 'name', 'tags', 'description', 'type'
        """
        self.df = pd.DataFrame(places_data)
        if not self.df.empty:
            self._prepare_vectors()

    def _prepare_vectors(self):
        # Create a "soup" of metadata
        # Fill NaN with empty strings to avoid errors
        self.df['description'] = self.df['description'].fillna('')
        self.df['tags'] = self.df['tags'].fillna('')
        self.df['type'] = self.df['type'].fillna('')
        
        self.df['soup'] = (
            self.df['name'] + " " + 
            self.df['type'] + " " + 
            self.df['tags'] + " " + 
            self.df['description']
        )
        
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(self.df['soup'])
        self.cosine_sim = linear_kernel(self.tfidf_matrix, self.tfidf_matrix)
        
        # Mapping from Place ID to Matrix Index
        self.id_to_idx = pd.Series(self.df.index, index=self.df['id'])

    def recommend(self, place_id, limit=3):
        if self.df.empty or place_id not in self.id_to_idx:
            return []

        idx = self.id_to_idx[place_id]
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Skip index 0 (self)
        sim_scores = sim_scores[1:limit+1]
        
        place_indices = [i[0] for i in sim_scores]
        return self.df.iloc[place_indices]['id'].tolist()