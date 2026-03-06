from django.contrib import admin
from .models import SystemLog

@admin.register(SystemLog)
class SystemLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'log_level', 'event_name', 'actor_type', 'actor_id', 'service_name', 'ip_address')
    list_filter = ('log_level', 'actor_type', 'event_name', 'service_name', 'timestamp')
    search_fields = ('message', 'event_name', 'actor_id', 'request_id', 'ip_address')
    readonly_fields = ('timestamp', 'log_level', 'event_name', 'message', 'actor_type', 'actor_id', 
                       'model_name', 'file_name', 'function_name', 'traceback', 'metadata', 
                       'service_name', 'request_id', 'ip_address', 'user_agent', 'created_at')
    
    # We strictly don't want anyone modifying immutable logs via the backend UI
    def has_add_permission(self, request):
        return False
        
    def has_change_permission(self, request, obj=None):
        return False
