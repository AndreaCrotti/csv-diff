import unittest
import csvdiff

class TestCsvDiff(unittest.TestCase):

    def test_index_to_excel(self):
        idx_to_st = {
            0: 'A',
            3: 'D',
            26: 'AA',
            52: 'BA'
        }

        for val, res in idx_to_st.items():
            self.assertEqual(csvdiff.index_to_excel(val), res)

    def test_diffs(self):
        diffs = {
            (1, 1.1): 0.1,
            (0, 0): 0,
            (-1, 2): 3
        }

        for vals, diff in diffs.items():
            self.assertAlmostEqual(csvdiff.compute_diff(*vals), diff)


if __name__ == '__main__':
    unittest.main()

