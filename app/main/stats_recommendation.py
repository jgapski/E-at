from datetime import datetime
import functools
import operator


class StatsRecommendation():
    def __init__(self):
        self.conn = "conn"

    def create_recommendations(self, user:str) -> [str]:
        history = self.get_history(user)
        last_24_h_history = self.filter_last_24_h(history)
        accumulated = self.accumulate(last_24_h_history)
        recommendations = self.do_recommendations(accumulated)
        return recommendations

    def guideline_daily_amount(self):
        return {
            'calories': 2000,
            'fat': 70,
            'carbs': 270,
            'protin': 50,
            'fiber': 25
        }

    def do_recommendations(self, accumulated):
        recommendations = []
        if accumulated['calories'] > self.guideline_daily_amount()['calories']:
            recommendations.append('You eat too many calories already!')
        else:
            recommendations.append('You need to eat more.')
        # TODO add more recomendations
        return recommendations

    def get_history(self, user):
        # TODO actually implement (get from DB)
        now = datetime.now()
        history = {
            'user': "Andrzej",
            'meals':
            [
                {
                    'date': datetime.timestamp(now),
                    'food': 'pizza',
                    'calories': 1,
                    'fat': 9.8,
                    'carbs': 33.6,
                    'protin': 12.3,
                    'fiber': 1.8
                },
                                {
                    'date': datetime.timestamp(now),
                    'food': 'pizza',
                    'calories': 2,
                    'fat': 9.8,
                    'carbs': 33.6,
                    'protin': 12.3,
                    'fiber': 1.8
                }

            ]
        }
        return history

    def filter_last_24_h(self, history):
        # TODO implement
        return history['meals']

    def accumulate(self, last_24_h_history):
        acc = {
            'calories': 0,
            'fat': 0,
            'carbs': 0,
            'protin': 0,
            'fiber': 0
        }
        return functools.reduce(lambda x, y: self.add(x, y), last_24_h_history)

    def add(self, a, b):
        a['calories'] += b['calories']
        a['fat'] += b['fat']
        a['carbs'] += b['carbs']
        a['protin'] += b['protin']
        a['fiber'] += b['fiber']
        return a
