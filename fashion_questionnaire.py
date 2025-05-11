#!/usr/bin/env python3
"""
Fashion Recommendation Questionnaire

This script provides an interactive questionnaire to collect user preferences
and generate personalized fashion recommendations.
"""
import sys
import json
import argparse
import os
import pandas as pd
import numpy as np
from fashion_recommender import FashionRecommender
import pandas as pd
import numpy as np
from fashion_recommender import FashionRecommender

class FashionQuestionnaire:
    """Interactive questionnaire for fashion recommendations."""
    
    def __init__(self, recommender):
        """
        Initialize the fashion questionnaire
        
        Args:
            recommender (FashionRecommender): The fashion recommender instance
        """
        self.recommender = recommender
        self.preferences = {
            "gender": None,
            "item_types": [],
            "style_vibes": [],
            "favorite_colors": [],
            "preferred_materials": [],
            "key_occasions": [],
            "primary_seasons": [],
            "item_specific_preferences": {}
        }
        
        # Define constants for question options
        self.GENDERS = ["Men", "Women", "Prefer not to say"]
        self.ITEM_TYPES = ["Blazer", "Boots", "Jacket", "Jewelry", "Oxfords", "Pants", "Scarf", "Skirt", "Sneakers", "Suit"]
        self.STYLES = ["Athleisure", "Boho", "Casual", "Elegant", "Formal", "Grunge", "Preppy", "Vintage"]
        self.COLORS = ["Black", "Blue", "Brown", "Gray", "Green", "Pink", "Purple", "Red", "White", "Yellow"]
        self.MATERIALS = ["Cotton", "Denim", "Leather", "Linen", "Nylon", "Silk", "Suede", "Wool"]
        self.OCCASIONS = ["Casual", "Concert", "Date", "Indoor", "Interview", "Office", "Outdoor", "Party", "Wedding"]
        self.SEASONS = ["Autumn", "Spring", "Summer", "Winter"]
    
    def print_options(self, options, allow_multiple=False):
        """
        Print options with numbers for user selection
        
        Args:
            options (list): List of options to display
            allow_multiple (bool): Whether multiple selections are allowed
        """
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        if allow_multiple:
            print("\nYou can select multiple options by entering numbers separated by commas,")
            print("or press Enter without a number to skip this question.")
        else:
            print("\nEnter a number or press Enter to skip this question.")
    
    def get_user_selection(self, options, allow_multiple=False, max_selections=None):
        """
        Get user selection from the provided options
        
        Args:
            options (list): List of options to choose from
            allow_multiple (bool): Whether multiple selections are allowed
            max_selections (int): Maximum number of selections allowed (None for unlimited)
            
        Returns:
            list or str: Selected option(s) or None if skipped
        """
        while True:
            try:
                response = input("Your selection: ").strip()
                
                # Handle empty response (skip)
                if not response:
                    return [] if allow_multiple else None
                
                if allow_multiple:
                    # Parse comma-separated numbers
                    selections = [int(i.strip()) for i in response.split(',') if i.strip()]
                    
                    # Validate selections
                    if not all(1 <= i <= len(options) for i in selections):
                        print(f"Please enter valid numbers between 1 and {len(options)}.")
                        continue
                    
                    # Check maximum selections
                    if max_selections and len(selections) > max_selections:
                        print(f"Please select at most {max_selections} options.")
                        continue
                    
                    # Return selected options
                    return [options[i-1] for i in selections]
                else:
                    # Parse single number
                    selection = int(response)
                    
                    # Validate selection
                    if not 1 <= selection <= len(options):
                        print(f"Please enter a valid number between 1 and {len(options)}.")
                        continue
                    
                    # Return selected option
                    return options[selection-1]
            
            except ValueError:
                print("Please enter valid number(s).")
                continue
    
    def ask_gender_preference(self):
        """Ask for gender preference."""
        print("\n==== Gender Preference ====")
        print("What is your gender preference for clothing styles?")
        self.print_options(self.GENDERS)
        
        self.preferences["gender"] = self.get_user_selection(self.GENDERS)
    
    def ask_item_types(self):
        """Ask for preferred item types."""
        print("\n==== Preferred Item Types ====")
        print("Which clothing or accessory items are you interested in? Select all that apply.")
        self.print_options(self.ITEM_TYPES, allow_multiple=True)
        
        self.preferences["item_types"] = self.get_user_selection(self.ITEM_TYPES, allow_multiple=True)
    
    def ask_style_vibes(self):
        """Ask for general style preferences."""
        print("\n==== General Style Vibes ====")
        print("What style vibes do you generally prefer across your wardrobe? Select up to 3.")
        self.print_options(self.STYLES, allow_multiple=True)
        
        self.preferences["style_vibes"] = self.get_user_selection(self.STYLES, allow_multiple=True, max_selections=3)
    
    def ask_favorite_colors(self):
        """Ask for favorite colors."""
        print("\n==== Favorite Colors ====")
        print("What colors do you love to wear? Select up to 5.")
        self.print_options(self.COLORS, allow_multiple=True)
        
        self.preferences["favorite_colors"] = self.get_user_selection(self.COLORS, allow_multiple=True, max_selections=5)
    
    def ask_preferred_materials(self):
        """Ask for preferred materials."""
        print("\n==== Preferred Materials ====")
        print("What fabrics or materials do you prefer for your clothing? Select up to 3.")
        self.print_options(self.MATERIALS, allow_multiple=True)
        
        self.preferences["preferred_materials"] = self.get_user_selection(self.MATERIALS, allow_multiple=True, max_selections=3)
    
    def ask_key_occasions(self):
        """Ask for key occasions."""
        print("\n==== Key Occasions ====")
        print("For which occasions do you often need outfits? Select all that apply.")
        self.print_options(self.OCCASIONS, allow_multiple=True)
        
        self.preferences["key_occasions"] = self.get_user_selection(self.OCCASIONS, allow_multiple=True)
    
    def ask_primary_seasons(self):
        """Ask for primary seasons."""
        print("\n==== Primary Seasons ====")
        print("Which seasons do you primarily shop for or style outfits for? Select all that apply.")
        self.print_options(self.SEASONS, allow_multiple=True)
        
        self.preferences["primary_seasons"] = self.get_user_selection(self.SEASONS, allow_multiple=True)
    
    def ask_item_specific_preferences(self):
        """Ask for item-specific preferences."""
        # Only ask if there are selected item types
        if not self.preferences["item_types"]:
            return
        
        print("\n==== Item-Specific Preferences ====")
        print("Let's get some more specific preferences for each item you selected.")
        
        for item in self.preferences["item_types"]:
            print(f"\n--- Preferences for {item} ---")
            item_prefs = {}
            
            # Style vibes for specific item
            print(f"Which style vibes do you prefer for {item}? Select up to 2.")
            self.print_options(self.STYLES, allow_multiple=True)
            item_prefs["styles"] = self.get_user_selection(self.STYLES, allow_multiple=True, max_selections=2)
            
            # Colors for specific item
            print(f"\nWhich colors do you prefer for {item}? Select up to 3.")
            self.print_options(self.COLORS, allow_multiple=True)
            item_prefs["colors"] = self.get_user_selection(self.COLORS, allow_multiple=True, max_selections=3)
            
            # Materials for specific item
            print(f"\nWhich materials do you prefer for {item}? Select up to 2.")
            self.print_options(self.MATERIALS, allow_multiple=True)
            item_prefs["materials"] = self.get_user_selection(self.MATERIALS, allow_multiple=True, max_selections=2)
            
            # Occasions for specific item
            print(f"\nFor which occasions do you wear {item}? Select all that apply.")
            self.print_options(self.OCCASIONS, allow_multiple=True)
            item_prefs["occasions"] = self.get_user_selection(self.OCCASIONS, allow_multiple=True)
            
            # Seasons for specific item
            print(f"\nFor which seasons do you wear {item}? Select all that apply.")
            self.print_options(self.SEASONS, allow_multiple=True)
            item_prefs["seasons"] = self.get_user_selection(self.SEASONS, allow_multiple=True)
            
            # Store preferences for this item
            self.preferences["item_specific_preferences"][item.lower()] = item_prefs
    
    def ask_casual_outfit_style(self):
        """Ask for casual outfit style preference."""
        print("\n==== Casual Outfit Style ====")
        print("For a casual occasion in your favorite season, what style vibe do you prefer for an outfit?")
        self.print_options(self.STYLES)
        
        casual_style = self.get_user_selection(self.STYLES)
        if casual_style:
            self.preferences["casual_outfit_style"] = casual_style
    
    def ask_formal_outfit_color(self):
        """Ask for formal outfit color preference."""
        print("\n==== Formal Outfit Color ====")
        print("For a formal event like a wedding or interview, what color do you prefer for your main clothing item?")
        self.print_options(self.COLORS)
        
        formal_color = self.get_user_selection(self.COLORS)
        if formal_color:
            self.preferences["formal_outfit_color"] = formal_color
    
    def ask_specific_occasion(self):
        """Ask for a specific occasion."""
        print("\n==== Specific Occasion ====")
        print("What's the occasion you're looking for outfit recommendations for?")
        self.print_options(self.OCCASIONS)
        
        occasion = self.get_user_selection(self.OCCASIONS)
        if occasion:
            self.preferences["specific_occasion"] = occasion
    
    def run_questionnaire(self):
        """Run the full questionnaire sequence."""
        print("\n==================================================")
        print("🧥 FASHION RECOMMENDATION QUESTIONNAIRE 👔")
        print("==================================================")
        print("\nPlease answer the following questions to get personalized fashion recommendations.")
        print("You can skip any question by pressing Enter without selecting an option.")
        
        # Ask all the questions
        self.ask_specific_occasion()
        self.ask_gender_preference()
        self.ask_item_types()
        self.ask_style_vibes()
        self.ask_favorite_colors()
        self.ask_preferred_materials()
        self.ask_key_occasions()
        self.ask_primary_seasons()
        self.ask_item_specific_preferences()
        self.ask_casual_outfit_style()
        self.ask_formal_outfit_color()
        
        # Return the collected preferences
        return self.preferences
    
    def get_recommendations(self):
        """Get fashion recommendations based on collected preferences."""
        # Run the questionnaire if preferences are not yet collected
        if not any(self.preferences.values()):
            self.run_questionnaire()
        
        # Process preferences to get tags
        tags = self.recommender.process_user_preferences(self.preferences)
        
        # Add specific occasion if provided
        if "specific_occasion" in self.preferences and self.preferences["specific_occasion"]:
            tags.append(self.preferences["specific_occasion"].lower())
        
        # Add casual outfit style if provided
        if "casual_outfit_style" in self.preferences and self.preferences["casual_outfit_style"]:
            if "specific_occasion" in self.preferences and self.preferences["specific_occasion"] == "Casual":
                tags.append(self.preferences["casual_outfit_style"].lower())
        
        # Add formal outfit color if provided
        if "formal_outfit_color" in self.preferences and self.preferences["formal_outfit_color"]:
            if "specific_occasion" in self.preferences and self.preferences["specific_occasion"] in ["Wedding", "Interview"]:
                tags.append(self.preferences["formal_outfit_color"].lower())
        
        # Get recommendations based on tags
        outfits = self.recommender.get_recommendations_from_tags(tags)
        
        # Format recommendations for display
        return self.recommender.format_outfit_recommendations(outfits)


def main():
    """Main function to run the fashion questionnaire."""
    parser = argparse.ArgumentParser(description="Fashion Recommendation Questionnaire")
    parser.add_argument("--dataset", "-d", default="fashion_dataset_updated.csv", 
                       help="Path to dataset CSV file")
    parser.add_argument("--save", "-s", help="Save preferences to JSON file")
    parser.add_argument("--load", "-l", help="Load preferences from JSON file")
    
    args = parser.parse_args()
    
    try:
        # Initialize the recommender
        recommender = FashionRecommender(args.dataset)
        
        # Create the questionnaire
        questionnaire = FashionQuestionnaire(recommender)
        
        # Load preferences from file if specified
        if args.load:
            try:
                with open(args.load, 'r') as f:
                    questionnaire.preferences = json.load(f)
                print(f"Loaded preferences from {args.load}")
            except Exception as e:
                print(f"Error loading preferences: {e}")
                sys.exit(1)
        else:
            # Run the questionnaire
            preferences = questionnaire.run_questionnaire()
            
            # Save preferences to file if specified
            if args.save:
                try:
                    with open(args.save, 'w') as f:
                        json.dump(preferences, f, indent=2)
                    print(f"Saved preferences to {args.save}")
                except Exception as e:
                    print(f"Error saving preferences: {e}")
        
        # Get and display recommendations
        print("\n==================================================")
        print("🧥 FASHION RECOMMENDATIONS 👔")
        print("==================================================")
        
        recommendations = questionnaire.get_recommendations()
        
        for outfit in recommendations:
            print(f"\nOutfit {outfit['outfit_number']}:")
            for category, item in outfit['components'].items():
                print(f"  {category.capitalize()}: {item}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
