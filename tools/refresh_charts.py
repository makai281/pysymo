#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = 'ilya-il'

from pymongo import MongoClient
from datetime import datetime

from config import MONGO_HOST, MONGO_PORT, MONGO_DATABASE

db = MongoClient(host=MONGO_HOST, port=MONGO_PORT)[MONGO_DATABASE]


# TOP HOSTS by messages count
def top_hosts():
    library = {
        'chart': {
            'height': 500
        },
        'title': {
            'text': 'Top10 hosts'
        },
        'plotOptions': {
            'pie': {
                'dataLabels': {
                    'enabled': 'true',
                    'format': '<b>{point.name}</b> - {point.y}'
                }
            }
        },
#        'legend': {
#            'layout': 'vertical',
#            'align': 'right',
#            'verticalAlign': 'middle'
#        }
    }

    res = db.messages.aggregate([{"$group": {"_id": "$h", "count": {"$sum": 1}}},
                                 {"$sort": {"count": -1}},
                                 {"$limit": 10}
                                 ])
    # data list [['Label', value], ] for chartkick
    # add count to hostname - create label for chart
    data = [[i['_id'], i['count']] for i in res['result']]

    db.charts.update({'name': 'tophosts'},
                     {'$set': {'type': 'pie',
                               'title': 'Top 10 hosts',
                               'library': library,
                               'created': datetime.now(),
                               'data': data}},
                     upsert=True)


# Messages count per day
def messages_per_day():
    library = {
        'title': {
            'text': 'Messages per day'
        }
    }
    res = db.messages.aggregate([{"$project": {"host": "$h",
                                               "y": {"$year": "$d"},
                                               "m": {"$month": "$d"},
                                               "d": {"$dayOfMonth": "$d"}}
                                  },
                                 {"$group": {"_id": {"y": "$y", "m": "$m", "d": "$d"},
                                             "count": {"$sum": 1}}
                                  }
                                 ])
    # data list [['Label', value], ] for chartkick
    data = [['{0}-{1:02d}-{2:02d}'.format(i["_id"]["y"], i["_id"]["m"], i["_id"]["d"]), i['count']]
            for i in res['result']]

    db.charts.update({'name': 'mesperday'},
                     {'$set': {'type': 'line',
                               'title': 'Messages per day',
                               'library': library,
                               'created': datetime.now(),
                               'data': data}},
                     upsert=True)


def main():
    top_hosts()
    messages_per_day()

if __name__ == '__main__':
    main()