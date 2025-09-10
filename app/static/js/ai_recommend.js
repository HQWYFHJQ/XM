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
        
        // 添加用户消息
        addMessage(messageText, 'user');
        userInput.value = '';
        
        // 显示AI正在输入
        showTypingIndicator();
        
        // 模拟AI思考时间
        setTimeout(() => {
            removeTypingIndicator();
            
            // 模拟AI回复 - 根据用户输入提供不同的回复
            const response = generateAIResponse(messageText);
            addMessage(response, 'ai');
        }, 1500 + Math.random() * 2000); // 随机延迟1.5-3.5秒，模拟思考过程
    }
    
    // 生成AI回复
    function generateAIResponse(userMessage) {
        const message = userMessage.toLowerCase();
        
        // 根据关键词生成不同的回复
        if (message.includes('推荐') || message.includes('商品')) {
            return "根据您的需求，我为您推荐以下几类商品：\n\n📱 电子产品：手机、平板、电脑配件\n💻 数码设备：耳机、音响、充电器\n🎮 游戏设备：游戏机、手柄、游戏卡带\n📚 学习用品：书籍、文具、学习工具\n\n您对哪一类商品比较感兴趣呢？我可以为您提供更具体的推荐！";
        } else if (message.includes('手机') || message.includes('iphone') || message.includes('android')) {
            return "关于手机推荐，我建议您考虑以下几个方面：\n\n🔍 预算范围：不同价位有不同的选择\n📱 品牌偏好：苹果、华为、小米、OPPO等\n⚡ 性能需求：处理器、内存、存储空间\n📷 拍照功能：摄像头配置和拍照效果\n🔋 续航能力：电池容量和充电速度\n\n请告诉我您的具体需求和预算，我会为您推荐合适的机型！";
        } else if (message.includes('电脑') || message.includes('笔记本') || message.includes('台式机')) {
            return "电脑推荐需要考虑您的使用场景：\n\n💻 学习办公：轻薄本、商务本\n🎮 游戏娱乐：游戏本、台式机\n🎨 设计创作：高性能笔记本、工作站\n📊 编程开发：配置要求较高的设备\n\n请告诉我您主要用于什么用途，以及预算范围，我会为您推荐合适的配置！";
        } else if (message.includes('价格') || message.includes('便宜') || message.includes('优惠')) {
            return "关于价格和优惠信息：\n\n💰 价格范围：我们平台上的商品价格都很实惠\n🎯 性价比：二手商品性价比通常更高\n💡 砍价技巧：可以尝试与卖家协商价格\n📅 促销活动：关注平台定期举办的优惠活动\n\n您想了解哪个商品的价格信息呢？";
        } else if (message.includes('质量') || message.includes('成色') || message.includes('新旧')) {
            return "关于商品质量保证：\n\n✅ 成色描述：每个商品都有详细的成色说明\n🔍 图片展示：多角度高清图片展示商品状态\n📝 功能测试：重要功能都会进行测试验证\n🛡️ 交易保障：平台提供交易安全保障\n\n建议您仔细查看商品详情和图片，如有疑问可以联系卖家详细了解！";
        } else if (message.includes('交易') || message.includes('购买') || message.includes('下单')) {
            return "交易流程很简单：\n\n1️⃣ 浏览商品：找到心仪的商品\n2️⃣ 联系卖家：通过平台消息功能沟通\n3️⃣ 确认交易：协商价格和交易方式\n4️⃣ 完成交易：线下或线上完成交易\n5️⃣ 评价反馈：交易完成后互相评价\n\n您想了解哪个环节的详细信息呢？";
        } else if (message.includes('帮助') || message.includes('怎么') || message.includes('如何')) {
            return "我很乐意为您提供帮助！\n\n❓ 常见问题：\n• 如何发布商品？\n• 如何联系卖家？\n• 如何修改个人信息？\n• 如何查看交易记录？\n\n💡 使用技巧：\n• 使用搜索功能快速找到商品\n• 关注感兴趣的商品类别\n• 设置价格提醒\n• 查看其他用户的评价\n\n请告诉我您具体需要什么帮助！";
        } else if (message.includes('你好') || message.includes('hi') || message.includes('hello')) {
            return "您好！很高兴为您服务！👋\n\n我是您的AI推荐助手，专门帮助您：\n• 推荐合适的商品\n• 解答购物疑问\n• 提供使用建议\n• 协助交易流程\n\n有什么我可以帮您的吗？";
        } else {
            // 默认回复
            const defaultResponses = [
                "我理解您的意思了。让我为您详细解释一下...",
                "这是一个很好的问题！根据我的分析，建议您可以...",
                "感谢您的提问。关于这个问题，我认为...",
                "我正在思考如何最好地回答这个问题...",
                "根据现有信息，我的建议是...",
                "您提到的这个问题很有意思，让我为您分析一下...",
                "我明白您的需求，这里有一些建议供您参考..."
            ];
            return defaultResponses[Math.floor(Math.random() * defaultResponses.length)];
        }
    }
    
    // 添加消息到聊天框
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ai-message-${sender}`;
        
        const bubbleDiv = document.createElement('div');
        bubbleDiv.className = `ai-bubble ai-bubble-${sender}`;
        
        // 处理换行符
        const formattedText = text.replace(/\n/g, '<br>');
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
            <span class="ai-typing-text">AI正在思考</span>
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
