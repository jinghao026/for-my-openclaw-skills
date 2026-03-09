# Document Parser Skill

✅ **已安装并测试成功！**

支持格式: DOCX ✅ | PPTX ✅ | XLSX ✅ | PDF ✅

一个全面的文档解析 skill，可以读取 Word、PowerPoint、Excel 和 PDF 文件的内容。

## Supported Formats

| Format | Extension | Status |
|--------|-----------|--------|
| Word Document | .docx | ✅ Supported |
| PowerPoint | .pptx | ✅ Supported |
| Excel | .xlsx | ✅ Supported |
| PDF | .pdf | ✅ Supported (with PyMuPDF/MinerU) |

## Installation

```bash
# Install Python dependencies
pip3 install --break-system-packages python-docx python-pptx openpyxl pymupdf

# Or use Docling for comprehensive parsing
pip3 install --break-system-packages docling
```

## Usage

### Read Word Document (.docx)
```python
from docx import Document

def read_docx(file_path):
    doc = Document(file_path)
    text = []
    for para in doc.paragraphs:
        text.append(para.text)
    return '\n'.join(text)
```

### Read PowerPoint (.pptx)
```python
from pptx import Presentation

def read_pptx(file_path):
    prs = Presentation(file_path)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return '\n'.join(text)
```

### Read PDF
```python
import fitz  # PyMuPDF

def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = []
    for page in doc:
        text.append(page.get_text())
    return '\n'.join(text)
```

## ClawHub Skills

Install from ClawHub:
```bash
npx clawhub@latest install pymupdf-pdf-parser-clawdbot-skill
npx clawhub@latest install pdf-parser-mineru
```

## References

- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [python-docx Documentation](https://python-docx.readthedocs.io/)
- [Docling GitHub](https://github.com/docling-project/docling)
