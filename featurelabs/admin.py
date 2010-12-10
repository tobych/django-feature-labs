from django.contrib import admin

from featurelabs.models import EnabledFeature

class EnabledFeatureAdmin(admin.ModelAdmin):
    list_display = ('feature', 'user')

admin.site.register(EnabledFeature, EnabledFeatureAdmin)
