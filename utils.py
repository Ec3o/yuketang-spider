import re
import requests
import font_parse
def clean_html(raw_html: str) -> str:
    """去除 HTML 标签"""
    clean_text = re.sub(r'<[^>]+>', '', raw_html)
    return clean_text.strip()


def download_font(url, save_path):
    """下载字体到指定目录文件名"""
    response = requests.get(url)
    response.raise_for_status()
    with open(save_path, 'wb') as f:
        f.write(response.content)
    print(f"[*] 字体已下载并保存至 {save_path}")

def restore_text(raw_html, font_path, hash_map):
    """
    辅助函数：清理html + 逐字符还原乱码
    """
    text = clean_html(raw_html)  # 先清除HTML标签
    restored = ""
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            real_char = font_parse.parse_obfuscated_char(ch, font_path, hash_map)
            restored += real_char if real_char else ch
        else:
            restored += ch
    return restored