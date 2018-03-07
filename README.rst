aws-ip-ranges
=============

This script retrieves AWS IP ranges data and produces a YAML file formatted
for use by the `aws_firewall <https://github.com/pmuller/puppet-aws_firewall>`_
Puppet module.


Installation
------------

.. code-block:: console

  $ pip install aws-ip-ranges


Usage
-----

.. code-block:: console

    $ aws-ip-ranges -h
    usage: aws-ip-ranges [-h] [-k YAML_KEY] [-f PATH | -u URL] [output_file]

    positional arguments:
      output_file           When defined, YAML is written to this path. By
                            default, it is written on stdout.

    optional arguments:
      -h, --help            show this help message and exit
      -k YAML_KEY, --yaml-key YAML_KEY
                            Top-level key in generated YAML document. Default:
                            aws::prefixes
      -f PATH, --ip-ranges-file PATH
                            Load data from a file.
      -u URL, --ip-ranges-url URL
                            Load data from a custom URL. Default: https://ip-
                            ranges.amazonaws.com/ip-ranges.json


Development
-----------

To launch tests of the project, use the following command:

.. code-block:: bash

  $ make check
