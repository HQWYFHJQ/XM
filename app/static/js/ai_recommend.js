// 智能推荐模态框交互功能
document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('ai-chat-container');
    const userInput = document.getElementById('ai-user-input');
    const sendButton = document.getElementById('ai-send-button');
    const modal = document.getElementById('aiRecommendModal');
    
    // 获取当前时间
    function getCurrentTime() {
        const now = new Date();
        const hours = now.getHours().toString().padStart(2, '0');
        const minutes = now.getMinutes().toString().padStart(2, '0');
        return `今天 ${hours}:${minutes}`;
    }
    
    // 发送消息
    function sendMessage() {
        const messageText = userInput.value.trim();
        if (messageText === '') return;
        
        // 检查用户是否已登录
        if (!window.currentUserId) {
            addMessage('请先登录后再使用智能推荐功能！', 'ai');
            return;
        }
        
        // 添加用户消息
        addMessage(messageText, 'user');
        userInput.value = '';
        
        // 显示AI正在输入
        showTypingIndicator();
        
        // 调用真实的AI推荐API
        callAIRecommendAPI(messageText);
    }
    
    // 调用AI推荐API
    function callAIRecommendAPI(userMessage) {
        fetch('/api/ai-recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_request: userMessage
            })
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator();
            
            if (data.success) {
                // 处理成功响应
                let responseText = '';
                if (data.data && data.data.content && data.data.content.parts && data.data.content.parts[0]) {
                    // 处理Gemini API返回的格式
                    responseText = data.data.content.parts[0].text;
                } else if (data.data && data.data.message) {
                    responseText = data.data.message;
                } else if (data.data && typeof data.data === 'string') {
                    responseText = data.data;
                } else if (data.data && data.data.recommendations) {
                    responseText = data.data.recommendations;
                } else {
                    responseText = '感谢您的提问！我已经为您分析了需求，请查看推荐结果。';
                }
                addMessage(responseText, 'ai');
            } else {
                // 处理错误响应
                addMessage(data.message || '抱歉，推荐服务暂时不可用，请稍后重试。', 'ai');
            }
        })
        .catch(error => {
            removeTypingIndicator();
            console.error('AI推荐API调用失败:', error);
            addMessage('网络连接出现问题，请检查网络后重试。', 'ai');
        });
    }
    
    // 简单的Markdown格式处理
    function formatMarkdown(text) {
        // 处理粗体 **text**
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // 处理斜体 *text*
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // 处理代码 `code`
        text = text.replace(/`(.*?)`/g, '<code>$1</code>');
        
        // 处理换行符
        text = text.replace(/\n/g, '<br>');
        
        // 处理表情符号和特殊字符
        text = text.replace(/🚀/g, '🚀');
        text = text.replace(/💪/g, '💪');
        text = text.replace(/🔥/g, '🔥');
        text = text.replace(/😊/g, '😊');
        text = text.replace(/💡/g, '💡');
        text = text.replace(/⭐/g, '⭐');
        
        return text;
    }
    
    // 添加消息到聊天框
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ai-message-${sender}`;
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = `ai-bubble ai-bubble-${sender}`;
        
        // 处理Markdown格式
        const formattedText = formatMarkdown(text);
        bubbleDiv.innerHTML = `${formattedText}<div class="ai-message-time">${getCurrentTime()}</div>`;
        
        messageDiv.appendChild(bubbleDiv);
        messageDiv.classList.add('ai-message-enter');
        
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }
    
    // 显示"正在输入"指示器
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'ai-message ai-message-ai';
        typingDiv.id = 'ai-typing-indicator';
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = 'ai-typing-indicator';
        bubbleDiv.innerHTML = `
            <span class="ai-typing-text">Gemini正在思考ing，请不要捉急(◕ᴗ◕✿)</span>
            <div class="ai-typing-dots">
                <div class="ai-typing-dot"></div>
                <div class="ai-typing-dot"></div>
                <div class="ai-typing-dot"></div>
            </div>
        `;
        
        typingDiv.appendChild(bubbleDiv);
        chatContainer.appendChild(typingDiv);
        scrollToBottom();
    }
    
    // 移除"正在输入"指示器
    function removeTypingIndicator() {
        const typingElement = document.getElementById('ai-typing-indicator');
        if (typingElement) {
            typingElement.remove();
        }
    }
    
    // 滚动到底部
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    
    // 事件监听
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
    
    // 模态框打开时自动聚焦输入框
    if (modal) {
        modal.addEventListener('shown.bs.modal', function() {
            if (userInput) {
                userInput.focus();
            }
        });
    }
    
    // 模态框关闭时清空输入框
    if (modal) {
        modal.addEventListener('hidden.bs.modal', function() {
            if (userInput) {
                userInput.value = '';
            }
        });
    }
    
    // 添加一些快捷回复按钮（可选）
    function addQuickReplies() {
        const quickReplies = [
            '推荐手机',
            '推荐电脑',
            '价格优惠',
            '商品质量',
            '交易流程',
            '使用帮助'
        ];
        
        const quickReplyContainer = document.createElement('div');
        quickReplyContainer.className = 'ai-quick-replies';
        quickReplyContainer.style.cssText = `
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 16px;
            padding: 0 16px;
        `;
        
        quickReplies.forEach(reply => {
            const button = document.createElement('button');
            button.className = 'btn btn-sm btn-outline-primary';
            button.textContent = reply;
            button.style.cssText = `
                border-radius: 20px;
                font-size: 12px;
                padding: 4px 12px;
                border: 1px solid #6c5ce7;
                color: #6c5ce7;
                background: transparent;
                cursor: pointer;
                transition: all 0.3s;
            `;
            
            button.addEventListener('click', function() {
                userInput.value = reply;
                sendMessage();
            });
            
            button.addEventListener('mouseenter', function() {
                this.style.background = '#6c5ce7';
                this.style.color = 'white';
            });
            
            button.addEventListener('mouseleave', function() {
                this.style.background = 'transparent';
                this.style.color = '#6c5ce7';
            });
            
            quickReplyContainer.appendChild(button);
        });
        
        // 在欢迎消息后插入快捷回复
        const welcomeMessage = chatContainer.querySelector('.ai-welcome-message');
        if (welcomeMessage) {
            welcomeMessage.parentNode.insertBefore(quickReplyContainer, welcomeMessage.nextSibling);
        }
    }
    
    // 初始化快捷回复
    addQuickReplies();
});
