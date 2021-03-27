import os
from typing import Any

import pytest
from beet import run_beet
from lectern import Document


@pytest.mark.parametrize("directory", os.listdir("examples"))
def test_build(snapshot: Any, directory: str):
    with run_beet(directory=f"examples/{directory}") as ctx:
        assert snapshot("pack.txt") == ctx.inject(Document)
