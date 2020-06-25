#!/usr/bin/env python3

import requests
import datetime
import os

class AskNicely(object):

    """
    See AskNicely Documentation:
    https://asknicely.asknice.ly/help/apidocs
    """

    def __init__(self, domain_key, api_key):
        self.domain_key = domain_key
        self.api_key = api_key

    def urlGenerator(self, endpoint, *args):
        url = "https://%s.asknice.ly/api/v1/%s/%s?X-apikey=%s" % ( self.domain_key,
                                                                   endpoint,
                                                                   "/".join(map(str, args)),
                                                                   self.api_key)
        return url

    def getResponses(self, sort_direction="asc", pagesize=50000, pagenumber=1, since_time=0,
                format="json", filter="answered", sort_by="sent", end_time=0):


        """
        Gets NPS responses from AskNicely

        >>> thirty_days_ago = (datetime.date.today() - datetime.timedelta(30)).strftime("%s")
        >>> today = datetime.datetime.today().strftime("%s")
        >>> asknicely = AskNicely(os.getenv('ASK_NICELY_DOMAIN_KEY'), os.getenv('ASK_NICELY_API_KEY'))
        >>> asknicely.getResponses(since_time=thirty_days_ago, end_time=today).status_code
        200
        >>> import json
        >>> parsed = asknicely.getResponses(since_time=thirty_days_ago, end_time=today, pagesize=1, pagenumber=1).json()
        >>> len(parsed["data"])
        1
        >>> asknicely = AskNicely("fake", "fake")
        >>> asknicely.getResponses(since_time=thirty_days_ago, end_time=today).status_code
        404

        """
        json = requests.get(self.urlGenerator("responses", sort_direction, pagesize, pagenumber,
                                                since_time, format, filter, sort_by, end_time))
        return json


if __name__ == "__main__":
    import doctest
    doctest.testmod()
