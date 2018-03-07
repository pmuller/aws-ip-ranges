from argparse import ArgumentParser
import json
import sys

from aws_ip_ranges import output, data


IP_RANGES_URL = 'https://ip-ranges.amazonaws.com/ip-ranges.json'


def parse_arguments(argv):
    """Parse CLI arguments.
    """
    parser = ArgumentParser()

    parser.add_argument(
        '-k', '--yaml-key', default='aws::prefixes',
        help='Top-level key in generated YAML document. Default: %(default)s')
    source_group = parser.add_mutually_exclusive_group()
    source_group.add_argument(
        '-f', '--ip-ranges-file', metavar='PATH',
        help='Load data from a file.')
    source_group.add_argument(
        '-u', '--ip-ranges-url', metavar='URL',
        help='Load data from a custom URL. Default: %s' % IP_RANGES_URL)

    parser.add_argument(
        'output_file', nargs='?',
        help='When defined, YAML is written to this path. '
             'By default, it is written on stdout.')

    return parser.parse_args(argv)


def main(argv=None, command=None):
    """CLI main entry point.
    """
    arguments = parse_arguments(argv)

    if arguments.ip_ranges_file:
        str_data = data.load(arguments.ip_ranges_file)
    else:
        str_data = data.download(arguments.ip_ranges_url or IP_RANGES_URL)

    json_data = json.loads(str_data)
    prefixes = data.transform(json_data)
    yaml_str = output.generate(
        prefixes, json_data['createDate'], arguments.yaml_key, command)

    if arguments.output_file:
        with open(arguments.output_file, 'w') as fileobj:
            fileobj.write(yaml_str)
    else:
        sys.stdout.write(yaml_str)
