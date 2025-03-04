"""QGIS Unit tests for QgsBox3d.

.. note:: This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""
__author__ = 'Nyall Dawson'
__date__ = '11/04/2017'
__copyright__ = 'Copyright 2017, The QGIS Project'

import sys

import qgis  # NOQA

from qgis.core import QgsBox3d, QgsPoint, QgsRectangle
from qgis.testing import unittest


class TestQgsBox3d(unittest.TestCase):

    def testCtor(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 10.0, 11.0, 12.0)

        self.assertEqual(box.xMinimum(), 5.0)
        self.assertEqual(box.yMinimum(), 6.0)
        self.assertEqual(box.zMinimum(), 7.0)
        self.assertEqual(box.xMaximum(), 10.0)
        self.assertEqual(box.yMaximum(), 11.0)
        self.assertEqual(box.zMaximum(), 12.0)

        # this should normalize
        box = QgsBox3d(7.0, 12.0, 11.0, 5.0, 10.0, 4.0)
        self.assertEqual(box.xMinimum(), 5.0)
        self.assertEqual(box.yMinimum(), 10.0)
        self.assertEqual(box.zMinimum(), 4.0)
        self.assertEqual(box.xMaximum(), 7.0)
        self.assertEqual(box.yMaximum(), 12.0)
        self.assertEqual(box.zMaximum(), 11.0)

        # without normalization
        box = QgsBox3d(7.0, 12.0, 11.0, 5.0, 10.0, 4.0, False)
        self.assertEqual(box.xMinimum(), 7.0)
        self.assertEqual(box.yMinimum(), 12.0)
        self.assertEqual(box.zMinimum(), 11.0)
        self.assertEqual(box.xMaximum(), 5.0)
        self.assertEqual(box.yMaximum(), 10.0)
        self.assertEqual(box.zMaximum(), 4.0)

        box = QgsBox3d(QgsPoint(5, 6, 7), QgsPoint(10, 11, 12))
        self.assertEqual(box.xMinimum(), 5.0)
        self.assertEqual(box.yMinimum(), 6.0)
        self.assertEqual(box.zMinimum(), 7.0)
        self.assertEqual(box.xMaximum(), 10.0)
        self.assertEqual(box.yMaximum(), 11.0)
        self.assertEqual(box.zMaximum(), 12.0)

        # point constructor should normalize by default
        box = QgsBox3d(QgsPoint(10, 11, 12), QgsPoint(5, 6, 7))
        self.assertEqual(box.xMinimum(), 5.0)
        self.assertEqual(box.yMinimum(), 6.0)
        self.assertEqual(box.zMinimum(), 7.0)
        self.assertEqual(box.xMaximum(), 10.0)
        self.assertEqual(box.yMaximum(), 11.0)
        self.assertEqual(box.zMaximum(), 12.0)

        box = QgsBox3d(QgsPoint(10, 11, 12), QgsPoint(5, 6, 7), False)
        self.assertEqual(box.xMinimum(), 10.0)
        self.assertEqual(box.yMinimum(), 11.0)
        self.assertEqual(box.zMinimum(), 12.0)
        self.assertEqual(box.xMaximum(), 5.0)
        self.assertEqual(box.yMaximum(), 6.0)
        self.assertEqual(box.zMaximum(), 7.0)

        box = QgsBox3d(QgsRectangle(5, 6, 11, 13))
        self.assertEqual(box.xMinimum(), 5.0)
        self.assertEqual(box.yMinimum(), 6.0)
        self.assertTrue(box.zMinimum() != box.zMinimum())
        self.assertEqual(box.xMaximum(), 11.0)
        self.assertEqual(box.yMaximum(), 13.0)
        self.assertTrue(box.zMaximum() != box.zMaximum())

        box = QgsBox3d(QgsRectangle(5, 6, 11, 13), -7.0, 9.0)
        self.assertEqual(box.xMinimum(), 5.0)
        self.assertEqual(box.yMinimum(), 6.0)
        self.assertEqual(box.zMinimum(), -7.0)
        self.assertEqual(box.xMaximum(), 11.0)
        self.assertEqual(box.yMaximum(), 13.0)
        self.assertEqual(box.zMaximum(), 9.0)

        box = QgsBox3d(QgsRectangle(5, 6, 11, 13), 12.0, 5.0, False)
        self.assertEqual(box.xMinimum(), 5.0)
        self.assertEqual(box.yMinimum(), 6.0)
        self.assertEqual(box.zMinimum(), 12.0)
        self.assertEqual(box.xMaximum(), 11.0)
        self.assertEqual(box.yMaximum(), 13.0)
        self.assertEqual(box.zMaximum(), 5.0)

    def testSetters(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 10.0, 11.0, 12.0)

        box.setXMinimum(35.0)
        box.setYMinimum(36.0)
        box.setZMinimum(37.0)
        box.setXMaximum(40.0)
        box.setYMaximum(41.0)
        box.setZMaximum(42.0)
        self.assertEqual(box.xMinimum(), 35.0)
        self.assertEqual(box.yMinimum(), 36.0)
        self.assertEqual(box.zMinimum(), 37.0)
        self.assertEqual(box.xMaximum(), 40.0)
        self.assertEqual(box.yMaximum(), 41.0)
        self.assertEqual(box.zMaximum(), 42.0)

    def testSetMinimal(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 10.0, 11.0, 12.0)
        box.setMinimal()
        self.assertEqual(box.xMinimum(), sys.float_info.max)
        self.assertEqual(box.yMinimum(), sys.float_info.max)
        self.assertEqual(box.zMinimum(), sys.float_info.max)
        self.assertEqual(box.xMaximum(), -sys.float_info.max)
        self.assertEqual(box.yMaximum(), -sys.float_info.max)
        self.assertEqual(box.zMaximum(), -sys.float_info.max)

    def testNormalize(self):
        box = QgsBox3d()
        box.setXMinimum(10.0)
        box.setYMinimum(11.0)
        box.setZMinimum(12.0)
        box.setXMaximum(5.0)
        box.setYMaximum(6.0)
        box.setZMaximum(7.0)

        box.normalize()
        self.assertEqual(box.xMinimum(), 5.0)
        self.assertEqual(box.yMinimum(), 6.0)
        self.assertEqual(box.zMinimum(), 7.0)
        self.assertEqual(box.xMaximum(), 10.0)
        self.assertEqual(box.yMaximum(), 11.0)
        self.assertEqual(box.zMaximum(), 12.0)

    def testDimensions(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        self.assertEqual(box.width(), 6.0)
        self.assertEqual(box.height(), 7.0)
        self.assertEqual(box.depth(), 8.0)

    def testIntersect(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        box2 = box.intersect(QgsBox3d(7.0, 8.0, 9.0, 10.0, 11.0, 12.0))
        self.assertEqual(box2.xMinimum(), 7.0)
        self.assertEqual(box2.yMinimum(), 8.0)
        self.assertEqual(box2.zMinimum(), 9.0)
        self.assertEqual(box2.xMaximum(), 10.0)
        self.assertEqual(box2.yMaximum(), 11.0)
        self.assertEqual(box2.zMaximum(), 12.0)
        box2 = box.intersect(QgsBox3d(0.0, 1.0, 2.0, 100.0, 111.0, 112.0))
        self.assertEqual(box2.xMinimum(), 5.0)
        self.assertEqual(box2.yMinimum(), 6.0)
        self.assertEqual(box2.zMinimum(), 7.0)
        self.assertEqual(box2.xMaximum(), 11.0)
        self.assertEqual(box2.yMaximum(), 13.0)
        self.assertEqual(box2.zMaximum(), 15.0)
        box2 = box.intersect(QgsBox3d(1.0, 2.0, 3.0, 6.0, 7.0, 8.0))
        self.assertEqual(box2.xMinimum(), 5.0)
        self.assertEqual(box2.yMinimum(), 6.0)
        self.assertEqual(box2.zMinimum(), 7.0)
        self.assertEqual(box2.xMaximum(), 6.0)
        self.assertEqual(box2.yMaximum(), 7.0)
        self.assertEqual(box2.zMaximum(), 8.0)

    def testIntersects(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        self.assertTrue(box.intersects(QgsBox3d(7.0, 8.0, 9.0, 10.0, 11.0, 12.0)))
        self.assertTrue(box.intersects(QgsBox3d(0.0, 1.0, 2.0, 100.0, 111.0, 112.0)))
        self.assertTrue(box.intersects(QgsBox3d(1.0, 2.0, 3.0, 6.0, 7.0, 8.0)))
        self.assertFalse(box.intersects(QgsBox3d(15.0, 16.0, 17.0, 110.0, 112.0, 113.0)))
        self.assertFalse(box.intersects(QgsBox3d(5.0, 6.0, 17.0, 11.0, 13.0, 113.0)))
        self.assertFalse(box.intersects(QgsBox3d(5.0, 16.0, 7.0, 11.0, 23.0, 15.0)))
        self.assertFalse(box.intersects(QgsBox3d(15.0, 6.0, 7.0, 21.0, 13.0, 15.0)))

    def testContains(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        self.assertTrue(box.contains(QgsBox3d(7.0, 8.0, 9.0, 10.0, 11.0, 12.0)))
        self.assertFalse(box.contains(QgsBox3d(0.0, 1.0, 2.0, 100.0, 111.0, 112.0)))
        self.assertFalse(box.contains(QgsBox3d(1.0, 2.0, 3.0, 6.0, 7.0, 8.0)))
        self.assertFalse(box.contains(QgsBox3d(15.0, 16.0, 17.0, 110.0, 112.0, 113.0)))
        self.assertFalse(box.contains(QgsBox3d(5.0, 6.0, 17.0, 11.0, 13.0, 113.0)))
        self.assertFalse(box.contains(QgsBox3d(5.0, 16.0, 7.0, 11.0, 23.0, 15.0)))
        self.assertFalse(box.contains(QgsBox3d(15.0, 6.0, 7.0, 21.0, 13.0, 15.0)))

    def testContainsPoint(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        self.assertTrue(box.contains(QgsPoint(6, 7, 8)))
        self.assertFalse(box.contains(QgsPoint(16, 7, 8)))
        self.assertFalse(box.contains(QgsPoint(6, 17, 8)))
        self.assertFalse(box.contains(QgsPoint(6, 7, 18)))
        # 2d containment
        self.assertTrue(box.contains(QgsPoint(6, 7)))
        self.assertFalse(box.contains(QgsPoint(16, 7)))
        self.assertFalse(box.contains(QgsPoint(6, 17)))

    def testCombineWith(self):
        # box2 contains box1
        box1 = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        box2 = QgsBox3d(2.0, 3.0, 4.0, 12.0, 15.0, 17.0)
        box1.combineWith(box2)
        self.assertEqual(box1.xMinimum(), box2.xMinimum())
        self.assertEqual(box1.yMinimum(), box2.yMinimum())
        self.assertEqual(box1.zMinimum(), box2.zMinimum())
        self.assertEqual(box1.xMaximum(), box2.xMaximum())
        self.assertEqual(box1.yMaximum(), box2.yMaximum())
        self.assertEqual(box1.zMaximum(), box2.zMaximum())

        # box3 and box4 do not intersect
        box3 = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        box4 = QgsBox3d(26.0, 23.0, 24.0, 32.0, 35.0, 37.0)
        box3.combineWith(box4)
        self.assertEqual(box3.xMinimum(), 5.0)
        self.assertEqual(box3.yMinimum(), 6.0)
        self.assertEqual(box3.zMinimum(), 7.0)
        self.assertEqual(box3.xMaximum(), box4.xMaximum())
        self.assertEqual(box3.yMaximum(), box4.yMaximum())
        self.assertEqual(box3.zMaximum(), box4.zMaximum())

        # Point is inside the box
        box5 = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        box5.combineWith(7.0, 9.0, 9.0)
        self.assertEqual(box5.xMinimum(), 5.0)
        self.assertEqual(box5.yMinimum(), 6.0)
        self.assertEqual(box5.zMinimum(), 7.0)
        self.assertEqual(box5.xMaximum(), 11.0)
        self.assertEqual(box5.yMaximum(), 13.0)
        self.assertEqual(box5.zMaximum(), 15.0)

        # Point is outside the box
        box6 = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        box6.combineWith(15.0, -2.0, 14.0)
        self.assertEqual(box6.xMinimum(), 5.0)
        self.assertEqual(box6.yMinimum(), -2.0)
        self.assertEqual(box6.zMinimum(), 7.0)
        self.assertEqual(box6.xMaximum(), 15.0)
        self.assertEqual(box6.yMaximum(), 13.0)
        self.assertEqual(box6.zMaximum(), 15.0)

    def testVolume(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        self.assertEqual(box.volume(), 336.0)

    def testToRectangle(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        rect = box.toRectangle()
        self.assertEqual(rect, QgsRectangle(5, 6, 11, 13))

    def testIs2d(self):
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        self.assertFalse(box.is2d())
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 7.0)
        self.assertTrue(box.is2d())
        box = QgsBox3d(5.0, 6.0, 0.0, 11.0, 13.0, 0.0)
        self.assertTrue(box.is2d())
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, -7.0)
        self.assertFalse(box.is2d())
        box = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, -7.0, False)
        self.assertTrue(box.is2d())
        box = QgsBox3d(5.0, 6.0, float('nan'), 11.0, 13.0, float('nan'))
        self.assertTrue(box.is2d())

    def testIs3d(self):
        box1 = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        self.assertTrue(box1.is3D())

        box2 = QgsBox3d(5.0, 6.0, 0.0, 11.0, 13.0, 0.0)
        self.assertFalse(box2.is3D())

        box3 = QgsBox3d(5.0, 6.0, 10.0, 11.0, 13.0, -10.0, False)
        self.assertFalse(box3.is3D())

    def testEquality(self):
        box1 = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        box2 = QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 15.0)
        self.assertEqual(box1, box2)
        self.assertNotEqual(box1, QgsBox3d(5.0, 6.0, 7.0, 11.0, 13.0, 14.0))
        self.assertNotEqual(box1, QgsBox3d(5.0, 6.0, 7.0, 11.0, 41.0, 15.0))
        self.assertNotEqual(box1, QgsBox3d(5.0, 6.0, 7.0, 12.0, 13.0, 15.0))
        self.assertNotEqual(box1, QgsBox3d(5.0, 6.0, 17.0, 11.0, 13.0, 15.0))
        self.assertNotEqual(box1, QgsBox3d(5.0, 16.0, 7.0, 11.0, 13.0, 15.0))
        self.assertNotEqual(box1, QgsBox3d(52.0, 6.0, 7.0, 11.0, 13.0, 15.0))

    def testScaling(self):
        box1 = QgsBox3d(-1, -1, -1, 1, 1, 1)
        box1.scale(3.0)
        self.assertEqual(box1.width(), 6.0)
        self.assertEqual(box1.height(), 6.0)
        self.assertEqual(box1.depth(), 6.0)
        self.assertEqual(box1.xMinimum(), -3.0)
        self.assertEqual(box1.yMinimum(), -3.0)
        self.assertEqual(box1.zMinimum(), -3.0)

        box2 = QgsBox3d(-1, -1, -1, 1, 1, 1)
        box2.scale(3.0, QgsPoint(-1.0, -1.0, -1.0))
        self.assertEqual(box2.width(), 6.0)
        self.assertEqual(box2.height(), 6.0)
        self.assertEqual(box2.depth(), 6.0)
        self.assertEqual(box2.xMinimum(), -1.0)
        self.assertEqual(box2.yMinimum(), -1.0)
        self.assertEqual(box2.zMinimum(), -1.0)

        box3 = QgsBox3d(-1, -1, -1, 1, 1, 1)
        box3.scale(3.0, QgsPoint(-2.0, 2.0, 0.0))
        self.assertEqual(box3.width(), 6.0)
        self.assertEqual(box3.height(), 6.0)
        self.assertEqual(box3.depth(), 6.0)
        self.assertEqual(box3.xMinimum(), 1.0)
        self.assertEqual(box3.yMinimum(), -7.0)
        self.assertEqual(box3.zMinimum(), -3.0)

    def testIsNull(self):
        box1 = QgsBox3d()
        self.assertTrue(box1.isNull())
        self.assertTrue(box1.toRectangle().isNull())

        box2 = QgsBox3d(0, 0, 0, 0, 0, 0)
        self.assertFalse(box2.isNull())

        box3 = QgsBox3d(1, 1, 1, 1, 1, 1)
        self.assertFalse(box3.isNull())

        box4 = QgsBox3d(5, 6, 7, 12, 13, 14)
        self.assertFalse(box4.isNull())

        box5 = QgsBox3d(5, 6, float('nan'), 12, 13, float('nan'))
        self.assertFalse(box5.isNull())

        box6 = QgsBox3d(0, 0, float('nan'), 0, 0, float('nan'))
        self.assertFalse(box6.isNull())

        box7 = QgsBox3d(0, 0, float('nan'), 0, 0, float('nan'))
        self.assertFalse(box7.isNull())

        box8 = QgsBox3d(0, 6, 8, 0, 13, 14)
        self.assertFalse(box8.isNull())

        box9 = QgsBox3d(5, 0, 7, 12, 0, 14)
        self.assertFalse(box9.isNull())

        box10 = QgsBox3d(5, 6, 0, 12, 13, 0)
        self.assertFalse(box10.isNull())

        box11 = QgsBox3d(
            sys.float_info.max, sys.float_info.max, sys.float_info.max,
            -sys.float_info.max, -sys.float_info.max, -sys.float_info.max, False)
        self.assertTrue(box11.isNull())

    def testIsEmpty(self):
        box1 = QgsBox3d()
        self.assertTrue(box1.isEmpty())

        box2 = QgsBox3d(0, 0, 0, 0, 0, 0)
        self.assertTrue(box2.isEmpty())

        box3 = QgsBox3d(1, 1, 1, 1, 1, 1)
        self.assertTrue(box3.isEmpty())

        box4 = QgsBox3d(5, 6, 7, 12, 13, 14, False)
        self.assertFalse(box4.isEmpty())

        # zMin > zMax
        box5 = QgsBox3d(5, 6, 7, 12, 13, 2, False)
        self.assertTrue(box5.isEmpty())

        # zMin == zMax
        box6 = QgsBox3d(5, 6, 7, 12, 13, 7, False)
        self.assertTrue(box6.isEmpty())

        # xMin > xMax
        box7 = QgsBox3d(5, 6, 7, -20, 13, 14, False)
        self.assertTrue(box7.isEmpty())

        # yMin > yMax
        box8 = QgsBox3d(5, 6, 7, 12, 2, 14, False)
        self.assertTrue(box8.isEmpty())

    def testToString(self):
        box1 = QgsBox3d()
        self.assertEqual(box1.toString(), "Null")

        box2 = QgsBox3d(0, 0, 0, 0, 0, 0)
        self.assertEqual(box2.toString(), "Empty")

        box3 = QgsBox3d(1, 1, 1, 1, 1, 1)
        self.assertEqual(box3.toString(), "Empty")

        box4 = QgsBox3d(1, 2, 3, 4, 5, 6)
        self.assertEqual(
            box4.toString(),
            ("1.0000000000000000,2.0000000000000000,3.0000000000000000 : "
             "4.0000000000000000,5.0000000000000000,6.0000000000000000"))

        box3 = QgsBox3d(1.451845, 2.8543302, 3.3490346, 4.654983, 5.5484343, 6.4567982)
        self.assertEqual(
            box3.toString(3),
            "1.452,2.854,3.349 : 4.655,5.548,6.457")


if __name__ == '__main__':
    unittest.main()
