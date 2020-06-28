import math
import unittest

import tsp.distance as d


class Test(unittest.TestCase):
    # Euclidean plane
    def test_euclidean_dist(self):
        self.assertEqual(d.euclidian_dist([0, 0], [0, 0]), 0)
        self.assertEqual(d.euclidian_dist([0, 0], [0, 0]), 0)
        self.assertEqual(d.euclidian_dist([0, 1], [0, 0]), 1)
        self.assertEqual(d.euclidian_dist([0, 0], [1, 1]), math.sqrt(2))
        self.assertEqual(d.euclidian_dist([0, 0], [-1, 0]), 1)
        self.assertEqual(d.euclidian_dist([0, 0], [-1, 0]), 1)
        self.assertEqual(d.euclidian_dist([-1, -1], [0, 0]), math.sqrt(2))

    # Points on unit ball (radius 1), described by latitude and longitude
    def test_orthodromic_dist(self):
        self.assertEqual(d.orthodromic_dist([0, 0], [0, 0]), 0)
        self.assertEqual(d.orthodromic_dist([0, 0], [0, 180]), 3.141592653589793)
        self.assertEqual(d.orthodromic_dist([0, 0], [0, 90]), 1.5707963267948963)
        self.assertEqual(d.orthodromic_dist([0, 0], [0, 45]), 0.7853981633974483)
        self.assertEqual(d.orthodromic_dist([45, 0], [0, 0]), 0.7853981633974483)
        self.assertEqual(d.orthodromic_dist([90, 0], [0, 0]), 1.5707963267948963)
        self.assertEqual(d.orthodromic_dist([-45, 0], [0, 0]), 0.7853981633974483)
        # Tower of London - Brandenburg Gate
        self.assertEqual(d.orthodromic_dist([-0.076132, 51.508530], [13.373298, 52.509761], 6371), 925.8725081781232)

#    def test_compute_distance_matrix(self):
#        # Euclidian example
#        d1 = [[0,math.sqrt(5),math.sqrt(5)],
#              [math.sqrt(5),0,math.sqrt(20)],
#              [math.sqrt(5),math.sqrt(20),0]]
#        self.assertListEqual(d.compute_distance_matrix([1,2,0], [2,4,0], method='euclidian').tolist(), d1)
#        # Orthodromic example
#        d2 = [[0, 404.01475184201, 8518.297],
#              [404.0148, 0, 8256.768],
#              [8518.2966, 8256.76831337012, 0]]
#        lat = [48.8534, 51.5072, 40.7142]
#        lon = [2.3488, -0.1275, -74.0059]
#        self.assertListEqual(d.compute_distance_matrix(lat, lon, method='orthodromic', radius=6371).tolist(), d2)

if __name__ == '__main__':
    unittest.main()


