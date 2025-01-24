from models.wow_class import ClassData


class MythicPlusSnapshot:

    def __init__(self, date: str, time: str, timestamp: str, region: str, season: str,
                 character_count: int, rating_cutoff: int, change: float, change_days: int,
                 dungeons: list[dict], class_data: dict[str, ClassData], score_list: list):
        self._date = date
        self._time = time
        self._timestamp = timestamp
        self._region = region
        self._season = season
        self._character_count = character_count
        self._rating_cutoff = rating_cutoff
        self._change = change
        self._change_days = change_days
        self._dungeons = dungeons
        self._class_data = class_data
        self._score_list = score_list

    @property
    def date(self):
        return self._date

    @property
    def time(self):
        return self._time

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def region(self):
        return self._region

    @property
    def season(self):
        return self._season

    @property
    def character_count(self):
        return self._character_count

    @property
    def rating_cutoff(self):
        return self._rating_cutoff

    @property
    def change(self):
        return self._change

    @property
    def change_days(self):
        return self._change_days

    @property
    def dungeons(self):
        return self._dungeons

    @property
    def class_data(self):
        return self._class_data

    @property
    def score_list(self):
        return self._score_list

    def to_json(self):
        return {
            'date': self.date,
            'time': self.time,
            'timestamp': self.timestamp,
            'region': self.region,
            'season': self.season,
            'character_count': self.character_count,
            'rating_cutoff': self.rating_cutoff,
            'change': self.change,
            'change_days': self.change_days,
            'dungeons': self.dungeons,
            'class_data': {key: val.to_json() for key, val in self.class_data.items()},
            'scores': self.score_list
        }
