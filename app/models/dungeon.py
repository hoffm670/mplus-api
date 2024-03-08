from repository.raider_api import RaiderApi


class Dungeon:

    def __init__(self, id, slug, name, short_name):
        self._id = id
        self._slug = slug
        self._name = name
        self._short_name = short_name

    @property
    def id(self):
        return self._id

    @property
    def slug(self):
        return self._slug

    @property
    def name(self):
        return self._name

    @property
    def short_name(self):
        return self._short_name

    def __str__(self):
        return str({"id": self.id, "slug": self.slug, "name": self.name, "short_name": self.short_name})
