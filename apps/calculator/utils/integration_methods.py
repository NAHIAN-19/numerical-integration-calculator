"""
Numerical Integration Methods Implementation
"""
import numpy as np
from typing import List, Tuple, Dict, Any


class IntegrationCalculator:
    """Main calculator class for numerical integration methods"""
    
    def __init__(self, x_values: List[float], y_values: List[float]):
        self.x_values = np.array(x_values)
        self.y_values = np.array(y_values)
        self.n = len(x_values) - 1  # number of intervals
        self.validate_data()
    
    def validate_data(self):
        """Validate input data"""
        if len(self.x_values) != len(self.y_values):
            raise ValueError("X and Y values must have the same length")
        
        if len(self.x_values) < 2:
            raise ValueError("At least 2 data points are required")
        
        # Check if x values are sorted
        if not np.all(self.x_values[:-1] <= self.x_values[1:]):
            raise ValueError("X values must be in ascending order")
    
    def trapezoidal_rule(self) -> Dict[str, Any]:
        """
        Implement Trapezoidal Rule
        Formula: ∫f(x)dx ≈ (h/2)[f(x₀) + 2f(x₁) + 2f(x₂) + ... + 2f(xₙ₋₁) + f(xₙ)]
        """
        steps = []
        h_values = np.diff(self.x_values)
        
        # Check if intervals are equal
        if np.allclose(h_values, h_values[0]):
            # Equal intervals
            h = h_values[0]
            steps.append(f"Step 1: Calculate interval width h = {h:.6f}")
            
            # Calculate sum
            sum_middle = np.sum(self.y_values[1:-1])
            steps.append(f"Step 2: Sum of middle terms = 2 × ({' + '.join([f'{y:.6f}' for y in self.y_values[1:-1]])}) = {2 * sum_middle:.6f}")
            
            result = (h / 2) * (self.y_values[0] + 2 * sum_middle + self.y_values[-1])
            steps.append(f"Step 3: Apply formula: ({h:.6f}/2) × ({self.y_values[0]:.6f} + {2 * sum_middle:.6f} + {self.y_values[-1]:.6f}) = {result:.6f}")
            
        else:
            # Unequal intervals
            steps.append("Step 1: Using composite trapezoidal rule for unequal intervals")
            result = 0
            for i in range(self.n):
                h_i = self.x_values[i+1] - self.x_values[i]
                area_i = (h_i / 2) * (self.y_values[i] + self.y_values[i+1])
                result += area_i
                steps.append(f"Interval {i+1}: h_{i+1} = {h_i:.6f}, Area = ({h_i:.6f}/2) × ({self.y_values[i]:.6f} + {self.y_values[i+1]:.6f}) = {area_i:.6f}")
            
            steps.append(f"Total Area = {result:.6f}")
        
        # Error estimation (for equal intervals)
        error_estimate = None
        if len(self.x_values) > 2 and np.allclose(h_values, h_values[0]):
            # Simple error estimation using second differences
            second_diff = np.diff(self.y_values, 2)
            if len(second_diff) > 0:
                max_second_diff = np.max(np.abs(second_diff))
                h = h_values[0]
                error_estimate = -(h**3 / 12) * max_second_diff * self.n
                steps.append(f"Error Estimate: ≈ {error_estimate:.6f}")
        
        return {
            'result': result,
            'steps': steps,
            'error_estimate': error_estimate,
            'method_name': 'Trapezoidal Rule'
        }
    
    def simpson_1_3_rule(self) -> Dict[str, Any]:
        """
        Implement Simpson's 1/3 Rule with adaptive approach
        Uses Simpson's 1/3 on evenly spaced chunks and Trapezoidal on uneven chunks
        """
        steps = []
        
        h_values = np.diff(self.x_values)
        
        # Check if all intervals are equal
        if np.allclose(h_values, h_values[0]):
            # All intervals are equal - use standard approach
            h = h_values[0]
            steps.append(f"Step 1: All intervals are equal (h = {h:.6f})")
            
            if self.n % 2 == 0:
                steps.append(f"Step 2: Number of intervals n = {self.n} (even, using pure Simpson's 1/3)")
                
                # Calculate weighted sum
                weighted_sum = self.y_values[0] + self.y_values[-1]  # First and last terms
                steps.append(f"Step 3: First and last terms: {self.y_values[0]:.6f} + {self.y_values[-1]:.6f} = {weighted_sum:.6f}")
                
                # Odd-indexed terms (coefficient 4)
                odd_sum = np.sum(self.y_values[1::2])
                weighted_sum += 4 * odd_sum
                steps.append(f"Step 4: Odd-indexed terms × 4: 4 × ({' + '.join([f'{y:.6f}' for y in self.y_values[1::2]])}) = {4 * odd_sum:.6f}")
                
                # Even-indexed terms (coefficient 2)
                if len(self.y_values[2:-1:2]) > 0:
                    even_sum = np.sum(self.y_values[2:-1:2])
                    weighted_sum += 2 * even_sum
                    steps.append(f"Step 5: Even-indexed terms × 2: 2 × ({' + '.join([f'{y:.6f}' for y in self.y_values[2:-1:2]])}) = {2 * even_sum:.6f}")
                
                result = (h / 3) * weighted_sum
                steps.append(f"Step 6: Apply formula: ({h:.6f}/3) × {weighted_sum:.6f} = {result:.6f}")
                
            else:
                # Odd number of intervals - use hybrid
                steps.append(f"Step 2: Number of intervals n = {self.n} (odd, using hybrid approach)")
                
                simpson_intervals = self.n - 1
                trapezoidal_intervals = 1
                
                steps.append(f"Step 3: Using {simpson_intervals} intervals for Simpson's 1/3 + {trapezoidal_intervals} interval for Trapezoidal")
                
                # Simpson's 1/3 part
                simpson_y = self.y_values[:-1]
                simpson_weighted_sum = simpson_y[0] + simpson_y[-1]
                simpson_odd_sum = np.sum(simpson_y[1::2])
                simpson_weighted_sum += 4 * simpson_odd_sum
                
                if len(simpson_y[2:-1:2]) > 0:
                    simpson_even_sum = np.sum(simpson_y[2:-1:2])
                    simpson_weighted_sum += 2 * simpson_even_sum
                
                simpson_result = (h / 3) * simpson_weighted_sum
                steps.append(f"Step 4: Simpson's 1/3 part: ({h:.6f}/3) × {simpson_weighted_sum:.6f} = {simpson_result:.6f}")
                
                # Trapezoidal part
                trapezoidal_result = (h / 2) * (self.y_values[-2] + self.y_values[-1])
                steps.append(f"Step 5: Trapezoidal part: ({h:.6f}/2) × ({self.y_values[-2]:.6f} + {self.y_values[-1]:.6f}) = {trapezoidal_result:.6f}")
                
                result = simpson_result + trapezoidal_result
                steps.append(f"Step 6: Total result = {simpson_result:.6f} + {trapezoidal_result:.6f} = {result:.6f}")
        
        else:
            # Unequal intervals - use adaptive approach
            steps.append("Step 1: Intervals are unequal - using adaptive approach")
            steps.append("Step 2: Identifying evenly spaced chunks for Simpson's 1/3 rule")
            
            result = 0
            i = 0
            
            while i < self.n:
                # Find the next chunk of equal intervals
                chunk_start = i
                chunk_h = h_values[i]
                
                # Find how many consecutive intervals have the same width
                j = i + 1
                while j < self.n and np.isclose(h_values[j], chunk_h, atol=1e-10):
                    j += 1
                
                chunk_end = j
                chunk_intervals = chunk_end - chunk_start
                chunk_points = chunk_intervals + 1
                
                steps.append(f"Step 3.{chunk_start+1}: Found evenly spaced chunk from point {chunk_start} to {chunk_end} (h = {chunk_h:.6f})")
                
                if chunk_intervals >= 2 and chunk_intervals % 2 == 0:
                    # Use Simpson's 1/3 rule on this chunk (even number of intervals)
                    chunk_y = self.y_values[chunk_start:chunk_end+1]
                    
                    weighted_sum = chunk_y[0] + chunk_y[-1]
                    odd_sum = np.sum(chunk_y[1::2])
                    weighted_sum += 4 * odd_sum
                    
                    if len(chunk_y[2:-1:2]) > 0:
                        even_sum = np.sum(chunk_y[2:-1:2])
                        weighted_sum += 2 * even_sum
                    
                    chunk_result = (chunk_h / 3) * weighted_sum
                    result += chunk_result
                    
                    steps.append(f"Step 4.{chunk_start+1}: Simpson's 1/3 on chunk: ({chunk_h:.6f}/3) × {weighted_sum:.6f} = {chunk_result:.6f}")
                    
                elif chunk_intervals >= 1:
                    # Use Trapezoidal rule on this chunk
                    chunk_result = 0
                    for k in range(chunk_start, chunk_end):
                        area_k = (h_values[k] / 2) * (self.y_values[k] + self.y_values[k+1])
                        chunk_result += area_k
                        steps.append(f"Step 4.{chunk_start+1}.{k-chunk_start+1}: Trapezoidal interval {k+1}: ({h_values[k]:.6f}/2) × ({self.y_values[k]:.6f} + {self.y_values[k+1]:.6f}) = {area_k:.6f}")
                    
                    result += chunk_result
                    steps.append(f"Step 5.{chunk_start+1}: Trapezoidal on chunk: {chunk_result:.6f}")
                
                i = chunk_end
            
            steps.append(f"Step 6: Total result = {result:.6f}")
        
        # Error estimation
        error_estimate = None
        if len(self.x_values) > 4:
            # Simple error estimation
            if np.allclose(h_values, h_values[0]):
                h = h_values[0]
                fourth_diff = np.diff(self.y_values, 4)
                if len(fourth_diff) > 0:
                    max_fourth_diff = np.max(np.abs(fourth_diff))
                    error_estimate = -(h**5 / 90) * max_fourth_diff * (self.x_values[-1] - self.x_values[0])
                    steps.append(f"Error Estimate: ≈ {error_estimate:.6f}")
        
        method_name = "Simpson's 1/3 Rule (Adaptive)" if not np.allclose(h_values, h_values[0]) else ("Simpson's 1/3 Rule" if self.n % 2 == 0 else "Simpson's 1/3 + Trapezoidal (Hybrid)")
        
        return {
            'result': result,
            'steps': steps,
            'error_estimate': error_estimate,
            'method_name': method_name
        }
    
    def simpson_3_8_rule(self) -> Dict[str, Any]:
        """
        Implement Simpson's 3/8 Rule with adaptive approach
        Uses Simpson's 3/8 on evenly spaced chunks and Trapezoidal on uneven chunks
        """
        steps = []
        
        h_values = np.diff(self.x_values)
        
        # Check if all intervals are equal
        if np.allclose(h_values, h_values[0]):
            # All intervals are equal - use standard approach
            h = h_values[0]
            steps.append(f"Step 1: All intervals are equal (h = {h:.6f})")
            
            if self.n % 3 == 0:
                steps.append(f"Step 2: Number of intervals n = {self.n} (multiple of 3, using pure Simpson's 3/8)")
                
                # Calculate weighted sum
                weighted_sum = self.y_values[0] + self.y_values[-1]  # First and last terms
                steps.append(f"Step 3: First and last terms: {self.y_values[0]:.6f} + {self.y_values[-1]:.6f} = {weighted_sum:.6f}")
                
                # Process in groups of 3 intervals
                for i in range(0, self.n, 3):
                    if i + 3 <= self.n:
                        # Terms with coefficient 3
                        if i + 1 < len(self.y_values):
                            weighted_sum += 3 * self.y_values[i + 1]
                        if i + 2 < len(self.y_values):
                            weighted_sum += 3 * self.y_values[i + 2]
                        
                        # Term with coefficient 2 (except for the last group)
                        if i + 3 < len(self.y_values) - 1:
                            weighted_sum += 2 * self.y_values[i + 3]
                
                # Detailed step breakdown
                coefficient_3_terms = []
                coefficient_2_terms = []
                
                for i in range(1, len(self.y_values) - 1):
                    pos_in_group = i % 3
                    if pos_in_group == 1 or pos_in_group == 2:
                        coefficient_3_terms.append(self.y_values[i])
                    elif pos_in_group == 0 and i < len(self.y_values) - 1:
                        coefficient_2_terms.append(self.y_values[i])
                
                if coefficient_3_terms:
                    steps.append(f"Step 4: Terms × 3: 3 × ({' + '.join([f'{y:.6f}' for y in coefficient_3_terms])}) = {3 * sum(coefficient_3_terms):.6f}")
                
                if coefficient_2_terms:
                    steps.append(f"Step 5: Terms × 2: 2 × ({' + '.join([f'{y:.6f}' for y in coefficient_2_terms])}) = {2 * sum(coefficient_2_terms):.6f}")
                
                result = (3 * h / 8) * weighted_sum
                steps.append(f"Step 6: Apply formula: (3 × {h:.6f}/8) × {weighted_sum:.6f} = {result:.6f}")
                
            else:
                # Not multiple of 3 - use hybrid
                steps.append(f"Step 2: Number of intervals n = {self.n} (not multiple of 3, using hybrid approach)")
                
                simpson_intervals = (self.n // 3) * 3
                trapezoidal_intervals = self.n - simpson_intervals
                
                steps.append(f"Step 3: Using {simpson_intervals} intervals for Simpson's 3/8 + {trapezoidal_intervals} intervals for Trapezoidal")
                
                # Simpson's 3/8 part
                simpson_y = self.y_values[:simpson_intervals + 1]
                
                if simpson_intervals > 0:
                    simpson_weighted_sum = simpson_y[0] + simpson_y[-1]
                    
                    # Process Simpson's 3/8 part
                    for i in range(0, simpson_intervals, 3):
                        if i + 1 < len(simpson_y):
                            simpson_weighted_sum += 3 * simpson_y[i + 1]
                        if i + 2 < len(simpson_y):
                            simpson_weighted_sum += 3 * simpson_y[i + 2]
                        if i + 3 < len(simpson_y) - 1:
                            simpson_weighted_sum += 2 * simpson_y[i + 3]
                    
                    simpson_result = (3 * h / 8) * simpson_weighted_sum
                    steps.append(f"Step 4: Simpson's 3/8 part: (3 × {h:.6f}/8) × {simpson_weighted_sum:.6f} = {simpson_result:.6f}")
                else:
                    simpson_result = 0
                    steps.append(f"Step 4: Simpson's 3/8 part: 0 (no suitable intervals)")
                
                # Trapezoidal part for remaining intervals
                trapezoidal_result = 0
                if trapezoidal_intervals > 0:
                    for i in range(simpson_intervals, self.n):
                        area_i = (h / 2) * (self.y_values[i] + self.y_values[i + 1])
                        trapezoidal_result += area_i
                        steps.append(f"Step 5.{i-simpson_intervals+1}: Trapezoidal interval {i+1}: ({h:.6f}/2) × ({self.y_values[i]:.6f} + {self.y_values[i+1]:.6f}) = {area_i:.6f}")
                
                result = simpson_result + trapezoidal_result
                steps.append(f"Step 6: Total result = {simpson_result:.6f} + {trapezoidal_result:.6f} = {result:.6f}")
        
        else:
            # Unequal intervals - use adaptive approach
            steps.append("Step 1: Intervals are unequal - using adaptive approach")
            steps.append("Step 2: Identifying evenly spaced chunks for Simpson's 3/8 rule")
            
            result = 0
            i = 0
            
            while i < self.n:
                # Find the next chunk of equal intervals
                chunk_start = i
                chunk_h = h_values[i]
                
                # Find how many consecutive intervals have the same width
                j = i + 1
                while j < self.n and np.isclose(h_values[j], chunk_h, atol=1e-10):
                    j += 1
                
                chunk_end = j
                chunk_intervals = chunk_end - chunk_start
                chunk_points = chunk_intervals + 1
                
                steps.append(f"Step 3.{chunk_start+1}: Found evenly spaced chunk from point {chunk_start} to {chunk_end} (h = {chunk_h:.6f})")
                
                if chunk_intervals >= 3 and chunk_intervals % 3 == 0:
                    # Use Simpson's 3/8 rule on this chunk (multiple of 3 intervals)
                    chunk_y = self.y_values[chunk_start:chunk_end+1]
                    
                    weighted_sum = chunk_y[0] + chunk_y[-1]
                    
                    # Process in groups of 3 intervals
                    for k in range(0, chunk_intervals, 3):
                        if k + 1 < len(chunk_y):
                            weighted_sum += 3 * chunk_y[k + 1]
                        if k + 2 < len(chunk_y):
                            weighted_sum += 3 * chunk_y[k + 2]
                        if k + 3 < len(chunk_y) - 1:
                            weighted_sum += 2 * chunk_y[k + 3]
                    
                    chunk_result = (3 * chunk_h / 8) * weighted_sum
                    result += chunk_result
                    
                    steps.append(f"Step 4.{chunk_start+1}: Simpson's 3/8 on chunk: (3 × {chunk_h:.6f}/8) × {weighted_sum:.6f} = {chunk_result:.6f}")
                    
                elif chunk_intervals >= 1:
                    # Use Trapezoidal rule on this chunk
                    chunk_result = 0
                    for k in range(chunk_start, chunk_end):
                        area_k = (h_values[k] / 2) * (self.y_values[k] + self.y_values[k+1])
                        chunk_result += area_k
                        steps.append(f"Step 4.{chunk_start+1}.{k-chunk_start+1}: Trapezoidal interval {k+1}: ({h_values[k]:.6f}/2) × ({self.y_values[k]:.6f} + {self.y_values[k+1]:.6f}) = {area_k:.6f}")
                    
                    result += chunk_result
                    steps.append(f"Step 5.{chunk_start+1}: Trapezoidal on chunk: {chunk_result:.6f}")
                
                i = chunk_end
            
            steps.append(f"Step 6: Total result = {result:.6f}")
        
        # Error estimation
        error_estimate = None
        if len(self.x_values) > 4:
            # Simple error estimation
            if np.allclose(h_values, h_values[0]):
                h = h_values[0]
                fourth_diff = np.diff(self.y_values, 4)
                if len(fourth_diff) > 0:
                    max_fourth_diff = np.max(np.abs(fourth_diff))
                    error_estimate = -(3 * h**5 / 80) * max_fourth_diff * (self.x_values[-1] - self.x_values[0])
                    steps.append(f"Error Estimate: ≈ {error_estimate:.6f}")
        
        method_name = "Simpson's 3/8 Rule (Adaptive)" if not np.allclose(h_values, h_values[0]) else ("Simpson's 3/8 Rule" if self.n % 3 == 0 else "Simpson's 3/8 + Trapezoidal (Hybrid)")
        
        return {
            'result': result,
            'steps': steps,
            'error_estimate': error_estimate,
            'method_name': method_name
        }
    
    def calculate_method(self, method: str) -> Dict[str, Any]:
        """Calculate using specified method"""
        methods = {
            'trapezoidal': self.trapezoidal_rule,
            'simpson_1_3': self.simpson_1_3_rule,
            'simpson_3_8': self.simpson_3_8_rule,
        }
        if method not in methods:
            raise ValueError(f"Unknown method: {method}")
        
        return methods[method]()
    
    def compare_all_methods(self) -> Dict[str, Any]:
        """Compare all applicable methods"""
        results = {}
        
        # Trapezoidal rule always works
        try:
            results['trapezoidal'] = self.calculate_method('trapezoidal')
        except Exception as e:
            results['trapezoidal'] = {'error': str(e)}
        
        # Simpson's 1/3 rule (now with hybrid support)
        try:
            results['simpson_1_3'] = self.calculate_method('simpson_1_3')
        except Exception as e:
            results['simpson_1_3'] = {'error': str(e)}
        
        # Simpson's 3/8 rule (now with hybrid support)
        try:
            results['simpson_3_8'] = self.calculate_method('simpson_3_8')
        except Exception as e:
            results['simpson_3_8'] = {'error': str(e)}
        
        return results