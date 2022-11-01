from django.db import models
from django.utils.translation import gettext_lazy as _
import diana.abstract.models as abstract

# Create your models here.

#Image?
# for the documents that we add, do we need to upload image for them?
# If yes, then why we don't have image attribute in models 

#Is there any tag for the books?

# Do we need to change these classes 


class Term(abstract.AbstractBaseModel):
    """A unique word occurring in documents (type, not token, can be numeric)."""

    term_id = models.AutoField(primary_key=True, verbose_name= _("id"))
    # The word in lowercase
    term_term = models.CharField(max_length=100, verbose_name= _("term"))
    # # Not used?
    term_stem = models.CharField(max_length=100, verbose_name= _("term stem"), blank=True, null=True)
    # # Document frequency, how many documents contain the word at least once
    term_df = models.IntegerField(verbose_name= _("document frequency of term"), blank=True, null=True)
    # # Documents edition
    version = models.IntegerField(verbose_name= _("version"), blank=True, null=True)

    class Meta:
        # managed = False
        unique_together = [['term_term', 'version']]
        verbose_name = _("term")
        verbose_name_plural = _("terms")


class DocTerm(abstract.AbstractBaseModel):
    """Mapping of a certain term in a certain document."""

    doc_term_id = models.AutoField(primary_key=True, verbose_name= _("ID"))
    # The document where it occurs at least once
    doc_id = models.ForeignKey('Document', on_delete=models.CASCADE, db_column='doc_id', related_name='doc_terms', verbose_name= _("document ID"))
    # The term
    term = models.ForeignKey('Term', on_delete=models.CASCADE, db_column='term_id', verbose_name= _("term"))
    # Term frequency, how many times the term occurs in the document
    tf = models.IntegerField(verbose_name= _("term frequency"), blank=True, null=True)
    # # Documents edition
    version = models.IntegerField(verbose_name= _("version"), blank=True, null=True)

    class Meta:
        # managed = False
        verbose_name = _("document-term relation")
        verbose_name_plural = _("document-term relations")


class Document(abstract.AbstractBaseModel):
    """An encyclopedic article on a topic."""

    doc_id = models.AutoField(primary_key=True, verbose_name= _("ID"))
    # The topic, one or a few words
    doc_keyword = models.CharField(max_length=100, verbose_name= _("document keyword"), blank=True, null=True)
    # Full description, may contain HTML tags
    doc_text = models.TextField(verbose_name= _("text"), blank=True, null=True)
    # Truncated description, max ca. 700 chars, possibly no incomplete HTML tags
    doc_abstr = models.CharField(max_length=2048, verbose_name= _("abstract"), blank=True, null=True)
    # Running number unique among documents with same keyword, starting from 0
    doc_suppl = models.IntegerField(verbose_name= _("running document ID"), blank=True, null=True)
    # # Documents edition
    version = models.IntegerField(verbose_name= _("version"), blank=True, null=True)

    class Meta:
        # managed = False
        verbose_name = _("document")
        verbose_name_plural = _("documents")


class Termsim(abstract.AbstractBaseModel):
    """Similarity of two terms.

    Each term pair occurs twice – once in each direction."""

    termsim_id = models.AutoField(primary_key=True, verbose_name= _("ID"))
    # Term one
    target = models.ForeignKey('Term', on_delete=models.CASCADE, db_column='term1_id', related_name='neighbors', verbose_name= _("target"))
    # Term two
    term = models.ForeignKey('Term', on_delete=models.CASCADE, db_column='term2_id', verbose_name= _("term"))
    # Similarity between 0 and 1
    similarity = models.FloatField(verbose_name= _("similarity"), blank=True, null=True)
    version = models.IntegerField(verbose_name= _("version"), blank=True, null=True)

    class Meta:
        # managed = False
        verbose_name = _("term similarity")
        verbose_name_plural = _("term similarities")


class Entity(abstract.AbstractBaseModel):
    ent_id = models.AutoField(primary_key=True, verbose_name= _("id"))
    doc_id =  models.ForeignKey('Document', on_delete=models.CASCADE, db_column='doc_id', verbose_name=_("document"))
    ent_type = models.TextField(verbose_name= _("entity type"), blank=True, null=True)
    ent_name = models.TextField(verbose_name= _("entity name"), blank=True, null=True)
    version = models.IntegerField(verbose_name= _("version"), blank=True, null=True)

    class Meta:
        # managed = False
        verbose_name = _("entity")
        verbose_name_plural = _("entities")
