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
        self.utilization_data = None  # Add this line
        self.dwelling_data = None # Add this line
        
    def load_facilities_data(self, file_path: str) -> bool:
        """Load and validate facilities data from Excel or CSV file."""
        try:
            # Read CSV file with specific dtypes
            self.facilities_data = pd.read_csv(
                file_path,
                dtype={
                    'name': str,
                    'type': str,
                    'status': str,
                    'address': str,
                    'state': str,
                    'country': str,
                    'region': str,
                    'zip': str,
                    'timeZone': str,
                    'Verified_Lat': float,
                    'Verified_Long': float,
                    'Match_Status': str,
                    'API_Status': str
                }
            )
            
            # Convert latitude and longitude columns separately to handle potential non-numeric values
            self.facilities_data['latitude'] = pd.to_numeric(self.facilities_data['latitude'], errors='coerce')
            self.facilities_data['longitude'] = pd.to_numeric(self.facilities_data['longitude'], errors='coerce')
            
            # Clean up the data
            self.facilities_data = self.facilities_data.fillna('')
            
            # Convert site codes to uppercase
            self.facilities_data['name'] = self.facilities_data['name'].str.upper()
            
            return True
            
        except Exception as e:
            print(f"Error loading facilities data: {str(e)}")
            self.facilities_data = None
            return False
    
    def load_cart_data(self, file_path: str) -> bool:
        """Load and validate cart supply & demand data from CSV with chunked processing."""
        try:
            # Import here to avoid circular imports and for processEvents
            from PyQt6.QtWidgets import QApplication
            
            print(f"Loading cart data from: {file_path}")
            
            # Read CSV in chunks to maintain responsiveness
            chunk_size = 1000
            chunks = []
            chunk_count = 0
            
            print("Reading cart data in chunks...")
            for chunk in pd.read_csv(
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
                },
                chunksize=chunk_size
            ):
                chunk_count += 1
                print(f"Processing cart data chunk {chunk_count} ({len(chunk)} rows)...")
                chunks.append(chunk)
                
                # Keep UI responsive
                if QApplication.instance():
                    QApplication.processEvents()
            
            # Combine all chunks
            print(f"Combining {len(chunks)} chunks of cart data...")
            self.cart_data = pd.concat(chunks, ignore_index=True)
            
            # Keep UI responsive during processing
            if QApplication.instance():
                QApplication.processEvents()
            
            print(f"Loaded columns: {self.cart_data.columns.tolist()}")
            
            # Rename columns to match our internal naming
            self.cart_data = self.cart_data.rename(columns={
                'Site Name': 'Site',
                'Origin Region': 'Region'
            })
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
            # Clean up site names
            print("Cleaning site names...")
            self.cart_data['Site'] = self.cart_data['Site'].apply(
                lambda x: str(x).strip().upper() if pd.notna(x) else ''
            )
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
            # Fill NaN values with 0 for numeric columns
            print("Processing numeric columns...")
            numeric_columns = ['Demand', 'Supply', 'Balance', 'Full Day Demand']
            self.cart_data[numeric_columns] = self.cart_data[numeric_columns].fillna(0)
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
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
        """Validate if a site exists in facilities data, including sister sites."""
        if self.facilities_data is None:
            return False
        site = str(site).strip().upper()
        
        # Check each row's name column for sister sites
        for facility_name in self.facilities_data['name'].values:
            if self._is_site_in_group(site, facility_name):
                return True
        return False
    
    def _is_site_in_group(self, search_site: str, facility_name: str) -> bool:
        """Check if a search site is part of a facility group (handles sister sites)."""
        if pd.isna(facility_name):
            return False
            
        facility_name = str(facility_name).strip().upper()
        search_site = search_site.strip().upper()
        
        # Split by " / " to get all sites in the group
        sites_in_group = [site.strip() for site in facility_name.split(' / ')]
        
        # Check if search site matches any site in the group
        return search_site in sites_in_group
    
    def _get_facility_by_site(self, site: str) -> pd.Series:
        """Get facility data for a site, including sister sites."""
        if self.facilities_data is None:
            return None
            
        site = str(site).strip().upper()
        
        # Find the row that contains this site (including sister sites)
        for idx, facility_name in enumerate(self.facilities_data['name']):
            if self._is_site_in_group(site, facility_name):
                return self.facilities_data.iloc[idx]
        return None
    
    def _format_site_name_display(self, facility_name: str) -> str:
        """Format site name for display with main site on top, sisters below."""
        if pd.isna(facility_name):
            return str(facility_name)
            
        facility_name = str(facility_name).strip()
        
        # Split by " / " to get all sites
        sites = [site.strip() for site in facility_name.split(' / ')]
        
        if len(sites) <= 1:
            # Single site, return as-is
            return facility_name
        
        # Multiple sites: main site on top, sisters on second line
        main_site = sites[0]
        sister_sites = sites[1:]
        
        return f"{main_site}\n{' / '.join(sister_sites)}"

    def get_dwelling_info(self, site: str = "") -> Optional[Dict]:
        """Get dwelling information for a specific site."""
        if self.dwelling_data is None or not site:
            return None
            
        site = str(site).strip().upper()
        
        # Try exact match first
        site_data = self.dwelling_data[self.dwelling_data['Shared Yard'].str.upper() == site]
        
        if site_data.empty:
            # Try matching with the site code extraction method
            extracted_site = self._extract_site_code(site)
            site_data = self.dwelling_data[self.dwelling_data['Extracted_Site'] == extracted_site]
        
        if site_data.empty:
            # Try matching without trailing numbers
            base_site = re.sub(r'\d+$', '', site)
            site_data = self.dwelling_data[
                (self.dwelling_data['Extracted_Site'].str.startswith(base_site)) |
                (self.dwelling_data['Shared Yard'].str.upper().str.startswith(base_site))
            ]
        
        if site_data.empty:
            return {
                'Total Trailers': 0,
                '<24 Hrs': 0,
                '24-72 Hrs': 0,
                '72-168 Hrs': 0,
                '>168 Hrs': 0
            }
        
        # Convert numeric values to float and handle NaN
        result = {}
        for column in ['Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs']:
            value = site_data.iloc[0][column]
            result[column] = float(value) if pd.notna(value) else 0
        
        return result

    def get_site_info(self, site: str) -> Optional[Dict]:
        """Get site information including cart data and dwelling data if available."""
        if self.facilities_data is None:
            return None
            
        site = str(site).strip().upper()
        
        # Use new method to find facility (handles sister sites)
        facility_row = self._get_facility_by_site(site)
        if facility_row is None:
            # If exact match fails, try to find a match using extraction logic
            extracted_code = self._extract_site_code(site)
            facility_row = self._get_facility_by_site(extracted_code)
            if facility_row is None:
                return None
            site = extracted_code # Use the valid extracted code
            
        site_data = facility_row.to_dict()
        
        # Format the name for display
        site_data['display_name'] = self._format_site_name_display(site_data['name'])
        
        # Initialize cart data fields
        site_data.update({
            'is_cart_site': False,
            'Demand': 0,
            'Full Day Demand': 0,
            'Supply': 0,
            'Balance': 0
        })

        if self.cart_data is not None:
            # Check all sites in the group for cart data
            facility_name = facility_row['name']
            sites_in_group = [s.strip().upper() for s in str(facility_name).split(' / ')]
            
            total_demand = 0
            total_supply = 0
            total_full_day_demand = 0
            found_cart_data = False
            
            for group_site in sites_in_group:
                cart_info = self.cart_data[self.cart_data['Site'] == group_site]
                if not cart_info.empty:
                    found_cart_data = True
                    total_demand += cart_info['Demand'].sum()
                    total_supply += cart_info['Supply'].sum()
                    total_full_day_demand += cart_info['Full Day Demand'].sum()
            
            if found_cart_data:
                site_data.update({
                    'is_cart_site': True,
                    'Demand': total_demand,
                    'Full Day Demand': total_full_day_demand,
                    'Supply': total_supply,
                    'Balance': total_supply - total_demand
                })
                
        # Initialize dwelling data fields
        site_data.update({
            'has_dwelling_data': False,
            'Total Trailers': 0,
            '<24 Hrs': 0,
            '24-72 Hrs': 0,
            '72-168 Hrs': 0,
            '>168 Hrs': 0
        })

        # Add dwelling information if available (check all sites in group)
        if self.dwelling_data is not None:
            facility_name = facility_row['name']
            sites_in_group = [s.strip().upper() for s in str(facility_name).split(' / ')]
            
            total_trailers = 0
            total_24hrs = 0
            total_24_72hrs = 0
            total_72_168hrs = 0
            total_168hrs = 0
            found_dwelling_data = False
            
            for group_site in sites_in_group:
                dwelling_info = self.get_dwelling_info(group_site)
                if dwelling_info and any(dwelling_info.values()):
                    found_dwelling_data = True
                    total_trailers += dwelling_info.get('Total Trailers', 0)
                    total_24hrs += dwelling_info.get('<24 Hrs', 0)
                    total_24_72hrs += dwelling_info.get('24-72 Hrs', 0)
                    total_72_168hrs += dwelling_info.get('72-168 Hrs', 0)
                    total_168hrs += dwelling_info.get('>168 Hrs', 0)
            
            if found_dwelling_data:
                site_data.update({
                    'has_dwelling_data': True,
                    'Total Trailers': total_trailers,
                    '<24 Hrs': total_24hrs,
                    '24-72 Hrs': total_24_72hrs,
                    '72-168 Hrs': total_72_168hrs,
                    '>168 Hrs': total_168hrs
                })
                
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

    def get_high_balance_sites(self):
        """Get sites with non-negative balance (supply >= demand)."""
        all_sites = self.get_all_cart_sites()
        if not all_sites:
            return []
        
        # Filter for sites with balance >= 0
        high_balance_sites = [site for site in all_sites if site.get('Balance', 0) >= 0]
        
        # Sort by Total Trailers first (most trailers first), then by Balance
        return sorted(high_balance_sites, key=lambda x: (x.get('Total Trailers', 0), x.get('Balance', 0)), reverse=True)

    def get_negative_balance_sites(self):
        """Get sites with negative balance (demand > supply)."""
        all_sites = self.get_all_cart_sites()
        if not all_sites:
            return []
            
        # Filter for sites with balance < 0
        negative_balance_sites = [site for site in all_sites if site.get('Balance', 0) < 0]
        
        # Sort by most negative first
        return sorted(negative_balance_sites, key=lambda x: x.get('Balance', 0))

    def get_all_cart_sites(self) -> List[Dict]:
        """Get all sites with cart data, including balance and dwelling information."""
        if self.cart_data is None or self.facilities_data is None:
            return []
            
        sites_data = []
        processed_facilities = set()  # Track processed facility groups to avoid duplicates
        
        # Get unique sites from the cart data
        unique_sites = self.cart_data['Site'].unique()

        for site in unique_sites:
            if not site or pd.isna(site):
                continue
                
            # Use get_site_info to ensure all data is consistently fetched
            site_info = self.get_site_info(site)
            
            if site_info and site_info.get('is_cart_site', False):
                # Check if we've already processed this facility group
                facility_name = site_info.get('name', '')
                if facility_name in processed_facilities:
                    continue
                processed_facilities.add(facility_name)
                
                # Ensure all required keys are present
                final_site_data = {
                    'Site Name': site_info.get('display_name', site_info.get('name', site)),  # Use formatted display name
                    'Region': site_info.get('region', 'Unknown'),
                    'Demand': site_info.get('Demand', 0),
                    'Supply': site_info.get('Supply', 0),
                    'Balance': site_info.get('Balance', 0),
                    'Total Trailers': site_info.get('Total Trailers', 0),
                    '<24 Hrs': site_info.get('<24 Hrs', 0),
                    '24-72 Hrs': site_info.get('24-72 Hrs', 0),
                    '72-168 Hrs': site_info.get('72-168 Hrs', 0),
                    '>168 Hrs': site_info.get('>168 Hrs', 0)
                }
                sites_data.append(final_site_data)

        return sites_data

    def load_utilization_data(self, file_path):
        """Load yard utilization data from CSV with chunked processing."""
        try:
            # Import here to avoid circular imports and for processEvents
            from PyQt6.QtWidgets import QApplication
            
            print(f"Loading utilization data from: {file_path}")
            
            # Read CSV in chunks to maintain responsiveness
            chunk_size = 500  # Smaller chunks for utilization data
            chunks = []
            chunk_count = 0
            
            print("Reading utilization data in chunks...")
            for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                chunk_count += 1
                print(f"Processing utilization chunk {chunk_count} ({len(chunk)} rows)...")
                chunks.append(chunk)
                
                # Keep UI responsive
                if QApplication.instance():
                    QApplication.processEvents()
            
            # Combine all chunks
            print(f"Combining {len(chunks)} chunks of utilization data...")
            self.utilization_data = pd.concat(chunks, ignore_index=True)
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
            # Ensure required columns exist
            required_columns = ['Site Code', 'On Site Utilization', 'On Site Capacity', 'On Site Usage']
            if not all(col in self.utilization_data.columns for col in required_columns):
                raise ValueError("Missing required columns in utilization data")
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
                
            print("Converting utilization values...")
            # Convert utilization to float, handling any invalid values
            self.utilization_data['On Site Utilization'] = pd.to_numeric(
                self.utilization_data['On Site Utilization'],
                errors='coerce'
            )
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
            print("Creating extracted site codes...")
            # Create the Extracted_Site column
            self.utilization_data['Extracted_Site'] = self.utilization_data['Site Code'].apply(
                lambda x: self._extract_site_code(str(x))
            )
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
            print("Utilization data loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading utilization data: {str(e)}")
            return False

    def load_dwelling_data(self, file_path: str) -> bool:
        """Load and validate TEC dwelling data from CSV with chunked processing."""
        try:
            # Import here to avoid circular imports and for processEvents
            from PyQt6.QtWidgets import QApplication
            
            print(f"Loading dwelling data from: {file_path}")
            
            # Read CSV in chunks to maintain responsiveness
            chunk_size = 500  # Smaller chunks for dwelling data
            chunks = []
            chunk_count = 0
            
            print("Reading dwelling data in chunks...")
            for chunk in pd.read_csv(
                file_path,
                dtype={
                    'Shared Yard': str,
                    'Total Trailers': float,
                    '<24 Hrs': float,
                    '24-72 Hrs': float,
                    '72-168 Hrs': float,
                    '>168 Hrs': float
                },
                chunksize=chunk_size
            ):
                chunk_count += 1
                print(f"Processing dwelling chunk {chunk_count} ({len(chunk)} rows)...")
                chunks.append(chunk)
                
                # Keep UI responsive
                if QApplication.instance():
                    QApplication.processEvents()
            
            # Combine all chunks
            print(f"Combining {len(chunks)} chunks of dwelling data...")
            self.dwelling_data = pd.concat(chunks, ignore_index=True)
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
            print("Cleaning dwelling site codes...")
            # Clean up site codes and create extracted site codes
            self.dwelling_data['Shared Yard'] = self.dwelling_data['Shared Yard'].apply(
                lambda x: str(x).strip().upper() if pd.notna(x) else ''
            )
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
            print("Creating extracted site codes for dwelling data...")
            # Add extracted site codes for better matching
            self.dwelling_data['Extracted_Site'] = self.dwelling_data['Shared Yard'].apply(self._extract_site_code)
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
            print("Processing dwelling numeric columns...")
            # Fill NaN values with 0 for numeric columns
            numeric_columns = ['Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs']
            self.dwelling_data[numeric_columns] = self.dwelling_data[numeric_columns].fillna(0)
            
            # Keep UI responsive
            if QApplication.instance():
                QApplication.processEvents()
            
            print("Dwelling data loaded successfully")
            return True
            
        except Exception as e:
            print(f"Error loading dwelling data: {str(e)}")
            self.dwelling_data = None
            return False

    def _extract_site_code(self, site_code: str) -> str:
        """Extract the site code from the utilization format to match cart data format."""
        # Remove any quotes and clean the string
        site_code = site_code.strip('"').strip().upper()
        
        # Try to extract the site code using various patterns
        patterns = [
            # Pattern for codes like AGS1, JAX2, etc.
            r'([A-Z]{3}\d+)',
            # Pattern for AACT-XXX format
            r'AACT-([A-Z]{3})',
            # Pattern for rail codes
            r'RAIL_(\w+)',
            # Pattern for NSD codes
            r'NSD_(\w+)',
            # Pattern for codes with underscores (take first part)
            r'^([^_]+)',
            # Pattern for codes with dashes (take first part)
            r'^([^-]+)',
            # Pattern for any alphanumeric sequence
            r'([A-Z0-9]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, site_code)
            if match:
                extracted = match.group(1)
                # If it's a 3-letter code without numbers, try to find a number after it
                if len(extracted) == 3 and extracted.isalpha():
                    number_match = re.search(r'\d+', site_code)
                    if number_match:
                        extracted += number_match.group(0)
                return extracted
        
        # If no pattern matches, return the original code
        return site_code

    def get_utilization_info(self, site: str = "") -> Optional[Dict]:
        """Get utilization information for a specific site."""
        if self.utilization_data is None:
            return None
            
        site = str(site).strip().upper()
        if not site:
            return None
            
        # Try exact match first
        site_data = self.utilization_data[self.utilization_data['Site Code'].str.upper() == site]
        
        if site_data.empty:
            # Try to match against the extracted site codes
            site_data = self.utilization_data[self.utilization_data['Extracted_Site'] == site]
        
        if site_data.empty:
            # Try matching without trailing numbers
            base_site = re.sub(r'\d+$', '', site)
            site_data = self.utilization_data[
                (self.utilization_data['Extracted_Site'].str.startswith(base_site)) |
                (self.utilization_data['Site Code'].str.upper().str.startswith(base_site))
            ]
        
        if site_data.empty:
            # Try matching with just the first part of the site code (before any separator)
            base_site = re.split(r'[_\-]', site)[0].strip()
            site_data = self.utilization_data[
                (self.utilization_data['Extracted_Site'].str.startswith(base_site)) |
                (self.utilization_data['Site Code'].str.upper().str.startswith(base_site))
            ]
        
        if site_data.empty:
            return None
            
        # Get the first matching row
        row = site_data.iloc[0]
        
        # Check if any of the required values are NaN
        if (pd.isna(row['On Site Utilization']) or 
            pd.isna(row['On Site Capacity']) or 
            pd.isna(row['On Site Usage'])):
            return None
            
        return {
            'Site Code': site,
            'On Site Utilization': float(row['On Site Utilization']),
            'On Site Capacity': float(row['On Site Capacity']),
            'On Site Usage': float(row['On Site Usage'])
        }

    def get_all_utilization_data(self) -> List[Dict]:
        """Get utilization information for all sites."""
        if self.utilization_data is None:
            return []
            
        result = []
        for _, row in self.utilization_data.iterrows():
            # Skip rows with NaN values or 0 utilization
            utilization = row['On Site Utilization']
            capacity = row['On Site Capacity']
            usage = row['On Site Usage']
            
            # Check each value individually
            if (isinstance(utilization, float) and np.isnan(utilization) or
                isinstance(capacity, float) and np.isnan(capacity) or
                isinstance(usage, float) and np.isnan(usage) or
                utilization == 0):
                continue
                
            result.append({
                'Site Code': row['Site Code'],
                'On Site Utilization': float(utilization),
                'On Site Capacity': float(capacity),
                'On Site Usage': float(usage)
            })
        return result
