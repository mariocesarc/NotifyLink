import re


def is_valid_url(url):
    url_pattern = r'^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$'
    return re.match(url_pattern, url, re.IGNORECASE) is not None