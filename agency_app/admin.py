
from django.contrib import admin
from agency_app.models import( 
        Pages,
        Category,
        Property,
        Agent,
        PartnerStok,
        Images, 
        Advertising,
        City,
        Qeustions,
        Appointement,
        PropertyStatistic
    )


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class PropImagesAdminInline(admin.TabularInline):
    model = Images
    extra = 2

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

class QeustionsAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('quest',),
    }

class AppointementAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('appointment',),
    }

class PropertyStatisticAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'date', 'views')  # отображаемые поля в админке
    search_fields = ('__str__', )               # поле, по которому производится поиск      


admin.site.register(City, CityProp)
admin.site.register(Advertising, AdminAdvertising)
admin.site.register(Pages, ThePagesAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Agent, AgentAdmin)
admin.site.register(PartnerStok, PartnerStokAdmin)
admin.site.register(Qeustions, QeustionsAdmin)
admin.site.register(Appointement, AppointementAdmin)
admin.site.register(PropertyStatistic, PropertyStatisticAdmin)

