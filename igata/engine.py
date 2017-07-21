#-*- coding: utf-8 -*-
import os
import StringIO
import sys

class Engine(object):
    def __init__(self):
        self.output = StringIO.StringIO()
        sys.stdout = self.output

    def prepareTemplateFile(self, template_file):
        with open(template_file, 'r') as source:
            template = StringIO.StringIO()

            for line in source:
                template.write(line)
        return template

    def find_path_to_result_file(self, template_file):
        resultfile = os.path.abspath(template_file)
        resultdir = os.path.dirname(resultfile)
        resultname = os.path.splitext(os.path.basename(resultfile))[0]
        return os.path.join(resultdir, resultname + '.py')

    def write(self, stream, filename):
        stream.seek(0)
        with open(filename, 'w') as resultfile:
            for line in stream:
                resultfile.write(line)

    def run(self, template_file):
        try:
            template = self.prepareTemplateFile(template_file)
            code = compile(template.getvalue(), template_file, 'exec')
            template.close()
            exec(code, {})
        except (NameError, SyntaxError, TypeError) as e:
            sys.stderr.write( "Error in %s: %s.\n" % (os.path.realpath( template_file), str(e)))
            raise

        sys.stdout = sys.__stdout__

        result_file = self.find_path_to_result_file(template_file)
        self.write(self.output, result_file)

def main(args):
    if not os.path.isfile(args.template):
        sys.stderr.write("error: Could not find the template file " + args.template + '\n')
        sys.exit(1)
    engine().run(args.template)

__global_engine = None

def engine():
    global __global_engine
    if not __global_engine:
        __global_engine = Engine()

    return __global_engine

