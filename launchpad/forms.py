
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
# from .models import Person

KEY_ENVIRONMENT = ((0, _('DIGITAL SKY OPERATOR')),(1, _('DIGITAL SKY MANUFACTURER')),(2, _('DIGITAL SKY PILOT')),(3, _('RFM')),(4, _('OTHER')),)
TOKEN_TYPE= ((0, _('PUBLIC_KEY')),(1, _('PRIVATE_KEY')),(2, _('AUTHENTICATION TOKEN')),(3, _('RFM KEY')),(4, _('OTHER')),)

# books/forms.py


# class PersonCreateForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.help_text_inline = True   
        
#         self.helper.layout = Layout(
#                 BS5Accordion(
#                     AccordionGroup("Mandatory Information",
#                         FloatingField("first_name"),
#                         FloatingField("middle_name"),
#                         FloatingField("last_name"),
#                         FloatingField("email"),
#                         FloatingField("phone_number"),
#                         FloatingField("country"),
#                         ),
#                     AccordionGroup("Optional Information",
#                         FloatingField("documents"),                        
#                         FloatingField("date_of_birth")
#                         ),                                 
#                     ),
#                     HTML("""
#                             <br>
#                         """),
#                     ButtonHolder(
#                                 Submit('submit', '+ Add Person'),
#                                 HTML("""<a class="btn btn-secondary" href="{% url 'people-list' %}" role="button">Cancel</a>""")
#                     )
#                 )     

#     class Meta:
#         model = Person
#         fields = '__all__'


#################################################################################################
# class PersonCreateForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.help_text_inline = True   
        
#         self.helper.layout = Layout(
#                 BS5Accordion(
#                     AccordionGroup("Mandatory Information",
#                         FloatingField("first_name"),
#                         FloatingField("middle_name"),
#                         FloatingField("last_name"),
#                         FloatingField("email"),
#                         FloatingField("phone_number"),
#                         FloatingField("country"),
#                         ),
#                     AccordionGroup("Optional Information",
#                         FloatingField("documents"),                        
#                         FloatingField("date_of_birth")
#                         ),                                 
#                     ),
#                     HTML("""
#                             <br>
#                         """),
#                     ButtonHolder(
#                                 Submit('submit', '+ Add Person'),
#                                 HTML("""<a class="btn btn-secondary" href="{% url 'people-list' %}" role="button">Cancel</a>""")
#                     )
#                 )     

#     class Meta:
#         model = Person
#         fields = '__all__'
###########################################
# Define your custom FloatingField
# Define your custom FloatingField2
class PersonCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
            BS5Accordion(
                AccordionGroup(_("Mandatory Information"),  # Translate the accordion group title
                    Field("first_name"),
                    Field("middle_name"),
                    Field("last_name"),
                    Field("email"),
                    Field("phone_number"),
                    Field("country"),
                ),
                
                AccordionGroup(_("Optional Information"),  # Translate the accordion group title
                    Field("documents"),                        
                    Field("date_of_birth")
                ),                                 
            ),
            HTML("""
                <br>
            """),
            ButtonHolder(
                Submit('submit', _('+ Add Person')),  # Translate the submit button text
                HTML("""<a class="btn btn-secondary" href="{% url 'people-list' %}" role="button">Cancel</a>""")  # Translate the cancel button text
            )
        )     

    class Meta:
        model = Person
        fields = '__all__'
        labels = {
            'first_name': _('First Name'),
            'middle_name': _('Middle Name'),
            'last_name': _('Last Name'),
            'email': _('Email'),
            'phone_number': _('Phone Number'),
            'country': _('Country'),
            'documents': _('Documents'),
            'date_of_birth': _('Date of Birth'),
        }
        help_texts = {
        'first_name': _('The first name of the person added to the database'),
        'email': _('Associate an email address with the person, this field is required"'),
        'phone_number': _('Associate a phone number of the person.'),
        'date_of_birth': _('Assign a date of birth to this person'),
    }
              
class AddressCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("address_line_1"),
                        Field("address_line_2"),
                        Field("address_line_3"),
                        Field("postcode"),                        
                        Field("city"),
                        Field("state"),
                        Field("country"),
                        ),                                
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit',_('+ Add Address')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'addresses-list' %}" role="button">Cancel</a>""")
                    )
                )     

    class Meta:
        model = Address
        fields = '__all__'
        labels = {
            'address_line_1': _('Address Line 1'),
            'address_line_2': _('Address Line 2'),
            'address_line_3': _('Address Line 3'),
            'postcode': _('Post code'),
            'city': _('City'),
            'state': _('State'),
            'country': _('Country'),
        }
        help_texts = {
        'city': _('Set a city of this address'),
        'state': _('Pick a state'),
            }
        

class OperatorCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        self.fields['company'].queryset = Company.objects.filter(role = 2)
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("company"),
                        Field("website"),
                        Field("email"),
                        Field("phone_number"),
                        Field("operator_type"),
                        Field("address"),
                        ),
                    AccordionGroup(_("Optional Information"),
                        Field("operational_authorizations"),
                        Field("authorized_activities"),
                        Field("insurance_number"),
                        Field("company_number"),
                        Field("vat_number"),
                        Field("country"),
                        ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Operator')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'operators-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    class Meta:
        model = Operator
        fields = '__all__'
        labels = {
            'company': _('Company'),
            'operator_type': _('Operator Type'),
            'operational_authorizations': _('Operational authorizations'),
            'authorized_activities': _('Company Number'),
        }
        help_texts = {
        'company': _('Specify the company associated with this operator'),
        'operator_type': _('Choose what kind of operator this is, classify the operator based on capabilites, use the adminsitration panel to add additional operator categories'),
        'operational_authorizations': _('Choose what kind of authorization this operator posseses, to add additional authorizations, use the administration panel'),
        'authorized_activities': _('Related to Authorization, select the kind of activities that this operator is allowed to conduct, you can add additional activities using the administration panel'),
            }

class AircraftCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("operator"),
                        Field("manufacturer"),
                        Field("final_assembly"),                        
                        Field("flight_controller_id"),
                        Field("status"),
                        Field("photo"),
                        Field("name")
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Aircraft')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircrafts-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     
        self.fields['final_assembly'].queryset = AircraftAssembly.objects.filter(~Exists(Aircraft.objects.filter(final_assembly=OuterRef('pk')))).filter(status=2)

    class Meta:
        model = Aircraft
        fields = ('operator','manufacturer', 'name','flight_controller_id', 'final_assembly','status','photo',)
        labels = {
            'operator': _('Operator'),
            'manufacturer': _('Manufacturer'),
            'final_assembly': _('Final assembly'),
            'flight_controller_id': _('Flight controller id'),
            'status': _('Photo'),
            'photo': _('Photo'),
            'name': _('Name'),
            
        }
        help_texts = {
        'operator': _('Associate a operator company with this Aircraft'),
        'manufacturer': _('Associate a manufacturer in the database to this aircraft'),
        'final_assembly': _('Assign a aircraft assembly to this aircraft, if you do not see a assembly, it means that you will need to create a new assembly first'),
        'flight_controller_id': _('This is the Drone ID from the RFM, if there are spaces in the ID, remove them '),
        'status': _('Set the status of this drone, if it is set as inactive, the GCS might fail and flight plans might not be able to load on the drone'),
        'photo': _('A URL of a photo of the drone'),
        'name': _('Set the internal name of the aircraft e.g. F1 #2'),
    }

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
                    AccordionGroup(_("Mandatory Information"),
                        Field("name"),
                        Field("family"),
                        Field("drawing"),
                        ),
                  
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Aircraft Master Component')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'aircraft-master-components-list' %}" role="button">Cancel</a>""")
                    )
                )
        )     

    class Meta:
        model = AircraftMasterComponent
        fields = ['name','family','drawing']
        labels = {
            'name': _('Name'),
            'family': _('Family'),
            'drawing': _('Drawing'),
        }
    help_texts = {
            'family': _('Set the component family'),
            'drawing': _('A URL to a photo of the component drawing.'),
        }
class AircraftModelCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("name"),
                        Field("popular_name"),
                        Field("category"),
                        Field("series"),
                        Field("sub_category"),
                        ),
                    AccordionGroup(_("Model Details"),
                       
                        Field("max_endurance"),
                        Field("max_range"),
                        Field("max_speed"),
                        Field("dimension_length"),
                        Field("dimension_breadth"),
                        Field("dimension_height"),
                        Field("operating_frequency"),
                        Field("type_certificate"),
                        Field("max_certified_takeoff_weight"),
                        Field("max_height_attainable"),
                        Field("icao_aircraft_type_designator"),
                        ),
                    AccordionGroup(_("Master Components"),
                        Field("master_components"),
                        ),
                    AccordionGroup(_("Documents"),
                        Field("documents"),
                        ),
                HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Aircraft Model')),
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
        labels = {
            'name': _('Name'),
            'popular_name': _('Popular name'),
            'category': _('Category'),
            'series': _('Series'),
            'sub_category': _('Sub category'),
            'max_endurance': _('Max endurance'),
            'max_range': _('Max range'),
            'max_speed': _('Max speed'),
            'dimension_length': _('Dimension length'),
            'dimension_height': _('Dimension height'),
            'operating_frequency': _('Operating frequency'),
            'type_certificate': _('Type certificate'),
            'max_certified_takeoff_weight': _('Max certified takeoff weight'),
            'max_height_attainable': _('Max height attainable'),
            'icao_aircraft_type_designator': _('Icao aircraft type designator'),
            'master_components': _('Master_components'),
            'documents': _('documents'),    
        }
        help_texts = {
            'name': _('Give this model a full name you can remember e.g. Aerobridge F1'),
            'popular_name': _('Give this e.g. F1'),
            'category': _('Set the category for this aircraft, use the closest aircraft type'),
            'series': _('Define the production series for this Aircraft Model e.g. 2022.1'),
            'max_endurance': _('Set the flight endurance of this model in minutes'),
            'max_range': _('Set the flight range of this model in kms.'),
            'max_speed': _('Set the maximum flight speed in km/hr'),
            'dimension_length': _('Set the maximum length of the drone in cms'),
            'dimension_height': _('Set the maximum breadth of the drone in cms'),
            'operating_frequency': _('Set the maximum height of the drone in cms'),
            'type_certificate': _('Set the type certificate if available for the drone'),
            'max_certified_takeoff_weight': _('Set the takeoff weight for the aircraft in gms.'),
            'max_height_attainable': _('Set the max attainable height in meters'),
            'icao_aircraft_type_designator': _('If available you can specify the type designator, see https://www.icao.int/publications/doc8643/pages/search.aspx'),
            'documents': _('Associate any existing documents to this series / model'),
        }

class CompanyCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("full_name"),
                        Field("common_name"),
                        Field("email"),
                        Field("website"),
                        Field("phone_number"),
                        Field("company_number"),
                        Field("address"),
                        
                        Field("role"),
                        Field("country"),
                        Field("documents"),
                        Field("vat_number"),
                        Field("insurance_number"),
                        ),
                    AccordionGroup(_("Optional Information"),
                        Field("documents"),
                        Field("vat_number"),
                        Field("insurance_number"),
                        ),                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Company')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'companies-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    class Meta:
        model = Company
        fields =('full_name','common_name', 'email','website','address','role','country', 'phone_number','documents','vat_number','insurance_number','company_number','role')

        labels = {
            'full_name': _('Full name'),
            'common_name': _('Common name'),
            'email': _('Email'),
            'website': _('WebSite'),
            'phone_number': _('Phone number'),       
            'company_number': _('Company number'),
            'address': _('Address'),
            'role': _('Role'),
            'country': _('Country'),
            'documents' :_('Documents'),
            'vat_number': _('Vat number') ,      
            'insurance_number': _('Insurance number'),
        }

        help_texts ={
            'full_name':_('Full legal name of the manufacturing entity'),
            'common_name': _('Common name for the manufacturer e.g. Skydio'),
            'email': _('Contact email for support and other queries'),
            'website': _('Put official URL of the company, if none is available then a manufacturers public facing URL is necessary'),
            'company_number': _('Company number if available'),
            'country': _('At the moment only India is configured, you can setup your own country'),
            'role': _('Set the type of the company'),
            'address': _('Assign a address to this manufacturers'),
            'documents': _('You can upload and associate documents to the manufacturer'),
            'vat_number': _('VAT / Tax number if available'),
            'insurance_number': _('Insurance number if avaialble'),
        }


class FirmwareCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("binary_file_url"),
                        Field("binary_file_hash"),
                        Field("version"),
                        Field("manufacturer"),
                        Field("friendly_name"),
                        "is_active",
                        ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Firmware')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'firmwares-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )
   
        

    class Meta:
        model = Firmware
        fields = '__all__'

        ######
        labels = {
             'binary_file_url': _('Binary file url'),
             'binary_file_hash': _('Binary file hash'),
             'version': _('Version'),
             'manufacturer': _('Manufacturer'),
             'friendly_name': _('Friendly name'),
             'is_active': _('Is active'),

        }

        help_texts = {
            'binary_file_url': _('Enter a url from where the firmware can be downloaded'),
            'binary_file_hash': _ ('Enter a SHA / Digest for the firmware, used to secure the firmware'),
            'version': _('Set a semantic version for the firmware version'),
            'manufacturer': _('Associate a manufacturer to the firmware'),
            'friendly_name': _('Give it a friendly name e.g. May-2021 1.2 release'),
            'is_active': _('Set if the firmware is active, dont forget to mark old firmware as inactive'),

        }


class FlightPlanCreateForm(forms.ModelForm):   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("name"),
                        Field("geo_json"),
                        ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Flight Plan')),
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

        labels = {
            'name': _('Name'),
            'geo_json': _('Geo json'),
        }

        help_texts = {
            'name': _('Give this flight plan a friendly name'),
            'geo_json': _('Paste the flight plan as GeoJSON'),
        }


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
                    AccordionGroup(_("Mandatory Information"),
                        Field("operation"),
                        Field("raw_log"),
                        ),
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Log')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'flightlogs-list' %}" role="button">Cancel</a>""")
                    )
                )     
        
     
    class Meta:
        model = FlightLog
        fields = ('operation','raw_log',)
        labels = {
            'operation': _('Operation'),
            'raw_log': _('Raw log'),
        }
        

class FlightOperationCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super (FlightOperationCreateForm,self ).__init__(*args,**kwargs) # populates the post        
        self.fields['flight_plan'].queryset = FlightPlan.objects.filter(is_editable=True)

        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("name"),
                        Field("drone"),
                        Field("flight_plan"),
                        Field("purpose"),
                        Field("operator"),
                        Field("pilot"),
                        Field("start_datetime"),
                        Field("end_datetime"),
                        ),
                    AccordionGroup(_("Optional Information"),
                        Field("type_of_operation")                                 
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Operation')),
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
            'name': _('Give a friendly name for this operation'),
            'drone': _('Pick the drone that will be used to fly this opreation'),
            'flight_plan': _('If a flight log is signed and is associated with a plan, that plan will not show here'),
             'purpose': _('To add additional categories, please add entries to the Activities table'),
            'operator': _('Assign a operator for this operaiton'),
             'end_datetime': _('Specify Flight end date and time in Indian Standard Time (IST)'),
             'type_of_operation': _('At the moment, only VLOS and BVLOS operations are supported, for other types of operations, please issue a pull-request'),
             
        }
        labels = {
            'name': _('Name'),
            'drone': _('Drone'),
            'flight_plan': _('Flightplan'),
            'purpose': _('Purpose'),
            'operator': _('Operator'),
            'pilot': _('Pilot'),
            'start_datetime': _('Start Date Time'),
            'end_datetime': _('End Date Time'),
            'type_of_operation': _('Type of operation'),
            
        }

class ContactCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("operator"),
                        Field("person"),
                        Field("address"),
                        Field("role_type")
                        ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Contact')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'contacts-list' %}" role="button">Cancel</a>""")
                    )
                )     
        )
    class Meta:
        model = Contact
        fields = ['operator','person','address','role_type']
        labels = {
            'operator': _('Operator'),
            'person': _('Person'),
            'address': _('Address'),
            'role_type': _('Role type'),
        }
        help_texts = {
        'operator': _('Set a operator for this contact'),
        'person': _('Associat a person for this contact'),
        'address': _('Add a address for this contact'),
        'role_type': _('A contact may or may not be legally responsible officer within a company, specify if the contact is responsible(legally) for opration in the company '),
    }


class PilotCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("operator"),
                        Field("person"),
                        # Field("photo"),
                        # Field("photo"),
                        # Field("identification_photo"),
                        Field("documents"),
                        Field("tests"),
                        Field("address"),
                        Field("is_active"),
                        ),
                        
                    AccordionGroup(_("Optional Information"),
                        Field("photo"),
                        Field("identification_photo"),
                        Field("tests"),
                        ),                                 
                    ),
                    
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Pilot')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'pilots-list' %}" role="button">Cancel</a>""")
                    )
                )     
        
    
    class Meta:
        model = Pilot
        fields = '__all__'

        labels = {
                    'operator': _('First Name'),
                    'person': _('Person*'),
                    'tests': _('Tests'),
                    'address': _('Address'),
                    'photo': _('Photo'),
                    'is_active': ('Is active'),
                    'documents': _('Documents'),
                   
                }
        help_texts = {
                        'photo': _('A URL to link to a photo of the pilot'),
                        'is_active': _('Is this pilot active? If he is not working for the company or has moved on, set it as inactive'),
                        'address': _('Assign a address to this Pilot'),
                        'tests': _('Specify the tests if any the pilot has taken'),
                        'person': _('Assign this pilot to a person object in the database'),
                       'operator': _('Assign this pilot to a operator'),
                    }

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
                    AccordionGroup(_("Mandatory Information"),
                        Field("title"),
                        Field("operation_max_height"),
                        Field("operation_altitude_system"),
                        Field("airspace_type"),
                        Field("operation_area_type"),
                        Field("risk_type"),
                        Field("authorization_type"),
                        Field("permit_to_fly_above_crowd"),
                        ),                   
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Activity')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'activities-list' %}" role="button">Cancel</a>""")
                    )
                )     
    class Meta:
        model = Authorization
        # exclude = ('is_created',)
        fields = '__all__'
        labels = {
            'title': _('Title'),
            'operation_max_height': _('Operation max height'),
            'operation_altitude_system': _('Operation altitude system'),
            'airspace_type': _('Airspace type'),
            'operation_area_type': _('Operation area type'),
            'risk_type': _('Risk type'),
            'authorization_type': _('Authorization type'),
            'permit_to_fly_above_crowd': _('Permit to fly above crowd '),
        }
        help_texts = {
        'operation_max_height': _('Specify the company associated with this operator'),
        'operation_altitude_system': _('Choose what kind of operator this is, classify the operator based on capabilites, use the adminsitration panel to add additional operator categories'),
        'airspace_type': _('Set the airspace type, if available'),
        'operation_area_type': _('Can the operator fly over crowds? '),
        'risk_type': _('If available, set the airspace risk type'),
        'authorization_type': _('Set the type of the authorization'),
        'permit_to_fly_above_crowd': _('Select if the company is permitted to fly above crowd'),
          
            }
     
class ActivityCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("name"),
                        Field('activity_type')
                        ),                   
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit',_('+ Add Activity')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'activities-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    class Meta:
        model = Activity
        # exclude = ('is_created',)
        fields = '__all__'
        labels = {
            'name': _('Name'),
            'activity_type': _('Activity Type'),
        }
        help_texts = {
        'name': _('Set a name for this activity'),
        'activity_type': _('Set the activity type and the airspace'),
    }
        
        
class TokenCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.help_text_inline = True   
        
        self.helper.layout = Layout(
                BS5Accordion(
                    AccordionGroup(_("Mandatory Information"),
                        Field("name"),
                        Field("token_type"),
                        Field("extension"),
                        Field("association"),
                        Field("credential"),
                    ),
                    AccordionGroup(_("Optional Information"),
                        Field("aircraft"),
                        Field("manufacturer"),
                        Field("operator"),
                        'is_active'
                        ),                   
                    ),
                    HTML("""
                            <br>
                        """),
                    ButtonHolder(
                                Submit('submit', _('+ Add Credentials')),
                                HTML("""<a class="btn btn-secondary" href="{% url 'credentials-list' %}" role="button">Cancel</a>""")
                    )
                )     
     
    credential = forms.CharField(widget=forms.Textarea, help_text="Paste the credential as plain text here")
    class Meta:
        model = AerobridgeCredential
        # fields = 'all'
        exclude = ('token',)
        labels = {
            'name': _('Name'),
            'token_type': _('Token typeDrone'),
            'extension': _('Extension'),
            'association': _('Association'),
            'credential': _('Credential'),
            'aircraft': _('Aircraft'),
            'manufacturer': _('Manufacturer'),
            'operator': _('Operator'),
            'is_active': _('Is active'),
        }
        help_texts = {
            'name': _('Give a friendly name for this operation'),
            'token_type': _('Pick the drone that will be used to fly this opreation'),
           ' extension': _('Specify the data format for this credential, if known'),
            'association': _('If a flight log is signed and is associated with a plan, that plan will not show here'),
            'credential': _('Paste the credential as plain text here'),
            'operator': _('Assign a operator for this operaiton'),
            'is_active': _(' Set whether the credential is still active'),
        
        }
        
        
class CustomCloudFileCreateForm(forms.Form):
    
    UPLOAD_TYPE = (
        ('logs', _('Logs')),
        ('documents', _('Documents')),
        ('receipts', _('Receipts')),
        ('invoices', _('Invoices')),
        ('other', _('Other')),
    )
    file = forms.FileField()
    file_type = forms.CharField(max_length=140,widget=forms.Select(choices=UPLOAD_TYPE))
    name = forms.CharField()

    labels = {
            'file': _('File'),
            'file_type': _('File type'),
            'name': _('Name'),
        }
        
    file = forms.FileField(label=_('File'))
    file_type = forms.CharField(max_length=140, label=_('File type'), widget=forms.Select(choices=UPLOAD_TYPE))
    name = forms.CharField(label=_('Name'))

        
class CutsomTokenCreateForm(forms.Form):
    name = forms.CharField(max_length=100)
    token_type = forms.IntegerField(widget=forms.Select(choices=TOKEN_TYPE),
    )
    association = forms.IntegerField(widget=forms.Select(choices=KEY_ENVIRONMENT),
    )
    token = forms.CharField(widget = forms.TextInput())