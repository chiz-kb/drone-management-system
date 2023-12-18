from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .forms import AircraftModelForm
from .models import AircraftMasterComponent, AircraftModel, Authorization, Activity, Company, ManufacturerPart, Operator, Contact, Aircraft, Person, Pilot, AircraftDetail, AircraftComponent, Firmware, AircraftAssembly, SupplierPart, MasterComponentAssembly
# Register your models here.



class AircraftModelAdmin( SimpleHistoryAdmin, admin.ModelAdmin,):
    form = AircraftModelForm

class AircraftComponentAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    readonly_fields = ('aerobridge_id',)

admin.site.register(Authorization)
admin.site.register(Activity)
admin.site.register(Company)
admin.site.register(Firmware)
admin.site.register(Operator)
admin.site.register(Contact)
admin.site.register(Pilot)
admin.site.register(Person)
admin.site.register(Aircraft, SimpleHistoryAdmin)
admin.site.register(AircraftModel,AircraftModelAdmin)
admin.site.register(AircraftAssembly,SimpleHistoryAdmin)
admin.site.register(AircraftDetail, SimpleHistoryAdmin)
admin.site.register(AircraftMasterComponent, SimpleHistoryAdmin)
admin.site.register(MasterComponentAssembly, SimpleHistoryAdmin)
admin.site.register(AircraftComponent, AircraftComponentAdmin)
admin.site.register(SupplierPart, SimpleHistoryAdmin)
admin.site.register(ManufacturerPart, SimpleHistoryAdmin)
