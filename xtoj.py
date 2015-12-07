#!/usr/bin/env python

import json
import xml.etree.ElementTree as xml

import re

import sys

__author__ = "Miso Mijatovic"


class xtoj:
    """class FeyeXJ
    This class will parse a generic XML file and convert it to JSON format

    funcs:
        constructor(input file, [output file])
        importXML(): parse xml file
        convert_recursive(root): convert xml to json
        to_file(root): convert xml to json and dumps to file

    To use as a module call with -h parameter
    """

    def __init__(self, input_file, output_file=None):
        """
        Class constructor
        :param input_file: read xml from here
        :param output_file: print json here
        """
        self.input_file = input_file
        self.tree = self.importXML()
        self.root = self.tree.getroot()
        self.output_file = output_file

    def importXML(self):
        """
        __importXML()
        :return: xml file parsed object
        """
        # Parse XML directly from the file path
        try:
            return xml.parse(self.input_file)
        except Exception as e:
            print e.message
            print e.args
            sys.exit(1)

    def convert_recursive(self, this_root):
        """
        convert_recursive(this_root)
        :param this_root: root of an xml obj
        :return: dict that contains all the items of an xml
        """
        out_dict = {}
        if len(this_root) > 0:
            out_dict = this_root.attrib
            for item in this_root:
                try:
                    name = re.search('}(.*)\'', str(item)).group(1)
                except:
                    name = str(item)
                out_dict[name] = self.convert_recursive(item)
            return out_dict
        else:
            out_dict = this_root.attrib
            if this_root.text is None:
                return 'Null'
            else:
                return this_root.text

    def to_file(self, this_root):
        """
        toFile(this_root)
        :param this_root: root of the xml obj
        :return: converts xml to json and dumps it to a file
        """
        try:
            converted = self.convert_recursive(this_root)
            converted = json.loads(converted)
            f = open(self.output_file)
            json.dump(converted, f)
            f.close()
            return 0
        except Exception as e:
            print e.message
            print e.args
            return 1

if __name__ == '__main__':
    Usage = ' ----- XML to JSON -----\nauthor: ' + __author__ + '\n\nparams:\n\t-h print this help\n\t-d print docstring\n\nusage:\n\txtoj <xml_filename>\t-\tdumps json conversion\n\txtoj <xml_filename> <json_filename>\t-\tdumps json conversion to file\n'
    args = len(sys.argv)
    if args != 2 and args != 3:
        print '-h to show help'
    else:
        if args == 2:
            if sys.argv[1] == '-h':
                print Usage
            elif sys.argv[1] == '-d':
                print xtoj.__doc__
            else:
                # is this a file?
                xj = xtoj(sys.argv[1])
                print json.dumps(xj.convert_recursive(xj.root))
        else:
            if sys.argv[1] != '-h' and sys.argv[1] != '-d':
                # two files
                xj = xtoj(sys.argv[1], sys.argv[2])
                xj.to_file(xj.root)
            else:
                print 'bad arguments'
