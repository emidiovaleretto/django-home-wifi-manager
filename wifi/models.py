from io import BytesIO

from django.db import models
from django.core.files.base import ContentFile

import wifi_qrcode_generator


class Network(models.Model):
  name = models.CharField(max_length=100)
  password = models.CharField(max_length=50, blank=True, null=True)
  qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    if not self.qr_code:
      qr_code = wifi_qrcode_generator.generator.wifi_qrcode(
          ssid=self.name, 
          hidden=False, 
          authentication_type='WPA', 
          password=self.password,
      )
      fname = f'qr_code-{self.name}.png'
      buffer = BytesIO()
      qr_code.make_image().save(buffer, 'PNG')
      self.qr_code = ContentFile(buffer.getvalue(), fname)

    super().save(*args, **kwargs)