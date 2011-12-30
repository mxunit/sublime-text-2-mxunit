"""
This should take the current file (or selected from navigator) and pass it to
MXUnit, who will return a TestResult (JSON or Text). The plugin should then
display the results in s Sublime way.
"""
 
import os
import tempfile
import json
import datetime
import re
import ConfigParser
from urllib2 import urlopen,HTTPError
import sublime_plugin


#To be specified by developer in a text file ... or can we prompt them here and 
#then save it to disk?
# server = 'localhost'
# port = '8301'
# component_root = '/'
# web_root = '/home/billy/software/jrun4/servers/dev/cfusion.ear/cfusion.war/'
# test_cfc = 'balisong/BalisongTest.cfc'



class mxunit_command(sublime_plugin.TextCommand):

	output_view = None
	#grab the runner config items
	config = ConfigParser.ConfigParser()
	config.read('./mxunit.config')
	server = config.get('mxunit', 'server')
	port = config.get('mxunit', 'port')
	web_root = config.get('mxunit', 'web_root')

	_win = None
	_edit = None
	_results = None

	def run(self,edit):
		
		view = self.view
		current_file = view.file_name()
		#test
		_test_cfc = current_file.replace(self.web_root, '')

		#temp
		# _test_cfc = 'balisong/BalisongTest.cfc'


		print 'Test: %s' % _test_cfc
		u = 'http://' + self.server + ':' + self.port + '/' + _test_cfc +'?method=runtestremote&output=json'
		self._edit = edit

		
		try:
			_res = urlopen(u)
			self._win = view.window()
			self._results = _res.read()
			view.window().run_command("show_panel", {"panel": "output.tests"})
			self.output_view = view.window().get_output_panel("tests")
			self.output_view.insert( edit, self.output_view.size(), self.pretty_results(self._results) ) 

		except HTTPError as e:
			sublime.error_message ('\nRuh roh, Raggy. Are you sure this is a valid MXUnit test?\n\n%s' % e)
		
		# self.view.window().show_quick_panel( [0,1,2,3,4], self.onSelect, sublime.MONOSPACE_FONT)
		
		# return 1
		#Good for running adhoc tests
		#view.window().show_input_panel('Yo. Which test do you want to run? ', '/path/to/test.cfc', None, None, None)
		#return
	


	def pretty_results(self,test_results):
		_results = '________________________________________________________\n\n'
		_results += '    :::::::   MXUnit Test Results  :::::::     \n'
		_results += '________________________________________________________\n\n'
		_results += '  Date:  %s\n' % (datetime.datetime.now())
		tests = json.loads(test_results)
		passed =  len( [ x for x in tests if x['TESTSTATUS']=='Passed'] )
		failed =  len( [ x for x in tests if x['TESTSTATUS']=='Failed'] )
		errors =  len( [ x for x in tests if x['TESTSTATUS']=='Error'] )
		_results += '  Passed: %s, Failed: %s, Errors: %s\n' % (passed,failed,errors)
		_results += '________________________________________________________\n'

		#To Do: Calculate totals --total, errors, failures, time
		#pprint( len(tests) )

		for test in tests:
			_results += '\n  %s.%s : status=%s\n' % (test['COMPONENT'],test['TESTNAME'], test['TESTSTATUS'] ) 
			if( test['DEBUG'] ):
				_debug = test['DEBUG']
				i=0
				for var in _debug:
					# print '%s = %s' % ( var, _debug[i] )
					_results += " >>Debug: %s\n\n" % (var) 
				
			_results += '\n|--------------------------------------------------------------------------------\n'
		
		_results += '\n________________________________________________________\n'
		_results += 'Test results:  Passed=%s, Failed=%s, Errors=%s\n' % (passed,failed,errors)
		return _results

	


	def parse_line(self,line):
		pattern = re.compile("""
			(private|package|remote|public)*[ ]*
			(any|string|array|numeric|boolean|component|struct|void)*[ ]*
			function[ ]+([a-z][a-z0-9_\-]+)
			""", 
			re.VERBOSE|re.MULTILINE|re.IGNORECASE)
		m = pattern.match(line)
		#return the 4th gouped regex, which should be the function name
		return m.group(3)


	
	def append(self, text, panel_name = 'example'):
		_view = self.view.window().get_output_panel(panel_name)
		_view.run_command("show_panel", {"panel": "output." + panel_name})	
		# return

		# if not hasattr(self, 'output_view'): 
		# 	self.output_view = self.window.get_output_panel(panel_name)
		# 	# _view = self.window.get_output_panel(panel_name)
		
		# _view = self.output_view

  #    	# Write this text to the output panel and display it
  #   	edit = _view.begin_edit()
  #   	_view.insert(edit, v.size(), text + '\n')
  #   	_view.end_edit(edit)
  #   	_view.show(v.size())
    	# self.view.window().run_command("show_panel", {"panel": "output." + panel_name})	
	

