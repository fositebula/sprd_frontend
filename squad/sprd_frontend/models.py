from django.db import models
from django.contrib.auth.models import User

from squad.core.models import Project, Environment
from squad.ci.models import Backend

class DisplayName(object):
    @property
    def displayname(self):
        return self.name


class TestDefinition(models.Model, DisplayName):
    name = models.CharField(default='', max_length=16)
    content = models.TextField(default='', null=True, blank=True)
    description = models.CharField(default='', max_length=256)
    actions = models.TextField(default='', null=True, blank=True)

    user = models.ForeignKey(User)

    def __str__(self):
        return self.name


class VtsVersion(models.Model, DisplayName):
    name = models.CharField(default='', max_length=16)
    vts_bar_url = models.CharField(default='', max_length=128)
    description = models.CharField(default='', max_length=256)

    user = models.ForeignKey(User)
    def __str__(self):
        return self.name

class VtsModel(models.Model, DisplayName):
    name = models.CharField(default='', max_length=64)
    options = models.CharField(default='', max_length=128)
    description = models.CharField(default='', max_length=256)

    test_definition = models.ForeignKey(TestDefinition)
    def __str__(self):
        return self.name


class DeviceType(models.Model, DisplayName):
    name = models.CharField(default='', max_length=64)
    pac_node = models.CharField(default='', max_length=128)
    slug = models.CharField(default='', max_length=64)
    base_pac_url = models.CharField(default='', max_length=128)

    backend = models.ForeignKey(Backend, null=True)
    project = models.ForeignKey(Project, null=True)
    env = models.ForeignKey(Environment, null=True)

    def __str__(self):
        return self.name
