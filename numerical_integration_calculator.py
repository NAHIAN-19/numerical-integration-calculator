import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp
from sympy import symbols, sin, cos, log, exp, pi
import os
import json
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class NumericalIntegrationCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Numerical Integration Calculator")
        self.root.geometry("1400x1000")
        
        # Variables
        self.function_var = tk.StringVar(value="x**2")
        self.a_var = tk.StringVar(value="0")
        self.b_var = tk.StringVar(value="1")
        self.n_var = tk.StringVar(value="10")
        self.method_var = tk.StringVar(value="Trapezoidal")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Parameters", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Function input
        ttk.Label(input_frame, text="Function f(x):").grid(row=0, column=0, sticky=tk.W, pady=5)
        function_entry = ttk.Entry(input_frame, textvariable=self.function_var, width=40)
        function_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        ttk.Label(input_frame, text="Examples: x**2, sin(x), cos(x), exp(x), log(x), pi*x").grid(row=1, column=1, columnspan=2, sticky=tk.W)
        
        # Limits input
        ttk.Label(input_frame, text="Lower limit (a):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.a_var, width=15).grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(input_frame, text="Upper limit (b):").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.b_var, width=15).grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Number of intervals
        ttk.Label(input_frame, text="Number of intervals (n):").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(input_frame, textvariable=self.n_var, width=15).grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Method selection
        ttk.Label(input_frame, text="Integration Method:").grid(row=5, column=0, sticky=tk.W, pady=5)
        method_combo = ttk.Combobox(input_frame, textvariable=self.method_var, 
                                   values=["Trapezoidal", "Simpson's 1/3", "Simpson's 3/8"], 
                                   state="readonly", width=15)
        method_combo.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Calculate and Compare buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=6, column=0, columnspan=3, pady=10)
        
        calculate_btn = ttk.Button(button_frame, text="Calculate Integration", command=self.calculate_integration)
        calculate_btn.grid(row=0, column=0, padx=5)
        
        compare_btn = ttk.Button(button_frame, text="Compare All Methods", command=self.compare_methods)
        compare_btn.grid(row=0, column=1, padx=5)
        
        # File operations buttons
        file_frame = ttk.Frame(input_frame)
        file_frame.grid(row=7, column=0, columnspan=3, pady=5)
        
        load_btn = ttk.Button(file_frame, text="Load from JSON", command=self.load_from_json)
        load_btn.grid(row=0, column=0, padx=5)
        
        save_btn = ttk.Button(file_frame, text="Save to JSON", command=self.save_to_json)
        save_btn.grid(row=0, column=1, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Text widget for results with larger dynamic sizing
        self.results_text = tk.Text(results_frame, height=25, width=120, wrap=tk.NONE, 
                                   font=("Consolas", 10), bg="white", fg="black")
        v_scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=self.results_text.xview)
        self.results_text.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Configure grid weights for dynamic sizing
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Export buttons
        export_frame = ttk.Frame(results_frame)
        export_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(export_frame, text="Export Results to PDF", command=self.export_pdf).grid(row=0, column=0, padx=5)
        ttk.Button(export_frame, text="Export Plot to PNG", command=self.export_png).grid(row=0, column=1, padx=5)
        ttk.Button(export_frame, text="Export Comparison to PDF", command=self.export_comparison_pdf).grid(row=0, column=2, padx=5)
        ttk.Button(export_frame, text="Export Comparison Graph", command=self.export_comparison_graph).grid(row=0, column=3, padx=5)
        
        # Plot section
        plot_frame = ttk.LabelFrame(main_frame, text="Plot", padding="10")
        plot_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        plot_frame.columnconfigure(0, weight=1)
        plot_frame.rowconfigure(0, weight=1)
        
    def parse_function(self, func_str):
        """Parse function string and return a callable function"""
        x = symbols('x')
        try:
            # Create a local namespace with mathematical functions
            local_dict = {
                'sin': sp.sin,
                'cos': sp.cos,
                'log': sp.log,
                'exp': sp.exp,
                'pi': sp.pi,
                'x': x
            }
            
            # Create the expression using the local dictionary
            expr = sp.sympify(func_str, locals=local_dict)
            return sp.lambdify(x, expr, modules=['numpy'])
        except Exception as e:
            raise ValueError(f"Invalid function: {e}")
    
    def parse_limits(self, a_str, b_str):
        """Parse limit strings and return numerical values"""
        try:
            # Create a local namespace with mathematical constants
            local_dict = {
                'pi': sp.pi,
                'e': sp.E
            }
            
            a = float(sp.sympify(a_str, locals=local_dict))
            b = float(sp.sympify(b_str, locals=local_dict))
            return a, b
        except Exception as e:
            raise ValueError(f"Invalid limits: {e}")
    
    def trapezoidal_rule(self, f, a, b, n):
        """Trapezoidal rule implementation"""
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = f(x)
        
        result = h * (0.5 * y[0] + 0.5 * y[-1] + np.sum(y[1:-1]))
        
        # Process details
        process = f"Trapezoidal Rule:\n"
        process += f"h = (b-a)/n = ({b}-{a})/{n} = {h:.6f}\n"
        process += f"x values: {x}\n"
        process += f"y values: {y}\n"
        process += f"Result = h * (y₀/2 + y₁ + y₂ + ... + yₙ₋₁ + yₙ/2)\n"
        process += f"Result = {h:.6f} * ({0.5*y[0]:.6f} + {np.sum(y[1:-1]):.6f} + {0.5*y[-1]:.6f})\n"
        process += f"Result = {result:.6f}\n"
        
        return result, process, x, y
    
    def simpson_one_third(self, f, a, b, n):
        """Simpson's 1/3 rule implementation"""
        if n % 2 != 0:
            n += 1  # Ensure n is even
        
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = f(x)
        
        result = h/3 * (y[0] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-1:2]) + y[-1])
        
        # Process details
        process = f"Simpson's 1/3 Rule:\n"
        process += f"h = (b-a)/n = ({b}-{a})/{n} = {h:.6f}\n"
        process += f"x values: {x}\n"
        process += f"y values: {y}\n"
        process += f"Result = h/3 * (y₀ + 4(y₁ + y₃ + ...) + 2(y₂ + y₄ + ...) + yₙ)\n"
        process += f"Result = {h/3:.6f} * ({y[0]:.6f} + 4*{np.sum(y[1:-1:2]):.6f} + 2*{np.sum(y[2:-1:2]):.6f} + {y[-1]:.6f})\n"
        process += f"Result = {result:.6f}\n"
        
        return result, process, x, y
    
    def simpson_three_eighth(self, f, a, b, n):
        """Simpson's 3/8 rule implementation"""
        if n % 3 != 0:
            n = ((n // 3) + 1) * 3  # Ensure n is divisible by 3
        
        h = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y = f(x)
        
        result = 3*h/8 * (y[0] + 3*np.sum(y[1:-1:3]) + 3*np.sum(y[2:-1:3]) + 2*np.sum(y[3:-1:3]) + y[-1])
        
        # Process details
        process = f"Simpson's 3/8 Rule:\n"
        process += f"h = (b-a)/n = ({b}-{a})/{n} = {h:.6f}\n"
        process += f"x values: {x}\n"
        process += f"y values: {y}\n"
        process += f"Result = 3h/8 * (y₀ + 3(y₁ + y₄ + ...) + 3(y₂ + y₅ + ...) + 2(y₃ + y₆ + ...) + yₙ)\n"
        process += f"Result = {3*h/8:.6f} * ({y[0]:.6f} + 3*{np.sum(y[1:-1:3]):.6f} + 3*{np.sum(y[2:-1:3]):.6f} + 2*{np.sum(y[3:-1:3]):.6f} + {y[-1]:.6f})\n"
        process += f"Result = {result:.6f}\n"
        
        return result, process, x, y
    
    def calculate_integration(self):
        """Calculate integration based on selected method"""
        try:
            # Get input values
            func_str = self.function_var.get()
            a_str = self.a_var.get()
            b_str = self.b_var.get()
            n_str = self.n_var.get()
            method = self.method_var.get()
            
            # Parse inputs
            f = self.parse_function(func_str)
            a, b = self.parse_limits(a_str, b_str)
            n = int(n_str)
            
            if n <= 0:
                raise ValueError("Number of intervals must be positive")
            
            # Calculate based on method
            if method == "Trapezoidal":
                result, process, x, y = self.trapezoidal_rule(f, a, b, n)
            elif method == "Simpson's 1/3":
                result, process, x, y = self.simpson_one_third(f, a, b, n)
            elif method == "Simpson's 3/8":
                result, process, x, y = self.simpson_three_eighth(f, a, b, n)
            else:
                raise ValueError("Invalid method selected")
            
            # Calculate exact value for error analysis
            exact_result = self.calculate_exact_value(f, a, b)
            error_analysis = self.calculate_error_analysis(result, exact_result)
            
            # Display results
            self.results_text.delete(1.0, tk.END)
            output = f"╔══════════════════════════════════════════════════════════════════════════════╗\n"
            output += f"║                           INTEGRATION RESULTS                              ║\n"
            output += f"╚══════════════════════════════════════════════════════════════════════════════╝\n\n"
            output += f"Function: f(x) = {func_str}\n"
            output += f"Limits: a = {a}, b = {b}\n"
            output += f"Number of intervals: n = {n}\n"
            output += f"Method: {method}\n\n"
            output += f"╔══════════════════════════════════════════════════════════════════════════════╗\n"
            output += f"║                              CALCULATION PROCESS                           ║\n"
            output += f"╚══════════════════════════════════════════════════════════════════════════════╝\n"
            output += process
            output += f"\n╔══════════════════════════════════════════════════════════════════════════════╗\n"
            output += f"║                                 FINAL RESULT                                ║\n"
            output += f"╚══════════════════════════════════════════════════════════════════════════════╝\n"
            output += f"∫f(x)dx from {a} to {b} ≈ {result:.6f}"
            
            if exact_result is not None:
                output += f"\nExact Value: {exact_result:.8f}"
            
            output += f"\n\nERROR ANALYSIS:\n{error_analysis}"
            
            self.results_text.insert(tk.END, output)
            
            # Plot the function
            self.plot_function(f, a, b, x, y, method, result)
            
        except Exception as e:
            messagebox.showerror("Error", f"Calculation failed: {str(e)}")
    
    def calculate_exact_value(self, f, a, b):
        """Calculate exact value using sympy integration"""
        try:
            x = symbols('x')
            # Create a local namespace with mathematical functions
            local_dict = {
                'sin': sp.sin,
                'cos': sp.cos,
                'log': sp.log,
                'exp': sp.exp,
                'pi': sp.pi,
                'x': x
            }
            
            # Get the function string and create expression
            func_str = self.function_var.get()
            expr = sp.sympify(func_str, locals=local_dict)
            
            # Integrate symbolically
            exact_integral = sp.integrate(expr, (x, a, b))
            return float(exact_integral)
        except Exception as e:
            return None  # Return None if exact integration fails
    
    def calculate_error_analysis(self, numerical_result, exact_result):
        """Calculate error analysis"""
        if exact_result is None:
            return "Exact value could not be calculated"
        
        absolute_error = abs(numerical_result - exact_result)
        relative_error = (absolute_error / abs(exact_result)) * 100 if exact_result != 0 else float('inf')
        
        return f"Absolute Error: {absolute_error:.8f}\nRelative Error: {relative_error:.4f}%"
    
    def compare_methods(self):
        """Compare all three integration methods"""
        try:
            # Get input values
            func_str = self.function_var.get()
            a_str = self.a_var.get()
            b_str = self.b_var.get()
            n_str = self.n_var.get()
            
            # Parse inputs
            f = self.parse_function(func_str)
            a, b = self.parse_limits(a_str, b_str)
            n = int(n_str)
            
            if n <= 0:
                raise ValueError("Number of intervals must be positive")
            
            # Calculate exact value for error analysis
            exact_result = self.calculate_exact_value(f, a, b)
            
            # Results storage
            results = {}
            
            # Test Trapezoidal Rule
            try:
                result, process, x, y = self.trapezoidal_rule(f, a, b, n)
                error_analysis = self.calculate_error_analysis(result, exact_result)
                results["Trapezoidal"] = {
                    "result": result,
                    "process": process,
                    "error": error_analysis,
                    "exact": exact_result
                }
            except Exception as e:
                results["Trapezoidal"] = {"error": f"Failed: {str(e)}"}
            
            # Test Simpson's 1/3 Rule
            try:
                n_13 = n if n % 2 == 0 else n + 1
                result, process, x, y = self.simpson_one_third(f, a, b, n_13)
                error_analysis = self.calculate_error_analysis(result, exact_result)
                results["Simpson's 1/3"] = {
                    "result": result,
                    "process": process,
                    "error": error_analysis,
                    "exact": exact_result
                }
            except Exception as e:
                results["Simpson's 1/3"] = {"error": f"Failed: {str(e)}"}
            
            # Test Simpson's 3/8 Rule
            try:
                n_38 = n if n % 3 == 0 else ((n // 3) + 1) * 3
                result, process, x, y = self.simpson_three_eighth(f, a, b, n_38)
                error_analysis = self.calculate_error_analysis(result, exact_result)
                results["Simpson's 3/8"] = {
                    "result": result,
                    "process": process,
                    "error": error_analysis,
                    "exact": exact_result
                }
            except Exception as e:
                results["Simpson's 3/8"] = {"error": f"Failed: {str(e)}"}
            
            # Display comparison results
            self.display_comparison_results(results, f, a, b, n)
            
            # Plot comparison graph
            self.plot_comparison_graph(f, a, b, results)
            
        except Exception as e:
            messagebox.showerror("Error", f"Comparison failed: {str(e)}")
    
    def display_comparison_results(self, results, f, a, b, n):
        """Display comparison results in the text widget"""
        self.results_text.delete(1.0, tk.END)
        
        output = f"╔══════════════════════════════════════════════════════════════════════════════╗\n"
        output += f"║                        METHOD COMPARISON RESULTS                            ║\n"
        output += f"╚══════════════════════════════════════════════════════════════════════════════╝\n\n"
        output += f"Function: f(x) = {self.function_var.get()}\n"
        output += f"Limits: a = {a}, b = {b}\n"
        output += f"Number of intervals: n = {n}\n\n"
        
        # Summary table
        output += "╔══════════════════════════════════════════════════════════════════════════════╗\n"
        output += f"║                                SUMMARY TABLE                                 ║\n"
        output += f"╚══════════════════════════════════════════════════════════════════════════════╝\n"
        output += f"{'Method':<20} {'Result':<20} {'Status':<15}\n"
        output += "─" * 55 + "\n"
        
        for method, data in results.items():
            if "error" in data and "Failed" in str(data["error"]):
                output += f"{method:<20} {'N/A':<20} {'Failed':<15}\n"
            else:
                output += f"{method:<20} {data['result']:<20.6f} {'Success':<15}\n"
        
        output += "\n╔══════════════════════════════════════════════════════════════════════════════╗\n"
        output += f"║                              DETAILED RESULTS                                ║\n"
        output += f"╚══════════════════════════════════════════════════════════════════════════════╝\n\n"
        
        # Detailed results for each method
        for method, data in results.items():
            output += f"╔══════════════════════════════════════════════════════════════════════════════╗\n"
            output += f"║                            {method.upper()} METHOD                              ║\n"
            output += f"╚══════════════════════════════════════════════════════════════════════════════╝\n"
            
            if "error" in data and "Failed" in str(data["error"]):
                output += f"Status: {data['error']}\n\n"
            else:
                output += f"Result: {data['result']:.8f}\n"
                if data['exact'] is not None:
                    output += f"Exact Value: {data['exact']:.8f}\n"
                output += f"Error Analysis:\n{data['error']}\n"
                output += f"Process:\n{data['process']}\n"
            
            output += "\n"
        
        # Best method analysis
        valid_results = {k: v for k, v in results.items() 
                        if "error" not in v or "Failed" not in str(v.get("error", ""))}
        
        if valid_results:
            best_method = min(valid_results.keys(), 
                            key=lambda x: abs(valid_results[x]["result"] - valid_results[x]["exact"]) 
                            if valid_results[x]["exact"] is not None else float('inf'))
            
            output += "\n╔══════════════════════════════════════════════════════════════════════════════╗\n"
            output += f"║                            BEST METHOD ANALYSIS                           ║\n"
            output += f"╚══════════════════════════════════════════════════════════════════════════════╝\n"
            output += f"Most Accurate: {best_method}\n"
            if valid_results[best_method]["exact"] is not None:
                error = abs(valid_results[best_method]["result"] - valid_results[best_method]["exact"])
                output += f"Error: {error:.8f}\n"
        
        self.results_text.insert(tk.END, output)
        
        # Store results for export
        self.comparison_results = results
    
    def plot_function(self, f, a, b, x_points, y_points, method, result):
        """Plot the function and integration points"""
        self.ax.clear()
        
        # Generate smooth curve for plotting
        x_smooth = np.linspace(a, b, 1000)
        y_smooth = f(x_smooth)
        
        # Plot the function
        self.ax.plot(x_smooth, y_smooth, 'b-', linewidth=2, label='f(x)')
        
        # Plot integration points
        self.ax.plot(x_points, y_points, 'ro', markersize=6, label='Integration points')
        
        # Fill area under curve
        self.ax.fill_between(x_smooth, y_smooth, alpha=0.3, color='blue')
        
        # Add grid and labels
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.set_title(f'{method} Integration\nResult: {result:.6f}')
        self.ax.legend()
        
        # Update canvas
        self.canvas.draw()
    
    def plot_comparison_graph(self, f, a, b, results):
        """Plot comparison graph showing all methods"""
        self.ax.clear()
        
        # Generate smooth curve for plotting
        x_smooth = np.linspace(a, b, 1000)
        y_smooth = f(x_smooth)
        
        # Plot the function
        self.ax.plot(x_smooth, y_smooth, 'b-', linewidth=2, label='f(x)')
        
        # Colors for different methods
        colors = ['red', 'green', 'orange']
        markers = ['o', 's', '^']
        
        # Plot integration points for each method
        for i, (method, data) in enumerate(results.items()):
            if "error" not in data or "Failed" not in str(data.get("error", "")):
                # Get x and y points from the process string
                try:
                    # Extract x and y values from the process
                    process_lines = data['process'].split('\n')
                    for line in process_lines:
                        if 'x values:' in line:
                            x_str = line.split('x values:')[1].strip()
                            x_points = np.array(eval(x_str))
                        elif 'y values:' in line:
                            y_str = line.split('y values:')[1].strip()
                            y_points = np.array(eval(y_str))
                            break
                    
                    # Plot points for this method
                    self.ax.plot(x_points, y_points, f'{colors[i]}{markers[i]}', 
                               markersize=8, label=f'{method} points')
                    
                except Exception as e:
                    print(f"Could not plot {method}: {e}")
        
        # Fill area under curve
        self.ax.fill_between(x_smooth, y_smooth, alpha=0.2, color='blue')
        
        # Add grid and labels
        self.ax.grid(True, alpha=0.3)
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('f(x)')
        self.ax.set_title(f'Method Comparison\nFunction: {self.function_var.get()}')
        self.ax.legend()
        
        # Update canvas
        self.canvas.draw()
    
    def export_pdf(self):
        """Export results to PDF"""
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Error", "PDF export requires reportlab library. Install it with: pip install reportlab")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if filename:
                # Get current results text
                results = self.results_text.get(1.0, tk.END)
                
                # Create a simple PDF report
                doc = SimpleDocTemplate(filename, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                
                # Add title
                title = Paragraph("Numerical Integration Results", styles['Title'])
                story.append(title)
                story.append(Spacer(1, 12))
                
                # Add results
                for line in results.split('\n'):
                    if line.strip():
                        p = Paragraph(line, styles['Normal'])
                        story.append(p)
                        story.append(Spacer(1, 6))
                
                doc.build(story)
                messagebox.showinfo("Success", f"Results exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PDF: {str(e)}")
    
    def export_png(self):
        """Export plot to PNG"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filename:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Plot exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export PNG: {str(e)}")
    
    def export_comparison_pdf(self):
        """Export comparison results to PDF"""
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Error", "PDF export requires reportlab library. Install it with: pip install reportlab")
            return
        
        if not hasattr(self, 'comparison_results'):
            messagebox.showwarning("Warning", "No comparison results to export. Run comparison first.")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pdf",
                filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            if filename:
                # Create PDF report
                doc = SimpleDocTemplate(filename, pagesize=letter)
                styles = getSampleStyleSheet()
                story = []
                
                # Add title
                title = Paragraph("Numerical Integration Method Comparison", styles['Title'])
                story.append(title)
                story.append(Spacer(1, 12))
                
                # Add summary
                summary = Paragraph("Method Comparison Results", styles['Heading2'])
                story.append(summary)
                story.append(Spacer(1, 6))
                
                # Add function and parameters
                params = f"Function: {self.function_var.get()}<br/>"
                params += f"Limits: a = {self.a_var.get()}, b = {self.b_var.get()}<br/>"
                params += f"Intervals: n = {self.n_var.get()}"
                story.append(Paragraph(params, styles['Normal']))
                story.append(Spacer(1, 12))
                
                # Add results table
                for method, data in self.comparison_results.items():
                    method_title = Paragraph(f"{method} Method", styles['Heading3'])
                    story.append(method_title)
                    story.append(Spacer(1, 6))
                    
                    if "error" in data and "Failed" in str(data["error"]):
                        story.append(Paragraph(f"Status: {data['error']}", styles['Normal']))
                    else:
                        result_text = f"Result: {data['result']:.8f}<br/>"
                        if data['exact'] is not None:
                            result_text += f"Exact Value: {data['exact']:.8f}<br/>"
                        result_text += f"Error Analysis: {data['error']}"
                        story.append(Paragraph(result_text, styles['Normal']))
                    
                    story.append(Spacer(1, 12))
                
                # Add best method analysis
                valid_results = {k: v for k, v in self.comparison_results.items() 
                               if "error" not in v or "Failed" not in str(v.get("error", ""))}
                
                if valid_results:
                    best_method = min(valid_results.keys(), 
                                   key=lambda x: abs(valid_results[x]["result"] - valid_results[x]["exact"]) 
                                   if valid_results[x]["exact"] is not None else float('inf'))
                    
                    best_analysis = Paragraph("Best Method Analysis", styles['Heading2'])
                    story.append(best_analysis)
                    story.append(Spacer(1, 6))
                    
                    best_text = f"Most Accurate: {best_method}<br/>"
                    if valid_results[best_method]["exact"] is not None:
                        error = abs(valid_results[best_method]["result"] - valid_results[best_method]["exact"])
                        best_text += f"Error: {error:.8f}"
                    story.append(Paragraph(best_text, styles['Normal']))
                
                doc.build(story)
                messagebox.showinfo("Success", f"Comparison exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export comparison PDF: {str(e)}")
    
    def save_to_json(self):
        """Save current parameters to JSON file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                data = {
                    "function": self.function_var.get(),
                    "lower_limit": self.a_var.get(),
                    "upper_limit": self.b_var.get(),
                    "intervals": self.n_var.get(),
                    "method": self.method_var.get()
                }
                
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=2)
                
                messagebox.showinfo("Success", f"Parameters saved to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save JSON: {str(e)}")
    
    def load_from_json(self):
        """Load parameters from JSON file"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                # Update UI with loaded data
                self.function_var.set(data.get("function", ""))
                self.a_var.set(data.get("lower_limit", ""))
                self.b_var.set(data.get("upper_limit", ""))
                self.n_var.set(data.get("intervals", ""))
                self.method_var.set(data.get("method", "Trapezoidal"))
                
                messagebox.showinfo("Success", f"Parameters loaded from {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON: {str(e)}")
    
    def export_comparison_graph(self):
        """Export comparison graph to PNG"""
        if not hasattr(self, 'comparison_results'):
            messagebox.showwarning("Warning", "No comparison results to export. Run comparison first.")
            return
            
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filename:
                # Create a new figure for export
                fig, ax = plt.subplots(figsize=(12, 8))
                
                # Get current function and limits
                f = self.parse_function(self.function_var.get())
                a, b = self.parse_limits(self.a_var.get(), self.b_var.get())
                
                # Generate smooth curve for plotting
                x_smooth = np.linspace(a, b, 1000)
                y_smooth = f(x_smooth)
                
                # Plot the function
                ax.plot(x_smooth, y_smooth, 'b-', linewidth=2, label='f(x)')
                
                # Colors for different methods
                colors = ['red', 'green', 'orange']
                markers = ['o', 's', '^']
                
                # Plot integration points for each method
                for i, (method, data) in enumerate(self.comparison_results.items()):
                    if "error" not in data or "Failed" not in str(data.get("error", "")):
                        try:
                            # Extract x and y values from the process
                            process_lines = data['process'].split('\n')
                            for line in process_lines:
                                if 'x values:' in line:
                                    x_str = line.split('x values:')[1].strip()
                                    x_points = np.array(eval(x_str))
                                elif 'y values:' in line:
                                    y_str = line.split('y values:')[1].strip()
                                    y_points = np.array(eval(y_str))
                                    break
                            
                            # Plot points for this method
                            ax.plot(x_points, y_points, f'{colors[i]}{markers[i]}', 
                                   markersize=8, label=f'{method} points')
                            
                        except Exception as e:
                            print(f"Could not plot {method}: {e}")
                
                # Fill area under curve
                ax.fill_between(x_smooth, y_smooth, alpha=0.2, color='blue')
                
                # Add grid and labels
                ax.grid(True, alpha=0.3)
                ax.set_xlabel('x')
                ax.set_ylabel('f(x)')
                ax.set_title(f'Method Comparison\nFunction: {self.function_var.get()}')
                ax.legend()
                
                # Save the figure
                fig.savefig(filename, dpi=300, bbox_inches='tight')
                plt.close(fig)
                
                messagebox.showinfo("Success", f"Comparison graph exported to {filename}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export comparison graph: {str(e)}")

def main():
    root = tk.Tk()
    app = NumericalIntegrationCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 