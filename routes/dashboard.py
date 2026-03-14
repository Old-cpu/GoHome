from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from datetime import datetime, timedelta
from models.user import User
from models.storage import UserStorage, CheckinStorage
from routes.auth import login_required

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    """个人主页/仪表盘"""
    user = User(UserStorage.get_by_id(session['user_id']))
    stats = user.get_checkin_stats()
    days_away = user.get_days_away_from_home()

    # 获取最近 7 天的签到情况
    recent_checkins = CheckinStorage.get_by_user(user.id)
    recent_dates = [c['checkin_date'] for c in recent_checkins]

    # 生成最近 7 天的日历
    today = datetime.now().date()
    week_calendar = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        date_str = date.strftime('%Y-%m-%d')
        week_calendar.append({
            'date': date_str,
            'day': date.strftime('%m/%d'),
            'weekday': ['一', '二', '三', '四', '五', '六', '日'][date.weekday()],
            'checked': date_str in recent_dates
        })

    # 获取最后一次签到
    last_checkin = user.get_last_checkin()

    return render_template('dashboard.html',
                         user=user,
                         stats=stats,
                         days_away=days_away,
                         week_calendar=week_calendar,
                         last_checkin=last_checkin)


@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """个人资料设置"""
    user = User(UserStorage.get_by_id(session['user_id']))
    stats = user.get_checkin_stats()

    if request.method == 'POST':
        hometown = request.form.get('hometown', '').strip()
        current_city = request.form.get('current_city', '').strip()
        leave_home_date = request.form.get('leave_home_date', '')

        # 更新用户信息
        users = UserStorage.get_all()
        users[str(user.id)]['hometown'] = hometown
        users[str(user.id)]['current_city'] = current_city
        users[str(user.id)]['leave_home_date'] = leave_home_date
        UserStorage.save_all(users)

        flash('个人资料已更新', 'success')
        return redirect(url_for('dashboard.profile'))

    return render_template('profile.html', user=user, stats=stats)
