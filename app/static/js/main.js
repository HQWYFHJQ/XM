// 校园跳蚤市场 - 主JavaScript文件

$(document).ready(function() {
    // 初始化工具提示
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // 初始化弹出框
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // 自动隐藏提示消息
    initAlertAutoHide();

    // 图片懒加载
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // 搜索建议
    initSearchSuggestions();
    
    // 商品操作
    initItemActions();
    
    // 表单验证
    initFormValidation();
    
    // 回到顶部按钮
    initBackToTop();
});

// 搜索建议功能
function initSearchSuggestions() {
    const searchInput = $('input[name="search"]');
    if (searchInput.length === 0) return;

    let searchTimeout;
    searchInput.on('input', function() {
        const query = $(this).val().trim();
        
        clearTimeout(searchTimeout);
        if (query.length < 2) {
            hideSearchSuggestions();
            return;
        }

        searchTimeout = setTimeout(() => {
            fetchSearchSuggestions(query);
        }, 300);
    });

    // 点击外部隐藏建议
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.search-suggestions').length) {
            hideSearchSuggestions();
        }
    });
}

function fetchSearchSuggestions(query) {
    $.ajax({
        url: '/api/search',
        method: 'GET',
        data: { q: query, limit: 5 },
        success: function(response) {
            if (response.success && response.data.items.length > 0) {
                showSearchSuggestions(response.data.items);
            } else {
                hideSearchSuggestions();
            }
        },
        error: function() {
            hideSearchSuggestions();
        }
    });
}

function showSearchSuggestions(items) {
    let html = '<div class="search-suggestions dropdown-menu show">';
    items.forEach(item => {
        html += `
            <a class="dropdown-item" href="/item/${item.id}">
                <div class="d-flex align-items-center">
                    ${item.main_image ? 
                        `<img src="/static/uploads/items/${item.main_image}" class="me-2" width="40" height="40" style="object-fit: cover;">` :
                        `<div class="me-2 bg-light d-flex align-items-center justify-content-center" style="width: 40px; height: 40px;"><i class="fas fa-image text-muted"></i></div>`
                    }
                    <div>
                        <div class="fw-bold">${item.title}</div>
                        <small class="text-muted">¥${item.price}</small>
                    </div>
                </div>
            </a>
        `;
    });
    html += '</div>';
    
    $('.search-suggestions').remove();
    $('input[name="search"]').after(html);
}

function hideSearchSuggestions() {
    $('.search-suggestions').remove();
}

// 商品操作功能
function initItemActions() {
    // 点赞功能
    $(document).on('click', '.like-btn', function(e) {
        e.preventDefault();
        const btn = $(this);
        const itemId = btn.data('item-id');
        const isLiked = btn.hasClass('liked');
        
        if (btn.hasClass('loading')) return;
        
        btn.addClass('loading');
        
        $.ajax({
            url: `/api/like/${itemId}`,
            method: 'POST',
            success: function(response) {
                if (response.success) {
                    btn.toggleClass('liked', response.is_liked);
                    btn.find('.like-count').text(response.like_count);
                    
                    if (response.is_liked) {
                        btn.find('i').removeClass('far').addClass('fas');
                    } else {
                        btn.find('i').removeClass('fas').addClass('far');
                    }
                }
            },
            error: function() {
                showAlert('操作失败，请重试', 'error');
            },
            complete: function() {
                btn.removeClass('loading');
            }
        });
    });

    // 联系卖家功能
    $(document).on('click', '.contact-btn', function(e) {
        e.preventDefault();
        const btn = $(this);
        const itemId = btn.data('item-id');
        
        if (btn.hasClass('loading')) return;
        
        btn.addClass('loading');
        
        $.ajax({
            url: `/api/contact/${itemId}`,
            method: 'POST',
            success: function(response) {
                if (response.success) {
                    // 如果有对话ID，跳转到聊天页面
                    if (response.conversation_id) {
                        window.location.href = `/messages/${response.conversation_id}`;
                    } else {
                        // 否则显示联系信息模态框
                        showContactModal({
                            contact_info: response.contact_info,
                            contact_method: response.contact_method
                        });
                    }
                } else {
                    showAlert(response.message, 'error');
                }
            },
            error: function() {
                showAlert('操作失败，请重试', 'error');
            },
            complete: function() {
                btn.removeClass('loading');
            }
        });
    });
}

// 显示联系模态框
function showContactModal(data) {
    let modalHtml = `
        <div class="modal fade" id="contactModal" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">联系卖家</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <p>联系方式：${data.contact_method}</p>
                        <p>联系信息：${data.contact_info || '暂无'}</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    $('#contactModal').remove();
    $('body').append(modalHtml);
    $('#contactModal').modal('show');
}

// 表单验证
function initFormValidation() {
    // 密码确认验证
    $('#confirm_password').on('input', function() {
        const password = $('#password').val();
        const confirmPassword = $(this).val();
        
        if (password !== confirmPassword) {
            $(this).addClass('is-invalid');
            if (!$(this).next('.invalid-feedback').length) {
                $(this).after('<div class="invalid-feedback">两次输入的密码不一致</div>');
            }
        } else {
            $(this).removeClass('is-invalid').addClass('is-valid');
        }
    });

    // 实时验证
    $('input[required]').on('blur', function() {
        const input = $(this);
        if (input.val().trim() === '') {
            input.addClass('is-invalid');
        } else {
            input.removeClass('is-invalid').addClass('is-valid');
        }
    });
}

// 显示提示消息
function showAlert(message, type = 'info') {
    const alertClass = type === 'error' ? 'alert-danger' : `alert-${type}`;
    const alertId = 'alert-' + Date.now() + '-' + Math.random().toString(36).substr(2, 9);
    const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show" role="alert" id="${alertId}">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    $('.container').first().prepend(alertHtml);
    
    // 使用新的alert管理逻辑
    const alert = $(`#${alertId}`);
    alert.data('auto-hide-set', true);
    setTimeout(() => {
        if (alert.is(':visible')) {
            alert.fadeOut('slow', function() {
                $(this).remove();
            });
        }
    }, 5000);
}

// 加载更多功能
function loadMore(url, container, callback) {
    const btn = $('.load-more-btn');
    const originalText = btn.html();
    
    btn.html('<span class="loading"></span> 加载中...');
    btn.prop('disabled', true);
    
    $.ajax({
        url: url,
        method: 'GET',
        success: function(response) {
            if (response.success) {
                callback(response.data);
            } else {
                showAlert('加载失败，请重试', 'error');
            }
        },
        error: function() {
            showAlert('网络错误，请重试', 'error');
        },
        complete: function() {
            btn.html(originalText);
            btn.prop('disabled', false);
        }
    });
}

// 图片预览功能
function initImagePreview() {
    $(document).on('click', '.item-image', function() {
        const src = $(this).attr('src');
        const title = $(this).attr('alt');
        
        const modalHtml = `
            <div class="modal fade" id="imageModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body text-center">
                            <img src="${src}" class="img-fluid" alt="${title}">
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        $('#imageModal').remove();
        $('body').append(modalHtml);
        $('#imageModal').modal('show');
    });
}

// 初始化图片预览
initImagePreview();

// 工具函数
const utils = {
    // 格式化价格
    formatPrice: function(price) {
        return '¥' + parseFloat(price).toFixed(2);
    },
    
    // 格式化时间（北京时间）
    formatTime: function(time) {
        const date = new Date(time);
        const now = new Date();
        
        // 转换为北京时间（UTC+8）
        const beijingDate = new Date(date.getTime() + 8 * 60 * 60 * 1000);
        const beijingNow = new Date(now.getTime() + 8 * 60 * 60 * 1000);
        
        const diff = beijingNow - beijingDate;
        
        if (diff < 60000) { // 1分钟内
            return '刚刚';
        } else if (diff < 3600000) { // 1小时内
            return Math.floor(diff / 60000) + '分钟前';
        } else if (diff < 86400000) { // 1天内
            return Math.floor(diff / 3600000) + '小时前';
        } else if (diff < 2592000000) { // 30天内
            return Math.floor(diff / 86400000) + '天前';
        } else {
            return beijingDate.toLocaleDateString('zh-CN');
        }
    },
    
    // 格式化北京时间
    formatBeijingTime: function(time, format = 'YYYY-MM-DD HH:mm:ss') {
        const date = new Date(time);
        const beijingDate = new Date(date.getTime() + 8 * 60 * 60 * 1000);
        
        const year = beijingDate.getFullYear();
        const month = String(beijingDate.getMonth() + 1).padStart(2, '0');
        const day = String(beijingDate.getDate()).padStart(2, '0');
        const hours = String(beijingDate.getHours()).padStart(2, '0');
        const minutes = String(beijingDate.getMinutes()).padStart(2, '0');
        const seconds = String(beijingDate.getSeconds()).padStart(2, '0');
        
        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes)
            .replace('ss', seconds);
    },
    
    // 截断文本
    truncateText: function(text, length = 100) {
        if (text.length <= length) return text;
        return text.substring(0, length) + '...';
    }
};

// Alert管理功能
function initAlertAutoHide() {
    // 为每个现有的alert设置自动隐藏（排除公告）
    $('.alert:not(.alert-permanent):not(.announcement-item)').each(function() {
        const alert = $(this);
        if (!alert.data('auto-hide-set')) {
            alert.data('auto-hide-set', true);
            setTimeout(() => {
                if (alert.is(':visible')) {
                    alert.fadeOut('slow', function() {
                        $(this).remove();
                    });
                }
            }, 5000);
        }
    });
    
    // 监听新添加的alert
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1 && $(node).hasClass('alert')) {
                    const alert = $(node);
                    // 排除公告元素和永久alert
                    if (!alert.hasClass('alert-permanent') && !alert.hasClass('announcement-item') && !alert.data('auto-hide-set')) {
                        alert.data('auto-hide-set', true);
                        setTimeout(() => {
                            if (alert.is(':visible')) {
                                alert.fadeOut('slow', function() {
                                    $(this).remove();
                                });
                            }
                        }, 5000);
                    }
                }
            });
        });
    });
    
    // 观察body元素的变化
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
}

// 手动隐藏所有alert（排除公告）
function hideAllAlerts() {
    $('.alert:not(.announcement-item)').fadeOut('slow', function() {
        $(this).remove();
    });
}

// 回到顶部按钮功能 - 超高性能版本
function initBackToTop() {
    const backToTopBtn = $('#backToTop');
    
    if (backToTopBtn.length === 0) return;
    
    let isAnimating = false;
    let rafId = null;
    
    // 使用requestAnimationFrame的节流函数
    let ticking = false;
    function requestTick() {
        if (!ticking) {
            requestAnimationFrame(updateButtonVisibility);
            ticking = true;
        }
    }
    
    // 更新按钮可见性
    function updateButtonVisibility() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 300) {
            if (!backToTopBtn.hasClass('show')) {
                backToTopBtn.addClass('show');
            }
        } else {
            if (backToTopBtn.hasClass('show')) {
                backToTopBtn.removeClass('show');
            }
        }
        
        ticking = false;
    }
    
    // 使用passive listener提高性能
    window.addEventListener('scroll', requestTick, { passive: true });
    
    // 超流畅的回到顶部动画
    function scrollToTop() {
        if (isAnimating) return;
        
        isAnimating = true;
        backToTopBtn.removeClass('show');
        
        const startTime = performance.now();
        const startScrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const duration = 500; // 更快的动画
        
        function animateScroll(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // 使用更平滑的缓动函数
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const currentScrollTop = startScrollTop * (1 - easeOutQuart);
            
            window.scrollTo(0, currentScrollTop);
            
            if (progress < 1) {
                rafId = requestAnimationFrame(animateScroll);
            } else {
                isAnimating = false;
                rafId = null;
            }
        }
        
        rafId = requestAnimationFrame(animateScroll);
    }
    
    // 点击事件处理
    backToTopBtn.on('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        scrollToTop();
    });
    
    // 键盘支持
    $(document).on('keydown', function(e) {
        if (e.key === 'Home' && e.ctrlKey) {
            e.preventDefault();
            scrollToTop();
        }
    });
    
    // 触摸设备优化
    let touchStartTime = 0;
    backToTopBtn.on('touchstart', function(e) {
        touchStartTime = performance.now();
    }, { passive: true });
    
    backToTopBtn.on('touchend', function(e) {
        const touchDuration = performance.now() - touchStartTime;
        if (touchDuration < 500) { // 短按
            e.preventDefault();
            scrollToTop();
        }
    });
    
    // 清理函数
    return function() {
        if (rafId) {
            cancelAnimationFrame(rafId);
        }
        window.removeEventListener('scroll', requestTick);
    };
}

// 导出工具函数
window.utils = utils;
window.hideAllAlerts = hideAllAlerts;
