import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import string
import pyperclip
import json
import os
from datetime import datetime

class ModernPasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("🔒 Advanced Password Generator")
        self.root.geometry("500x700")
        self.root.minsize(450, 650)
        self.root.configure(bg='#f8f9fa')
        
        # Modern color scheme - Light and professional
        self.bg_color = '#f8f9fa'
        self.card_bg = '#ffffff'
        self.accent_color = '#4361ee'
        self.accent_light = '#4895ef'
        self.success_color = '#4cc9f0'
        self.warning_color = '#f72585'
        self.text_color = '#2b2d42'
        self.text_light = '#6c757d'
        self.border_color = '#dee2e6'
        
        # Password storage file
        self.storage_file = "saved_passwords.json"
        self.saved_passwords = []
        
        # Load saved passwords
        self.load_saved_passwords()
        
        # Create scrollable frame
        self.create_scrollable_ui()
        
    def load_saved_passwords(self):
        """Load saved passwords from JSON file"""
        if os.path.exists(self.storage_file):
            try:
                with open(self.storage_file, 'r') as f:
                    self.saved_passwords = json.load(f)
            except (json.JSONDecodeError, Exception):
                self.saved_passwords = []
        
    def save_passwords_to_file(self):
        """Save passwords to JSON file"""
        try:
            with open(self.storage_file, 'w') as f:
                json.dump(self.saved_passwords, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save passwords: {str(e)}")
        
    def create_scrollable_ui(self):
        # Create main container with scrollbar
        main_container = tk.Frame(self.root, bg=self.bg_color)
        main_container.pack(fill='both', expand=True)
        
        # Create canvas and scrollbar
        self.canvas = tk.Canvas(main_container, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_color)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to scroll
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self._on_mousewheel)
        
        self.setup_ui()
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    def setup_ui(self):
        # Header Section
        header_frame = self.create_card(self.scrollable_frame, top_margin=10)
        
        title_label = tk.Label(
            header_frame, 
            text="🔒 Password Generator", 
            font=('Arial', 24, 'bold'),
            bg=self.card_bg,
            fg=self.text_color
        )
        title_label.pack(pady=(10, 5))
        
        subtitle_label = tk.Label(
            header_frame,
            text="Create strong and secure passwords instantly",
            font=('Arial', 11),
            bg=self.card_bg,
            fg=self.text_light
        )
        subtitle_label.pack(pady=(0, 15))
        
        # Password Length Section
        length_card = self.create_card(self.scrollable_frame, "Password Length")
        
        length_value_frame = tk.Frame(length_card, bg=self.card_bg)
        length_value_frame.pack(fill='x', pady=10)
        
        self.length_var = tk.IntVar(value=16)
        
        self.length_value_label = tk.Label(
            length_value_frame,
            text="16",
            font=('Arial', 16, 'bold'),
            bg=self.card_bg,
            fg=self.accent_color
        )
        self.length_value_label.pack()
        
        self.length_scale = tk.Scale(
            length_card,
            from_=8,
            to=32,
            orient='horizontal',
            variable=self.length_var,
            bg=self.card_bg,
            fg=self.text_color,
            highlightbackground=self.card_bg,
            troughcolor=self.accent_light,
            sliderrelief='flat',
            length=400,
            command=self.on_length_change,
            showvalue=False
        )
        self.length_scale.pack(fill='x', pady=10)
        
        min_max_frame = tk.Frame(length_card, bg=self.card_bg)
        min_max_frame.pack(fill='x')
        
        tk.Label(min_max_frame, text="8", bg=self.card_bg, fg=self.text_light).pack(side='left')
        tk.Label(min_max_frame, text="32", bg=self.card_bg, fg=self.text_light).pack(side='right')
        
        # Character Types Section
        chars_card = self.create_card(self.scrollable_frame, "Character Types")
        
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        # Create modern checkboxes in grid
        check_frame = tk.Frame(chars_card, bg=self.card_bg)
        check_frame.pack(fill='x', pady=10)
        
        # Row 1
        row1 = tk.Frame(check_frame, bg=self.card_bg)
        row1.pack(fill='x', pady=8)
        
        self.create_modern_checkbox(row1, "Uppercase (A-Z)", self.uppercase_var).pack(side='left', padx=(0, 20))
        self.create_modern_checkbox(row1, "Lowercase (a-z)", self.lowercase_var).pack(side='left')
        
        # Row 2
        row2 = tk.Frame(check_frame, bg=self.card_bg)
        row2.pack(fill='x', pady=8)
        
        self.create_modern_checkbox(row2, "Numbers (0-9)", self.numbers_var).pack(side='left', padx=(0, 20))
        self.create_modern_checkbox(row2, "Symbols (!@#$%)", self.symbols_var).pack(side='left')
        
        # Security Rules Section
        security_card = self.create_card(self.scrollable_frame, "Security Settings")
        
        self.no_similar_var = tk.BooleanVar(value=True)
        self.no_ambiguous_var = tk.BooleanVar(value=False)
        self.require_all_types_var = tk.BooleanVar(value=True)
        
        security_frame = tk.Frame(security_card, bg=self.card_bg)
        security_frame.pack(fill='x', pady=10)
        
        self.create_modern_checkbox(security_frame, "Exclude similar characters (i, l, 1, L, o, 0, O)", 
                                  self.no_similar_var).pack(anchor='w', pady=5)
        self.create_modern_checkbox(security_frame, "Exclude ambiguous characters ({ } [ ] ( ) / \\ ' \" ` ~)", 
                                  self.no_ambiguous_var).pack(anchor='w', pady=5)
        self.create_modern_checkbox(security_frame, "Include all character types", 
                                  self.require_all_types_var).pack(anchor='w', pady=5)
        
        # Exclude Characters Section
        exclude_card = self.create_card(self.scrollable_frame, "Exclude Characters (Optional)")
        
        self.exclude_var = tk.StringVar()
        exclude_entry = tk.Entry(
            exclude_card,
            textvariable=self.exclude_var,
            font=('Arial', 11),
            bg='#f8f9fa',
            fg=self.text_color,
            relief='flat',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.accent_color,
            highlightbackground=self.border_color
        )
        exclude_entry.pack(fill='x', pady=10, ipady=8)
        
        tk.Label(
            exclude_card,
            text="Enter specific characters to exclude from password",
            font=('Arial', 9),
            bg=self.card_bg,
            fg=self.text_light
        ).pack(anchor='w')
        
        # Generated Password Section
        password_card = self.create_card(self.scrollable_frame, "Generated Password")
        
        # Strength indicator
        self.strength_var = tk.StringVar(value="Click Generate to see strength")
        self.strength_label = tk.Label(
            password_card,
            textvariable=self.strength_var,
            font=('Arial', 10, 'bold'),
            bg=self.card_bg,
            fg=self.text_light
        )
        self.strength_label.pack(anchor='w', pady=(0, 10))
        
        # Password display
        password_display_frame = tk.Frame(password_card, bg=self.card_bg)
        password_display_frame.pack(fill='x', pady=10)
        
        self.password_var = tk.StringVar()
        password_entry = tk.Entry(
            password_display_frame,
            textvariable=self.password_var,
            font=('Consolas', 14, 'bold'),
            state='readonly',
            bg='#f8f9fa',
            fg=self.text_color,
            justify='center',
            relief='flat',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.border_color,
            highlightbackground=self.border_color
        )
        password_entry.pack(fill='x', ipady=12)
        
        # Save Password Section
        save_card = self.create_card(self.scrollable_frame, "Save Password")
        
        # Website/App name
        website_frame = tk.Frame(save_card, bg=self.card_bg)
        website_frame.pack(fill='x', pady=5)
        
        tk.Label(
            website_frame,
            text="Website/App:",
            font=('Arial', 10, 'bold'),
            bg=self.card_bg,
            fg=self.text_color
        ).pack(anchor='w')
        
        self.website_var = tk.StringVar()
        website_entry = tk.Entry(
            website_frame,
            textvariable=self.website_var,
            font=('Arial', 11),
            bg='#f8f9fa',
            fg=self.text_color,
            relief='flat',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.accent_color,
            highlightbackground=self.border_color
        )
        website_entry.pack(fill='x', pady=5, ipady=8)
        
        # Username/Email
        username_frame = tk.Frame(save_card, bg=self.card_bg)
        username_frame.pack(fill='x', pady=5)
        
        tk.Label(
            username_frame,
            text="Username/Email:",
            font=('Arial', 10, 'bold'),
            bg=self.card_bg,
            fg=self.text_color
        ).pack(anchor='w')
        
        self.username_var = tk.StringVar()
        username_entry = tk.Entry(
            username_frame,
            textvariable=self.username_var,
            font=('Arial', 11),
            bg='#f8f9fa',
            fg=self.text_color,
            relief='flat',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.accent_color,
            highlightbackground=self.border_color
        )
        username_entry.pack(fill='x', pady=5, ipady=8)
        
        # Notes
        notes_frame = tk.Frame(save_card, bg=self.card_bg)
        notes_frame.pack(fill='x', pady=5)
        
        tk.Label(
            notes_frame,
            text="Notes (optional):",
            font=('Arial', 10, 'bold'),
            bg=self.card_bg,
            fg=self.text_color
        ).pack(anchor='w')
        
        self.notes_var = tk.StringVar()
        notes_entry = tk.Entry(
            notes_frame,
            textvariable=self.notes_var,
            font=('Arial', 11),
            bg='#f8f9fa',
            fg=self.text_color,
            relief='flat',
            bd=1,
            highlightthickness=1,
            highlightcolor=self.accent_color,
            highlightbackground=self.border_color
        )
        notes_entry.pack(fill='x', pady=5, ipady=8)
        
        # Action Buttons
        buttons_card = self.create_card(self.scrollable_frame, top_margin=10, bottom_margin=20)
        
        buttons_frame = tk.Frame(buttons_card, bg=self.card_bg)
        buttons_frame.pack(fill='x', pady=10)
        
        # Generate Button (Primary)
        self.generate_btn = tk.Button(
            buttons_frame,
            text="🎲 GENERATE PASSWORD",
            command=self.generate_password,
            font=('Arial', 12, 'bold'),
            bg=self.accent_color,
            fg='white',
            relief='flat',
            bd=0,
            padx=30,
            pady=15,
            cursor='hand2'
        )
        self.generate_btn.pack(fill='x', pady=5)
        
        # Secondary buttons frame
        secondary_buttons = tk.Frame(buttons_frame, bg=self.card_bg)
        secondary_buttons.pack(fill='x', pady=10)
        
        # Save Button
        self.save_btn = tk.Button(
            secondary_buttons,
            text="💾 Save Password",
            command=self.save_password,
            font=('Arial', 10),
            bg='#38b000',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.save_btn.pack(side='left', padx=(0, 10))
        
        # Copy Button
        self.copy_btn = tk.Button(
            secondary_buttons,
            text="📋 Copy Password",
            command=self.copy_to_clipboard,
            font=('Arial', 10),
            bg=self.accent_color,
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.copy_btn.pack(side='left', padx=(0, 10))
        
        # View Saved Button
        self.view_btn = tk.Button(
            secondary_buttons,
            text="📁 View Saved",
            command=self.view_saved_passwords,
            font=('Arial', 10),
            bg='#6a4c93',
            fg='white',
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.view_btn.pack(side='left', padx=(0, 10))
        
        # Clear Button
        self.clear_btn = tk.Button(
            secondary_buttons,
            text="🔄 Clear",
            command=self.clear_all,
            font=('Arial', 10),
            bg='#e9ecef',
            fg=self.text_color,
            relief='flat',
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.clear_btn.pack(side='left')
        
        # Add hover effects
        self.setup_button_hover()
        
    def create_card(self, parent, title=None, top_margin=5, bottom_margin=5):
        """Create a modern card container"""
        card = tk.Frame(parent, bg=self.card_bg, relief='flat', bd=1, highlightbackground=self.border_color, highlightthickness=1)
        card.pack(fill='x', pady=(top_margin, bottom_margin), ipadx=15, ipady=10)
        
        if title:
            title_label = tk.Label(
                card,
                text=title,
                font=('Arial', 12, 'bold'),
                bg=self.card_bg,
                fg=self.text_color
            )
            title_label.pack(anchor='w', pady=(0, 5))
            
        return card
        
    def create_modern_checkbox(self, parent, text, variable):
        """Create a modern-looking checkbox"""
        frame = tk.Frame(parent, bg=self.card_bg)
        
        def toggle_checkbox():
            variable.set(not variable.get())
            self.update_checkbox_display()
            self.update_password_strength()
            
        def update_checkbox_display():
            if variable.get():
                check_canvas.configure(bg=self.accent_color)
                check_label.config(fg=self.text_color)
            else:
                check_canvas.configure(bg='#e9ecef')
                check_label.config(fg=self.text_light)
                
        # Checkbox canvas
        check_canvas = tk.Canvas(frame, width=20, height=20, bg='#e9ecef', highlightthickness=0)
        check_canvas.pack(side='left', padx=(0, 8))
        check_canvas.bind("<Button-1>", lambda e: toggle_checkbox())
        
        # Checkbox label
        check_label = tk.Label(
            frame,
            text=text,
            font=('Arial', 10),
            bg=self.card_bg,
            fg=self.text_light,
            cursor='hand2'
        )
        check_label.pack(side='left')
        check_label.bind("<Button-1>", lambda e: toggle_checkbox())
        
        # Store references for updating
        frame.check_canvas = check_canvas
        frame.check_label = check_label
        frame.variable = variable
        frame.update_display = update_checkbox_display
        
        # Initial update
        update_checkbox_display()
        
        return frame
        
    def update_checkbox_display(self):
        """Update all checkbox displays"""
        for widget in self.scrollable_frame.winfo_children():
            self._update_checkbox_widget(widget)
            
    def _update_checkbox_widget(self, widget):
        if hasattr(widget, 'update_display'):
            widget.update_display()
        for child in widget.winfo_children():
            self._update_checkbox_widget(child)
        
    def setup_button_hover(self):
        # Generate button hover
        self.generate_btn.bind("<Enter>", lambda e: self.generate_btn.config(bg=self.accent_light))
        self.generate_btn.bind("<Leave>", lambda e: self.generate_btn.config(bg=self.accent_color))
        
        # Save button hover
        self.save_btn.bind("<Enter>", lambda e: self.save_btn.config(bg='#2d7a00'))
        self.save_btn.bind("<Leave>", lambda e: self.save_btn.config(bg='#38b000'))
        
        # Copy button hover
        self.copy_btn.bind("<Enter>", lambda e: self.copy_btn.config(bg=self.accent_light))
        self.copy_btn.bind("<Leave>", lambda e: self.copy_btn.config(bg=self.accent_color))
        
        # View button hover
        self.view_btn.bind("<Enter>", lambda e: self.view_btn.config(bg='#5a3d7a'))
        self.view_btn.bind("<Leave>", lambda e: self.view_btn.config(bg='#6a4c93'))
        
        # Clear button hover
        self.clear_btn.bind("<Enter>", lambda e: self.clear_btn.config(bg='#dee2e6'))
        self.clear_btn.bind("<Leave>", lambda e: self.clear_btn.config(bg='#e9ecef'))
        
    def on_length_change(self, value):
        length = int(float(value))
        self.length_var.set(length)
        self.length_value_label.config(text=str(length))
        self.update_password_strength()
        
    def get_character_sets(self):
        """Get character sets based on user selection"""
        char_sets = []
        
        if self.uppercase_var.get():
            char_sets.append(string.ascii_uppercase)
        if self.lowercase_var.get():
            char_sets.append(string.ascii_lowercase)
        if self.numbers_var.get():
            char_sets.append(string.digits)
        if self.symbols_var.get():
            char_sets.append('!@#$%^&*()_+-=[]{}|;:,.<>?')
        
        return char_sets
    
    def apply_security_rules(self, char_sets):
        """Apply security rules to character sets"""
        excluded_chars = self.exclude_var.get()
        
        if self.no_similar_var.get():
            excluded_chars += 'il1Lo0O'
        
        if self.no_ambiguous_var.get():
            excluded_chars += '{}[]()/\\\'"`~,;:.<>'
        
        # Remove excluded characters from all sets
        filtered_sets = []
        for char_set in char_sets:
            filtered_set = ''.join(char for char in char_set if char not in excluded_chars)
            if filtered_set:  # Only add non-empty sets
                filtered_sets.append(filtered_set)
        
        return filtered_sets
    
    def validate_input(self):
        """Validate user input"""
        char_sets = self.get_character_sets()
        if not char_sets:
            messagebox.showerror("Error", "Please select at least one character type!")
            return False
        
        filtered_sets = self.apply_security_rules(char_sets)
        if not filtered_sets:
            messagebox.showerror("Error", "No characters available after applying security rules and exclusions!")
            return False
        
        return True
    
    def generate_password(self):
        """Generate password based on user criteria"""
        if not self.validate_input():
            return
        
        length = self.length_var.get()
        char_sets = self.get_character_sets()
        filtered_sets = self.apply_security_rules(char_sets)
        
        # Combine all character sets
        all_chars = ''.join(filtered_sets)
        
        max_attempts = 100
        for attempt in range(max_attempts):
            # Generate password
            password = ''.join(random.choice(all_chars) for _ in range(length))
            
            # Check if we need to require all types
            if self.require_all_types_var.get():
                if not self.contains_all_types(password, filtered_sets):
                    continue
            
            # Password meets all criteria
            self.password_var.set(password)
            self.update_password_strength()
            return
        
        # If we couldn't generate a password meeting all criteria
        messagebox.showwarning("Warning", 
                              "Could not generate password meeting all security rules. "
                              "Try increasing length or relaxing some rules.")
        self.generate_fallback_password(filtered_sets, length)
    
    def generate_fallback_password(self, char_sets, length):
        """Generate a password without strict type requirements"""
        all_chars = ''.join(char_sets)
        password = ''.join(random.choice(all_chars) for _ in range(length))
        self.password_var.set(password)
        self.update_password_strength()
    
    def contains_all_types(self, password, char_sets):
        """Check if password contains at least one character from each selected type"""
        for char_set in char_sets:
            if not any(char in char_set for char in password):
                return False
        return True
    
    def calculate_password_strength(self, password):
        """Calculate password strength based on various factors"""
        if not password:
            return 0, "Not calculated", self.text_light
        
        score = 0
        length = len(password)
        
        # Length score
        if length >= 8:
            score += 1
        if length >= 12:
            score += 1
        if length >= 16:
            score += 1
        if length >= 20:
            score += 1
        
        # Character variety score
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(not c.isalnum() for c in password)
        
        variety_count = sum([has_upper, has_lower, has_digit, has_symbol])
        score += variety_count
        
        # Entropy bonus
        unique_chars = len(set(password))
        if unique_chars / length > 0.8:
            score += 1
        
        # Determine strength level
        if score >= 8:
            return score, "Very Strong 🔒", self.success_color
        elif score >= 6:
            return score, "Strong 🔐", self.success_color
        elif score >= 4:
            return score, "Good 🛡️", '#4895ef'
        elif score >= 2:
            return score, "Weak ⚠️", self.warning_color
        else:
            return score, "Very Weak 🚨", self.warning_color
    
    def update_password_strength(self, event=None):
        """Update password strength indicator"""
        password = self.password_var.get()
        score, strength, color = self.calculate_password_strength(password)
        
        # Update strength label
        char_sets = self.get_character_sets()
        if not char_sets:
            self.strength_var.set("Please select character types")
            self.strength_label.configure(fg=self.text_light)
        elif not password:
            self.strength_var.set("Click Generate to see strength")
            self.strength_label.configure(fg=self.text_light)
        else:
            self.strength_var.set(f"Strength: {strength} (Score: {score}/10)")
            self.strength_label.configure(fg=color)
    
    def save_password(self):
        """Save the generated password with metadata"""
        password = self.password_var.get()
        website = self.website_var.get().strip()
        username = self.username_var.get().strip()
        
        if not password:
            messagebox.showwarning("Warning", "No password generated to save!")
            return
            
        if not website:
            messagebox.showwarning("Warning", "Please enter a website or app name!")
            return
            
        if not username:
            messagebox.showwarning("Warning", "Please enter a username or email!")
            return
        
        # Create password entry
        password_entry = {
            'website': website,
            'username': username,
            'password': password,
            'notes': self.notes_var.get().strip(),
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'length': len(password),
            'strength': self.calculate_password_strength(password)[1]
        }
        
        # Add to saved passwords
        self.saved_passwords.append(password_entry)
        
        # Save to file
        self.save_passwords_to_file()
        
        # Clear save fields
        self.website_var.set("")
        self.username_var.set("")
        self.notes_var.set("")
        
        messagebox.showinfo("Success", f"Password for {website} saved successfully!")
    
    def view_saved_passwords(self):
        """Display saved passwords in a new window"""
        if not self.saved_passwords:
            messagebox.showinfo("Info", "No saved passwords found!")
            return
        
        # Create new window
        view_window = tk.Toplevel(self.root)
        view_window.title("📁 Saved Passwords")
        view_window.geometry("600x500")
        view_window.configure(bg=self.bg_color)
        view_window.minsize(500, 400)
        
        # Header
        header_frame = tk.Frame(view_window, bg=self.card_bg, relief='flat', bd=1, 
                               highlightbackground=self.border_color, highlightthickness=1)
        header_frame.pack(fill='x', padx=20, pady=10, ipadx=15, ipady=10)
        
        tk.Label(
            header_frame,
            text="📁 Saved Passwords",
            font=('Arial', 16, 'bold'),
            bg=self.card_bg,
            fg=self.text_color
        ).pack()
        
        # Create scrollable text area
        text_frame = tk.Frame(view_window, bg=self.bg_color)
        text_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        text_widget = scrolledtext.ScrolledText(
            text_frame,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg=self.card_bg,
            fg=self.text_color,
            relief='flat',
            bd=1,
            highlightbackground=self.border_color,
            highlightthickness=1
        )
        text_widget.pack(fill='both', expand=True)
        
        # Display saved passwords
        for i, entry in enumerate(self.saved_passwords, 1):
            text_widget.insert(tk.END, f"Entry #{i}\n")
            text_widget.insert(tk.END, f"Website/App: {entry['website']}\n")
            text_widget.insert(tk.END, f"Username: {entry['username']}\n")
            text_widget.insert(tk.END, f"Password: {entry['password']}\n")
            text_widget.insert(tk.END, f"Length: {entry['length']} | Strength: {entry['strength']}\n")
            if entry['notes']:
                text_widget.insert(tk.END, f"Notes: {entry['notes']}\n")
            text_widget.insert(tk.END, f"Created: {entry['created_at']}\n")
            text_widget.insert(tk.END, "-" * 50 + "\n\n")
        
        text_widget.config(state=tk.DISABLED)
        
        # Buttons frame
        buttons_frame = tk.Frame(view_window, bg=self.bg_color)
        buttons_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(
            buttons_frame,
            text="Close",
            command=view_window.destroy,
            font=('Arial', 10),
            bg=self.accent_color,
            fg='white',
            relief='flat',
            padx=20,
            pady=8
        ).pack(side='right')
    
    def copy_to_clipboard(self):
        """Copy generated password to clipboard"""
        password = self.password_var.get()
        if password:
            try:
                pyperclip.copy(password)
                messagebox.showinfo("Success", "Password copied to clipboard!")
            except Exception as e:
                messagebox.showerror("Error", f"Could not copy to clipboard: {str(e)}")
        else:
            messagebox.showwarning("Warning", "No password generated to copy!")
    
    def clear_all(self):
        """Clear all fields"""
        self.password_var.set("")
        self.exclude_var.set("")
        self.website_var.set("")
        self.username_var.set("")
        self.notes_var.set("")
        self.update_password_strength()

def main():
    try:
        import pyperclip
    except ImportError:
        print("Installing pyperclip...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyperclip"])
        import pyperclip
    
    root = tk.Tk()
    app = ModernPasswordGenerator(root)
    root.mainloop()

if __name__ == "__main__":
    main()