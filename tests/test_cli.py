from os.path import join, dirname

from aws_ip_ranges.cli import main


DATA_DIR = join(dirname(__file__), 'data')
SOURCE_PATH = join(DATA_DIR, 'ip-ranges.json')
EXPECTED_PATH = join(DATA_DIR, 'ip-ranges.yaml')


def test_stdout(capsys):
    main(['-f', SOURCE_PATH], command='test')
    captured = capsys.readouterr()
    assert not captured.err
    with open(EXPECTED_PATH) as fileobj:
        assert captured.out == fileobj.read()


def test_file(capsys, tmpdir):
    destination = tmpdir.join('ip-ranges.yaml')
    main(['-f', SOURCE_PATH, str(destination)], command='test')
    captured = capsys.readouterr()
    assert not captured.err
    assert not captured.out
    with open(EXPECTED_PATH) as expected, open(str(destination)) as result:
        assert expected.read() == result.read()
