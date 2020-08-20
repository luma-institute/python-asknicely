# python-asknicely

[![CircleCI](https://circleci.com/github/luma-institute/python-asknicely.svg?style=svg)](https://circleci.com/github/luma-institute/python-asknicely/)

Simple sdk for interacting with [AskNicely](https://www.asknicely.com) API services. Supports the following actions:

* Add person
* Delete person
* Get historical statistics
* Get NPS
* Get person
* Get responses
* Get sent statistics
* Get unsubscribed
* Remove person
* Send survey
* Send bulk surveys

### Requirements

* Python3 
* [requests](https://pypi.org/project/requests/) library
* Valid API credentials provided by AskNicely

### Installation

```bash
git clone git@github.com:luma-institute/python-asknicely.git
cd asknicely 
pip install --upgrade requests build
python -m build
```
You can also add the following dependency to your requirements.txt file:

```bash
requests
-e git+git@github.com:luma-institute/python-asknicely.git@master#egg=asknicely
```

### Basic usage

```python
import asknicely

asknicely = AskNicely("domain_key", "api_key")

asknicely.add_person("Test user", "test3@example.com")
asknicely.delete_person("test3@example.com")
asknicely.get_historical_stats("2019", "8", "1")
asknicely.get_nps()
asknicely.get_person("getuser@example.com")
asknicely.get_responses(since_time=thirty_days_ago, end_time=today)
asknicely.get_sent_stats("30", "10", "1")
asknicely.get_unsubscribed()
asknicely.remove_person("fakeuser@example.com")
asknicely.send_survey("fakeuser@example.com", "Fake User", False)
asknicely.send_survey_bulk(users)
```

For supported arguments see the [code](asknicely/sdk.py).

### Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D
