import pytest
from bs4 import BeautifulSoup

from starboard.stars.utilities import ignore_sources


@pytest.mark.parametrize("img_tag,ignore_urls,expected", [
    ("<img src='shields.io'/>", ["shields"], True),
    ("<img src='shields.io'/>", [], False),
    ("<img src='shields.io'/>", ["cats"], False),
    ("<img src='asdf' data-canonical-src='shields.io'/>", ["shields"], True),
    ("<img src='asdf' data-canonical-src='shields.io'/>", ["cats"], False),
    ("<img src='asdf'></img>", [], False),

    ("<img data-canonical-src='shields.io'/>", [], True),  # no src
    ("<img />", [], True),
    ("<img></img>", [], True),
])
def test_ignore_sources(img_tag, ignore_urls, expected):
    soup = BeautifulSoup(img_tag, "html.parser")
    assert ignore_sources(soup.img, ignore_urls=ignore_urls) == expected
