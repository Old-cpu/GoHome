import random
from models.storage import QuoteStorage


class QuoteGenerator:
    """思乡话语生成器"""

    @staticmethod
    def get_random_quote(user_id=None):
        """获取随机一句思乡话语"""
        if user_id:
            quotes = QuoteStorage.get_all_quotes(user_id)
        else:
            quotes = QuoteStorage.get_built_in()

        if not quotes:
            return {
                'id': 0,
                'content': '家，是心中永远的港湾。',
                'category': '默认'
            }

        return random.choice(quotes)

    @staticmethod
    def get_quote_by_id(quote_id):
        """根据 ID 获取话语"""
        built_in = QuoteStorage.get_built_in()
        for quote in built_in:
            if quote['id'] == quote_id:
                return quote

        # 在所有用户自定义中查找
        data = QuoteStorage.get_all()
        for user_quotes in data.get('custom', {}).values():
            for quote in user_quotes:
                if quote['id'] == quote_id:
                    return quote

        return None

    @staticmethod
    def get_quotes_by_category(category, user_id=None):
        """按分类获取话语"""
        if user_id:
            quotes = QuoteStorage.get_all_quotes(user_id)
        else:
            quotes = QuoteStorage.get_built_in()

        return [q for q in quotes if q.get('category') == category]

    @staticmethod
    def get_all_categories():
        """获取所有分类"""
        quotes = QuoteStorage.get_built_in()
        categories = list(set(q.get('category', '其他') for q in quotes))
        return categories
