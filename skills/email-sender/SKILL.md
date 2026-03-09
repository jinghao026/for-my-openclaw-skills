---
name: email-sender
description: |
  通用邮件发送工具，支持多种SMTP服务器（Gmail、QQ、163、Outlook等）。
  支持纯文本、HTML邮件和附件发送。
  
  特性：
  - 支持多种邮箱服务商
  - 支持纯文本和HTML邮件
  - 支持附件发送（自动识别MIME类型，避免bin格式问题）
  - 自动处理SSL/TLS加密
  - 配置文件管理
  - 智能文件类型识别（PDF、Word、Excel、图片等）
---

# Email Sender Skill

通用邮件发送工具，支持 Gmail、QQ、163、Outlook 等主流邮箱。

## 快速开始

### 1. 配置邮箱

创建配置文件 `~/.openclaw/.env`：

```bash
# Gmail 示例
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_SENDER=your-email@gmail.com
EMAIL_SMTP_PASSWORD=your-app-password
EMAIL_USE_TLS=true

# QQ邮箱示例
EMAIL_SMTP_SERVER=smtp.qq.com
EMAIL_SMTP_PORT=465
EMAIL_SENDER=your-qq@qq.com
EMAIL_SMTP_PASSWORD=your-auth-code
EMAIL_USE_TLS=false

# 163邮箱示例
EMAIL_SMTP_SERVER=smtp.163.com
EMAIL_SMTP_PORT=465
EMAIL_SENDER=your-email@163.com
EMAIL_SMTP_PASSWORD=your-auth-code
EMAIL_USE_TLS=false
```

### 2. 发送邮件

```python
from skills.email_sender.email_sender import send_email, send_html_email, send_email_with_attachments

# 发送纯文本邮件
send_email(
    to_email="recipient@example.com",
    subject="测试邮件",
    body="这是一封测试邮件"
)

# 发送HTML邮件
send_html_email(
    to_email="recipient@example.com",
    subject="HTML邮件",
    html_body="<h1>标题</h1><p>内容</p>"
)

# 发送带附件的邮件（自动识别文件类型）
send_email_with_attachments(
    to_email="recipient@example.com",
    subject="带附件的邮件",
    body="请查收附件",
    attachments=[
        ("report.pdf", "/path/to/report.pdf"),
        ("data.xlsx", "/path/to/data.xlsx"),
        ("image.jpg", "/path/to/image.jpg")
    ]
)
```

## 支持的文件类型

附件发送时会自动识别MIME类型，确保收件方正确显示文件格式：

| 文件类型 | 扩展名 | MIME类型 |
|----------|--------|----------|
| PDF | .pdf | application/pdf |
| Word文档 | .doc, .docx | application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document |
| Excel表格 | .xls, .xlsx | application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet |
| PowerPoint | .ppt, .pptx | application/vnd.ms-powerpoint |
| 图片 | .jpg, .jpeg, .png, .gif, .bmp | image/jpeg, image/png, image/gif |
| 文本 | .txt, .csv, .json | text/plain, text/csv, application/json |
| 压缩包 | .zip, .rar, .7z | application/zip, application/x-rar-compressed |
| 其他 | 任意 | 自动识别或application/octet-stream |

## 支持的邮箱服务商

| 服务商 | SMTP服务器 | 端口 | 密码类型 |
|--------|-----------|------|----------|
| Gmail | smtp.gmail.com | 587 | App Password |
| QQ邮箱 | smtp.qq.com | 465 | 授权码 |
| 163邮箱 | smtp.163.com | 465 | 授权码 |
| Outlook | smtp.office365.com | 587 | 邮箱密码 |
| 飞书 | smtp.feishu.cn | 465 | 邮箱密码 |

## 获取授权码

### Gmail App Password
1. 开启两步验证
2. 访问 https://myaccount.google.com/apppasswords
3. 生成 16 位 App Password

### QQ邮箱授权码
1. 登录 mail.qq.com
2. 设置 → 账户 → POP3/IMAP/SMTP
3. 开启 SMTP 服务，获取授权码

### 163邮箱授权码
1. 登录 mail.163.com
2. 设置 → POP3/SMTP/IMAP
3. 开启 SMTP 服务，获取授权码

## 命令行使用

```bash
# 发送纯文本邮件
python3 skills/email_sender/email_sender.py \
  --to "recipient@example.com" \
  --subject "测试" \
  --body "内容"

# 发送HTML邮件
python3 skills/email_sender/email_sender.py \
  --to "recipient@example.com" \
  --subject "测试" \
  --body "<h1>标题</h1>" \
  --html

# 发送带附件的邮件（自动识别类型）
python3 skills/email_sender/email_sender.py \
  --to "recipient@example.com" \
  --subject "测试" \
  --body "请查收" \
  --attachments "report.pdf,data.xlsx,image.jpg"
```

## 常见问题

### Q: 为什么附件显示为bin格式？
**A:** 这是因为MIME类型未正确设置。本工具已修复该问题，使用 `mimetypes` 模块自动识别文件类型，确保PDF显示为PDF、Word显示为Word文档。

### Q: 某些特殊格式无法识别怎么办？
**A:** 工具会自动退化为 `application/octet-stream`，收件方可以手动选择打开方式。如需支持特定格式，可联系管理员扩展MIME类型映射。

## 注意事项

- 使用授权码而不是邮箱密码（QQ、163等）
- Gmail 必须使用 App Password
- 确保网络环境可以访问 SMTP 服务器
- 部分邮箱有发送频率限制
- 大附件可能受邮箱服务商大小限制

## 依赖

- Python 3.7+
- 标准库（smtplib, email, ssl, os, mimetypes）

## 更新日志

- **2026-03-09**: 修复附件MIME类型识别问题，支持自动识别PDF、Word、Excel、图片等格式，避免bin格式问题
- **2026-03-05**: 初始版本，支持多服务商 SMTP 发送
