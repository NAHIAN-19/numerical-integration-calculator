# Numerical Integration Calculator

A comprehensive GUI application for numerical integration using Python and tkinter. This calculator supports three integration methods: Trapezoidal Rule, Simpson's 1/3 Rule, and Simpson's 3/8 Rule with advanced features like error analysis, method comparison, and export capabilities.

## 🚀 Features

### **Integration Methods**
- **Trapezoidal Rule** - Approximates area using trapezoids
- **Simpson's 1/3 Rule** - Uses quadratic polynomials (requires even intervals)
- **Simpson's 3/8 Rule** - Uses cubic polynomials (requires intervals divisible by 3)

### **Input Support**
- Mathematical functions: `sin(x)`, `cos(x)`, `exp(x)`, `log(x)`, `x**2`, etc.
- Constants like `π (pi)` in functions and limits
- Custom limits and number of intervals
- JSON file import/export for parameter management

### **Advanced Features**
- **Error Analysis** - Exact value calculation with absolute and relative errors
- **Method Comparison** - Compare all three methods simultaneously
- **Graph Comparison** - Visual comparison of integration points
- **Dynamic Results Display** - Large, scrollable text area with professional formatting
- **Export Capabilities** - PDF reports, PNG plots, and comparison graphs


## 🛠️ Installation

### **Step 1: Clone or Download the Project**
```bash
# If using git
git clone --branch exam --single-branch https://github.com/NAHIAN-19/numerical-integration-calculator.git
cd numerical-integration-calculator

# Or download and extract the project files and checkout `exam` branch
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python3 -m venv env

# Activate virtual environment
# On Linux/macOS:
source env/bin/activate

# On Windows:
env\Scripts\activate
```

### **Step 3: Install Dependencies**
```bash
# Install all required packages
pip install -r requirements.txt

# Or install manually:
pip install numpy matplotlib sympy reportlab pytest
```

### **Step 4: Verify Installation**
```bash
# Run tests to verify everything works
python3 test_integration.py
python3 test_enhanced_features.py
python3 test_graph_comparison.py
```

## 🎯 Usage

### **Starting the Application**
```bash
# Make sure virtual environment is activated
source env/bin/activate

# Run the main application
python3 numerical_integration_calculator.py
```

### **Basic Usage**

1. **Enter Function**: Type your mathematical function (e.g., `sin(x)`, `x**2`, `exp(x)`)
2. **Set Limits**: Enter lower and upper limits (e.g., `0`, `pi`, `1`)
3. **Choose Intervals**: Set number of intervals (higher = more accurate)
4. **Select Method**: Choose integration method
5. **Calculate**: Click "Calculate Integration" or "Compare All Methods"

### **Advanced Usage**

#### **Method Comparison**
- Click "Compare All Methods" to see all three methods with error analysis
- View visual comparison graph showing integration points
- See which method is most accurate for your function

#### **File Operations**
- **Save Parameters**: Click "Save to JSON" to save current settings
- **Load Parameters**: Click "Load from JSON" to load saved settings
- Use provided sample files: `sample_config.json`, `sample_config2.json`

#### **Export Features**
- **PDF Export**: Save detailed results and process to PDF
- **PNG Export**: Save current plot as high-resolution image
- **Comparison Export**: Export comparison results and graphs

## 📊 Function Examples

| Function | Description | Example Input |
|----------|-------------|---------------|
| `x**2` | Quadratic function | `x**2` |
| `sin(x)` | Sine function | `sin(x)` |
| `cos(x)` | Cosine function | `cos(x)` |
| `exp(x)` | Exponential function | `exp(x)` |
| `log(x)` | Natural logarithm | `log(x)` |
| `pi*x` | π times x | `pi*x` |
| `x**3 + 2*x**2 - 5` | Polynomial | `x**3 + 2*x**2 - 5` |
| `sin(x) + cos(x)` | Sum of functions | `sin(x) + cos(x)` |
| `exp(-x**2)` | Gaussian function | `exp(-x**2)` |

## 📏 Limit Examples

| Lower Limit (a) | Upper Limit (b) | Description |
|-----------------|-----------------|-------------|
| `0` | `1` | Simple numbers |
| `0` | `pi` | Using π constant |
| `-pi/2` | `pi/2` | Negative to positive |
| `0` | `2*pi` | Multiple of π |

## 🔍 Error Analysis

The application provides comprehensive error analysis:
- **Exact Value Calculation** - Uses symbolic integration to find exact results
- **Absolute Error** - Difference between numerical and exact results
- **Relative Error** - Percentage error relative to exact value
- **Method Comparison** - Ranks methods by accuracy
- **Best Method Selection** - Automatically identifies the most accurate method
- **Graph Comparison** - Visual comparison of integration points for all methods

## 📁 Project Structure

```
numerical-integration-calculator/
├── numerical_integration_calculator.py  # Main application
├── requirements.txt                     # Dependencies
├── README.md                           # This file
├── test_integration.py                 # Basic integration tests
├── test_enhanced_features.py           # Error analysis tests
├── test_graph_comparison.py            # Graph and JSON tests
├── test_function_parsing.py            # Function parsing tests
├── sample_config.json                  # Sample configuration
├── sample_config2.json                 # Another sample configuration
└── env/                                # Virtual environment (created)
```

## 🧪 Testing

### **Run All Tests**
```bash
# Run all test files
python3 test_integration.py
python3 test_enhanced_features.py
python3 test_graph_comparison.py
python3 test_function_parsing.py
```

### **Individual Test Files**
- `test_integration.py` - Tests basic integration methods
- `test_enhanced_features.py` - Tests error analysis and method comparison
- `test_graph_comparison.py` - Tests JSON functionality and graph comparison
- `test_function_parsing.py` - Tests function parsing with trigonometric functions

## 📤 Export Features

- **PDF Export** - Saves calculation results and process to PDF file
- **PNG Export** - Saves current plot as high-resolution PNG image
- **Comparison PDF Export** - Saves method comparison results with error analysis
- **Comparison Graph Export** - Saves comparison graph showing all methods
- **JSON Export/Import** - Save and load calculation parameters

## ⚠️ Troubleshooting

### **Common Issues**

1. **ModuleNotFoundError**: Make sure virtual environment is activated and dependencies are installed
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **PDF Export Fails**: Install reportlab if not already installed
   ```bash
   pip install reportlab
   ```

3. **Plot Not Displaying**: Ensure matplotlib is properly installed
   ```bash
   pip install matplotlib
   ```

4. **Function Parsing Errors**: Check function syntax (use `sin(x)`, not `sin x`)

### **System Requirements**
- **Linux**: Python 3.7+, tkinter (usually included)
- **macOS**: Python 3.7+, tkinter (usually included)
- **Windows**: Python 3.7+, tkinter (usually included)

## 🎓 Educational Value

This project demonstrates:
- **Numerical Methods** - Implementation of integration algorithms
- **GUI Development** - Tkinter interface design
- **Error Analysis** - Mathematical error calculation and comparison
- **Data Visualization** - Matplotlib plotting and graph comparison
- **File I/O** - JSON import/export functionality
- **Testing** - Comprehensive test suite for validation

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the troubleshooting section above
2. Verify all dependencies are installed
3. Run the test files to identify specific problems
4. Check that your Python version is 3.7 or higher

---

**Happy Integrating! 🧮✨** 