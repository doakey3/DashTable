import os
import sys
import unittest

file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.abspath(file_path))

import dashtable

class TestPyLRC(unittest.TestCase):
    def setUp(self):
        self.static_path = os.path.join(file_path, 'tests', 'static')
    
    
    def test_html_to_tables(self):
        for file in os.listdir(self.static_path):
            if file.endswith('.html'):
                html_path = os.path.join(self.static_path, file)
                rst = dashtable.html2rst(html_path)
                md = dashtable.html2md(html_path)
                
                rst_name = os.path.splitext(file)[0] + '.rst'
                rst_path = os.path.join(self.static_path, rst_name)
                rst_file = open(rst_path, 'r')
                rst_text = rst_file.read().rstrip()
                rst_file.close()
                
                self.assertEqual(rst, rst_text)
                
                md_name = os.path.splitext(file)[0] + '.md'
                md_path = os.path.join(self.static_path, md_name)
                md_file = open(md_path, 'r')
                md_text = md_file.read().rstrip()
                md_file.close()
                
                self.assertEqual(md, md_text)
                
        
        #self.assertEqual(1, 1)
        
if __name__ == '__main__':
    unittest.main()
