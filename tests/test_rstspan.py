import unittest

from dashtable import data2rst, grid2data

class TestSpans(unittest.TestCase):
    def setUp(self) -> None:
        self.span_table1 = '''\
+-----+--------+-------+
| 0,0 | 0,1    | 0,2   |
+=====+========+=======+
| 1,0 | 1,1    | 1,2   |
+-----+--------+-------+
| 2,0 | 2,1        2,2 |
|     |                |
+-----+ 3,1        3,2 |
| 3,0 |                |
|     +--------+-------+
| 4,0 | 4,1    | 4,2   |
+-----+--------+-------+'''

        self.table1, self.spans1, self.header1 = grid2data(self.span_table1)

        self.span_table2 = data2rst(self.table1, self.spans1, self.header1)
        self.table2, self.spans2, self.header2 = grid2data(self.span_table2)

    def test_table_parse(self):
        self.assertMultiLineEqual(self.span_table1, self.span_table2, "Tables' RST do not match.")

    def test_table_contents(self):
        self.assertEqual(len(self.table1), len(self.table2), 'Row lengths do not match.')
        for row1, row2 in zip(self.table1, self.table2):
            self.assertEqual(len(row1), len(row2), 'Column lengths do not match.')

    def test_spans(self):
        self.assertEqual(self.spans1, self.spans2, "Tables' spans do not match.")

    def test_header(self):
        self.assertEqual(self.header1, self.header2, "Tables' header flags do not match.")

if __name__ == '__main__':
    unittest.main()