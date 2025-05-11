import unittest
import os
import sys

# Add parent directory to path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from fashion_recommender import FashionRecommender

class TestFashionRecommender(unittest.TestCase):
    def setUp(self):
        # Locate dataset relative to this test file
        test_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.join(test_dir, '..')
        dataset_path = os.path.join(project_dir, "fashion_dataset_updated.csv")
        self.recommender = FashionRecommender(dataset_path)
    
    def test_get_recommendations_from_tags(self):
        tags = ['casual', 'summer', 'party']
        outfits = self.recommender.get_recommendations_from_tags(tags)
        
        # Check that we get outfits
        self.assertTrue(len(outfits) > 0)
        
        # Check that each outfit has the required components
        for outfit in outfits:
            self.assertIn('topwear', outfit)
            self.assertIn('bottomwear', outfit)
            self.assertIn('footwear', outfit)
    
    def test_get_recommendations_from_question(self):
        question = "What should I wear for a casual summer party?"
        outfits = self.recommender.get_recommendations_from_question(question)
        
        # Check that we get outfits
        self.assertTrue(len(outfits) > 0)
        
        # Check that each outfit has the required components
        for outfit in outfits:
            self.assertIn('topwear', outfit)
            self.assertIn('bottomwear', outfit)
            self.assertIn('footwear', outfit)
    
    def test_process_user_preferences(self):
        user_preferences = {
            'gender': 'Men',
            'item_types': ['Blazer', 'Pants', 'Oxfords'],
            'style_vibes': ['Formal', 'Elegant'],
            'favorite_colors': ['Blue', 'Black'],
            'preferred_materials': ['Cotton', 'Wool'],
            'key_occasions': ['Interview', 'Office'],
            'primary_seasons': ['Autumn', 'Winter']
        }
        
        tags = self.recommender.process_user_preferences(user_preferences)
        
        # Check that all preference categories are represented in tags
        self.assertIn('men', tags)
        self.assertIn('blazer', tags)
        self.assertIn('formal', tags)
        self.assertIn('blue', tags)
        self.assertIn('cotton', tags)
        self.assertIn('interview', tags)
        self.assertIn('autumn', tags)
        
        # Get recommendations from these tags
        outfits = self.recommender.get_recommendations_from_tags(tags)
        
        # Check that we get outfits
        self.assertTrue(len(outfits) > 0)
        
        # Check that each outfit has the required components
        for outfit in outfits:
            self.assertIn('topwear', outfit)
            self.assertIn('bottomwear', outfit)
            self.assertIn('footwear', outfit)

if __name__ == '__main__':
    unittest.main()
