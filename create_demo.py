#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
演示数据生成脚本
用于快速创建测试用户和签到记录
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash
from models.storage import UserStorage, CheckinStorage, QuoteStorage

def create_demo_user():
    """创建演示用户"""
    # 检查是否已存在演示用户
    existing = UserStorage.get_by_username('demo')
    if existing:
        print("演示用户已存在")
        return existing

    user_data = {
        'username': 'demo',
        'password_hash': generate_password_hash('123456'),
        'hometown': '湖南长沙',
        'current_city': '北京',
        'leave_home_date': (datetime.now() - timedelta(days=158)).strftime('%Y-%m-%d'),
        'created_at': datetime.now().isoformat()
    }
    user = UserStorage.create(user_data)
    print(f"创建演示用户：{user['username']} (密码：123456)")
    return user

def create_demo_checkins(user_id):
    """创建演示签到记录"""
    existing = CheckinStorage.get_by_user(user_id)
    if existing:
        print("演示签到记录已存在")
        return

    # 创建最近 7 天中有 5 天签到的记录
    today = datetime.now()
    checkin_days = [0, 1, 2, 4, 5, 6]  # 除了 3 天前都签到了

    for days_ago in checkin_days:
        checkin_date = today - timedelta(days=days_ago)
        checkin_data = {
            'checkin_date': checkin_date.strftime('%Y-%m-%d'),
            'checkin_time': checkin_date.replace(hour=9, minute=30).isoformat(),
            'quote_id': (days_ago % 20) + 1
        }
        CheckinStorage.add_checkin(user_id, checkin_data)

    print(f"创建 {len(checkin_days)} 条签到记录")

def main():
    print("=" * 50)
    print("思乡签到 - 演示数据生成")
    print("=" * 50)

    user = create_demo_user()
    create_demo_checkins(user['id'])

    print("=" * 50)
    print("演示数据创建完成!")
    print(f"登录账号：demo")
    print(f"登录密码：123456")
    print(f"访问地址：http://localhost:5001")
    print("=" * 50)

if __name__ == '__main__':
    main()
