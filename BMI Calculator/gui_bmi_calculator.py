# gui_bmi_calculator.py

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import numpy as np

# Configure matplotlib style
plt.style.use('seaborn-v0_8')

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 Advanced BMI Calculator")
        self.root.geometry("1000x750")
        self.root.configure(bg='#f0f8ff')
        self.root.resizable(True, True)
        
        # Set application icon (you can replace with actual icon file)
        try:
            self.root.iconbitmap('bmi_icon.ico')  # Optional: add an icon file
        except:
            pass
        
        # Data storage
        self.data_file = "bmi_data.json"
        self.user_data = self.load_data()
        
        # Color scheme
        self.colors = {
            'primary': '#2c3e50',
            'secondary': '#3498db',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'light': '#ecf0f1',
            'dark': '#2c3e50',
            'background': '#f0f8ff'
        }
        
        # Unit variables
        self.weight_unit_var = tk.StringVar(value='kg')
        self.height_unit_var = tk.StringVar(value='m')
        
        # Create notebook for tabs
        self.create_notebook()
        
        # Apply styling
        self.setup_styles()
    
    def setup_styles(self):
        """Configure widget styles"""
        style = ttk.Style()
        
        # Configure theme
        style.theme_use('clam')
        
        # Configure styles for different widgets
        style.configure('TNotebook', background=self.colors['light'])
        style.configure('TNotebook.Tab', 
                       font=('Arial', 10, 'bold'),
                       padding=[20, 10],
                       background=self.colors['light'])
        
        style.configure('Title.TLabel',
                       font=('Arial', 18, 'bold'),
                       foreground=self.colors['primary'],
                       background=self.colors['background'])
        
        style.configure('Subtitle.TLabel',
                       font=('Arial', 12, 'bold'),
                       foreground=self.colors['secondary'],
                       background=self.colors['background'])
        
        style.configure('Custom.TFrame',
                       background=self.colors['background'])
        
        style.configure('Custom.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=10,
                       background=self.colors['secondary'],
                       foreground='white')
        
        style.map('Custom.TButton',
                 background=[('active', self.colors['primary']),
                           ('pressed', self.colors['dark'])])
    
    def create_notebook(self):
        """Create the main notebook with tabs"""
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create tabs
        self.create_welcome_tab()
        self.create_calculator_tab()
        self.create_history_tab()
        self.create_analysis_tab()
        self.create_about_tab()
    
    def create_welcome_tab(self):
        """Create welcome tab with overview"""
        welcome_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(welcome_frame, text="🏠 Welcome")
        
        # Main content frame
        content_frame = ttk.Frame(welcome_frame, style='Custom.TFrame')
        content_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Title
        title_label = ttk.Label(content_frame, text="🏥 BMI Calculator Pro", 
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ttk.Label(content_frame, 
                                  text="Your Comprehensive Health Monitoring Solution",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=10)
        
        # Features frame
        features_frame = ttk.LabelFrame(content_frame, text="🌟 Features", 
                                       style='Custom.TFrame')
        features_frame.pack(pady=30, fill='x', padx=50)
        
        features = [
            "📊 Accurate BMI Calculation with Multiple Units",
            "🔄 Support for kg/lb weight and m/cm/ft height",
            "📈 Trend Analysis with Charts",
            "💾 Secure Data Storage",
            "📱 User-Friendly Interface",
            "📋 Historical Data Tracking",
            "🎯 Health Recommendations"
        ]
        
        for feature in features:
            feature_label = ttk.Label(features_frame, text=feature,
                                    font=('Arial', 11),
                                    background=self.colors['light'])
            feature_label.pack(anchor='w', pady=5, padx=20)
        
        # Quick stats
        stats_frame = ttk.Frame(content_frame, style='Custom.TFrame')
        stats_frame.pack(pady=20)
        
        total_users = len(self.user_data)
        total_records = sum(len(records) for records in self.user_data.values())
        
        stats_text = f"📊 Quick Stats: {total_users} Users | {total_records} Records"
        stats_label = ttk.Label(stats_frame, text=stats_text,
                              font=('Arial', 10, 'bold'),
                              foreground=self.colors['secondary'])
        stats_label.pack()
    
    def create_calculator_tab(self):
        """Create the main calculator tab"""
        calculator_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(calculator_frame, text="🧮 Calculator")
        
        # Main content frame with padding
        main_frame = ttk.Frame(calculator_frame, style='Custom.TFrame')
        main_frame.pack(fill='both', expand=True, padx=30, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="BMI Calculator", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Input frame with modern design
        input_container = ttk.LabelFrame(main_frame, text="Personal Information",
                                        style='Custom.TFrame')
        input_container.pack(pady=20, padx=20, fill='x')
        
        # User name
        name_frame = ttk.Frame(input_container, style='Custom.TFrame')
        name_frame.pack(fill='x', pady=10, padx=20)
        
        ttk.Label(name_frame, text="👤 Name:", 
                 font=('Arial', 11, 'bold')).pack(side='left')
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, 
                              font=('Arial', 11), width=25)
        name_entry.pack(side='left', padx=10)
        
        # Weight input with unit selection
        weight_frame = ttk.Frame(input_container, style='Custom.TFrame')
        weight_frame.pack(fill='x', pady=10, padx=20)
        
        ttk.Label(weight_frame, text="⚖️ Weight:", 
                 font=('Arial', 11, 'bold')).pack(side='left')
        self.weight_var = tk.StringVar()
        weight_entry = ttk.Entry(weight_frame, textvariable=self.weight_var, 
                                font=('Arial', 11), width=15)
        weight_entry.pack(side='left', padx=5)
        
        # Weight unit dropdown
        weight_unit_combo = ttk.Combobox(weight_frame, 
                                        textvariable=self.weight_unit_var,
                                        values=['kg', 'lb'],
                                        state="readonly",
                                        width=8,
                                        font=('Arial', 10))
        weight_unit_combo.pack(side='left', padx=5)
        
        # Height input with unit selection
        height_frame = ttk.Frame(input_container, style='Custom.TFrame')
        height_frame.pack(fill='x', pady=10, padx=20)
        
        ttk.Label(height_frame, text="📏 Height:", 
                 font=('Arial', 11, 'bold')).pack(side='left')
        self.height_var = tk.StringVar()
        height_entry = ttk.Entry(height_frame, textvariable=self.height_var, 
                                font=('Arial', 11), width=15)
        height_entry.pack(side='left', padx=5)
        
        # Height unit dropdown
        height_unit_combo = ttk.Combobox(height_frame, 
                                        textvariable=self.height_unit_var,
                                        values=['m', 'cm', 'ft'],
                                        state="readonly",
                                        width=8,
                                        font=('Arial', 10))
        height_unit_combo.pack(side='left', padx=5)
        
        # Unit info label
        unit_info_frame = ttk.Frame(input_container, style='Custom.TFrame')
        unit_info_frame.pack(fill='x', pady=5, padx=20)
        
        unit_info = ttk.Label(unit_info_frame, 
                             text="💡 Supported units: Weight (kg, lb) • Height (m, cm, ft)",
                             font=('Arial', 9),
                             foreground=self.colors['secondary'])
        unit_info.pack()
        
        # Button frame with modern buttons
        button_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="🧮 Calculate BMI", 
                  command=self.calculate_bmi, style='Custom.TButton').pack(side='left', padx=10)
        ttk.Button(button_frame, text="🔄 Clear", 
                  command=self.clear_inputs, style='Custom.TButton').pack(side='left', padx=10)
        ttk.Button(button_frame, text="💾 Save Record", 
                  command=self.save_record, style='Custom.TButton').pack(side='left', padx=10)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(main_frame, text="📊 Results",
                                           style='Custom.TFrame')
        self.results_frame.pack(pady=20, padx=20, fill='both', expand=True)
        
        self.result_text = scrolledtext.ScrolledText(self.results_frame, height=10, 
                                                    font=('Consolas', 10),
                                                    bg=self.colors['light'],
                                                    relief='flat')
        self.result_text.pack(fill='both', expand=True, padx=10, pady=10)
        self.result_text.config(state=tk.DISABLED)
    
    def create_history_tab(self):
        """Create the history tab"""
        history_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(history_frame, text="📋 History")
        
        # Title
        title_label = ttk.Label(history_frame, text="BMI History", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Controls frame
        controls_frame = ttk.LabelFrame(history_frame, text="User Selection",
                                       style='Custom.TFrame')
        controls_frame.pack(pady=10, padx=20, fill='x')
        
        controls_inner = ttk.Frame(controls_frame, style='Custom.TFrame')
        controls_inner.pack(pady=15, padx=15)
        
        ttk.Label(controls_inner, text="👤 Select User:", 
                 font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        self.user_var = tk.StringVar()
        self.user_combo = ttk.Combobox(controls_inner, textvariable=self.user_var, 
                                      font=('Arial', 10), width=20, state="readonly")
        self.user_combo.pack(side='left', padx=10)
        self.user_combo.bind('<<ComboboxSelected>>', self.load_user_history)
        
        ttk.Button(controls_inner, text="🔄 Refresh", 
                  command=self.update_user_list, style='Custom.TButton').pack(side='left', padx=5)
        ttk.Button(controls_inner, text="🗑️ Clear All Data", 
                  command=self.clear_all_data, style='Custom.TButton').pack(side='left', padx=5)
        
        # History display
        history_display_frame = ttk.LabelFrame(history_frame, text="User History",
                                             style='Custom.TFrame')
        history_display_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.history_text = scrolledtext.ScrolledText(history_display_frame, height=15,
                                                     font=('Consolas', 9),
                                                     bg=self.colors['light'],
                                                     relief='flat')
        self.history_text.pack(pady=10, padx=10, fill='both', expand=True)
        self.history_text.config(state=tk.DISABLED)
        
        self.update_user_list()
    
    def create_analysis_tab(self):
        """Create the analysis and visualization tab"""
        analysis_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(analysis_frame, text="📈 Analysis")
        
        # Title
        title_label = ttk.Label(analysis_frame, text="BMI Trend Analysis", 
                               style='Title.TLabel')
        title_label.pack(pady=10)
        
        # Controls
        controls_frame = ttk.LabelFrame(analysis_frame, text="Chart Controls",
                                       style='Custom.TFrame')
        controls_frame.pack(pady=10, padx=20, fill='x')
        
        controls_inner = ttk.Frame(controls_frame, style='Custom.TFrame')
        controls_inner.pack(pady=15, padx=15)
        
        ttk.Label(controls_inner, text="👤 Select User:", 
                 font=('Arial', 11, 'bold')).pack(side='left', padx=5)
        self.analysis_user_var = tk.StringVar()
        self.analysis_user_combo = ttk.Combobox(controls_inner, 
                                               textvariable=self.analysis_user_var,
                                               font=('Arial', 10), width=20,
                                               state="readonly")
        self.analysis_user_combo.pack(side='left', padx=10)
        
        ttk.Button(controls_inner, text="📊 Generate Chart", 
                  command=self.generate_chart, style='Custom.TButton').pack(side='left', padx=5)
        ttk.Button(controls_inner, text="🔄 Refresh", 
                  command=self.update_analysis_user_list, style='Custom.TButton').pack(side='left', padx=5)
        
        # Chart frame
        self.chart_frame = ttk.LabelFrame(analysis_frame, text="Visualization",
                                        style='Custom.TFrame')
        self.chart_frame.pack(pady=10, padx=20, fill='both', expand=True)
        
        self.update_analysis_user_list()
    
    def create_about_tab(self):
        """Create about tab with information"""
        about_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(about_frame, text="ℹ️ About")
        
        content_frame = ttk.Frame(about_frame, style='Custom.TFrame')
        content_frame.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Title
        title_label = ttk.Label(content_frame, text="About BMI Calculator Pro", 
                               style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Information
        info_text = """
📋 Project Description:

This Advanced BMI Calculator is developed as a comprehensive Python internship project. 
It features both command-line and graphical user interface versions with advanced 
data tracking and visualization capabilities.

🎯 Key Features:

• 🧮 Accurate BMI Calculation with Multiple Units
• ⚖️ Weight units: kg, lb
• 📏 Height units: m, cm, ft
• 📊 Beautiful Data Visualization with Matplotlib
• 💾 Secure JSON Data Storage
• 📈 Trend Analysis and Historical Tracking
• 🎨 Modern, User-Friendly Interface
• ✅ Input Validation and Error Handling

📊 BMI Classification:

• Underweight: BMI < 18.5
• Normal weight: 18.5 ≤ BMI < 25
• Overweight: 25 ≤ BMI < 30
• Obese: BMI ≥ 30

🛠️ Technical Stack:

• Python 3.x
• Tkinter for GUI
• Matplotlib for Visualization
• JSON for Data Storage

Developed for Python Internship Training
        """
        
        info_label = tk.Text(content_frame, font=('Arial', 11), 
                           bg=self.colors['light'], relief='flat',
                           wrap=tk.WORD, padx=20, pady=20)
        info_label.insert(tk.END, info_text)
        info_label.config(state=tk.DISABLED)
        info_label.pack(fill='both', expand=True)
    
    def convert_weight_to_kg(self, weight, weight_unit):
        """Convert weight to kilograms"""
        if weight_unit == 'lb':
            return weight * 0.453592  # 1 lb = 0.453592 kg
        return weight
    
    def convert_height_to_m(self, height, height_unit):
        """Convert height to meters"""
        if height_unit == 'cm':
            return height / 100
        elif height_unit == 'ft':
            return height * 0.3048  # 1 ft = 0.3048 m
        return height
    
    def calculate_bmi(self):
        """Calculate BMI and display results"""
        try:
            # Validate inputs
            name = self.name_var.get().strip()
            weight_str = self.weight_var.get().strip()
            height_str = self.height_var.get().strip()
            weight_unit = self.weight_unit_var.get()
            height_unit = self.height_unit_var.get()
            
            if not name:
                messagebox.showerror("Error", "❌ Please enter your name.")
                return
            
            if not weight_str or not height_str:
                messagebox.showerror("Error", "❌ Please enter both weight and height.")
                return
            
            weight = float(weight_str)
            height = float(height_str)
            
            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "❌ Weight and height must be positive numbers.")
                return
            
            # Validate reasonable ranges based on units
            if weight_unit == 'kg' and weight > 300:
                messagebox.showerror("Error", "❌ Weight seems too high. Please check your input.")
                return
            elif weight_unit == 'lb' and weight > 660:
                messagebox.showerror("Error", "❌ Weight seems too high. Please check your input.")
                return
            
            if height_unit == 'm' and height > 2.5:
                messagebox.showerror("Error", "❌ Height seems too high. Please check your input.")
                return
            elif height_unit == 'cm' and height > 250:
                messagebox.showerror("Error", "❌ Height seems too high. Please check your input.")
                return
            elif height_unit == 'ft' and height > 8:
                messagebox.showerror("Error", "❌ Height seems too high. Please check your input.")
                return
            
            # Convert to metric system
            weight_kg = self.convert_weight_to_kg(weight, weight_unit)
            height_m = self.convert_height_to_m(height, height_unit)
            
            # Calculate BMI
            bmi = weight_kg / (height_m ** 2)
            category = self.classify_bmi(bmi)
            color = self.get_bmi_color(bmi)
            
            # Display results
            self.display_results(name, weight, weight_unit, height, height_unit, bmi, category, color)
            
        except ValueError:
            messagebox.showerror("Error", "❌ Please enter valid numbers for weight and height.")
    
    def classify_bmi(self, bmi):
        """Classify BMI into categories"""
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 25:
            return "Normal weight"
        elif 25 <= bmi < 30:
            return "Overweight"
        else:
            return "Obese"
    
    def get_bmi_color(self, bmi):
        """Get color based on BMI category"""
        if bmi < 18.5:
            return self.colors['warning']  # Orange
        elif 18.5 <= bmi < 25:
            return self.colors['success']  # Green
        elif 25 <= bmi < 30:
            return self.colors['warning']  # Orange
        else:
            return self.colors['danger']   # Red
    
    def display_results(self, name, weight, weight_unit, height, height_unit, bmi, category, color):
        """Display BMI calculation results with styling"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        # Create formatted results
        result = f"""
╔══════════════════════════════════════╗
║            BMI RESULTS               ║
╠══════════════════════════════════════╣
║  👤 Name:    {name:<20} ║
║  ⚖️ Weight:  {weight:<8.2f} {weight_unit:<5}    ║
║  📏 Height:  {height:<8.2f} {height_unit:<5}    ║
║  🔢 BMI:     {bmi:<8.2f}             ║
║  🏷️ Category: {category:<16}     ║
╠══════════════════════════════════════╣
║          BMI CLASSIFICATION          ║
╠══════════════════════════════════════╣
║  Underweight    BMI < 18.5           ║
║  Normal weight  18.5 ≤ BMI < 25      ║
║  Overweight     25 ≤ BMI < 30        ║
║  Obese          BMI ≥ 30             ║
╚══════════════════════════════════════╝

💡 Recommendation:
"""
        
        # Add recommendation based on category
        if category == "Underweight":
            result += "Consider consulting a healthcare provider for nutritional advice."
        elif category == "Normal weight":
            result += "Great! Maintain your healthy lifestyle. 🎉"
        elif category == "Overweight":
            result += "Consider incorporating more physical activity and balanced diet."
        else:
            result += "Please consult a healthcare provider for guidance."
        
        self.result_text.insert(tk.END, result)
        
        # Apply color to BMI value
        self.result_text.tag_configure("bmi_color", foreground=color)
        self.result_text.tag_add("bmi_color", f"5.14", f"5.22")
        
        self.result_text.config(state=tk.DISABLED)
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.name_var.set("")
        self.weight_var.set("")
        self.height_var.set("")
        self.weight_unit_var.set('kg')
        self.height_unit_var.set('m')
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        messagebox.showinfo("Cleared", "✅ All inputs have been cleared.")
    
    def save_record(self):
        """Save the current BMI record"""
        try:
            name = self.name_var.get().strip()
            weight_str = self.weight_var.get().strip()
            height_str = self.height_var.get().strip()
            weight_unit = self.weight_unit_var.get()
            height_unit = self.height_unit_var.get()
            
            if not name or not weight_str or not height_str:
                messagebox.showerror("Error", "❌ Please calculate BMI before saving.")
                return
            
            weight = float(weight_str)
            height = float(height_str)
            
            # Convert to metric system for storage
            weight_kg = self.convert_weight_to_kg(weight, weight_unit)
            height_m = self.convert_height_to_m(height, height_unit)
            
            bmi = weight_kg / (height_m ** 2)
            category = self.classify_bmi(bmi)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create record (store original units and converted values)
            record = {
                'timestamp': timestamp,
                'weight': weight_kg,  # Store in kg for consistency
                'height': height_m,   # Store in meters for consistency
                'bmi': bmi,
                'category': category,
                'original_weight': weight,
                'original_weight_unit': weight_unit,
                'original_height': height,
                'original_height_unit': height_unit
            }
            
            # Add to user data
            if name not in self.user_data:
                self.user_data[name] = []
            
            self.user_data[name].append(record)
            self.save_data()
            
            messagebox.showinfo("Success", f"✅ BMI record saved for {name}!")
            self.update_user_list()
            self.update_analysis_user_list()
            
        except (ValueError, AttributeError):
            messagebox.showerror("Error", "❌ Please calculate BMI before saving.")
    
    def load_data(self):
        """Load user data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def save_data(self):
        """Save user data to JSON file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.user_data, f, indent=2)
        except IOError:
            messagebox.showerror("Error", "❌ Could not save data to file.")
    
    def update_user_list(self):
        """Update the user list in history tab"""
        users = list(self.user_data.keys())
        self.user_combo['values'] = users
        if users:
            self.user_var.set(users[0])
            self.load_user_history()
    
    def update_analysis_user_list(self):
        """Update the user list in analysis tab"""
        users = list(self.user_data.keys())
        self.analysis_user_combo['values'] = users
        if users:
            self.analysis_user_var.set(users[0])
    
    def load_user_history(self, event=None):
        """Load and display user history"""
        user = self.user_var.get()
        if not user or user not in self.user_data:
            return
        
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        
        records = self.user_data[user]
        if not records:
            self.history_text.insert(tk.END, f"📝 No records found for {user}.")
        else:
            self.history_text.insert(tk.END, f"📋 BMI History for {user}:\n\n")
            for i, record in enumerate(records, 1):
                # Use original units if available, otherwise use stored metric
                weight = record.get('original_weight', record['weight'])
                weight_unit = record.get('original_weight_unit', 'kg')
                height = record.get('original_height', record['height'])
                height_unit = record.get('original_height_unit', 'm')
                
                color = self.get_bmi_color(record['bmi'])
                self.history_text.insert(tk.END, 
                    f"📅 Record #{i}\n"
                    f"   Date: {record['timestamp']}\n"
                    f"   Weight: {weight:.2f} {weight_unit}\n"
                    f"   Height: {height:.2f} {height_unit}\n"
                    f"   BMI: {record['bmi']:.2f}\n"
                    f"   Category: {record['category']}\n"
                    f"{'─' * 50}\n"
                )
        
        self.history_text.config(state=tk.DISABLED)
    
    def generate_chart(self):
        """Generate BMI trend chart for selected user"""
        user = self.analysis_user_var.get()
        if not user or user not in self.user_data:
            messagebox.showerror("Error", "❌ Please select a user with data.")
            return
        
        records = self.user_data[user]
        if len(records) < 2:
            messagebox.showwarning("Warning", "⚠️ Need at least 2 records to generate a trend chart.")
            return
        
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Prepare data
        dates = [datetime.strptime(record['timestamp'], "%Y-%m-%d %H:%M:%S") 
                for record in records]
        bmis = [record['bmi'] for record in records]
        weights = [record['weight'] for record in records]
        
        # Create figure and subplots with custom style
        fig = Figure(figsize=(12, 8), facecolor=self.colors['light'])
        gs = fig.add_gridspec(2, 1, height_ratios=[2, 1])
        ax1 = fig.add_subplot(gs[0])
        ax2 = fig.add_subplot(gs[1])
        
        # Plot BMI trend
        ax1.plot(dates, bmis, 'o-', color=self.colors['secondary'], 
                linewidth=3, markersize=8, markerfacecolor='white', markeredgewidth=2)
        ax1.set_title(f'📈 BMI Trend Analysis for {user}', fontsize=14, fontweight='bold', pad=20)
        ax1.set_ylabel('BMI', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Add BMI classification zones with transparency
        ax1.axhspan(0, 18.5, alpha=0.2, color='blue', label='Underweight')
        ax1.axhspan(18.5, 25, alpha=0.2, color='green', label='Normal')
        ax1.axhspan(25, 30, alpha=0.2, color='orange', label='Overweight')
        ax1.axhspan(30, max(bmis) + 2, alpha=0.2, color='red', label='Obese')
        ax1.legend(loc='upper right', framealpha=0.9)
        
        # Plot weight trend
        ax2.plot(dates, weights, 's-', color=self.colors['danger'], 
                linewidth=2, markersize=6, markerfacecolor='white', markeredgewidth=2)
        ax2.set_title(f'⚖️ Weight Trend for {user}', fontsize=12, fontweight='bold', pad=15)
        ax2.set_ylabel('Weight (kg)', fontweight='bold')
        ax2.set_xlabel('Date', fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        # Format dates
        date_format = mdates.DateFormatter('%Y-%m-%d')
        ax1.xaxis.set_major_formatter(date_format)
        ax2.xaxis.set_major_formatter(date_format)
        
        # Rotate date labels
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
        
        # Adjust layout
        fig.tight_layout(pad=4.0)
        
        # Embed chart in tkinter
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Add toolbar (optional)
        from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
        toolbar = NavigationToolbar2Tk(canvas, self.chart_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def clear_all_data(self):
        """Clear all stored data"""
        if messagebox.askyesno("Confirm", "🗑️ Are you sure you want to delete all data? This action cannot be undone."):
            self.user_data = {}
            self.save_data()
            self.update_user_list()
            self.update_analysis_user_list()
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete(1.0, tk.END)
            self.history_text.config(state=tk.DISABLED)
            messagebox.showinfo("Success", "✅ All data has been cleared.")

def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = BMICalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()