from django.db import models
import uuid
from django.db.models.deletion import CASCADE
from django.utils.translation import ugettext_lazy as _
from registry.models import Contact

class DigitalSkyCredentials(models.Model):
    ''' A class to store tokens from Digital Sky '''
    
    KEY_ENVIRONMENT = ((0, _('DIGITAL SKY OPERATOR')),(1, _('DIGITAL SKY MANUFACTURER')),(2, _('DIGITAL SKY PILOT')),(3, _('RFM')),(4, _('RFM')),)
    
    TOKEN_TYPE= ((0, _('PUBLIC_KEY')),(1, _('PRIVATE_KEY')),(2, _('AUTHENTICATION TOKEN')),(3, _('RFM KEY')),(4, _('OTHER')),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    token_type = models.IntegerField(choices=TOKEN_TYPE)
    environment = models.IntegerField(choices=KEY_ENVIRONMENT, default = 4)
    token = models.BinaryField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def token_type_verbose(self):
        return dict(DigitalSkyCredentials.TOKEN_TYPE)[self.token_type]