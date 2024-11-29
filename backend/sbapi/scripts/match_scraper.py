import logging
from typing import Dict, Any, Optional
import pandas as pd
from selenium import webdriver
from django.db import transaction

from sbapi.services.main import getMatchData, createMatchesDF, createEventsDF
from sbapi.loaders.match_loader import MatchLoader
from sbapi.loaders.event_loader import load_match_events

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MatchScraper:
    """Handles scraping and processing of match data"""
    
    def __init__(self):
        self.match_loader = MatchLoader()
        
    def scrape_match(self, url: str) -> Dict[str, Any]:
        """
        Get match data from URL
        """
        try:
            driver = webdriver.Chrome()
            match_data = getMatchData(driver, url, close_window=True)
            return match_data
        except Exception as e:
            logger.error(f"Error scraping match data: {str(e)}")
            raise

    def process_match_data(self, match_data: Dict[str, Any]) -> Optional[Dict[str, pd.DataFrame]]:
        """
        Process raw match data into DataFrames and load into database
        """
        try:
            # Create DataFrames
            matches_df = createMatchesDF(match_data)
            events_df = createEventsDF(match_data)
            
            # Load data into database using transaction
            with transaction.atomic():
                # Load match data first
                match = self.match_loader.load_match(match_data)
                
                # Load events data
                load_match_events(match, events_df)
                
                logger.info(f"Successfully processed match {match_data['matchId']}")
                
            return {
                'matches': matches_df,
                'events': events_df
            }
            
        except Exception as e:
            logger.error(f"Error processing match data: {str(e)}")
            raise