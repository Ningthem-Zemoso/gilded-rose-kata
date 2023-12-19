from item import Item
from updators import UPDATOR_MAPPER, BaseUpdator, NormalItemUpdator

   
class GildedRose:
    """Gilded Rose Shop main items handler"""
    def __init__(self, items: list[Item]):
        self.items = items

    def update_quality(self):
        for item in self.items:
            UpdatorClass = UPDATOR_MAPPER.get(item.name, NormalItemUpdator)
            _instance: BaseUpdator = UpdatorClass()
            _instance.update(item)
