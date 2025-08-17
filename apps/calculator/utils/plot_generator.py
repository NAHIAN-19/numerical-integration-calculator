"""
Plot generation utilities for visualization
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Any
import io
import base64


class PlotGenerator:
    """Generate plots for numerical integration visualization"""
    
    def __init__(self, x_values: List[float], y_values: List[float]):
        self.x_values = np.array(x_values)
        self.y_values = np.array(y_values)
    
    def create_integration_plot(self, method: str, result_data: Dict[str, Any]) -> str:
        """Create a plot showing the integration method visualization"""
        plt.figure(figsize=(12, 8))
        
        # Create smooth curve for visualization
        x_smooth = np.linspace(self.x_values[0], self.x_values[-1], 1000)
        y_smooth = np.interp(x_smooth, self.x_values, self.y_values)
        
        # Plot the smooth curve
        plt.plot(x_smooth, y_smooth, 'b-', linewidth=2, label='f(x)', alpha=0.7)
        
        # Plot original data points
        plt.plot(self.x_values, self.y_values, 'ro', markersize=8, label='Data Points', zorder=5)
        
        # Add method-specific visualization
        if method == 'trapezoidal':
            self._add_trapezoidal_visualization()
        elif method == 'simpson_1_3':
            self._add_simpson_1_3_visualization()
        elif method == 'simpson_3_8':
            self._add_simpson_3_8_visualization()
        
        # Formatting
        plt.xlabel('X', fontsize=12)
        plt.ylabel('Y', fontsize=12)
        plt.title(f'Numerical Integration - {result_data.get("method_name", method)}', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        # Add result text
        result_text = f'Result: {result_data["result"]:.6f}'
        if result_data.get('error_estimate'):
            result_text += f'\nError Estimate: ±{abs(result_data["error_estimate"]):.6f}'
        
        plt.text(0.02, 0.98, result_text, transform=plt.gca().transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        plt.tight_layout()
        
        # Convert to base64 string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plot_data = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return base64.b64encode(plot_data).decode()
    
    def _add_trapezoidal_visualization(self):
        """Add trapezoidal rule visualization"""
        for i in range(len(self.x_values) - 1):
            x_trap = [self.x_values[i], self.x_values[i], self.x_values[i+1], self.x_values[i+1]]
            y_trap = [0, self.y_values[i], self.y_values[i+1], 0]
            plt.fill(x_trap, y_trap, alpha=0.3, color='green', edgecolor='darkgreen')
    
    def _add_simpson_1_3_visualization(self):
        """Add Simpson's 1/3 rule visualization"""
        # For Simpson's 1/3, show parabolic segments
        for i in range(0, len(self.x_values) - 1, 2):
            if i + 2 < len(self.x_values):
                x_seg = self.x_values[i:i+3]
                y_seg = self.y_values[i:i+3]
                
                # Create parabolic interpolation
                x_para = np.linspace(x_seg[0], x_seg[2], 100)
                # Fit parabola through 3 points
                coeffs = np.polyfit(x_seg, y_seg, 2)
                y_para = np.polyval(coeffs, x_para)
                
                # Fill area under parabola
                plt.fill_between(x_para, 0, y_para, alpha=0.3, color='orange', edgecolor='darkorange')
    
    def _add_simpson_3_8_visualization(self):
        """Add Simpson's 3/8 rule visualization"""
        # For Simpson's 3/8, show cubic segments
        for i in range(0, len(self.x_values) - 1, 3):
            if i + 3 < len(self.x_values):
                x_seg = self.x_values[i:i+4]
                y_seg = self.y_values[i:i+4]
                
                # Create cubic interpolation
                x_cubic = np.linspace(x_seg[0], x_seg[3], 100)
                # Fit cubic through 4 points
                coeffs = np.polyfit(x_seg, y_seg, 3)
                y_cubic = np.polyval(coeffs, x_cubic)
                
                # Fill area under cubic
                plt.fill_between(x_cubic, 0, y_cubic, alpha=0.3, color='purple', edgecolor='darkviolet')
    
    def create_comparison_plot(self, comparison_results: Dict[str, Any]) -> str:
        """Create a comparison plot showing all methods"""
        plt.figure(figsize=(15, 10))
        
        # Create smooth curve
        x_smooth = np.linspace(self.x_values[0], self.x_values[-1], 1000)
        y_smooth = np.interp(x_smooth, self.x_values, self.y_values)
        
        # Plot original function
        plt.plot(x_smooth, y_smooth, 'b-', linewidth=3, label='f(x)', alpha=0.8)
        plt.plot(self.x_values, self.y_values, 'ko', markersize=10, label='Data Points', zorder=5)
        
        # Add visualizations for each method
        colors = {'trapezoidal': 'green', 'simpson_1_3': 'orange', 'simpson_3_8': 'purple'}
        alphas = {'trapezoidal': 0.2, 'simpson_1_3': 0.3, 'simpson_3_8': 0.25}
        
        for method, result in comparison_results.items():
            if 'error' not in result:
                if method == 'trapezoidal':
                    for i in range(len(self.x_values) - 1):
                        x_trap = [self.x_values[i], self.x_values[i], self.x_values[i+1], self.x_values[i+1]]
                        y_trap = [0, self.y_values[i], self.y_values[i+1], 0]
                        plt.fill(x_trap, y_trap, alpha=alphas[method], color=colors[method], 
                                edgecolor=colors[method], linewidth=1)
        
        # Formatting
        plt.xlabel('X', fontsize=14)
        plt.ylabel('Y', fontsize=14)
        plt.title('Numerical Integration Methods Comparison', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        # Create results text
        results_text = "Results:\n"
        for method, result in comparison_results.items():
            if 'error' not in result:
                method_name = result.get('method_name', method)
                results_text += f"{method_name}: {result['result']:.6f}\n"
                if result.get('error_estimate'):
                    results_text += f"  Error: ±{abs(result['error_estimate']):.6f}\n"
            else:
                results_text += f"{method}: Error - {result['error']}\n"
        
        plt.text(0.02, 0.98, results_text, transform=plt.gca().transAxes, 
                verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
                fontsize=10)
        
        plt.legend(loc='upper right')
        plt.tight_layout()
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        plot_data = buffer.getvalue()
        buffer.close()
        plt.close()
        
        return base64.b64encode(plot_data).decode()