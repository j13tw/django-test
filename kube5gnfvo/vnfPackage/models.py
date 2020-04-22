from django.db import models
from django_mysql.models import EnumField
import uuid

# Create your models here.
class VnfPkgInfo(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    vnfdId = models.TextField(null=True, blank=True)
    vnfProvider = models.TextField(null=True, blank=True)
    vnfProductName = models.TextField(null=True, blank=True)
    vnfSoftwareVersion = models.TextField(null=True, blank=True)
    vnfdVersion = models.TextField(null=True, blank=True)
    onboardingState = EnumField(choices=["CREATED", "UPLOADING ", "PROCESSING ", "ONBOARDED"], default="CREATED")
    operationalState = EnumField(choices=["ENABLED", "DISABLED"], default="DISABLED") 
    usageState = EnumField(choices=["IN_USE", "NOT_IN_USE"], default="NOT_IN_USE")
    userDefinedData = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "VnfPkgInfo"

    def __str__(self):
        return str(self.id)

class VnfPkgInfoLink(models.Model):
    _links = models.OneToOneField(
        VnfPkgInfo,
        on_delete=models.CASCADE,
        related_name='vnf_package_info_fk_links'
    )
    link_self = models.URLField()
    vnfd = models.URLField(null=True, blank=True)
    packageContent = models.URLField()

    class Meta:
        db_table = "VnfPkgInfoLink"


class VnfPackageSoftwareImageInfo(models.Model):
    vnf_package_info_fk_software_image_info = models.ForeignKey(
        VnfPkgInfo,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='vnf_package_info_fk_software_image_info'
    )
    name = models.TextField()
    provider = models.TextField()
    version = models.TextField()
    containerFormat = EnumField(choices=["AKI", "AMI", "ARI", "BARE", "DOCKER", "OVA", "OVF"], default="DOCKER")
    diskFormat = EnumField(choices=["AKI", "AMI", "ARI", "ISO", "QCOW2", "RAW", "VDI", "VHD", "VHDX", "VMDK"], default="RAW")
    createdAt = models.DateTimeField(auto_now_add=True)
    minDisk = models.PositiveIntegerField()
    minRam = models.PositiveIntegerField()
    size = models.PositiveIntegerField()
    userMetadata = models.TextField(null=True, blank=True)
    imagePath = models.TextField()

    class Meta:
        db_table = "VnfPackageSoftwareImageInfo"

class VnfPackageArtifactInfo(models.Model):
    vnf_package_info_fk_artifact_info = models.ForeignKey(
        VnfPkgInfo,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='vnf_package_info_fk_artifact_info'
    )
    artifactPath = models.TextField(null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "VnfPackageArtifactInfo"

class Checksum(models.Model):
    vnf_package_info_fk_checksum = models.OneToOneField(
        VnfPkgInfo,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='vnf_package_info_fk_checksum'
    )
    vnf_package_software_image_fk_checksum = models.OneToOneField(
        VnfPackageSoftwareImageInfo,
        on_delete=models.CASCADE,
        related_name='vnf_package_software_image_fk_checksum'
    )
    vnf_package_artifact_info_fk_checksum = models.OneToOneField(
        VnfPackageArtifactInfo,
        on_delete=models.CASCADE,
        related_name='vnf_package_artifact_info_fk_checksum'
    )
    algorithm = models.TextField()
    hash = models.TextField()

    class Meta:
        db_table = "Checksum"

