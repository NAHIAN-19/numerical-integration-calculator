# Team Plan - Numerical Integration Calculator

## Project Structure & Role Assignments

```
numerical_integration_calculator/
├── core/                       # Core Developer: Nahid
│   ├── __init__.py
│   ├── methods.py             # Nahid: all integration routines
│   ├── error.py               # Nahid: error‐estimation utilities
│   └── utils.py               # Nahid: subinterval partitioner, helper functions
│
├── io/                         # UI/UX Designer & Developer: Nahian
│   ├── __init__.py
│   ├── parser.py              # Nahian: file‐input parsing (JSON/DSL → callable)
│   └── validator.py           # Nahian: input sanity checks
│
├── gui/                        # UI/UX Designer & Developer: Nahian
│   ├── __init__.py
│   ├── main_window.py         # Nahian: top‐level window + menu
│   ├── widgets/               # Nahian: custom UI components
│   │   ├── method_selector.py # Nahian: choose integration rules
│   │   ├── plot_canvas.py     # Nahian: Matplotlib canvas wrapper
│   │   └── export_dialog.py   # Nahian: save‐as dialog logic
│   └── controller.py          # Nahian: glue UI ↔ core & io
│
├── exports/                    # UI/UX Designer & Developer: Nahian
│   ├── __init__.py
│   ├── to_csv.py              # Nahian: write results table to CSV
│   ├── to_png.py              # Nahian: render & save plots as PNG
│   └── to_pdf.py              # Nahian: bundle figures + tables into PDF
│
├── tests/                      # Documentation & Testing: Amirul
│   ├── test_methods.py        # Amirul: verify core methods via tests
│   ├── test_error.py          # Amirul: test error‐estimation accuracy
│   ├── test_parser.py         # Amirul: validate io/parser & validator
│   └── test_integration.py    # Amirul: headless GUI→core smoke tests
│
├── requirements.txt            # Documentation & Testing: Amirul
├── README.md                   # Documentation & Testing: Amirul
└── setup.py                    # Documentation & Testing: Amirul
```

## Team Member Responsibilities

### Nahid (Core Developer)
**Primary Focus:** Core numerical computation modules

**Responsibilities:**
- `core/`: All numerical methods, error utilities, helper functions
- Implementation of various numerical integration algorithms
- Error estimation and analysis utilities
- Helper functions for subinterval partitioning and mathematical operations

### Nahian (UI/UX Designer & Developer)
**Primary Focus:** User interface and data handling

**Responsibilities:**
- `io/`: Parsing & validation modules
  - File input parsing (JSON/DSL → callable functions)
  - Input sanity checks and validation
- `gui/`: Complete user interface implementation
  - Main window and menu system
  - Custom UI widgets and components
  - Application controller (UI ↔ core & io integration)
- `exports/`: Data export functionality
  - CSV export for results tables
  - PNG export for plots and visualizations
  - PDF generation for comprehensive reports

### Amirul (Documentation & Testing)
**Primary Focus:** Quality assurance and project documentation

**Responsibilities:**
- `tests/`: Comprehensive testing suite
  - Unit tests for core numerical methods
  - Error estimation accuracy testing
  - Parser and validator testing
  - Integration tests for GUI-core interactions
- **Project Documentation:**
  - `requirements.txt`: Dependency management
  - `README.md`: Project documentation and user guide
  - `setup.py`: Installation and packaging configuration
