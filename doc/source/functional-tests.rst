.. _functional-tests:

===================
 Functional tests
===================

The functional tests run against a live Designate, making real requests and
verifying they were successful.

Installation
============

The functional tests are written using ``tempest-lib``. All the dependencies
should be in the requirements files:

::

    cd designate
    pip install -r requirements.txt -r test-requirements.txt
    pip install -e .

Configuration
=============

The Tempest tests require a config file. The config specifies the keystone
endpoint to authenticate against, or to run in noauth mode against a Designate
without keystone.

Set the ``TEMPEST_CONFIG`` environment variable to specify where the config
file is:

::

    export TEMPEST_CONFIG=tempest.conf


The config file should look like the following:

::

    [identity]
    # Replace these with values that represent your identity configuration
    uri = http://localhost:5000/v2.0
    uri_v3 = http://localhost:5000/v3
    auth_version = v2
    region = RegionOne

    username = demo
    tenant_name = demo
    password = password
    domain_name = Default

    alt_username = alt_demo
    alt_tenant_name = alt_demo
    alt_password = password
    alt_domain_name = Default

    admin_username = admin
    admin_tenant_name = admin
    admin_password = password
    admin_domain_name = Default

    [noauth]
    # set this to True to run against designate in noauth mode
    use_noauth = False
    designate_endpoint = http://127.0.0.1:9001
    tenant_id = demo
    alt_tenant_id = alt_demo
    admin_tenant_id = admin

    [designate]
    # the tests will verify changes propagate out to these nameservers
    nameservers = 127.0.0.1:53,127.0.0.2:53


Running the tests
=================

Make sure to set the ``TEMPEST_CONFIG`` environment variable to point to your
test config file.

Then run the tests with tox (you may need to ``pip install tox``):

::

    tox -e functional
