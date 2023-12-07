import unittest

from EventDataSegment import EventDataSegment
from JsonToWegsegmentProcessor import JsonToWegsegmentProcessor
from WegLocatieData import WegLocatieData


class JsonToWegsegmentProcessorTests(unittest.TestCase):
    list_segmenten = [
        EventDataSegment(begin=WegLocatieData(ident8='R9010001', positie=0.0, afstand=0.0, opschrift=0.0),
                         eind=WegLocatieData(ident8='R9010001', positie=1.0, afstand=0.0, opschrift=1.0)),
        EventDataSegment(begin=WegLocatieData(ident8='N0010001', positie=0.0, afstand=0.0, opschrift=0.0),
                         eind=WegLocatieData(ident8='N0010001', positie=1.0, afstand=0.0, opschrift=1.0)),
        EventDataSegment(begin=WegLocatieData(ident8='N0010001', positie=3.0, afstand=0.0, opschrift=3.0),
                         eind=WegLocatieData(ident8='N0010001', positie=4.0, afstand=0.0, opschrift=4.0)),
        EventDataSegment(begin=WegLocatieData(ident8='N0010002', positie=0.0, afstand=0.0, opschrift=0.0),
                         eind=WegLocatieData(ident8='N0010002', positie=1.0, afstand=0.0, opschrift=1.0)),
        EventDataSegment(begin=WegLocatieData(ident8='N0010002', positie=0.005, afstand=5.0, opschrift=0.0),
                         eind=WegLocatieData(ident8='N0010002', positie=0.995, afstand=-5.0, opschrift=1.0)),
        EventDataSegment(begin=WegLocatieData(ident8='N0010001', positie=0.005, afstand=5.0, opschrift=0.0),
                         eind=WegLocatieData(ident8='N0010001', positie=0.995, afstand=-5.0, opschrift=1.0)),
        EventDataSegment(begin=WegLocatieData(ident8='N0010002', positie=0.5, afstand=0.0, opschrift=0.5),
                         eind=WegLocatieData(ident8='N0010002', positie=1.005, afstand=5.0, opschrift=1.0)),
        EventDataSegment(begin=WegLocatieData(ident8='N0010002', positie=0.0, afstand=0.0, opschrift=0.0),
                         eind=WegLocatieData(ident8='N0010002', positie=0.995, afstand=-5.0, opschrift=1.0)),
        EventDataSegment(begin=WegLocatieData(ident8='N0010002', positie=0.1, afstand=0.0, opschrift=0.1),
                         eind=WegLocatieData(ident8='N0010002', positie=0.2, afstand=0.0, opschrift=0.2)),
        EventDataSegment(begin=WegLocatieData(ident8='N0010002', positie=0.9, afstand=0.0, opschrift=0.9),
                         eind=WegLocatieData(ident8='N0010002', positie=0.995, afstand=-5.0, opschrift=1.0)),
    ]

    def test_keep_one_side_2_different_ident8(self):
        segmenten_to_test = [self.list_segmenten[0], self.list_segmenten[1]]
        result = JsonToWegsegmentProcessor.keep_one_side(segmenten_to_test)

        self.assertListEqual(result, segmenten_to_test)

    def test_keep_one_side_2_identical_ident8(self):
        segmenten_to_test = [self.list_segmenten[1], self.list_segmenten[2]]
        result = JsonToWegsegmentProcessor.keep_one_side(segmenten_to_test)

        self.assertListEqual(result, segmenten_to_test)

    def test_keep_one_side_2_matching_ident8(self):
        segmenten_to_test = [self.list_segmenten[1], self.list_segmenten[3]]
        result = JsonToWegsegmentProcessor.keep_one_side(segmenten_to_test)

        self.assertListEqual(result, [segmenten_to_test[0]])

    def test_keep_one_side_2_matching_ident8_2nd_within_bounds(self):
        segmenten_to_test = [self.list_segmenten[1], self.list_segmenten[4]]
        result = JsonToWegsegmentProcessor.keep_one_side(segmenten_to_test)

        self.assertListEqual(result, [segmenten_to_test[0]])

    def test_keep_one_side_2_matching_ident8_2nd_within_bounds_matching_begin(self):
        segmenten_to_test = [self.list_segmenten[1], self.list_segmenten[7]]
        result = JsonToWegsegmentProcessor.keep_one_side(segmenten_to_test)

        self.assertListEqual(result, [segmenten_to_test[0]])

    def test_keep_one_side_2_matching_ident8_1st_within_bounds(self):
        segmenten_to_test = [self.list_segmenten[3], self.list_segmenten[5]]
        result = JsonToWegsegmentProcessor.keep_one_side(segmenten_to_test)

        self.assertListEqual(result, [segmenten_to_test[0]])

    def test_keep_one_side_2_matching_ident8_2nd_within_bounds_slightly_off(self):
        segmenten_to_test = [self.list_segmenten[1], self.list_segmenten[6]]
        result = JsonToWegsegmentProcessor.keep_one_side(segmenten_to_test)

        self.assertListEqual(result, [segmenten_to_test[0]])

    def test_keep_one_side_2_matching_ident8_2_other_within_bounds(self):
        segmenten_to_test = [self.list_segmenten[1], self.list_segmenten[8], self.list_segmenten[9]]
        result = JsonToWegsegmentProcessor.keep_one_side(segmenten_to_test)

        self.assertListEqual(result, [segmenten_to_test[0]])