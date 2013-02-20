from tastypie import fields
from tastypie.resources import ModelResource
from memopol.reps.models import Party,\
                                Opinion,\
                                Representative,\
                                PartyRepresentative,\
                                Email,\
                                CV,\
                                WebSite,\
                                OpinionREP


class REPPartyResource(ModelResource):
    partyrepresentative_set = fields.ToManyField("memopol.reps.api.REPPartyRepresentativeResource", "partyrepresentative_set")

    class Meta:
        queryset = Party.objects.all()


class REPOpinionResource(ModelResource):
    opinionrep_set = fields.ToManyField("memopol.reps.api.REPOpinionREPResource", "opinionrep_set")

    class Meta:
        queryset = Opinion.objects.all()


class REPRepresentativeResource(ModelResource):
    opinionrep_set = fields.ToManyField("memopol.reps.api.REPOpinionREPResource", "opinionrep_set")
    email_set = fields.ToManyField("memopol.reps.api.REPEmailResource", "email_set")
    website_set = fields.ToManyField("memopol.reps.api.REPWebSiteResource", "website_set")
    cv_set = fields.ToManyField("memopol.reps.api.REPCVResource", "cv_set")
    partyrepresentative_set = fields.ToManyField("memopol.reps.api.REPPartyRepresentativeResource", "partyrepresentative_set")
    score_set = fields.ToManyField("votes.api.ScoreResource", "score_set")
    vote_set = fields.ToManyField("votes.api.VoteResource", "vote_set")

    class Meta:
        queryset = Representative.objects.all()


class REPPartyRepresentativeResource(ModelResource):
    representative = fields.ForeignKey(REPRepresentativeResource, "representative")
    party = fields.ForeignKey(REPPartyResource, "party")

    class Meta:
        queryset = PartyRepresentative.objects.all()


class REPEmailResource(ModelResource):
    representative = fields.ForeignKey(REPRepresentativeResource, "representative")

    class Meta:
        queryset = Email.objects.all()


class REPCVResource(ModelResource):
    representative = fields.ForeignKey(REPRepresentativeResource, "representative")

    class Meta:
        queryset = CV.objects.all()


class REPWebSiteResource(ModelResource):
    representative = fields.ForeignKey(REPRepresentativeResource, "representative")

    class Meta:
        queryset = WebSite.objects.all()


class REPOpinionREPResource(ModelResource):
    representative = fields.ForeignKey(REPRepresentativeResource, "representative")
    opinion = fields.ForeignKey(REPOpinionResource, "opinion")

    class Meta:
        queryset = OpinionREP.objects.all()
