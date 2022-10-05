from django.db import models

import diana.abstract.models as abstract

# Create your models here.

#Image?
# for the documents that we add, do we need to upload image for them?
# If yes, then why we don't have image attribute in models 

#Is there any tag for the books?

# Do we need to change these classes 


class Term(abstract.AbstractBaseModel):
    """A unique word occurring in documents (type, not token, can be numeric)."""

    term_id = models.AutoField(primary_key=True)
    # The word in lowercase
    term_term = models.CharField(unique=True, max_length=100)
    # # Not used?
    term_stem = models.CharField(max_length=100, blank=True, null=True)
    # # Document frequency, how many documents contain the word at least once
    term_df = models.IntegerField(blank=True, null=True)
    # # Documents edition
    version = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'term'


class DocTerm(abstract.AbstractBaseModel):
    """Mapping of a certain term in a certain document."""

    doc_term_id = models.AutoField(primary_key=True)
    # The document where it occurs at least once
    doc_id = models.ForeignKey('Document', on_delete=models.PROTECT, db_column='doc_id', related_name='doc_terms')
    # The term
    term = models.ForeignKey('Term', on_delete=models.PROTECT, db_column='term_id')
    # Term frequency, how many times the term occurs in the document
    tf = models.IntegerField(blank=True, null=True)
    # # Documents edition
    version = models.IntegerField(blank=True, null=True)
    class Meta:
        # managed = False
        db_table = 'doc_term'

class Document(abstract.AbstractBaseModel):
    """An encyclopedic article on a topic."""

    doc_id = models.AutoField(primary_key=True)
    # The topic, one or a few words
    doc_keyword = models.CharField(max_length=100)
    # Full description, may contain HTML tags
    doc_text = models.TextField()
    # Truncated description, max ca. 700 chars, possibly no incomplete HTML tags
    doc_abstr = models.CharField(max_length=2048)
    # Running number unique among documents with same keyword, starting from 0
    doc_suppl = models.IntegerField(blank=True, null=True)
    # # Documents edition
    version = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'document'

class Termsim(abstract.AbstractBaseModel):
    """Similarity of two terms.

    Each term pair occurs twice – once in each direction."""

    termsim_id = models.AutoField(primary_key=True)
    # Term one
    target = models.ForeignKey('Term', on_delete=models.PROTECT, db_column='term1_id', related_name='neighbors')
    # Term two
    term = models.ForeignKey('Term', on_delete=models.PROTECT, db_column='term2_id')
    # Similarity between 0 and 1
    similarity = models.FloatField()

    class Meta:
        # managed = False
        db_table = 'termsim'


class Entity(abstract.AbstractBaseModel):
    ent_id = models.AutoField(primary_key=True)
    doc_id =  models.IntegerField(blank=True, null=True)
    ent_type = models.TextField()
    ent_name = models.TextField()

    class Meta:
        # managed = False
        db_table = 'entity'
