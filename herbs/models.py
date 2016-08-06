from __future__ import unicode_literals
from future.builtins import str
from future.utils import native

from io import BytesIO
import os
from string import punctuation
from zipfile import ZipFile

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import models
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from mezzanine.conf import settings
from mezzanine.core.fields import FileField
from mezzanine.core.models import Displayable, Orderable, RichText
from mezzanine.pages.models import Page
from mezzanine.utils.importing import import_dotted_path
from mezzanine.utils.models import upload_to


# Set the directory where gallery images are uploaded to,
# either MEDIA_ROOT + 'galleries', or filebrowser's upload
# directory if being used.
GALLERIES_UPLOAD_DIR = "galleries"
if settings.PACKAGE_NAME_FILEBROWSER in settings.INSTALLED_APPS:
	fb_settings = "%s.settings" % settings.PACKAGE_NAME_FILEBROWSER
	try:
		GALLERIES_UPLOAD_DIR = import_dotted_path(fb_settings).DIRECTORY
	except ImportError:
		pass



"""
Page of herbs
"""
class HerbGallery(Page, RichText):

	class Meta:
		verbose_name = _("Herb Gallery")
		verbose_name_plural = _("Herb Galleries")



"""
A single herb
"""
class Herb(Displayable):

	gallery = models.ManyToManyField(HerbGallery, blank=True)
	file = FileField(_("File"), max_length=200, format="Image",
		upload_to=upload_to("herbs.Herb.file", "herbs"), blank=True)
	latin = models.CharField(_("Latin"), max_length=1000, blank=True)
	price_per_oz = models.DecimalField(_("Price Per Oz"), max_digits=9,
		decimal_places=2, blank=True)


	class Meta:
		ordering = ('title',)
		verbose_name = _("Herb")
		verbose_name_plural = _("Herbs")


	def __unicode__(self, *args, **kwargs):
		return self.title


	def get_absolute_url(self):
		return reverse("herb", kwargs={"slug": self.slug})


	def save(self, *args, **kwargs):
		"""
		If no herb name is given when created, create one from the
		file name.
		"""
		if not self.id and not self.title:
			name = force_text(self.file.name)
			name = name.rsplit("/", 1)[-1].rsplit(".", 1)[0]
			name = name.replace("'", "")
			name = "".join([c if c not in punctuation else " " for c in name])
			# str.title() doesn't deal with unicode very well.
			# http://bugs.python.org/issue6412
			name = "".join([s.upper() if i == 0 or name[i - 1] == " " else s
							for i, s in enumerate(name)])
			self.title = name
			
		"""
		TODO: Create a thumbnail for the uploaded file
		"""

		super(Herb, self).save(*args, **kwargs)
