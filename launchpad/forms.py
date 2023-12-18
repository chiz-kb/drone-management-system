
import json

import geojson
from registry.models import AircraftMasterComponent, ManufacturerPart, Person, Address, Operator, Aircraft, Company, Firmware, Contact, Pilot, Activity, Authorization, AircraftDetail, AircraftComponent,AircraftModel,AircraftAssembly,SupplierPart, MasterComponentAssembly
from gcs_operations.models import FlightOperation, FlightLog, FlightPlan, FlightPermission
from supply_chain_operations.models import Incident
from pki_framework.models import AerobridgeCredential
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import arrow
from crispy_forms.helper import FormHelper
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from crispy_forms.layout import Layout, ButtonHolder, Submit, HTML
from crispy_forms.bootstrap import AccordionGroup
from crispy_bootstrap5.bootstrap5 import Field, FloatingField, BS5Accordion
from django.db.models import OuterRef, Exists
from django.db.models import Q

KEY_ENVIRONMENT = ((0, _('DIGITAL SKY OPERATOR')),(1, _('DIGITAL SKY MANUFACTURER')),(2, _('DIGITAL SKY PILOT')),(3, _('RFM')),(4, _('OTHER')),)
TOKEN_TYPE= ((0, _('PUBLIC_KEY')),(1, _('PRIVATE_KEY')),(2, _('AUTHENTICATION TOKEN')),(3, _('RFM KEY')),(4, _('OTHER')),)

# books/forms.py


class PersonCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("first_name"),
                        FloatingField("middle_name"),
                        FloatingField("last_name"),
                        FloatingField("email"),
                        FloatingField("phone_number"),
                        FloatingField("country"),
                        ),
                    AccordionGroup("Optional Information",
                        FloatingField("documents"),                        
                        FloatingField("date_of_birth")
                        ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Person'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'people-list' %}" role="button">Cancel</a>""")
                    )
                )     

    class Meta:
        model = Person
        fields = '__all__'
        
class AddressCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("address_line_1"),
                        FloatingField("address_line_2"),
                        FloatingField("address_line_3"),
                        FloatingField("postcode"),                        
                        FloatingField("city"),
                        FloatingField("state"),
                        FloatingField("country"),
                        ),                                
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Address'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'addresses-list' %}" role="button">Cancel</a>""")
                    )
                )     

    class Meta:
        model = Address
        fields = '__all__'


class OperatorCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        self.fields['company'].queryset = Company.objects.filter(role = 2)
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("company"),
                        FloatingField("website"),
                        FloatingField("email"),
                        FloatingField("phone_number"),
                        FloatingField("operator_type"),
                        FloatingField("address"),
                        ),
                    AccordionGroup("Optional Information",
                        "operational_authorizations",
                        "authorized_activities",
                        FloatingField("insurance_number"),
                        FloatingField("company_number"),
                        FloatingField("vat_number"),
                        FloatingField("country"),
                        ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Operator'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'operators-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    class Meta:
        model = Operator
        exclude = ('expiration',)

class AircraftCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operator"),
                        FloatingField("manufacturer"),
                        FloatingField("final_assembly"),                        
                        FloatingField("flight_controller_id"),
                        FloatingField("status"),
                        FloatingField("photo"),
                        FloatingField("name")
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircrafts-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     
        self.fields['final_assembly'].queryset = AircraftAssembly.objects.filter(~Exists(Aircraft.objects.filter(final_assembly=OuterRef('pk')))).filter(status=2)

    class Meta:
        model = Aircraft
        fields = ('operator','manufacturer', 'name','flight_controller_id', 'final_assembly','status','photo',)

class AircraftDetailCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("aircraft"),
                        FloatingField("is_registered"),  
                        FloatingField("registration_mark"),                                                 
                        FloatingField("commission_date")                    
                        ),
                    AccordionGroup("Optional Information",                                                 
                        FloatingField("identification_photo"),
                        ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft Details'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircrafts-list' %}" role="button">Cancel</a>""")
                    )
                )     
    
    class Meta:
        model = AircraftDetail
        fields = '__all__'

class AircraftComponentCreateForm(forms.ModelForm):
    def __init__(self, aircraft_master_component_id=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True
        
        if aircraft_master_component_id:
            master_component = AircraftMasterComponent.objects.get(id = aircraft_master_component_id)
        
            supplier_part_exists = SupplierPart.objects.filter(manufacturer_part__master_component = master_component).exists()
            if supplier_part_exists:
                self.model_qs =  SupplierPart.objects.filter(manufacturer_part__master_component = master_component)
            else: 
                self.model_qs = SupplierPart.objects.all()
        else:
            self.model_qs = SupplierPart.objects.all()


        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                    
                        FloatingField("supplier_part"),            
                        FloatingField("invoice_receipt"),
                        FloatingField("description"),   
                        ),
                    AccordionGroup("Optional Information",                                                 
                        FloatingField("status"),     
                        FloatingField("purchase_price"),
                        ),                                 
                    
                    
                   
                    ButtonHolder(
                                HTML("""<br>"""),
                                Submit('submit', '+ Add Aircraft Component Details'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-components-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     

        self.fields['supplier_part'] = forms.ModelChoiceField(
                required=True,
                empty_label=None,
                queryset=self.model_qs)

    class Meta:
        model = AircraftComponent
        fields = ('supplier_part','invoice_receipt','description','status','purchase_price')

class AircraftAssemblyCreateForm(forms.ModelForm):
    
    def __init__(self,  *args,aircraft_model_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.model_qs =  AircraftModel.objects.filter(id = aircraft_model_id)
        aircraft_model = AircraftModel.objects.get(id = aircraft_model_id)
        # The components that have not been selected

        
        self.all_master_components = aircraft_model.master_components.all()
        self.relevant_supplier_parts = SupplierPart.objects.filter(manufacturer_part__master_component__in = self.all_master_components)

        self.components_qs = AircraftComponent.objects.filter(~Exists(AircraftAssembly.objects.filter(components__in=OuterRef('pk')))).filter(supplier_part__in =  self.relevant_supplier_parts).filter(status=10)
              
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("status"),
                        FloatingField("model"),
                        Field("components"),
                        HTML("""
                                <small>Select from available components, if no components are avialable, check the inventory and order new ones.</small>
                                <br>
                            """),
                        ),
                  
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft Assembly'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-assemblies-list' %}" role="button">Cancel</a>""")
                    )
                )
        )            
        
        self.fields['model'] = forms.ModelChoiceField(
                required=True,
                empty_label=None,
                queryset=self.model_qs)

        self.fields['components'] = forms.ModelMultipleChoiceField(
                required=True,
                queryset=self.components_qs,
                widget=forms.SelectMultiple())

    def clean_components(self):
        submitted_components = self.cleaned_data['components']
        all_component_occurances = []
        not_found_components = []
        for master_component in self.all_master_components:   
            is_found = False
            all_occurances = []
            for current_component in submitted_components:
                if current_component.supplier_part.manufacturer_part.master_component == master_component:
                    is_found = True
                    break
            if not is_found:
                not_found_components.append(master_component.name)
            
            all_occurances.append(is_found)
                

            all_component_occurances.append(all(all_occurances))
                
        if not_found_components:
            missing_components = ', '.join(not_found_components)
            
            raise ValidationError(
                _("All components from the blueprint must be selected to complete a assembly. if a component is missing please select it or order it to add to the inventory. Following components are missing: %s" % missing_components)
            )
        return submitted_components
    class Meta:
        model = AircraftAssembly
        fields = '__all__'
        help_texts = {
            'components': 'Select from available components',
        }
        
        
class AircraftAssemblyUpdateForm(forms.ModelForm):
    
    def __init__(self,  *args,aircraft_assembly_id, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.model_qs =  AircraftAssembly.objects.filter(id = aircraft_assembly_id)
        aircraft_assembly = AircraftAssembly.objects.get(id = aircraft_assembly_id)
        all_assembly_components = aircraft_assembly.components.all()
        # The components that have not been selected
        aircraft_model = aircraft_assembly.aircraft_model
        self.aircraft_model_qs =  AircraftModel.objects.filter(id = aircraft_model.id)
        self.all_master_components = aircraft_model.master_components.all()

        all_assembly_master_components = []
        for current_component in all_assembly_components:
            supplier_part_exists = current_component.supplier_part
            if supplier_part_exists is not None:
                all_assembly_master_components.append(current_component.supplier_part.manufacturer_part.master_component.id)
            else: 
                all_assembly_master_components.append(current_component.master_component.id)

        
        all_assembly_master_components_qs = AircraftMasterComponent.objects.filter(pk__in = all_assembly_master_components)
        self.qs_diff = self.all_master_components.difference(all_assembly_master_components_qs)    
        

        missing_id_list = self.qs_diff.values_list('id', flat=True)
        self.components_qs = AircraftComponent.objects.filter(Q(master_component__in = missing_id_list)| Q(supplier_part__manufacturer_part__master_component__in = missing_id_list)).filter(status=10).filter(~Exists(AircraftAssembly.objects.filter(components__in=OuterRef('pk'))))

              
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        Field("aircraft_model"),
                        Field("components"),
                        HTML("""
                                <small>Select from available components, if no components are avialable, the assembly is complete and does not need changes.</small>
                                <br>                                
                            """),
                        ),
                            
                        HTML("""
                                <br>
                            """),
                    ButtonHolder(
                                Submit('submit', 'Update Aircraft Assembly'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-assemblies-list' %}" role="button">Cancel</a>""")
                    )
                )
        )            
        
        self.fields['components'] = forms.ModelMultipleChoiceField(
                required=True,
                queryset=self.components_qs,
                widget=forms.SelectMultiple())

        self.fields['aircraft_model'] = forms.ModelChoiceField(                
                empty_label=None, 
                queryset=self.aircraft_model_qs)



    def clean(self):        
        
        added_components = self.cleaned_data.get('components')        
        existing_components = self.instance.components        
        for added_component in added_components.all():
            existing_components.add(added_component)
        # check if the assembly is complete
        all_master_components = self.instance.aircraft_model.master_components
        master_component_referenced_list = []
        for master_component in all_master_components.all():
            master_component_referenced = False
            for component in existing_components.all():                
                supplier_part_exists = component.supplier_part
                if component.master_component == master_component:
                    master_component_referenced = True
                    break
                elif supplier_part_exists: 
                    component.supplier_part.manufacturer_part.master_component == master_component
                    master_component_referenced = True
                    break
            master_component_referenced_list.append(master_component_referenced)

        if all(master_component_referenced_list):
            self.instance.status = 2
            self.instance.save()
                

        self.cleaned_data['components'] = existing_components.all()
        
        return self.cleaned_data

    class Meta:
        model = AircraftAssembly
        exclude = ('status',)
        
        help_texts = {
            'components': 'Select from available components',
        }
        
class IncidentCreateForm(forms.ModelForm):
    def __init__(self,aircraft_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.aircraft_qs =  Aircraft.objects.filter(id =aircraft_id)
        aircraft =  Aircraft.objects.get(id =aircraft_id)
        aircraft_assembly = aircraft.final_assembly
        # The components that have not been selected
        self.impacted_components_qs = aircraft_assembly.components
                     
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("aircraft"),            
                        Field("impacted_components",css_class="full-length", help_text='Select the components impacted in this incident, you can select multiple.'),                        
                        FloatingField("notes"),
                        FloatingField("new_status"),                        
                        FloatingField("event_datetime"),
                        ), 
                        always_open=True                   
                    ),
                    HTML("""
                            <br>
                        """),
                                    
                    ButtonHolder(
                                Submit('submit', '+ Add Incident'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'incidents-list' %}" role="button">Cancel</a>""")
                    )
                )  

        self.fields['aircraft'] = forms.ModelChoiceField(
                required=True,                
                empty_label=None,
                queryset=self.aircraft_qs)

        self.fields['impacted_components'] = forms.ModelMultipleChoiceField(
                required=True,
                queryset=self.impacted_components_qs,
                widget=forms.SelectMultiple())
    
    def clean(self):
        
        impacted_components = self.cleaned_data.get('impacted_components', None)
        aircraft = self.cleaned_data.get('aircraft')
        new_status = self.cleaned_data.get('new_status', 50)

        aircraft.status = 0
        aircraft.save()
        if impacted_components:
            for component in impacted_components.all():
                component.status = new_status
                component.save()

        return self.cleaned_data

    class Meta:
        model = Incident
        fields = '__all__'
        
        widgets = {            
            'event_datetime': forms.DateTimeInput( attrs={'class':'form-control', 'placeholder':'Select a date / time', 'type':'datetime-local'}),
            'impacted_components': forms.CheckboxSelectMultiple( attrs={'class':'form-control'})
        }
        

class AircraftMasterComponentCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        FloatingField("family"),
                        FloatingField("drawing"),
                        ),
                  
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft Master Component'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-master-components-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     

    class Meta:
        model = AircraftMasterComponent
        fields = '__all__'

class AircraftModelCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        FloatingField("popular_name"),
                        FloatingField("category"),
                        FloatingField("series"),
                        FloatingField("sub_category"),
                        ),
                    AccordionGroup("Model Details",
                       
                        FloatingField("max_endurance"),
                        FloatingField("max_range"),
                        FloatingField("max_speed"),
                        FloatingField("dimension_length"),
                        FloatingField("dimension_breadth"),
                        FloatingField("dimension_height"),
                        FloatingField("operating_frequency"),
                        FloatingField("type_certificate"),
                        FloatingField("max_certified_takeoff_weight"),
                        FloatingField("max_height_attainable"),
                        FloatingField("icao_aircraft_type_designator"),
                        ),
                    AccordionGroup("Master Components",
                        Field("master_components"),
                        ),
                    AccordionGroup("Documents",
                        Field("documents"),
                        ),
                HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Aircraft Model'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-models-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     

    def clean(self):
        """
        Checks that all the words belong to the sentence's language.
        """
        master_components = self.cleaned_data.get('master_components')
        components_that_have_assembly = []
        assemblies_are_ok = False
        for master_component in master_components:
            if master_component.assembly: 
                components_that_have_assembly.append(master_component)
        relevant_assemblies = []
        if components_that_have_assembly:
            # all the assemblies that have this component
            r_a = MasterComponentAssembly.objects.filter(assembly_components__in = components_that_have_assembly).distinct()
            for r in r_a:
                relevant_assemblies.append(r)
            
            for sub_assembly in relevant_assemblies:
                assembly_components = sub_assembly.assembly_components

                for assembly_component in assembly_components.all():
                    if assembly_component not in master_components:
                        assemblies_are_ok = False
                        break

    
        if not assemblies_are_ok:
            raise ValidationError("You have components selected that are part of an assembly, however that assembly is incomplete")
        return self.cleaned_data
    class Meta:
        model = AircraftModel
        fields = '__all__'

class CompanyCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("full_name"),
                        FloatingField("common_name"),
                        FloatingField("email"),
                        FloatingField("website"),
                        FloatingField("phone_number"),
                        FloatingField("company_number"),
                        FloatingField("address"),
                        
                        FloatingField("role"),
                        FloatingField("country"),
                        FloatingField("documents"),
                        FloatingField("vat_number"),
                        FloatingField("insurance_number"),
                        ),
                    # AccordionGroup("Optional Information",
                    #     FloatingField("documents"),
                    #     FloatingField("vat_number"),
                    #     FloatingField("insurance_number"),
                    #     ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Company'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'companies-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    class Meta:
        model = Company
        fields =('full_name','common_name', 'email','website','address','role','country', 'phone_number','documents','vat_number','insurance_number','company_number','role')

class FirmwareCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("binary_file_url"),
                        FloatingField("binary_file_hash"),
                        FloatingField("version"),
                        FloatingField("manufacturer"),
                        FloatingField("friendly_name"),
                        "is_active",
                        ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Firmware'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'firmwares-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )
   
        

    class Meta:
        model = Firmware
        fields = '__all__'

class FlightPlanCreateForm(forms.ModelForm):   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        "geo_json",
                        ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Flight Plan'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'flightplans-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )

    def clean_geo_json(self):
        gj = self.cleaned_data.get('geo_json', False)  
        
        try:
            parsed_geojson = geojson.loads(json.dumps(gj))
        except Exception as ve:      
            raise ValidationError(_("Not a valid GeoJSON, please enter a valid GeoJSON object %s "% ve))
        try:            
            assert parsed_geojson.is_valid
        except AssertionError as ae:             
            raise ValidationError(_("Not a valid GeoJSON, please enter a valid GeoJSON object %s" % ae))
        except AttributeError as atr_e:             
            raise ValidationError(_("Valid GeoJSON not provided"))
        else:
            return gj

        
    class Meta:
        model = FlightPlan
        exclude = ('is_editable','plan_file_json',)
        

class FlightPermissionCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(FlightPermissionCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operation"),
                        FloatingField("status_code"),
                        FloatingField('token'),
                        FloatingField('geo_cage')
                        ),
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Permission'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'flightpermissions-list' %}" role="button">Cancel</a>""")
                    )
                )     
        
    class Meta:
        model = FlightPermission
        fields = '__all__'
        # fields = ('operation','status_code')
    

class FlightLogCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (FlightLogCreateForm,self ).__init__(*args,**kwargs) # populates the post        
        self.fields['operation'].queryset = FlightOperation.objects.filter(is_editable=True)

        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operation"),
                        FloatingField("raw_log"),
                        ),
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Log'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'flightlogs-list' %}" role="button">Cancel</a>""")
                    )
                )     
        
     
    class Meta:
        model = FlightLog
        fields = ('operation','raw_log',)
        

class FlightOperationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super (FlightOperationCreateForm,self ).__init__(*args,**kwargs) # populates the post        
        self.fields['flight_plan'].queryset = FlightPlan.objects.filter(is_editable=True)

        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        FloatingField("drone"),
                        FloatingField("flight_plan"),
                        FloatingField("purpose"),
                        FloatingField("operator"),
                        FloatingField("pilot"),
                        "start_datetime",
                        "end_datetime",
                        ),
                    AccordionGroup("Optional Information",
                        FloatingField("type_of_operation")                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Operation'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'flightoperations-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )
     
    
    def clean(self):
        cleaned_data = super().clean()
        s_date = cleaned_data.get("start_datetime")
        e_date = cleaned_data.get("end_datetime")
        start_date = arrow.get(s_date)
        end_date = arrow.get(e_date)
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.")

    class Meta:
        model = FlightOperation
        exclude = ('is_editable','created_at',)
        widgets = {            
            'start_datetime': forms.DateTimeInput( attrs={'class':'form-control', 'placeholder':'Select a date / time', 'type':'datetime-local'}),
            'end_datetime': forms.DateTimeInput( attrs={'class':'form-control', 'placeholder':'Select a date / time ', 'type':'datetime-local'}),
        }
        help_texts = {
            'flight_plan': 'If a flight log is signed and is associated with a plan, that plan will not show here',
        }

class ContactCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operator"),
                        FloatingField("person"),
                        FloatingField("address"),
                        FloatingField("role_type")
                        ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Contact'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'contacts-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )

    
    class Meta:
        model = Contact
        fields = '__all__'


class PilotCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("operator"),
                        FloatingField("person"),
                        # "photo",
                        FloatingField("photo"),
                        # FloatingField("identification_photo"),
                        FloatingField("documents"),
                        FloatingField("tests"),
                        FloatingField("address"),
                        "is_active",
                        ),
                        
                    # AccordionGroup("Optional Information",
                    #     FloatingField("photo"),
                    #     FloatingField("identification_photo"),
                    #     FloatingField("tests"),
                    #     ),                                 
                    ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Pilot'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'pilots-list' %}" role="button">Cancel</a>""")
                    )
                )     
        
    
    class Meta:
        model = Pilot
        fields = '__all__'

# class DigitalSkyLogCreateForm(forms.ModelForm):
#     class Meta:
#         model = DigitalSkyLog
#         fields = '__all__'

# class DigitalSkyTransactionCreateForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = '__all__'

class AuthorizationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("title"),
                        FloatingField("operation_max_height"),
                        FloatingField("operation_altitude_system"),
                        FloatingField("airspace_type"),
                        FloatingField("operation_area_type"),
                        FloatingField("risk_type"),
                        FloatingField("authorization_type"),
                        "permit_to_fly_above_crowd",
                        ),                   
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Activity'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'activities-list' %}" role="button">Cancel</a>""")
                    )
                )     
    class Meta:
        model = Authorization
        # exclude = ('is_created',)
        fields = '__all__'
        
class ActivityCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        'activity_type'
                        ),                   
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Activity'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'activities-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    class Meta:
        model = Activity
        # exclude = ('is_created',)
        fields = '__all__'
        
class TokenCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup("Mandatory Information",
                        FloatingField("name"),
                        FloatingField("token_type"),
                        FloatingField("extension"),
                        FloatingField("association"),
                        "credential"
                    ),
                    AccordionGroup("Optional Information",
                        FloatingField("aircraft"),
                        FloatingField("manufacturer"),
                        FloatingField("operator"),
                        'is_active'
                        ),                   
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', '+ Add Credentials'),
                                HTML("""<a class="btn btn-secondary" href="{% url 'credentials-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    credential = forms.CharField(widget=forms.Textarea, help_text="Paste the credential as plain text here")
    class Meta:
        model = AerobridgeCredential
        # fields = '__all__'
        exclude = ('token',)
        
        
        
class CustomCloudFileCreateForm(forms.Form):
    
    UPLOAD_TYPE = (
        ('logs', 'Logs'),
        ('documents', 'Documents'),
        ('receipts', 'Receipts'),
        ('invoices', 'Invoices'),
        ('other', 'Other'),
    )
    file = forms.FileField()
    file_type = forms.CharField(max_length=140,widget=forms.Select(choices=UPLOAD_TYPE))
    name = forms.CharField()
        
class CutsomTokenCreateForm(forms.Form):
    name = forms.CharField(max_length=100)
    token_type = forms.IntegerField(widget=forms.Select(choices=TOKEN_TYPE),
    )
    association = forms.IntegerField(widget=forms.Select(choices=KEY_ENVIRONMENT),
    )
    token = forms.CharField(widget = forms.TextInput())