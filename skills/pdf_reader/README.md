# PDF 读取技能

> "让 Chronos 能阅读 PDF 文档。"

## 依赖

```bash
cd /home/claworc/.openclaw/workspace
./scrapling_env/bin/pip install pymupdf
```

## 使用方法

### 命令行

```bash
./scrapling_env/bin/python skills/pdf_reader/read.py <pdf 文件路径>
```

### Python API

```python
from skills.pdf_reader.read import read_pdf

text = read_pdf("/path/to/file.pdf")
print(text)
```

## 输出

- 提取 PDF 全部文本内容
- 按页面分隔
- 支持中文

## 限制

- 仅支持文本型 PDF（非扫描图片）
- 加密 PDF 需要密码

---

**状态：** 🟢 已创建
**依赖：** PyMuPDF (fitz)
