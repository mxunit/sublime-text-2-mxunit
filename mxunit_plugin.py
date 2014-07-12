"""
This should take the current file (or selected from navigator) and pass it to MXUnit, who will return a TestResult (JSON or Text).

The plugin should then display the results in s Sublime way.
"""
 
import json
import datetime
import re
from urllib.request import urlopen,HTTPError
import sublime_plugin
import sublime


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class BaseCommand(sublime_plugin.TextCommand):
	
	"""Main Command implemented by child commands."""

	def __init__(self, view):
		"""Initializing instance members."""
		global_settings = sublime.load_settings("mxunit.settings")
		self.last_run_settings = sublime.load_settings("mxunit-last-run.sublime-settings")
		self.view = view
		self.output_view = None
		#grab the runner config items
		self.port = global_settings.get('port', '80')
		self.server = global_settings.get('server', 'localhost')
		self.protocol = 'https://' if self.port == '443' else 'http://'
		self.component_root = global_settings.get('component_root', '/')
		self.web_root = global_settings.get('web_root', '/var/www/html/')
		self._win = None
		self.test_items = { 'test-1':{'url':'AAAAAA'},
							'test-2':{'url':'BBBBBB'},
							'test-3':{'url':'CCCCCC'},
							}
	
	
	def show_qp(self):
		""" Playing with quick panel. Losts of opportunities here! (Run test history, etc.). """
		self.view.window().show_quick_panel(self.test_items.keys(), self.on_done)	
	

	def on_done(self,selected_item):
		""" Playing with quick panel events. Does nothing useful."""
		keys = self.test_items.keys()
		key = keys[selected_item]
		print(self.test_items[key])
	

	def run_test(self, url, edit, show_failures_only=False):
		""" Main test runner. Intended to be called  from child command."""
		try:
			_res = urlopen(url)
			self._win = self.view.window()
			self._results = _res.read()
			self.view.window().run_command("show_panel", {"panel": "output.tests"})
			self.output_view = self.view.window().get_output_panel("tests")
			self.output_view.insert( edit, self.output_view.size(), pretty_results(self._results, show_failures_only) ) 
			self.save_test_run(url,show_failures_only)

		except HTTPError as e:
			sublime.error_message ('\nRuh roh, Raggy. Are you sure this is a valid MXUnit test?\n\n%s\n\nCheck syntax, too.\n\nTarget: %s' % (e,url) )
		
		except Exception as e:
			sublime.error_message ('\nAh Snap, Scoob. Like something went way South!\n\n%s\n\nTarget: %s' % (e,url) )

	
	
	def save_test_run(self, url, show_failures_only):
		"""
		Persist the last run test.

		To Do:  Save it as a stack with a MAX num. Stack can be displayed with the quick panel.
		"""
		print('Saving url: %s' % url)
		self.last_run_settings.set("last_test_run", url)
		self.last_run_settings.set("show_failures_only", show_failures_only)
		sublime.save_settings("mxunit-last-run.sublime-settings")
		print(self.last_run_settings.get('last_test_run'))



class ShowQpCommand(BaseCommand):

	""" 
	Just playing with the quick panel. Does nothing except confuse the user.

	To Do: 
		(1)  Could show a history of test runs and run the selected history item.
		(2)  Could display a list of valid tests in current file and run the selected one.
	"""

	def run(self,edit):
		""" Run. """
		self.show_qp()	




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class HideTestPanelCommand(BaseCommand):
	
	""" Hide the test results panel (esc works fine, but whatever...)."""
	
	def run(self,edit):
		""" Run. """
		self.view.window().run_command("hide_panel", {"panel": "output.tests"})	


class ShowTestPanelCommand(BaseCommand):
	
	""" Shows the test results panel. """
	
	def run(self,edit):
		""" Run. """
		self.view.window().run_command("show_panel", {"panel": "output.tests"})			



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class MxunitCommand(BaseCommand):
	
	""" Runs all tests in an MXUnit testcase."""
	
	def run(self,edit):
		""" Run. """
		_view = self.view
		_current_file = self.canonize( _view.file_name() )
		_web_root = self.canonize(self.web_root)
		_test_cfc = _current_file.replace(_web_root, '')
		print('Test: %s' % _test_cfc)
		_url = self.protocol + self.server + ':' + self.port + self.component_root + _test_cfc +'?method=runtestremote&output=json'
		self.run_test(_url, edit)

	def canonize(self,path):
		""" Canonize. """
		return path.replace('\\','/')
		

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RunAllFailuresOnlyCommand(BaseCommand):
	
	""" Runs all tests in an MXUnit testcase but display only failures. """
	
	def run(self,edit):
		""" Run. """
		_view = self.view
		_current_file = _view.file_name()
		#test
		_test_cfc = _current_file.replace(self.web_root, '')
		print('Test: %s' % _test_cfc)
		_url = self.protocol + self.server + ':' + self.port + self.component_root  + _test_cfc +'?method=runtestremote&output=json'
		self.run_test(_url, edit,show_failures_only=True)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class RunLastTestCommand(BaseCommand):
	
	""" Looks up the last run test and simly runs it. """
	
	def run(self,edit):
		""" Run. """
		_url = self.last_run_settings.get("last_test_run")
		_show_failures = self.last_run_settings.get("show_failures_only")
		self.run_test(_url, edit,_show_failures)



#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class SingleTestCommand(BaseCommand):
	
	"""
	Runs a single MXUnit test.

	Expect that user has placed cursor on line where test exists.
	We parse the line, extracting the test name and pass that to MXUnit.
	"""
	
	def run(self,edit):
		""" Run. """
		_view = self.view
		for region in _view.sel():
			line = _view.line(region)
			line_contents = _view.substr(line) + '\n'
			test_method = parse_line(line_contents)
		
		_current_file = _view.file_name()
		#test
		_test_cfc = _current_file.replace(self.web_root, '')
		print('Test: %s - %s' %  (_test_cfc, test_method,))
		if test_method == '' : 
			sublime.error_message ('\nRuh roh, Raggy. The line the cursor is on doesn\'t look like a test.\n\n')
			return
		_url = self.protocol + self.server + ':' + self.port + self.component_root + _test_cfc +'?method=runtestremote&output=json&testmethod=' + test_method
		self.run_test(_url, edit)






#########################################################################################
#                                                                                       #
#           Utility methods used by all classes (could be in BaseCommand)               #
#                                                                                       #  
#########################################################################################

def pretty_results(test_results, show_failures_only):
	"""
	Format JSON to string output.

	(To Do: use Python template and JSON as context)
	"""
	_results =  '__________________________________________________________________________________\n\n'
	_results += '		:::::::   MXUnit Test Results  :::::::     \n'
	tests = json.loads(test_results)
	 
	passed =  len( [ x for x in tests if x['TESTSTATUS']=='Passed'] )
	failed =  len( [ x for x in tests if x['TESTSTATUS']=='Failed'] )
	errors =  len( [ x for x in tests if x['TESTSTATUS']=='Error'] )
	
	total_time = sum([ float(x['TIME']) for x in tests ])
	_results += '		Passed: %s, Failed: %s, Errors: %s, Time: %sms\n' % (passed,failed,errors,total_time)
	_results += '		Date:  %s\n' % (datetime.datetime.now().strftime("%A, %B %d, %Y, %I:%M %p"))
	_results += '__________________________________________________________________________________\n\n'

	if show_failures_only:
		_results += '				  *** Showing Failures Only ***  \n\n'
		tests = [ _test for _test in tests if _test['TESTSTATUS']=='Failed' ]

	for test in tests:
		_results += '	%s.%s (%s) %sms\n' % (test['COMPONENT'], test['TESTNAME'], test['TESTSTATUS'], test['TIME'] ) 
		
		if( test['DEBUG'] ):
			_debug = test['DEBUG']
			i=0
			for var in _debug:
				print('%s = %s' % ( var, _debug[i] ))
				if 'var' in var:
					var_val = var['var']
				elif 'VAR' in var:
					var_val = var['VAR']
				else:
					var_val = None

				if var_val != None:
					_results += "		Debug: 	%s \n " % var_val

		if( test['TESTSTATUS'] in ('Failed','Error') ):
			_results += '		Message: %s\n' % test['ERROR']['Message']
			_results += '		StackTrace: {\n%s\t\t\n\t\t}\n' % pretty_print_stacktrace(test['ERROR']['StackTrace']) 

		
			
		_results += '\n|--------------------------------------------------------------------------------\n'
	
	_results += '\n__________________________________________________________________________________\n\n'
	_results += 'Test results:  Passed=%s, Failed=%s, Errors=%s\n' % (passed,failed,errors)
	return _results



def pretty_print_stacktrace(data):
	""" Pretty print the stacktrace. """
	results = ''
	print(len(data[0]))
	for e in data:
		results += '\t\t\t%s.%s\t%s - %s \n' % (e['ClassName'],e['MethodName'],e['FileName'],e['LineNumber'])
	# return data
	return results



def parse_line(line):
	""" From a line of text gets the function name. """
	pattern = re.compile("""
		[ \t]*
		(private|package|remote|public)*[ ]*
		(any|string|array|numeric|boolean|component|struct|void)*[ ]*
		(function[ ]+|\<cffunction[ ]+name[ ]*=[ ]*\"?)([_\-a-z][a-z0-9_\-]+)
		""", 
		re.VERBOSE|re.MULTILINE|re.IGNORECASE)
	m = pattern.match(line)
	#return the 5th gouped regex, which should be the function name
	ret_val =  m.group(4) if m else ''
	return ret_val

