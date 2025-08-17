from django.core.management.base import BaseCommand
from django.conf import settings
import os
import csv
from calculator.models import CalculationResult
from calculator.utils.integration_methods import IntegrationCalculator


class Command(BaseCommand):
    help = 'Load sample calculation results from CSV files'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Specific CSV file to load (optional)',
        )

    def handle(self, *args, **options):
        sample_data_dir = os.path.join(settings.BASE_DIR, 'static', 'sample_data')
        
        if options['file']:
            files_to_process = [options['file']]
        else:
            files_to_process = [
                'sample_integration_data.csv',
                'quadratic_function.csv',
                'sine_function.csv',
                'sine_sample_data_100.csv'
            ]

        for filename in files_to_process:
            file_path = os.path.join(sample_data_dir, filename)
            
            if not os.path.exists(file_path):
                self.stdout.write(
                    self.style.WARNING(f'File not found: {filename}')
                )
                continue

            try:
                self.load_csv_file(file_path, filename)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully loaded: {filename}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Error loading {filename}: {str(e)}')
                )

    def load_csv_file(self, file_path, filename):
        x_values = []
        y_values = []
        
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                x_values.append(float(row['X']))
                y_values.append(float(row['Y']))

        # Calculate using all methods
        calculator = IntegrationCalculator(x_values, y_values)
        
        methods = ['trapezoidal', 'simpson_1_3', 'simpson_3_8']
        
        for method in methods:
            try:
                result = calculator.calculate_method(method)
                
                # Save to database
                calc_result = CalculationResult(
                    method=method,
                    result=result['result'],
                    error_estimate=result.get('error_estimate')
                )
                calc_result.set_x_values(x_values)
                calc_result.set_y_values(y_values)
                calc_result.set_calculation_steps(result['steps'])
                calc_result.save()
                
                self.stdout.write(f'  - {method}: {result["result"]:.6f}')
                
            except Exception as e:
                self.stdout.write(f'  - {method}: Error - {str(e)}')