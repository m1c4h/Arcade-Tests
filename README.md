Synopsis

Utilize a single testing framework for the entire organization - Robot framework. Can be used for all types of testing Is simple to pickup for non-technical resources. Easier to support a single tool. Tests will be created more consistently. Results and reporting can be made consistent.

http://robotframework.org/

libraries robotframework==3.0 robotframework-debuglibrary==0.3 robotframework-requests==0.3.8 robotframework-selenium2library==1.7.4 robotframework-extendedselenium2library==0.9.0 selenium==2.52.0 simplejson==3.8.0 requests[security]==2.7.0 fake-factory==0.5.2 robotframework-faker==3.0.0 robotframework-pabot==0.22

Code Example

Installing the Robot Framework allows developers/testers to Run tests as quickly as possible and for all to consume.

Motivation

We would like to make test automation consistent between all pillars Robot allows us to do this very easily.

Installation

$ curl -O https://bootstrap.pypa.io/get-pip.py
$ sudo python get-pip.py


Then install Virtual Env
$ sudo pip install virtualenv
$ mkdir "Create your Your own directory name"
$ cd "Into Your own directory name"
$ virtualenv Robot
Kick off your virtual env.

source /path/to/virtualenv/activate
Install all fo the libraries needed for the Robots to run.

pip install -r requirements.txt
Commands to pass via the terminal.

-- To run the tests with locally  python robotrun.py -e dev  -r all

Contributors



License

Robot Framework itself is open source software released under Apache License 2.0, and most of the libraries and tools in the ecosystem are also open source.
Status API Training Shop Blog About
© 2016 GitHub, Inc. Terms Privacy Security Contact Help
