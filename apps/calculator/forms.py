from django import forms


class DataInputForm(forms.Form):
    x_values = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'rows': 4,
            'placeholder': 'Enter X values separated by commas (e.g., 0, 1, 2, 3, 4)'
        }),
        label='X Values',
        help_text='Enter X values separated by commas'
    )
    
    y_values = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'rows': 4,
            'placeholder': 'Enter Y values separated by commas (e.g., 1, 4, 9, 16, 25)'
        }),
        label='Y Values',
        help_text='Enter Y values separated by commas'
    )
    
    method = forms.ChoiceField(
        choices=[
            ('trapezoidal', 'Trapezoidal Rule'),
            ('simpson_1_3', "Simpson's 1/3 Rule"),
            ('simpson_3_8', "Simpson's 3/8 Rule"),
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'
        }),
        label='Integration Method',
        required=False  # Make method field optional
    )


class ComparisonForm(forms.Form):
    """Form for comparing all methods - doesn't require method selection"""
    x_values = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'rows': 4,
            'placeholder': 'Enter X values separated by commas (e.g., 0, 1, 2, 3, 4)'
        }),
        label='X Values',
        help_text='Enter X values separated by commas'
    )
    
    y_values = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500',
            'rows': 4,
            'placeholder': 'Enter Y values separated by commas (e.g., 1, 4, 9, 16, 25)'
        }),
        label='Y Values',
        help_text='Enter Y values separated by commas'
    )


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'hidden',
            'accept': '.csv'
        }),
        label='CSV File'
    )