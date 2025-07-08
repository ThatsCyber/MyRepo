import pandas as pd
from pathlib import Path
from typing import Tuple, Dict, List, Optional
import re
from datetime import datetime
import numpy as np

class DataHandler:
    def __init__(self):
        self.facilities_data = None
        self.cart_data = None
        self.regions_data = None
        
    def load_facilities_data(self, file_path: str) -> bool:
        """Load and validate facilities data from Excel file."""
        try:
            # Read Excel file with string dtype for 'name' column to prevent date conversion
            self.facilities_data = pd.read_excel(
                file_path,
                sheet_name='Facilities_Updated',
                dtype={'name': str}
            )
            
            # Clean up site names to ensure proper formatting
            self.facilities_data['name'] = self.facilities_data['name'].apply(
                lambda x: str(x).strip().upper()
            )
            
            # Validate required columns
            required_columns = {'name', 'type', 'address', 'state', 'region', 'latitude', 'longitude'}
            missing_columns = required_columns - set(self.facilities_data.columns)
            if missing_columns:
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
            
            # Validate that there are no duplicate site names
            duplicate_sites = self.facilities_data['name'].duplicated()
            if duplicate_sites.any():
                duplicated_names = self.facilities_data[duplicate_sites]['name'].tolist()
                raise ValueError(f"Found duplicate site names: {', '.join(duplicated_names)}")
            
            # Print summary
            print(f"Successfully loaded {len(self.facilities_data)} facilities")
            print(f"Unique regions: {', '.join(sorted(self.facilities_data['region'].unique()))}")
            
            return True
        except Exception as e:
            print(f"Error loading facilities data: {str(e)}")
            return False
    
    def load_cart_data(self, file_path: str) -> bool:
        """Load and validate cart supply & demand data from CSV."""
        try:
            print(f"Attempting to load cart data from: {file_path}")
            
            # Read CSV with specific dtypes to prevent conversion errors
            self.cart_data = pd.read_csv(
                file_path,
                dtype={
                    'Site Name': str,
                    'Origin Region': str,
                    'Origin Type': str,
                    'Date': str,
                    'Demand': float,
                    'Supply': float,
                    'Balance': float,
                    'Full Day Demand': float
                }
            )
            
            print(f"Loaded columns: {self.cart_data.columns.tolist()}")
            
            # Rename columns to match our internal naming
            self.cart_data = self.cart_data.rename(columns={
                'Site Name': 'Site',
                'Origin Region': 'Region'
            })
            
            # Clean up site names
            self.cart_data['Site'] = self.cart_data['Site'].apply(
                lambda x: str(x).strip().upper() if pd.notna(x) else ''
            )
            
            # Fill NaN values with 0 for numeric columns
            numeric_columns = ['Demand', 'Supply', 'Balance', 'Full Day Demand']
            self.cart_data[numeric_columns] = self.cart_data[numeric_columns].fillna(0)
            
            # Validate all cart sites exist in facilities data
            if self.facilities_data is not None:
                valid_sites = set(self.cart_data['Site'].unique()) - {''}
                missing_sites = valid_sites - set(self.facilities_data['name'])
                if missing_sites:
                    print(f"Warning: Cart sites not found in facilities data: {missing_sites}")
            
            print("Cart data loaded successfully")
            return True
            
        except pd.errors.EmptyDataError:
            print("Error: The CSV file is empty")
            return False
        except pd.errors.ParserError as e:
            print(f"Error parsing CSV file: {str(e)}")
            return False
        except ValueError as e:
            print(f"Error with data format: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error loading cart data: {str(e)}")
            return False
    
    def validate_site(self, site: str) -> bool:
        """Validate if a site exists in facilities data."""
        if self.facilities_data is None:
            return False
        site = str(site).strip().upper()
        return site in self.facilities_data['name'].values
    
    def get_site_info(self, site: str) -> Optional[Dict]:
        """Get site information including cart data if available."""
        if self.facilities_data is None:
            return None
            
        site = str(site).strip().upper()
        if not self.validate_site(site):
            return None
            
        matching_sites = self.facilities_data[self.facilities_data['name'] == site]
        
        if matching_sites.empty:
            return None
            
        site_data = matching_sites.iloc[0].to_dict()
        
        if self.cart_data is not None:
            cart_info = self.cart_data[self.cart_data['Site'] == site]
            if not cart_info.empty:
                site_data.update({
                    'is_cart_site': True,
                    'Demand': cart_info.iloc[0]['Demand'],
                    'Full Day Demand': cart_info.iloc[0]['Full Day Demand'],
                    'Supply': cart_info.iloc[0]['Supply'],
                    'Balance': cart_info.iloc[0]['Balance']
                })
            else:
                site_data['is_cart_site'] = False
                
        return site_data
    
    def format_output(self, site: str, action: str) -> str:
        """Format output string with proper capitalization."""
        # Handle single site format only
        site_info = self.get_site_info(site)
        if not site_info:
            return f"INVALID SITE: {site.upper()}"
            
        return f"{site.upper()}- {action.upper()} TEC {site_info['region'].upper()}"
    
    def process_site_to_site(self, input_str: str, action: str = "DEPART") -> str:
        """Process site-to-site format (e.g., 'GYR1->GYR2')."""
        match = re.match(r'^([A-Za-z0-9]+)->([A-Za-z0-9]+)$', input_str.upper())
        if not match:
            return f"Invalid format: {input_str.upper()}"
            
        origin, destination = match.groups()
        if not self.validate_site(origin) or not self.validate_site(destination):
            return f"Invalid site in pair: {input_str.upper()}"
            
        origin_info = self.get_site_info(origin)
        destination_info = self.get_site_info(destination)
        if not origin_info or not destination_info:
            return f"Could not get info for sites: {input_str.upper()}"
            
        # Format the output with proper capitalization and action type
        if action == "NEED":
            return f"{origin}->{destination}- NEED TEC {origin_info['region'].upper()}"
        else:  # DEPART
            return f"{origin}->{destination}- DEPART TEC {origin_info['region'].upper()}"
        
    def get_demand_info(self, search_text: str = "") -> List[Dict]:
        """Get demand information for sites matching the search text."""
        if self.cart_data is None:
            return []
            
        search_text = str(search_text).strip().upper()
        
        # Filter data based on search text
        if search_text:
            filtered_data = self.cart_data[
                self.cart_data['Site'].str.contains(search_text)
            ]
        else:
            filtered_data = self.cart_data
            
        # Convert to list of dictionaries
        result = []
        for _, row in filtered_data.iterrows():
            result.append({
                'Site Name': row['Site'],
                'Demand': row['Demand'],
                'Full Day Demand': row['Full Day Demand'],
                'Supply': row['Supply'],
                'Balance': row['Balance']
            })
            
        return result 

    def get_negative_balance_sites(self):
        """Get sites with negative balance (demand > supply)."""
        if self.cart_data is None:
            return []
            
        sites_data = []
        for site in self.cart_data['Site'].unique():
            if not site:  # Skip empty site names
                continue
                
            site_data = self.cart_data[self.cart_data['Site'] == site]
            if site_data.empty:
                continue
                
            try:
                demand = float(site_data['Demand'].sum())
                supply = float(site_data['Supply'].sum())
                balance = supply - demand
                
                if balance < 0:
                    region = 'Unknown'
                    if 'Region' in site_data.columns:
                        # Convert to list and get first non-empty region
                        regions = site_data['Region'].tolist()
                        valid_regions = [r for r in regions if r and pd.notna(r)]
                        if valid_regions:
                            region = str(valid_regions[0])
                    
                    sites_data.append({
                        'Site Name': site,
                        'Region': region,
                        'Demand': demand,
                        'Supply': supply,
                        'Balance': balance
                    })
            except (ValueError, TypeError) as e:
                print(f"Error processing site {site}: {str(e)}")
                continue
                
        return sorted(sites_data, key=lambda x: x['Balance'])  # Sort by most negative first 

    def get_all_cart_sites(self) -> List[Dict]:
        """Get all sites with cart data, including balance information."""
        if self.cart_data is None:
            return []
            
        sites_data = []
        for site in self.cart_data['Site'].unique():
            if not site:  # Skip empty site names
                continue
                
            site_data = self.cart_data[self.cart_data['Site'] == site]
            if site_data.empty:
                continue
                
            try:
                demand = float(site_data['Demand'].sum())
                supply = float(site_data['Supply'].sum())
                balance = supply - demand
                
                region = 'Unknown'
                if 'Region' in site_data.columns:
                    # Convert to list and get first non-empty region
                    regions = site_data['Region'].tolist()
                    valid_regions = [r for r in regions if r and pd.notna(r)]
                    if valid_regions:
                        region = str(valid_regions[0])
                
                sites_data.append({
                    'Site Name': site,
                    'Region': region,
                    'Demand': demand,
                    'Supply': supply,
                    'Balance': balance
                })
            except (ValueError, TypeError) as e:
                print(f"Error processing site {site}: {str(e)}")
                continue
                
        return sites_data 