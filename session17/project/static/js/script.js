// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 自动隐藏Flash消息
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        }, 5000); // 5秒后自动隐藏
    });

    // 确认删除操作
    const deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('确定要删除吗？此操作不可恢复！')) {
                e.preventDefault();
            }
        });
    });

    // 搜索框焦点效果
    const searchInput = document.querySelector('.nav-search input');
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.style.width = '250px';
        });
        
        searchInput.addEventListener('blur', function() {
            if (this.value === '') {
                this.style.width = '200px';
            }
        });
    }

    // 文章内容代码块美化
    const codeBlocks = document.querySelectorAll('pre code');
    codeBlocks.forEach(function(block) {
        // 添加行号
        const lines = block.innerHTML.split('\n');
        if (lines.length > 1) {
            const lineNumbers = lines.map((_, i) => i + 1).join('\n');
            const lineNumberDiv = document.createElement('div');
            lineNumberDiv.className = 'line-numbers';
            lineNumberDiv.textContent = lineNumbers;
            block.parentElement.insertBefore(lineNumberDiv, block);
            block.parentElement.style.position = 'relative';
            block.parentElement.style.paddingLeft = '3em';
        }
    });

    // 平滑滚动到顶部
    const scrollToTop = function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    };

    // 显示/隐藏返回顶部按钮
    let scrollButton = document.createElement('button');
    scrollButton.innerHTML = '↑';
    scrollButton.className = 'scroll-to-top';
    scrollButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 40px;
        height: 40px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 50%;
        cursor: pointer;
        display: none;
        font-size: 20px;
        z-index: 1000;
    `;
    document.body.appendChild(scrollButton);

    scrollButton.addEventListener('click', scrollToTop);

    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            scrollButton.style.display = 'block';
        } else {
            scrollButton.style.display = 'none';
        }
    });

    // 文章字数统计
    const postContent = document.querySelector('.post-detail .post-content');
    if (postContent) {
        const text = postContent.textContent || postContent.innerText;
        const wordCount = text.trim().length;
        const readTime = Math.ceil(wordCount / 300); // 假设每分钟阅读300字
        
        const statsElement = document.createElement('div');
        statsElement.className = 'reading-stats';
        statsElement.innerHTML = `约 ${wordCount} 字 · 阅读时间 ${readTime} 分钟`;
        statsElement.style.cssText = `
            color: #666;
            font-size: 14px;
            margin-bottom: 20px;
            padding: 10px;
            background-color: #f8f9fa;
            border-radius: 4px;
        `;
        
        const postHeader = document.querySelector('.post-detail .post-header');
        if (postHeader) {
            postHeader.appendChild(statsElement);
        }
    }

    // 标签云动画
    const tags = document.querySelectorAll('.tag-cloud .tag');
    tags.forEach(function(tag, index) {
        tag.style.animationDelay = `${index * 0.1}s`;
        tag.style.animation = 'fadeIn 0.5s ease-in-out forwards';
    });

    // 添加CSS动画
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .line-numbers {
            position: absolute;
            left: 0;
            top: 1rem;
            width: 2em;
            text-align: right;
            color: #999;
            font-size: 0.875em;
            line-height: 1.5;
            user-select: none;
        }
        
        .scroll-to-top:hover {
            background-color: #0056b3 !important;
        }
    `;
    document.head.appendChild(style);

    // 表单验证增强
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc3545';
                    
                    // 添加错误提示
                    let errorMsg = field.nextElementSibling;
                    if (!errorMsg || !errorMsg.classList.contains('field-error')) {
                        errorMsg = document.createElement('small');
                        errorMsg.className = 'field-error';
                        errorMsg.style.color = '#dc3545';
                        errorMsg.textContent = '此字段不能为空';
                        field.parentNode.insertBefore(errorMsg, field.nextSibling);
                    }
                } else {
                    field.style.borderColor = '';
                    const errorMsg = field.nextElementSibling;
                    if (errorMsg && errorMsg.classList.contains('field-error')) {
                        errorMsg.remove();
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
            }
        });
    });

    console.log('博客系统已加载完成');
}); 