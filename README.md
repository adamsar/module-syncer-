Sweet opencms module syncer
===========================

INSTALLATION
==========================
Like most python projects, you'll want to create a virtual environment inside
the directory with

virtualenv --no-site-packages .

Then install with setup.py

bin/python setup.py install

Then you'll need to configure the application

Configuration
===========================
You'll need to write a Python configuration script for the project you're working on.
There is a blank configuration script in the confs directory called blank.config; you
can use that as a template.

Additionally you will need to edit the roles in the fabfile.py to reflect the URLs in
your system. This is unable to be bootstrapped by a configuration file.

Usage
===========================
Fabric is the primary interace for using this application.  It contains four primary 
commands that you will have access to. The principal command is as follows

bin/fab -r {role(dev|stage|prod)} command:{config_file},{config_section}

The commands and examples are

sync -- sync files to a server
bin/fab -r dev sync:confs/myconfig.config,local

publish -- Remotely publishes files on your server
bin/fab -r stage sync:conf/myconfig.config,stage

restart_server -- Remotely restarts your tomcat server
bin/fab -r stage sync:conf/mymenu.config,stage

deploy -- syncs the files, then publishes, then restarts the server
bin/fab -r stage sync:conf/mymenu.config,stage
