import os
from rest_framework import serializers
from .models import *
import json

class ChecksumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checksum
        fields = ('algorithm', 'hash')

class VnfPkgInfoLinkSerializer(serializers.ModelSerializer):
    self = serializers.URLField(source='link_self')

    class Meta:
        model = VnfPkgInfoLink
        fields = ('self', 'vnfd', 'packageContent')

class VnfPackageArtifactInfoSerializer(serializers.ModelSerializer):
    checksum = ChecksumSerializer(source='vnf_package_artifact_info_fk_checksum')

    class Meta:
        model = VnfPackageArtifactInfo
        fields = ('checksum', 'artifactPath', 'metadata')

class VnfPackageSoftwareImageInfoSerializer(serializers.ModelSerializer):
    checksum = ChecksumSerializer(source='vnf_package_software_image_fk_checksum')

    class Meta:
        model = VnfPackageSoftwareImageInfo
        fields = ('id', 'name', 'provider', 'version', 'checksum', 'containerFormat', 'diskFormat', 'createdAt', 'minDisk', 'minRam', 'size', 'userMetadata', 'imagePath')

class VnfPkgInfoSerializer(serializers.ModelSerializer):

    checksum = ChecksumSerializer(
        required=False,
        source='vnf_package_info_fk_checksum'
    )
    softwareImages = VnfPackageSoftwareImageInfoSerializer(
        required=False,
        many=True,
        source='vnf_package_info_fk_software_image_info'
    )
    additionalArtifacts = VnfPackageArtifactInfoSerializer(
        required=False,
        many=True,
        source='vnf_package_info_fk_artifact_info'
    )
    _links = VnfPkgInfoLinkSerializer(
        source='vnf_package_info_fk_links'
    )

    class Meta:
        model = VnfPkgInfo
        fields = "__all__"

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        for x in instance:
            if x == 'userDefinedData' and instance[x] != None:
                instance[x] = json.loads(instance[x])
        return instance

    def create(self, validated_data):
        """
        Create and return a new `VnfPfgInfo` instance, given the validated data.
        """
        _links_value = validated_data.pop('vnf_package_info_fk_links')
        vnf_package_info = VnfPkgInfo.objects.create(**validated_data)
        vnf_package_base_path = VnfPkgInfo
        VnfPkgInfoLink.objects.create(
            _links=vnf_package_info,
            **{'link_self': "{}{}".format(_links_value['link_self'], vnf_package_info.id),
            'vnfd': "{}{}/{}".format(_links_value['vnfd'], vnf_package_info.id, "vnfd"),
            'packageContent': "{}{}/{}".format(_links_value['packageContent'], vnf_package_info.id, "package_content")}
        )
        return vnf_package_info

    def update(self, instance, validated_data):
        """
        Update and return an existing `VnfPfgInfo` instance, given the validated data.
        """
        validated_data.pop('')
        instance.vnfdId = validated_data.get('vnfId', instance.vnfdId)
        instance.vnfProvider = validated_data.get('vnfProvider', instance.vnfProvider)
        instance.vnfProductName = validated_data.get('vnfProductName', instance.vnfProductName)
        instance.vnfSoftwareVersion = validated_data.get('vnfSoftwareVersion', instance.vnfSoftwareVersion)
        instance.vnfdVersion = validated_data.get('vnfdVersion', instance.vnfdVersion)
        instance.additionalArtifacts = validated_data.get('title', instance.additionalArtifacts)
        instance.onboardingState = validated_data.get('additionalArtifacts', instance.onboardingState)
        instance.operationalState = validated_data.get('operationalState', instance.operationalState)
        instance.usageState = validated_data.get('usageState', instance.usageState)
        instance.userDefinedData = validated_data.get('userDefinedData', instance.userDefinedData)
        instance.save()


    #     if ['operationalState', 'userDefinedData'] in validated_data:
    #         instance.operationalState = validated_data['operationalState']
    #         instance.userDefinedData = validated_data['userDefinedData']
    #         instance.save()
    #     else:
    #         instance.title = validated_data.get('title', instance.title)
    #         instance.code = validated_data.get('code', instance.code)
    #         instance.linenos = validated_data.get('linenos', instance.linenos)
    #         instance.language = validated_data.get('language', instance.language)
    #         instance.style = validated_data.get('style', instance.style)
    #         instance.save()
        return instance