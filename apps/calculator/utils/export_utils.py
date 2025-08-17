"""
Export utilities for results and data
"""
import json
import csv
import io
import pandas as pd
from typing import Dict, Any, List
from django.http import HttpResponse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class ExportUtils:
    """Utility class for exporting results in various formats"""
    
    @staticmethod
    def export_to_csv(x_values: List[float], y_values: List[float], 
                     results: Dict[str, Any], filename: str = "integration_results.csv") -> HttpResponse:
        """Export data and results to CSV format"""
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        writer = csv.writer(response)
        
        # Write header
        writer.writerow(['Numerical Integration Results'])
        writer.writerow([])
        
        # Write data points
        writer.writerow(['Data Points'])
        writer.writerow(['X', 'Y'])
        for x, y in zip(x_values, y_values):
            writer.writerow([x, y])
        
        writer.writerow([])
        
        # Write results
        if isinstance(results, dict) and 'result' in results:
            # Single method result
            writer.writerow(['Results'])
            writer.writerow(['Method', results.get('method_name', 'Unknown')])
            writer.writerow(['Result', results['result']])
            if results.get('error_estimate'):
                writer.writerow(['Error Estimate', results['error_estimate']])
            
            writer.writerow([])
            writer.writerow(['Calculation Steps'])
            for i, step in enumerate(results.get('steps', []), 1):
                writer.writerow([f'Step {i}', step])
        
        else:
            # Multiple methods comparison
            writer.writerow(['Comparison Results'])
            writer.writerow(['Method', 'Result', 'Error Estimate'])
            for method, result in results.items():
                if 'error' not in result:
                    method_name = result.get('method_name', method)
                    error_est = result.get('error_estimate', 'N/A')
                    writer.writerow([method_name, result['result'], error_est])
                else:
                    writer.writerow([method, 'Error', result['error']])
        
        return response
    
    @staticmethod
    def export_to_json(x_values: List[float], y_values: List[float], 
                      results: Dict[str, Any], filename: str = "integration_results.json") -> HttpResponse:
        """Export data and results to JSON format"""
        export_data = {
            'data_points': {
                'x_values': x_values,
                'y_values': y_values
            },
            'results': results,
            'export_timestamp': str(pd.Timestamp.now())
        }
        
        response = HttpResponse(
            json.dumps(export_data, indent=2),
            content_type='application/json'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response
    
    @staticmethod
    def export_detailed_report(x_values: List[float], y_values: List[float], 
                             results: Dict[str, Any], filename: str = "integration_report.txt") -> HttpResponse:
        """Export detailed text report"""
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        report = []
        report.append("NUMERICAL INTEGRATION CALCULATION REPORT")
        report.append("=" * 50)
        report.append("")
        
        # Data summary
        report.append("DATA SUMMARY:")
        report.append(f"Number of data points: {len(x_values)}")
        report.append(f"X range: [{min(x_values):.6f}, {max(x_values):.6f}]")
        report.append(f"Y range: [{min(y_values):.6f}, {max(y_values):.6f}]")
        report.append("")
        
        # Data points
        report.append("DATA POINTS:")
        report.append("X\t\tY")
        report.append("-" * 20)
        for x, y in zip(x_values, y_values):
            report.append(f"{x:.6f}\t{y:.6f}")
        report.append("")
        
        # Results
        if isinstance(results, dict) and 'result' in results:
            # Single method
            report.append("CALCULATION RESULTS:")
            report.append(f"Method: {results.get('method_name', 'Unknown')}")
            report.append(f"Result: {results['result']:.10f}")
            if results.get('error_estimate'):
                report.append(f"Error Estimate: ±{abs(results['error_estimate']):.10f}")
            report.append("")
            
            report.append("CALCULATION STEPS:")
            for step in results.get('steps', []):
                report.append(f"  {step}")
        
        else:
            # Multiple methods
            report.append("COMPARISON RESULTS:")
            report.append("-" * 30)
            for method, result in results.items():
                if 'error' not in result:
                    method_name = result.get('method_name', method)
                    report.append(f"{method_name}:")
                    report.append(f"  Result: {result['result']:.10f}")
                    if result.get('error_estimate'):
                        report.append(f"  Error Estimate: ±{abs(result['error_estimate']):.10f}")
                    report.append("")
                else:
                    report.append(f"{method}: Error - {result['error']}")
                    report.append("")
        
        response.write('\n'.join(report))
        return response