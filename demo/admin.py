from django.contrib import admin
from demo.models import TimeCredit
# Create a TimeCredit object with the desired fields
# new_credit = TimeCredit.objects.create(service_id=1, hours_available=10)
from .models import Service, UserActivity,ServiceRequest
from django.utils.html import format_html

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'created_at', 'is_approved', 'action_buttons')
    list_filter = ('is_approved',)
    search_fields = ('title', 'user__username', 'description')

    # Custom buttons to approve/reject
    def action_buttons(self, obj):
        approve_button = format_html(
            '<a class="button" href="/admin/app_name/service/{}/approve/">Approve</a>',
            obj.id
        )
        reject_button = format_html(
            '<a class="button" href="/admin/app_name/service/{}/reject/">Reject</a>',
            obj.id
        )
        return f"{approve_button} {reject_button}"
    action_buttons.short_description = "Actions"

    # Custom action for approve/reject
    def approve_service(self, request, queryset):
        queryset.update(is_approved=True)
    
    def reject_service(self, request, queryset):
        queryset.update(is_approved=False)
    
    approve_service.short_description = 'Approve selected services'
    reject_service.short_description = 'Reject selected services'

    actions = [approve_service, reject_service]

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'user', 'category', 'hours_requested', 'date_created', 'accepted', 'accepted_by')
    
    # Fields to filter by in the admin interface
    list_filter = ('category', 'accepted', 'date_created')
    
    # Searchable fields in the admin interface
    search_fields = ('title', 'description', 'user__username', 'accepted_by__username')
    
    # Default ordering for the list view
    ordering = ('-date_created',)
    
    # Fieldsets to organize the form view
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'hours_requested', 'user')
        }),
        ('Status', {
            'fields': ('accepted', 'accepted_by')
        }),
        ('Important Dates', {
            'fields': ('date_created',)
        }),
    )
    
    # Read-only fields in the admin form
    readonly_fields = ('date_created',)

class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'timestamp')
    search_fields = ('user__username', 'action')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)

# Register the models with the admin interface
admin.site.register(Service, ServiceAdmin)
admin.site.register(UserActivity, UserActivityAdmin)




