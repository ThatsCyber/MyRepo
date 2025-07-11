from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QLabel, QTextEdit,
    QTableWidget, QTableWidgetItem, QComboBox,
    QFileDialog, QMessageBox, QApplication, QSplitter,
    QCheckBox, QHeaderView, QTabWidget
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from qt_material import apply_stylesheet
from data_handler import DataHandler
from proximity import ProximityAnalyzer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Facility Management")
        self.setMinimumSize(800, 500)
        
        # Initialize data handlers
        self.data_handler = DataHandler()
        self.proximity_analyzer = ProximityAnalyzer(self.data_handler)
        
        # Set up the main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setSpacing(3)  # Even smaller spacing between elements
        layout.setContentsMargins(5, 5, 5, 5)  # Smaller margins
        
        # Set application-wide font
        self._set_application_font()
        
        # Create file section in header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(3)  # Smaller spacing
        header_layout.setContentsMargins(2, 2, 2, 2)  # Smaller margins
        
        # File section
        file_layout = QHBoxLayout()
        file_layout.setSpacing(5)  # Reduce spacing
        
        # Set a fixed width for all buttons to ensure they fit nicely
        button_width = 150  # Adjust this value if needed for better fit
        
        # Left button - Facilities (stays in the same position)
        self.load_facilities_btn = QPushButton("Load Facilities Excel")
        self.load_facilities_btn.setFixedHeight(25)  # Make button smaller
        self.load_facilities_btn.setFixedWidth(button_width)
        self.load_facilities_btn.clicked.connect(self._load_facilities_file)
        file_layout.addWidget(self.load_facilities_btn)
        
        # Middle button - Supply & Demand
        self.load_cart_btn = QPushButton("Load Cart Data CSV")
        self.load_cart_btn.setFixedHeight(25)  # Make button smaller
        self.load_cart_btn.setFixedWidth(button_width)
        self.load_cart_btn.clicked.connect(self._load_cart_file)
        file_layout.addWidget(self.load_cart_btn)
        
        # Right button - Yard Utilization
        self.load_utilization_btn = QPushButton("Load Yard Utilization")
        self.load_utilization_btn.setFixedHeight(25)  # Make button smaller
        self.load_utilization_btn.setFixedWidth(button_width)
        self.load_utilization_btn.clicked.connect(self._load_utilization_file)
        file_layout.addWidget(self.load_utilization_btn)
        
        header_layout.addLayout(file_layout)
        layout.addLayout(header_layout)
        
        # Apply dark theme
        apply_stylesheet(self, theme='dark_amber.xml')
        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QPushButton { background-color: #ff9900; color: black; }
            QTableWidget { gridline-color: #404040; }
            QTextEdit, QLineEdit {
                selection-background-color: #2a5a8c;
                selection-color: white;
            }
            QTableWidget::item:selected {
                background-color: #2a5a8c;
            }
            QHeaderView::section {
                padding: 2px;
                background-color: #2b2b2b;
            }
            QSplitter::handle {
                background-color: #404040;
            }
            QSplitter::handle:horizontal {
                width: 4px;
            }
            QSplitter::handle:vertical {
                height: 4px;
            }
        """)
        
        # Create main vertical splitter
        self.main_splitter = QSplitter(Qt.Orientation.Vertical)
        self.main_splitter.setHandleWidth(4)  # Make handles more visible
        layout.addWidget(self.main_splitter)
        
        # Top section (input and output)
        top_widget = QWidget()
        top_layout = QVBoxLayout(top_widget)
        top_layout.setSpacing(3)  # Smaller spacing
        self._create_input_section(top_layout)
        self._create_output_section(top_layout)
        self.main_splitter.addWidget(top_widget)
        
        # Middle section (site info only)
        self.site_info_table = QTableWidget()
        self._setup_table(self.site_info_table)
        self.main_splitter.addWidget(self.site_info_table)
        
        # Bottom section (proximity and cart balance)
        bottom_splitter = QSplitter(Qt.Orientation.Horizontal)
        bottom_splitter.setHandleWidth(4)  # Make handles more visible
        
        # Proximity section
        proximity_widget = QWidget()
        proximity_layout = QVBoxLayout(proximity_widget)
        proximity_layout.setSpacing(3)  # Smaller spacing
        self._create_proximity_section(proximity_layout)
        bottom_splitter.addWidget(proximity_widget)
        
        # Cart balance section with tabs
        cart_balance_widget = QWidget()
        cart_layout = QVBoxLayout(cart_balance_widget)
        cart_layout.setSpacing(3)  # Smaller spacing
        self._create_cart_balance_section(cart_layout)
        bottom_splitter.addWidget(cart_balance_widget)
        
        self.main_splitter.addWidget(bottom_splitter)
        
        # Set the initial sizes for the main splitter sections
        # Format: [top_section, middle_section, bottom_section]
        self.main_splitter.setSizes([100, 250, 350])  # Give more height to the middle section
        
        # Load initial data if available
        self._load_initial_data()
        
    def _set_application_font(self):
        """Set a smaller font size for the entire application."""
        try:
            default_font = QFont("Arial", 7)
            # Apply font to the main window and its children
            self.setFont(default_font)
            for widget in self.findChildren(QWidget):
                if widget is not None:
                    widget.setFont(default_font)
        except Exception as e:
            print(f"Warning: Could not set application font: {str(e)}")
        
    def _setup_table(self, table):
        """Setup common table properties."""
        try:
            # Set fonts
            content_font = QFont("Arial", 7)
            header_font = QFont("Arial", 6)  # Keep small font for better fit
            header_font.setBold(True)
            
            table.setFont(content_font)
            
            # Configure headers if they exist
            header = table.horizontalHeader()
            if header is not None:
                header.setFont(header_font)
                header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            
            vert_header = table.verticalHeader()
            if vert_header is not None:
                vert_header.setFont(content_font)
                vert_header.setDefaultSectionSize(30)
            
            # Make table read-only
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            
            # Style the table with minimal padding and consistent dark theme colors
            table.setStyleSheet("""
                QTableWidget {
                    gridline-color: #404040;
                    border: none;
                    background-color: #2b2b2b;
                    alternate-background-color: #323232;
                    color: #ffffff;
                }
                QTableWidget::item {
                    padding: 1px;
                    background-color: #2b2b2b;
                    color: #ffffff;
                }
                QTableWidget::item:selected {
                    background-color: #2a5a8c;
                    color: #ffffff;
                }
                QHeaderView::section {
                    padding: 2px;
                    background-color: #2b2b2b;
                    color: #ffffff;
                    border: none;
                }
                QHeaderView {
                    background-color: #2b2b2b;
                }
            """)
            
            # Add pixel-by-pixel horizontal scrolling
            table.setHorizontalScrollMode(QTableWidget.ScrollMode.ScrollPerPixel)
        except Exception as e:
            print(f"Warning: Could not setup table properties: {str(e)}")
        
    def _set_table_column_widths(self, table, widths):
        """Set the width of each column in the table."""
        for col, width in enumerate(widths):
            table.setColumnWidth(col, width)
            
    def _get_utilization_color(self, utilization_percentage):
        """
        Returns a QColor based on utilization percentage:
        - 0-89.99%: White
        - 90-95.99%: Orange
        - 96-99.99%: Orange-Red gradient
        - 100%+: Red
        """
        # Add a small epsilon to handle floating point comparison
        epsilon = 0.0001
        
        if utilization_percentage >= 100:
            return QColor(255, 0, 0)  # Pure red
        elif utilization_percentage >= 96:
            # Calculate gradient between orange and red
            # As we go from 96 to 99, we reduce the green component
            green = int(140 - (140 * (utilization_percentage - 96) / 3))
            return QColor(255, green, 0)
        elif utilization_percentage >= (90 - epsilon):  # Include values very close to 90
            return QColor(255, 140, 0)  # Orange
        else:
            return QColor(255, 255, 255)  # White
            
    def _create_input_section(self, parent_layout):
        """Create input section with site input and action buttons."""
        input_layout = QVBoxLayout()
        input_layout.setSpacing(3)  # Smaller spacing
        input_layout.setContentsMargins(2, 2, 2, 2)  # Smaller margins
        
        # Site input field
        input_field_layout = QHBoxLayout()
        self.site_input = QTextEdit()
        self.site_input.setPlaceholderText("Enter site name")
        self.site_input.setMaximumHeight(80)  # Smaller height
        self.site_input.setFont(QFont("Arial", 7))  # Smaller font
        self.site_input.setStyleSheet("""
            QTextEdit {
                selection-background-color: #2a5a8c;
                selection-color: white;
            }
        """)
        input_field_layout.addWidget(self.site_input)
        
        # Action buttons in vertical layout
        button_layout = QVBoxLayout()
        button_layout.setSpacing(2)  # Minimal spacing between buttons
        
        for btn_text, action in [
            ("Depart TEC", lambda: self._process_site_action("DEPART")),
            ("Need TEC", lambda: self._process_site_action("NEED")),
            ("Check Site Info", self._check_cart_site)
        ]:
            btn = QPushButton(btn_text)
            btn.setFixedHeight(22)  # Smaller button height
            btn.setFont(QFont("Arial", 7))  # Smaller font
            btn.clicked.connect(action)
            button_layout.addWidget(btn)
        
        input_field_layout.addLayout(button_layout)
        input_layout.addLayout(input_field_layout)
        parent_layout.addLayout(input_layout)
        
    def _create_output_section(self, parent_layout):
        """Create output text area."""
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setMaximumHeight(80)  # Smaller height
        self.output_text.setFont(QFont("Arial", 7))  # Smaller font
        self.output_text.setStyleSheet("""
            QTextEdit {
                selection-background-color: #2a5a8c;
                selection-color: white;
            }
        """)
        parent_layout.addWidget(self.output_text)
        
    def _create_site_info_section(self, parent_layout):
        """Create site information table."""
        self.site_info_table = QTableWidget()
        self.site_info_table.setMaximumHeight(200)
        parent_layout.addWidget(self.site_info_table)
        
    def _create_proximity_section(self, parent_layout):
        """Create proximity analysis section."""
        proximity_layout = QVBoxLayout()
        proximity_layout.setSpacing(3)  # Smaller spacing
        
        # Controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(5)  # Reduce spacing
        
        # Number of sites combo
        limit_label = QLabel("Number of sites:")
        limit_label.setFont(QFont("Arial", 7))
        controls_layout.addWidget(limit_label)
        
        self.limit_combo = QComboBox()
        self.limit_combo.setFont(QFont("Arial", 7))
        self.limit_combo.addItems([str(i) for i in range(5, 51, 5)])  # 5 to 50 in steps of 5
        self.limit_combo.setMaxVisibleItems(4)  # Show only 4 items at a time
        self.limit_combo.setStyleSheet("""
            QComboBox {
                max-height: 20px;
            }
            QComboBox QAbstractItemView {
                selection-background-color: #2a5a8c;
                selection-color: white;
                min-height: 100px;  /* Ensure dropdown is tall enough to scroll */
            }
        """)
        controls_layout.addWidget(self.limit_combo)
        
        # Cart sites only checkbox
        self.cart_sites_only = QCheckBox("Cart sites only")
        self.cart_sites_only.setFont(QFont("Arial", 7))
        controls_layout.addWidget(self.cart_sites_only)
        
        # Find nearby button with smaller font
        self.find_nearby_btn = QPushButton("Find Nearby Sites")
        self.find_nearby_btn.setFont(QFont("Arial", 7))
        self.find_nearby_btn.setFixedHeight(22)  # Make button smaller
        self.find_nearby_btn.clicked.connect(self._find_nearby_sites)
        controls_layout.addWidget(self.find_nearby_btn)
        
        proximity_layout.addLayout(controls_layout)
        
        # Results table
        self.proximity_table = QTableWidget()
        self._setup_table(self.proximity_table)  # This already sets small font
        proximity_layout.addWidget(self.proximity_table)
        
        parent_layout.addLayout(proximity_layout)

    def _create_cart_balance_section(self, parent_layout):
        """Create section for displaying cart balance information with tabs."""
        # Create tab widget
        self.cart_tabs = QTabWidget()
        self.cart_tabs.setFont(QFont("Arial", 7))
        
        # Create tabs
        negative_tab = QWidget()
        positive_tab = QWidget()
        
        negative_layout = QVBoxLayout(negative_tab)
        positive_layout = QVBoxLayout(positive_tab)
        
        # Create tables
        self.negative_balance_table = QTableWidget()
        self.positive_balance_table = QTableWidget()
        
        # Set up tables
        for table in [self.negative_balance_table, self.positive_balance_table]:
            self._setup_table(table)
            table.setColumnCount(8)  # Updated column count
            table.setHorizontalHeaderLabels([
                'Site Name', 'Region', 'Demand', 'Supply', 'Balance',
                'Utilization', 'Capacity', 'Usage'
            ])
            # Set widths to fit column titles
            self._set_table_column_widths(table, [
                85,   # Site Name
                65,   # Region
                65,   # Demand
                65,   # Supply
                65,   # Balance
                85,   # Utilization
                75,   # Capacity
                65    # Usage
            ])
            
            # Ensure headers are word-wrapped and tall enough
            try:
                header = table.horizontalHeader()
                if header is not None:
                    header.setMinimumHeight(30)  # Make header taller
                    header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align headers
                    # Allow columns to be resized by user
                    header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
            except Exception as e:
                print(f"Warning: Could not configure table header: {str(e)}")
        
        negative_layout.addWidget(self.negative_balance_table)
        positive_layout.addWidget(self.positive_balance_table)
        
        # Add tabs to widget
        self.cart_tabs.addTab(negative_tab, "Negative Balance")
        self.cart_tabs.addTab(positive_tab, "High Balance")
        
        parent_layout.addWidget(self.cart_tabs)
        
        # Initial update
        self._update_cart_balance_tables()
        
    def _update_cart_balance_tables(self):
        """Update both negative and positive balance tables."""
        if self.data_handler.cart_data is None:
            return
            
        # Get all sites with cart data
        sites_data = self.data_handler.get_all_cart_sites()
        
        # Split into negative and positive balance
        negative_sites = [site for site in sites_data if site['Balance'] < 0]
        positive_sites = [site for site in sites_data if site['Balance'] > 0]
        
        # Sort both lists by balance
        negative_sites.sort(key=lambda x: x['Balance'])  # Most negative first
        positive_sites.sort(key=lambda x: x['Balance'], reverse=True)  # Most positive first
        
        # Update negative balance table
        self.negative_balance_table.setRowCount(len(negative_sites))
        self._fill_balance_table(self.negative_balance_table, negative_sites)
        
        # Update positive balance table
        self.positive_balance_table.setRowCount(len(positive_sites))
        self._fill_balance_table(self.positive_balance_table, positive_sites)
        
    def _fill_balance_table(self, table, sites_data):
        """Helper method to fill a balance table with site data."""
        font = QFont("Arial", 7)
        
        for row, site in enumerate(sites_data):
            # Site Name
            item = QTableWidgetItem(site['Site Name'])
            item.setFont(font)
            table.setItem(row, 0, item)
            
            # Region
            item = QTableWidgetItem(site['Region'])
            item.setFont(font)
            table.setItem(row, 1, item)
            
            # Demand
            item = QTableWidgetItem(str(site['Demand']))
            item.setFont(font)
            table.setItem(row, 2, item)
            
            # Supply
            item = QTableWidgetItem(str(site['Supply']))
            item.setFont(font)
            table.setItem(row, 3, item)
            
            # Balance
            item = QTableWidgetItem(str(site['Balance']))
            item.setFont(font)
            if site['Balance'] < 0:
                item.setBackground(QColor(255, 0, 0))
            table.setItem(row, 4, item)
            
            # Add utilization data
            utilization_info = self.data_handler.get_utilization_info(site['Site Name'])
            if utilization_info:
                # Utilization (as percentage)
                if utilization_info.get('On Site Utilization') is not None:
                    try:
                        utilization = float(utilization_info['On Site Utilization'])
                        utilization_percentage = utilization * 100
                        value = f"{utilization_percentage:.2f}%"
                        item = QTableWidgetItem(value)
                        item.setFont(QFont("Arial", 7))
                        # Use our color helper method for the text color
                        color = self._get_utilization_color(utilization_percentage)
                        item.setForeground(color)
                    except (ValueError, TypeError):
                        value = 'N/A'
                        item = QTableWidgetItem(value)
                        item.setFont(QFont("Arial", 7))
                else:
                    value = 'N/A'
                    item = QTableWidgetItem(value)
                    item.setFont(QFont("Arial", 7))
                table.setItem(row, 5, item)
                
                # Capacity
                value = utilization_info.get('On Site Capacity')
                if value == 'N/A' or value is None:
                    value = 'N/A'
                item = QTableWidgetItem(str(value))
                item.setFont(font)
                table.setItem(row, 6, item)
                
                # Usage
                value = utilization_info.get('On Site Usage')
                if value == 'N/A' or value is None:
                    value = 'N/A'
                item = QTableWidgetItem(str(value))
                item.setFont(font)
                table.setItem(row, 7, item)
            else:
                # Fill with N/A if no utilization data
                for col in range(5, 8):
                    item = QTableWidgetItem('N/A')
                    item.setFont(font)
                    table.setItem(row, col, item)
        
        # Reapply column widths
        self._set_table_column_widths(table, [
            85,   # Site Name
            65,   # Region
            65,   # Demand
            65,   # Supply
            65,   # Balance
            85,   # Utilization
            75,   # Capacity
            65    # Usage
        ])

    def _create_utilization_section(self, parent_layout):
        """Create the yard utilization section with a table."""
        # Create and set up the table
        self.utilization_table = QTableWidget()
        self._setup_table(self.utilization_table)
        
        # Set up columns
        columns = ['Site Code', 'Utilization', 'Capacity', 'Usage']
        self.utilization_table.setColumnCount(len(columns))
        self.utilization_table.setHorizontalHeaderLabels(columns)
        
        # Set column widths
        self._set_table_column_widths(
            self.utilization_table,
            [100, 200, 80, 80]  # Wider Utilization column for progress bar
        )
        
        parent_layout.addWidget(self.utilization_table)

    def _update_utilization_table(self):
        """Update the yard utilization table with current data."""
        if not hasattr(self, 'utilization_table'):
            return
            
        # Get all utilization data
        utilization_data = self.data_handler.get_all_utilization_data()
        
        # Clear existing rows
        self.utilization_table.setRowCount(0)
        
        # Add data to table
        for data in utilization_data:
            row = self.utilization_table.rowCount()
            self.utilization_table.insertRow(row)
            
            # Site Code
            site_item = QTableWidgetItem(data['Site Code'])
            self.utilization_table.setItem(row, 0, site_item)
            
            # Utilization (as progress bar)
            utilization = data['On Site Utilization']
            progress_widget = QWidget()
            progress_layout = QHBoxLayout(progress_widget)
            progress_layout.setContentsMargins(4, 2, 4, 2)
            
            # Create progress bar background
            bar_width = 150
            bar_height = 15
            
            # Calculate width of filled portion
            filled_width = int(min(max(utilization * 100, 0), 100) * bar_width / 100)
            
            # Create filled portion
            filled = QWidget()
            filled.setFixedSize(filled_width, bar_height)
            filled.setStyleSheet(
                f"background-color: {'red' if utilization > 1 else 'green'}; "
                "border-radius: 2px;"
            )
            
            # Create background
            background = QWidget()
            background.setFixedSize(bar_width, bar_height)
            background.setStyleSheet(
                "background-color: #404040; border-radius: 2px;"
            )
            
            # Add percentage label
            label = QLabel(f"{utilization:.2%}")
            label.setStyleSheet("color: white; background: transparent;")
            
            # Layout the progress bar
            progress_layout.addWidget(background)
            progress_layout.addWidget(filled)
            progress_layout.addWidget(label)
            progress_layout.addStretch()
            
            self.utilization_table.setCellWidget(row, 1, progress_widget)
            
            # Capacity
            capacity_item = QTableWidgetItem(str(int(data['On Site Capacity'])))
            self.utilization_table.setItem(row, 2, capacity_item)
            
            # Usage
            usage_item = QTableWidgetItem(str(int(data['On Site Usage'])))
            self.utilization_table.setItem(row, 3, usage_item)
        
        # Reapply column widths instead of resizing to contents
        self._set_table_column_widths(
            self.utilization_table,
            [100, 200, 80, 80]  # Wider Utilization column for progress bar
        )
        
    def _load_initial_data(self):
        """Load initial data files if available."""
        # Removed automatic data loading
        pass
            
    def _load_facilities_file(self):
        """Load facilities Excel file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Facilities Excel File", "", "Excel Files (*.xlsx *.xlsm)"
        )
        if file_path and self.data_handler.load_facilities_data(file_path):
            QMessageBox.information(self, "Success", "Facilities data loaded successfully!")
        
    def _load_cart_file(self):
        """Load cart data file and update tables."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Cart Data CSV",
            "",
            "CSV Files (*.csv)"
        )
        
        if not file_path:
            return
            
        # Try to load the data
        success = self.data_handler.load_cart_data(file_path)
        
        if success:
            self._update_cart_balance_tables()
            QMessageBox.information(self, "Success", "Cart data loaded successfully!")
        else:
            # Show detailed error from data handler's print statements
            error_msg = (
                "Failed to load cart data. Common issues:\n\n"
                "1. Check that your CSV file has these columns:\n"
                "   - Site\n"
                "   - Region\n"
                "   - Demand\n"
                "   - Supply\n"
                "   - Balance\n"
                "   - Full Day Demand\n\n"
                "2. Make sure the data format is correct\n"
                "3. Check if the file is not empty or corrupted\n\n"
                "Please check the terminal/console for detailed error messages."
            )
            QMessageBox.warning(self, "Error", error_msg)

    def _load_utilization_file(self):
        """Load yard utilization data from a CSV file."""
        try:
            # Open file dialog
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Load Yard Utilization Data",
                "",
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if not file_path:  # User cancelled
                return
                
            # Load the data
            success = self.data_handler.load_utilization_data(file_path)
            
            if success:
                # Update tables
                self._update_cart_balance_tables()
                QMessageBox.information(self, "Success", "Utilization data loaded successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to load utilization data")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load utilization data: {str(e)}")
            
    def _process_site_action(self, action: str):
        """Process site action (DEPART or NEED) for multiple sites."""
        input_text = self.site_input.toPlainText().strip()
        if not input_text:
            return
            
        # Split input into lines and process each site
        sites = [site.strip() for site in input_text.split('\n') if site.strip()]
        outputs = []
        
        for site in sites:
            if "->" in site:
                # Pass the action type to process_site_to_site
                output = self.data_handler.process_site_to_site(site, action)
            else:
                output = self.data_handler.format_output(site, action)
            outputs.append(output)
            
        # Update output text with all results
        self.output_text.setText('\n'.join(outputs))
        
        # Update site info table for multiple sites
        self._update_site_info_multiple(sites)
        
    def _check_cart_site(self):
        """Check if sites are cart sites and display information."""
        input_text = self.site_input.toPlainText().strip()
        if not input_text:
            return
            
        # Process both sides of arrows for site pairs
        all_sites = []
        for line in input_text.split('\n'):
            if not line.strip():
                continue
            if "->" in line:
                start_site, end_site = line.strip().split("->")
                all_sites.extend([start_site.strip(), end_site.strip()])
            else:
                all_sites.append(line.strip())
                
        # Remove duplicates while preserving order
        seen = set()
        unique_sites = [x for x in all_sites if not (x in seen or seen.add(x))]
        outputs = []
        
        for site in unique_sites:
            site_info = self.data_handler.get_site_info(site)
            
            if not site_info:
                outputs.append(f"Invalid site: {site}")
                continue
                
            if site_info.get('is_cart_site'):
                outputs.append(
                    f"Site: {site}\n"
                    f"Demand: {site_info['Demand']}\n"
                    f"Supply: {site_info['Supply']}\n"
                    f"Balance: {site_info['Balance']}\n"
                )
            else:
                outputs.append(f"{site} is not a cart site\n")
                
        self.output_text.setText('\n'.join(outputs))
        self._update_site_info_multiple(input_text.split('\n'))
        
    def _update_site_info_multiple(self, sites: list):
        """Update site information table with multiple sites."""
        if not sites:
            return
            
        # Split input into lines and process each line
        lines = [line.strip() for line in sites if line.strip()]
        
        # Track consecutive appearances for start and end positions separately
        start_site_appearances = {}  # site -> list of line numbers where it appears as start
        end_site_appearances = {}    # site -> list of line numbers where it appears as end
        single_site_appearances = {} # for lines without arrows
        
        for line_num, line in enumerate(lines):
            if "->" in line:
                start_site, end_site = line.split("->")
                start_site = start_site.strip()
                end_site = end_site.strip()
                
                if start_site not in start_site_appearances:
                    start_site_appearances[start_site] = []
                start_site_appearances[start_site].append(line_num)
                
                if end_site not in end_site_appearances:
                    end_site_appearances[end_site] = []
                end_site_appearances[end_site].append(line_num)
            else:
                site = line.strip()
                if site not in single_site_appearances:
                    single_site_appearances[site] = []
                single_site_appearances[site].append(line_num)
        
        # Function to check if appearances are consecutive
        def has_consecutive_appearances(line_numbers):
            if len(line_numbers) <= 1:
                return False
            sorted_lines = sorted(line_numbers)
            for i in range(1, len(sorted_lines)):
                if sorted_lines[i] - sorted_lines[i-1] == 1:
                    return True
            return False
        
        # Create list of sites to exclude based on consecutive appearances in the same position
        sites_to_exclude = set()
        for site, line_nums in start_site_appearances.items():
            if has_consecutive_appearances(line_nums):
                sites_to_exclude.add(site)
                
        for site, line_nums in end_site_appearances.items():
            if has_consecutive_appearances(line_nums):
                sites_to_exclude.add(site)
                
        for site, line_nums in single_site_appearances.items():
            if has_consecutive_appearances(line_nums):
                sites_to_exclude.add(site)
        
        # Build final list of sites to display
        all_sites = []
        for line in lines:
            if "->" in line:
                start_site, end_site = line.split("->")
                start_site = start_site.strip()
                end_site = end_site.strip()
                
                if start_site not in sites_to_exclude and start_site not in all_sites:
                    all_sites.append(start_site)
                if end_site not in sites_to_exclude and end_site not in all_sites:
                    all_sites.append(end_site)
            else:
                site = line.strip()
                if site not in sites_to_exclude and site not in all_sites:
                    all_sites.append(site)
                
        # Use the filtered list
        unique_sites = all_sites
            
        # Set up columns (added utilization columns)
        columns = [
            'Name', 'Type', 'Address', 'Region', 
            'Demand', 'Full Day Demand', 'Supply', 'Balance',
            'Utilization', 'Capacity', 'Usage'
        ]
        self.site_info_table.setColumnCount(len(columns))
        self.site_info_table.setHorizontalHeaderLabels(columns)
        
        # Set column widths
        self._set_table_column_widths(
            self.site_info_table,
            [80, 70, 200, 70, 70, 100, 70, 75, 100, 70, 70]  # Added widths for new columns
        )
        
        # Clear existing rows
        self.site_info_table.setRowCount(0)
        
        # Add site information
        for site in unique_sites:
            site_info = self.data_handler.get_site_info(site)
            if site_info:
                row = self.site_info_table.rowCount()
                self.site_info_table.insertRow(row)
                
                # Add items with smaller font
                font = QFont("Arial", 9)
                
                # Basic info columns
                basic_info = {
                    'Name': site.upper(),
                    'Type': site_info.get('type', ''),
                    'Address': site_info.get('address', ''),
                    'Region': site_info.get('region', ''),
                }
                
                # Demand info columns with default values
                demand_info = {
                    'Demand': site_info.get('Demand', 0),
                    'Full Day Demand': site_info.get('Full Day Demand', 0),
                    'Supply': site_info.get('Supply', 0),
                    'Balance': site_info.get('Balance', 0)
                }
                
                # Get utilization info
                utilization_info = self.data_handler.get_utilization_info(site)
                if utilization_info:
                    utilization_data = {
                        'Utilization': utilization_info['On Site Utilization'],
                        'Capacity': utilization_info['On Site Capacity'],
                        'Usage': utilization_info['On Site Usage']
                    }
                else:
                    utilization_data = {
                        'Utilization': 'N/A',
                        'Capacity': 'N/A',
                        'Usage': 'N/A'
                    }
                
                # Combine all info
                all_info = {**basic_info, **demand_info, **utilization_data}
                
                # Fill the row
                for col, column_name in enumerate(columns):
                    value = all_info[column_name]
                    
                    if column_name == 'Utilization':
                        # Create progress bar for utilization
                        progress_widget = QWidget()
                        progress_layout = QHBoxLayout(progress_widget)
                        progress_layout.setContentsMargins(4, 2, 4, 2)
                        
                        if value == 'N/A':
                            label = QLabel('N/A')
                            label.setStyleSheet("color: white; background: transparent;")
                        else:
                            utilization = float(value)
                            utilization_percentage = utilization * 100
                            label = QLabel(f"{utilization_percentage:.2f}%")
                            # Use our color helper method for the text color
                            color = self._get_utilization_color(utilization_percentage)
                            label.setStyleSheet(
                                f"color: rgb({color.red()}, {color.green()}, {color.blue()}); "
                                "background: transparent;"
                            )
                        progress_layout.addWidget(label)
                        
                        self.site_info_table.setCellWidget(row, col, progress_widget)
                    else:
                        item = QTableWidgetItem(str(value))
                        item.setFont(font)
                        
                        # Highlight negative balance
                        if column_name == 'Balance' and float(value) < 0:
                            item.setBackground(QColor(255, 0, 0))
                            
                        self.site_info_table.setItem(row, col, item)
                
        self.site_info_table.resizeColumnsToContents()
        
    def _find_nearby_sites(self):
        """Find nearby sites."""
        site = self.site_input.toPlainText().strip().split("->")[0]
        limit = int(self.limit_combo.currentText())
        cart_sites_only = self.cart_sites_only.isChecked()
        
        # Get nearby sites, passing cart_sites_only flag
        nearby_sites = self.proximity_analyzer.find_nearest_sites(
            site=site,
            limit=limit,
            cart_sites_only=cart_sites_only
        )
        
        if not nearby_sites:
            if cart_sites_only:
                self.output_text.setText("No nearby cart sites found")
            else:
                self.output_text.setText("No nearby sites found or invalid site")
            return
            
        # Set up table
        self.proximity_table.setRowCount(len(nearby_sites))
        
        # Always include all columns
        columns = ['name', 'address', 'state', 'region', 'distance']
        
        # Add cart data and utilization columns
        columns.extend(['Demand', 'Supply', 'Balance', 'Utilization', 'Capacity', 'Usage'])
            
        self.proximity_table.setColumnCount(len(columns))
        self.proximity_table.setHorizontalHeaderLabels(columns)
        
        # Set widths to fit column titles and values
        widths = [
            85,   # name
            200,  # address (keep wider for addresses)
            65,   # state
            65,   # region
            90,   # distance (increased for decimal numbers)
            80,   # Demand (increased for numbers)
            80,   # Supply (increased for numbers)
            80,   # Balance (increased for numbers)
            85,   # Utilization (for percentage)
            90,   # Capacity (increased for larger numbers like 337.0)
            80    # Usage (increased for larger numbers like 229.0)
        ]
            
        self._set_table_column_widths(self.proximity_table, widths)
        
        # Fill data
        for row, site_info in enumerate(nearby_sites):
            for col, field in enumerate(columns):
                value = site_info.get(field, '')
                
                # Special handling for utilization data
                if field in ['Utilization', 'Capacity', 'Usage']:
                    utilization_info = self.data_handler.get_utilization_info(site_info['name'])
                    if utilization_info:
                        if field == 'Utilization':
                            try:
                                utilization = float(utilization_info['On Site Utilization'])
                                utilization_percentage = utilization * 100
                                value = f"{utilization_percentage:.2f}%"
                                item = QTableWidgetItem(value)
                                item.setFont(QFont("Arial", 7))
                                # Use our color helper method for the text color
                                color = self._get_utilization_color(utilization_percentage)
                                item.setForeground(color)
                            except (ValueError, TypeError):
                                value = 'N/A'
                                item = QTableWidgetItem(value)
                                item.setFont(QFont("Arial", 7))
                        else:
                            value = utilization_info.get(f'On Site {field}', 'N/A')
                            if value == 'N/A' or value is None:
                                value = 'N/A'
                            item = QTableWidgetItem(str(value))
                            item.setFont(QFont("Arial", 7))
                    else:
                        value = 'N/A'
                        item = QTableWidgetItem(value)
                        item.setFont(QFont("Arial", 7))
                elif field == 'distance':
                    # Format distance to 2 decimal places
                    try:
                        value = f"{float(value):.2f}"
                    except (ValueError, TypeError):
                        value = 'N/A'
                    item = QTableWidgetItem(str(value))
                    item.setFont(QFont("Arial", 7))  # Ensure small font
                else:
                    item = QTableWidgetItem(str(value))
                    item.setFont(QFont("Arial", 7))  # Ensure small font
                
                # Highlight negative balance
                if field == 'Balance':
                    try:
                        balance = float(site_info.get(field, 0))
                        if balance < 0:
                            item.setBackground(QColor(255, 0, 0))
                    except (ValueError, TypeError):
                        pass
                    
                self.proximity_table.setItem(row, col, item)
                
        # Ensure headers are properly sized and aligned
        try:
            header = self.proximity_table.horizontalHeader()
            if header is not None:
                header.setMinimumHeight(30)  # Make header taller
                header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align headers
                header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        except Exception as e:
            print(f"Warning: Could not configure table header: {str(e)}")
            
        # Removed resizeColumnsToContents() to maintain our custom widths 