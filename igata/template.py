from collections import namedtuple

import data
from mode import *

Credentials = namedtuple('Credentials', ['user', 'password'])

def OfflineScript(name = None):
    """
    Creates a new script file for editing a domain in offline mode.

    Shall be used in a 'with statement'.

    with OfflineScript('scriptname'):
       PreClasspathDir()
    """
    return scope(name, 'offline')

def Domain(name, credentials):
    """
    Domain

    Create a new domain.

    Only to use in offline editing mode.
    """
    if state().editing_mode and state().editing_mode != 'offline':
        raise SyntaxError('Domain can only be used in offline editing mode')

    add_pre_script_definition("domain_name = '%s'" % name)
    print data.domain.format(domain={'user' : credentials.user, 'password' : credentials.password})

def PreClasspathDir(dirname = None):
    """
    PreClasspathDir

    Create configuration for a pre-classpath dir.
    """
    if not dirname:
        dirname = 'pre-classpath'
    print data.pre_classpath_dir.format(domain={'pre-classpath-dir': dirname})

