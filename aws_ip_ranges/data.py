import codecs
from collections import defaultdict

import requests
from netaddr import IPSet


KEYS = {
    4: {'prefixes': 'prefixes', 'prefix': 'ip_prefix'},
    6: {'prefixes': 'ipv6_prefixes', 'prefix': 'ipv6_prefix'},
}


def download(url):
    """Retrieve the AWS IP ranges data from the Internet.
    """
    return requests.get(url).text


def load(filepath, encoding='UTF-8'):
    """Read the AWS IP ranges data from a local file.
    """
    with codecs.open(filepath, encoding=encoding) as fileobj:
        return fileobj.read()


def transform(data):
    """Convert raw AWS IP ranges data to internal representation.
    """
    # Build a dict using 3 levels: region, service, ip_version
    prefixes = defaultdict(
        lambda: defaultdict(lambda: {4: IPSet(), 6: IPSet()}))

    for ip_version, ip_version_keys in KEYS.items():
        for prefix_data in data[ip_version_keys['prefixes']]:
            region = str(prefix_data['region'])
            service = str(prefix_data['service'])
            prefix = prefix_data[ip_version_keys['prefix']]
            prefixes[region][service][ip_version].add(prefix)

    # Remove service-specific prefixes from the "AMAZON" service
    for region, region_data in prefixes.items():
        for service, service_data in region_data.items():
            for ip_version, service_prefixes in service_data.items():
                if service != 'AMAZON':
                    amazon_prefixes = prefixes[region]['AMAZON'][ip_version]
                    prefixes[region]['AMAZON'][ip_version] = \
                        amazon_prefixes - service_prefixes

    return prefixes
