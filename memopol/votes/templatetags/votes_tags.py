from django import template
from memopol.votes.models import Vote, Score

register = template.Library()


@register.simple_tag(takes_context=True)
def mep_votes_list_on_proposal(context, mep, proposal):
    context['mep_votes'] = sorted(Vote.objects.filter(representative=mep.representative_ptr, recommendation__proposal=proposal), key=lambda x: x.recommendation.datetime)
    return ''


@register.simple_tag(takes_context=True)
def mep_score_on_vote(context, mep, proposal):
    context['mep_score'] = Score.objects.get(representative=mep, proposal=proposal)
    return ''


@register.simple_tag(takes_context=True)
def rep_position_on_recommendation(context, rep, recommendation):
    context['rep_position'] = Vote.objects.get(representative=rep, recommendation=recommendation)
    return ''
