from datetime import datetime, timedelta
import functools
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

class StatsRecommendation():
    def __init__(self):
        self.conn = "conn"

    def render(self, history):
        history_stats = list(map(lambda x: x['stats'], history))
        hist_size = len(history_stats)
        calories = list(map(lambda x: x['calories'], history_stats))
        fat = list(map(lambda x: x['fat'], history_stats))
        carbs = list(map(lambda x: x['carbs'], history_stats))
        protein = list(map(lambda x: x['protein'], history_stats))
        fiber = list(map(lambda x: x['fiber'], history_stats))

        plt.figure(figsize=(4, 20))

        plt.subplot(5, 1, 1)
        plt.title('calories')
        sns.lineplot(range(0, hist_size), calories)
        plt.subplot(5, 1, 2)
        plt.title('fat')
        sns.lineplot(range(0, hist_size), fat)
        plt.subplot(5, 1, 3)
        plt.title('carbs')
        sns.lineplot(range(0, hist_size), carbs)
        plt.subplot(5, 1, 4)
        plt.title('protein')
        sns.lineplot(range(0, hist_size), protein)
        plt.subplot(5, 1, 5)
        plt.title('fiber')
        sns.lineplot(range(0, hist_size), fiber)

        plt.savefig("nt_plots.jpg")

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
            'protein': 50,
            'fiber': 25
        }

    def do_recommendations(self, accumulated):
        recommendations = []
        for nutrsioan in self.guideline_daily_amount().keys():
            if accumulated[nutrsioan] > self.guideline_daily_amount()[nutrsioan]:
                recommendations.append('You eat too many '+ str(nutrsioan) +' already!')
            else:
                recommendations.append('You should consume more ' + str(nutrsioan))
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
        a['protein'] += b['protein']
        a['fiber'] += b['fiber']
        return a