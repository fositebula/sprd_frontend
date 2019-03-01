from . import models

from django.contrib import admin
from django.conf import settings

from squad.sprd_frontend.tasks import update_pac_node

admin_site_name = '%s administration' % settings.SITE_NAME
admin.site.site_title = admin_site_name
admin.site.site_header = admin_site_name



def update_pac_nodes(modeladmin, request, queryset):
    for device_type in queryset:
        update_pac_node.delay(device_type.id)


update_pac_nodes.short_description = "update pac nodes"
class DeviceTypeAdmin(admin.ModelAdmin):
    """
    Handles global tokens, i.e. tokens that are not projec-specific.
    """
    model = models.DeviceType
    fields = ['name', 'pac_node', 'backend', 'project', 'env', 'slug', 'base_pac_url']
    list_display = ['name', 'backend', 'project', 'env', 'slug',]
    actions = [update_pac_nodes]

class VtsVersionAdmin(admin.ModelAdmin):
    """
    Handles global tokens, i.e. tokens that are not projec-specific.
    """
    model = models.VtsVersion
    fields = ['name', 'vts_bar_url', 'description', 'user']
    list_display = ['name', 'user']


class VtsModelAdmin(admin.ModelAdmin):
    """
    Handles global tokens, i.e. tokens that are not projec-specific.
    """
    model = models.VtsModel
    fields = ['name', 'options', 'description', 'test_definition']
    list_display = ['name']

class TestDefinitionAdmin(admin.ModelAdmin):
    """
    Handles global tokens, i.e. tokens that are not projec-specific.
    """
    model = models.TestDefinition
    fields = ['name', 'content', 'description', 'actions', 'user']
    list_display = ['name', 'user']


admin.site.register(models.DeviceType, DeviceTypeAdmin)
admin.site.register(models.VtsVersion, VtsVersionAdmin)
admin.site.register(models.VtsModel, VtsModelAdmin)
admin.site.register(models.TestDefinition, TestDefinitionAdmin)
