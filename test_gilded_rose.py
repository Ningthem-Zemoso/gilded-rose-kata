import unittest
from gilded_rose import GildedRose
from item import Item

class GildedRoseTest(unittest.TestCase):
    @staticmethod
    def bulk_updater(obj: GildedRose, times: int = 1) -> None:
        for _ in range(times):
            obj.update_quality()
    def test_normal_item(self) -> None:
        item = Item("Mountain Dew", 20, 40)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual("Mountain Dew", item.name)
        self.assertEqual(item.sell_in, 19)
        self.assertEqual(item.quality, 39)
        GildedRoseTest.bulk_updater(gilded_rose, item.sell_in + 1)
        # sell by date passed
        self.assertEqual(item.sell_in, -1)
        # Quality degrades twice as fast now
        self.assertEqual(item.quality, 18)
        GildedRoseTest.bulk_updater(gilded_rose, 10)
        self.assertEqual(item.quality, 0)  # never be less than 0
        self.assertEqual(item.sell_in, -11)
    def test_aged_brie(self) -> None:
        item = Item("Aged Brie", 20, 20)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual("Aged Brie", item.name)
        self.assertEqual(item.sell_in, 19)
        self.assertEqual(item.quality, 21)
        GildedRoseTest.bulk_updater(gilded_rose, item.sell_in + 1)
        # sell by date passed
        self.assertEqual(item.sell_in, -1)
        # Quality increases twice as fast now
        self.assertEqual(item.quality, 42)
        GildedRoseTest.bulk_updater(gilded_rose, 10)
        self.assertEqual(item.quality, 50)  # never be more than 50
        self.assertEqual(item.sell_in, -11)
    def test_sulfuras(self) -> None:
        item = Item("Sulfuras, Hand of Ragnaros", 20, 80)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual("Sulfuras, Hand of Ragnaros", item.name)
        self.assertNotEqual(item.sell_in, 19)
        self.assertEqual(item.sell_in, 20)  # does not change
        self.assertEqual(item.quality, 80)  # never alters
        GildedRoseTest.bulk_updater(gilded_rose, item.sell_in + 1)
        # sell by date passed
        self.assertEqual(item.sell_in, 20)  # still same
        self.assertNotEqual(item.sell_in, -1)  # it is not equal so passes
    def test_backstage_passes(self) -> None:
        item = Item("Backstage passes to a TAFKAL80ETC concert", 20, 20)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual("Backstage passes to a TAFKAL80ETC concert", item.name)
        self.assertEqual(item.sell_in, 19)
        self.assertEqual(item.quality, 21)
        GildedRoseTest.bulk_updater(gilded_rose, 9)
        # sellin approaches to 10 or less
        self.assertEqual(item.sell_in, 10)
        self.assertEqual(item.quality, 30)
        GildedRoseTest.bulk_updater(gilded_rose)
        self.assertEqual(item.sell_in, 9)
        self.assertEqual(item.quality, 32)
        # sellin approaches to 5 or less
        GildedRoseTest.bulk_updater(gilded_rose, 4)
        self.assertEqual(item.sell_in, 5)
        self.assertEqual(item.quality, 40)
        GildedRoseTest.bulk_updater(gilded_rose)
        self.assertEqual(item.sell_in, 4)
        self.assertEqual(item.quality, 43)
        GildedRoseTest.bulk_updater(gilded_rose, 2)
        self.assertEqual(item.sell_in, 2)
        self.assertEqual(item.quality, 49)
        # corner cases: never gets beyond 50 and drops to 0 once sellin passed
        GildedRoseTest.bulk_updater(gilded_rose)
        self.assertEqual(item.sell_in, 1)
        self.assertEqual(item.quality, 50)
        GildedRoseTest.bulk_updater(gilded_rose, 2)
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 0)

    def test_conjured(self) -> None:
        item = Item("Conjured Mana Cake", 20, 50)
        gilded_rose = GildedRose([item])
        gilded_rose.update_quality()
        self.assertEqual("Conjured Mana Cake", item.name)
        self.assertEqual(item.sell_in, 19)
        self.assertEqual(item.quality, 48)
        GildedRoseTest.bulk_updater(gilded_rose, item.sell_in + 1)
        # sell by date passed -- will decrease twice as fast as normal items (-4)
        self.assertEqual(item.sell_in, -1)
        self.assertEqual(item.quality, 6)
        GildedRoseTest.bulk_updater(gilded_rose)
        self.assertEqual(item.sell_in, -2)
        self.assertEqual(item.quality, 2)
        GildedRoseTest.bulk_updater(gilded_rose)
        self.assertEqual(item.sell_in, -3)
        self.assertEqual(item.quality, 0)   # never less than 0

if __name__ == '__main__':
    unittest.main()