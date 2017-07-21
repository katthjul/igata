from collections import namedtuple

import data

Domain = namedtuple('Domain', ['name'])
Credentials = namedtuple('Credentials', ['user', 'password'])

def CreateDomain(domain, credentials):
    """
    CreateDomain

    Create a new domain
    """
    print data.domain.format(domain={'name' : domain.name, 'user' : credentials.user, 'password' : credentials.password})

