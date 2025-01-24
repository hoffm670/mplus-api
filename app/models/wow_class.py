class ClassData:

    def __init__(self, count: int, wow_class: str, spec: str, role: str):
        self._count = count
        self._wow_class = wow_class
        self._spec = spec
        self._role = role

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    @property
    def wow_class(self):
        return self._wow_class

    @property
    def spec(self):
        return self._spec

    @property
    def role(self):
        return self._role

    def to_json(self):
        return {
            "count": self.count,
            "wow_class": self.wow_class,
            "spec": self.spec,
            "role": self.role
        }

    def __str__(self):
        return str(self.to_json())
