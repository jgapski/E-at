class StatisticsRepository:

    def __init__(self, m_db):
        self.stats_collection = m_db['statistics']

    def put_statistics(self, username, timestamp, stats):
        self.stats_collection.insert_one({"username": username, "timestamp": timestamp, "stats": stats})

    def find_for_user(self, username):
        list(self.stats_collection.find({"username": username}))
