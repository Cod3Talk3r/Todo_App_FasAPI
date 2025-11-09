def test_equal_or_not_equal():
    assert 3 == 3
    assert 3 != 1


def test_is_instance():
    assert isinstance("this is a string", str)
    assert not isinstance("1", int)


def test_boolean():
    v = True

    assert v is True
    assert ("he" == "sa") is False