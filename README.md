This script and accompanying ini file will allow you to run actions against groups defined in Red Hat Insights. Currently this script will only generate lists from hosts that are defined within a group.

Future enhancements:
* Add all hosts without an existing group to a more generic Ansible grouping such as 'insights-other' or 'insights-all'
* Potentially add some metadata from Red Hat Insights registration to a `--host` request, which currently only returns an empty dict.
* Better flexibility around username/password storage

To get started with this script, first replace 'RH_ACCT' and 'RH_PASSWD' in the ini file with the appropriate credentials.

This script can be run independently from Ansible for testing purposes:

`./insights_inventory.py --list`

Or can be used within Ansible:

`ansible all -i ./insights_inventory.py`
