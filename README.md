BMO CONTROLLER
==============

About
-----

Interface para controlador universal de sinais de radio e infravermelho.


How does it works
-----------------

* Scans and send InfraRed, RF315 and 433 MHz signals
* Clone and reply these signals


How to start
------------

Install it

    $ git clone git@github.com:perenecabuto/bmo_controller.git
    $ cd bmo_controller
    $ make
    
**PS: make by default runs *mkvirtualenv install syncdb* tasks, if something goes wrong, try to run these tasks step-by-step**

    
Upload code to arduino

    $ make arduino-upload


Run it

    $ make run


And open http://localhost:8000


Dependencies
------------

- ino (http://inotool.org/)
- Django
- pyserial


TODO
------------

* Support listners to trigger actions when specific signals are detected. Actions could be to run another cloned command (as a command proxy) or shell commands