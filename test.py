#!/usr/bin/python
import subprocess
import os
import base64
import sys
import json
import random, string

successTestCases = [
    '''{"a":"b\\""}''',
    '''{"a":"b"}''',
    '''{"a":["b",1]}''',
    #'''{"asdf":"qwer","zxcv":[1,2,3,4],"fdsa":{"a":"b"}}''',
    #'''{"a":1.234,"b":"c"}''',
    #'''{"a":true,"b":false,"c":null}''',
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

keys = []
values = []

for jString in successTestCases:
    jObject = json.loads(jString)
    keys.append(jObject.keys())
    values.append(jObject.values())

# print(keys)
# print(values)
for i in range(0, 10000):
    for key in keys:
        for val in values:
            randJson = {key[0].join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)]): val}
            j = json.dumps(randJson)
            child = subprocess.Popen("./jsonParser", stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            _, stdErrOut = child.communicate(input = j)
            if child.returncode != 0 or stdErrOut != "" :
                print "BROKEN SUCCESS TEST CASE (%d): %s" % (child.returncode, j)
                print "|%s|" % stdErrOut
                sys.exit(0)

#l = [chr(i) for i in xrange(127)]

# for testcase in successTestCases :
# for i in range(0, 10000):
#     randJson = {''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(8)]) : float(decimal.Decimal(random.randrange(155, 389))/100)}
#     j = json.dumps(randJson)
#     child = subprocess.Popen("./jsonParser", stdin=subprocess.PIPE, stderr=subprocess.PIPE)
#     _, stdErrOut = child.communicate(input = j)
#     if child.returncode != 0 or stdErrOut != "" :
#         print "BROKEN SUCCESS TEST CASE (%d): %s" % (child.returncode, j)
#         print "|%s|" % stdErrOut
#         sys.exit(0)
