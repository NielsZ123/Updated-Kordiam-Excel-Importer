#!/usr/bin/env python3
"""
Kordiam Excel Importer - GUI Version
A simple graphical interface for importing Excel data to Kordiam.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import json
import os
import sys
import threading
from datetime import datetime
import io
import pandas as pd

# Import our existing importer
from kordiam_excel_importer import KordiamConfig, KordiamImporter, load_config

class KordiamImporterGUI:
    FIELD_DEFINITIONS = [
        # (section, label, kordiam_field, field_type)
        ("element_fields", "Title", "title", "text"),
        ("element_fields", "Slug", "slug", "text"),
        ("element_fields", "Element Status", "elementStatus", "id"),
        ("tasks", "Task Status ID", "status", "id"),
        ("tasks", "Task Format ID", "format", "id"),
        ("tasks", "Assigned User ID", "user", "id"),
        ("tasks", "Task Deadline", "deadline", "datetime"),
        ("tasks", "Confirmation Status", "confirmationStatus", "id"),
        ("publications", "Platform ID", "platform", "id"),
        ("publications", "Publication Date", "single", "date"),
        ("publications", "Task Assignments", "assignments", "bool"),
        ("groups", "Group IDs", "id", "group_ids"),
        ("event", "Event Start Date", "fromDate", "date"),
        ("event", "Event Start Time", "fromTime", "time"),
        ("event", "Event End Date", "toDate", "date"),
        ("event", "Event End Time", "toTime", "time"),
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("Kordiam Excel Importer")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.excel_file = tk.StringVar()
        self.mapping_file = tk.StringVar()
        self.config_file = tk.StringVar()
        self.dry_run = tk.BooleanVar(value=True)
        self.log_output = tk.StringVar()
        self.mapping_source = tk.StringVar(value="builder")
        self.excel_headers = []
        self.field_vars = {}
        self.field_widgets = []
        
        # Set default values
        self.mapping_file.set("kordiam_mapping_clean.json")
        self.config_file.set("config.json")
        
        self.create_widgets()
        self.load_default_config()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Kordiam Excel Importer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        file_frame = ttk.LabelFrame(main_frame, text="File Selection", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        # Excel file
        ttk.Label(file_frame, text="Excel File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.excel_file, width=50).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_excel_file).grid(row=0, column=2, pady=5)
        
        # Mapping file
        ttk.Label(file_frame, text="Mapping File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.mapping_file, width=50).grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_mapping_file).grid(row=1, column=2, pady=5)
        
        # Config file
        ttk.Label(file_frame, text="Config File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.config_file, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(5, 5), pady=5)
        ttk.Button(file_frame, text="Browse", command=self.browse_config_file).grid(row=2, column=2, pady=5)

        # Mapping source section
        mapping_source_frame = ttk.LabelFrame(main_frame, text="Mapping Source", padding="10")
        mapping_source_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Radiobutton(
            mapping_source_frame,
            text="Build mapping from Excel columns",
            variable=self.mapping_source,
            value="builder"
        ).grid(row=0, column=0, sticky=tk.W, pady=2)

        ttk.Radiobutton(
            mapping_source_frame,
            text="Use mapping JSON file",
            variable=self.mapping_source,
            value="file"
        ).grid(row=1, column=0, sticky=tk.W, pady=2)

        ttk.Button(
            mapping_source_frame,
            text="Load Mapping File Into Selector",
            command=self.load_mapping_into_selectors
        ).grid(row=0, column=1, padx=(10, 0), pady=2)

        ttk.Button(
            mapping_source_frame,
            text="Save Mapping From Selector",
            command=self.save_mapping_from_selectors
        ).grid(row=1, column=1, padx=(10, 0), pady=2)

        # Mapping builder section
        mapping_frame = ttk.LabelFrame(main_frame, text="Field Mapping Builder", padding="10")
        mapping_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        mapping_frame.columnconfigure(0, weight=1)

        self.mapping_notebook = ttk.Notebook(mapping_frame)
        self.mapping_notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        mapping_frame.rowconfigure(0, weight=1)

        self.mapping_tabs = {
            "id": self._create_mapping_tab(self.mapping_notebook, "IDs"),
            "date": self._create_mapping_tab(self.mapping_notebook, "Dates/Times"),
            "text": self._create_mapping_tab(self.mapping_notebook, "Text/Other")
        }

        self._build_mapping_ui()
        
        # Options section
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Dry run checkbox
        ttk.Checkbutton(options_frame, text="Dry Run (Test without creating elements)", variable=self.dry_run).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        # Buttons section
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=3, pady=(0, 10))
        
        ttk.Button(button_frame, text="Create Example Data", command=self.create_example_data).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Test Import (Dry Run)", command=self.test_import).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Run Import", command=self.run_import).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).grid(row=0, column=3)
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Log Output", padding="10")
        log_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E))
    
    def load_default_config(self):
        """Load default configuration if available."""
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    config = json.load(f)
                self.log_message("✓ Loaded configuration from config.json")
            else:
                self.log_message("⚠ No config.json found. Please create one from config_template.json")
        except Exception as e:
            self.log_message(f"⚠ Error loading config: {e}")
    
    def browse_excel_file(self):
        filename = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if filename:
            self.excel_file.set(filename)
            self.update_excel_headers()
    
    def browse_mapping_file(self):
        filename = filedialog.askopenfilename(
            title="Select Mapping File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.mapping_file.set(filename)
    
    def browse_config_file(self):
        filename = filedialog.askopenfilename(
            title="Select Config File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.config_file.set(filename)

    def _create_mapping_tab(self, notebook, title):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text=title)

        canvas = tk.Canvas(tab, height=200)
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return scrollable_frame

    def _build_mapping_ui(self):
        for section, label, kordiam_field, field_type in self.FIELD_DEFINITIONS:
            if field_type in ["id", "group_ids"]:
                tab_key = "id"
            elif field_type in ["date", "time", "datetime"]:
                tab_key = "date"
            else:
                tab_key = "text"

            parent = self.mapping_tabs[tab_key]
            row_frame = ttk.Frame(parent)
            row_frame.pack(fill=tk.X, pady=2)

            display_label = f"[{section}] {label}"
            ttk.Label(row_frame, text=display_label, width=30).pack(side=tk.LEFT)

            var = tk.StringVar(value="(none)")
            combo = ttk.Combobox(row_frame, textvariable=var, width=40, state="readonly")
            combo["values"] = ["(none)"] + self.excel_headers
            combo.pack(side=tk.LEFT, padx=(5, 0))

            self.field_vars[(section, kordiam_field)] = var
            self.field_widgets.append(combo)

    def update_excel_headers(self):
        path = self.excel_file.get()
        if not path or not os.path.exists(path):
            return

        try:
            df = pd.read_excel(path, nrows=0)
            headers = [str(c) for c in df.columns]
            self.excel_headers = headers

            for combo in self.field_widgets:
                combo["values"] = ["(none)"] + headers
                if combo.get() not in combo["values"]:
                    combo.set("(none)")

            self.log_message(f"Loaded {len(headers)} columns from Excel")
        except Exception as e:
            self.log_message(f"Error reading Excel headers: {e}")

    def build_mapping_from_selectors(self):
        mapping_config = {
            "element_fields": {},
            "tasks": {},
            "publications": {},
            "groups": {},
            "event": {}
        }

        for section, _, kordiam_field, _ in self.FIELD_DEFINITIONS:
            key = (section, kordiam_field)
            selected = self.field_vars.get(key).get() if key in self.field_vars else "(none)"
            if selected and selected != "(none)":
                mapping_config[section][selected] = kordiam_field

        # Remove empty sections
        mapping_config = {k: v for k, v in mapping_config.items() if v}
        return mapping_config

    def load_mapping_into_selectors(self):
        try:
            path = self.mapping_file.get()
            if not path or not os.path.exists(path):
                raise ValueError("Mapping file not found")

            with open(path, "r") as f:
                mapping_config = json.load(f)

            for section, _, kordiam_field, _ in self.FIELD_DEFINITIONS:
                selected = "(none)"
                for excel_col, target in mapping_config.get(section, {}).items():
                    if target == kordiam_field:
                        selected = excel_col
                        break
                self.field_vars[(section, kordiam_field)].set(selected)

            self.mapping_source.set("builder")
            self.log_message("Loaded mapping file into selector")
        except Exception as e:
            self.log_message(f"Error loading mapping file: {e}")
            messagebox.showerror("Error", f"Error loading mapping file: {e}")

    def save_mapping_from_selectors(self):
        try:
            mapping_config = self.build_mapping_from_selectors()
            if not mapping_config:
                raise ValueError("No mappings selected")

            filename = filedialog.asksaveasfilename(
                title="Save Mapping File",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if not filename:
                return

            with open(filename, "w") as f:
                json.dump(mapping_config, f, indent=2)

            self.mapping_file.set(filename)
            self.log_message(f"Saved mapping to {filename}")
        except Exception as e:
            self.log_message(f"Error saving mapping: {e}")
            messagebox.showerror("Error", f"Error saving mapping: {e}")
    
    def log_message(self, message):
        """Add message to log with timestamp."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the log output."""
        self.log_text.delete(1.0, tk.END)
        self.status_var.set("Log cleared")
    
    def create_example_data(self):
        """Create example Excel data."""
        try:
            self.status_var.set("Creating example data...")
            self.log_message("Creating example Excel file...")
            
            # Import and run the example creator
            import create_kordiam_example_clean
            create_kordiam_example_clean
            
            self.log_message("✓ Example data created successfully!")
            self.log_message("File: kordiam_example_clean.xlsx")
            self.excel_file.set("kordiam_example_clean.xlsx")
            self.status_var.set("Example data created")
            
        except Exception as e:
            error_msg = f"Error creating example data: {e}"
            self.log_message(f"✗ {error_msg}")
            messagebox.showerror("Error", error_msg)
            self.status_var.set("Error creating example data")
    
    def run_import_thread(self, dry_run=False):
        """Run the import in a separate thread."""
        try:
            # Validate inputs
            if not self.excel_file.get():
                raise ValueError("Please select an Excel file")
            
            if not os.path.exists(self.excel_file.get()):
                raise ValueError(f"Excel file not found: {self.excel_file.get()}")
            
            mapping_config = None
            if self.mapping_source.get() == "builder":
                mapping_config = self.build_mapping_from_selectors()
                if not mapping_config:
                    raise ValueError("No mapping selections found. Choose Excel columns or use a mapping file.")
            else:
                if not os.path.exists(self.mapping_file.get()):
                    raise ValueError(f"Mapping file not found: {self.mapping_file.get()}")
            
            # Load configuration
            self.log_message("Loading configuration...")
            config = load_config(self.config_file.get())
            
            # Load mapping
            if not mapping_config:
                self.log_message("Loading mapping configuration from file...")
                with open(self.mapping_file.get(), 'r') as f:
                    mapping_config = json.load(f)
            else:
                self.log_message("Using mapping configuration from selector...")
            
            # Create importer
            importer = KordiamImporter(config)
            
            # Run import
            operation = "dry run" if dry_run else "import"
            self.log_message(f"Starting {operation}...")
            
            results = importer.import_from_excel(
                excel_file=self.excel_file.get(),
                mapping_config=mapping_config,
                dry_run=dry_run
            )
            
            # Display results
            self.log_message(f"✓ {operation.capitalize()} completed!")
            self.log_message(f"Success: {results['success']}")
            self.log_message(f"Errors: {results['errors']}")
            
            if results['errors'] > 0:
                self.log_message("⚠ Some errors occurred. Check the details above.")
            
            self.status_var.set(f"{operation.capitalize()} completed - {results['success']} success, {results['errors']} errors")
            
        except Exception as e:
            error_msg = f"Error during import: {e}"
            self.log_message(f"✗ {error_msg}")
            messagebox.showerror("Error", error_msg)
            self.status_var.set("Import failed")
    
    def test_import(self):
        """Run a test import (dry run)."""
        self.status_var.set("Running test import...")
        self.log_message("=== Starting Test Import (Dry Run) ===")
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.run_import_thread, args=(True,))
        thread.daemon = True
        thread.start()
    
    def run_import(self):
        """Run the actual import."""
        if not self.dry_run.get():
            # Ask for confirmation
            result = messagebox.askyesno(
                "Confirm Import",
                "This will create actual elements in Kordiam.\n\nAre you sure you want to proceed?"
            )
            if not result:
                return
        
        self.status_var.set("Running import...")
        self.log_message("=== Starting Actual Import ===")
        
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.run_import_thread, args=(self.dry_run.get(),))
        thread.daemon = True
        thread.start()

def main():
    root = tk.Tk()
    app = KordiamImporterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
