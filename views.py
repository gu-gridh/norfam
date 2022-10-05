import re
import timeit
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.renderers import JSONRenderer
from . import schemas
from .serializers import TermSerializer, DocumentSerializer, TermsimSerializer, DocTermSerializer, NeighborhoodSerializer, EntitySerializer, QuerySerializer
from .models import Term, Document, DocTerm, Termsim, Entity
from django.db.models import Prefetch
from math import log2
from functools import cmp_to_key

def sort_tfidf(docA, docB):
    totA = 0.0
    totB = 0.0
    tfA = 1
    tfB = 1
    for doc_term in docA.doc_terms.all():
        tfA = log2(doc_term.tf + 1)
        idfA = log2(100_000) - log2(doc_term.term.term_df)
        totA += tfA * idfA
    for doc_term in docB.doc_terms.all():
        tfB = log2(doc_term.tf + 1)
        idfB = log2(100_000) - log2(doc_term.term.term_df)
        totB += tfB * idfB
    if totA > totB:
        return -1
    elif totA < totB:
        return 1
    else:
        return 0


class TermViewSet(viewsets.ModelViewSet):
    queryset = Term.objects.all()
    serializer_class = TermSerializer
    lookup_field = 'term_term'

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = '__all__'
    # schema = schemas.MetaDataSchema()
    

class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()
    lookup_field = 'doc_id'

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = '__all__'
    # schema = schemas.MetaDataSchema()
    
class TermsimViewSet(viewsets.ModelViewSet):
    serializer_class = NeighborhoodSerializer
    def get_queryset(self): 
        q = self.request.query_params.get('q')
        q = [str(term).lower() for term in re.split(r"\s+", self.request.GET.get("q"))]
        queryset = Term.objects.distinct().prefetch_related(
            Prefetch('neighbors', queryset=Termsim.objects.order_by('-similarity'))
        ).select_related().filter(neighbors__target__term_term__in=q).all()
        return queryset
       
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = '__all__'
    # schema = schemas.MetaDataSchema()


class EntityViewSet(viewsets.ModelViewSet):
    # queryset = Entity.objects.all()
    serializer_class = EntitySerializer
    def get_queryset(self):
        q = int(self.request.query_params.get('q'))
        queryset = Entity.objects.distinct().select_related().filter(doc_id=q).all()
        return queryset

    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = '__all__'
    # schema = schemas.MetaDataSchema()

class QueryViewSet(viewsets.ModelViewSet):
    serializer_class = QuerySerializer
    def get_queryset(self):
        search_mode = "w"
        if "m" in self.request.GET:
            search_mode = self.request.GET["m"]
        q = [str(term).lower() for term in re.split(r"\s+", self.request.GET["q"])]
        if search_mode == "t":
            tic = timeit.default_timer()
            queryset = Document.objects.distinct().prefetch_related(
                Prefetch('doc_terms', queryset = DocTerm.objects.filter(term__term_term__in=q))
            ).select_related().filter(doc_terms__term__term_term__in=q).all()
            toc = timeit.default_timer()
            print(toc-tic)
            return sorted(queryset, key=cmp_to_key(sort_tfidf))
            
        else:
            from django.db.models.functions import Lower
            queryset = Document.objects.annotate(doc_keyword_lower=Lower('doc_keyword')).distinct().prefetch_related(
                Prefetch('doc_terms', queryset = DocTerm.objects.filter(term__term_term__in=q))
            ).filter(doc_keyword_lower__in=q).all()
            return queryset

# class QueryViewSet(viewsets.ModelViewSet):
#     serializer_class = QuerySerializer
#     def get_queryset(self):
#         search_mode = "w"
#         if "m" in self.request.GET:
#             search_mode = self.request.GET["m"]
#         database = "cdh"
#         q = [str(term).lower() for term in re.split(r"\s+", self.request.GET["q"])]
#         if search_mode == "t":
#             tic = timeit.default_timer()
#             queryset = Document.objects.distinct().prefetch_related(
#                 Prefetch('doc_terms', queryset = DocTerm.objects.filter(term__term_term__in=q))
#             ).select_related().filter(doc_terms__term__term_term__in=q).all().using(database)
#             print(queryset.query)
#             toc = timeit.default_timer()
#             print(toc-tic)
#             return sorted(queryset, key=cmp_to_key(sort_tfidf))
#         else:
#             queryset = Document.objects.distinct().prefetch_related(
#                 Prefetch('doc_terms', queryset = DocTerm.objects.filter(term__term_term__in=q))
#             ).filter(doc_keyword__in=q).all().using(database).order_by('doc_keyword', 'doc_suppl')
#             print(queryset.query)
#             return queryset