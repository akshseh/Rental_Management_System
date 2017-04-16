from django.contrib import admin

# Register your models here.
from .models import Visitor
from .models import Owner
from .models import Property
from .models import Rented
from .models import Review, User

class UserAdmin(admin.ModelAdmin):
	last_display = ['id', 'username']
	class Meta:
		model = User

class VisitorAdmin(admin.ModelAdmin):
	last_display = ["id","profile","num_views","pref_location"]
	class Meta:
		model = Visitor

class OwnerAdmin(admin.ModelAdmin):
	last_display = ["id","owner_name","num_properties"]
	class Meta:
		model = Owner

class PropertyAdmin(admin.ModelAdmin):
	last_display = ["id","description","price","location","num_views"]
	class Meta:
		model = Property

class RentedAdmin(admin.ModelAdmin):
	last_display = ["property_id","owner_id","visitor_id","rent_to_be_paid"]
	class Meta:
		model = Rented

class ReviewAdmin(admin.ModelAdmin):
	last_display = ["property_id","visitor_id","visitor_name","rating","comment"]
	class Meta:
		model = Review


admin.site.register(Owner,   OwnerAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Property,PropertyAdmin)
admin.site.register(Rented,  RentedAdmin)
admin.site.register(Review,  ReviewAdmin)
admin.site.register(User, UserAdmin)