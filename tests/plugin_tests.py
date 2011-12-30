import sys
sys.path.append('../')
sys.path.append('/home/billy/programs/Sublime Text 2/')
import re
import unittest
import json
from pprint import pprint
from mxunit_plugin import mxunit_command



class MXUnitTest(unittest.TestCase):
	
	def test_read_json_data(self):
		test_results=open('tests/test_results_fixture.json').read()
		# pprint (test_results)
	
	#To Do: Hanlde cffunction name="asdasd" . HTML attribute
	def test_parse_line_for_test_method_name(self):
		line = 'function thisIs_thE_test-MEt0D_nam3(asd,asd,asd)'
		cmd = mxunit_command(None)
		actual = cmd.parse_line(line)
		# actual = self.parse_line(line)
		print actual
		# return
		expected = 'thisIs_thE_test-MEt0D_nam3'
		self.assertEquals( expected,actual )


    