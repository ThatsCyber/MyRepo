from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QLabel, QTextEdit,
    QTableWidget, QTableWidgetItem, QComboBox,
    QFileDialog, QMessageBox, QApplication, QSplitter,
    QCheckBox, QHeaderView, QTabWidget, QProgressDialog
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QFont, QKeySequence, QShortcut, QClipboard
from qt_material import apply_stylesheet
from data_handler import DataHandler
from proximity import ProximityAnalyzer
import pandas as pd

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
        self.load_facilities_btn = QPushButton("Load Facilities (Excel/CSV)")
        self.load_facilities_btn.setFixedHeight(25)  # Make button smaller
        self.load_facilities_btn.setFixedWidth(button_width)
        self.load_facilities_btn.clicked.connect(self._load_facilities_file)
        file_layout.addWidget(self.load_facilities_btn)
        
        # Middle button - Supply & Demand
        self.load_cart_btn = QPushButton("Load Supply Demand")
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
        
        # Far right button - TEC Dwelling
        self.load_dwelling_btn = QPushButton("Load TEC Dwelling")
        self.load_dwelling_btn.setFixedHeight(25)  # Make button smaller
        self.load_dwelling_btn.setFixedWidth(button_width)
        self.load_dwelling_btn.clicked.connect(self._load_dwelling_file)
        file_layout.addWidget(self.load_dwelling_btn)
        
        # Add some spacing
        file_layout.addStretch(20)
        
        # Auto Download button (smaller, different styling)
        self.auto_download_btn = QPushButton("⬇ Auto Load")
        self.auto_download_btn.setFixedHeight(25)
        self.auto_download_btn.setFixedWidth(120)  # Smaller width
        self.auto_download_btn.clicked.connect(self._auto_download_data)
        self.auto_download_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 3px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)
        file_layout.addWidget(self.auto_download_btn)
        
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
            QMenu {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #404040;
            }
            QMenu::item {
                background-color: transparent;
                padding: 5px 20px;
            }
            QMenu::item:selected {
                background-color: #2a5a8c;
            }
            QMenu::separator {
                height: 1px;
                background-color: #404040;
                margin: 4px 0px;
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
            header_font = QFont("Arial", 8)  # Increased from 6 to 8 for better readability
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
                # Enable automatic row height adjustment
                vert_header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            
            # Make table read-only
            table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
            
            # Enable multi-cell selection
            table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
            table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
            
            # Enable keyboard events
            table.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
            
            # Add copy functionality with Ctrl+C using keyPressEvent override
            original_keyPressEvent = table.keyPressEvent
            def enhanced_keyPressEvent(event):
                if event.matches(QKeySequence.StandardKey.Copy):
                    self._copy_selected_cells(table)
                    event.accept()
                else:
                    original_keyPressEvent(event)
            
            table.keyPressEvent = enhanced_keyPressEvent
            
            # Add Shift+scroll wheel horizontal scrolling
            original_wheelEvent = table.wheelEvent
            def enhanced_wheelEvent(event):
                # Check if Shift is pressed
                if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                    # Convert vertical scroll to horizontal scroll
                    horizontal_scrollbar = table.horizontalScrollBar()
                    if horizontal_scrollbar:
                        # Get the scroll delta (typically +/- 120 for one wheel step)
                        delta = event.angleDelta().y()
                        # Apply the scroll to horizontal scrollbar (invert direction for natural feel)
                        current_value = horizontal_scrollbar.value()
                        new_value = current_value - delta // 3  # Divide by 3 to make scrolling less sensitive
                        horizontal_scrollbar.setValue(new_value)
                        event.accept()
                        return
                
                # Default behavior for normal scrolling
                original_wheelEvent(event)
            
            table.wheelEvent = enhanced_wheelEvent
            
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
                    padding: 3px;
                    background-color: #2b2b2b;
                    color: #ffffff;
                    vertical-align: top;
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
    
    def _copy_selected_cells(self, table):
        """Copy selected cells to clipboard in a tab-separated format."""
        try:
            # Get selected ranges from the selection model
            selection_model = table.selectionModel()
            if not selection_model or not selection_model.hasSelection():
                return
            
            # Get all selected indexes
            selected_indexes = selection_model.selectedIndexes()
            if not selected_indexes:
                return
            
            # Group indexes by row and column
            selected_positions = set()
            for index in selected_indexes:
                selected_positions.add((index.row(), index.column()))
            
            # Find the bounds of the selection
            rows = sorted(set(pos[0] for pos in selected_positions))
            cols = sorted(set(pos[1] for pos in selected_positions))
            
            # Build the clipboard text
            clipboard_text = []
            for row in rows:
                row_data = []
                for col in cols:
                    if (row, col) in selected_positions:
                        # Get text from either table item or custom widget
                        text = ""
                        
                        # First, check if there's a custom widget at this position
                        widget = table.cellWidget(row, col)
                        if widget:
                            # Try to extract text from widget (e.g., from QLabel in utilization cells)
                            label = widget.findChild(QLabel)
                            if label:
                                text = label.text()
                        else:
                            # Use regular table item text
                            item = table.item(row, col)
                            if item:
                                text = item.text()
                        
                        row_data.append(text)
                    else:
                        row_data.append("")  # Empty cell in rectangular selection
                clipboard_text.append("\t".join(row_data))
            
            # Copy to clipboard
            final_text = "\n".join(clipboard_text)
            clipboard = QApplication.clipboard()
            clipboard.setText(final_text)
            
        except Exception as e:
            print(f"Error copying cells: {str(e)}")
            
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
    
    def _get_best_utilization_info(self, site_name):
        """Get utilization info for a site, handling sister site display names."""
        if not site_name:
            return None
            
        # If the site name contains newlines (sister site display), try each site individually
        if '\n' in site_name:
            # Split by newline - first line is main site, second line is sister sites
            lines = site_name.split('\n')
            main_site = lines[0].strip()
            
            # Try main site first
            utilization_info = self.data_handler.get_utilization_info(main_site)
            if utilization_info:
                return utilization_info
                
            # If main site doesn't have utilization data, try sister sites
            if len(lines) > 1:
                sister_sites_line = lines[1].strip()
                # Sister sites are separated by " / "
                sister_sites = [site.strip() for site in sister_sites_line.split(' / ')]
                for sister_site in sister_sites:
                    utilization_info = self.data_handler.get_utilization_info(sister_site)
                    if utilization_info:
                        return utilization_info
        else:
            # Single site, try direct lookup
            return self.data_handler.get_utilization_info(site_name)
            
        return None
            
    def _create_input_section(self, parent_layout):
        """Create input section with site input and action buttons."""
        input_layout = QVBoxLayout()
        input_layout.setSpacing(3)  # Smaller spacing
        input_layout.setContentsMargins(2, 2, 2, 2)  # Smaller margins
        
        # Site input field
        input_field_layout = QHBoxLayout()
        self.site_input = QTextEdit()
        self.site_input.setPlaceholderText("Enter site name")
        self.site_input.setMaximumHeight(80)  # Back to original height
        self.site_input.setFont(QFont("Arial", 7))  # Back to original smaller font
        
        # Original styling to match the output display below (yellow text/border)
        self.site_input.setStyleSheet("""
            QTextEdit {
                selection-background-color: #2a5a8c;
                selection-color: white;
            }
        """)
        
        # Force plain text mode to completely prevent rich formatting
        self.site_input.setAcceptRichText(False)  # This prevents any rich text formatting
        
        # Additional protection: override insertFromMimeData to ensure plain text only
        original_insertFromMimeData = self.site_input.insertFromMimeData
        def insertPlainTextOnly(source):
            if source.hasText():
                # Get plain text and insert it directly
                plain_text = source.text()
                cursor = self.site_input.textCursor()
                cursor.insertText(plain_text)
            else:
                # Fallback to original behavior for non-text data
                original_insertFromMimeData(source)
        
        self.site_input.insertFromMimeData = insertPlainTextOnly
        
        # Add Ctrl+Enter shortcut for Check Site Info
        shortcut = QShortcut(QKeySequence("Ctrl+Return"), self.site_input)
        shortcut.activated.connect(self._check_cart_site)
        
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
        
        # Define columns and widths once
        columns = [
            'Site Name', 'Region', 'Demand', 'Supply', 'Balance',
            'Utilization', 'Capacity', 'Usage', 'Slips Available',
            'Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs'
        ]
        column_widths = [100, 100, 80, 80, 80, 100, 70, 70, 110, 120, 80, 80, 80, 80]  # Widened Slips Available from 90 to 110

        # Set up tables
        for table in [self.negative_balance_table, self.positive_balance_table]:
            self._setup_table(table)
            table.setColumnCount(len(columns))
            table.setHorizontalHeaderLabels(columns)
            self._set_table_column_widths(table, column_widths)
            
            # Ensure headers are word-wrapped and tall enough
            try:
                header = table.horizontalHeader()
                if header is not None:
                    header.setMinimumHeight(30)  # Make header taller
                    header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align headers
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
        """Update both negative and positive balance tables with enhanced responsiveness."""
        if self.data_handler.cart_data is None:
            return
            
        print("Updating cart balance tables...")
        
        # Keep UI responsive before starting
        QApplication.processEvents()
        
        # Get pre-filtered and sorted data from data_handler
        negative_sites = self.data_handler.get_negative_balance_sites()
        high_balance_sites = self.data_handler.get_high_balance_sites()
        
        print(f"Updating negative balance table with {len(negative_sites)} sites...")
        
        # Keep UI responsive
        QApplication.processEvents()
        
        # Update negative balance table
        self._fill_balance_table(self.negative_balance_table, negative_sites)
        
        print(f"Updating positive balance table with {len(high_balance_sites)} sites...")
        
        # Keep UI responsive
        QApplication.processEvents()
        
        # Update positive balance table
        self._fill_balance_table(self.positive_balance_table, high_balance_sites)
        
        print("Cart balance tables updated successfully")
        
    def _fill_balance_table(self, table, sites_data):
        """Fill the balance table with site data using chunked processing for responsiveness."""
        # Define columns - this must match the data from get_all_cart_sites
        columns = [
            'Site Name', 'Region', 'Demand', 'Supply', 'Balance',
            'Utilization', 'Capacity', 'Usage', 'Slips Available',
            'Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs'
        ]
        
        numeric_columns = {
            'Demand', 'Supply', 'Balance',
            'Capacity', 'Usage', 'Slips Available',
            'Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs'
        }
        
        # CRITICAL: Clear all existing content first to prevent overlaps
        table.clear()
        table.setRowCount(len(sites_data))
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        

        
        # Keep UI responsive before starting row processing
        QApplication.processEvents()
        
        # Process rows in chunks to maintain responsiveness
        chunk_size = 50  # Process 50 rows at a time
        total_rows = len(sites_data)
        
        for chunk_start in range(0, total_rows, chunk_size):
            chunk_end = min(chunk_start + chunk_size, total_rows)
            
            print(f"Processing table rows {chunk_start + 1}-{chunk_end} of {total_rows}...")
            
            # Process this chunk of rows
            for row in range(chunk_start, chunk_end):
                site_data = sites_data[row]
                
                for col, column in enumerate(columns):
                    if column == 'Utilization':
                        # Get utilization info - handle sister sites by extracting individual site codes
                        site_name = site_data.get('Site Name', '')
                        utilization_info = self._get_best_utilization_info(site_name)
                        
                        if utilization_info:
                            try:
                                utilization = float(utilization_info['On Site Utilization'])
                                utilization_percentage = utilization * 100
                                value = f"{utilization_percentage:.2f}%"
                                
                                # Use custom widget for utilization (same as other tables)
                                widget = QWidget()
                                layout = QHBoxLayout(widget)
                                layout.setContentsMargins(4, 2, 4, 2)
                                
                                label = QLabel(value)
                                color = self._get_utilization_color(utilization_percentage)
                                
                                # Check if this is a cart site to make utilization bold
                                is_cart_site = site_name and self.data_handler.get_site_info(site_name) and self.data_handler.get_site_info(site_name).get('is_cart_site', False)
                                
                                # Build the stylesheet with conditional bold formatting
                                font_weight = "font-weight: bold;" if is_cart_site else ""
                                label.setStyleSheet(
                                    f"color: rgb({color.red()}, {color.green()}, {color.blue()}); "
                                    f"background: transparent; {font_weight}"
                                )
                                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                layout.addWidget(label)
                                
                                # Clear any existing item and widget first to prevent overlap
                                table.setItem(row, col, None)  # Clear existing item
                                table.setCellWidget(row, col, None)  # Clear any existing widget
                                table.setCellWidget(row, col, widget)  # Set the utilization widget
                                # Skip all remaining processing for this column
                                continue
                            except (ValueError, TypeError):
                                pass
                        
                        # If we get here, create N/A item and let it process normally
                        item = QTableWidgetItem('N/A')
                    elif column in ['Capacity', 'Usage', 'Slips Available']:
                        # Get utilization info for capacity, usage, and slips available - handle sister sites
                        site_name = site_data.get('Site Name', '')
                        utilization_info = self._get_best_utilization_info(site_name)
                        if utilization_info:
                            if column == 'Slips Available':
                                # Calculate Slips Available = Capacity - Usage
                                try:
                                    capacity = float(utilization_info.get('On Site Capacity', 0))
                                    usage = float(utilization_info.get('On Site Usage', 0))
                                    slips_available = capacity - usage
                                    item = QTableWidgetItem(f"{int(slips_available)}")  # Remove decimal formatting
                                except (ValueError, TypeError):
                                    item = QTableWidgetItem('N/A')
                            else:
                                value = utilization_info.get(f'On Site {column}', 'N/A')
                                if value != 'N/A':
                                    try:
                                        value = int(float(value))  # Remove decimal formatting
                                        item = QTableWidgetItem(str(value))
                                    except (ValueError, TypeError):
                                        item = QTableWidgetItem('N/A')
                                else:
                                    item = QTableWidgetItem('N/A')
                        else:
                            item = QTableWidgetItem('N/A')
                    else:
                        value = site_data.get(column, 0 if column in numeric_columns else '')
                        # Format value based on column type
                        if column in numeric_columns:
                            try:
                                float_value = float(value)
                                formatted_value = f"{int(float_value)}"  # Remove decimal formatting
                                item = QTableWidgetItem(formatted_value)
                                # Note: Red text for negatives applied after bold formatting below
                            except (ValueError, TypeError):
                                item = QTableWidgetItem("0")
                        else:
                            item = QTableWidgetItem(str(value))
                    
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    
                    # Check if this is a cart site and make the entire row bold
                    site_name = site_data.get('Site Name', '')
                    is_cart_site = site_name and self.data_handler.get_site_info(site_name) and self.data_handler.get_site_info(site_name).get('is_cart_site', False)
                    
                    # Check if this is a negative number that needs red text
                    is_negative = False
                    negative_value = 0
                    if column in numeric_columns:
                        try:
                            # For calculated columns like "Slips Available", use the item text
                            if column == 'Slips Available':
                                value = float(item.text()) if item.text() != 'N/A' else 0
                            else:
                                # For other columns, use original site_data
                                raw_value = site_data.get(column, 0)
                                value = float(raw_value)
                            
                            if value < 0:
                                is_negative = True
                                negative_value = value
                        except (ValueError, TypeError):
                            pass
                    
                    # Apply formatting: Bold + Red if needed
                    if is_cart_site:
                        font = item.font()
                        font.setBold(True)
                        item.setFont(font)
                    
                    # Apply red color for negative numbers using CUSTOM WIDGET (like utilization does)
                    if is_negative:
                        # Create custom widget with QLabel (same as utilization approach)
                        widget = QWidget()
                        layout = QHBoxLayout(widget)
                        layout.setContentsMargins(4, 2, 4, 2)
                        
                        # Create red label with bold text
                        label = QLabel(item.text())
                        red_color = QColor(255, 0, 0)  # Same red as utilization
                        label.setStyleSheet(
                            f"color: rgb({red_color.red()}, {red_color.green()}, {red_color.blue()}); "
                            "background: transparent; font-weight: bold;"
                        )
                        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        layout.addWidget(label)
                        
                        # NEVER set an item when using a custom widget - use ONLY the widget
                        table.setCellWidget(row, col, widget)

                    else:
                        # Apply bold formatting for cart sites (non-negative)  
                        if is_cart_site:
                            font = item.font()
                            font.setBold(True)
                            item.setFont(font)
                        # Only set item if we're NOT using a custom widget
                        table.setItem(row, col, item)
            
            # Keep UI responsive after processing each chunk
            QApplication.processEvents()
        
        # After populating all rows, adjust row heights for sister sites
        self._adjust_row_heights_for_sister_sites(table)

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
            
            # Check if this is a cart site to make utilization bold
            site_code = data['Site Code']
            is_cart_site = site_code and self.data_handler.get_site_info(site_code) and self.data_handler.get_site_info(site_code).get('is_cart_site', False)
            
            # Build the stylesheet with conditional bold formatting
            font_weight = "font-weight: bold;" if is_cart_site else ""
            label.setStyleSheet(f"color: white; background: transparent; {font_weight}")
            
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
        """Load facilities data from Excel or CSV file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Facilities Data",
            "",
            "Facilities Files (*.xlsx *.xlsm *.csv);;Excel Files (*.xlsx *.xlsm);;CSV Files (*.csv);;All Files (*)"
        )
        
        if not file_path:  # User cancelled
            return
            
        # Load the data
        success = self.data_handler.load_facilities_data(file_path)
        
        if success:
            QMessageBox.information(self, "Success", "Facilities data loaded successfully!")
        else:
            QMessageBox.warning(self, "Error", "Failed to load facilities data. Check the console for details.")
        
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
        
        # New target site logic: identify most frequent site and exclude it
        site_frequency = {}  # Count how many times each site appears
        all_unique_sites = set()  # Track all sites that appear
        
        for line in lines:
            if "->" in line:
                start_site, end_site = line.split("->")
                start_site = start_site.strip()
                end_site = end_site.strip()
                
                # Count frequency
                site_frequency[start_site] = site_frequency.get(start_site, 0) + 1
                site_frequency[end_site] = site_frequency.get(end_site, 0) + 1
                
                # Track unique sites
                all_unique_sites.add(start_site)
                all_unique_sites.add(end_site)
            else:
                site = line.strip()
                site_frequency[site] = site_frequency.get(site, 0) + 1
                all_unique_sites.add(site)
        
        # Find target sites (most frequent) - handle ties and single sites
        target_sites = set()
        if site_frequency:
            max_frequency = max(site_frequency.values())
            
            # If there's only one unique site, or all sites have the same frequency, show all
            if len(all_unique_sites) == 1 or all(freq == max_frequency for freq in site_frequency.values()):
                unique_sites = list(all_unique_sites)
            else:
                # Only exclude sites that appear more frequently than others
                for site, freq in site_frequency.items():
                    if freq == max_frequency:
                        target_sites.add(site)
                
                # Build final list: all sites except the target sites (but only if there are non-targets)
                unique_sites = []
                for site in all_unique_sites:
                    if site not in target_sites:
                        unique_sites.append(site)
        else:
            unique_sites = []
            
        # Set up columns (added dwelling columns and Slips Available)
        columns = [
            'Name', 'Type', 'Address', 'Region', 
            'Demand', 'Full Day Demand', 'Supply', 'Balance',
            'Utilization', 'Capacity', 'Usage', 'Slips Available',
            'Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs'  # Updated dwelling columns
        ]
        self.site_info_table.setColumnCount(len(columns))
        self.site_info_table.setHorizontalHeaderLabels(columns)
        
        # Set column widths
        self._set_table_column_widths(
            self.site_info_table,
            [80, 70, 200, 70, 70, 100, 70, 75, 100, 70, 70, 110, 70, 70, 70, 70, 70]  # Widened Slips Available from 90 to 110
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
                    'Name': site_info.get('display_name', site.upper()),  # Use formatted display name
                    'Type': site_info.get('type', ''),
                    'Address': site_info.get('address', ''),
                    'Region': site_info.get('region', ''),
                }
                
                # Demand info columns with default values
                demand_info = {
                    'Demand': int(site_info.get('Demand', 0)),
                    'Full Day Demand': int(site_info.get('Full Day Demand', 0)),
                    'Supply': int(site_info.get('Supply', 0)),
                    'Balance': int(site_info.get('Balance', 0))
                }
                
                # Get utilization info
                utilization_info = self.data_handler.get_utilization_info(site)
                if utilization_info:
                    utilization_data = {
                        'Utilization': utilization_info['On Site Utilization'],
                        'Capacity': int(utilization_info['On Site Capacity']),  # Convert to integer
                        'Usage': int(utilization_info['On Site Usage'])  # Convert to integer
                    }
                    # Calculate Slips Available
                    try:
                        capacity = float(utilization_info['On Site Capacity'])
                        usage = float(utilization_info['On Site Usage'])
                        slips_available = capacity - usage
                        utilization_data['Slips Available'] = f"{int(slips_available)}"  # Remove decimal formatting
                    except (ValueError, TypeError):
                        utilization_data['Slips Available'] = 'N/A'
                else:
                    utilization_data = {
                        'Utilization': 'N/A',
                        'Capacity': 'N/A',
                        'Usage': 'N/A',
                        'Slips Available': 'N/A'
                    }
                
                # Get dwelling info
                if site_info.get('has_dwelling_data', False):
                    dwelling_data = {
                        'Total Trailers': int(site_info.get('Total Trailers', 0)) if site_info.get('Total Trailers', 0) != 'N/A' else 'N/A',
                        '<24 Hrs': int(site_info.get('<24 Hrs', 0)) if site_info.get('<24 Hrs', 0) != 'N/A' else 'N/A',
                        '24-72 Hrs': int(site_info.get('24-72 Hrs', 0)) if site_info.get('24-72 Hrs', 0) != 'N/A' else 'N/A',
                        '72-168 Hrs': int(site_info.get('72-168 Hrs', 0)) if site_info.get('72-168 Hrs', 0) != 'N/A' else 'N/A',
                        '>168 Hrs': int(site_info.get('>168 Hrs', 0)) if site_info.get('>168 Hrs', 0) != 'N/A' else 'N/A'
                    }
                else:
                    dwelling_data = {
                        'Total Trailers': 'N/A',
                        '<24 Hrs': 'N/A',
                        '24-72 Hrs': 'N/A',
                        '72-168 Hrs': 'N/A',
                        '>168 Hrs': 'N/A'
                    }
                
                # Combine all info
                all_info = {**basic_info, **demand_info, **utilization_data, **dwelling_data}
                
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
                            
                            # Check if this is a cart site to make utilization bold
                            is_cart_site = site_info and site_info.get('is_cart_site', False)
                            
                            # Build the stylesheet with conditional bold formatting
                            font_weight = "font-weight: bold;" if is_cart_site else ""
                            label.setStyleSheet(
                                f"color: rgb({color.red()}, {color.green()}, {color.blue()}); "
                                f"background: transparent; {font_weight}"
                            )
                        progress_layout.addWidget(label)
                        
                        self.site_info_table.setCellWidget(row, col, progress_widget)
                    else:
                        item = QTableWidgetItem(str(value))
                        item.setFont(font)
                        
                        # Set alignment based on column type
                        if column_name == 'Name' and '\n' in str(value):
                            # Multi-line text for sister sites - align to top-left
                            item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                        elif column_name in ['Demand', 'Full Day Demand', 'Supply', 'Balance', 'Slips Available', 'Capacity', 'Usage', 'Utilization', 'Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs']:
                            # Center align numerical columns for consistency with balance tables
                            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                        
                        # Check for negative numbers and use custom widget approach
                        is_negative = False
                        if column_name in ['Demand', 'Full Day Demand', 'Supply', 'Balance', 'Slips Available', 'Capacity', 'Usage', 'Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs']:
                            try:
                                # Handle both numeric values and string values (like "Slips Available")
                                if isinstance(value, (int, float)):
                                    check_value = float(value)
                                else:
                                    # Try to convert string to float (skip "N/A")
                                    check_value = float(value) if str(value) != 'N/A' else 0
                                
                                if check_value < 0:
                                    is_negative = True
                            except (ValueError, TypeError):
                                pass
                        
                        # Check if this is a cart site
                        site_info = self.data_handler.get_site_info(site)
                        is_cart_site = site_info and site_info.get('is_cart_site', False)
                        
                        if is_negative:
                            # Use custom widget for negative numbers (same as balance tables)
                            widget = QWidget()
                            layout = QHBoxLayout(widget)
                            layout.setContentsMargins(4, 2, 4, 2)
                            
                            label = QLabel(str(value))
                            red_color = QColor(255, 0, 0)
                            label.setStyleSheet(
                                f"color: rgb({red_color.red()}, {red_color.green()}, {red_color.blue()}); "
                                "background: transparent; font-weight: bold;"
                            )
                            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                            layout.addWidget(label)
                            
                            # Clear any existing item first
                            self.site_info_table.setItem(row, col, None)
                            self.site_info_table.setCellWidget(row, col, widget)
                        else:
                            # Regular item - apply bold for cart sites
                            if is_cart_site:
                                font.setBold(True)
                            item.setFont(font)
                            
                            # Special handling for Name column with sister sites
                            if column_name == 'Name' and '\n' in str(value):
                                item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                            
                            self.site_info_table.setItem(row, col, item)
                
        self.site_info_table.resizeColumnsToContents()
        
        # After populating all rows, adjust row heights for sister sites
        self._adjust_row_heights_for_sister_sites(self.site_info_table)

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
            
        # Update nearby sites with display names
        for site_info in nearby_sites:
            site_name = site_info.get('name', '')
            if site_name:
                # Get the formatted display name for sister sites
                full_site_info = self.data_handler.get_site_info(site_name)
                if full_site_info and 'display_name' in full_site_info:
                    site_info['display_name'] = full_site_info['display_name']
                else:
                    site_info['display_name'] = site_name
        
        # Set up table ONCE, outside the loop
        self.proximity_table.setRowCount(len(nearby_sites))
        
        # Clear all existing content (widgets and items)
        self.proximity_table.clearContents()
        
        # Always include all columns
        columns = ['name', 'address', 'state', 'region', 'distance']
        
        # Add cart data, utilization columns, and dwelling time columns
        columns.extend(['Demand', 'Supply', 'Balance', 'Utilization', 'Capacity', 'Usage', 'Slips Available', 'Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs'])
            
        self.proximity_table.setColumnCount(len(columns))
        self.proximity_table.setHorizontalHeaderLabels(columns)
        
        # Define numeric columns for consistent formatting
        numeric_columns = {
            'Demand', 'Supply', 'Balance', 'distance',
            'Capacity', 'Usage', 'Slips Available', 'Total Trailers',
            '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs'
        }
        
        # Set optimized column widths
        widths = [
            80,   # name
            150,  # address (reduced but still readable)
            50,   # state
            60,   # region
            70,   # distance
            70,   # Demand
            70,   # Supply
            70,   # Balance
            85,   # Utilization
            70,   # Capacity
            70,   # Usage
            110,  # Slips Available (widened from 90 to 110)
            120,  # Total Trailers (increased to match balance tables)
            70,   # <24 Hrs
            70,   # 24-72 Hrs
            80,   # 72-168 Hrs (increased to match balance tables)
            70    # >168 Hrs
        ]
            
        self._set_table_column_widths(self.proximity_table, widths)
        
        # Create larger font for row values
        row_font = QFont("Arial", 8)  # Increased from 7 to 8 to match other tables
        
        # Fill data
        for row, site_info in enumerate(nearby_sites):
            # Get dwelling info for the site
            dwelling_info = self.data_handler.get_dwelling_info(site_info['name'])
            
            for col, field in enumerate(columns):
                # Handle dwelling time columns
                if field in ['Total Trailers', '<24 Hrs', '24-72 Hrs', '72-168 Hrs', '>168 Hrs']:
                    value = dwelling_info.get(field, 'N/A') if dwelling_info else 'N/A'
                    if value != 'N/A':
                        try:
                            value = f"{int(float(value))}"  # Remove decimals consistently
                        except (ValueError, TypeError):
                            value = 'N/A'
                    item = QTableWidgetItem(str(value))
                # Special handling for name field to show sister sites
                elif field == 'name':
                    display_name = site_info.get('display_name', site_info.get('name', ''))
                    item = QTableWidgetItem(str(display_name))
                # Special handling for utilization data
                elif field in ['Utilization', 'Capacity', 'Usage', 'Slips Available']:
                    utilization_info = self.data_handler.get_utilization_info(site_info['name'])
                    if utilization_info:
                        if field == 'Utilization':
                            try:
                                utilization = float(utilization_info['On Site Utilization'])
                                utilization_percentage = utilization * 100
                                value = f"{utilization_percentage:.2f}%"
                                
                                # Use custom widget for utilization (same as balance tables)
                                widget = QWidget()
                                layout = QHBoxLayout(widget)
                                layout.setContentsMargins(4, 2, 4, 2)
                                
                                label = QLabel(value)
                                color = self._get_utilization_color(utilization_percentage)
                                label.setStyleSheet(
                                    f"color: rgb({color.red()}, {color.green()}, {color.blue()}); "
                                    "background: transparent;"
                                )
                                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                                layout.addWidget(label)
                                
                                # Clear any existing item and widget first to prevent overlap
                                self.proximity_table.setItem(row, col, None)
                                self.proximity_table.setCellWidget(row, col, None)
                                self.proximity_table.setCellWidget(row, col, widget)
                                continue  # Skip normal item creation
                            except (ValueError, TypeError):
                                value = 'N/A'
                                item = QTableWidgetItem(value)
                        elif field == 'Slips Available':
                            # Calculate Slips Available = Capacity - Usage
                            try:
                                capacity = float(utilization_info.get('On Site Capacity', 0))
                                usage = float(utilization_info.get('On Site Usage', 0))
                                slips_available = capacity - usage
                                value = f"{int(slips_available)}"  # Remove decimal formatting
                                item = QTableWidgetItem(value)
                            except (ValueError, TypeError):
                                value = 'N/A'
                                item = QTableWidgetItem(value)
                        else:
                            value = utilization_info.get(f'On Site {field}', 'N/A')
                            if value != 'N/A' and value is not None:
                                try:
                                    value = f"{int(float(value))}"  # Remove decimal formatting
                                except (ValueError, TypeError):
                                    value = 'N/A'
                            else:
                                value = 'N/A'
                            item = QTableWidgetItem(str(value))
                    else:
                        value = 'N/A'
                        item = QTableWidgetItem(value)
                else:
                    # Get the value from site_info for all other fields
                    value = site_info.get(field, '')
                    
                    # Format numeric values consistently (remove decimals except for distance)
                    if field in numeric_columns and value != '':
                        try:
                            if field == 'distance':
                                value = f"{float(value):.2f}"  # Keep decimals for distance
                            else:
                                value = f"{int(float(value))}"  # Remove decimals for other numeric fields
                        except (ValueError, TypeError):
                            value = 'N/A'
                    
                    item = QTableWidgetItem(str(value))
                
                # Apply consistent formatting to all cells
                item.setFont(row_font)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                
                # Special handling for name column with sister sites
                if field == 'name' and '\n' in str(display_name):
                    # Multi-line text for sister sites
                    item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
                    # Set word wrap for multi-line display
                    item.setData(Qt.ItemDataRole.DisplayRole, display_name)
                
                # Check for negative numbers and use custom widget
                is_negative = False
                if field in numeric_columns and value != '' and value != 'N/A':
                    try:
                        # Handle percentage values
                        check_value = value.replace('%', '') if '%' in str(value) else value
                        numeric_value = float(check_value)
                        if numeric_value < 0:
                            is_negative = True
                    except (ValueError, TypeError):
                        pass
                
                if is_negative:
                    # Use custom widget for negative numbers (same as balance tables)
                    widget = QWidget()
                    layout = QHBoxLayout(widget)
                    layout.setContentsMargins(4, 2, 4, 2)
                    
                    label = QLabel(str(value))
                    red_color = QColor(255, 0, 0)
                    label.setStyleSheet(
                        f"color: rgb({red_color.red()}, {red_color.green()}, {red_color.blue()}); "
                        "background: transparent;"
                    )
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    layout.addWidget(label)
                    
                    # Clear any existing item and widget first to prevent overlap
                    self.proximity_table.setItem(row, col, None)
                    self.proximity_table.setCellWidget(row, col, None)
                    self.proximity_table.setCellWidget(row, col, widget)
                else:
                    # Regular item - no bold formatting in proximity table
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
            
        # After populating all rows, adjust row heights for sister sites
        self._adjust_row_heights_for_sister_sites(self.proximity_table)
        
        # Removed resizeColumnsToContents() to maintain our custom widths 

    def _load_dwelling_file(self):
        """Load TEC dwelling data from a CSV file."""
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Load TEC Dwelling Data",
                "",
                "CSV Files (*.csv);;All Files (*)"
            )
            
            if not file_path:  # User cancelled
                return
                
            # Load the data
            success = self.data_handler.load_dwelling_data(file_path)
            
            if success:
                # Update all tables that show dwelling data
                self._update_site_info_multiple([])  # Clear and refresh the site info table
                self._update_cart_balance_tables()   # Update balance tables
                QMessageBox.information(self, "Success", "TEC dwelling data loaded successfully!")
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Failed to load TEC dwelling data. Please check that your CSV file has the correct format:\n\n"
                    "Required columns:\n"
                    "- Site Code\n"
                    "- Region\n"
                    "- TEC Count\n"
                    "- Dwelling Time"
                )
        except pd.errors.EmptyDataError:
            QMessageBox.warning(self, "Error", "The CSV file is empty")
        except pd.errors.ParserError as e:
            QMessageBox.warning(self, "Error", f"Error parsing CSV file: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load TEC dwelling data: {str(e)}") 
            
    def _auto_download_data(self):
        """Automatically detect and load the most recent relevant files from Downloads folder."""
        # Import required modules at the top so they're accessible to timer methods
        import os
        from pathlib import Path
        import glob
        from datetime import datetime
        
        try:
            # Create and show loading dialog with more micro-steps
            loading_dialog = QProgressDialog("🔍 Initializing auto load...", None, 0, 20, self)
            loading_dialog.setWindowTitle("Auto Loading Data")
            loading_dialog.setWindowModality(Qt.WindowModality.WindowModal)
            loading_dialog.setCancelButton(None)  # Remove cancel button
            loading_dialog.setMinimumDuration(0)  # Show immediately
            
            # Style the progress dialog to make percentage text more visible
            loading_dialog.setStyleSheet("""
                QProgressDialog {
                    background-color: #2b2b2b;
                    color: #ffffff;
                    border: 1px solid #404040;
                }
                QProgressDialog QLabel {
                    color: #ffffff;
                    background-color: transparent;
                    font-size: 11px;
                }
                QProgressBar {
                    border: 1px solid #404040;
                    border-radius: 3px;
                    background-color: #404040;
                    text-align: center;
                    color: #000000;
                    font-weight: bold;
                    font-size: 11px;
                }
                QProgressBar::chunk {
                    background-color: #28a745;
                    border-radius: 2px;
                }
            """)
            
            loading_dialog.setValue(0)
            loading_dialog.show()
            QApplication.processEvents()
            
            # Store dialog and data as instance variables for timer access
            self._loading_dialog = loading_dialog
            self._load_results = {}
            self._loaded_count = 0
            self._load_errors = []
            self._current_step = 0
            
            # Get the user's Downloads folder
            downloads_folder = Path.home() / "Downloads"
            if not downloads_folder.exists():
                loading_dialog.close()
                QMessageBox.warning(
                    self,
                    "Downloads Folder Not Found",
                    f"Could not find Downloads folder at: {downloads_folder}"
                )
                return
            
            # Step 1: Scan for files
            self._loading_dialog.setLabelText("🔍 Scanning Downloads folder...")
            self._loading_dialog.setValue(1)
            QApplication.processEvents()
            
            # Define file patterns for each data type
            file_patterns = {
                'supply_demand': [
                    '*supply*demand*.csv',
                    '*supply_demand*.csv', 
                    '*demand*.csv',
                    '*cart*.csv'
                ],
                'yard_utilization': [
                    '*yard*utilization*.csv',
                    '*utilization*.csv',
                    '*yard*.csv'
                ],
                'tec_dwelling': [
                    '*tec*dwelling*.csv',
                    '*dwelling*.csv',
                    '*tec*.csv',
                    '*all*dwelling*.csv'
                ]
            }
            
            # Function to find most recent file matching patterns
            def find_most_recent_file(patterns):
                all_files = []
                for pattern in patterns:
                    files = glob.glob(str(downloads_folder / pattern), recursive=False)
                    all_files.extend(files)
                
                if not all_files:
                    return None
                    
                # Sort by modification time, most recent first
                all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                return all_files[0]
            
            # Find all files first
            self._files_to_load = []
            supply_demand_file = find_most_recent_file(file_patterns['supply_demand'])
            if supply_demand_file:
                self._files_to_load.append(('supply_demand', supply_demand_file, 'Supply & Demand'))
            else:
                self._load_errors.append("No Supply & Demand files found in Downloads")
            
            utilization_file = find_most_recent_file(file_patterns['yard_utilization'])
            if utilization_file:
                self._files_to_load.append(('yard_utilization', utilization_file, 'Yard Utilization'))
            else:
                self._load_errors.append("No Yard Utilization files found in Downloads")
            
            dwelling_file = find_most_recent_file(file_patterns['tec_dwelling'])
            if dwelling_file:
                self._files_to_load.append(('tec_dwelling', dwelling_file, 'TEC Dwelling'))
            else:
                self._load_errors.append("No TEC Dwelling files found in Downloads")
            
            # Step 2: Files found
            self._loading_dialog.setLabelText(f"📋 Found {len(self._files_to_load)} file(s) to load...")
            self._loading_dialog.setValue(2)
            QApplication.processEvents()
            
            # Start the micro-chunked loading process
            self._file_index = 0
            self._current_load_step = 'start'  # Track micro-steps within file loading
            self._load_timer = QTimer()
            self._load_timer.setSingleShot(True)
            self._load_timer.timeout.connect(self._process_next_load_step)
            
            # Small delay to show "files found" message, then start loading
            QTimer.singleShot(300, self._load_timer.start)
                
        except Exception as e:
            if hasattr(self, '_loading_dialog'):
                self._loading_dialog.close()
            QMessageBox.warning(
                self,
                "Auto Load Error",
                f"Error during auto load: {str(e)}\n\n"
                "You can still load files manually using the individual load buttons."
            )
    
    def _process_next_load_step(self):
        """Process the next micro-step in the loading sequence."""
        import os
        
        try:
            if self._file_index >= len(self._files_to_load):
                # All files processed, show results
                self._show_load_results()
                return
            
            file_type, file_path, display_name = self._files_to_load[self._file_index]
            
            # Calculate progress step (each file gets ~6 steps: read, parse, update, etc.)
            base_step = 3 + (self._file_index * 6)
            
            if self._current_load_step == 'start':
                # Step 1: Show file info
                file_size = os.path.getsize(file_path)
                file_size_kb = file_size / 1024
                self._loading_dialog.setLabelText(f"📁 Preparing to load {display_name}... ({file_size_kb:.1f} KB)")
                self._loading_dialog.setValue(base_step)
                QApplication.processEvents()
                self._current_load_step = 'reading'
                QTimer.singleShot(100, self._process_next_load_step)
                
            elif self._current_load_step == 'reading':
                # Step 2: Reading file
                self._loading_dialog.setLabelText(f"📖 Reading {display_name} file...")
                self._loading_dialog.setValue(base_step + 1)
                QApplication.processEvents()
                self._current_load_step = 'parsing'
                QTimer.singleShot(50, self._process_next_load_step)
                
            elif self._current_load_step == 'parsing':
                # Step 3: Parse the data (this is the heavy operation)
                self._loading_dialog.setLabelText(f"⚙️ Parsing {display_name} data...")
                self._loading_dialog.setValue(base_step + 2)
                QApplication.processEvents()
                
                # Do the actual file loading
                success = False
                try:
                    if file_type == 'supply_demand':
                        success = self.data_handler.load_cart_data(file_path)
                    elif file_type == 'yard_utilization':
                        success = self.data_handler.load_utilization_data(file_path)
                    elif file_type == 'tec_dwelling':
                        success = self.data_handler.load_dwelling_data(file_path)
                    
                    if success:
                        self._load_results[display_name] = os.path.basename(file_path)
                        self._loaded_count += 1
                        self._current_load_step = 'processing'
                    else:
                        self._load_errors.append(f"Failed to load {display_name}: {os.path.basename(file_path)}")
                        self._current_load_step = 'next_file'
                        
                except Exception as e:
                    self._load_errors.append(f"Error loading {display_name}: {str(e)}")
                    self._current_load_step = 'next_file'
                
                QTimer.singleShot(50, self._process_next_load_step)
                
            elif self._current_load_step == 'processing':
                # Step 4: Processing loaded data
                self._loading_dialog.setLabelText(f"🔄 Processing {display_name} data...")
                self._loading_dialog.setValue(base_step + 3)
                QApplication.processEvents()
                self._current_load_step = 'updating'
                QTimer.singleShot(50, self._process_next_load_step)
                
            elif self._current_load_step == 'updating':
                # Step 5: Update tables
                self._loading_dialog.setLabelText(f"📊 Updating tables with {display_name}...")
                self._loading_dialog.setValue(base_step + 4)
                QApplication.processEvents()
                
                # Update tables (this can also be heavy)
                try:
                    self._update_cart_balance_tables()
                except Exception as e:
                    self._load_errors.append(f"Error updating tables for {display_name}: {str(e)}")
                
                self._current_load_step = 'completing'
                QTimer.singleShot(50, self._process_next_load_step)
                
            elif self._current_load_step == 'completing':
                # Step 6: Complete this file
                self._loading_dialog.setLabelText(f"✅ Completed {display_name}")
                self._loading_dialog.setValue(base_step + 5)
                QApplication.processEvents()
                self._current_load_step = 'next_file'
                QTimer.singleShot(200, self._process_next_load_step)
                
            elif self._current_load_step == 'next_file':
                # Move to next file
                self._file_index += 1
                self._current_load_step = 'start'
                QTimer.singleShot(50, self._process_next_load_step)
            
        except Exception as e:
            self._loading_dialog.close()
            QMessageBox.warning(
                self,
                "Auto Load Error",
                f"Error during micro-step processing: {str(e)}"
            )
    
    def _show_load_results(self):
        """Show the final results and close loading dialog."""
        try:
            # Final progress step
            self._loading_dialog.setLabelText("🎉 Auto load complete!")
            self._loading_dialog.setValue(20)
            QApplication.processEvents()
            
            # Brief pause, then close
            QTimer.singleShot(300, self._finalize_load_results)
            
        except Exception as e:
            self._loading_dialog.close()
            QMessageBox.warning(self, "Error", f"Error showing results: {str(e)}")
    
    def _finalize_load_results(self):
        """Finalize the loading process and show results."""
        try:
            self._loading_dialog.close()
            
            # Show results using the same logic as before
            if self._loaded_count > 0:
                success_message = f"Successfully loaded {self._loaded_count} file(s):\n\n"
                for data_type, filename in self._load_results.items():
                    success_message += f"✅ {data_type}: {filename}\n"
                
                # Check what data types had no matching files found (not already loaded)
                missing_files = []
                if self._loaded_count < 3:  # If we didn't load all 3 types, check what files were missing
                    if 'Supply & Demand' not in self._load_results:
                        missing_files.append("Supply & Demand")
                    if 'Yard Utilization' not in self._load_results:
                        missing_files.append("Yard Utilization") 
                    if 'TEC Dwelling' not in self._load_results:
                        missing_files.append("TEC Dwelling")
                
                if missing_files:
                    success_message += f"\n📋 Files not found in Downloads:\n"
                    for data_type in missing_files:
                        success_message += f"• {data_type} (no matching file found)\n"
                
                if self._load_errors:
                    success_message += f"\n⚠️ Issues encountered:\n"
                    for error in self._load_errors:
                        success_message += f"• {error}\n"
                
                QMessageBox.information(
                    self,
                    "Auto Load Complete",
                    success_message
                )
            else:
                # No files were loaded
                error_message = "No files could be loaded automatically.\n\n"
                error_message += "Common file name patterns searched:\n"
                error_message += "• Supply & Demand: files containing 'supply', 'demand', or 'cart'\n"
                error_message += "• Yard Utilization: files containing 'yard' or 'utilization'\n"
                error_message += "• TEC Dwelling: files containing 'tec' or 'dwelling'\n\n"
                if self._load_errors:
                    error_message += "Errors encountered:\n"
                    for error in self._load_errors:
                        error_message += f"• {error}\n"
                
                QMessageBox.warning(
                    self,
                    "Auto Load Failed", 
                    error_message
                )
            
            # Clean up instance variables
            if hasattr(self, '_loading_dialog'):
                delattr(self, '_loading_dialog')
            if hasattr(self, '_load_timer'):
                delattr(self, '_load_timer')
                
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error finalizing results: {str(e)}")
    
    def _record_download_actions(self):
        """Record the download actions using Playwright."""
        try:
            # Show recording instructions
            instructions = QMessageBox(self)
            instructions.setWindowTitle("Recording Instructions")
            instructions.setText(
                "Recording will start in a moment!\n\n"
                "In the browser that opens:\n"
                "1. Navigate to your QuickSight dashboard\n"
                "2. Complete authentication (PIN + security key)\n"
                "3. Find the Supply & Demand section\n"
                "4. Click the 3-dots menu\n"
                "5. Click 'Export to CSV'\n"
                "6. Wait for download to complete\n"
                "7. Close the browser to finish recording\n\n"
                "The actions will be saved automatically!"
            )
            instructions.exec()
            
            # Start recording process
            QMessageBox.information(
                self,
                "Starting Recording",
                "Browser will open shortly for recording.\n\n"
                "Perform the download actions, then close the browser when done."
            )
            
            # This will be implemented next with the actual recording logic
            self._run_playwright_recording()
                
        except Exception as e:
            QMessageBox.warning(
                self,
                "Recording Error",
                f"Error during recording: {str(e)}"
            )
    
    def _run_playwright_recording(self):
        """Record actions on the existing authenticated Chrome browser."""
        import subprocess
        import os
        
        try:
            # Check if Chrome is running with debugging
            setup_dialog = QMessageBox(self)
            setup_dialog.setWindowTitle("Record on Authenticated Chrome")
            setup_dialog.setText(
                "Perfect! Now we can record on your authenticated Chrome.\n\n"
                "Make sure:\n"
                "1. Chrome is running with debugging (--remote-debugging-port=9222)\n"
                "2. You're logged into QuickSight in that Chrome window\n"
                "3. You can see the dashboard with the data you want to download\n\n"
                "Playwright will connect to your existing Chrome and record your actions!\n\n"
                "Click 'Start Recording' when ready."
            )
            setup_dialog.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            
            if setup_dialog.exec() == QMessageBox.StandardButton.Cancel:
                return
            
            # Create a directory for our recorded script
            script_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recorded_scripts")
            os.makedirs(script_dir, exist_ok=True)
            
            # The recorded script will be saved here
            script_path = os.path.join(script_dir, "download_script_new.py")
            
            # Show recording instructions
            QMessageBox.information(
                self,
                "Recording Instructions", 
                "Playwright will now connect to your Chrome and start recording.\n\n"
                "In your existing Chrome window:\n"
                "1. Navigate to the Supply & Demand section\n"
                "2. Click the 3-dots menu\n"
                "3. Click 'Export to CSV'\n"
                "4. Wait for download to complete\n"
                "5. Close the Playwright inspector window when done\n\n"
                "All your actions will be recorded!"
            )

            # Show recording instructions
            QMessageBox.information(
                self,
                "Recording Instructions", 
                "Playwright will open a new browser for recording.\n\n"
                "Since this won't have your enterprise extensions:\n"
                "1. Just navigate through the QuickSight interface as if you were authenticated\n"
                "2. Click where the 3-dots menu would be\n"
                "3. Click where 'Export to CSV' would be\n"
                "4. We'll modify the recorded script to work with your authenticated Chrome\n\n"
                "The goal is to record the UI interactions, not worry about authentication!"
            )
            
            # Simple recording approach - let user manually navigate
            quicksight_url = "https://us-east-1.quicksight.aws.amazon.com/sn/account/amazonbi/dashboards/855adf29-7e31-4755-960f-cf99f0fc7e6a"
            
            cmd = [
                "py", "-m", "playwright", "codegen",
                "--target", "python",
                "-o", script_path,
                quicksight_url
            ]
            
            # Run the recording command
            try:
                subprocess.run(cmd, check=True)
                
                QMessageBox.information(
                    self,
                    "Recording Complete",
                    f"Actions recorded successfully!\n\n"
                    f"New script saved to: {script_path}\n\n"
                    "The script should now work with your authenticated Chrome session.\n"
                    "Use 'Run Recorded' to test it!"
                )
                
            except subprocess.CalledProcessError as e:
                # If CDP connection fails, fall back to manual approach
                QMessageBox.warning(
                    self,
                    "CDP Recording Failed",
                    "Could not connect to existing Chrome for recording.\n\n"
                    "Alternative approach:\n"
                    "1. Manually perform the download in your authenticated Chrome\n"
                    "2. I'll help you create a script that replicates those actions\n"
                    "3. We can use the existing working connection method\n\n"
                    "This will still work - we just need to manually define the steps."
                )
                    
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Recording error: {str(e)}"
            )
    
    def _run_recorded_actions(self):
        """Run the previously recorded actions."""
        import os
        
        # Use the directory where this GUI script is located
        gui_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Try the new script first, then fall back to old one
        new_script_path = os.path.join(gui_dir, "recorded_scripts", "download_script_new.py")
        old_script_path = os.path.join(gui_dir, "recorded_scripts", "download_script.py")
        
        if os.path.exists(new_script_path):
            script_path = new_script_path
            print(f"Using new script: {script_path}")
        elif os.path.exists(old_script_path):
            script_path = old_script_path
            print(f"Using old script: {script_path}")
        else:
            script_path = new_script_path  # Default to new for error message
            
        print(f"Script exists: {os.path.exists(script_path)}")
        
        if not os.path.exists(script_path):
            QMessageBox.warning(
                self,
                "No Recording Found",
                "No recorded script found!\n\n"
                "Please use 'Record Actions' first to record the download process."
            )
            return
        
        try:
            # Show progress
            progress = QMessageBox(self)
            progress.setWindowTitle("Running Automation")
            progress.setText("Executing recorded download actions...")
            progress.setStandardButtons(QMessageBox.StandardButton.NoButton)
            progress.show()
            QApplication.processEvents()
            
            # Execute the recorded script
            # We'll implement this next by modifying the recorded script
            self._execute_recorded_script(script_path)
            
            progress.accept()
            QMessageBox.information(
                self,
                "Success",
                "Download automation completed!\n\n"
                "Check your Downloads folder for the CSV file."
                )
                
        except Exception as e:
            if 'progress' in locals():
                progress.accept()
            QMessageBox.warning(
                self,
                "Execution Error",
                f"Error running recorded actions: {str(e)}"
            )
    
    def _execute_recorded_script(self, script_path):
        """Execute the recorded Playwright script."""
        import sys
        import os
        import importlib.util
        
        try:
            # Load the recorded script as a module
            spec = importlib.util.spec_from_file_location("download_script", script_path)
            download_module = importlib.util.module_from_spec(spec)
            
            # Add the script directory to Python path so imports work
            script_dir = os.path.dirname(script_path)
            if script_dir not in sys.path:
                sys.path.insert(0, script_dir)
            
            # Execute the module
            spec.loader.exec_module(download_module)
            
            # Call the run_download function
            if hasattr(download_module, 'run_download'):
                download_module.run_download()
            else:
                print("Warning: run_download function not found in script")
                
        except Exception as e:
            print(f"Error executing recorded script: {e}")
            import traceback
            traceback.print_exc()
            raise e 

    def _adjust_row_heights_for_sister_sites(self, table):
        """Adjust row heights dynamically for sites with sister sites."""
        try:
            for row in range(table.rowCount()):
                # Check the Name/Site Name column (usually column 0)
                name_item = table.item(row, 0)
                if name_item:
                    text = name_item.text()
                    if '\n' in text:
                        # Sister sites found - increase row height
                        # Calculate height based on number of lines
                        line_count = text.count('\n') + 1
                        row_height = max(50, line_count * 25)  # Min 50px, 25px per line
                        table.setRowHeight(row, row_height)
                    else:
                        # Single site - use default height
                        table.setRowHeight(row, 30)
        except Exception as e:
            print(f"Warning: Could not adjust row heights: {str(e)}") 