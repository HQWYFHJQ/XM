// 悬浮聊天窗口JavaScript

class FloatingChat {
    constructor() {
        this.isOpen = false;
        this.isMinimized = false;
        this.currentConversationId = null;
        this.conversations = [];
        this.messages = [];
        this.unreadCount = 0;
        this.refreshInterval = null;
        this.lastMessageSentAt = 0; // 记录最后发送消息的时间
        
        this.init();
    }
    
    init() {
        this.createElements();
        this.bindEvents();
        this.loadConversations();
        this.startAutoRefresh();
    }
    
    createElements() {
        // 创建悬浮按钮
        this.toggleBtn = document.createElement('button');
        this.toggleBtn.className = 'chat-toggle-btn';
        this.toggleBtn.innerHTML = '<i class="fas fa-comments"></i>';
        this.toggleBtn.title = '打开聊天';
        document.body.appendChild(this.toggleBtn);
        
        // 创建聊天窗口
        this.chatWindow = document.createElement('div');
        this.chatWindow.className = 'floating-chat';
        this.chatWindow.innerHTML = `
            <div class="chat-header" onclick="floatingChat.toggleMinimize()">
                <h6>我的消息</h6>
                <div class="chat-controls">
                    <button class="btn" onclick="floatingChat.refreshConversations()" title="刷新">
                        <i class="fas fa-sync-alt"></i>
                    </button>
                    <button class="btn" onclick="floatingChat.toggleChat()" title="最小化">
                        <i class="fas fa-minus"></i>
                    </button>
                </div>
            </div>
            <div class="chat-content">
                <div class="conversations-list" id="conversationsList">
                    <div class="empty-state">
                        <i class="fas fa-comments"></i>
                        <h6>暂无对话</h6>
                        <p>开始与卖家聊天吧！</p>
                    </div>
                </div>
                <div class="chat-input-area" style="display: none;">
                    <div class="chat-input-group">
                        <input type="text" class="chat-input" id="chatMessageInput" placeholder="输入消息...">
                        <button class="chat-send-btn" id="chatSendBtn">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        document.body.appendChild(this.chatWindow);
    }
    
    bindEvents() {
        // 切换聊天窗口
        this.toggleBtn.addEventListener('click', () => this.toggleChat());
        
        // 发送消息
        const sendBtn = this.chatWindow.querySelector('#chatSendBtn');
        const messageInput = this.chatWindow.querySelector('#chatMessageInput');
        
        sendBtn.addEventListener('click', () => this.sendMessage());
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // 点击外部关闭
        document.addEventListener('click', (e) => {
            if (this.isOpen && !this.chatWindow.contains(e.target) && !this.toggleBtn.contains(e.target)) {
                this.closeChat();
            }
        });
    }
    
    toggleChat() {
        if (this.isOpen) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }
    
    openChat() {
        this.isOpen = true;
        this.isMinimized = false;
        this.chatWindow.classList.add('show');
        this.toggleBtn.style.display = 'none';
        this.loadConversations();
    }
    
    closeChat() {
        this.isOpen = false;
        this.isMinimized = false;
        this.chatWindow.classList.remove('show');
        this.toggleBtn.style.display = 'flex';
        this.hideMessages();
    }
    
    toggleMinimize() {
        if (this.isMinimized) {
            this.expandChat();
        } else {
            this.minimizeChat();
        }
    }
    
    minimizeChat() {
        this.isMinimized = true;
        this.chatWindow.classList.add('minimized');
        this.hideMessages();
    }
    
    expandChat() {
        this.isMinimized = false;
        this.chatWindow.classList.remove('minimized');
        this.showConversations();
    }
    
    async loadConversations() {
        try {
            console.log('加载对话列表...');
            const response = await fetch('/api/messages/conversations');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            console.log('对话API响应:', data);
            
            if (data.success) {
                this.conversations = data.conversations || [];
                this.unreadCount = this.conversations.reduce((sum, conv) => sum + (conv.unread_count || 0), 0);
                console.log('对话数据:', this.conversations);
                console.log('未读消息总数:', this.unreadCount);
                this.updateConversationsList();
                this.updateUnreadBadge();
            } else {
                console.error('API返回失败:', data.error || '未知错误');
            }
        } catch (error) {
            console.error('加载对话失败:', error);
        }
    }
    
    updateConversationsList() {
        const container = this.chatWindow.querySelector('#conversationsList');
        console.log('更新对话列表，对话数量:', this.conversations.length);
        console.log('容器元素:', container);
        
        if (this.conversations.length === 0) {
            console.log('没有对话，显示空状态');
            container.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-comments"></i>
                    <h6>暂无对话</h6>
                    <p>开始与卖家聊天吧！</p>
                </div>
            `;
            return;
        }
        
        const conversationsHtml = this.conversations.map(conv => {
            const lastMessage = conv.last_message;
            const isUnread = conv.unread_count > 0;
            
            return `
                <div class="conversation-item ${isUnread ? 'unread' : ''}" 
                     onclick="floatingChat.openConversation(${conv.id})">
                    <div class="conversation-avatar">
                        ${conv.other_participant.avatar ? 
                            `<img src="/static/uploads/avatars/${conv.other_participant.avatar}" alt="头像">` :
                            '<i class="fas fa-user"></i>'
                        }
                    </div>
                    <div class="conversation-info">
                        <div class="conversation-name">${conv.other_participant.username}</div>
                        <div class="conversation-preview">
                            ${lastMessage ? lastMessage.content.substring(0, 30) + '...' : '暂无消息'}
                        </div>
                    </div>
                    <div class="conversation-meta">
                        <div class="conversation-time">
                            ${lastMessage ? this.formatTime(lastMessage.created_at) : ''}
                        </div>
                        ${isUnread ? `<div class="unread-badge">${conv.unread_count}</div>` : ''}
                    </div>
                </div>
            `;
        }).join('');
        
        container.innerHTML = conversationsHtml;
    }
    
    async openConversation(conversationId) {
        this.currentConversationId = conversationId;
        this.showMessages();
        await this.loadMessages(conversationId);
    }
    
    showMessages() {
        const chatContent = this.chatWindow.querySelector('.chat-content');
        const conversationsList = this.chatWindow.querySelector('.conversations-list');
        const chatInputArea = this.chatWindow.querySelector('.chat-input-area');
        
        conversationsList.style.display = 'none';
        chatInputArea.style.display = 'block';
        
        // 更新头部显示
        const header = this.chatWindow.querySelector('.chat-header h6');
        header.innerHTML = '发送消息';
        
        // 添加返回按钮
        const controls = this.chatWindow.querySelector('.chat-controls');
        if (!controls.querySelector('.back-btn')) {
            const backBtn = document.createElement('button');
            backBtn.className = 'btn back-btn';
            backBtn.innerHTML = '<i class="fas fa-arrow-left"></i>';
            backBtn.title = '返回对话列表';
            backBtn.onclick = () => this.showConversations();
            controls.insertBefore(backBtn, controls.firstChild);
        }
    }
    
    showConversations() {
        const chatContent = this.chatWindow.querySelector('.chat-content');
        const conversationsList = this.chatWindow.querySelector('.conversations-list');
        const chatInputArea = this.chatWindow.querySelector('.chat-input-area');
        
        conversationsList.style.display = 'block';
        chatInputArea.style.display = 'none';
        
        // 更新头部显示
        const header = this.chatWindow.querySelector('.chat-header h6');
        header.innerHTML = '我的消息';
        
        // 移除返回按钮
        const backBtn = this.chatWindow.querySelector('.back-btn');
        if (backBtn) {
            backBtn.remove();
        }
        
        this.currentConversationId = null;
    }
    
    async loadMessages(conversationId) {
        try {
            console.log('加载消息，对话ID:', conversationId);
            const response = await fetch(`/api/messages/${conversationId}/messages`);
            const data = await response.json();
            
            console.log('消息API响应:', data);
            
            if (data.success) {
                this.messages = data.messages;
                console.log('设置消息数据:', this.messages);
                this.displayMessages();
                this.markAsRead(conversationId);
            }
        } catch (error) {
            console.error('加载消息失败:', error);
        }
    }
    
    displayMessages() {
        console.log('显示消息，消息数量:', this.messages.length);
        const chatContent = this.chatWindow.querySelector('.chat-content');
        
        // 创建消息列表容器
        let messagesContainer = chatContent.querySelector('.messages-list');
        if (!messagesContainer) {
            messagesContainer = document.createElement('div');
            messagesContainer.className = 'messages-list';
            chatContent.insertBefore(messagesContainer, chatContent.querySelector('.chat-input-area'));
        }
        
        if (this.messages.length === 0) {
            console.log('没有消息，显示空状态');
            messagesContainer.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-comment"></i>
                    <h6>开始对话</h6>
                    <p>发送第一条消息开始聊天吧！</p>
                </div>
            `;
            return;
        }
        
        const messagesHtml = this.messages.map(msg => {
            const isSent = msg.sender_id === window.currentUserId;
            const messageClass = isSent ? 'sent' : 'received';
            
            return `
                <div class="message-item ${messageClass}">
                    <div class="message-bubble">
                        <div>${msg.content}</div>
                        <div class="message-time">
                            ${this.formatTime(msg.created_at)}
                            ${isSent ? '<span class="message-status"><i class="fas fa-check"></i></span>' : ''}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        
        messagesContainer.innerHTML = messagesHtml;
        this.scrollToBottom();
    }
    
    async sendMessage() {
        const input = this.chatWindow.querySelector('#chatMessageInput');
        const content = input.value.trim();
        
        if (!content || !this.currentConversationId) return;
        
        const sendBtn = this.chatWindow.querySelector('#chatSendBtn');
        const originalHtml = sendBtn.innerHTML;
        
        // 显示发送状态
        sendBtn.innerHTML = '<div class="loading-spinner"></div>';
        sendBtn.disabled = true;
        
        try {
            const response = await fetch('/api/messages/send', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    conversation_id: this.currentConversationId,
                    content: content,
                    message_type: 'text'
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                input.value = '';
                this.messages.push(data.message);
                this.displayMessages();
                this.lastMessageSentAt = Date.now(); // 记录发送时间
                // 不立即刷新对话列表，让自动刷新机制处理
                // this.loadConversations(); // 刷新对话列表
            } else {
                this.showAlert(data.error, 'error');
            }
        } catch (error) {
            console.error('发送消息失败:', error);
            this.showAlert('发送失败，请重试', 'error');
        } finally {
            sendBtn.innerHTML = originalHtml;
            sendBtn.disabled = false;
        }
    }
    
    async markAsRead(conversationId) {
        try {
            await fetch(`/api/messages/${conversationId}/read`, {
                method: 'POST'
            });
        } catch (error) {
            console.error('标记已读失败:', error);
        }
    }
    
    async refreshConversations() {
        const refreshBtn = this.chatWindow.querySelector('.chat-controls .btn');
        const originalHtml = refreshBtn.innerHTML;
        
        refreshBtn.innerHTML = '<div class="loading-spinner"></div>';
        
        await this.loadConversations();
        
        refreshBtn.innerHTML = originalHtml;
    }
    
    updateUnreadBadge() {
        if (this.unreadCount > 0) {
            if (!this.toggleBtn.querySelector('.notification-badge')) {
                const badge = document.createElement('div');
                badge.className = 'notification-badge';
                this.toggleBtn.appendChild(badge);
            }
            this.toggleBtn.querySelector('.notification-badge').textContent = this.unreadCount;
        } else {
            const badge = this.toggleBtn.querySelector('.notification-badge');
            if (badge) {
                badge.remove();
            }
        }
    }
    
    startAutoRefresh() {
        // 每5秒刷新一次对话列表和当前对话的消息
        this.refreshInterval = setInterval(() => {
            if (this.isOpen) {
                this.loadConversations();
                // 如果当前有打开的对话，也刷新消息
                // 但避免在刚发送消息后立即重新加载（10秒内）
                if (this.currentConversationId) {
                    const timeSinceLastMessage = Date.now() - this.lastMessageSentAt;
                    if (timeSinceLastMessage > 10000) { // 10秒后才重新加载消息
                        this.loadMessages(this.currentConversationId);
                    }
                }
            }
        }, 5000);
    }
    
    scrollToBottom() {
        const messagesContainer = this.chatWindow.querySelector('.messages-list');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }
    
    formatTime(timeString) {
        const date = new Date(timeString);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) { // 1分钟内
            return '刚刚';
        } else if (diff < 3600000) { // 1小时内
            const minutes = Math.floor(diff / 60000);
            return `${minutes}分钟前`;
        } else if (diff < 86400000) { // 1天内
            const hours = Math.floor(diff / 3600000);
            return `${hours}小时前`;
        } else {
            return date.toLocaleDateString('zh-CN');
        }
    }
    
    showAlert(message, type = 'info') {
        // 简单的提示实现
        const alert = document.createElement('div');
        alert.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
        alert.style.position = 'fixed';
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '9999';
        alert.style.minWidth = '300px';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // 3秒后自动移除
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 3000);
    }
    
    destroy() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }
        if (this.toggleBtn && this.toggleBtn.parentNode) {
            this.toggleBtn.remove();
        }
        if (this.chatWindow && this.chatWindow.parentNode) {
            this.chatWindow.remove();
        }
    }
}

// 全局实例
let floatingChat = null;

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 检查用户是否已登录
    if (window.currentUserId) {
        // 检查是否在对话详情页面，如果是则不显示悬浮聊天窗口
        const isConversationPage = window.location.pathname.includes('/messages/') && 
                                  window.location.pathname !== '/messages/';
        
        if (!isConversationPage) {
            floatingChat = new FloatingChat();
        }
    }
});

// 导出到全局
window.FloatingChat = FloatingChat;
window.floatingChat = floatingChat;
