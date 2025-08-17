// Enhanced JavaScript functionality for Numerical Integration Calculator

class NumericalIntegrationUI {
    constructor() {
        this.initializeEventListeners();
        this.initializeTooltips();
        this.initializeKeyboardShortcuts();
    }

    initializeEventListeners() {
        // Enhanced file drag and drop
        this.setupFileDragDrop();
        
        // Form validation
        this.setupFormValidation();
        
        // Result visualization enhancements
        this.setupResultEnhancements();
        
        // Export functionality
        this.setupExportHandlers();
    }

    setupFileDragDrop() {
        const dropZone = document.querySelector('.file-upload-area');
        if (!dropZone) return;

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('dragover');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('dragover');
            }, false);
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    setupFormValidation() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!this.validateForm(form)) {
                    e.preventDefault();
                    this.showValidationErrors(form);
                }
            });
        });
    }

    validateForm(form) {
        const xValues = form.querySelector('[name="x_values"]');
        const yValues = form.querySelector('[name="y_values"]');
        
        if (!xValues || !yValues) return true;

        const xArray = this.parseValues(xValues.value);
        const yArray = this.parseValues(yValues.value);

        if (xArray.length !== yArray.length) {
            this.showError('X and Y values must have the same number of elements');
            return false;
        }

        if (xArray.length < 2) {
            this.showError('At least 2 data points are required');
            return false;
        }

        // Check if X values are sorted
        for (let i = 1; i < xArray.length; i++) {
            if (xArray[i] <= xArray[i-1]) {
                this.showError('X values must be in ascending order');
                return false;
            }
        }

        return true;
    }

    parseValues(valueString) {
        try {
            return valueString.split(',').map(v => parseFloat(v.trim())).filter(v => !isNaN(v));
        } catch (e) {
            return [];
        }
    }

    showValidationErrors(form) {
        // Add visual feedback for validation errors
        const invalidInputs = form.querySelectorAll(':invalid');
        invalidInputs.forEach(input => {
            input.classList.add('border-red-500', 'bg-red-50');
            setTimeout(() => {
                input.classList.remove('border-red-500', 'bg-red-50');
            }, 3000);
        });
    }

    setupResultEnhancements() {
        // Add copy-to-clipboard functionality for results
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('copy-result')) {
                const resultText = e.target.dataset.result;
                this.copyToClipboard(resultText);
                this.showNotification('Result copied to clipboard!', 'success');
            }
        });

        // Add result comparison highlighting
        this.highlightBestResult();
    }

    highlightBestResult() {
        const resultCards = document.querySelectorAll('.method-card');
        if (resultCards.length < 2) return;

        let bestAccuracy = -Infinity;
        let bestCard = null;

        resultCards.forEach(card => {
            const errorElement = card.querySelector('[data-error]');
            if (errorElement) {
                const error = Math.abs(parseFloat(errorElement.dataset.error) || Infinity);
                if (error < Math.abs(bestAccuracy) || bestAccuracy === -Infinity) {
                    bestAccuracy = error;
                    bestCard = card;
                }
            }
        });

        if (bestCard) {
            bestCard.classList.add('ring-2', 'ring-green-500', 'bg-green-50');
            const badge = document.createElement('div');
            badge.className = 'absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full';
            badge.textContent = 'Most Accurate';
            bestCard.style.position = 'relative';
            bestCard.appendChild(badge);
        }
    }

    setupExportHandlers() {
        // Enhanced export with progress indication
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('export-btn')) {
                this.handleExport(e.target.dataset.format, e.target.dataset.type);
            }
        });
    }

    async handleExport(format, type) {
        const exportBtn = document.querySelector(`[data-format="${format}"]`);
        const originalText = exportBtn.textContent;
        
        exportBtn.textContent = 'Exporting...';
        exportBtn.disabled = true;

        try {
            const response = await fetch(`/export/?format=${format}&type=${type}`);
            if (response.ok) {
                const blob = await response.blob();
                this.downloadBlob(blob, `integration_results.${format}`);
                this.showNotification(`Results exported as ${format.toUpperCase()}!`, 'success');
            } else {
                throw new Error('Export failed');
            }
        } catch (error) {
            this.showNotification('Export failed. Please try again.', 'error');
        } finally {
            exportBtn.textContent = originalText;
            exportBtn.disabled = false;
        }
    }

    downloadBlob(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }

    copyToClipboard(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transition-all duration-300 ${
            type === 'error' ? 'bg-red-500 text-white' :
            type === 'success' ? 'bg-green-500 text-white' :
            type === 'warning' ? 'bg-yellow-500 text-white' :
            'bg-blue-500 text-white'
        }`;
        
        notification.innerHTML = `
            <div class="flex items-center">
                <span class="mr-2">${this.getNotificationIcon(type)}</span>
                <span>${message}</span>
                <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                    ×
                </button>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
            notification.style.opacity = '1';
        }, 100);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            notification.style.opacity = '0';
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                }
            }, 300);
        }, 5000);
    }

    getNotificationIcon(type) {
        const icons = {
            error: '⚠️',
            success: '✅',
            warning: '⚡',
            info: 'ℹ️'
        };
        return icons[type] || icons.info;
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    initializeTooltips() {
        // Add tooltips for method explanations
        const tooltips = {
            'trapezoidal': 'Uses linear interpolation between points. Good for general use.',
            'simpson_1_3': 'Uses quadratic interpolation. Requires even number of intervals.',
            'simpson_3_8': 'Uses cubic interpolation. Requires intervals divisible by 3.'
        };

        Object.keys(tooltips).forEach(method => {
            const elements = document.querySelectorAll(`[data-method="${method}"]`);
            elements.forEach(element => {
                element.title = tooltips[method];
                element.setAttribute('data-tooltip', tooltips[method]);
            });
        });
    }

    initializeKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl+Enter to calculate
            if (e.ctrlKey && e.key === 'Enter') {
                const calculateBtn = document.querySelector('button[type="submit"]');
                if (calculateBtn && !calculateBtn.disabled) {
                    calculateBtn.click();
                }
            }
            
            // Ctrl+Shift+C to compare methods
            if (e.ctrlKey && e.shiftKey && e.key === 'C') {
                const compareBtn = document.querySelector('.btn-secondary');
                if (compareBtn && !compareBtn.disabled) {
                    compareBtn.click();
                }
            }
            
            // Escape to clear results
            if (e.key === 'Escape') {
                this.clearResults();
            }
        });
    }

    clearResults() {
        const resultsSection = document.querySelector('[x-show="results || comparisonResults"]');
        if (resultsSection) {
            // Trigger Alpine.js to clear results
            const event = new CustomEvent('clear-results');
            document.dispatchEvent(event);
        }
    }

    // Utility method for formatting numbers with proper precision
    formatNumber(num, precision = 6) {
        if (typeof num !== 'number' || isNaN(num)) return 'N/A';
        
        // Use scientific notation for very large or very small numbers
        if (Math.abs(num) >= 1e6 || (Math.abs(num) < 1e-3 && num !== 0)) {
            return num.toExponential(precision);
        }
        
        return num.toFixed(precision);
    }

    // Method to validate CSV data format
    validateCSVData(csvText) {
        const lines = csvText.trim().split('\n');
        if (lines.length < 2) {
            throw new Error('CSV must contain at least 2 rows of data');
        }

        const dataRows = lines.slice(1); // Skip header if present
        const parsedData = [];

        dataRows.forEach((line, index) => {
            const values = line.split(',').map(v => v.trim());
            if (values.length < 2) {
                throw new Error(`Row ${index + 2} must contain at least 2 values`);
            }

            const x = parseFloat(values[0]);
            const y = parseFloat(values[1]);

            if (isNaN(x) || isNaN(y)) {
                throw new Error(`Row ${index + 2} contains invalid numerical data`);
            }

            parsedData.push({ x, y });
        });

        // Sort by X values
        parsedData.sort((a, b) => a.x - b.x);

        return {
            x_values: parsedData.map(d => d.x),
            y_values: parsedData.map(d => d.y)
        };
    }
}

// Initialize the UI when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NumericalIntegrationUI();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NumericalIntegrationUI;
}