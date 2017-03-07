import sys
import operator
import requests
import json
import twitter
from watson_developer_cloud import PersonalityInsightsV2 as PersonalityInsights

from Constants import (twitter_consumer_key,twitter_consumer_secret,twitter_access_token,
  twitter_access_secret,pi_username,pi_password)

twitter_api = twitter.Api(consumer_key=twitter_consumer_key, consumer_secret=twitter_consumer_secret, access_token_key=twitter_access_token, access_token_secret=twitter_access_secret)
personality_insights_api = PersonalityInsights(username=pi_username, password=pi_password)

def analyze(handle):
  statuses = twitter_api.GetUserTimeline(screen_name=handle, count=200, include_rts=False)


  text = b"" # must initialize text blob as a bytes object,
  for status in statuses:
    if (status.lang == 'en'):
       text += status.text.encode('utf-8') # .encode() returns bytes object
  return text


def flatten(orig):
    data = {}
    for c in orig['tree']['children']:
        if 'children' in c:
            for c2 in c['children']:
                if 'children' in c2:
                    for c3 in c2['children']:
                        if 'children' in c3:
                            for c4 in c3['children']:
                                if (c4['category'] == 'personality'):
                                    data[c4['id']] = c4['percentage']
                                    if 'children' not in c3:
                                        if (c3['category'] == 'personality'):
                                                data[c3['id']] = c3['percentage']
    return data

def compare(dict1,dict2):
  compared_data = {}
  for keys in dict1:
    if dict1[keys] != dict2[keys]:
      compared_data[keys]=abs(dict1[keys]-dict2[keys])
  return compared_data


# define the twitter handles of the two people to be compared
# (what combo can be more different than elon musk and donald trump?)
handleOne = '@elonmusk'
handleTwo = '@realDonaldTrump'

user_result = personality_insights_api.profile(analyze(handleOne))
celebrity_result = personality_insights_api.profile(analyze(handleTwo))

user = flatten(user_result)
celebrity = flatten(celebrity_result)
compared_results = compare(user,celebrity)

sorted_result = sorted(compared_results.items(), key=operator.itemgetter(1))

for keys, value in sorted_result[:5]:
    title = '-----------'+keys+'-----------'
    print (title),
    print(handleOne,user[keys]),
    print (handleTwo,celebrity[keys]),
    print ('diff:',compared_results[keys])
    print ('-'*len(title),'\n\n')
