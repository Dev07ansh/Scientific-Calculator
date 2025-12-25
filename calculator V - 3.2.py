"""
Scientific Calculator Application
Project: Calculator Software
Student: Devansh Maheshwari (AU2520243)
Course: ENR106 Introduction to Programming

Features:
- Basic arithmetic operations (Add, Subtract, Multiply, Divide, Modulo)
- Scientific functions (Trigonometry, Logarithms, Powers, Roots)
- Sine curve visualization when calculating sin values
- Error handling and validation
- Calculation history tracking
- User-friendly GUI with Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class ScientificCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator - AU2520243")
        self.root.geometry("1100x650")
        self.root.resizable(True, True)
        self.root.configure(bg='#1a1a2e')
        
        # Variables
        self.display_var = tk.StringVar(value="0")
        self.equation = ""
        self.history = []
        self.is_degree = True
        self.error_message = tk.StringVar(value="")
        self.show_graph = False
        
        # Graph variables
        self.graph_frame = None
        self.canvas = None
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title Frame
        title_frame = tk.Frame(self.root, bg='#1a1a2e')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="Scientific Calculator with Sine Curve Visualization",
            font=('Arial', 16, 'bold'),
            bg='#1a1a2e',
            fg='#ffffff'
        )
        title_label.pack()
        
        student_label = tk.Label(
            title_frame,
            text="Devansh Maheshwari - AU2520243",
            font=('Arial', 9),
            bg='#1a1a2e',
            fg='#a8a8ff'
        )
        student_label.pack()
        
        # Main container
        main_container = tk.Frame(self.root, bg='#1a1a2e')
        main_container.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Left side - Calculator
        calc_frame = tk.Frame(main_container, bg='#2d2d44', relief='raised', bd=2)
        calc_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)
        
        # Display Frame
        display_frame = tk.Frame(calc_frame, bg='#16213e', relief='sunken', bd=3)
        display_frame.pack(padx=10, pady=10, fill='x')
        
        # Equation display
        self.equation_label = tk.Label(
            display_frame,
            text="",
            font=('Arial', 12),
            bg='#16213e',
            fg='#a8a8ff',
            anchor='e',
            height=1
        )
        self.equation_label.pack(fill='x', padx=5)
        
        # Main display
        display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=('Arial', 22, 'bold'),
            bg='#16213e',
            fg="#0e0e0e",
            justify='right',
            bd=0,
            state='readonly'
        )
        display.pack(fill='x', padx=5, pady=5)
        
        # Error message
        error_label = tk.Label(
            display_frame,
            textvariable=self.error_message,
            font=('Arial', 10),
            bg='#16213e',
            fg='#ff6b6b',
            anchor='e',
            height=1
        )
        error_label.pack(fill='x', padx=5)
        
        # Mode buttons
        mode_frame = tk.Frame(calc_frame, bg='#2d2d44')
        mode_frame.pack(pady=5)
        
        self.deg_rad_btn = tk.Button(
            mode_frame,
            text="DEG",
            font=('Arial', 10, 'bold'),
            bg='#4a4e69',
            fg='#ffffff',
            width=8,
            command=self.toggle_degree_radian
        )
        self.deg_rad_btn.pack(side='left', padx=5)
        
        # Graph toggle button
        self.graph_toggle_btn = tk.Button(
            mode_frame,
            text="Show Graph",
            font=('Arial', 10, 'bold'),
            bg='#4a4e69',
            fg='#ffffff',
            width=12,
            command=self.toggle_graph
        )
        self.graph_toggle_btn.pack(side='left', padx=5)
        
        # Scientific Functions Frame
        sci_frame = tk.Frame(calc_frame, bg='#2d2d44')
        sci_frame.pack(pady=5)
        
        scientific_buttons = [
            ('sin', 'cos', 'tan', 'x^y', '√'),
            ('ln', 'log', '∛', 'x²', '|x|'),
            ('n!', '%', '+/-', 'mod', 'π')
        ]
        
        for row in scientific_buttons:
            row_frame = tk.Frame(sci_frame, bg='#2d2d44')
            row_frame.pack()
            for btn_text in row:
                btn = tk.Button(
                    row_frame,
                    text=btn_text,
                    font=('Arial', 10, 'bold'),
                    bg='#5e60ce',
                    fg='#ffffff',
                    width=6,
                    height=1,
                    command=lambda t=btn_text: self.handle_scientific(t)
                )
                btn.pack(side='left', padx=2, pady=2)
        
        # Basic Buttons Frame
        buttons_frame = tk.Frame(calc_frame, bg='#2d2d44')
        buttons_frame.pack(pady=10)
        
        basic_buttons = [
            ('C', '⌫', '(', ')'),
            ('7', '8', '9', '÷'),
            ('4', '5', '6', '×'),
            ('1', '2', '3', '-'),
            ('0', '.', '=', '+')
        ]
        
        for row in basic_buttons:
            row_frame = tk.Frame(buttons_frame, bg='#2d2d44')
            row_frame.pack()
            for btn_text in row:
                if btn_text == 'C':
                    bg_color = '#dc3545'
                elif btn_text == '⌫':
                    bg_color = '#fd7e14'
                elif btn_text == '=':
                    bg_color = '#28a745'
                elif btn_text in ['÷', '×', '-', '+']:
                    bg_color = '#6c5ce7'
                else:
                    bg_color = '#495057'
                
                btn = tk.Button(
                    row_frame,
                    text=btn_text,
                    font=('Arial', 14, 'bold'),
                    bg=bg_color,
                    fg='#ffffff',
                    width=6,
                    height=1,
                    command=lambda t=btn_text: self.handle_button(t)
                )
                btn.pack(side='left', padx=2, pady=2)
        
        # Right side - History
        history_frame = tk.Frame(main_container, bg='#2d2d44', relief='raised', bd=2)
        history_frame.pack(side='right', padx=10, pady=10, fill='both')
        
        history_title = tk.Label(
            history_frame,
            text="History",
            font=('Arial', 12, 'bold'),
            bg='#2d2d44',
            fg='#ffffff'
        )
        history_title.pack(pady=5)
        
        self.history_text = scrolledtext.ScrolledText(
            history_frame,
            font=('Courier', 9),
            bg='#16213e',
            fg='#ffffff',
            width=28,
            height=25,
            state='disabled'
        )
        self.history_text.pack(padx=5, pady=5)
        
        clear_history_btn = tk.Button(
            history_frame,
            text="Clear History",
            font=('Arial', 10),
            bg='#dc3545',
            fg='#ffffff',
            command=self.clear_history
        )
        clear_history_btn.pack(pady=5)
        
        # Graph Frame (initially hidden)
        self.graph_container = tk.Frame(main_container, bg='#2d2d44', relief='raised', bd=2)
        
        # Features info
        info_frame = tk.Frame(self.root, bg='#2d2d44', relief='raised', bd=2)
        info_frame.pack(padx=20, pady=10, fill='x')
        
        info_text = "Features: Basic Operations | Scientific Functions | Sine Curve Visualization | Error Handling"
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 8),
            bg='#2d2d44',
            fg='#a8a8ff',
            wraplength=1000,
            justify='center'
        )
        info_label.pack(pady=5)
    
    def toggle_graph(self):
        """Toggle graph visibility"""
        self.show_graph = not self.show_graph
        if self.show_graph:
            self.graph_container.pack(side='right', padx=10, pady=10, fill='both', expand=True)
            self.graph_toggle_btn.config(text="Hide Graph")
            self.root.geometry("1400x650")
        else:
            self.graph_container.pack_forget()
            self.graph_toggle_btn.config(text="Show Graph")
            self.root.geometry("1100x650")
    
    def plot_sine_curve(self, angle_input, result):
        """Plot sine curve with the calculated point"""
        # Clear previous graph
        for widget in self.graph_container.winfo_children():
            widget.destroy()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(5, 4), facecolor='#2d2d44')
        ax.set_facecolor('#16213e')
        
        # Generate sine curve data
        if self.is_degree:
            x_degrees = np.linspace(-360, 360, 1000)
            x_radians = np.radians(x_degrees)
            angle_rad = np.radians(angle_input)
            xlabel = 'Angle (degrees)'
            angle_display = angle_input
        else:
            x_radians = np.linspace(-2*np.pi, 2*np.pi, 1000)
            x_degrees = np.degrees(x_radians)
            angle_rad = angle_input
            xlabel = 'Angle (radians)'
            angle_display = angle_input
        
        y = np.sin(x_radians)
        
        # Plot sine curve
        ax.plot(x_degrees if self.is_degree else x_radians, y, 
                color='#5e60ce', linewidth=2, label='sin(x)')
        
        # Mark the calculated point
        ax.scatter(angle_display, result, color='#ff6b6b', s=100, 
                  zorder=5, label=f'sin({angle_display:.2f}) = {result:.4f}')
        
        # Styling
        ax.set_xlabel(xlabel, color='#ffffff', fontsize=10)
        ax.set_ylabel('sin(x)', color='#ffffff', fontsize=10)
        ax.set_title('Sine Curve', color='#ffffff', fontsize=12, fontweight='bold')
        ax.grid(True, alpha=0.3, color='#a8a8ff')
        ax.axhline(0, color='#ffffff', linewidth=0.5, alpha=0.5)
        ax.axvline(0, color='#ffffff', linewidth=0.5, alpha=0.5)
        ax.tick_params(colors='#ffffff', labelsize=8)
        ax.legend(facecolor='#2d2d44', edgecolor='#5e60ce', 
                 labelcolor='#ffffff', fontsize=8)
        
        # Adjust spines
        for spine in ax.spines.values():
            spine.set_color('#5e60ce')
        
        plt.tight_layout()
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Store canvas reference
        self.canvas = canvas
    
    def handle_button(self, btn_text):
        """Handle basic button clicks"""
        self.error_message.set("")
        
        if btn_text == 'C':
            self.clear()
        elif btn_text == '⌫':
            self.backspace()
        elif btn_text == '=':
            self.calculate()
        elif btn_text in ['÷', '×', '-', '+']:
            self.handle_operator(btn_text)
        elif btn_text in ['(', ')']:
            self.add_parenthesis(btn_text)
        elif btn_text == '.':
            self.add_decimal()
        else:
            self.add_number(btn_text)
    
    def add_number(self, num):
        """Add number to display"""
        current = self.display_var.get()
        if current == "0" or current == "Error":
            self.display_var.set(num)
        else:
            self.display_var.set(current + num)
    
    def add_decimal(self):
        """Add decimal point"""
        current = self.display_var.get()
        if '.' not in current:
            self.display_var.set(current + '.')
    
    def add_parenthesis(self, paren):
        """Add parenthesis"""
        current = self.display_var.get()
        if current == "0":
            self.display_var.set(paren)
        else:
            self.display_var.set(current + paren)
    
    def handle_operator(self, operator):
        """Handle operator button clicks"""
        if self.display_var.get() == "Error":
            return
        
        # Map symbols
        op_map = {'÷': '/', '×': '*'}
        op = op_map.get(operator, operator)
        
        if self.equation and not self.equation.endswith(' '):
            self.calculate()
        
        self.equation = self.display_var.get() + ' ' + op + ' '
        self.equation_label.config(text=self.equation)
        self.display_var.set("0")
    
    def calculate(self):
        """Calculate the result"""
        self.error_message.set("")
        try:
            if self.equation:
                parts = self.equation.strip().split(' ')
                num1 = float(parts[0])
                operator = parts[1]
                num2 = float(self.display_var.get())
                
                # Error checking
                if operator == '/' and num2 == 0:
                    self.error_message.set("Error: Division by zero")
                    self.display_var.set("Error")
                    self.equation = ""
                    self.equation_label.config(text="")
                    return
                
                if operator == '%' and num2 == 0:
                    self.error_message.set("Error: Modulo by zero")
                    self.display_var.set("Error")
                    self.equation = ""
                    self.equation_label.config(text="")
                    return
                
                # Calculate
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    result = num1 / num2
                elif operator == '%':
                    result = num1 % num2
                elif operator == '**':
                    result = num1 ** num2
                else:
                    result = num2
                
                # Format result
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
                
                # Add to history
                history_entry = f"{num1} {operator} {num2} = {result}"
                self.add_to_history(history_entry)
                
                self.display_var.set(str(result))
                self.equation = ""
                self.equation_label.config(text="")
        
        except Exception as e:
            self.error_message.set("Error: Invalid calculation")
            self.display_var.set("Error")
            self.equation = ""
            self.equation_label.config(text="")
    
    def handle_scientific(self, func):
        """Handle scientific function buttons"""
        self.error_message.set("")
        try:
            current = self.display_var.get()
            
            if func == 'π':
                self.display_var.set(str(math.pi))
                return
            
            if func == 'mod':
                self.handle_operator('%')
                return
            
            if func == 'x^y':
                if self.equation and not self.equation.endswith(' '):
                    self.calculate()
                self.equation = self.display_var.get() + ' ** '
                self.equation_label.config(text=self.equation + '^')
                self.display_var.set("0")
                return
            
            num = float(current)
            result = None
            
            # Error checking for specific functions
            if func == '√' and num < 0:
                self.error_message.set("Error: Square root of negative number")
                self.display_var.set("Error")
                return
            
            if func in ['ln', 'log'] and num <= 0:
                self.error_message.set("Error: Logarithm of non-positive number")
                self.display_var.set("Error")
                return
            
            if func == 'n!' and (num < 0 or num != int(num)):
                self.error_message.set("Error: Factorial requires non-negative integer")
                self.display_var.set("Error")
                return
            
            # Calculate scientific functions
            if func == 'sin':
                angle = math.radians(num) if self.is_degree else num
                result = math.sin(angle)
                # Plot sine curve if graph is visible
                if self.show_graph:
                    self.plot_sine_curve(num, result)
            elif func == 'cos':
                angle = math.radians(num) if self.is_degree else num
                result = math.cos(angle)
            elif func == 'tan':
                angle = math.radians(num) if self.is_degree else num
                result = math.tan(angle)
            elif func == '√':
                result = math.sqrt(num)
            elif func == '∛':
                result = num ** (1/3)
            elif func == 'ln':
                result = math.log(num)
            elif func == 'log':
                result = math.log10(num)
            elif func == 'x²':
                result = num ** 2
            elif func == '|x|':
                result = abs(num)
            elif func == 'n!':
                result = math.factorial(int(num))
            elif func == '%':
                result = num / 100
            elif func == '+/-':
                result = -num
            
            if result is not None:
                # Format result
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 10)
                
                # Add to history
                history_entry = f"{func}({num}) = {result}"
                self.add_to_history(history_entry)
                
                self.display_var.set(str(result))
        
        except Exception as e:
            self.error_message.set(f"Error: Invalid operation")
            self.display_var.set("Error")
    
    def clear(self):
        """Clear display and equation"""
        self.display_var.set("0")
        self.equation = ""
        self.equation_label.config(text="")
        self.error_message.set("")
    
    def backspace(self):
        """Remove last character"""
        current = self.display_var.get()
        if len(current) > 1 and current != "Error":
            self.display_var.set(current[:-1])
        else:
            self.display_var.set("0")
    
    def toggle_degree_radian(self):
        """Toggle between degree and radian mode"""
        self.is_degree = not self.is_degree
        self.deg_rad_btn.config(text="DEG" if self.is_degree else "RAD")
    
    def add_to_history(self, entry):
        """Add calculation to history"""
        self.history.insert(0, entry)
        if len(self.history) > 50:
            self.history.pop()
        
        self.update_history_display()
    
    def update_history_display(self):
        """Update history text widget"""
        self.history_text.config(state='normal')
        self.history_text.delete(1.0, tk.END)
        for entry in self.history:
            self.history_text.insert(tk.END, entry + '\n')
        self.history_text.config(state='disabled')
    
    def clear_history(self):
        """Clear calculation history"""
        self.history.clear()
        self.update_history_display()


def main():
    """Main function to run the calculator"""
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()