from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from email.utils import format_datetime, parsedate_to_datetime
from pathlib import Path
from xml.etree import ElementTree as ET

UTC = timezone.utc
JST = timezone(timedelta(hours=9))


def rfc2822(dt: datetime) -> str:
    """RFC 2822形式の日時文字列を返す"""
    return format_datetime(dt)


def parse_pubdate_from_title(title: str) -> tuple[int | None, tuple[int, int, int] | None]:
    """
    タイトルから日数と時刻を抽出
    例: "【テスト】pubDate 91日前の23時59分の記事-guidありそのまま" -> (91, (23, 59, 59))
    例: "【テスト】pubDate 90日前の0時0分の記事-guidありそのまま" -> (90, (0, 0, 0))
    例: "【テスト】pubDate 90日前の記事-1" -> (90, None)
    """
    # パターン: "91日前の23時59分" のような形式
    pattern = r'(\d+)日前の(\d+)時(\d+)分'
    match = re.search(pattern, title)
    if match:
        days = int(match.group(1))
        hour = int(match.group(2))
        minute = int(match.group(3))
        # 秒の推測: 23時59分の場合は59秒、0時0分の場合は0秒、その他は既存のpubDateから取得
        if hour == 23 and minute == 59:
            second = 59
        elif hour == 0 and minute == 0:
            second = 0
        else:
            # その他の場合は、既存のpubDateから取得する必要があるためNoneを返す
            # 実際の処理では既存のpubDateから秒を取得する
            second = 0  # デフォルト値
        return days, (hour, minute, second)

    # パターン: "90日前の記事" のような形式（時刻指定なし）
    pattern_simple = r'(\d+)日前の記事'
    match_simple = re.search(pattern_simple, title)
    if match_simple:
        days = int(match_simple.group(1))
        return days, None

    return None, None


def update_feed_regist(xml_path: Path) -> None:
    """feed-regist.xmlを更新する"""
    # XMLファイルを読み込む
    content = xml_path.read_text(encoding='utf-8')

    # 現在の日時を取得
    now = datetime.now(UTC).replace(microsecond=0)

    # lastBuildDateを更新
    last_build_pattern = r'(<lastBuildDate>)(.*?)(</lastBuildDate>)'
    new_last_build = rfc2822(now)
    content = re.sub(
        last_build_pattern,
        lambda m: f"{m.group(1)}{new_last_build}{m.group(3)}",
        content,
        flags=re.DOTALL
    )

    # XMLを解析して各itemを処理
    tree = ET.fromstring(content)
    items = tree.findall('.//item')

    # 各itemのpubDateを更新
    for item in items:
        title_elem = item.find('title')
        pubdate_elem = item.find('pubDate')

        if title_elem is None or pubdate_elem is None:
            continue

        title = title_elem.text or ""
        old_pubdate_str = pubdate_elem.text or ""

        # タイトルから日数と時刻を抽出
        days_ago, time_tuple = parse_pubdate_from_title(title)

        # 既存のpubDateを解析
        try:
            old_dt = parsedate_to_datetime(old_pubdate_str)
            old_tz = old_dt.tzinfo if old_dt.tzinfo else UTC
        except Exception:
            continue

        # 新しいpubDateを計算
        if days_ago is not None:
            # タイトルから日数が取得できた場合
            if time_tuple is not None:
                # 時刻も指定されている場合
                hour, minute, second_from_title = time_tuple
                # 秒が0の場合は既存のpubDateから秒を取得（タイトルに秒が明示されていないため）
                if second_from_title == 0 and hour == 0 and minute == 0:
                    # 0時0分の場合は0秒
                    second = 0
                elif second_from_title == 59:
                    # 59秒が指定されている場合
                    second = 59
                else:
                    # その他の場合は既存のpubDateから秒を取得
                    second = old_dt.second
                new_dt = (now - timedelta(days=days_ago)).replace(
                    hour=hour, minute=minute, second=second, microsecond=0
                )
                # 既存のタイムゾーンを維持
                new_dt = new_dt.replace(tzinfo=old_tz)
            else:
                # 時刻が指定されていない場合は、既存の時刻を維持
                new_dt = (now - timedelta(days=days_ago)).replace(
                    hour=old_dt.hour, minute=old_dt.minute, second=old_dt.second, microsecond=0
                )
                new_dt = new_dt.replace(tzinfo=old_tz)
        else:
            # タイトルから日数が取得できない場合は、既存のpubDateから相対日数を計算
            delta = now - old_dt.replace(tzinfo=UTC)
            days_ago = delta.days
            new_dt = (now - timedelta(days=days_ago)).replace(
                hour=old_dt.hour, minute=old_dt.minute, second=old_dt.second, microsecond=0
            )
            new_dt = new_dt.replace(tzinfo=old_tz)

        new_pubdate_str = rfc2822(new_dt)

        # 正規表現で置換（既存のフォーマットを保持）
        # エスケープして正確にマッチさせる
        escaped_old = re.escape(old_pubdate_str)
        pubdate_pattern = f'<pubDate>{escaped_old}</pubDate>'
        content = re.sub(
            pubdate_pattern,
            f'<pubDate>{new_pubdate_str}</pubDate>',
            content
        )

    # ファイルに書き込む
    xml_path.write_text(content, encoding='utf-8', newline='\n')


def main() -> None:
    """メイン関数"""
    # リポジトリルートを取得
    repo_root = Path(__file__).resolve().parents[1]
    xml_path = repo_root / "feed-regist.xml"

    if not xml_path.exists():
        print(f"エラー: {xml_path} が見つかりません")
        return

    print(f"更新中: {xml_path}")
    update_feed_regist(xml_path)
    print("更新完了")


if __name__ == "__main__":
    main()
