import sys
sys.path.append('../')
sys.path.append('/home/billy/programs/Sublime Text 2/sublime_plugin.py')
import unittest
import json
from pprint import pprint



from mxunit_plugin import mxunit_command

class MXUnitTest(unittest.TestCase):
	
	def test_read_json_data(self):
		test_results=open('./test_results_fixture.json').read()
		print self.pretty_results(test_results)
		return
    