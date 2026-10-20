from utilities.is_archive import is_archive

def test_is_archive_returns_false_for_non_archive():

    assert is_archive("sample.txt") is False


def test_is_archive_returns_true_for_zip():

    assert is_archive("sample.zip") is True


def test_is_archive_returns_true_for_tar():

    assert is_archive("sample.tar") is True


def test_is_archive_returns_true_for_tar_gz():

    assert is_archive("sample.tar.gz") is True


def test_is_archive_returns_true_for_tgz():

    assert is_archive("sample.tgz") is True

