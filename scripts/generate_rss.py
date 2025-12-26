from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path

UTC = timezone.utc
BASE_URL = "https://sakurai-shift.github.io/rss-test"  # 末尾スラッシュなし推奨


def rfc2822(dt: datetime) -> str:
    # RFC 2822: "Fri, 26 Dec 2025 00:00:00 +0000" 形式（ロケール依存なし）
    return format_datetime(dt)


def build(days_ago: int, out_path: Path) -> None:
    now = datetime.now(UTC).replace(microsecond=0)
    pub = (now - timedelta(days=days_ago)).replace(
        hour=23, minute=27, second=44, microsecond=0
    )

    base = BASE_URL.rstrip("/")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"
  xmlns:content="http://purl.org/rss/1.0/modules/content/"
  xmlns:wfw="http://wellformedweb.org/CommentAPI/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"
  xmlns:slash="http://purl.org/rss/1.0/modules/slash/"
>

  <channel>
    <title>遊技台・検定情報 &#8211; テスト（{days_ago}日前） &#8211; P-MEDIA JAPAN</title>
    <atom:link href="{base}/feed-{days_ago}days.xml" rel="self" type="application/rss+xml" />
    <link>https://p-media.info</link>
    <description>パチンコ業界人のためのプロフェッショナルサイト（境界値テスト用）</description>
    <lastBuildDate>{rfc2822(now)}</lastBuildDate>
    <language>ja</language>
    <sy:updatePeriod>hourly</sy:updatePeriod>
    <sy:updateFrequency>1</sy:updateFrequency>
    <generator>https://wordpress.org/?v=5.1.10</generator>

    <item>
      <title>【テスト】pubDate {days_ago}日前の記事</title>
      <link>https://p-media.info/post-test-{days_ago}/</link>
      <pubDate>{rfc2822(pub)}</pubDate>
      <dc:creator><![CDATA[testuser]]></dc:creator>
      <category><![CDATA[遊技台・検定情報]]></category>
      <guid isPermaLink="false">https://p-media.info/?p=test-{days_ago}</guid>
      <description><![CDATA[境界値テスト用（{days_ago}日前）]]></description>
    </item>
  </channel>
</rss>
"""
    out_path.write_text(xml, encoding="utf-8", newline="\n")


def main() -> None:
    # scripts/ 配下から実行しても、常にリポジトリルートに出力する
    repo_root = Path(__file__).resolve().parents[1]

    for days in (89, 90, 91):
        build(days, repo_root / f"feed-{days}days.xml")


if __name__ == "__main__":
    main()
