#!/usr/bin/python
import subprocess
import os
import base64
import sys

successTestCases = [
    '''{"a":"b\\""}''',
    '''{"a":"b"}''',
    '''{"a":["b",1]}''',
    '''{"asdf":"qwer","zxcv":[1,2,3,4],"fdsa":{"a":"b"}}''',
    '''{"a":1.234,"b":"c"}''',
    '''{"a":true,"b":false,"c":null}''',
    '''{"a":-1}''',
    '''{"a":"?"}''',
    '''{"a":"this is mult"}''',
    '''{"a mult":"t"}''',
    '''{ "a":"t"}''',
    '''{"a" :"t"}''',
    '''{"a": "t"}''',
    '''{"a":"t" }''',
    '''{"a":1E-4}''',
]

for testcase in successTestCases :
    child = subprocess.Popen("./jsonParser", stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stdErrOut = child.communicate(input = testcase)
    if child.returncode != 0 or stdErrOut != "" :
        print "BROKEN SUCCESS TEST CASE (%d): %s" % (child.returncode, testcase)
        print "|%s|" % stdErrOut
        sys.exit(0)

failureTestCases = [
    '''{a}''',
    '''"asdf"''',
    '''{1:"a"}''',
    '''{"a:1}''',
    '''{"a":truetrue}''',
    '''{"a":1234.123.123}''',
    '''{"a":1E-4E-5}''',
]

for testcase in failureTestCases:
    child = subprocess.Popen("./jsonParser", stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stdErrOut = child.communicate(input = testcase)
    print "Correctly found error in failure case : %s" % stdErrOut
    if child.returncode != 0 or stdErrOut == "" :
        print "BROKEN FAILURE TEST CASE (%d): %s" % (child.returncode, testcase)
        print "|%s|" % stdErrOut
        sys.exit(0)

print "EVERYTHING PASSES"
