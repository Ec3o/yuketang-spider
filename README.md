# 📚 Yuketang Spider

> 自动爬取雨课堂作业题目，处理字体反爬虫，智能还原乱码，输出完整题库！

---

## ✨ 项目简介

Yuketang Spider 是一个针对雨课堂平台的作业爬取与解密工具。  
它可以自动：
- 爬取雨课堂的作业/测试数据
- 下载网页中使用的加密字体文件
- 对乱码汉字进行逆向还原（通过字体解析 + 哈希比对）
- 恢复题干与选项中的真实文字，输出清晰、可读的题目列表

本项目适用于需要备份雨课堂练习、或研究字体反爬虫机制的同学与开发者。

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```
### 2. 调整参数
根据`config.yaml.example`和实际抓包获取到的参数编写一份`config.yaml`,用于请求发送.
```yaml
sessionid: xxxxxxxxxxxxxxxxxxxxxxxxxxx
uv_id: xxxx
classroom_id: xxxxxxxx
exercise_id: xxxxxxx
xtbz: ykt
```
### 3. 检查映射表
正常来说，映射表`glyph_hash_map.json`会随着项目一起被clone下来.
如果没有，需要手动运行一次`font_parse.py`来生成映射表.
### 4. 运行主函数
```bash
python main.py
```