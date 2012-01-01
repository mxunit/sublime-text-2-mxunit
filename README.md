## MXUnit Test Runner Plugin for [Sublime Text 2](http://www.sublimetext.com/)

### Description
A plugin for Sublime Text 2 that runs MXUnit tests.

_As of Jan-1-2012, this is brand new, unstable, and likely has numerous issues._

### How it works
 - Open an MXUnit testcase in Sublime Text 2
 - To run all tests for an MXUnit testcase hit ```alt+r```
 - To run a single test, move your cursor to the test function and hit ```shift+alt+r```
 - To re-run last test  hit ```ctrl+alt+r```

 Alternatively, you can right-click on a testcase and select: MXUnit > [Run tests | Run test on line | Run last test]


### Installation

1. Clone this repository to one of the following directories:

 	- Mac: ~/Library/Application Support/Sublime Text 2/Packages/
 	- Windows: %APPDATA%/Sublime Text 2/Packages/
 	- Linux: ~/.config/sublime-text-2/Packages/

	E.g,: 

	```bash
	$ cd ~/.config/sublime-text-2/Packages/
	$ git clone git://github.com/virtix/sublime-text-2-mxunit.git

	```

2. Edit the ```mxunit.settings``` configuration file located in the plugin's root folder,
   adding your development-specific settings:

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



### Docs and Bugs

 - https://github.com/virtix/sublime-text-2-mxunit/wiki
  
 - https://github.com/virtix/sublime-text-2-mxunit/issues


### To Do
Lots!


###References

 - Sublimetext 2 API - http://www.sublimetext.com/docs/2/api_reference.html
 - How to create a plugin: http://net.tutsplus.com/tutorials/python-tutorials/how-to-create-a-sublime-text-2-plugin/
 - Unoffical (but very good) docs - http://sublimetext.info/docs/en/




------


Special thanks to https://github.com/maltize/sublime-text-2-ruby-tests. Much of what is here is copied from their excellent work.