.. highlight:: rst

========================================================
Igata: A Tool and DSL for creating JEE server domains
========================================================

---------------------
Current limitations
---------------------
For now only Oracle Weblogic is supported with IBM DB2 as the only supported DataSource provider. Support for payara and other Databases will follow shortly

-----------------
Installing igata
-----------------

* Install igata using pip::

     pip install igata

* To create a basic weblogic domain add the following to a file, weblogic_test.igata::

    from igata.template import *

    with Configuration():
        Domain(name="weblogic-test", credentials=Credentials('weblogic','weblogic1'))

    with Resources():

        with WTCExport():
            Service(name="testTuxedoService",ejbName="this.is.the.jdni.name.of.the.exporting.ejb")

        with WTCImport(name="tuxedoAccessPointName", networkAddress="//tuxedohostname:1234"):
            Service(name="tuxedoServiceName")

        with Messaging():
            Queue("queueName")
            ConnectionFactory("connectionFactoryName")

* Generate the domain creation scripts using::

    igata generate weblogic_test.igata

* Create the domain with the following steps::

    igata run weblogic_test.py
    start the weblogic domain
    igata run weblogic_test_resources.py

* You should now have a weblogic domain with the declared resources
