# Numerical Integration Calculator

A modern web-based numerical integration calculator built with Django that implements three fundamental numerical integration methods: Trapezoidal Rule, Simpson's 1/3 Rule, and Simpson's 3/8 Rule.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🚀 Features

### Core Integration Methods
- **Trapezoidal Rule**: Works with any number of data points, handles equal/unequal intervals
- **Simpson's 1/3 Rule**: Higher accuracy for smooth functions, uses adaptive approach for optimal precision
- **Simpson's 3/8 Rule**: Excellent for cubic polynomials, uses adaptive approach for optimal precision
- **Adaptive Integration**: Automatically uses Simpson's rules on evenly spaced chunks and Trapezoidal on uneven chunks

### Data Input Options
- **Manual Entry**: Direct input of x and y coordinates
- **CSV Upload**: Drag-and-drop or browse to upload CSV files
- **Sample Data**: Pre-loaded datasets for testing

### Advanced Features
- **Step-by-Step Solutions**: Detailed calculation steps for education
- **Error Estimation**: Automatic error bounds calculation
- **Method Comparison**: Compare all applicable methods side-by-side
- **Visual Plots**: Interactive matplotlib-generated plots
- **Export Options**: CSV, JSON, or detailed text report formats
- **Calculation History**: Track recent calculations

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- pip
- Git

### Quick Setup
```bash
# Clone repository
git clone https://github.com/yourusername/numerical_integration.git
cd numerical_integration

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Load sample data (optional)
python manage.py load_sample_data

# Run server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to use the calculator.

## 📊 Usage

1. **Choose data input**: Manual entry or CSV upload
2. **Select method**: Trapezoidal, Simpson's 1/3, or Simpson's 3/8
3. **Calculate**: Single method or compare all methods
4. **Review results**: Value, error estimate, steps, and plot
5. **Export** (optional): CSV, JSON, or detailed report

## 📁 Sample Data

Included datasets:
- `sine_function.csv`: Sine wave data
- `quadratic_function.csv`: Quadratic function
- `sine_sample_data_100.csv`: High-resolution sine wave
- `cleaned_airquality.csv`: Real-world air quality data
- `sample_integration_data.csv`: Basic example

## 🧮 Mathematical Methods

### Trapezoidal Rule
```
∫f(x)dx ≈ (h/2)[f(x₀) + 2f(x₁) + 2f(x₂) + ... + 2f(xₙ₋₁) + f(xₙ)]
```

### Simpson's 1/3 Rule
```
∫f(x)dx ≈ (h/3)[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + f(xₙ)]
```

### Simpson's 3/8 Rule
```
∫f(x)dx ≈ (3h/8)[f(x₀) + 3f(x₁) + 3f(x₂) + 2f(x₃) + 3f(x₄) + ... + f(xₙ)]
```

### Adaptive Integration
The calculator uses an intelligent adaptive approach that maximizes accuracy:

- **Simpson's 1/3 Rule**: Applied to evenly spaced chunks with even number of intervals (O(h⁴) accuracy)
- **Simpson's 3/8 Rule**: Applied to evenly spaced chunks with intervals that are multiple of 3 (O(h⁴) accuracy)
- **Trapezoidal Rule**: Applied to uneven chunks or remaining intervals (O(h²) accuracy)

This adaptive strategy ensures optimal accuracy by using higher-order methods where possible while maintaining compatibility with any data distribution.

## 📦 Dependencies

- **Django 5.2.4**: Web framework
- **NumPy 2.3.2**: Numerical computing
- **SciPy 1.16.1**: Scientific computing
- **Pandas 2.3.1**: Data manipulation
- **Matplotlib 3.10.5**: Plotting and visualization

## 🧪 Testing

```bash
python manage.py test
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 📞 Support

- Check [Issues](https://github.com/yourusername/numerical_integration/issues)
- Create a new issue with detailed description
- Contact: your.email@example.com

---

**Made with ❤️ for numerical computing education** 