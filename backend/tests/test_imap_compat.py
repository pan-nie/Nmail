"""IMAP 兼容性回归测试：Coremail（网易企业邮）两个坑。

1. UID SEARCH 不得带显式 CHARSET——Coremail 报 BAD Could not parse command；
2. imaplib 必须注册 RFC 2971 的 ID 命令——否则 _simple_command("ID") KeyError，
   网易系要求的 ID 静默发不出去（imap_client 模块加载期注册）。
"""
from __future__ import annotations

import imaplib


def test_search_uids_不带charset():
    from app.core import imap_client

    sent = {}

    class FakeMB:
        def uids(self, criteria, charset="US-ASCII"):
            sent["criteria"] = criteria
            sent["charset"] = charset
            return ["1", "2"]

    assert imap_client.search_uids(FakeMB(), "ALL") == ["1", "2"]
    assert sent["charset"] is None


def test_fetch_不带charset():
    from app.core import imap_client

    sent = {}

    class FakeMB:
        def fetch(self, criteria, charset="US-ASCII", **kw):
            sent["charset"] = charset
            return iter(())

    assert imap_client.fetch_uids_parsed(FakeMB(), [1, 2]) == []
    assert sent["charset"] is None


def test_imaplib_已注册ID命令():
    import app.core.imap_client  # noqa: F401 — 导入即注册

    assert "ID" in imaplib.Commands
    assert "AUTH" in imaplib.Commands["ID"]
