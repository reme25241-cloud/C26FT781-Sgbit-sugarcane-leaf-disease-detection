from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group  # Import Group model
from .models import CustomUser, Feedback, Message




# -------------------------------
# Admin Site Branding
# -------------------------------
admin.site.site_header = "Main App Admin"
admin.site.site_title = "Dashboard | Main Application"
admin.site.index_title = "Welcome to the Main Application Dashboard"

# -------------------------------
# Custom User Admin
# -------------------------------
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'gender')
    search_fields = ('email', 'name')
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('name', 'contact', 'age', 'gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

# -------------------------------
# Feedback Admin
# -------------------------------
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'resolved']
    list_filter = ['resolved']
    search_fields = ['user__name', 'message']
    ordering = ['-created_at']
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        updated = queryset.update(resolved=True)
        self.message_user(request, f"{updated} feedback(s) marked as resolved.")
    mark_resolved.short_description = "Mark selected feedback as resolved"

# -------------------------------
# Message Admin
# -------------------------------
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'timestamp', 'is_group_message')
    search_fields = ('sender__email', 'receiver__email', 'text')
    list_filter = ('is_group_message', 'timestamp')
    readonly_fields = ('timestamp',)
    ordering = ['-timestamp']

# -------------------------------
# Unregister Group model to remove it from admin
# -------------------------------
admin.site.unregister(Group)


    ## ========= Main|Application|Functionality_2O_8O_O7P1_2Q5 ## =========
