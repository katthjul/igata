from collections import namedtuple

import data
from script import *

Credentials = namedtuple('Credentials', ['user', 'password'])

def Configuration(name = None):
    """
    Configuration

    A block with configuration for a domain.

    Shall be used in a 'with statement'.

    with OfflineScript('scriptname'):
       PreClasspathDir()
    """
    return scope(name, 'config')

def Domain(name, credentials):
    """
    Domain

    Create a new domain.

    Only to use in a configuration block
    """
    if state().block and state().block != 'config':
        raise SyntaxError('Domain can only be used in a configuration block')

    add_pre_script_definition("domain_name = '%s'" % name)
    add_pre_script_definition("admin_user = '%s'" % credentials.user )
    add_pre_script_definition("admin_password = '%s'" % credentials.password )
    print data.domain.format(domain={'user' : 'admin_user', 'password' : 'admin_password'})

def PreClasspathDir(dirname = None):
    """
    PreClasspathDir

    Create configuration for a pre-classpath dir.
    """
    if not dirname:
        dirname = 'pre-classpath'
    print data.pre_classpath_dir.format(domain={'pre-classpath-dir': dirname})

