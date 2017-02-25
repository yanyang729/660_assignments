import os
import json
import requests
from flask import Flask, request, Response
import re

application = Flask(__name__)
# Now this the only inbound url for our channel. mine was deleted
slack_inbound_url = 'https://hooks.slack.com/services/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'


def is_sublist(a, b):
    if a == []: return True
    if b == []: return False
    return b[:len(a)] == a or is_sublist(a, b[1:])


@application.route('/slack', methods=['POST'])
def inbound():

    channel = request.form.get('channel_name')
    username = request.form.get('user_name')
    text = request.form.get('text')

    #  ===============task 1=====================
    if username in ['zac.wentzell','yangyang729'] and re.findall('<BOTS_RESPOND>',text):
        response = {
            'username': 'yy_bot',
            'icon_emoji': ':dog:',
            'text': 'Hello, my name is yy_bot. I belong to yang yang. I live at 52.10.92.153'
        }
        requests.post(slack_inbound_url, json=response)

    #  ===============task 2&3=====================
    elif username in ['zac.wentzell','yangyang729'] and re.findall('<I_NEED_HELP_WITH CODING>:',text):
        query = re.sub(r'<.*>:|\[.+','',text)
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
                creation_date.append(item['creation_date']) #int
                answer_count.append(item['answer_count']) #int
                link.append(item['link'])
                title.append(item['title'])

            for cd,ac,l,t,c in zip(creation_date,answer_count,link,title,colors):
                temp_dict ={
                    "fallback": "Required plain-text summary of the attachment.",
                    "color": c,
                    "pretext": "See if these below can help",
                    "title": t,
                    "title_link": l,
                    "footer": "Number of responses:{}".format(str(ac)),
                    "ts": cd
                }
                attachments.append(temp_dict)

            response = {
                'username': 'yy_bot',
                'icon_emoji': ':dog:',
                'attachments': attachments
            }

        except:
            response = {
                'username': 'yy_bot',
                'icon_emoji': ':dog:',
                'text': 'error2: No answer, something must be wrong '
            }

        requests.post(slack_inbound_url, json=response)

    #  ===============task 3=====================
    if username in ['zac.wentzell','yangyang729'] and re.findall("<WHAT'S_THE_WEATHER_LIKE_AT>:",text):
        query = re.sub(r'<.+>','',text)
        # google geocoding api



    # print info on my sever and return
    print username + " in " + channel + " says: " + text
    print request.form
    return Response(), 200


@application.route('/', methods=['GET'])
def test():
    return Response('It works!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)