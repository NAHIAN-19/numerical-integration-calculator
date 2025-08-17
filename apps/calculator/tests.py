from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
import json
from apps.calculator.models import CalculationResult
from apps.calculator.utils.integration_methods import IntegrationCalculator
from apps.calculator.utils.data_parser import DataParser


class IntegrationMethodsTestCase(TestCase):
    """Test cases for numerical integration methods"""
    
    def setUp(self):
        self.x_values = [0, 1, 2, 3, 4]
        self.y_values = [1, 4, 9, 16, 25]  # y = x^2 + 1
        self.calculator = IntegrationCalculator(self.x_values, self.y_values)
    
    def test_trapezoidal_rule(self):
        """Test trapezoidal rule calculation"""
        result = self.calculator.trapezoidal_rule()
        self.assertIsInstance(result['result'], float)
        self.assertIn('steps', result)
        self.assertIn('method_name', result)
        self.assertEqual(result['method_name'], 'Trapezoidal Rule')
    
    def test_simpson_1_3_rule(self):
        """Test Simpson's 1/3 rule calculation"""
        result = self.calculator.simpson_1_3_rule()
        self.assertIsInstance(result['result'], float)
        self.assertIn('steps', result)
        self.assertEqual(result['method_name'], "Simpson's 1/3 Rule")
    
    def test_simpson_3_8_rule_invalid_intervals(self):
        """Test Simpson's 3/8 rule with invalid number of intervals"""
        with self.assertRaises(ValueError):
            self.calculator.simpson_3_8_rule()
    
    def test_compare_all_methods(self):
        """Test comparison of all methods"""
        results = self.calculator.compare_all_methods()
        self.assertIn('trapezoidal', results)
        self.assertIn('simpson_1_3', results)
        self.assertIn('simpson_3_8', results)


class DataParserTestCase(TestCase):
    """Test cases for data parsing utilities"""
    
    def test_parse_manual_input(self):
        """Test parsing manual input strings"""
        x_string = "0, 1, 2, 3, 4"
        y_string = "1, 4, 9, 16, 25"
        
        x_values, y_values = DataParser.parse_manual_input(x_string, y_string)
        
        self.assertEqual(len(x_values), 5)
        self.assertEqual(len(y_values), 5)
        self.assertEqual(x_values, [0.0, 1.0, 2.0, 3.0, 4.0])
        self.assertEqual(y_values, [1.0, 4.0, 9.0, 16.0, 25.0])
    
    def test_parse_csv_file(self):
        """Test parsing CSV file content"""
        csv_content = "X,Y\n0,1\n1,4\n2,9\n3,16\n4,25"
        
        x_values, y_values = DataParser.parse_csv_file(csv_content)
        
        self.assertEqual(len(x_values), 5)
        self.assertEqual(len(y_values), 5)
        self.assertEqual(x_values, [0.0, 1.0, 2.0, 3.0, 4.0])
        self.assertEqual(y_values, [1.0, 4.0, 9.0, 16.0, 25.0])
    
    def test_validate_data_for_method(self):
        """Test data validation for specific methods"""
        x_values = [0, 1, 2, 3, 4]
        y_values = [1, 4, 9, 16, 25]
        
        # Should pass for trapezoidal
        errors = DataParser.validate_data_for_method(x_values, y_values, 'trapezoidal')
        self.assertEqual(len(errors), 0)
        
        # Should pass for Simpson's 1/3 (even number of intervals)
        errors = DataParser.validate_data_for_method(x_values, y_values, 'simpson_1_3')
        self.assertEqual(len(errors), 0)
        
        # Should fail for Simpson's 3/8 (not divisible by 3)
        errors = DataParser.validate_data_for_method(x_values, y_values, 'simpson_3_8')
        self.assertGreater(len(errors), 0)


class ViewsTestCase(TestCase):
    """Test cases for Django views"""
    
    def setUp(self):
        self.client = Client()
    
    def test_index_view(self):
        """Test main calculator page"""
        response = self.client.get(reverse('calculator:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Numerical Integration Calculator')
    
    def test_calculate_view_manual_input(self):
        """Test calculation with manual input"""
        data = {
            'x_values': '0, 1, 2, 3, 4',
            'y_values': '1, 4, 9, 16, 25',
            'method': 'trapezoidal'
        }
        
        response = self.client.post(reverse('calculator:calculate'), data)
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data.get('success'))
        self.assertIn('result', response_data)
        self.assertIn('plot', response_data)
    
    def test_compare_methods_view(self):
        """Test method comparison"""
        data = {
            'x_values': '0, 1, 2, 3, 4',
            'y_values': '1, 4, 9, 16, 25'
        }
        
        response = self.client.post(reverse('calculator:compare'), data)
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data.get('success'))
        self.assertIn('results', response_data)
        self.assertIn('plot', response_data)
    
    def test_csv_upload_view(self):
        """Test CSV file upload"""
        csv_content = b"X,Y\n0,1\n1,4\n2,9\n3,16\n4,25"
        csv_file = SimpleUploadedFile("test.csv", csv_content, content_type="text/csv")
        
        response = self.client.post(reverse('calculator:upload_csv'), {'csv_file': csv_file})
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertTrue(response_data.get('success'))
        self.assertEqual(response_data.get('data_points'), 5)


class ModelTestCase(TestCase):
    """Test cases for Django models"""
    
    def test_calculation_result_model(self):
        """Test CalculationResult model"""
        x_values = [0, 1, 2, 3, 4]
        y_values = [1, 4, 9, 16, 25]
        steps = ["Step 1: Calculate h", "Step 2: Apply formula"]
        
        calc_result = CalculationResult(
            method='trapezoidal',
            result=42.0,
            error_estimate=0.5
        )
        calc_result.set_x_values(x_values)
        calc_result.set_y_values(y_values)
        calc_result.set_calculation_steps(steps)
        calc_result.save()
        
        # Test retrieval
        saved_result = CalculationResult.objects.get(id=calc_result.id)
        self.assertEqual(saved_result.get_x_values(), x_values)
        self.assertEqual(saved_result.get_y_values(), y_values)
        self.assertEqual(saved_result.get_calculation_steps(), steps)
        self.assertEqual(saved_result.method, 'trapezoidal')
        self.assertEqual(saved_result.result, 42.0)
        self.assertEqual(saved_result.error_estimate, 0.5)