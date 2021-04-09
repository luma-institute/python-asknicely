#!/usr/bin/env python3

import datetime
import json
import requests


class AskNicely(object):
    """
    See AskNicely Documentation:
    https://asknicely.asknice.ly/help/apidocs
    """

    def __init__(self, domain_key, api_key):
        self.domain_key = domain_key
        self.api_key = api_key

    def url_generator(self, endpoint, *args):
        url = "https://%s.asknice.ly/api/v1/%s/%s?X-apikey=%s" % (
            self.domain_key, endpoint, "/".join(map(str, args)), self.api_key)
        return url

    def url_generator_no_args(self, endpoint, apikey=True):
        if apikey:
            url = "https://%s.asknice.ly/api/v1/%s?X-apikey=%s" % (
                self.domain_key, endpoint, self.api_key)
        else:
            url = "https://%s.asknice.ly/api/v1/%s" % (
                self.domain_key, endpoint)

        return url

    def bool_stringify(self, bool) -> str:
        return str(bool).lower()

    def get_responses(
            self,
            sort_direction="asc",
            pagesize=50000,
            pagenumber=1,
            since_time=0,
            format="json",
            filter="answered",
            sort_by="sent",
            end_time=0) -> dict:
        """
        Gets NPS responses from AskNicely
        >>> thirty_days_ago = (datetime.date.today() - datetime.timedelta(30)).strftime("%s")
        >>> today = datetime.datetime.today().strftime("%s")
        >>> request = asknicely.get_responses(since_time=thirty_days_ago, end_time=today)
        >>> request["success"]
        True
        >>> import json
        >>> parsed = asknicely.get_responses(since_time=thirty_days_ago, end_time=today, pagesize=1, pagenumber=1)
        >>> parsed["success"]
        True
        >>> request = asknicely.get_responses(since_time=thirty_days_ago, end_time=today)
        >>> request["success"]
        True
        """
        response = requests.get(
            self.url_generator(
                "responses",
                sort_direction,
                pagesize,
                pagenumber,
                since_time,
                format,
                filter,
                sort_by,
                end_time))
        return response.json()

    def send_survey(
            self,
            email,
            name,
            triggeremail=True,
            add_person=True,
            delayminutes=10,
            segment="",
            customproperty="",
            thendeactivate=True) -> dict:
        """
        The api endpoint for sending a survey works differently from
        the other endpoints.
        >>> request = asknicely.send_survey("fakeuser@example.com", "Fake User", False)
        >>> request["success"]
        True
        >>> print(request["result"][0]["email"])
        fakeuser@example.com
        >>> request = asknicely.remove_person("fakeuser@example.com")
        >>> request["success"]
        True
        """
        url = self.url_generator_no_args("person/trigger", False)

        data = {"email": email,
                "name": name,
                "triggeremail": self.bool_stringify(triggeremail),
                "add_person": self.bool_stringify(add_person),
                "delayminutes": delayminutes,
                "segment": segment,
                "customproperty": customproperty,
                "thendeactivate": self.bool_stringify(thendeactivate)
                }

        headers = {'X-apikey': self.api_key}
        response = requests.post(url, data=data, headers=headers)
        return response.json()

    def send_survey_bulk(self, users, obeyrules=True,
                         triggeremail=False) -> dict:
        """
        >>> users = [ { "name": "Test User1", "email": "test1@example.com"}, { "name": "Test User2", "email": "test2@example.com"} ]
        >>> request = asknicely.send_survey_bulk(users)
        >>> request["success"]
        True
        >>> requst = asknicely.remove_person("test1@example.com")
        >>> request["success"]
        True
        >>> request = asknicely.remove_person("test2@example.com")
        >>> request["success"]
        True
        """

        url = self.url_generator_no_args("person/add", False)
        headers = {'X-apikey': self.api_key}
        for user in users:
            user.update({"obeyrules": self.bool_stringify(obeyrules)})
            user.update({"triggeremail": self.bool_stringify(triggeremail)})
        data = {"people": [user for user in users]}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response.json()

    def add_person(self, name, email) -> dict:
        """
        >>> request = asknicely.add_person("Test user", "test3@example.com")
        >>> request["success"]
        True
        >>> request = asknicely.remove_person("test3@example.com")
        >>> request["success"]
        True
        """
        url = self.url_generator_no_args("person/add", False)
        headers = {'X-apikey': self.api_key}
        data = {"people": [{"name": name, "email": email}]}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response.json()

    def get_person(self, search, key="email") -> dict:
        """
        >>> request = asknicely.send_survey("getuser@example.com", "Fake User", False)
        >>> request["success"]
        True
        >>> request = asknicely.get_person("getuser@example.com")
        >>> request["success"]
        True
        >>> request = asknicely.remove_person("getuser@example.com")
        >>> request["success"]
        True
        """
        response = requests.get(self.url_generator("person/get", search, key))
        return response.json()

    def remove_person(self, search, key="email") -> dict:
        """
        >>> email = "remove@example.com"
        >>> request = asknicely.send_survey(email, "Fake User", False)
        >>> request["success"]
        True
        >>> request = asknicely.remove_person(email)
        >>> request["success"]
        True
        """
        response = requests.get(
            self.url_generator(
                "person/remove", search, key))
        return response.json()

    def delete_person(self, email, notify=1) -> dict:
        """
        >>> request = asknicely.send_survey(random_email, "Fake User", False)
        >>> request["success"]
        True
        >>> deletion = asknicely.delete_person(random_email)
        >>> deletion["success"]
        True
        >>> deletion = asknicely.delete_person(random_email)
        >>> deletion["success"]
        False
        """

        url = self.url_generator_no_args("privacy/remove", False)
        headers = {'X-apikey': self.api_key}
        data = {"email": email, "notify": notify}
        response = requests.post(url, data=data, headers=headers)
        return response.json()

    def get_unsubscribed(self) -> dict:
        """
        >>> request = asknicely.get_unsubscribed()
        >>> request["success"]
        True
        """
        response = requests.get(
            self.url_generator_no_args("person/unsubscribed"))
        return response.json()

    def get_nps(self) -> dict:
        """
        >>> request = asknicely.get_nps()
        >>> if "NPS" in request:
        ...     True
        ... else:
        ...     False
        True
        """
        response = requests.get(self.url_generator_no_args("getnps"))
        return response.json()

    def get_historical_stats(
            self,
            year,
            month,
            day,
            segment="",
            start_time="",
            end_time="") -> dict:
        """
        >>> request = asknicely.get_historical_stats("2019", "8", "1")
        >>> request["success"]
        True
        """
        url = self.url_generator_no_args("stats")

        data = {"year": year,
                "month": month,
                "day": day,
                "segment": segment,
                "start_time": start_time,
                "end_time": end_time
                }

        response = requests.get(url, data=json.dumps(data))
        return response.json()

    def get_sent_stats(self, days, field, value) -> dict:
        """
        >>> request = asknicely.get_sent_stats("30", "10", "1")
        >>> isinstance(request["nps"], int)
        True
        >>> isinstance(request["sent"], int)
        True
        >>> isinstance(request["delivered"], int)
        True
        """
        url = self.url_generator_no_args("sentstats")

        data = {"days": days,
                "field": field,
                "value": value
                }

        response = requests.get(url, data=json.dumps(data))
        return response.json()


if __name__ == "__main__":
    import doctest
    import random
    import string
    import os

    domainkey = os.getenv('ASK_NICELY_DOMAIN_KEY')
    apikey = os.getenv('ASK_NICELY_API_KEY')
    letters = string.ascii_lowercase
    random = ''.join(random.choice(letters) for i in range(10))

    doctest.testmod(extraglobs={'asknicely': AskNicely(domainkey, apikey),
                                'random_email': random + "@example.com"})
