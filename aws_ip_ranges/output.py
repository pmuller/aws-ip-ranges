from collections import defaultdict
from os.path import basename
import sys

from netaddr import IPSet
import yaml


TEMPLATE = """\
# Generated with "{command}"
# AWS creation date: {creation_date}
"""


class Dumper(yaml.Dumper):  # pylint: disable=too-many-ancestors
    """Dump data containing a ``netaddr.IPSet``.
    """

    def __init__(self, *args, **kwargs):
        """Register the custom representers.
        """
        super(Dumper, self).__init__(*args, **kwargs)
        self.yaml_representers[IPSet] = Dumper.represent_ipset
        self.yaml_representers[defaultdict] = Dumper.represent_defaultdict

    def process_tag(self):
        """Do nothing, because we don't want tags in the serialized document.
        """

    def represent_ipset(self, ipset):
        """Represent a ``netaddr.IPSet`` as a regular list.
        """
        return self.represent_sequence(
            'ipset', [str(network) for network in sorted(ipset._cidrs.keys())])

    def represent_defaultdict(self, dict_):
        """Represent a ``defaultdict`` as a regular dict.
        """
        return self.represent_mapping('defaultdict', dict_)


def generate(prefixes, creation_date, top_level_key, command=None):
    """Generate the YAML document.
    """
    yaml_str = TEMPLATE.format(
        command=command or ' '.join([basename(sys.argv[0])] + sys.argv[1:]),
        creation_date=creation_date)
    yaml_str += yaml.dump(
        {top_level_key: prefixes},
        indent=2, width=80, default_flow_style=False, Dumper=Dumper)

    return yaml_str
