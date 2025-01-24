class CutoffStats:

    def __init__(self, cutoff_score, num_eligible, change, change_days):
        self._cutoff_score = cutoff_score
        self._num_eligible = num_eligible
        self._change = change
        self._change_days = change_days

    @property
    def cutoff_score(self):
        return self._cutoff_score

    @property
    def num_eligible(self):
        return self._num_eligible

    @num_eligible.setter
    def num_eligible(self, value):
        self._num_eligible = value

    @property
    def change(self):
        return self._change

    @property
    def change_days(self):
        return self._change_days
