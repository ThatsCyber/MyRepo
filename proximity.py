from geopy.distance import geodesic
from typing import List, Dict, Optional
import pandas as pd

class ProximityAnalyzer:
    def __init__(self, data_handler):
        self.data_handler = data_handler
        
    def get_coordinates(self, site_data: Dict) -> Optional[tuple]:
        """Get coordinates for a site, preferring verified coordinates."""
        if site_data is None:
            return None
            
        # Check verified coordinates
        verified_lat = site_data.get('Verified_Lat')
        verified_long = site_data.get('Verified_Long')
        if verified_lat is not None and verified_long is not None and pd.notna(verified_lat) and pd.notna(verified_long):
            return (float(verified_lat), float(verified_long))
            
        # Fall back to regular coordinates
        lat = site_data.get('latitude')
        long = site_data.get('longitude')
        if lat is not None and long is not None and pd.notna(lat) and pd.notna(long):
            return (float(lat), float(float(long)))
            
        return None
        
    def calculate_distance(self, coord1: tuple, coord2: tuple) -> float:
        """Calculate distance between two coordinates in miles."""
        return geodesic(coord1, coord2).miles
        
    def find_nearest_sites(self, site: str, limit: int = 5, max_distance: float = 50.0, cart_sites_only: bool = False) -> List[Dict]:
        """Find nearest sites within specified distance."""
        if not self.data_handler.validate_site(site):
            return []
            
        origin_data = self.data_handler.get_site_info(site)
        origin_coords = self.get_coordinates(origin_data)
        
        if not origin_coords:
            return []
            
        nearby_sites = []
        
        # Get all cart sites from cart data for filtering
        cart_sites = set()
        if self.data_handler.cart_data is not None:
            cart_sites = set(self.data_handler.cart_data['Site'].unique())
        
        # Iterate through all sites
        for _, row in self.data_handler.facilities_data.iterrows():
            target_site = row['name']
            if target_site.upper() == site.upper():
                continue
                
            # Skip if we're only looking for cart sites and this isn't one
            if cart_sites_only and target_site not in cart_sites:
                continue
                
            target_data = self.data_handler.get_site_info(target_site)
            target_coords = self.get_coordinates(target_data)
            
            if not target_coords:
                continue
                
            distance = self.calculate_distance(origin_coords, target_coords)
            
            if distance <= max_distance:
                site_info = {
                    'name': target_site,
                    'address': target_data['address'],
                    'state': target_data['state'],
                    'region': target_data['region'],
                    'distance': round(distance, 2)
                }
                
                # Add cart site information if available
                if target_data.get('is_cart_site'):
                    site_info.update({
                        'Demand': target_data['Demand'],
                        'Supply': target_data['Supply'],
                        'Balance': target_data['Balance']
                    })
                
                nearby_sites.append(site_info)
        
        # Sort by distance and limit results
        nearby_sites.sort(key=lambda x: x['distance'])
        return nearby_sites[:limit] 