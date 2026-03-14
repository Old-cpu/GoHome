from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from models.storage import QuoteStorage, UserStorage
from utils.quote_generator import QuoteGenerator
from routes.auth import login_required

quotes_bp = Blueprint('quotes', __name__)


@quotes_bp.route('/quotes')
@login_required
def index():
    """话语列表"""
    user_id = session['user_id']
    all_quotes = QuoteStorage.get_all_quotes(user_id)
    categories = QuoteGenerator.get_all_categories()

    # 按分类分组
    quotes_by_category = {}
    for quote in all_quotes:
        category = quote.get('category', '其他')
        if category not in quotes_by_category:
            quotes_by_category[category] = []
        quotes_by_category[category].append(quote)

    return render_template('quotes.html', quotes_by_category=quotes_by_category, categories=categories)


@quotes_bp.route('/quotes/add', methods=['GET', 'POST'])
@login_required
def add_quote():
    """添加自定义话语"""
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        category = request.form.get('category', '个人').strip()

        if not content:
            flash('话语内容不能为空', 'error')
            return render_template('quote_add.html')

        if len(content) > 100:
            flash('话语内容不能超过 100 字', 'error')
            return render_template('quote_add.html')

        QuoteStorage.add_custom(session['user_id'], content, category)
        flash('话语添加成功', 'success')
        return redirect(url_for('quotes.index'))

    return render_template('quote_add.html')


@quotes_bp.route('/quotes/delete/<int:quote_id>', methods=['POST'])
@login_required
def delete_quote(quote_id):
    """删除自定义话语"""
    user_id = session['user_id']
    data = QuoteStorage.get_all()

    custom_quotes = data.get('custom', {}).get(str(user_id), [])
    original_count = len(custom_quotes)

    # 过滤掉要删除的话语
    data['custom'][str(user_id)] = [q for q in custom_quotes if q['id'] != quote_id]
    QuoteStorage.save_all(data)

    flash('话语已删除', 'success')
    return redirect(url_for('quotes.index'))
