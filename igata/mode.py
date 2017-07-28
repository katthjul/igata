from contextlib import contextmanager
import re

import data
from engine import *

def normalize(text):
    return re.sub( '[^\w]+', '_', text)

class State:
    def __init__(self, mode = None):
        self.editing_mode = mode

global_current_state = State()

def state():
    return global_current_state

@contextmanager
def scope(name, mode=None):
    global global_current_state

    if name:
        name = normalize(name)

    old_state = global_current_state
    global_current_state = State(mode)

    current_resultfile_state = None

    try:
        current_resultfile_state = engine().scopeBegin(name)
        pre_script_code()
        yield
    finally:
        post_script_code()

        engine().scopeEnd()
        global_current_state = old_state

def pre_script_code():
    if state().editing_mode == 'offline':
        print data.offline_begin

def post_script_code():
    if state().editing_mode == 'offline':
        print data.offline_end

