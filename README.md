pySQRL
====

**Python SQRL (Secure QR Login) Client**


What is SQRL?

A newly proposed authentication scheme from Steve Gibson of GRC.com. It allows
for user authentication without the need of:

* Username / Password pair
* OTP (One Time Password)
* Third party Interactions
* Revealing your identity during login
* An in-band authentication exchange

In a normal web authentication system your credentials are stored with the site
you are trying to access. If the site were to be compromised yours and
every other users' account information may be accessible; allowing the intruder
to attempt to use your credentials elsewhere. The best part about SQRL is
that the site never has your login credentials. With SQRL you **_never_** send your
**_"password"_**. The site authenticates you by verifying your identity by 
using a private / public key signature. This ends up being vastly more secure.

Details can be found here: https://www.grc.com/sqrl/sqrl.htm

The SQRL protocol is new and is subject to change. I'll try my best to follow the published implementation found here:
https://www.grc.com/sqrl/details.htm

Install
-------
This package requires **ed25519**, **docopt** and **pyinotify**

     git clone http://github.com/bushxnyc/sqrl.git
     cd sqrl
     sudo python setup.py install

Usage
-----
     Usage: sqrl [-d] [-n] [--path=<Dir>] <SQRLURL>

     Options:
          -d               Debugging output
          -n               Notify via libnotify (Gnome)
          -p --path=<Dir>  Path for config and key storage

     Example:
         sqrl "sqrl://example.com/login/sqrl?d=6&nut=a95fa8e88dc499758"

You feed the sqrl URL provided by the authentication service to the script and
it uses it to submit an authentication request on your behalf. Depending on how
the site is designed, you may automatically get logged in. **It's that simple**.

Features
--------

* **Debug** - Displays the content of the payload to you for verification
* **Notification** - Displays notifications on successful or failed auth attempts
  (Gnome Only)

Debug
-----

When the [-d] argument is given the script outputs all the components of the
request.

    Url: localhost:8080/sqrl?nut=1bfe7ef6f9989bd5709d61f7ac28195e&sqrlver=1&sqrlkey=Zl_nrges0MGPRelRoH9SEwwPcARQSA0QmYNx-ZDcOKU
    Domain: "localhost"
    SQRLver: 1
    SQRLkey: Zl_nrges0MGPRelRoH9SEwwPcARQSA0QmYNx-ZDcOKU
    SQRLsig: LtYQU_j5Lwp6c0TrWEGhP0tj5o_PM8yni_tLmrG375aEIkUNdJzWl_XmLUN-dtZHuKWP1pf8iNUVSSyYRq3QDA
    signature is good

