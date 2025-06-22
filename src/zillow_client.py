"""
Zillow API Client for reVal
Fetches property data from RapidAPI Zillow endpoints
"""

import os
import requests
import logging
from typing import Dict, Optional, Any
from dotenv import load_dotenv

load_dotenv()

class ZillowClient:
    """Client for interacting with Zillow API via RapidAPI"""
    
    def __init__(self):
        self.api_key = os.getenv('RAPIDAPI_KEY')
        self.host = os.getenv('RAPIDAPI_HOST', 'zillow-com1.p.rapidapi.com')
        self.base_url = f"https://{self.host}"
        
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY not found in environment variables")
        
        self.headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.host
        }
        
        self.logger = logging.getLogger(__name__)
    
    def search_properties(self, address: str, city: str, state: str) -> Optional[Dict[str, Any]]:
        """
        Search for properties by address
        
        Args:
            address: Street address
            city: City name
            state: State abbreviation
            
        Returns:
            Property search results or None if error
        """
        endpoint = "/propertyExtendedSearch"
        
        params = {
            'location': f"{address}, {city}, {state}",
            'home_type': 'Houses'
        }
        
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error searching properties: {e}")
            return None
    
    def get_property_details(self, zpid: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed property information by Zillow Property ID
        
        Args:
            zpid: Zillow Property ID
            
        Returns:
            Detailed property data or None if error
        """
        endpoint = "/property"
        
        params = {'zpid': zpid}
        
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error getting property details: {e}")
            return None
    
    def get_comparable_sales(self, zpid: str) -> Optional[Dict[str, Any]]:
        """
        Get comparable sales data for a property
        
        Args:
            zpid: Zillow Property ID
            
        Returns:
            Comparable sales data or None if error
        """
        endpoint = "/similarSales"
        
        params = {'zpid': zpid}
        
        try:
            response = requests.get(
                f"{self.base_url}{endpoint}",
                headers=self.headers,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error getting comparable sales: {e}")
            return None
