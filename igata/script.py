from contextlib import contextmanager
import re

import data
from engine import *

def normalize(text):
    return re.sub( '[^\w]+', '_', text)

global_pre_script_definitions = []

class State:
    def __init__(self, block = None):
        self.block = block

        self.pre_script_definitions = list()

global_current_state = State()

def state():
    return global_current_state

@contextmanager
def scope(name, block=None):
    global global_current_state

    if name:
        name = normalize(name)

    old_state = global_current_state
    global_current_state = State(block)

    current_resultfile_state = None

    try:
        current_resultfile_state = engine().scopeBegin(name)
        pre_script_code()
        yield
    finally:
        post_script_code()
        engine().scopeEnd()

        global global_pre_script_definitions
        global_pre_script_definitions.extend(global_current_state.pre_script_definitions)

        global_current_state = old_state

def pre_script_code():
    if state().block == 'config':
        print data.config_begin

def post_script_code():
    if state().block == 'config':
        print data.config_end

def add_pre_script_definition(pre_script_definition):
    state().pre_script_definitions.append(pre_script_definition)

