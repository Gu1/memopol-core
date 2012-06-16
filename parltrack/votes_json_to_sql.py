#!/usr/bin/python
# -*- coding:Utf-8 -*-

import os
import sys
from datetime import datetime
from json import loads

sys.path += [os.path.abspath(os.path.split(__file__)[0])[:-len("parltrack")] + "apps/"]

from votes.models import RecommendationData

if __name__ == "__main__":
    print "cleaning"
    RecommendationData.objects.all().delete()
    print "read file"
    lines = open("ep_votes.json").readlines()
    a = 1
    for vote in lines:
        jayson = loads(vote)
        #print jayson.get("report", None), jayson["title"], jayson["ts"]["$date"]
        RecommendationData.objects.create(proposal_name=jayson.get("report", jayson["title"]),
                                         title=jayson["title"],
                                         data=vote,
                                         date=datetime.fromtimestamp(int(str(jayson["ts"]["$date"])[:-3])))
        sys.stdout.write("%s/%s\r" % (a, len(lines)))
        sys.stdout.flush()
        a += 1
    sys.stdout.write("\n")

# vim:set shiftwidth=4 tabstop=4 expandtab:
