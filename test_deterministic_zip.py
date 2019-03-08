import deterministic_zip as dz


def test_version():
    assert isinstance(dz.__version__, str)
