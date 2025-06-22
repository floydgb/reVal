"""
reVal Agent - Main orchestrator for real estate valuation
Coordinates Zillow API data fetching, analysis, and PDF generation
"""

import logging
from typing import Dict, Any, Optional
from .zillow_client import ZillowClient
from .pdf_generator import ReValPDFGenerator

class ReValAgent:
    """Main agent that coordinates property valuation and report generation"""
    
    def __init__(self):
        self.zillow_client = ZillowClient()
        self.pdf_generator = ReValPDFGenerator()
        self.logger = logging.getLogger(__name__)
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def generate_property_report(self, address: str, city: str, state: str) -> Optional[str]:
        """
        Generate a complete property valuation report
        
        Args:
            address: Street address
            city: City name
            state: State abbreviation
            
        Returns:
            Path to generated PDF report or None if error
        """
        try:
            # Step 1: Search for property
            self.logger.info(f"Searching for property: {address}, {city}, {state}")
            search_results = self.zillow_client.search_properties(address, city, state)
            
            if not search_results or not search_results.get('results'):
                self.logger.error("No properties found")
                return None
            
            # Get the first property from search results
            property_basic = search_results['results'][0]
            zpid = property_basic.get('zpid')
            
            if not zpid:
                self.logger.error("No ZPID found for property")
                return None
            
            # Step 2: Get detailed property information
            self.logger.info(f"Fetching detailed information for ZPID: {zpid}")
            property_details = self.zillow_client.get_property_details(zpid)
            
            if not property_details:
                self.logger.error("Failed to get property details")
                return None
            
            # Step 3: Get comparable sales (optional)
            comparable_sales = self.zillow_client.get_comparable_sales(zpid)
            
            # Step 4: Analyze property data for 10 quality factors
            analysis = self._analyze_property_factors(property_details, comparable_sales)
            
            # Step 5: Generate PDF report
            self.logger.info("Generating PDF report")
            pdf_path = self.pdf_generator.generate_report(property_details, analysis)
            
            self.logger.info(f"Report generated successfully: {pdf_path}")
            return pdf_path
            
        except Exception as e:
            self.logger.error(f"Error generating property report: {e}")
            return None
    
    def _analyze_property_factors(self, property_data: Dict[str, Any], comparable_sales: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Analyze property data and map to 10 quality factors
        
        Args:
            property_data: Detailed property information
            comparable_sales: Comparable sales data (optional)
            
        Returns:
            Analysis results for each quality factor
        """
        analysis = {}
        
        # 1. Location
        analysis['location'] = self._analyze_location(property_data)
        
        # 2. Lot Quality
        analysis['lot_quality'] = self._analyze_lot_quality(property_data)
        
        # 3. Lot Utilization
        analysis['lot_utilization'] = self._analyze_lot_utilization(property_data)
        
        # 4. Lot Orientation
        analysis['lot_orientation'] = self._analyze_lot_orientation(property_data)
        
        # 5. Privacy
        analysis['privacy'] = self._analyze_privacy(property_data)
        
        # 6. Views
        analysis['views'] = self._analyze_views(property_data)
        
        # 7. Architectural Style
        analysis['architectural_style'] = self._analyze_architectural_style(property_data)
        
        # 8. Finishes
        analysis['finishes'] = self._analyze_finishes(property_data)
        
        # 9. Layout
        analysis['layout'] = self._analyze_layout(property_data)
        
        # 10. Scale & Volume
        analysis['scale_&_volume'] = self._analyze_scale_volume(property_data)
        
        return analysis
    
    def _analyze_location(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze location quality factor"""
        address = data.get('address', '')
        city = data.get('city', '')
        state = data.get('state', '')
        
        # Basic analysis based on available data
        score = 7  # Default score
        analysis = f"Property located at {address}, {city}, {state}."
        
        # Enhance based on neighborhood data if available
        if data.get('schools'):
            score += 1
            analysis += " Good school district in area."
        
        return {
            'score': min(score, 10),
            'analysis': analysis
        }
    
    def _analyze_lot_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze lot quality factor"""
        lot_size = data.get('lotAreaValue', 0)
        
        score = 6  # Default score
        analysis = f"Lot size: {lot_size} sq ft."
        
        if lot_size > 10000:
            score = 9
            analysis += " Large lot provides excellent space and potential."
        elif lot_size > 7500:
            score = 7
            analysis += " Good-sized lot with adequate space."
        elif lot_size > 5000:
            score = 6
            analysis += " Standard lot size for the area."
        else:
            score = 4
            analysis += " Smaller lot may limit outdoor activities."
        
        return {
            'score': score,
            'analysis': analysis
        }
    
    def _analyze_lot_utilization(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze lot utilization factor"""
        living_area = data.get('livingArea', 0)
        lot_size = data.get('lotAreaValue', 1)
        
        utilization_ratio = living_area / lot_size if lot_size > 0 else 0
        
        score = 6  # Default
        analysis = f"Building covers {utilization_ratio:.1%} of lot."
        
        if 0.15 <= utilization_ratio <= 0.25:
            score = 8
            analysis += " Optimal utilization with good balance of built and open space."
        elif utilization_ratio < 0.15:
            score = 6
            analysis += " Conservative use of lot space, potential for expansion."
        else:
            score = 5
            analysis += " High lot coverage may limit outdoor space."
        
        return {
            'score': score,
            'analysis': analysis
        }
    
    def _analyze_lot_orientation(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze lot orientation factor"""
        # This would require more detailed data about property positioning
        score = 6  # Default neutral score
        analysis = "Lot orientation analysis requires additional survey data."
        
        return {
            'score': score,
            'analysis': analysis
        }
    
    def _analyze_privacy(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze privacy factor"""
        lot_size = data.get('lotAreaValue', 0)
        
        score = 6  # Default
        analysis = "Privacy assessment based on lot characteristics."
        
        if lot_size > 15000:
            score = 8
            analysis = "Large lot provides excellent privacy and buffer from neighbors."
        elif lot_size > 8000:
            score = 7
            analysis = "Good lot size allows for reasonable privacy."
        else:
            score = 5
            analysis = "Standard lot size with typical suburban privacy levels."
        
        return {
            'score': score,
            'analysis': analysis
        }
    
    def _analyze_views(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze views factor"""
        # This would require more detailed data about surroundings
        score = 6  # Default neutral score
        analysis = "View quality assessment requires on-site evaluation."
        
        return {
            'score': score,
            'analysis': analysis
        }
    
    def _analyze_architectural_style(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze architectural style factor"""
        year_built = data.get('yearBuilt', 0)
        home_type = data.get('propertyType', '')
        
        score = 6  # Default
        analysis = f"{home_type} built in {year_built}."
        
        if year_built > 2010:
            score = 7
            analysis += " Modern construction with contemporary design."
        elif year_built > 1990:
            score = 6
            analysis += " Well-maintained property with updated features."
        elif year_built > 1970:
            score = 5
            analysis += " Mature property that may benefit from updates."
        
        return {
            'score': score,
            'analysis': analysis
        }
    
    def _analyze_finishes(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze finishes factor"""
        year_built = data.get('yearBuilt', 0)
        
        score = 6  # Default
        analysis = "Finish quality assessment based on property age and data."
        
        if year_built > 2015:
            score = 7
            analysis = "Recent construction likely features modern finishes."
        elif year_built > 2000:
            score = 6
            analysis = "Property likely has good quality finishes with some updates needed."
        
        return {
            'score': score,
            'analysis': analysis
        }
    
    def _analyze_layout(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze layout factor"""
        bedrooms = data.get('bedrooms', 0)
        bathrooms = data.get('bathrooms', 0)
        living_area = data.get('livingArea', 0)
        
        score = 6  # Default
        analysis = f"{bedrooms} bedrooms, {bathrooms} bathrooms, {living_area:,} sq ft."
        
        # Calculate space efficiency
        if bedrooms > 0:
            space_per_bedroom = living_area / bedrooms
            if space_per_bedroom > 600:
                score = 7
                analysis += " Spacious layout with generous room sizes."
            elif space_per_bedroom > 400:
                score = 6
                analysis += " Well-proportioned layout."
            else:
                score = 5
                analysis += " Compact layout may feel cramped."
        
        return {
            'score': score,
            'analysis': analysis
        }
    
    def _analyze_scale_volume(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze scale & volume factor"""
        living_area = data.get('livingArea', 0)
        stories = data.get('stories', 1)
        
        score = 6  # Default
        analysis = f"{living_area:,} sq ft across {stories} stor{'y' if stories == 1 else 'ies'}."
        
        if living_area > 3000:
            score = 8
            analysis += " Generous scale provides impressive volume and presence."
        elif living_area > 2000:
            score = 7
            analysis += " Good scale appropriate for family living."
        elif living_area > 1500:
            score = 6
            analysis += " Comfortable scale for most households."
        else:
            score = 5
            analysis += " Compact scale suitable for smaller households."
        
        return {
            'score': score,
            'analysis': analysis
        }
