#!/usr/bin/env python3
"""
Fashion Recommendation System Core Module

This module provides a fashion recommendation engine that suggests outfits based on 
user input (questions, tags, or preferences).
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import json


class FashionRecommender:
    """Fashion recommendation engine that suggests outfits based on tags or questions."""
    
    def __init__(self, dataset_path):
        """
        Initialize the Fashion Recommender model
        
        Args:
            dataset_path (str): Path to the fashion dataset CSV
        """
        # Load the dataset
        self.df = pd.read_csv(dataset_path)
        
        # Create tag embeddings
        self.vectorizer = TfidfVectorizer()
        self.tag_matrix = self.vectorizer.fit_transform(self.df['Tags'])
        
        # Map item types to categories
        self.category_mapping = {
            'shirt': 'topwear', 'jacket': 'topwear', 'blazer': 'topwear', 'suit': 'topwear',
            'pants': 'bottomwear', 'skirt': 'bottomwear', 'jeans': 'bottomwear', 
            'boots': 'footwear', 'oxfords': 'footwear', 'sneakers': 'footwear', 'loafers': 'footwear',
            'jewelry': 'accessory', 'scarf': 'accessory'
        }
        
        # Extract unique values for each tag category
        self.item_types = list(self.category_mapping.keys())
        self.styles = ['athleisure', 'boho', 'casual', 'elegant', 'formal', 'grunge', 'preppy', 'vintage']
        self.colors = ['black', 'blue', 'brown', 'gray', 'green', 'pink', 'purple', 'red', 'white', 'yellow']
        self.materials = ['cotton', 'denim', 'leather', 'linen', 'nylon', 'silk', 'suede', 'wool']
        self.occasions = ['casual', 'concert', 'date', 'indoor', 'interview', 'office', 'outdoor', 'party', 'wedding']
        self.seasons = ['autumn', 'spring', 'summer', 'winter']
        
    def get_recommendations_from_tags(self, tags, n_recommendations=7):
        """
        Get fashion recommendations based on input tags
        
        Args:
            tags (list): List of tags (e.g., ['casual', 'summer', 'blue'])
            n_recommendations (int): Number of outfit combinations to recommend
            
        Returns:
            dict: Dictionary containing outfit recommendations
        """
        query_tags = ' '.join(tags)
        query_vector = self.vectorizer.transform([query_tags])
        
        # Calculate similarity scores
        similarities = cosine_similarity(query_vector, self.tag_matrix).flatten()
        
        # Get recommendations for each category
        recommendations = {
            'topwear': [],
            'bottomwear': [],
            'footwear': [],
            'accessory': []
        }
        
        # Filter dataset by categories and get the most similar items
        for category, items in self.category_mapping.items():
            category_df = self.df[self.df['Tags'].str.contains(category)]
            if not category_df.empty:
                category_indices = category_df.index.tolist()
                category_similarities = [(idx, similarities[idx]) for idx in category_indices]
                top_indices = sorted(category_similarities, key=lambda x: x[1], reverse=True)[:n_recommendations]
                
                # Add recommendations
                category_type = self.category_mapping[category]
                for idx, sim_score in top_indices:
                    if sim_score > 0:  # Only consider somewhat relevant matches
                        answer = self.df.iloc[idx]['AnswerText']
                        recommendations[category_type].append({
                            'item': answer,
                            'similarity': float(sim_score),
                            'tags': self.df.iloc[idx]['Tags']
                        })
        
        # Create outfit combinations
        outfits = []
        for i in range(min(n_recommendations, 7)):  # Limit to 7 outfits as required
            outfit = {}
            
            # Add one item from each mandatory category
            for category in ['topwear', 'bottomwear', 'footwear']:
                if recommendations[category]:
                    # Get random item from top recommendations if available
                    available_items = recommendations[category]
                    if available_items:
                        item = random.choice(available_items)
                        outfit[category] = item
                        # Remove the item to avoid duplicates in other outfits
                        recommendations[category].remove(item)
                    else:
                        outfit[category] = None
            
            # Add accessory only if it's relevant to the query
            if recommendations['accessory'] and any(tag in query_tags for tag in ['jewelry', 'scarf']):
                item = random.choice(recommendations['accessory'])
                outfit['accessory'] = item
                recommendations['accessory'].remove(item)
            
            # Add complete outfit to results if it has all mandatory components
            if all(outfit.get(cat) is not None for cat in ['topwear', 'bottomwear', 'footwear']):
                outfits.append(outfit)
        
        return outfits
    
    def get_recommendations_from_question(self, question, n_recommendations=7):
        """
        Get fashion recommendations based on a natural language question
        
        Args:
            question (str): Natural language question (e.g., "What should I wear for a casual summer event?")
            n_recommendations (int): Number of outfit combinations to recommend
            
        Returns:
            dict: Dictionary containing outfit recommendations
        """
        # Extract tags from the question
        extracted_tags = []
        
        # Extract item types
        for item in self.item_types:
            if item in question.lower():
                extracted_tags.append(item)
        
        # Extract styles
        for style in self.styles:
            if style in question.lower():
                extracted_tags.append(style)
        
        # Extract colors
        for color in self.colors:
            if color in question.lower():
                extracted_tags.append(color)
        
        # Extract materials
        for material in self.materials:
            if material in question.lower():
                extracted_tags.append(material)
        
        # Extract occasions
        for occasion in self.occasions:
            if occasion in question.lower():
                extracted_tags.append(occasion)
        
        # Extract seasons
        for season in self.seasons:
            if season in question.lower():
                extracted_tags.append(season)
        
        # If no tags were extracted, try to find closest question in dataset
        if not extracted_tags:
            # Use TF-IDF vectorization for questions
            question_vectorizer = TfidfVectorizer()
            question_matrix = question_vectorizer.fit_transform(self.df['QuestionText'])
            question_vector = question_vectorizer.transform([question])
            
            # Calculate similarity scores
            similarities = cosine_similarity(question_vector, question_matrix).flatten()
            top_idx = similarities.argsort()[-1]  # Get the most similar question
            
            # Extract tags from the closest question's tags
            closest_tags = self.df.iloc[top_idx]['Tags']
            extracted_tags = closest_tags.split(',')
        
        # Get recommendations based on extracted tags
        return self.get_recommendations_from_tags(extracted_tags, n_recommendations)
        
    def process_user_preferences(self, preferences):
        """
        Process user preferences from form inputs
        
        Args:
            preferences (dict): Dictionary of user preferences
                - gender: string (Men, Women, Prefer not to say)
                - item_types: list of selected items
                - style_vibes: list of selected styles
                - favorite_colors: list of selected colors
                - preferred_materials: list of selected materials
                - key_occasions: list of selected occasions
                - primary_seasons: list of selected seasons
                - item_specific_preferences: dict of item-specific preferences
                
        Returns:
            list: Processed tags for recommendation
        """
        tags = []
        
        # Process gender preference
        if preferences.get('gender') and preferences['gender'] != 'Prefer not to say':
            tags.append(preferences['gender'].lower())
        
        # Process selected item types
        if preferences.get('item_types'):
            for item in preferences['item_types']:
                tags.append(item.lower())
        
        # Process style vibes
        if preferences.get('style_vibes'):
            for style in preferences['style_vibes']:
                tags.append(style.lower())
        
        # Process colors
        if preferences.get('favorite_colors'):
            for color in preferences['favorite_colors']:
                tags.append(color.lower())
        
        # Process materials
        if preferences.get('preferred_materials'):
            for material in preferences['preferred_materials']:
                tags.append(material.lower())
        
        # Process occasions
        if preferences.get('key_occasions'):
            for occasion in preferences['key_occasions']:
                tags.append(occasion.lower())
        
        # Process seasons
        if preferences.get('primary_seasons'):
            for season in preferences['primary_seasons']:
                tags.append(season.lower())
        
        # Process item-specific preferences if available
        if preferences.get('item_specific_preferences'):
            for item, item_prefs in preferences['item_specific_preferences'].items():
                # Only add item-specific tags if the item is selected
                if item in preferences.get('item_types', []):
                    for pref_category, pref_values in item_prefs.items():
                        for value in pref_values:
                            tags.append(value.lower())
        
        return list(set(tags))  # Remove duplicates
    
    def format_outfit_recommendations(self, outfits):
        """
        Format outfit recommendations for display
        
        Args:
            outfits (list): List of outfit dictionaries
            
        Returns:
            list: Formatted outfit recommendations
        """
        formatted_outfits = []
        
        for i, outfit in enumerate(outfits):
            formatted_outfit = {
                'outfit_number': i + 1,
                'components': {}
            }
            
            # Format components
            for category, item in outfit.items():
                if item:
                    formatted_outfit['components'][category] = item['item']
            
            formatted_outfits.append(formatted_outfit)
        
        return formatted_outfits

# Command-line interface for testing
if __name__ == "__main__":
    import argparse
    import sys
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Fashion Recommendation System")
    parser.add_argument("--query", "-q", help="Natural language query for outfit recommendations")
    parser.add_argument("--tags", "-t", help="Comma-separated tags for outfit recommendations")
    parser.add_argument("--preferences", "-p", help="JSON file with user preferences")
    parser.add_argument("--count", "-c", type=int, default=7, help="Number of recommendations to generate")
    parser.add_argument("--output", "-o", choices=["json", "text"], default="text", 
                      help="Output format (json or text)")
    parser.add_argument("--dataset", "-d", default="fashion_dataset_updated.csv", 
                      help="Path to dataset CSV file")
    
    args = parser.parse_args()
    
    # Initialize recommender
    try:
        recommender = FashionRecommender(args.dataset)
    except Exception as e:
        print(f"Error loading dataset: {e}")
        sys.exit(1)
    
    outfits = None
    
    # Process based on input type
    if args.query:
        outfits = recommender.get_recommendations_from_question(args.query, args.count)
    elif args.tags:
        tags = [tag.strip() for tag in args.tags.split(",")]
        outfits = recommender.get_recommendations_from_tags(tags, args.count)
    elif args.preferences:
        try:
            with open(args.preferences, 'r') as f:
                user_preferences = json.load(f)
            tags = recommender.process_user_preferences(user_preferences)
            outfits = recommender.get_recommendations_from_tags(tags, args.count)
        except Exception as e:
            print(f"Error processing preferences file: {e}")
            sys.exit(1)
    else:
        print("Please provide either a query, tags, or preferences file.")
        parser.print_help()
        sys.exit(1)
    
    # Format and display results
    formatted_outfits = recommender.format_outfit_recommendations(outfits)
    
    if args.output == "json":
        print(json.dumps(formatted_outfits, indent=2))
    else:
        source_description = ""
        if args.query:
            source_description = f"Query: {args.query}"
        elif args.tags:
            source_description = f"Tags: {args.tags}"
        elif args.preferences:
            source_description = f"Preferences file: {args.preferences}"
            
        print(f"Fashion recommendations based on {source_description}\n")
        for outfit in formatted_outfits:
            print(f"Outfit {outfit['outfit_number']}:")
            for category, item in outfit['components'].items():
                print(f"  {category.capitalize()}: {item}")
            print()