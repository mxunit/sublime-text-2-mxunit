import unittest
import json
from pprint import pprint

class MXUnitTest(unittest.TestCase):
	
	def test_read_json_data(self):
		test_results=open('./test_results_fixture.json').read()
		print self.pretty_results(test_results)
		return

	

	def pretty_results(self,test_results):
		_results = ''
		tests = json.loads(test_results)
		pprint( len(tests) )

		for test in tests:
			_results += '\n%s.%s : status=%s\n' % (test['COMPONENT'],test['TESTNAME'], test['TESTSTATUS'] ) 
			if( test['DEBUG'] ):
				_debug = test['DEBUG']
				i=0
				for var in _debug:
					# print '%s = %s' % ( var, _debug[i] )
					_results += ">>Debug: %s" % (var) 
				
			_results += '\n/---------------------------------------------------------------/'
		return _results
    
    