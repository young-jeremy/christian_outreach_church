import sys

# Print the current recursion limit
print(f"Current recursion limit: {sys.getrecursionlimit()}")

# Temporarily increase the recursion limit to see where the error occurs
# (This is just for debugging, not a permanent solution)
sys.setrecursionlimit(3000)  # Default is usually 1000


# Add this to your admin.py to help debug
class EmailAddressAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        print("Initializing EmailAddressAdmin")
        super().__init__(*args, **kwargs)

    def changelist_view(self, request, extra_context=None):
        print("In changelist_view")
        return super().changelist_view(request, extra_context)
