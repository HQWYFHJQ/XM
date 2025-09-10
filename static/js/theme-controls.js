/**
 * 主题控制和无障碍功能开关
 * 提供夜间/白天模式切换和无障碍功能控制
 */

class ThemeControls {
    constructor() {
        this.themeToggle = document.getElementById('theme-toggle');
        this.accessibilityToggle = document.getElementById('accessibility-toggle');
        this.themeIcon = document.getElementById('theme-icon');
        this.themeText = document.getElementById('theme-text');
        this.accessibilityIcon = document.getElementById('accessibility-icon');
        this.accessibilityText = document.getElementById('accessibility-text');
        
        this.init();
    }
    
    init() {
        // 加载保存的设置
        this.loadSettings();
        
        // 绑定事件监听器
        this.bindEvents();
        
        // 应用初始设置
        this.applySettings();
    }
    
    bindEvents() {
        // 主题切换事件
        if (this.themeToggle) {
            this.themeToggle.addEventListener('click', () => {
                this.toggleTheme();
            });
            
            this.themeToggle.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleTheme();
                }
            });
        }
        
        // 无障碍功能切换事件
        if (this.accessibilityToggle) {
            this.accessibilityToggle.addEventListener('click', () => {
                this.toggleAccessibility();
            });
            
            this.accessibilityToggle.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.toggleAccessibility();
                }
            });
        }
        
        // 监听系统主题变化
        if (window.matchMedia) {
            const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
            mediaQuery.addEventListener('change', (e) => {
                // 只有在用户没有手动设置主题时才跟随系统
                if (!localStorage.getItem('theme')) {
                    this.setTheme(e.matches ? 'dark' : 'light');
                }
            });
        }
        
        // 监听减少动画偏好变化
        if (window.matchMedia) {
            const motionQuery = window.matchMedia('(prefers-reduced-motion: reduce)');
            motionQuery.addEventListener('change', (e) => {
                this.updateAnimationSettings(e.matches);
            });
        }
    }
    
    loadSettings() {
        // 加载主题设置
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme) {
            this.currentTheme = savedTheme;
        } else {
            // 检测系统偏好
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                this.currentTheme = 'dark';
            } else {
                this.currentTheme = 'light';
            }
        }
        
        // 加载无障碍设置
        const savedAccessibility = localStorage.getItem('accessibility');
        this.accessibilityEnabled = savedAccessibility === 'enabled';
        
        // 加载动画设置
        const savedAnimation = localStorage.getItem('animation');
        if (savedAnimation) {
            this.animationEnabled = savedAnimation === 'enabled';
        } else {
            // 检测系统偏好
            if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
                this.animationEnabled = false;
            } else {
                this.animationEnabled = true;
            }
        }
    }
    
    applySettings() {
        // 应用主题
        this.setTheme(this.currentTheme);
        
        // 应用无障碍设置
        this.setAccessibility(this.accessibilityEnabled);
        
        // 应用动画设置
        this.setAnimation(this.animationEnabled);
    }
    
    toggleTheme() {
        this.currentTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(this.currentTheme);
        this.saveSettings();
        this.announceChange(`已切换到${this.currentTheme === 'dark' ? '夜间' : '白天'}模式`);
    }
    
    setTheme(theme) {
        this.currentTheme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        
        // 更新按钮状态
        if (this.themeIcon && this.themeText) {
            if (theme === 'dark') {
                this.themeIcon.className = 'fas fa-moon';
                this.themeText.textContent = '切换到白天模式';
                this.themeToggle.setAttribute('aria-label', '切换到白天模式');
                this.themeToggle.setAttribute('title', '切换到白天模式');
            } else {
                this.themeIcon.className = 'fas fa-sun';
                this.themeText.textContent = '切换到夜间模式';
                this.themeToggle.setAttribute('aria-label', '切换到夜间模式');
                this.themeToggle.setAttribute('title', '切换到夜间模式');
            }
        }
    }
    
    toggleAccessibility() {
        this.accessibilityEnabled = !this.accessibilityEnabled;
        this.setAccessibility(this.accessibilityEnabled);
        this.saveSettings();
        this.announceChange(`无障碍功能已${this.accessibilityEnabled ? '开启' : '关闭'}`);
    }
    
    setAccessibility(enabled) {
        this.accessibilityEnabled = enabled;
        
        if (enabled) {
            document.documentElement.setAttribute('data-accessibility', 'enabled');
            
            // 更新按钮状态
            if (this.accessibilityIcon && this.accessibilityText) {
                this.accessibilityIcon.className = 'fas fa-universal-access';
                this.accessibilityText.textContent = '关闭无障碍功能';
                this.accessibilityToggle.setAttribute('aria-label', '关闭无障碍功能');
                this.accessibilityToggle.setAttribute('title', '关闭无障碍功能');
                this.accessibilityToggle.classList.add('active');
            }
            
            // 启用无障碍功能
            this.enableAccessibilityFeatures();
        } else {
            document.documentElement.removeAttribute('data-accessibility');
            
            // 更新按钮状态
            if (this.accessibilityIcon && this.accessibilityText) {
                this.accessibilityIcon.className = 'fas fa-universal-access';
                this.accessibilityText.textContent = '开启无障碍功能';
                this.accessibilityToggle.setAttribute('aria-label', '开启无障碍功能');
                this.accessibilityToggle.setAttribute('title', '开启无障碍功能');
                this.accessibilityToggle.classList.remove('active');
            }
            
            // 禁用无障碍功能
            this.disableAccessibilityFeatures();
        }
    }
    
    enableAccessibilityFeatures() {
        // 显示跳过链接
        this.showSkipLinks();
        
        // 增强焦点指示器
        this.enhanceFocusIndicators();
        
        // 增加字体大小选项
        this.addFontSizeControls();
        
        // 添加朗读控制按钮
        this.addReadingControls();
        
        // 启用高对比度模式
        this.enableHighContrast();
        
        // 启用键盘导航增强
        this.enhanceKeyboardNavigation();
        
        // 启用屏幕阅读器支持
        this.enhanceScreenReaderSupport();
    }
    
    disableAccessibilityFeatures() {
        // 隐藏跳过链接
        this.hideSkipLinks();
        
        // 移除增强的焦点指示器
        this.removeEnhancedFocusIndicators();
        
        // 移除字体大小控制
        this.removeFontSizeControls();
        
        // 移除朗读控制按钮
        this.removeReadingControls();
        
        // 禁用高对比度模式
        this.disableHighContrast();
        
        // 禁用键盘导航增强
        this.disableKeyboardNavigationEnhancements();
        
        // 禁用屏幕阅读器增强
        this.disableScreenReaderEnhancements();
    }
    
    showSkipLinks() {
        // 显示跳过链接
        const skipLinks = document.getElementById('skip-links');
        if (skipLinks) {
            skipLinks.style.display = 'block';
        }
    }
    
    hideSkipLinks() {
        // 隐藏跳过链接
        const skipLinks = document.getElementById('skip-links');
        if (skipLinks) {
            skipLinks.style.display = 'none';
        }
    }
    
    enhanceFocusIndicators() {
        // 添加更强的焦点样式
        const style = document.createElement('style');
        style.id = 'accessibility-focus-styles';
        style.textContent = `
            [data-accessibility="enabled"] *:focus {
                outline: 3px solid #ff6b6b !important;
                outline-offset: 2px !important;
            }
            
            [data-accessibility="enabled"] .btn:focus {
                box-shadow: 0 0 0 0.25rem rgba(255, 107, 107, 0.5) !important;
            }
            
            [data-accessibility="enabled"] .form-control:focus {
                box-shadow: 0 0 0 0.25rem rgba(255, 107, 107, 0.5) !important;
            }
        `;
        document.head.appendChild(style);
    }
    
    removeEnhancedFocusIndicators() {
        const style = document.getElementById('accessibility-focus-styles');
        if (style) {
            style.remove();
        }
    }
    
    addFontSizeControls() {
        // 添加字体大小控制按钮
        if (!document.getElementById('font-size-controls')) {
            const controls = document.createElement('div');
            controls.id = 'font-size-controls';
            controls.className = 'font-size-controls visually-hidden';
            controls.innerHTML = `
                <button type="button" class="btn btn-sm btn-outline-secondary" id="font-decrease" aria-label="减小字体">
                    <i class="fas fa-minus" aria-hidden="true"></i>
                </button>
                <span id="font-size-indicator">100%</span>
                <button type="button" class="btn btn-sm btn-outline-secondary" id="font-increase" aria-label="增大字体">
                    <i class="fas fa-plus" aria-hidden="true"></i>
                </button>
                <button type="button" class="btn btn-sm btn-outline-secondary" id="font-reset" aria-label="重置字体大小">
                    <i class="fas fa-undo" aria-hidden="true"></i>
                </button>
            `;
            
            // 插入到控制开关区域
            const controlArea = document.querySelector('.d-flex.align-items-center.me-3');
            if (controlArea) {
                controlArea.appendChild(controls);
            }
            
            // 绑定字体大小控制事件
            this.bindFontSizeControls();
        }
        
        // 显示字体大小控制
        const controls = document.getElementById('font-size-controls');
        if (controls) {
            controls.classList.remove('visually-hidden');
        }
    }
    
    removeFontSizeControls() {
        const controls = document.getElementById('font-size-controls');
        if (controls) {
            controls.classList.add('visually-hidden');
        }
    }
    
    addReadingControls() {
        // 添加朗读控制按钮
        if (!document.getElementById('reading-controls')) {
            const controls = document.createElement('div');
            controls.id = 'reading-controls';
            controls.className = 'reading-controls visually-hidden';
            controls.innerHTML = `
                <button type="button" class="btn btn-sm btn-outline-info" id="read-page-title" aria-label="朗读页面标题">
                    <i class="fas fa-heading" aria-hidden="true"></i>
                    <span class="visually-hidden">朗读页面标题</span>
                </button>
                <button type="button" class="btn btn-sm btn-outline-info" id="read-page-content" aria-label="朗读页面内容">
                    <i class="fas fa-file-text" aria-hidden="true"></i>
                    <span class="visually-hidden">朗读页面内容</span>
                </button>
                <button type="button" class="btn btn-sm btn-outline-info" id="read-navigation" aria-label="朗读导航信息">
                    <i class="fas fa-sitemap" aria-hidden="true"></i>
                    <span class="visually-hidden">朗读导航信息</span>
                </button>
                <button type="button" class="btn btn-sm btn-outline-info" id="read-focused" aria-label="朗读当前焦点元素">
                    <i class="fas fa-eye" aria-hidden="true"></i>
                    <span class="visually-hidden">朗读当前焦点元素</span>
                </button>
            `;
            
            // 插入到控制开关区域
            const controlArea = document.querySelector('.d-flex.align-items-center.me-3');
            if (controlArea) {
                controlArea.appendChild(controls);
            }
            
            // 绑定朗读控制事件
            this.bindReadingControls();
        }
        
        // 显示朗读控制
        const controls = document.getElementById('reading-controls');
        if (controls) {
            controls.classList.remove('visually-hidden');
        }
    }
    
    removeReadingControls() {
        const controls = document.getElementById('reading-controls');
        if (controls) {
            controls.classList.add('visually-hidden');
        }
    }
    
    bindReadingControls() {
        const readPageTitle = document.getElementById('read-page-title');
        const readPageContent = document.getElementById('read-page-content');
        const readNavigation = document.getElementById('read-navigation');
        const readFocused = document.getElementById('read-focused');
        
        if (readPageTitle) {
            readPageTitle.addEventListener('click', () => {
                if (window.Accessibility) {
                    window.Accessibility.readPageTitle();
                }
            });
        }
        
        if (readPageContent) {
            readPageContent.addEventListener('click', () => {
                if (window.Accessibility) {
                    window.Accessibility.readPageContent();
                }
            });
        }
        
        if (readNavigation) {
            readNavigation.addEventListener('click', () => {
                if (window.Accessibility) {
                    window.Accessibility.readNavigationInfo();
                }
            });
        }
        
        if (readFocused) {
            readFocused.addEventListener('click', () => {
                if (window.Accessibility) {
                    window.Accessibility.readFocusedElement();
                }
            });
        }
    }
    
    bindFontSizeControls() {
        const decreaseBtn = document.getElementById('font-decrease');
        const increaseBtn = document.getElementById('font-increase');
        const resetBtn = document.getElementById('font-reset');
        const indicator = document.getElementById('font-size-indicator');
        
        if (decreaseBtn) {
            decreaseBtn.addEventListener('click', () => {
                this.adjustFontSize(-0.1);
            });
        }
        
        if (increaseBtn) {
            increaseBtn.addEventListener('click', () => {
                this.adjustFontSize(0.1);
            });
        }
        
        if (resetBtn) {
            resetBtn.addEventListener('click', () => {
                this.resetFontSize();
            });
        }
    }
    
    adjustFontSize(delta) {
        const currentSize = parseFloat(document.documentElement.style.fontSize) || 1;
        const newSize = Math.max(0.8, Math.min(1.5, currentSize + delta));
        document.documentElement.style.fontSize = newSize + 'em';
        
        const indicator = document.getElementById('font-size-indicator');
        if (indicator) {
            indicator.textContent = Math.round(newSize * 100) + '%';
        }
        
        localStorage.setItem('fontSize', newSize);
        this.announceChange(`字体大小已调整为${Math.round(newSize * 100)}%`);
    }
    
    resetFontSize() {
        document.documentElement.style.fontSize = '';
        localStorage.removeItem('fontSize');
        
        const indicator = document.getElementById('font-size-indicator');
        if (indicator) {
            indicator.textContent = '100%';
        }
        
        this.announceChange('字体大小已重置');
    }
    
    enableHighContrast() {
        // 应用高对比度样式
        document.documentElement.classList.add('high-contrast');
    }
    
    disableHighContrast() {
        // 移除高对比度样式
        document.documentElement.classList.remove('high-contrast');
    }
    
    enhanceKeyboardNavigation() {
        // 增强键盘导航功能
        document.addEventListener('keydown', this.handleKeyboardNavigation.bind(this));
    }
    
    disableKeyboardNavigationEnhancements() {
        // 移除键盘导航增强
        document.removeEventListener('keydown', this.handleKeyboardNavigation.bind(this));
    }
    
    handleKeyboardNavigation(e) {
        if (!this.accessibilityEnabled) return;
        
        // 添加键盘快捷键
        if (e.altKey) {
            switch (e.key) {
                case '1':
                    e.preventDefault();
                    document.getElementById('main-content')?.focus();
                    break;
                case '2':
                    e.preventDefault();
                    document.getElementById('navigation')?.focus();
                    break;
                case '3':
                    e.preventDefault();
                    document.getElementById('search-input')?.focus();
                    break;
                case 't':
                    e.preventDefault();
                    this.toggleTheme();
                    break;
                case 'a':
                    e.preventDefault();
                    this.toggleAccessibility();
                    break;
                case 'r':
                    e.preventDefault();
                    if (window.Accessibility) {
                        window.Accessibility.readPageContent();
                    }
                    break;
                case 'h':
                    e.preventDefault();
                    if (window.Accessibility) {
                        window.Accessibility.readPageTitle();
                    }
                    break;
                case 'n':
                    e.preventDefault();
                    if (window.Accessibility) {
                        window.Accessibility.readNavigationInfo();
                    }
                    break;
                case 'f':
                    e.preventDefault();
                    if (window.Accessibility) {
                        window.Accessibility.readFocusedElement();
                    }
                    break;
            }
        }
    }
    
    enhanceScreenReaderSupport() {
        // 增强屏幕阅读器支持
        this.announceToScreenReader('无障碍功能已启用，您现在可以使用增强的导航功能');
    }
    
    disableScreenReaderEnhancements() {
        // 禁用屏幕阅读器增强
        this.announceToScreenReader('无障碍功能已禁用');
    }
    
    setAnimation(enabled) {
        this.animationEnabled = enabled;
        
        if (enabled) {
            document.documentElement.classList.remove('no-animation');
        } else {
            document.documentElement.classList.add('no-animation');
        }
    }
    
    updateAnimationSettings(reduced) {
        this.animationEnabled = !reduced;
        this.setAnimation(this.animationEnabled);
        this.saveSettings();
    }
    
    saveSettings() {
        localStorage.setItem('theme', this.currentTheme);
        localStorage.setItem('accessibility', this.accessibilityEnabled ? 'enabled' : 'disabled');
        localStorage.setItem('animation', this.animationEnabled ? 'enabled' : 'disabled');
    }
    
    announceChange(message) {
        this.announceToScreenReader(message);
        
        // 显示视觉提示
        this.showNotification(message);
    }
    
    announceToScreenReader(message) {
        const liveRegion = document.getElementById('sr-live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }
    
    showNotification(message) {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = 'accessibility-notification';
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--primary-color);
            color: white;
            padding: 10px 20px;
            border-radius: 4px;
            z-index: 10000;
            font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        `;
        
        document.body.appendChild(notification);
        
        // 3秒后移除通知
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new ThemeControls();
});

// 导出类供其他脚本使用
window.ThemeControls = ThemeControls;
