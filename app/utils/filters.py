# expects to receive a datetime
def format_date(date):
    # strftime() method converts datetime to a string, %m/%d/%y = '01/01/20'
    return date.strftime('%m/%d/%y')

# tests that the format_date function is working properly, when run python app/utils/filters.py in powershell
# from datetime import datetime
# print(format_date(datetime.now()))

# removes all extraneous information from a URL string, leaving only the domain name.
def format_url(url):
    return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# tests that the format_url function is working properly, when run python app/utils/filters.py in powershell
# print(format_url('http://google.com/test/'))
# print(format_url('https://www.google.com?q=test'))


def format_plural(amount, word):
    if amount != 1:
        return word + 's'

    return word

# tests whether format_plural function works properly
# print(format_plural(2, 'cat'))
# print(format_plural(1, 'dog'))