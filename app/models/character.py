class Character:

    def __init__(self, name: str, realm: str, region: str, wow_class: str, role: dict, runs: list[dict], score: float):
        self._name = name
        self._realm = realm
        self._region = region
        self._wow_class = wow_class
        self._role = role
        self._runs = runs
        self._score = score

    @property
    def name(self):
        return self._name

    @property
    def realm(self):
        return self._realm

    @property
    def region(self):
        return self._region

    @property
    def wow_class(self):
        return self._wow_class

    @property
    def role(self):
        return self._role

    @property
    def runs(self):
        return self._runs

    @property
    def score(self):
        return self._score

    def __str__(self):
        return str({"name": self.name, "realm": self.realm, "region": self.region, "wow_class": self.wow_class, "role": self.role, "runs": self.runs})
