from datetime import datetime, timedelta
import functools
import operator


class StatsRecommendation():
    def __init__(self):
        self.conn = "conn"

    def create_recommendations(self, history):
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

    def f(self, meal):
        last_hour_date_time = datetime.now() - timedelta(hours=24)
        return meal['timestamp'] > datetime.timestamp(last_hour_date_time)

    def filter_last_24_h(self, history):
        return filter(lambda x: self.f(x), history)

    def accumulate(self, last_24_h_history):
        history_stats = map(lambda x:x['stats'], last_24_h_history)
        return functools.reduce(lambda x, y: self.add(x, y), history_stats)

    def add(self, a, b):
        a['calories'] += b['calories']
        a['fat'] += b['fat']
        a['carbs'] += b['carbs']
        a['protin'] += b['protin']
        a['fiber'] += b['fiber']
        return a