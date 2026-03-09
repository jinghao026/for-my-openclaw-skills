---
name: email-attachment-mime-fix
description: |
  邮件附件MIME类型自动识别解决方案
  
  解决邮件附件统一显示为bin格式的问题
  使用Python的mimetypes模块自动识别文件类型
  
  适用场景：
  - 邮件附件显示为application/octet-stream
  - 收件方无法直接识别文件类型
  - 需要发送PDF、Word、Excel等格式文件
---

# 邮件附件MIME类型修复方案

## 问题描述

发送邮件时，附件统一显示为 `bin` 格式或 `application/octet-stream`，收件方无法直接识别文件真实类型（PDF、Word、Excel等）。

## 问题原因

邮件发送代码使用了通用的MIME类型：

```python
# 错误做法
attachment = MIMEBase('application', 'octet-stream')
```

`application/octet-stream` 是通用二进制流类型，邮件客户端无法据此判断文件实际格式。

## 解决方案

使用Python标准库 `mimetypes` 根据文件扩展名自动识别MIME类型：

```python
import mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders

def create_attachment_with_correct_mime(filename, filepath):
    """创建带有正确MIME类型的附件"""
    
    # 1. 自动识别MIME类型
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    
    maintype, subtype = ctype.split('/', 1)
    
    # 2. 读取文件内容
    with open(filepath, 'rb') as f:
        file_data = f.read()
    
    # 3. 根据MIME类型创建对应的附件对象
    if maintype == 'text':
        # 文本文件 (.txt, .csv, .json)
        attachment = MIMEText(
            file_data.decode('utf-8', errors='ignore'), 
            _subtype=subtype, 
            _charset='utf-8'
        )
    elif maintype == 'image':
        # 图片文件 (.jpg, .png, .gif)
        attachment = MIMEImage(file_data, _subtype=subtype)
    elif maintype == 'audio':
        # 音频文件 (.mp3, .wav)
        attachment = MIMEAudio(file_data, _subtype=subtype)
    elif maintype == 'application':
        # 应用程序文件 (.pdf, .doc, .xlsx)
        attachment = MIMEApplication(file_data, _subtype=subtype)
    else:
        # 其他类型使用通用MIMEBase
        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(file_data)
        encoders.encode_base64(attachment)
    
    # 4. 添加Content-Disposition头
    attachment.add_header(
        'Content-Disposition',
        f'attachment; filename="{filename}"'
    )
    
    return attachment
```

## 支持的文件类型映射

| 文件扩展名 | MIME类型 | Python类 |
|-----------|----------|----------|
| .pdf | application/pdf | MIMEApplication |
| .doc | application/msword | MIMEApplication |
| .docx | application/vnd.openxmlformats-officedocument.wordprocessingml.document | MIMEApplication |
| .xls | application/vnd.ms-excel | MIMEApplication |
| .xlsx | application/vnd.openxmlformats-officedocument.spreadsheetml.sheet | MIMEApplication |
| .ppt | application/vnd.ms-powerpoint | MIMEApplication |
| .pptx | application/vnd.openxmlformats-officedocument.presentationml.presentation | MIMEApplication |
| .jpg, .jpeg | image/jpeg | MIMEImage |
| .png | image/png | MIMEImage |
| .gif | image/gif | MIMEImage |
| .txt | text/plain | MIMEText |
| .csv | text/csv | MIMEText |
| .json | application/json | MIMEApplication |
| .zip | application/zip | MIMEApplication |
| .mp3 | audio/mpeg | MIMEAudio |
| .mp4 | video/mp4 | MIMEApplication |

## 完整使用示例

```python
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

def send_email_with_proper_attachments(
    to_email, subject, body, attachments, 
    from_email, password, smtp_server, smtp_port
):
    """
    发送带有正确MIME类型的附件邮件
    
    Args:
        to_email: 收件人邮箱
        subject: 邮件主题
        body: 邮件正文
        attachments: 附件列表 [("文件名", "文件路径"), ...]
        from_email: 发件人邮箱
        password: 邮箱密码/授权码
        smtp_server: SMTP服务器地址
        smtp_port: SMTP端口
    """
    
    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 处理每个附件
    for filename, filepath in attachments:
        if not Path(filepath).exists():
            print(f"警告: 文件不存在 {filepath}")
            continue
        
        # 识别MIME类型
        ctype, _ = mimetypes.guess_type(filepath)
        if ctype is None:
            ctype = 'application/octet-stream'
        
        maintype, subtype = ctype.split('/', 1)
        
        # 读取文件
        with open(filepath, 'rb') as f:
            file_data = f.read()
        
        # 创建对应类型的附件
        if maintype == 'application':
            attachment = MIMEApplication(file_data, _subtype=subtype)
        elif maintype == 'image':
            from email.mime.image import MIMEImage
            attachment = MIMEImage(file_data, _subtype=subtype)
        elif maintype == 'text':
            attachment = MIMEText(
                file_data.decode('utf-8', errors='ignore'),
                _subtype=subtype,
                _charset='utf-8'
            )
        else:
            from email.mime.base import MIMEBase
            from email import encoders
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(file_data)
            encoders.encode_base64(attachment)
        
        # 添加文件名头
        attachment.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename}"'
        )
        
        msg.attach(attachment)
    
    # 发送邮件
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(from_email, password)
        server.send_message(msg)
    
    print(f"邮件已发送至 {to_email}")

# 使用示例
send_email_with_proper_attachments(
    to_email="boss@example.com",
    subject="工作报告",
    body="请查收附件中的报告文件",
    attachments=[
        ("月度报告.pdf", "/path/to/report.pdf"),
        ("数据分析.xlsx", "/path/to/data.xlsx"),
        ("会议照片.jpg", "/path/to/photo.jpg")
    ],
    from_email="your-email@163.com",
    password="your-auth-code",
    smtp_server="smtp.163.com",
    smtp_port=465
)
```

## 扩展MIME类型

如需支持特殊文件格式，可自定义MIME类型映射：

```python
import mimetypes

# 添加自定义MIME类型映射
mimetypes.add_type('application/vnd.custom', '.custom')
mimetypes.add_type('text/x-markdown', '.md')

# 现在可以正确识别.custom和.md文件
ctype = mimetypes.guess_type('file.custom')  # ('application/vnd.custom', None)
```

## 验证方法

发送测试邮件后，可通过以下方式验证MIME类型是否正确：

1. **查看邮件源码**：在邮件客户端选择"显示原始邮件"或"查看源码"
2. **检查Content-Type头**：确认附件部分的 `Content-Type` 字段
3. **正确示例**：
   ```
   Content-Type: application/pdf; name="report.pdf"
   Content-Disposition: attachment; filename="report.pdf"
   ```

## 相关工具函数

```python
def get_file_mime_info(filepath):
    """获取文件的MIME类型信息"""
    ctype, encoding = mimetypes.guess_type(filepath)
    return {
        'path': filepath,
        'mime_type': ctype or 'application/octet-stream',
        'encoding': encoding,
        'is_recognized': ctype is not None
    }

# 批量检查文件类型
files = ['report.pdf', 'data.xlsx', 'image.jpg', 'unknown.xyz']
for f in files:
    info = get_file_mime_info(f)
    print(f"{f}: {info['mime_type']} (识别成功: {info['is_recognized']})")
```

## 注意事项

1. **文件名编码**：非ASCII文件名需使用RFC 2231编码
2. **大文件处理**：大附件建议使用流式读取避免内存溢出
3. **兼容性**：部分老旧邮件客户端可能不支持某些MIME类型
4. **安全考虑**：注意验证文件路径，防止路径遍历攻击

## 参考资料

- [Python mimetypes文档](https://docs.python.org/3/library/mimetypes.html)
- [MIME类型标准](https://www.iana.org/assignments/media-types/media-types.xhtml)
- [RFC 2046 - MIME Part Two](https://tools.ietf.org/html/rfc2046)

---

**创建日期**: 2026-03-09  
**适用版本**: Python 3.7+  
**关联Skill**: email-sender
