"""
Scientific Calculator Application
Project: Calculator Software
Student: Devansh Maheshwari (AU2520243)
Course: ENR106 Introduction to Programming

Features:
- Basic arithmetic operations (Add, Subtract, Multiply, Divide, Modulo)
- Scientific functions (Trigonometry, Logarithms, Powers, Roots)
- Error handling and validation
- Calculation history tracking
- User-friendly GUI with Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import math

class ScientificCalculator:
    def __init__(window, root):
        window.root = root
        window.root.title("Scientific Calculator - AU2520243")
        window.root.geometry("750x650")
        window.root.resizable(True, True)
        window.root.configure(bg='#1a1a2e')
        
        # Variables
        window.display_var = tk.StringVar(value="0")
        window.equation = ""
        window.history = []
        window.is_degree = True
        window.error_message = tk.StringVar(value="")
        
        # Setup UI
        window.setup_ui()
        
    def setup_ui(window):
        """Setup the user interface"""
        # Title Frame
        title_frame = tk.Frame(window.root, bg='#1a1a2e')
        title_frame.pack(pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="Scientific Calculator",
            font=('Arial', 18, 'bold'),
            bg='#1a1a2e',
            fg="#F9F8F8"
        )
        title_label.pack()
        
        student_label = tk.Label(
            title_frame,
            font=('Arial', 9),
            bg='#1a1a2e',
            fg='#a8a8ff'
        )
        student_label.pack()
        
        # Main container
        main_container = tk.Frame(window.root, bg='#1a1a2e')
        main_container.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Left side - Calculator
        calc_frame = tk.Frame(main_container, bg='#2d2d44', relief='raised', bd=2)
        calc_frame.pack(side='left', padx=10, pady=10, fill='both', expand=True)
        
        # Display Frame
        display_frame = tk.Frame(calc_frame, bg='#16213e', relief='sunken', bd=3)
        display_frame.pack(padx=10, pady=10, fill='x')
        
        # Equation display
        window.equation_label = tk.Label(
            display_frame,
            text="",
            font=('Arial', 12),
            bg='#16213e',
            fg='#a8a8ff',
            anchor='e',
            height=1
        )
        window.equation_label.pack(fill='x', padx=5)
        
        # Main display
        display = tk.Entry(
            display_frame,
            textvariable=window.display_var,
            font=('Arial', 22, 'bold'),
            bg='#16213e',
            fg="#101010",
            justify='right',
            bd=0,
            state='readonly'
        )
        display.pack(fill='x', padx=5, pady=5)
        
        # Error message
        error_label = tk.Label(
            display_frame,
            textvariable=window.error_message,
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
        
        window.deg_rad_btn = tk.Button(
            mode_frame,
            text="DEG",
            font=('Arial', 10, 'bold'),
            bg='#4a4e69',
            fg='#ffffff',
            width=8,
            command=window.toggle_degree_radian
        )
        window.deg_rad_btn.pack(side='left', padx=5)
        
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
                    command=lambda t=btn_text: window.handle_scientific(t)
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
                    command=lambda t=btn_text: window.handle_button(t)
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
        
        window.history_text = scrolledtext.ScrolledText(
            history_frame,
            font=('Courier', 9),
            bg='#16213e',
            fg='#ffffff',
            width=28,
            height=25,
            state='disabled'
        )
        window.history_text.pack(padx=5, pady=5)
        
        clear_history_btn = tk.Button(
            history_frame,
            text="Clear History",
            font=('Arial', 10),
            bg='#dc3545',
            fg='#ffffff',
            command=window.clear_history
        )
        clear_history_btn.pack(pady=5)
        
        # Features info
        info_frame = tk.Frame(window.root, bg='#2d2d44', relief='raised', bd=2)
        info_frame.pack(padx=20, pady=10, fill='x')
        
        info_text = "Features: Basic Operations (+ - × ÷ %) | Scientific Functions (sin, cos, tan, ln, log, √, ∛, x², x^y) | Error Handling"
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=('Arial', 8),
            bg='#2d2d44',
            fg='#a8a8ff',
            wraplength=700,
            justify='center'
        )
        info_label.pack(pady=5)
    
    def handle_button(window, btn_text):
        """Handle basic button clicks"""
        window.error_message.set("")
        
        if btn_text == 'C':
            window.clear()
        elif btn_text == '⌫':
            window.backspace()
        elif btn_text == '=':
            window.calculate()
        elif btn_text in ['÷', '×', '-', '+']:
            window.handle_operator(btn_text)
        elif btn_text in ['(', ')']:
            window.add_parenthesis(btn_text)
        elif btn_text == '.':
            window.add_decimal()
        else:
            window.add_number(btn_text)
    
    def add_number(window, num):
        """Add number to display"""
        current = window.display_var.get()
        if current == "0" or current == "Error":
            window.display_var.set(num)
        else:
            window.display_var.set(current + num)
    
    def add_decimal(window):
        """Add decimal point"""
        current = window.display_var.get()
        if '.' not in current:
            window.display_var.set(current + '.')
    
    def add_parenthesis(window, paren):
        """Add parenthesis"""
        current = window.display_var.get()
        if current == "0":
            window.display_var.set(paren)
        else:
            window.display_var.set(current + paren)
    
    def handle_operator(window, operator):
        """Handle operator button clicks"""
        if window.display_var.get() == "Error":
            return
        
        # Map symbols
        op_map = {'÷': '/', '×': '*'}
        op = op_map.get(operator, operator)
        
        if window.equation and not window.equation.endswith(' '):
            window.calculate()
        
        window.equation = window.display_var.get() + ' ' + op + ' '
        window.equation_label.config(text=window.equation)
        window.display_var.set("0")
    
    def calculate(window):
        """Calculate the result"""
        window.error_message.set("")
        try:
            if window.equation:
                parts = window.equation.strip().split(' ')
                num1 = float(parts[0])
                operator = parts[1]
                num2 = float(window.display_var.get())
                
                # Error checking
                if operator == '/' and num2 == 0:
                    window.error_message.set("Error: Division by zero")
                    window.display_var.set("Error")
                    window.equation = ""
                    window.equation_label.config(text="")
                    return
                
                if operator == '%' and num2 == 0:
                    window.error_message.set("Error: Modulo by zero")
                    window.display_var.set("Error")
                    window.equation = ""
                    window.equation_label.config(text="")
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
                window.add_to_history(history_entry)
                
                window.display_var.set(str(result))
                window.equation = ""
                window.equation_label.config(text="")
        
        except Exception as e:
            window.error_message.set("Error: Invalid calculation")
            window.display_var.set("Error")
            window.equation = ""
            window.equation_label.config(text="")
    
    def handle_scientific(window, func):
        """Handle scientific function buttons"""
        window.error_message.set("")
        try:
            current = window.display_var.get()
            
            if func == 'π':
                window.display_var.set(str(math.pi))
                return
            
            if func == 'mod':
                window.handle_operator('%')
                return
            
            if func == 'x^y':
                if window.equation and not window.equation.endswith(' '):
                    window.calculate()
                window.equation = window.display_var.get() + ' ** '
                window.equation_label.config(text=window.equation + '^')
                window.display_var.set("0")
                return
            
            num = float(current)
            result = None
            
            # Error checking for specific functions
            if func == '√' and num < 0:
                window.error_message.set("Error: Square root of negative number")
                window.display_var.set("Error")
                return
            
            if func in ['ln', 'log'] and num <= 0:
                window.error_message.set("Error: Logarithm of non-positive number")
                window.display_var.set("Error")
                return
            
            if func == 'n!' and (num < 0 or num != int(num)):
                window.error_message.set("Error: Factorial requires non-negative integer")
                window.display_var.set("Error")
                return
            
            # Calculate scientific functions
            if func == 'sin':
                angle = math.radians(num) if window.is_degree else num
                result = math.sin(angle)
            elif func == 'cos':
                angle = math.radians(num) if window.is_degree else num
                result = math.cos(angle)
            elif func == 'tan':
                angle = math.radians(num) if window.is_degree else num
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
                window.add_to_history(history_entry)
                
                window.display_var.set(str(result))
        
        except Exception as e:
            window.error_message.set(f"Error: Invalid operation")
            window.display_var.set("Error")
    
    def clear(window):
        """Clear display and equation"""
        window.display_var.set("0")
        window.equation = ""
        window.equation_label.config(text="")
        window.error_message.set("")
    
    def backspace(window):
        """Remove last character"""
        current = window.display_var.get()
        if len(current) > 1 and current != "Error":
            window.display_var.set(current[:-1])
        else:
            window.display_var.set("0")
    
    def toggle_degree_radian(window):
        """Toggle between degree and radian mode"""
        window.is_degree = not window.is_degree
        window.deg_rad_btn.config(text="DEG" if window.is_degree else "RAD")
    
    def add_to_history(window, entry):
        """Add calculation to history"""
        window.history.insert(0, entry)
        if len(window.history) > 50:
            window.history.pop()
        
        window.update_history_display()
    
    def update_history_display(window):
        """Update history text widget"""
        window.history_text.config(state='normal')
        window.history_text.delete(1.0, tk.END)
        for entry in window.history:
            window.history_text.insert(tk.END, entry + '\n')
        window.history_text.config(state='disabled')
    
    def clear_history(window):
        """Clear calculation history"""
        window.history.clear()
        window.update_history_display()


def main():
    """Main function to run the calculator"""
    root = tk.Tk()
    app = ScientificCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()