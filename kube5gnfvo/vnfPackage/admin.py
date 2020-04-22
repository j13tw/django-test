from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(VnfPkgInfo)
admin.site.register(VnfPackageArtifactInfo)
admin.site.register(VnfPackageSoftwareImageInfo)
admin.site.register(Checksum)
admin.site.register(VnfPkgInfoLink)
