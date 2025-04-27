# font_parse.py
import json
import hashlib
import os
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import RecordingPen

# 字体文件路径
FONT_PATH = "fonts/SourceHanSansSC-VF.ttf"
HASH_MAP_PATH = "glyph_hash_map.json"

# 加载字体
font = TTFont(FONT_PATH)
glyph_set = font.getGlyphSet()

def hash_glyph(glyph_name):
    """
    根据字形名提取绘制指令并返回其SHA-1哈希值。
    """
    if glyph_name not in glyph_set:
        raise ValueError(f"字形 {glyph_name} 不存在于字体中")

    glyph = glyph_set[glyph_name]
    pen = RecordingPen()
    glyph.draw(pen)

    commands_list = [(command, points) for command, points in pen.value]
    commands_json = json.dumps(commands_list, separators=(',', ':'), ensure_ascii=False)

    hash_obj = hashlib.sha1()
    hash_obj.update(commands_json.encode('utf-8'))
    glyph_hash = hash_obj.hexdigest()

    return glyph_hash

def build_glyph_hash_map():
    """
    遍历整个字体，建立 {hash: glyph_name} 的映射表。
    """
    glyph_hash_map = {}
    for glyph_name in glyph_set.keys():
        try:
            glyph_hash = hash_glyph(glyph_name)
            glyph_hash_map[glyph_hash] = glyph_name
        except Exception as e:
            print(f"处理 {glyph_name} 出错: {e}")
    return glyph_hash_map

def save_hash_map_to_file(hash_map, path):
    """
    将哈希表保存到JSON文件。
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(hash_map, f, ensure_ascii=False, indent=2)
    print(f"哈希表已保存到 {path}")

def load_hash_map_from_file(path):
    """
    从JSON文件加载哈希表。
    """
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_glyph_by_hash(target_hash, glyph_hash_map):
    """
    输入目标哈希值，返回对应的 glyph_name。
    """
    return glyph_hash_map.get(target_hash, None)

def glyph_name_to_char(glyph_name):
    """
    将 'uniXXXX' 形式的 glyph_name 转换成真实中文字符。
    """
    if glyph_name and glyph_name.startswith("uni") and len(glyph_name) == 7:
        try:
            code_point = int(glyph_name[3:], 16)
            return chr(code_point)
        except ValueError:
            return None
    return None

# 主程序示例
if __name__ == "__main__":
    # 尝试先加载已有哈希表
    glyph_hash_map = load_hash_map_from_file(HASH_MAP_PATH)

    if glyph_hash_map is None:
        print("未找到缓存哈希表，正在重新生成...")
        glyph_hash_map = build_glyph_hash_map()
        save_hash_map_to_file(glyph_hash_map, HASH_MAP_PATH)

    # 测试：查询某个字形的哈希值
    test_glyph = "uni4E73"
    h = hash_glyph(test_glyph)
    print(f"字形 {test_glyph} 的哈希值是:", h)

    # 用哈希值反查
    found_glyph = find_glyph_by_hash(h, glyph_hash_map)
    character = glyph_name_to_char(found_glyph)
    if found_glyph:
        print(f"通过哈希值 {h} 找到字形名: {found_glyph} 对应汉字: {character}")
    else:
        print("未找到对应的字形")
def parse_obfuscated_char(char, obfuscated_font_path, standard_glyph_hash_map):
    """
    输入一个乱码汉字，使用混淆字体解析，返回真实汉字。

    参数:
        char (str): 单个乱码字符
        obfuscated_font_path (str): 混淆字体文件路径
        standard_glyph_hash_map (dict): 标准字体的 {hash: glyph_name} 映射表

    返回:
        str: 真实汉字，如果无法识别返回 None
    """
    # 打开混淆字体
    font = TTFont(obfuscated_font_path)
    glyph_set = font.getGlyphSet()

    # 获取字符对应的unicode编码
    codepoint = ord(char)  # 比如 "A" -> 65

    # 找到unicode -> glyph name映射
    cmap_table = None
    for table in font['cmap'].tables:
        if table.isUnicode():
            cmap_table = table
            break

    if cmap_table is None:
        raise ValueError("字体文件中没有有效的Unicode cmap表")

    glyph_name = cmap_table.cmap.get(codepoint)
    if glyph_name is None:
        # print(f"字符 {char} (U+{codepoint:04X}) 不在字体cmap表中")
        return None

    # 取出字形，生成指令哈希
    pen = RecordingPen()
    glyph = glyph_set[glyph_name]
    glyph.draw(pen)

    commands_list = [(command, points) for command, points in pen.value]
    commands_json = json.dumps(commands_list, separators=(',', ':'), ensure_ascii=False)

    hash_obj = hashlib.sha1()
    hash_obj.update(commands_json.encode('utf-8'))
    glyph_hash = hash_obj.hexdigest()

    # 根据哈希在标准表反查
    standard_glyph_name = standard_glyph_hash_map.get(glyph_hash)
    if standard_glyph_name is None:
        print(f"字符 {char} 的哈希 {glyph_hash} 未找到对应标准字形")
        return None

    # 转回真实汉字
    real_char = glyph_name_to_char(standard_glyph_name)
    return real_char
