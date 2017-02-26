import os
import json
import requests
from flask import Flask, request, Response
import re

application = Flask(__name__)
# Now this the only inbound url for our channel. mine was deleted

# NEEED TO BE CHANGED !!!!!!!!!!!!
slack_inbound_url = 'https://hooks.slack.com/services/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'


def is_sublist(a, b):
    if a == []: return True
    if b == []: return False
    return b[:len(a)] == a or is_sublist(a, b[1:])


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
    #  ===============task 1=====================
    # NEED TO BE CHANGED !!!!!!!!!!!!
    if botname != username and username in ['zac.wentzell','yanyang729'] and re.findall(u'BOTS_RESPOND',text):
        response = {
            'username': 'yy_bot',
            'icon_emoji': ':dog:',
            'text': 'Hello, my name is yy_bot. I belong to yang yang. I live at 52.41.107.14'
        }
        requests.post(slack_inbound_url, json=response)

    # ===============task 2&3=====================
    # NEED TO BE CHANGED !!!!!!!!!!!!
    if botname != username and username in ['zac.wentzell', 'yanyang729'] and re.findall(u'I_NEED_HELP_WITH_CODING',text):
        query = re.sub(r'&lt;.*&gt;:|\[.+','',text)
        # stack overflow api
        url_api = 'https://api.stackexchange.com/2.2/search/advanced?' \
                  'order=desc&sort=relevance&q={}&accepted=True&site=stackoverflow'.format(query)
        # data from api
        answer_dict = json.loads(requests.get(url_api).text)

        # filter by tag
        do_task3 = re.findall('(?<=\[)\w+',text) # ['python','list']

        if do_task3:
            for item in answer_dict['items']:
                if not is_sublist(do_task3,item['tags']):
                    answer_dict['items'].remove(item)

        creation_date = []
        answer_count = []
        link = []
        title = []
        colors = ['#0000ff','#4000ff','#8000ff','#bf00ff','#ff00ff']

        attachments = []

        try:
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

        except:
            response = {
                'username': 'yy_bot',
                'icon_emoji': ':dog:',
                'text': 'error from task 2: No answer, something must be wrong '
            }

        requests.post(slack_inbound_url, json=response)

    #  ===============task 3=====================
    # NEED TO BE CHANGED !!!!!!!!!!!!
    if botname != username and username in ['zac.wentzell','yanyang729'] and re.findall(u"WHAT'S_THE_WEATHER_LIKE_AT",text):
        location = re.sub(r'&lt;.+&gt;:', '', text)
        # google geocoding api
        url_api = 'https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyCPOz9zoUR9Pzi9wthkBAIV_IOpojiDBuA'.format(location)
        geo_dict = json.loads(requests.get(url_api).text)['results'][0]
        geometry = geo_dict['geometry']['location']
        lat,lng = geometry['lat'],geometry['lng']
        loc_name = geo_dict['formatted_address']

        # google static map api
        url_img = 'https://maps.googleapis.com/maps/api/staticmap?center=' + str(lat)+ ',' +str(lng) + \
                  '&zoom=14&size=400x320&path=weight:3%7Ccolor:blue%7Cenc:{coaHnetiVjM??_SkM??~R' \
                  '&key=AIzaSyCwj1c2EaBN9ifZLBXyqjJt6DLi61gAPeM'


        # dark sky api https://darksky.net/dev/
        url_api = 'https://api.darksky.net/forecast/d1614cf4d7e533a9a0599b4f8bac3114/{},{}'.format(lat,lng)
        weather_dict = json.loads(requests.get(url_api).text)

        smry_cur = weather_dict['currently']['summary']
        temp = weather_dict['currently']['temperature']
        feel = weather_dict['currently']['apparentTemperature']
        wind = weather_dict['currently']['windBearing']

        smry_day = weather_dict['daily']['summary']

        try:
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
                            },{
                                "title": "Current temperature",
                                "value": temp,
                                "short": True
                            },{
                                "title": "Feel like",
                                "value": feel,
                                "short": True
                            },{
                                "title": "wind",
                                "value": "High",
                                "short": True
                            },{
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

        except:
            response = {
                'username': 'yy_bot',
                'icon_emoji': ':dog:',
                'text': 'error from task 3: No answer, something must be wrong '
            }

        requests.post(slack_inbound_url, json=response)

    # print info on my sever and return
    print username + " in " + channel + " says: " + text
    print request.form
    return Response(), 200


@application.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)