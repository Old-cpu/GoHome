from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from datetime import datetime
from models.user import User
from models.storage import CheckinStorage, QuoteStorage, UserStorage
from utils.quote_generator import QuoteGenerator
from routes.auth import login_required

checkin_bp = Blueprint('checkin', __name__)


@checkin_bp.route('/checkin', methods=['GET', 'POST'])
@login_required
def do_checkin():
    """签到打卡"""
    user = User(UserStorage.get_by_id(session['user_id']))

    if request.method == 'POST':
        # 检查今天是否已签到
        if user.has_checked_in_today():
            flash('今天已经签到过了', 'info')
            return redirect(url_for('dashboard.index'))

        # 获取或生成思乡话语
        quote = QuoteGenerator.get_random_quote(user.id)

        # 创建签到记录
        checkin_data = {
            'checkin_date': datetime.now().strftime('%Y-%m-%d'),
            'checkin_time': datetime.now().isoformat(),
            'quote_id': quote['id']
        }
        CheckinStorage.add_checkin(user.id, checkin_data)

        flash('签到成功！', 'success')
        return render_template('checkin_result.html', user=user, quote=quote)

    # GET 请求显示签到页面
    if user.has_checked_in_today():
        flash('今天已经签到过了', 'info')
        return redirect(url_for('dashboard.index'))

    return render_template('checkin.html', user=user)


@checkin_bp.route('/checkin/history')
@login_required
def history():
    """签到历史"""
    user = User(UserStorage.get_by_id(session['user_id']))
    checkins = CheckinStorage.get_by_user(user.id)

    # 按时间倒序排列
    checkins = sorted(checkins, key=lambda x: x.get('checkin_time', ''), reverse=True)

    # 获取每条签到对应的话语
    for checkin in checkins:
        quote_id = checkin.get('quote_id')
        if quote_id:
            quote = QuoteGenerator.get_quote_by_id(quote_id)
            checkin['quote'] = quote

    return render_template('checkin_history.html', user=user, checkins=checkins)
