
from django.contrib import admin
from agency_app.models import( 
        Pages, Category, Property, Agent, PartnerStok, Images, 
        Advertising, City
    )


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PropImagesAdminInline(admin.TabularInline):
    model = Images
    extra = 10

class CityProp(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PropertyAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',),
    }

    inlines = [PropImagesAdminInline]


class AgentAdmin(admin.ModelAdmin):
    pass

class PartnerStokAdmin(admin.ModelAdmin):
    pass

class ThePagesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class AdminAdvertising(admin.ModelAdmin):
    pass
        
admin.site.register(City, CityProp)
admin.site.register(Advertising, AdminAdvertising)
admin.site.register(Pages, ThePagesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(PartnerStok, PartnerStokAdmin)
