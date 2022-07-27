import os
import base64
import numpy
from django.conf import settings


class captchaImage:
    def __init__(self):
        self.files = os.listdir(os.path.join(settings.STATICFILES_DIRS[0], 'captchaImage'))
        self.file = numpy.random.choice(self.files)

    def get_base64Image(self):
        with open(os.path.join(os.path.join(settings.STATICFILES_DIRS[0], 'captchaImage'), self.file), 'rb') as f:
            temp_file = f.read()
        b64_byt = base64.b64encode(temp_file)
        b64_str = b64_byt.decode('utf-8')
        return b64_str

    def get_randomImage(self):
        image_value = self.file[:5]
        image = self.get_base64Image()
        return image_value, image
