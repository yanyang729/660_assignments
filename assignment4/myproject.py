import json
import requests
from flask import Flask, request, Response
import re
from mykeys import *

application = Flask(__name__)
slack_inbound_url = 'https://hooks.slack.com/services/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'


# helper function to test if a is sublist of b
def is_sublist(a, b):
    if a == []: return True
    if b == []: return False
    return b[:len(a)] == a or is_sublist(a, b[1:])


# This is for task 1:
def task1():
    """send a post request back to inbound url"""
    response = {
        'username': 'yy_bot',
        'icon_emoji': ':dog:',
        'text': 'Hello, my name is yy_bot. I belong to yang yang. I live at 52.41.107.14'
    }
    requests.post(slack_inbound_url, json=response)


# This is for task 2:
def task2(text):
    """parse from stackoverflow api, make a dict with 'attachments' key which have 5 elements"""
    query = re.sub(r'&lt;.*&gt;:|\[.+', '', text)
    url_api = 'https://api.stackexchange.com/2.2/search/advanced?' \
              'order=desc&sort=relevance&q={}&accepted=True&site=stackoverflow'.format(query)  # stack overflow api
    answer_dict = json.loads(requests.get(url_api).text)  # data from api
    do_task3 = re.findall('(?<=\[)\w+', text)  # filter by tag ['python','list']

    if do_task3:
        for item in answer_dict['items']:
            if not is_sublist(do_task3, item['tags']):
                answer_dict['items'].remove(item)

    creation_date = []
    answer_count = []
    link = []
    title = []
    colors = ['#0000ff', '#4000ff', '#8000ff', '#bf00ff', '#ff00ff']
    attachments = []

    for item in answer_dict['items'][:5]:
        creation_date.append(item['creation_date'])  # int
        answer_count.append(item['answer_count'])  # int
        link.append(item['link'])
        title.append(item['title'])

    for cd, ac, l, t, c in zip(creation_date, answer_count, link, title, colors):
        temp_dict = {
            "fallback": "Required plain-text summary of the attachment.",
            "color": c,
            "title": t,
            "title_link": l,
            "footer": "Number of responses:{}".format(str(ac)),
            "ts": cd + 18000  # adjust time
        }
        attachments.append(temp_dict)

    response = {
        'username': 'yy_bot',
        'icon_emoji': ':dog:',
        'text': 'See if these can help',
        'attachments': attachments
    }

    requests.post(slack_inbound_url, json=response)


# This is for task 3:
def task3(text):
    """get geo coordinate from received text, use coordinate to get map image and weather info, put them in a dict"""
    location = re.sub(r'&lt;.+&gt;:', '', text)
    url_api = 'https://maps.googleapis.com/maps/api/geocode/json?address=' + location + '&key=' + key_geo  # google geocoding api

    geo_dict = json.loads(requests.get(url_api).text)['results'][0]
    geometry = geo_dict['geometry']['location']
    lat, lng = geometry['lat'], geometry['lng']
    loc_name = geo_dict['formatted_address']

    url_img = 'https://maps.googleapis.com/maps/api/staticmap?center=' + str(lat) + ',' + str(lng) + \
              '&zoom=14&size=400x320&path=weight:3%7Ccolor:blue%7Cenc:{coaHnetiVjM??_SkM??~R' \
              '&key=' + key_map  # google static map api

    url_api = 'https://api.darksky.net/forecast/' + key_sky + '/' + str(lat) + ',' + str(lng)
    weather_dict = json.loads(requests.get(url_api).text)  # dark sky api https://darksky.net/dev/

    smry_cur = weather_dict['currently']['summary']
    temp = weather_dict['currently']['temperature']
    feel = weather_dict['currently']['apparentTemperature']
    wind = weather_dict['currently']['windBearing']

    smry_day = weather_dict['daily']['summary']

    response = {
        'username': 'yy_bot',
        'icon_emoji': ':dog:',
        "attachments": [
            {
                "color": "#DCDCDC",
                "pretext": "Here is the weather infomation",
                "fields": [
                    {
                        "title": "Now",
                        "value": smry_cur,
                        "short": True
                    }, {
                        "title": "Current temperature",
                        "value": temp,
                        "short": True
                    }, {
                        "title": "Feel like",
                        "value": feel,
                        "short": True
                    }, {
                        "title": "wind",
                        "value": wind,
                        "short": True
                    }, {
                        "title": "Forecast",
                        "value": smry_day,
                        "short": False
                    }
                ],
                "image_url": url_img,
                "footer": loc_name
            }
        ]
    }

    requests.post(slack_inbound_url, json=response)



@application.before_request
def log_request_info():
    application.logger.debug('Headers: %s', request.headers)
    application.logger.debug('Body: %s', request.get_data())


@application.route('/slack', methods=['POST'])
def inbound():
    channel = request.form['channel_name']
    username = request.form['user_name']
    text = request.form['text']
    botname = 'yy_bot'

    if botname != username and username in ['zac.wentzell','yanyang729','yangyang729'] and re.findall(u'BOTS_RESPOND',text):
        task1()
    if botname != username and username in ['zac.wentzell', 'yanyang729','yangyang729'] and re.findall(u'I_NEED_HELP_WITH_CODING',text):
        task2(text)
    if botname != username and username in ['zac.wentzell','yanyang729','yangyang729'] and re.findall(u"WHAT'S_THE_WEATHER_LIKE_AT",text):
        task3(text)

    print username + " in " + channel + " says: " + text
    print request.form
    return Response(), 200


@application.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)