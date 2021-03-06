#!/usr/bin/env python
# encoding: utf-8
"""
junit.py

Created by Mahmood Ali on 2009-12-19.
Copyright (c) 2009 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from datetime import datetime
from xml.dom.minidom import Document

CLASSNAME = "com.sun."
def classname(name):
    return CLASSNAME + name.replace(".java", "").replace("/", ".")

class JunitListener(object):
    doc = Document()
    suite = doc.createElement("testsuite")
    doc.appendChild(suite)

    properties = doc.createElement("properties")
    suite.appendChild(properties)

    total = 0
    passed = 0
    ignored = 0
    failed = 0
    errors = 0

    time = 0

    def __init__(self, output):
        self.output = output

    def prepare(self):
        pass

    def testPassed(self, name, time, message):
        self.time += time
        self.passed += 1
        self.total += 1
        case = self.doc.createElement("testcase")
        case.setAttribute("classname", classname(name))
        case.setAttribute("name", name)
        case.setAttribute("time", "1")
        self.suite.appendChild(case)
        pass

    def testFailed(self, name, time, message):
        self.time += time
        self.failed += 1
        self.total += 1
        case = self.doc.createElement("testcase")
        case.setAttribute("classname", classname(name))
        case.setAttribute("name", name)
        case.setAttribute("time", "1")

        failure = self.doc.createElement("failure")
        failure.setAttribute("type", "java.lang.AssertionError")
        text = self.doc.createTextNode(message.encode('ascii', 'replace'))
        failure.appendChild(text)

        case.appendChild(failure)
        self.suite.appendChild(case)

    def testErrored(self, name, time, message):
        self.testErrored(name, time, message)
        pass

    def testIgnored(self, name, time, message):
        pass

    def done(self):
        self.suite.setAttribute("errors", str(self.errors))
        self.suite.setAttribute("failures", str(self.failed))
        self.suite.setAttribute("hostname", "localhost")
        self.suite.setAttribute("name", "all-jtreg")
        self.suite.setAttribute("tests", str(self.total))
        self.suite.setAttribute("timestamp", datetime.now().isoformat())

        if self.output == None:
            print self.doc.toprettyxml(encoding="UTF-8")
        else:
            f = open(self.output, "w")
            self.doc.writexml(writer=f, indent="    ", addindent="    ", newl="\n", encoding="UTF-8")
            f.close()
            pass

def main():
	pass


if __name__ == '__main__':
    import jtreg
    jtreg.main()

