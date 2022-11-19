from pydoc import Doc
from django.contrib import admin
from django.contrib.gis.db import models
from .models import *
from diana.abstract.admin_view import *
import diana.abstract.models
from diana.abstract.models import DEFAULT_EXCLUDE, DEFAULT_FIELDS, get_many_to_many_fields
from django.contrib.gis import admin
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

def get_fields(model: models.Model):

    exclude = DEFAULT_EXCLUDE 
    fields  = [field for field in diana.abstract.models.get_fields(model) if field not in exclude]
    return fields

# Register your models here.
# admin.site.register(Term)
@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = get_fields(Term) + DEFAULT_FIELDS 


@admin.register(DocTerm)
class DocTermAdmin(admin.ModelAdmin):
    list_display = get_fields(DocTerm) + DEFAULT_FIELDS 

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = get_fields(Document) + DEFAULT_FIELDS 

@admin.register(Termsim)
class TermsimAdmin(admin.ModelAdmin):
    list_display = get_fields(Termsim) + DEFAULT_FIELDS 


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = get_fields(Entity) + DEFAULT_FIELDS 

ordering = [
        "Documents",
        "Terms",
        "Document-term relations", 
        "Term similarities",
        "Entities"]

get_apps_order('Norfam', ordering)