# MXUnit Test Runner Plugin for [Sublime Text 2](http://www.sublimetext.com/)

## Description
A plugin for Sublime Text 2 that runs MXUnit tests - http://mxunit.org.


### News
 - May-12-2012:  Added completions for assertions and other MXUnit functions.
 - Jan-05-2012:  Still unstable, but improving nicely. 
 - Jan-01-2012:  Brand new, unstable, and likely has numerous issues



## How it works

Open an MXUnit testcase in Sublime Text 2 and then:

__(Using Sublime's Command Pallette)__

 - Type ```shift+ctrl+p``` (Command pallette)
 - Type ```mx``` to see list of available commands
 - Select [ ```Run tests``` | ```Run test on line``` | ```Run last test``` | ```Run tests - show failures only```]
 - (More to come!)


![MXUnit Sublime Screenshot](https://github.com/virtix/sublime-text-2-mxunit/raw/master/MXUnit-Sublime-Text-Command_Window.png)


__Or (Using keyboard shortcuts)__

 - To run all tests for an MXUnit testcase type ```alt+r```
 - To run all tests and display only failures type ```ctrl+alt+shift+r```
 - To run a single test, move your cursor to the test function and type ```shift+alt+r```
 - To re-run last test type ```ctrl+alt+r```



__Or (Using mouse clicks)__

  - Right-click on a testcase and select: 
  - MXUnit > [Run tests | Run test on line | Run last test | Run all tests - show failures only]


## Installation

1. Clone this repository to one of the following directories:

 	- Mac: ~/Library/Application Support/Sublime Text 2/Packages/
 	- Windows: %APPDATA%/Sublime Text 2/Packages/
 	- Linux: ~/.config/sublime-text-2/Packages/

	E.g,: 

	```bash
	$ cd ~/.config/sublime-text-2/Packages/
	$ git clone git://github.com/virtix/sublime-text-2-mxunit.git

	```
2. Rename the cloned directory to ```MXUnit```

3. Create an ```mxunit.settings``` configuration file located in the plugin's root folder,
   adding your development-specific settings. Note, you can copy ```mxunit.settings.example``` to 
   ```mxunit.settings```.  You can also get to this location in Sublime by selecting
   Preferences > Browse Packages. Find the MXUnit directory.

	```bash
	{
	
		"server" : "localhost",
		"port" : "8301" ,
		"component_root" : "/" ,
		"web_root" :  "/home/billy/software/jrun4/servers/dev/cfusion.ear/cfusion.war/" ,
	
	}
	``` 
	The ```component_root``` is how the web server sees your application. Above assumed all apps are visible from
	http://localhost:8301/  and all files are stored in the  ```web_root``` directory.


## Installation via [Package Control](http://wbond.net/sublime_packages/package_control)

1. Type ```ctrl+shift+p``` (see below)
2. Select 'Package Control: Install Package' 
3. Select 'MXUnit'
4. Follow step #3 above for editing the ```mxunit.settings``` file.

![Package Control Screenshot](https://github.com/virtix/sublime-text-2-mxunit/raw/master/pacakge-control-ss.png)


## Docs and Bugs (to do)

 - Docs: https://github.com/virtix/sublime-text-2-mxunit/wiki
  
 - Bugs: https://github.com/virtix/sublime-text-2-mxunit/issues


## To Do
Lots - and the project could use some help!  Fork this repository, hack away, and make a pull request.  

These are some ideas/issues:

 - Display a list of test methods in the quick panel and when the method is selected, run the test
 - Maintain a history of test runs and display that history in a quick panel
 - Pretty print debug output and wrap it in folding regions
 - Run all tests in a directory
 - Implement concurrency for test runs.  This should support long-running test suites
 - Ant? Or some Python build script?
 - Key bindings to switch back and forth between test and code
 - Plugin tests!  Sadly, testing is not baked into Sublime plugin development. Something is needed to make this happen.


##References

 - Sublimetext 2 API - http://www.sublimetext.com/docs/2/api_reference.html
 - How to create a plugin: http://net.tutsplus.com/tutorials/python-tutorials/how-to-create-a-sublime-text-2-plugin/
 - Unoffical (but very good) docs - http://sublimetext.info/docs/en/
 - ColdFusion Sublime Text bundle - https://github.com/SublimeText/ColdFusion
 	


