"""
This should take the current file (or selected from navigator) and pass it to
MXUnit, who will return a TestResult (JSON or Text). The plugin should then
display the results in s Sublime way.
"""
 
import os
import json
import datetime
import re
from urllib2 import urlopen,HTTPError
import sublime_plugin
import sublime


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseCommand(sublime_plugin.TextCommand):

	def __init__(self, view):
		global_settings = sublime.load_settings("mxunit.settings")
		self.last_run_settings = sublime.load_settings("mxunit-last-run.sublime-settings")
		self.server = global_settings.get('server', 'localhost')
		self.view = view
		self.output_view = None
		#grab the runner config items
		self.port = global_settings.get('port', '80')
		self.web_root = global_settings.get('web_root', '/var/www/html/')
		self._win = None
		self.test_items = { 'test-1':{'url':'AAAAAA'},
							'test-2':{'url':'BBBBBB'},
							'test-3':{'url':'CCCCCC'},
							}
	
	
	def show_qp(self):
		panel_items = []
		self.view.window().show_quick_panel(self.test_items.keys(), self.on_done)	
	

	def on_done(self,selected_item):
		keys = self.test_items.keys()
		key = keys[selected_item]
		print  self.test_items[ key ]
	

	def run_test(self, url, edit):
		try:
			_res = urlopen(url)
			self._win = self.view.window()
			self._results = _res.read()
			self.save_test_run(url)
			
			self.view.window().run_command("show_panel", {"panel": "output.tests"})
			self.output_view = self.view.window().get_output_panel("tests")
			#self.show_tests_panel()
			self.output_view.insert( edit, self.output_view.size(), pretty_results(self._results) ) 

			# print self.output_view.viewport_extent()
			_debug_regions = self.output_view.find_all('>>Debug:.*<<$')

			print _debug_regions
			# self.output_view.fold(_debug_regions)
			# mark = [s for s in _debug_regions]
			# self.output_view.add_regions("mark", mark, "debug", "bookmark") 
											# sublime.HIDDEN | sublime.PERSISTENT)
			# self.output_view.fold(_debug_regions)


		except HTTPError as e:
			sublime.error_message ('\nRuh roh, Raggy. Are you sure this is a valid MXUnit test?\n\n%s' % e)

	
	#saves it to Packages/User ...?
	def save_test_run(self, url):
		print 'Saving url: %s' % url
		self.last_run_settings.set("last_test_run", url)
		sublime.save_settings("mxunit-last-run.sublime-settings")
		print self.last_run_settings.get('last_test_run')



class ShowQpCommand(BaseCommand):

	def run(self,edit):
		self.show_qp()	

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MxunitCommand(BaseCommand):

	def run(self,edit):
		_view = self.view
		_current_file = _view.file_name()
		#test
		_test_cfc = _current_file.replace(self.web_root, '')
		print 'Test: %s' % _test_cfc
		_url = 'http://' + self.server + ':' + self.port + '/' + _test_cfc +'?method=runtestremote&output=json'
		self.run_test(_url, edit)
		




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RunLastTestCommand(BaseCommand):

	def run(self,edit):
		_url = self.last_run_settings.get("last_test_run")
		self.run_test(_url, edit)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SingleTestCommand(BaseCommand):

	def run(self,edit):
		_view = self.view
		for region in _view.sel():
			line = _view.line(region)
			line_contents = _view.substr(line) + '\n'
			test_method = parse_line(line_contents)
		
		_current_file = _view.file_name()
		#test
		_test_cfc = _current_file.replace(self.web_root, '')
		print 'Test: %s - %s' %  (_test_cfc, test_method,)
		if test_method == '' : 
			sublime.error_message ('\nRuh roh, Raggy. The line the cursor is on doesn\'t look like a test.\n\n')
			return
		_url = 'http://' + self.server + ':' + self.port + '/' + _test_cfc +'?method=runtestremote&output=json&testmethod=' + test_method
		self.run_test(_url, edit)






#########################################################################################
#                                                                                       #
#           Utility methods used by all classes (could be in BaseCommand)               #
#                                                                                       #  
#########################################################################################

def pretty_results(test_results):
	_results = '__________________________________________________________________________________\n\n'
	_results += '		:::::::   MXUnit Test Results  :::::::     \n\n'
	#_results += '__________________________________________________________________________\n\n'
	tests = json.loads(test_results)
	passed =  len( [ x for x in tests if x['TESTSTATUS']=='Passed'] )
	failed =  len( [ x for x in tests if x['TESTSTATUS']=='Failed'] )
	errors =  len( [ x for x in tests if x['TESTSTATUS']=='Error'] )
	_results += '		Passed: %s, Failed: %s, Errors: %s\n' % (passed,failed,errors)
	_results += '		Date:  %s\n' % (datetime.datetime.now().strftime("%A, %B %d, %Y, %I:%M %p"))
	_results += '__________________________________________________________________________________\n\n'

	#To Do: Calculate totals --total, errors, failures, time
	#pprint( len(tests) )

	for test in tests:
		_results += '	%s.%s (%s)\n' % (test['COMPONENT'],test['TESTNAME'], test['TESTSTATUS'] ) 
		if( test['DEBUG'] ):
			_debug = test['DEBUG']
			i=0
			for var in _debug:
				# print '%s = %s' % ( var, _debug[i] )
				_results += "		Debug: %s \n" % ( var['VAR'] )  
			
		_results += '\n|--------------------------------------------------------------------------------\n'
	
	_results += '\n__________________________________________________________________________________\n\n'
	_results += 'Test results:  Passed=%s, Failed=%s, Errors=%s\n' % (passed,failed,errors)
	return _results



def print_debug(data):
	db = ''


def parse_line(line):
	"""
	From a line of text gets the function name (Only with script. Not tags, yet)
	"""
	pattern = re.compile("""
		(private|package|remote|public)*[ ]*
		(any|string|array|numeric|boolean|component|struct|void)*[ ]*
		function[ ]+([_\-a-z][a-z0-9_\-]+)
		""", 
		re.VERBOSE|re.MULTILINE|re.IGNORECASE)
	m = pattern.match(line)
	#return the 4th gouped regex, which should be the function name
	ret_val =  m.group(3) if m else ''
	return ret_val

