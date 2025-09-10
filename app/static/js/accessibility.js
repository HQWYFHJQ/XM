/**
 * 无障碍支持JavaScript文件
 * 提供键盘导航、焦点管理、屏幕阅读器支持等功能
 */

(function() {
    'use strict';

    // 无障碍支持对象
    const Accessibility = {
        // 初始化
        init: function() {
            this.setupKeyboardNavigation();
            this.setupFocusManagement();
            this.setupSkipLinks();
            this.setupFormValidation();
            this.setupLiveRegions();
            this.setupCarouselAccessibility();
            this.setupModalAccessibility();
            this.setupAutoReading();
            this.setupContentReading();
        },

        // 键盘导航支持
        setupKeyboardNavigation: function() {
            // 为所有可聚焦元素添加键盘事件监听
            document.addEventListener('keydown', function(e) {
                // ESC键关闭模态框和下拉菜单
                if (e.key === 'Escape') {
                    const openModal = document.querySelector('.modal.show');
                    if (openModal) {
                        const modal = bootstrap.Modal.getInstance(openModal);
                        if (modal) modal.hide();
                    }

                    const openDropdown = document.querySelector('.dropdown-menu.show');
                    if (openDropdown) {
                        const dropdown = bootstrap.Dropdown.getInstance(openDropdown.previousElementSibling);
                        if (dropdown) dropdown.hide();
                    }
                }

                // 箭头键导航支持
                if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
                    const focusedElement = document.activeElement;
                    const isInDropdown = focusedElement.closest('.dropdown-menu');
                    
                    if (isInDropdown) {
                        e.preventDefault();
                        const items = Array.from(isInDropdown.querySelectorAll('.dropdown-item'));
                        const currentIndex = items.indexOf(focusedElement);
                        
                        if (e.key === 'ArrowDown') {
                            const nextIndex = (currentIndex + 1) % items.length;
                            items[nextIndex].focus();
                        } else {
                            const prevIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
                            items[prevIndex].focus();
                        }
                    }
                }
            });

            // 为卡片链接添加键盘支持
            document.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    const card = e.target.closest('.card');
                    if (card && !e.target.matches('a, button, input, select, textarea')) {
                        e.preventDefault();
                        const cardLink = card.querySelector('.card a, .card button');
                        if (cardLink) {
                            if (cardLink.tagName === 'A') {
                                window.location.href = cardLink.href;
                            } else {
                                cardLink.click();
                            }
                        }
                    }
                }
            });
        },

        // 焦点管理
        setupFocusManagement: function() {
            // 模态框焦点管理
            document.addEventListener('shown.bs.modal', function(e) {
                const modal = e.target;
                const focusableElements = modal.querySelectorAll(
                    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
                );
                if (focusableElements.length > 0) {
                    focusableElements[0].focus();
                }
            });

            // 下拉菜单焦点管理
            document.addEventListener('shown.bs.dropdown', function(e) {
                const dropdown = e.target;
                const menu = dropdown.querySelector('.dropdown-menu');
                if (menu) {
                    const firstItem = menu.querySelector('.dropdown-item');
                    if (firstItem) {
                        firstItem.focus();
                    }
                }
            });

            // 轮播图焦点管理
            document.addEventListener('slide.bs.carousel', function(e) {
                const carousel = e.target;
                const activeSlide = carousel.querySelector('.carousel-item.active');
                if (activeSlide) {
                    const focusableElements = activeSlide.querySelectorAll(
                        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
                    );
                    if (focusableElements.length > 0) {
                        focusableElements[0].focus();
                    }
                }
            });
        },

        // 跳过链接支持
        setupSkipLinks: function() {
            const skipLinks = document.querySelectorAll('.skip-link');
            skipLinks.forEach(link => {
                link.addEventListener('click', function(e) {
                    e.preventDefault();
                    const target = document.querySelector(this.getAttribute('href'));
                    if (target) {
                        target.focus();
                        target.scrollIntoView({ behavior: 'smooth' });
                    }
                });
            });
        },

        // 表单验证支持
        setupFormValidation: function() {
            const forms = document.querySelectorAll('form[novalidate]');
            forms.forEach(form => {
                form.addEventListener('submit', function(e) {
                    if (!form.checkValidity()) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        // 聚焦到第一个无效字段
                        const firstInvalid = form.querySelector(':invalid');
                        if (firstInvalid) {
                            firstInvalid.focus();
                            this.announceToScreenReader('请检查表单中的错误信息');
                        }
                    }
                    form.classList.add('was-validated');
                });
            });

            // 实时验证
            const inputs = document.querySelectorAll('input, select, textarea');
            inputs.forEach(input => {
                input.addEventListener('blur', function() {
                    this.checkValidity();
                });
            });
        },

        // 实时区域支持
        setupLiveRegions: function() {
            // 创建屏幕阅读器通知区域
            if (!document.getElementById('sr-live-region')) {
                const liveRegion = document.createElement('div');
                liveRegion.id = 'sr-live-region';
                liveRegion.setAttribute('aria-live', 'polite');
                liveRegion.setAttribute('aria-atomic', 'true');
                liveRegion.className = 'visually-hidden';
                document.body.appendChild(liveRegion);
            }
        },

        // 轮播图无障碍支持
        setupCarouselAccessibility: function() {
            const carousels = document.querySelectorAll('.carousel');
            carousels.forEach(carousel => {
                // 暂停自动播放当用户与轮播图交互时
                carousel.addEventListener('mouseenter', function() {
                    const bsCarousel = bootstrap.Carousel.getInstance(this);
                    if (bsCarousel) {
                        bsCarousel.pause();
                    }
                });

                carousel.addEventListener('mouseleave', function() {
                    const bsCarousel = bootstrap.Carousel.getInstance(this);
                    if (bsCarousel) {
                        bsCarousel.cycle();
                    }
                });

                // 键盘控制
                carousel.addEventListener('keydown', function(e) {
                    const bsCarousel = bootstrap.Carousel.getInstance(this);
                    if (!bsCarousel) return;

                    switch(e.key) {
                        case 'ArrowLeft':
                            e.preventDefault();
                            bsCarousel.prev();
                            break;
                        case 'ArrowRight':
                            e.preventDefault();
                            bsCarousel.next();
                            break;
                        case 'Home':
                            e.preventDefault();
                            bsCarousel.to(0);
                            break;
                        case 'End':
                            e.preventDefault();
                            const totalSlides = this.querySelectorAll('.carousel-item').length;
                            bsCarousel.to(totalSlides - 1);
                            break;
                    }
                });
            });
        },

        // 模态框无障碍支持
        setupModalAccessibility: function() {
            document.addEventListener('shown.bs.modal', function(e) {
                const modal = e.target;
                modal.setAttribute('aria-hidden', 'false');
                
                // 设置焦点陷阱
                const focusableElements = modal.querySelectorAll(
                    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
                );
                
                if (focusableElements.length > 0) {
                    const firstElement = focusableElements[0];
                    const lastElement = focusableElements[focusableElements.length - 1];
                    
                    modal.addEventListener('keydown', function(e) {
                        if (e.key === 'Tab') {
                            if (e.shiftKey) {
                                if (document.activeElement === firstElement) {
                                    e.preventDefault();
                                    lastElement.focus();
                                }
                            } else {
                                if (document.activeElement === lastElement) {
                                    e.preventDefault();
                                    firstElement.focus();
                                }
                            }
                        }
                    });
                }
            });

            document.addEventListener('hidden.bs.modal', function(e) {
                const modal = e.target;
                modal.setAttribute('aria-hidden', 'true');
            });
        },

        // 屏幕阅读器通知
        announceToScreenReader: function(message, priority = 'polite') {
            const liveRegion = document.getElementById(priority === 'assertive' ? 'sr-status-region' : 'sr-live-region');
            if (liveRegion) {
                liveRegion.textContent = message;
                setTimeout(() => {
                    liveRegion.textContent = '';
                }, 1000);
            }
        },

        // 朗读页面内容
        readPageContent: function() {
            const mainContent = document.getElementById('main-content') || document.querySelector('main');
            if (mainContent) {
                const textContent = this.extractTextContent(mainContent);
                this.announceToScreenReader(`页面内容：${textContent}`, 'assertive');
            }
        },

        // 朗读当前焦点元素
        readFocusedElement: function() {
            const focusedElement = document.activeElement;
            if (focusedElement && focusedElement !== document.body) {
                const text = this.getElementDescription(focusedElement);
                this.announceToScreenReader(text, 'assertive');
            }
        },

        // 朗读页面标题
        readPageTitle: function() {
            const title = document.title;
            const h1 = document.querySelector('h1');
            const pageTitle = h1 ? h1.textContent : title;
            this.announceToScreenReader(`页面标题：${pageTitle}`, 'assertive');
        },

        // 朗读导航信息
        readNavigationInfo: function() {
            const navItems = document.querySelectorAll('.navbar-nav .nav-link');
            const navText = Array.from(navItems).map(item => item.textContent.trim()).join('，');
            this.announceToScreenReader(`导航菜单包含：${navText}`, 'polite');
        },

        // 朗读表单信息
        readFormInfo: function(form) {
            const labels = form.querySelectorAll('label');
            const inputs = form.querySelectorAll('input, select, textarea');
            let formInfo = '表单包含以下字段：';
            
            inputs.forEach((input, index) => {
                const label = labels[index] || input.getAttribute('aria-label') || input.placeholder || '未标记字段';
                const type = input.type || input.tagName.toLowerCase();
                formInfo += `${label}（${type}），`;
            });
            
            this.announceToScreenReader(formInfo, 'polite');
        },

        // 朗读商品信息
        readItemInfo: function(itemElement) {
            const title = itemElement.querySelector('.card-title, h3, h4, h5')?.textContent || '未知商品';
            const price = itemElement.querySelector('.price, .text-primary')?.textContent || '价格未知';
            const description = itemElement.querySelector('.card-text, p')?.textContent || '';
            const location = itemElement.querySelector('.location, .text-muted')?.textContent || '';
            
            let itemInfo = `商品：${title}，价格：${price}`;
            if (description) itemInfo += `，描述：${description.substring(0, 100)}`;
            if (location) itemInfo += `，位置：${location}`;
            
            this.announceToScreenReader(itemInfo, 'polite');
        },

        // 提取文本内容
        extractTextContent: function(element) {
            // 移除脚本和样式元素
            const clone = element.cloneNode(true);
            const scripts = clone.querySelectorAll('script, style');
            scripts.forEach(script => script.remove());
            
            // 获取纯文本内容
            let text = clone.textContent || clone.innerText || '';
            
            // 清理文本
            text = text.replace(/\s+/g, ' ').trim();
            
            // 限制长度
            if (text.length > 500) {
                text = text.substring(0, 500) + '...';
            }
            
            return text;
        },

        // 获取元素描述
        getElementDescription: function(element) {
            let description = '';
            
            // 获取标签名
            const tagName = element.tagName.toLowerCase();
            
            // 获取文本内容
            const text = element.textContent?.trim() || '';
            
            // 获取aria-label
            const ariaLabel = element.getAttribute('aria-label');
            
            // 获取title属性
            const title = element.getAttribute('title');
            
            // 获取alt属性（图片）
            const alt = element.getAttribute('alt');
            
            // 构建描述
            if (ariaLabel) {
                description = ariaLabel;
            } else if (title) {
                description = title;
            } else if (alt) {
                description = alt;
            } else if (text) {
                description = text;
            } else {
                description = `${tagName}元素`;
            }
            
            // 添加元素类型信息
            if (element.type) {
                description += `（${element.type}）`;
            } else if (tagName === 'button') {
                description += '（按钮）';
            } else if (tagName === 'a') {
                description += '（链接）';
            } else if (tagName === 'input') {
                description += '（输入框）';
            }
            
            return description;
        },

        // 朗读搜索结果
        readSearchResults: function() {
            const results = document.querySelectorAll('.card, .item-card, .product-item');
            if (results.length > 0) {
                this.announceToScreenReader(`找到${results.length}个搜索结果`, 'polite');
            } else {
                this.announceToScreenReader('未找到搜索结果', 'polite');
            }
        },

        // 朗读页面状态
        readPageStatus: function() {
            const breadcrumb = document.querySelector('.breadcrumb');
            const pageTitle = document.querySelector('h1');
            const status = document.querySelector('.alert');
            
            let statusInfo = '';
            
            if (breadcrumb) {
                const breadcrumbText = breadcrumb.textContent.trim();
                statusInfo += `当前位置：${breadcrumbText}。`;
            }
            
            if (pageTitle) {
                statusInfo += `页面标题：${pageTitle.textContent.trim()}。`;
            }
            
            if (status) {
                statusInfo += `状态信息：${status.textContent.trim()}。`;
            }
            
            if (statusInfo) {
                this.announceToScreenReader(statusInfo, 'assertive');
            }
        },

        // 高对比度模式检测
        detectHighContrast: function() {
            if (window.matchMedia && window.matchMedia('(prefers-contrast: high)').matches) {
                document.body.classList.add('high-contrast');
            }
        },

        // 减少动画偏好检测
        detectReducedMotion: function() {
            if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                document.body.classList.add('reduced-motion');
            }
        },

        // 设置自动朗读功能
        setupAutoReading: function() {
            // 页面加载完成后自动朗读页面标题和状态
            setTimeout(() => {
                this.readPageStatus();
            }, 1000);

            // 监听页面变化
            const observer = new MutationObserver((mutations) => {
                mutations.forEach((mutation) => {
                    if (mutation.type === 'childList' && mutation.addedNodes.length > 0) {
                        // 检查是否有新的重要内容
                        const hasNewContent = Array.from(mutation.addedNodes).some(node => {
                            return node.nodeType === 1 && (
                                node.classList?.contains('alert') ||
                                node.classList?.contains('card') ||
                                node.tagName === 'H1' ||
                                node.tagName === 'H2'
                            );
                        });
                        
                        if (hasNewContent) {
                            setTimeout(() => {
                                this.readPageStatus();
                            }, 500);
                        }
                    }
                });
            });

            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        },

        // 设置内容朗读功能
        setupContentReading: function() {
            // 为商品卡片添加朗读功能
            document.addEventListener('click', (e) => {
                const card = e.target.closest('.card, .item-card, .product-item');
                if (card) {
                    this.readItemInfo(card);
                }
            });

            // 为表单添加朗读功能
            document.addEventListener('focusin', (e) => {
                const form = e.target.closest('form');
                if (form && !form.hasAttribute('data-read')) {
                    form.setAttribute('data-read', 'true');
                    this.readFormInfo(form);
                }
            });

            // 为搜索结果添加朗读功能
            const searchForm = document.querySelector('form[role="search"]');
            if (searchForm) {
                searchForm.addEventListener('submit', () => {
                    setTimeout(() => {
                        this.readSearchResults();
                    }, 1000);
                });
            }

            // 为导航链接添加朗读功能
            document.addEventListener('focusin', (e) => {
                if (e.target.classList.contains('nav-link')) {
                    const navText = e.target.textContent.trim();
                    this.announceToScreenReader(`导航到：${navText}`, 'polite');
                }
            });
        }
    };

    // 页面加载完成后初始化
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            Accessibility.init();
        });
    } else {
        Accessibility.init();
    }

    // 监听媒体查询变化
    if (window.matchMedia) {
        window.matchMedia('(prefers-contrast: high)').addEventListener('change', function() {
            if (this.matches) {
                document.body.classList.add('high-contrast');
            } else {
                document.body.classList.remove('high-contrast');
            }
        });

        window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', function() {
            if (this.matches) {
                document.body.classList.add('reduced-motion');
            } else {
                document.body.classList.remove('reduced-motion');
            }
        });
    }

    // 将无障碍支持对象暴露到全局
    window.Accessibility = Accessibility;

})();
