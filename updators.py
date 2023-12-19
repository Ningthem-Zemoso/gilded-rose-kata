from abc import ABC, abstractmethod
from item import Item
from constants import ItemEnums, MIN_QUALITY, MAX_QUALITY

class BaseUpdator(ABC):
    """Base updator abstract class"""

    @abstractmethod
    def update(self, item: Item):
        pass


class NormalItemUpdator(BaseUpdator):
    """Updator for normal items"""

    def update(self, item: Item):
        if item.sell_in > 0:
            item.quality -= 1
        else:
            item.quality -= 2
        item.quality = max(item.quality, MIN_QUALITY)
        item.sell_in -= 1
        

class AgedBrieUpdator(BaseUpdator):
    """Updator for Aged Brie items"""

    def update(self, item: Item):
        # Increase quality by 2 if sell_in is 0 or less (past sell date), else by 1
        if item.sell_in <= 0:
            item.quality += 2
        else:
            item.quality += 1
        # Ensure quality does not exceed maximum
        item.quality = min(item.quality, MAX_QUALITY)
        # Decrease sell_in
        item.sell_in -= 1


class BackStagePassesUpdator(BaseUpdator):
    """Updator for back-stage items"""

    def update(self, item: Item):
        if MIN_QUALITY <= item.quality <= MAX_QUALITY:
            if item.sell_in <= 0:
                item.quality = 0
            else:
                if item.sell_in <= 5:
                    increase = 3
                elif item.sell_in <= 10:
                    increase = 2
                else:
                    increase = 1
                
                item.quality += increase
                item.quality = min(MAX_QUALITY, item.quality)

        item.sell_in -= 1


class ConjuredUpdator(BaseUpdator):
    """Updator for conjured items"""

    def update(self, item: Item):
        if item.sell_in > 0:
            item.quality -= 2
        else:
            item.quality -= 4
        item.quality = max(item.quality, MIN_QUALITY)
        item.sell_in -= 1


class SkipUpdator(BaseUpdator):
    """No updation required"""

    def update(self, item: Item):
        # Do nothing
        pass

UPDATOR_MAPPER = {
    ItemEnums.AGED_BRIE.value: AgedBrieUpdator,
    ItemEnums.BACKSTAGE_PASSES.value: BackStagePassesUpdator,
    ItemEnums.CONJURED_MANA_CAKE.value: ConjuredUpdator,
    ItemEnums.SULFURAS.value: SkipUpdator
}