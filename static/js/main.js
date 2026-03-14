// 思乡签到 - 主脚本文件

// 页面加载完成后的初始化
document.addEventListener('DOMContentLoaded', function() {
    // 自动隐藏 Flash 消息
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        }, 5000);
    });

    // 表单验证增强
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
            let isValid = true;

            inputs.forEach(function(input) {
                if (!input.value.trim()) {
                    isValid = false;
                    input.style.borderColor = 'var(--error-color)';
                } else {
                    input.style.borderColor = 'var(--border-color)';
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('请填写所有必填字段');
            }
        });
    });

    // 输入框聚焦效果
    const inputs = document.querySelectorAll('input, textarea');
    inputs.forEach(function(input) {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
});

// 复制分享文本函数
function copyShareText() {
    const text = document.getElementById('shareText');
    if (text) {
        const range = document.createRange();
        range.selectNode(text);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);
        document.execCommand('copy');
        window.getSelection().removeAllRanges();

        // 显示复制成功提示
        const btn = event.target;
        const originalText = btn.innerText;
        btn.innerText = '已复制!';
        btn.style.background = 'var(--success-color)';
        setTimeout(function() {
            btn.innerText = originalText;
            btn.style.background = '';
        }, 2000);
    }
}

// 确认删除对话框
function confirmDelete(message) {
    return confirm(message || '确定要删除吗？');
}

// 日期格式化
function formatDate(dateString) {
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
}

// 计算天数差
function daysBetween(date1, date2) {
    const oneDay = 24 * 60 * 60 * 1000;
    const firstDate = new Date(date1);
    const secondDate = new Date(date2);
    return Math.round(Math.abs((firstDate - secondDate) / oneDay));
}
