from django.db import models
import json


class CalculationResult(models.Model):
    METHOD_CHOICES = [
        ('trapezoidal', 'Trapezoidal Rule'),
        ('simpson_1_3', "Simpson's 1/3 Rule"),
        ('simpson_3_8', "Simpson's 3/8 Rule"),
    ]
    
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    x_values = models.TextField()  # JSON string
    y_values = models.TextField()  # JSON string
    result = models.FloatField()
    error_estimate = models.FloatField(null=True, blank=True)
    calculation_steps = models.TextField()  # JSON string
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_x_values(self, x_list):
        self.x_values = json.dumps(x_list)
    
    def get_x_values(self):
        return json.loads(self.x_values)
    
    def set_y_values(self, y_list):
        self.y_values = json.dumps(y_list)
    
    def get_y_values(self):
        return json.loads(self.y_values)
    
    def set_calculation_steps(self, steps):
        self.calculation_steps = json.dumps(steps)
    
    def get_calculation_steps(self):
        return json.loads(self.calculation_steps)
    
    class Meta:
        ordering = ['-created_at']