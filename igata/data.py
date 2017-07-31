#-*- coding: utf-8 -*-

offline_begin = """
import ntpath
import os
import posixpath
import sys

wl_home = os.environ["WL_HOME"]
if len(sys.argv)<2:
    domain_path = os.path.dirname(sys.argv[0])
else:
    domain_path = sys.argv[1]

if not domain_name:
    domain_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
domain_dir = os.path.normpath(os.path.join(domain_path, domain_name))
domain_root_dir = os.path.join(domain_dir, 'domain-root')
"""

offline_end = """
exit()
"""

domain = """
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

setOption('OverwriteDomain', 'true')
writeDomain(domain_root_dir)

closeTemplate()
"""

# Create custom configuration
pre_classpath_dir = """
pre_classpath = '{domain[pre-classpath-dir]}'
pre_classpath_path = os.path.join(domain_dir, pre_classpath)

try:
    os.mkdir(pre_classpath_path)
except:
    print "Directory %s does already exists" % pre_classpath_path

domain_env_file = os.path.join(domain_root_dir, 'bin', 'setUserOverrides')

try:
    f = open(domain_env_file + '.cmd', 'w')
    f.write("@echo off\\n")
    f.write("for %%%%a in (\\"%%DOMAIN_HOME%%/../%s/*\\") do (\\n" % pre_classpath)
    f.write("   call :AddToPath %%a\\n")
    f.write(")\\n")
    f.write("echo %EXT_PRE_CLASSPATH%\\n")
    f.write("goto :EOF\\n")
    f.write("\\n")
    f.write(":AddToPath\\n")
    f.write("if NOT \\"%EXT_PRE_CLASSPATH%\\"==\\"\\" (\\n")
    f.write("   set EXT_PRE_CLASSPATH=%EXT_PRE_CLASSPATH%;%1\\n")
    f.write(") else (\\n")
    f.write("   set EXT_PRE_CLASSPATH=%1\\n")
    f.write(")\\n")
    f.write("goto :EOF\\n")
    f.close()
except:
    print "Failed to configuration to %s" % domain_env_file + '.cmd'

try:
    f = open(domain_env_file + '.sh', 'w')
    f.write("for i in $DOMAIN_HOME/../%s/*; do\\n" % pre_classpath)
    f.write("   if [ ! \\"$EXT_PRE_CLASSPATH\\" = \\"\\" ]; then\\n")
    f.write("      EXT_PRE_CLASSPATH=$EXT_PRE_CLASSPATH:$i\\n")
    f.write("   else\\n")
    f.write("      EXT_PRE_CLASSPATH=$i\\n")
    f.write("   fi\\n")
    f.write("done\\n")
    f.write("echo \\"EXT_PRE_CLASSPATH=$EXT_PRE_CLASSPATH\\"")
    f.write("export EXT_PRE_CLASSPATH\\n")
    f.close()
except:
    print "Failed to configuration to %s" % domain_env_file + '.sh'
"""

