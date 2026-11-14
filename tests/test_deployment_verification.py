import importlib.util
import json
from pathlib import Path
from unittest.mock import patch

import pytest

spec = importlib.util.spec_from_file_location(
    "verify_public_release",
    Path(__file__).resolve().parents[1] / "scripts/verify_public_release.py",
)
release = importlib.util.module_from_spec(spec)
spec.loader.exec_module(release)


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
    with (
        patch.object(release, "fetch", return_value=b'{"commit":"old"}') as fetch,
        patch.object(release.time, "sleep"),
        pytest.raises(RuntimeError, match="another commit"),
    ):
        release.main()
    assert fetch.call_count == 6


def test_missing_assets_cannot_pass(monkeypatch):
    monkeypatch.setenv("SITE_URL", "https://example.test")
    monkeypatch.setenv("GITHUB_SHA", "expected")
    with (
        patch.object(
            release, "fetch", side_effect=[b'{"commit":"expected"}', b"<html>error</html>"] * 6
        ),
        patch.object(release.time, "sleep"),
        pytest.raises(RuntimeError, match="No application assets"),
    ):
        release.main()
