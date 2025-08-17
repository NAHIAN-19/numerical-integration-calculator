from django.contrib import admin
from apps.calculator.models import CalculationResult


@admin.register(CalculationResult)
class CalculationResultAdmin(admin.ModelAdmin):
    list_display = ['method', 'result', 'error_estimate', 'created_at']
    list_filter = ['method', 'created_at']
    search_fields = ['method']
    readonly_fields = ['created_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')
    
    fieldsets = (
        ('Method Information', {
            'fields': ('method', 'result', 'error_estimate')
        }),
        ('Data', {
            'fields': ('x_values', 'y_values', 'calculation_steps'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )