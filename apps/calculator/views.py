from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import traceback

from apps.calculator.forms import DataInputForm, CSVUploadForm, ComparisonForm
from apps.calculator.models import CalculationResult
from apps.calculator.utils.integration_methods import IntegrationCalculator
from apps.calculator.utils.data_parser import DataParser
from apps.calculator.utils.plot_generator import PlotGenerator
from apps.calculator.utils.export_utils import ExportUtils


def index(request):
    """Main calculator page"""
    form = DataInputForm()
    comparison_form = ComparisonForm()
    csv_form = CSVUploadForm()
    
    context = {
        'form': form,
        'comparison_form': comparison_form,
        'csv_form': csv_form,
        'recent_calculations': CalculationResult.objects.all()[:5]
    }
    
    return render(request, 'calculator/index.html', context)


@require_http_methods(["POST"])
def calculate(request):
    """Handle single method calculation"""
    try:
        # Parse input data
        if request.POST.get('data_source') == 'csv':
            # Data from CSV (stored in session)
            if 'csv_data' not in request.session:
                return JsonResponse({'error': 'No CSV data found. Please upload a CSV file first.'})
            
            csv_data = request.session['csv_data']
            x_values = csv_data['x_values']
            y_values = csv_data['y_values']
        else:
            # Manual input
            form = DataInputForm(request.POST)
            if not form.is_valid():
                return JsonResponse({'error': 'Invalid form data', 'form_errors': form.errors})
            
            x_values, y_values = DataParser.parse_manual_input(
                form.cleaned_data['x_values'],
                form.cleaned_data['y_values']
            )
        
        method = request.POST.get('method')
        if not method:
            return JsonResponse({'error': 'Method not specified'})
        
        # Validate data for the specific method
        validation_errors = DataParser.validate_data_for_method(x_values, y_values, method)
        if validation_errors:
            return JsonResponse({'error': 'Data validation failed', 'validation_errors': validation_errors})
        
        # Perform calculation
        calculator = IntegrationCalculator(x_values, y_values)
        result = calculator.calculate_method(method)
        
        # Generate plot
        plot_generator = PlotGenerator(x_values, y_values)
        plot_base64 = plot_generator.create_integration_plot(method, result)
        
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
        
        # Store in session for export
        request.session['last_calculation'] = {
            'x_values': x_values,
            'y_values': y_values,
            'result': result,
            'method': method
        }
        
        return JsonResponse({
            'success': True,
            'result': result,
            'plot': plot_base64,
            'data_points': {'x': x_values, 'y': y_values}
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Calculation error: {str(e)}',
            'traceback': traceback.format_exc() if request.user.is_superuser else None
        })


@require_http_methods(["POST"])
def compare_methods(request):
    """Handle comparison of all methods"""
    try:
        # Parse input data
        if request.POST.get('data_source') == 'csv':
            if 'csv_data' not in request.session:
                return JsonResponse({'error': 'No CSV data found. Please upload a CSV file first.'})
            
            csv_data = request.session['csv_data']
            x_values = csv_data['x_values']
            y_values = csv_data['y_values']
        else:
            form = ComparisonForm(request.POST)
            if not form.is_valid():
                return JsonResponse({'error': 'Invalid form data', 'form_errors': form.errors})
            
            x_values, y_values = DataParser.parse_manual_input(
                form.cleaned_data['x_values'],
                form.cleaned_data['y_values']
            )
        
        # Perform comparison
        calculator = IntegrationCalculator(x_values, y_values)
        comparison_results = calculator.compare_all_methods()
        
        # Generate comparison plot
        plot_generator = PlotGenerator(x_values, y_values)
        plot_base64 = plot_generator.create_comparison_plot(comparison_results)
        
        # Store in session for export
        request.session['last_comparison'] = {
            'x_values': x_values,
            'y_values': y_values,
            'results': comparison_results
        }
        
        return JsonResponse({
            'success': True,
            'results': comparison_results,
            'plot': plot_base64,
            'data_points': {'x': x_values, 'y': y_values}
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'Comparison error: {str(e)}',
            'traceback': traceback.format_exc() if request.user.is_superuser else None
        })


@csrf_exempt
@require_http_methods(["POST"])
def upload_csv(request):
    """Handle CSV file upload"""
    try:
        csv_form = CSVUploadForm(request.POST, request.FILES)
        if not csv_form.is_valid():
            return JsonResponse({'error': 'Invalid file upload', 'form_errors': csv_form.errors})
        
        csv_file = request.FILES['csv_file']
        
        # Validate file type
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'Please upload a CSV file'})
        
        # Read file content
        try:
            file_content = csv_file.read().decode('utf-8')
        except UnicodeDecodeError:
            return JsonResponse({'error': 'Unable to read CSV file. Please ensure it is UTF-8 encoded.'})
        
        # Parse CSV data
        x_values, y_values = DataParser.parse_csv_file(file_content)
        
        # Store in session
        request.session['csv_data'] = {
            'x_values': x_values,
            'y_values': y_values,
            'filename': csv_file.name
        }
        
        return JsonResponse({
            'success': True,
            'message': f'Successfully loaded {len(x_values)} data points from {csv_file.name}',
            'data_points': len(x_values),
            'x_range': [min(x_values), max(x_values)],
            'y_range': [min(y_values), max(y_values)],
            'preview': {
                'x': x_values[:5],  # First 5 points for preview
                'y': y_values[:5]
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'CSV upload error: {str(e)}',
            'traceback': traceback.format_exc() if request.user.is_superuser else None
        })


def export_results(request):
    """Export calculation results"""
    export_format = request.GET.get('format', 'csv')
    export_type = request.GET.get('type', 'last')  # 'last' or 'comparison'
    
    try:
        if export_type == 'comparison' and 'last_comparison' in request.session:
            data = request.session['last_comparison']
            x_values = data['x_values']
            y_values = data['y_values']
            results = data['results']
            filename_base = 'integration_comparison'
        elif 'last_calculation' in request.session:
            data = request.session['last_calculation']
            x_values = data['x_values']
            y_values = data['y_values']
            results = data['result']
            filename_base = f'integration_{data["method"]}'
        else:
            messages.error(request, 'No calculation results to export')
            return redirect('calculator:index')
        
        # Generate export based on format
        if export_format == 'csv':
            return ExportUtils.export_to_csv(x_values, y_values, results, f'{filename_base}.csv')
        elif export_format == 'json':
            return ExportUtils.export_to_json(x_values, y_values, results, f'{filename_base}.json')
        elif export_format == 'txt':
            return ExportUtils.export_detailed_report(x_values, y_values, results, f'{filename_base}.txt')
        else:
            messages.error(request, 'Invalid export format')
            return redirect('calculator:index')
            
    except Exception as e:
        messages.error(request, f'Export error: {str(e)}')
        return redirect('calculator:index')