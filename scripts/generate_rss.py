from __future__ import annotations

from datetime import datetime, timedelta, timezone
from email.utils import format_datetime
from pathlib import Path

UTC = timezone.utc
BASE_URL = "https://sakurai-shift.github.io/rss-test"  # 末尾スラッシュなし推奨


def rfc2822(dt: datetime) -> str:
    # RFC 2822: "Fri, 26 Dec 2025 00:00:00 +0000" 形式（ロケール依存なし）
    return format_datetime(dt)


def build(days_ago: int, out_path: Path, item_count: int = 30) -> None:
    now = datetime.now(UTC).replace(microsecond=0)

    # ★ここを「元のやつ」に戻す：days_ago 日前の 23:27:44 固定
    pub = (now - timedelta(days=days_ago)).replace(
        hour=23, minute=27, second=44, microsecond=0
    )

    base = BASE_URL.rstrip("/")

    items_xml = []
    for i in range(1, item_count + 1):
        # 89日前の場合の特別処理
        is_special_89 = days_ago == 89 and i in (1, 2, 3, 4, 5, 6, 7, 21, 22, 23, 24, 25, 26, 27)

        if is_special_89:
            # 89日前の特別なアイテムの設定
            if i == 1:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}更新"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousin/"
                updated_pub = (now - timedelta(days=days_ago)).replace(
                    hour=23, minute=59, second=59, microsecond=0,
                    tzinfo=timezone(timedelta(hours=9))
                )
            elif i == 2:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}更新"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousin/"
                updated_pub = (now - timedelta(days=days_ago-1)).replace(
                    hour=0, minute=0, second=0, microsecond=0,
                    tzinfo=timezone(timedelta(hours=9))
                )
            elif i == 3:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}titleのみ更新"
                link = f"https://p-media.info/post-test-{days_ago}-{i}/"
                updated_pub = pub  # 通常のpubDate
            elif i == 4:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}"
                link = f"https://p-media.info/post-test-{days_ago}-{i}/"
                updated_pub = pub.replace(second=0)  # 秒を0に
            elif i == 5:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousin/"
                updated_pub = pub  # 通常のpubDate
            elif i == 6:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}更新対象確認"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousintaisyou/"
                updated_pub = (now - timedelta(days=days_ago)).replace(
                    hour=23, minute=59, second=59, microsecond=0,
                    tzinfo=timezone(timedelta(hours=9))
                )
            elif i == 7:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}更新対象確認"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousintaisyou/"
                updated_pub = (now - timedelta(days=days_ago-1)).replace(
                    hour=0, minute=0, second=0, microsecond=0,
                    tzinfo=timezone(timedelta(hours=9))
                )
            elif i == 21:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}更新"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousin/"
                updated_pub = (now - timedelta(days=days_ago)).replace(
                    hour=14, minute=59, second=59, microsecond=0,
                    tzinfo=UTC
                )
            elif i == 22:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}更新"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousin/"
                updated_pub = (now - timedelta(days=days_ago)).replace(
                    hour=15, minute=0, second=0, microsecond=0,
                    tzinfo=UTC
                )
            elif i == 23:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}titleのみ更新"
                link = f"https://p-media.info/post-test-{days_ago}-{i}/"
                updated_pub = pub  # 通常のpubDate
            elif i == 24:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}"
                link = f"https://p-media.info/post-test-{days_ago}-{i}/"
                updated_pub = pub.replace(second=0)  # 秒を0に
            elif i == 25:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousin/"
                updated_pub = pub  # 通常のpubDate
            elif i == 26:
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}更新対象確認"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousintaisyou/"
                updated_pub = (now - timedelta(days=days_ago)).replace(
                    hour=14, minute=59, second=59, microsecond=0,
                    tzinfo=UTC
                )
            else:  # i == 27
                title = f"【テスト】pubDate {days_ago}日前の記事-{i}更新対象確認"
                link = f"https://p-media.info/post-test-{days_ago}-{i}kousintaisyou/"
                updated_pub = (now - timedelta(days=days_ago)).replace(
                    hour=15, minute=0, second=0, microsecond=0,
                    tzinfo=UTC
                )

            pub_date = rfc2822(updated_pub)
            creator_cdata = "<![CDATA[ testuser ]]>"
            category_cdata = "<![CDATA[ 遊技台・検定情報 ]]>"
            desc_cdata = f"<![CDATA[ 境界値テスト用（{days_ago}日前 / item{i}） ]]>"
        else:
            # 通常版の設定
            title = f"【テスト】pubDate {days_ago}日前の記事-{i}"
            link = f"https://p-media.info/post-test-{days_ago}-{i}/"
            pub_date = rfc2822(pub)
            creator_cdata = "<![CDATA[ testuser ]]>"
            category_cdata = "<![CDATA[ 遊技台・検定情報 ]]>"
            desc_cdata = f"<![CDATA[ 境界値テスト用（{days_ago}日前 / item{i}） ]]>"

        # 1〜19: guidあり / 20〜30: guidなし
        guid_xml = ""
        if i <= 19:
            guid = f"https://p-media.info/?p=test-{days_ago}-{i}"
            guid_xml = f'\n      <guid isPermaLink="false">{guid}</guid>'

        item = f"""    <item>
      <title>{title}</title>
      <link>{link}</link>
      <pubDate>{pub_date}</pubDate>
      <dc:creator>{creator_cdata}</dc:creator>
      <category>{category_cdata}</category>{guid_xml}
      <description>{desc_cdata}</description>
    </item>"""
        items_xml.append(item)

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

{chr(10).join(items_xml)}
  </channel>
</rss>
"""
    out_path.write_text(xml, encoding="utf-8", newline="\n")


def main() -> None:
    # scripts/ 配下から実行しても、常にリポジトリルートに出力する
    repo_root = Path(__file__).resolve().parents[1]

    for days in (89, 90, 91):
        build(days, repo_root / f"feed-{days}days.xml", item_count=30)


if __name__ == "__main__":
    main()
