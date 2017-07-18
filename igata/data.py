#-*- coding: utf-8 -*-

domain = """
import os
import sys

if len(sys.argv)<2:
    domain_path = os.path.dirname(sys.argv[0])
else:
    domain_path = sys.argv[1]

domain_name = '{domain[name]}'
if not domain_name:
    domain_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
wl_home = os.environ["WL_HOME"]

readTemplate(os.path.join(wl_home, 'common', 'templates', 'wls', 'wls.jar'))

# Configure the admin server
cd('Servers/AdminServer')
set('ListenAddress','')
set('ListenPort', 7001)

create('AdminServer','SSL')
cd('SSL/AdminServer')
set('Enabled', 'True')
set('ListenPort', 7002)

# Set the domain password for the WebLogic Server administration user
cd('/')
cd('Security/base_domain/User/{domain[user]}')
cmo.setPassword('{domain[password]}')

# If the domain already exists, overwrite the domain
setOption('OverwriteDomain', 'true')

# write the domain and close the template
writeDomain(os.path.normpath(os.path.join(domain_path, domain_name)))

closeTemplate()
exit()
"""

