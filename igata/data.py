#-*- coding: utf-8 -*-

config_begin = """
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

config_end = """
exit()
"""

resources_begin = """
connect(admin_user, admin_password, server_url)

edit()
startEdit()
"""

resources_end = """
activate()
disconnect()
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
cd('Security/base_domain/User/%s' % {domain[user]})
cmo.setPassword({domain[password]})

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
    print "Directory %s does already exist" % pre_classpath_path

domain_env_file = os.path.join(domain_root_dir, 'bin', 'setUserOverrides')
domain_pre_classpath = "%%DOMAIN_HOME%%/../%s" % pre_classpath

try:
    f = open(domain_env_file + '.cmd', 'w')
    f.write("@echo off\\n")
    f.write("for %%%%a in (\\"%s/*\\") do (\\n" % domain_pre_classpath)
    f.write("   call :AddToPath \\"%s/%%%%~nxa\\"\\n" % domain_pre_classpath)
    f.write(")\\n")
    f.write("echo %EXT_PRE_CLASSPATH%\\n")
    f.write("goto :EOF\\n")
    f.write("\\n")
    f.write(":AddToPath\\n")
    f.write("if NOT \\"%EXT_PRE_CLASSPATH%\\"==\\"\\" (\\n")
    f.write("   set EXT_PRE_CLASSPATH=%EXT_PRE_CLASSPATH%;%~dpfn1\\n")
    f.write(") else (\\n")
    f.write("   set EXT_PRE_CLASSPATH=%~dpfn1\\n")
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

data_source_function = """
def addProperty(name, key, value):
    cd('/JDBCSystemResources/%(name)s/JDBCResource/%(name)s/JDBCDriverParams/%(name)s/Properties/%(name)s' % {'name' : name})
    cmo.createProperty(key)

    cd('/JDBCSystemResources/%(name)s/JDBCResource/%(name)s/JDBCDriverParams/%(name)s/Properties/%(name)s/Properties/%(key)s' % {'name' : name, 'key' : key})
    cmo.setValue(value)

def addDataSource(name, jndiName, databaseName, host, portNumber, user, password):
    dsURL = 'jdbc:db2://%(host)s:%(portNumber)s/%(databaseName)s' % {'host': host, 'portNumber': portNumber, 'databaseName' : databaseName}
    dsDriver = 'com.ibm.db2.jcc.DB2XADataSource'

    cd('/')
    cmo.createJDBCSystemResource(name)

    cd('/JDBCSystemResources/%(name)s/JDBCResource/%(name)s' % {'name' : name})
    cmo.setName(name)

    cd('/JDBCSystemResources/%(name)s/JDBCResource/%(name)s/JDBCDataSourceParams/%(name)s' % {'name' : name})
    set('JNDINames',jarray.array([String(jndiName)], String))

    cd('/JDBCSystemResources/%(name)s/JDBCResource/%(name)s' % {'name' : name})
    cmo.setDatasourceType('GENERIC')

    cd('/JDBCSystemResources/%(name)s/JDBCResource/%(name)s/JDBCDriverParams/%(name)s' % {'name' : name})
    cmo.setUrl(dsURL)
    cmo.setDriverName(dsDriver)
    cmo.setPassword(password)

    cd('/JDBCSystemResources/%(name)s/JDBCResource/%(name)s/JDBCConnectionPoolParams/%(name)s' % {'name' : name})
    cmo.setTestTableName('SQL SELECT COUNT(*) FROM SYSIBM.SYSDUMMY1\\r\\n')

    addProperty(name, 'user', user)
    addProperty(name, 'portNumber', portNumber)
    addProperty(name, 'databaseName', databaseName)
    addProperty(name, 'serverName', host)
    addProperty(name, 'batchPerformanceWorkaround', 'true')
    addProperty(name, 'driverType', '4')

    cd('/JDBCSystemResources/%(name)s/JDBCResource/%(name)s/JDBCDataSourceParams/%(name)s' % {'name' : name})
    cmo.setGlobalTransactionsProtocol('OnePhaseCommit')

    cd('/JDBCSystemResources/%(name)s' % {'name' : name})
    set('Targets',jarray.array([ObjectName('com.bea:Name=AdminServer,Type=Server')], ObjectName))

    save()
"""

data_source = """
addDataSource('{dataSource[name]}', '{dataSource[jndiName]}', '{dataSource[databaseName]}', '{dataSource[host]}', '{dataSource[portNumber]}', '{dataSource[user]}', '{dataSource[password]}')
"""

wtc_function = """
import socket
wtc_server = 'WTCServer'
local_access_point = socket.gethostname()
def addWTCServer():
    try:
        cd('/WTCServers/%(wtcServer)s' % {'wtcServer' : wtc_server})
        print "WTC-Server %s does already exist" % wtc_server
        return
    except:
        pass
    cd('/')
    cmo.createWTCServer(wtc_server)

def addLocalAccessPoint():
    try:
        cd('/WTCServers/%(wtcServer)s/WTCLocalTuxDoms/%(localAccessPoint)s' % {'wtcServer' : wtc_server, 'localAccessPoint' : local_access_point})
        print "Local access point %s does already exist" % local_access_point
        return
    except:
        pass
    local_network_address = '//localhost:7003'

    cd('/WTCServers/%(wtcServer)s' % {'wtcServer' : wtc_server})
    cmo.createWTCLocalTuxDom(local_access_point)

    cd('/WTCServers/%(wtcServer)s/WTCLocalTuxDoms/%(localAccessPoint)s' % {'wtcServer' : wtc_server, 'localAccessPoint' : local_access_point})
    cmo.setAccessPoint(local_access_point)
    cmo.setAccessPointId(local_access_point)
    cmo.setNWAddr(local_network_address)

def addRemoteAccessPoint(remote_access_point, networkAddress):
    try:
        cd('/WTCServers/%(wtcServer)s/RemoteTuxDoms/%(remoteAccessPoint)s' % {'wtcServer' : wtc_server, 'remoteAccessPoint' : remote_access_point})
        print "Remote access point %s does already exist" % remote_access_point
        return
    except:
        pass
    cd('/WTCServers/%(wtcServer)s' % {'wtcServer' : wtc_server})
    cmo.createWTCRemoteTuxDom(remote_access_point)

    cd('/WTCServers/%(wtcServer)s/RemoteTuxDoms/%(remoteAccessPoint)s' % {'wtcServer' : wtc_server, 'remoteAccessPoint' : remote_access_point})
    cmo.setAccessPoint(remote_access_point)
    cmo.setAccessPointId(remote_access_point)
    cmo.setLocalAccessPoint(local_access_point)
    cmo.setNWAddr(networkAddress)
    cmo.setFederationURL('')
    cmo.setFederationName('')

def addExportedService(service_name, ejb_name):
    cd('/WTCServers/%(wtcServer)s' % {'wtcServer' : wtc_server})
    cmo.createWTCExport(service_name)

    cd('/WTCServers/%(wtcServer)s/WTCExports/%(serviceName)s' % {'wtcServer' : wtc_server, 'serviceName' : service_name})
    cmo.setResourceName(service_name)
    cmo.setLocalAccessPoint(local_access_point)
    cmo.setEJBName(ejb_name)
    cmo.setRemoteName('')

def addImportedService(service_name, remote_access_point):
    cd('/WTCServers/%(wtcServer)s' % {'wtcServer' : wtc_server})
    cmo.createWTCImport(service_name)

    cd('/WTCServers/%(wtcServer)s/Imports/%(serviceName)s' % {'wtcServer' : wtc_server, 'serviceName' : service_name})
    cmo.setResourceName(service_name)
    cmo.setLocalAccessPoint(local_access_point)
    cmo.setRemoteAccessPointList(remote_access_point)
    cmo.setRemoteName('')
"""

wtc_begin = """
addWTCServer()
addLocalAccessPoint()
"""

wtc_exported_service = """
addExportedService('{service[name]}', '{service[ejbName]}')
"""

wtc_remote_access_point = """
remote_access_point = '{remoteAccessPoint[name]}'
addRemoteAccessPoint(remote_access_point, '{remoteAccessPoint[networkAddress]}')
"""

wtc_imported_service = """
addImportedService('{service[name]}', remote_access_point)
"""

