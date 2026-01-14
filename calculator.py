import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")
        self.root.configure(bg="#0f0f0f")
        self.root.resizable(False, False)
        
        # Variables
        self.current_input = "0"
        self.expression = ""
        self.should_reset = False
        
        # Configure styles
        self.setup_styles()
        
        # Create UI
        self.create_display()
        self.create_buttons()
        
        # Keyboard bindings
        self.setup_keyboard()
        
    def setup_styles(self):
        """Configure color scheme and fonts"""
        self.colors = {
            'bg': '#0f0f0f',
            'display_bg': '#1a1a1a',
            'display_text': '#ff8c00',
            'expression_text': '#ff8c00',
            'number_bg': '#2a2a2a',
            'number_fg': '#ffffff',
            'operator_bg': '#ff8c00',
            'operator_fg': '#0f0f0f',
            'clear_bg': '#ff4444',
            'clear_fg': '#ffffff',
            'equals_bg': '#00cc66',
            'equals_fg': '#ffffff',
            'hover_number': '#353535',
            'hover_operator': '#ff9900',
            'hover_clear': '#ff5555',
            'hover_equals': '#00dd77'
        }
        
        self.display_font = font.Font(family="Segoe UI", size=36, weight="bold")
        self.expression_font = font.Font(family="Segoe UI", size=16)
        self.button_font = font.Font(family="Segoe UI", size=20, weight="bold")
        
    def create_display(self):
        """Create the display area"""
        display_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=20, pady=20)
        display_frame.pack(fill=tk.BOTH, expand=True)
        
        # Expression display
        self.expression_label = tk.Label(
            display_frame,
            text="",
            bg=self.colors['display_bg'],
            fg=self.colors['expression_text'],
            font=self.expression_font,
            anchor='e',
            padx=15,
            pady=10,
            relief=tk.FLAT
        )
        self.expression_label.pack(fill=tk.BOTH, expand=True)
        
        # Result display
        self.result_label = tk.Label(
            display_frame,
            text="0",
            bg=self.colors['display_bg'],
            fg=self.colors['display_text'],
            font=self.display_font,
            anchor='e',
            padx=15,
            pady=15,
            relief=tk.FLAT
        )
        self.result_label.pack(fill=tk.BOTH, expand=True)
        
        # Add border effect
        display_frame.configure(highlightbackground='#ff8c00', highlightthickness=2)
        
    def create_buttons(self):
        """Create button grid"""
        button_frame = tk.Frame(self.root, bg=self.colors['bg'], padx=15, pady=15)
        button_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button layout
        buttons = [
            ['C', 'CE', '⌫', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        self.buttons = {}
        
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == '=':
                    # Equals button spans 2 columns
                    btn = self.create_button(
                        button_frame, text, self.colors['equals_bg'], 
                        self.colors['equals_fg'], self.colors['hover_equals']
                    )
                    btn.grid(row=i, column=j, columnspan=2, sticky='nsew', padx=5, pady=5)
                elif text == '0':
                    # Zero button
                    btn = self.create_button(
                        button_frame, text, self.colors['number_bg'], 
                        self.colors['number_fg'], self.colors['hover_number']
                    )
                    btn.grid(row=i, column=j, sticky='nsew', padx=5, pady=5)
                elif text in ['C', 'CE']:
                    # Clear buttons
                    btn = self.create_button(
                        button_frame, text, self.colors['clear_bg'], 
                        self.colors['clear_fg'], self.colors['hover_clear']
                    )
                    btn.grid(row=i, column=j, sticky='nsew', padx=5, pady=5)
                elif text in ['+', '−', '×', '÷', '⌫']:
                    # Operator buttons
                    btn = self.create_button(
                        button_frame, text, self.colors['operator_bg'], 
                        self.colors['operator_fg'], self.colors['hover_operator']
                    )
                    btn.grid(row=i, column=j, sticky='nsew', padx=5, pady=5)
                else:
                    # Number buttons
                    btn = self.create_button(
                        button_frame, text, self.colors['number_bg'], 
                        self.colors['number_fg'], self.colors['hover_number']
                    )
                    btn.grid(row=i, column=j, sticky='nsew', padx=5, pady=5)
                
                self.buttons[text] = btn
        
        # Configure grid weights
        for i in range(5):
            button_frame.grid_rowconfigure(i, weight=1)
        for j in range(4):
            button_frame.grid_columnconfigure(j, weight=1)
    
    def create_button(self, parent, text, bg, fg, hover_bg):
        """Create a styled button with hover effect"""
        btn = tk.Button(
            parent,
            text=text,
            font=self.button_font,
            bg=bg,
            fg=fg,
            activebackground=hover_bg,
            activeforeground=fg,
            relief=tk.FLAT,
            borderwidth=0,
            cursor='hand2',
            padx=10,
            pady=15
        )
        
        # Bind hover effects
        def on_enter(e):
            btn.config(bg=hover_bg)
        
        def on_leave(e):
            btn.config(bg=bg)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        # Bind click event
        btn.config(command=lambda t=text: self.button_click(t))
        
        return btn
    
    def button_click(self, text):
        """Handle button clicks"""
        if text in '0123456789':
            self.append_number(text)
        elif text == '.':
            self.append_decimal()
        elif text in ['+', '−', '×', '÷']:
            self.append_operator(text)
        elif text == '=':
            self.calculate()
        elif text == 'C':
            self.clear_all()
        elif text == 'CE':
            self.clear_entry()
        elif text == '⌫':
            self.delete_last()
    
    def append_number(self, number):
        """Append a number to current input"""
        if self.should_reset:
            self.current_input = "0"
            self.expression = ""
            self.should_reset = False
        
        if self.current_input == "0":
            self.current_input = number
        else:
            self.current_input += number
        
        self.update_display()
    
    def append_decimal(self):
        """Append decimal point"""
        if self.should_reset:
            self.current_input = "0"
            self.expression = ""
            self.should_reset = False
        
        if '.' not in self.current_input:
            self.current_input += '.'
        
        self.update_display()
    
    def append_operator(self, operator):
        """Append an operator"""
        if self.should_reset:
            self.should_reset = False
        
        # Map display operators to Python operators
        op_map = {'+': '+', '−': '-', '×': '*', '÷': '/'}
        
        if self.expression and self.expression[-1] not in ['+', '-', '*', '/']:
            self.expression += ' ' + self.current_input + ' ' + op_map[operator]
            self.current_input = "0"
        elif self.expression and self.expression[-1] in ['+', '-', '*', '/']:
            self.expression = self.expression[:-1] + op_map[operator]
        else:
            self.expression = self.current_input + ' ' + op_map[operator]
            self.current_input = "0"
        
        self.update_display()
    
    def calculate(self):
        """Perform calculation"""
        if not self.expression:
            return
        
        try:
            calculation = self.expression + ' ' + self.current_input
            result = eval(calculation)
            
            # Check for valid result
            if isinstance(result, (int, float)) and (result != float('inf') and result != float('-inf')):
                # Round to avoid floating point errors
                result = round(result, 10)
                
                # Format result
                if result == int(result):
                    self.current_input = str(int(result))
                else:
                    self.current_input = str(result)
                
                self.expression = ""
                self.should_reset = True
                self.update_display()
            else:
                raise ValueError("Invalid result")
        except:
            self.current_input = "Error"
            self.expression = ""
            self.should_reset = True
            self.update_display()
            self.root.after(2000, self.clear_all)
    
    def clear_all(self):
        """Clear everything"""
        self.current_input = "0"
        self.expression = ""
        self.should_reset = False
        self.update_display()
    
    def clear_entry(self):
        """Clear current entry"""
        self.current_input = "0"
        self.update_display()
    
    def delete_last(self):
        """Delete last character"""
        if self.should_reset:
            self.clear_all()
            return
        
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        
        self.update_display()
    
    def update_display(self):
        """Update the display labels"""
        self.result_label.config(text=self.current_input)
        
        # Format expression for display
        display_expr = self.expression.replace('+', '+').replace('-', '−').replace('*', '×').replace('/', '÷')
        self.expression_label.config(text=display_expr)
    
    def setup_keyboard(self):
        """Setup keyboard bindings"""
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
    
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.char
        
        if key in '0123456789':
            self.append_number(key)
        elif key == '.':
            self.append_decimal()
        elif key == '+':
            self.append_operator('+')
        elif key == '-':
            self.append_operator('−')
        elif key == '*':
            self.append_operator('×')
        elif key == '/':
            self.append_operator('÷')
        elif key == '\r' or key == '=':
            self.calculate()
        elif event.keysym == 'Escape':
            self.clear_all()
        elif event.keysym == 'BackSpace':
            self.delete_last()
        elif event.keysym == 'Delete':
            self.clear_entry()

def main():
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
