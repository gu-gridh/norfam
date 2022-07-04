from rest_framework import serializers
from .models import Term, Document, DocTerm, Termsim, Entity


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ['term_term', 'term_stem', 'term_df']

class TermsimSerializer(serializers.ModelSerializer):
    term = TermSerializer(read_only=True)
    class Meta:
        model = Termsim
        fields = ['term', 'similarity']

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['ent_type', 'ent_name']

class NeighborhoodSerializer(serializers.ModelSerializer):
    neighbors = TermsimSerializer(many=True)
    class Meta:
        model = Term
        fields = ['term_term', 'neighbors']

class DocTermSerializer(serializers.ModelSerializer):
    term = TermSerializer(read_only=True)
    class Meta:
        model = DocTerm
        fields = ['tf', 'term']

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['doc_keyword', 'doc_text', 'doc_suppl']

class QuerySerializer(serializers.ModelSerializer):
    doc_terms = DocTermSerializer(many=True)
    class Meta:
        model = Document
        fields = ['doc_keyword', 'doc_abstr', 'doc_terms', 'doc_suppl']
