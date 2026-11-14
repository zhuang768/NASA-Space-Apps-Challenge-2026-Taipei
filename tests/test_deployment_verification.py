import json
from unittest.mock import patch

import pytest

from scripts import verify_public_release as release


def test_release_checks_stamp_and_both_assets(monkeypatch):
    monkeypatch.setenv("SITE_URL", "https://example.test")
    monkeypatch.setenv("GITHUB_SHA", "expected")
    responses = [
        json.dumps({"commit": "expected"}).encode(),
        b'<script src="/assets/app.js"></script><link href="/assets/app.css">',
        b"javascript",
        b"css",
    ]
    with patch.object(release, "fetch", side_effect=responses) as fetch:
        release.main()
    assert fetch.call_count == 4
    assert fetch.call_args_list[-1].args[0] == "https://example.test/assets/app.css"


def test_old_release_cannot_pass(monkeypatch):
    monkeypatch.setenv("SITE_URL", "https://example.test")
    monkeypatch.setenv("GITHUB_SHA", "expected")
    with patch.object(release, "fetch", return_value=b'{"commit":"old"}') as fetch:
        with patch.object(release.time, "sleep"):
            with pytest.raises(RuntimeError, match="another commit"):
                release.main()
    assert fetch.call_count == 6


def test_missing_assets_cannot_pass(monkeypatch):
    monkeypatch.setenv("SITE_URL", "https://example.test")
    monkeypatch.setenv("GITHUB_SHA", "expected")
    with patch.object(
        release, "fetch", side_effect=[b'{"commit":"expected"}', b"<html>error</html>"] * 6
    ):
        with patch.object(release.time, "sleep"):
            with pytest.raises(RuntimeError, match="No application assets"):
                release.main()
