# -*- coding: utf-8 -*-
import logging

from django.views.generic import TemplateView
from django.http import QueryDict

from haystack.query import SearchQuerySet, EmptySearchQuerySet

from dynamiq.utils import get_advanced_search_formset_class, FormsetQBuilder, ParsedStringQBuilder

from memopol.meps.views import render_to_csv

from .forms import MEPSearchForm, MEPSearchAdvancedFormset, MEPSimpleSearchForm
from .shortcuts import TopRated, WorstRated


log = logging.getLogger(__name__)


class SearchView(TemplateView):

    template_name = 'search/search.html'
    list_template_name = "blocks/representative_list.html"

    def get_template_names(self):
        """
        Dispatch template according to the kind of request: ajax or normal.
        """
        if self.request.is_ajax():
            return [self.list_template_name]
        else:
            return [self.template_name]

    def get(self, request, *args, **kwargs):
        query = None
        sort = MEPSearchAdvancedFormset.options_form_class.SORT_INITIAL
        limit = MEPSearchAdvancedFormset.options_form_class.LIMIT_INITIAL
        format = MEPSearchAdvancedFormset.options_form_class.FORMAT_INITIAL
        label = ""

        formset_class = get_advanced_search_formset_class(self.request.user, MEPSearchAdvancedFormset, MEPSearchForm)
        form = MEPSimpleSearchForm(self.request.GET or None)
        # if form.is_valid():
        #     F = ParsedStringQBuilder(form.cleaned_data['q'], MEPSearchForm)
        #     query, label = F()
        #     limit = form.cleaned_data.get("limit") or limit
        #     sort = form.cleaned_data.get("sort") or sort
        #     format = form.cleaned_data.get("format") or format

        def generate_form_args_part(query_part, form_number, filter_type):
            parts = query_part.split(' ')
            data_type = MEPSearchForm.determine_filter_type(parts[0])
            form_args = dict((
                ("form-%s-filter_name" % form_number, parts[0]),
                ("form-%s-%s_lookup" % (form_number, data_type), parts[1]),
                ("form-%s-filter_value_%s" % (form_number, data_type), u' '.join(parts[2:])),
                ("form-%s-filter_right_op" % form_number, filter_type),
            ))
            return form_args

        def generate_form_args(query):
            form_args = {}
            global_counter = 0
            or_filter = "OR"
            or_parts = query.split(" %s " % or_filter)
            for or_counter, query_part in enumerate(or_parts):
                and_filter = "AND"
                if and_filter in query_part:
                    and_parts = query_part.split(" %s " % and_filter)
                    for and_counter, query_part in enumerate(and_parts):
                        type_filter = len(and_parts) > and_counter + 1 and and_filter or or_filter
                        if type_filter == or_filter:
                            type_filter = len(or_parts) > or_counter + 1 and type_filter or ''
                        form_args.update(generate_form_args_part(query_part, global_counter, type_filter))
                        global_counter += 1
                else:
                    type_filter = len(or_parts) > or_counter + 1 and or_filter or ''
                    form_args.update(generate_form_args_part(query_part, global_counter, type_filter))
                    global_counter += 1
            return form_args, global_counter

        def generate_formset_args_from_querydict(get_args):
            """
            Turns a GET QueryDict generated by js to a QueryDict
            dedicated to fill a formset.
            """
            form_args = {}
            query = get_args.get('q', False)
            if not query:
                return None
            form_args, total_forms = generate_form_args(query)
            form_args.update({
                "form-TOTAL_FORMS": total_forms,
                "form-INITIAL_FORMS": 1,
            })
            form_args.update({
                "limit": get_args.get('limit', 15),
                "sort": get_args.get('sort', "last_name"),
                "format": get_args.get('format', format),
                "search_mode": "advanced",
            })
            query_string = u"&".join("%s=%s" % (k, v) for k, v in form_args.iteritems())
            return QueryDict(query_string) or None

        form_args = generate_formset_args_from_querydict(self.request.GET)
        formset = formset_class(form_args)
        formset.full_clean()
        if formset.is_valid():
            F = FormsetQBuilder(formset)
            query, label = F()
            sort = formset.options_form.cleaned_data.get("sort", sort)
            limit = formset.options_form.cleaned_data.get("limit", limit)
            format = formset.options_form.cleaned_data.get("format")

        if query:
            results = SearchQuerySet().filter(query)
            if sort:
                results = results.order_by(sort)
        else:
            results = EmptySearchQuerySet()
        context = {
            "dynamiq": {
                "results": results,
                "label": label,
                "formset": formset,
                "form": form,
                "shortcuts": [
                    TopRated({"request": self.request}),
                    WorstRated({"request": self.request})
                ]
            },
            "list_template_name": self.list_template_name,
            "per_page": limit
        }
        if format == MEPSearchAdvancedFormset.options_form_class.FORMAT.CSV:
            objects = [r.object for r in results]
            return render_to_csv(objects)
        else:
            return self.render_to_response(context)


class XhrSearchView(SearchView):

    template_name = "search/xhr.html"
