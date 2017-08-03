from collections import Counter
from contextlib import contextmanager
import re

import data
from engine import *

def normalize(text):
    return re.sub( '[^\w]+', '_', text)

global_pre_script_definitions = {}

class State:
    def __init__(self, block = None, old_state = None):
        self.block = block

        if old_state:
            self.pre_script_definitions = old_state.pre_script_definitions
        else:
            self.pre_script_definitions = {}

global_current_state = State()

def state():
    return global_current_state

@contextmanager
def scope(name, block = None):
    global global_current_state

    if name:
        name = normalize(name)

    old_state = global_current_state
    global_current_state = State(block, old_state)

    current_resultfile_state = None

    try:
        current_resultfile_state = engine().scopeBegin(name)
        pre_script_code()
        yield
    finally:
        post_script_code()
        engine().scopeEnd()

        global global_pre_script_definitions
        global_pre_script_definitions.update(global_current_state.pre_script_definitions)

        global_current_state = old_state

def pre_script_code():
    if state().block == 'config':
        print data.config_begin
    else:
        print data.data_source_function
        print data.resources_begin

def post_script_code():
    if state().block == 'config':
        print data.config_end
    else:
        print data.resources_end

def add_pre_script_definition(variable, value):
    state().pre_script_definitions[variable] = value

