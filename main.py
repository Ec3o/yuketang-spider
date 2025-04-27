import httpx
import exercise
import re
import utils
import font_parse

def main():
    # 加载标准哈希映射表
    standard_glyph_hash_map = font_parse.load_hash_map_from_file("glyph_hash_map.json")
    if standard_glyph_hash_map is None:
        print("无法加载标准哈希映射表 glyph_hash_map.json")
        return

    print("[*] 正在爬取雨课堂数据...")
    # 获取题目数据
    exercise_data = exercise.GetExerciseData()
    problems = exercise_data['data']['problems']

    # 下载混淆字体
    font_save_path = 'fonts/font.ttf'
    decrypt_font_url = exercise_data['data']['font']
    print("[*] 字体地址：", decrypt_font_url)
    utils.download_font(decrypt_font_url, font_save_path)

    # 恢复每一道题目的题干和选项
    for index, problem in enumerate(problems):
        problem_type = problem['content']['TypeText']
        problem_body_raw = problem['content']['Body']

        # 恢复题干
        restored_body = utils.restore_text(problem_body_raw, font_save_path, standard_glyph_hash_map)

        print(f"第{index+1}题 题型:{problem_type}")
        print(f"题干:{restored_body}")

        # 如果是选择题，还要处理选项
        if problem_type in ("单选题", "多选题") and 'Options' in problem['content']:
            options = problem['content']['Options']
            for opt in options:
                option_key = opt.get('key', '')
                option_value_raw = opt.get('value', '')
                restored_option = utils.restore_text(option_value_raw, font_save_path, standard_glyph_hash_map)
                print(f"选项 {option_key}: {restored_option}")

        print("-" * 50)

if __name__ == "__main__":
    main()
