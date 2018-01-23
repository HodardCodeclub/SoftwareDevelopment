

import pytest

from fossir.util.fs import secure_filename


@pytest.mark.parametrize(('filename', 'expected'), (
    ('', 'fallback'),
    (None, 'fallback'),
    ('foo.txt', 'foo.txt'),
    ('', 'fallback'),
    ('../../../etc/passwd', 'etc_passwd'),
    (u'm\xf6p.txt', 'moep.txt'),
    (u'm\xf6p.txt'.encode('utf-8'), 'moep.txt'),
    (u'/m\xf6p.txt', 'moep.txt'),
    (r'spacy   \filename', 'spacy_filename'),
))
def test_secure_filename(filename, expected):
    assert secure_filename(filename, 'fallback') == expected
