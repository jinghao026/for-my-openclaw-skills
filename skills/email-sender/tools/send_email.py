#!/usr/bin/env python3
"""
邮件发送工具
"""
import json
import smtplib
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
ACCOUNTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'accounts.json')

def load_config(account=None):
    """加载配置文件
    
    Args:
        account: 指定邮箱账号，默认使用默认账号
    """
    # 先尝试加载多账号配置
    if os.path.exists(ACCOUNTS_PATH):
        with open(ACCOUNTS_PATH, 'r') as f:
            accounts = json.load(f)
        
        if account and account in accounts:
            return accounts[account]
        
        # 如果没有指定账号，使用第一个账号
        if accounts:
            first_account = list(accounts.keys())[0]
            return accounts[first_account]
    
    # 回退到单账号配置
    if not os.path.exists(CONFIG_PATH):
        print(f"错误：配置文件不存在: {CONFIG_PATH}")
        print("请先创建配置文件，参考 SKILL.md 说明")
        sys.exit(1)
    
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def send_email(to_emails, subject, body, attachments=None, account=None):
    """
    发送邮件
    
    Args:
        to_emails: 收件人邮箱列表（逗号分隔或列表）
        subject: 邮件主题
        body: 邮件正文
        attachments: 附件路径列表（可选）
        account: 指定发送账号（可选）
    """
    config = load_config(account)
    
    # 解析收件人
    if isinstance(to_emails, str):
        to_emails = [e.strip() for e in to_emails.split(',')]
    
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = config['username']
    msg['To'] = ', '.join(to_emails)
    msg['Subject'] = subject
    
    # 添加正文
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # 添加附件
    if attachments:
        if isinstance(attachments, str):
            attachments = [attachments]
        
        for filepath in attachments:
            if not os.path.exists(filepath):
                print(f"警告：附件不存在: {filepath}")
                continue
            
            filename = os.path.basename(filepath)
            with open(filepath, 'rb') as f:
                attachment = MIMEBase('application', 'octet-stream')
                attachment.set_payload(f.read())
            
            encoders.encode_base64(attachment)
            attachment.add_header(
                'Content-Disposition',
                f'attachment; filename= {filename}'
            )
            msg.attach(attachment)
    
    # 连接 SMTP 服务器并发送
    try:
        server = smtplib.SMTP(config['smtp_server'], config['smtp_port'])
        server.starttls()
        server.login(config['username'], config['password'])
        
        text = msg.as_string()
        server.sendmail(config['username'], to_emails, text)
        server.quit()
        
        print(f"✅ 邮件发送成功！")
        print(f"   收件人: {', '.join(to_emails)}")
        print(f"   主题: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ 发送失败: {str(e)}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("用法: python send_email.py <收件人> <主题> <内容> [账号] [附件路径...]")
        print("示例: python send_email.py 'user@example.com' '测试' 'Hello World' 163")
        sys.exit(1)
    
    to_emails = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    account = sys.argv[4] if len(sys.argv) > 4 else None
    attachments = sys.argv[5:] if len(sys.argv) > 5 else None
    
    send_email(to_emails, subject, body, attachments, account)
