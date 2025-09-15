from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Item, Transaction
from app.services.email_service import EmailService
from datetime import datetime

transaction_api_bp = Blueprint('transaction_api', __name__)

@transaction_api_bp.route('/purchase', methods=['POST'])
@login_required
def purchase_item():
    """购买商品API"""
    try:
        data = request.get_json()
        item_id = data.get('item_id')
        
        if not item_id:
            return jsonify({
                'success': False,
                'message': '商品ID不能为空'
            }), 400
        
        # 获取商品信息
        item = Item.query.get(item_id)
        if not item:
            return jsonify({
                'success': False,
                'message': '商品不存在'
            }), 404
        
        # 检查商品状态
        if item.status != 'active':
            return jsonify({
                'success': False,
                'message': '商品已下架或售出'
            }), 400
        
        # 检查是否是自己发布的商品
        if item.seller_id == current_user.id:
            return jsonify({
                'success': False,
                'message': '不能购买自己发布的商品'
            }), 400
        
        # 检查是否已有进行中的交易
        existing_transaction = Transaction.query.filter(
            Transaction.item_id == item_id,
            Transaction.buyer_id == current_user.id,
            Transaction.status.in_(['pending', 'paid', 'shipped', 'delivered'])
        ).first()
        
        if existing_transaction:
            return jsonify({
                'success': False,
                'message': '您已购买此商品，请勿重复购买'
            }), 400
        
        # 创建交易记录
        transaction = Transaction(
            item_id=item_id,
            buyer_id=current_user.id,
            seller_id=item.seller_id,
            price=item.price,
            status='pending',
            payment_method='wechat'
        )
        
        db.session.add(transaction)
        
        # 更新商品状态为售出待买家确认
        item.status = 'sold'
        item.sold_at = datetime.utcnow()
        
        db.session.commit()
        
        # 发送邮件通知卖家
        email_service = EmailService()
        
        # 发送发货提醒邮件给卖家
        seller_email = item.seller.email
        subject = '校园跳蚤市场 - 商品售出通知'
        body = f"""
        <html>
        <body>
            <h2>🎉 恭喜！您的商品已售出</h2>
            <p>亲爱的 {item.seller.username}，</p>
            <p>您的商品《{item.title}》已被用户 {current_user.username} 购买！</p>
            <p>商品信息：</p>
            <ul>
                <li>商品名称：{item.title}</li>
                <li>售价：¥{item.price}</li>
                <li>买家：{current_user.username}</li>
                <li>购买时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <p>请及时登录系统确认发货，买家正在等待您的商品！</p>
            <p><a href="{request.host_url}admin/transactions" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">查看交易详情</a></p>
            <hr>
            <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
        </body>
        </html>
        """
        
        email_service.send_email(seller_email, subject, body)
        
        # 创建发货提醒定向推送公告
        from app.services.announcement_service import AnnouncementService
        announcement_service = AnnouncementService()
        announcement_service.create_transaction_announcement(transaction, 'shipping_reminder')
        
        return jsonify({
            'success': True,
            'message': '购买成功，已通知卖家发货',
            'transaction_id': transaction.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'购买失败: {str(e)}'
        }), 500

@transaction_api_bp.route('/<int:transaction_id>/confirm-payment', methods=['POST'])
@login_required
def confirm_payment(transaction_id):
    """确认支付API"""
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        
        # 检查权限
        if transaction.buyer_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '无权限操作此交易'
            }), 403
        
        # 检查交易状态
        if transaction.status != 'pending':
            return jsonify({
                'success': False,
                'message': '交易状态不正确'
            }), 400
        
        # 确认支付
        transaction.confirm_payment()
        db.session.commit()
        
        # 发送邮件通知卖家发货
        email_service = EmailService()
        
        seller_email = transaction.seller.email
        subject = '校园跳蚤市场 - 支付确认，请及时发货'
        body = f"""
        <html>
        <body>
            <h2>💰 买家已确认支付，请及时发货</h2>
            <p>亲爱的 {transaction.seller.username}，</p>
            <p>买家 {transaction.buyer.username} 已确认支付，请及时发货！</p>
            <p>交易信息：</p>
            <ul>
                <li>商品：{transaction.item.title}</li>
                <li>价格：¥{transaction.price}</li>
                <li>买家：{transaction.buyer.username}</li>
                <li>支付确认时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <p><a href="{request.host_url}admin/transactions" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">确认发货</a></p>
            <hr>
            <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
        </body>
        </html>
        """
        
        email_service.send_email(seller_email, subject, body)
        
        return jsonify({
            'success': True,
            'message': '支付确认成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'确认支付失败: {str(e)}'
        }), 500

@transaction_api_bp.route('/<int:transaction_id>/ship', methods=['POST'])
@login_required
def ship_item(transaction_id):
    """发货API"""
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        
        # 检查权限
        if transaction.seller_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '无权限操作此交易'
            }), 403
        
        # 检查交易状态
        if transaction.status != 'paid':
            return jsonify({
                'success': False,
                'message': '交易状态不正确'
            }), 400
        
        data = request.get_json()
        shipping_notes = data.get('shipping_notes', '')
        
        # 标记为已发货
        transaction.mark_shipped(shipping_notes)
        db.session.commit()
        
        # 发送邮件通知买家
        email_service = EmailService()
        
        buyer_email = transaction.buyer.email
        subject = '校园跳蚤市场 - 商品已发货'
        body = f"""
        <html>
        <body>
            <h2>📦 您的商品已发货</h2>
            <p>亲爱的 {transaction.buyer.username}，</p>
            <p>您购买的商品《{transaction.item.title}》已发货！</p>
            <p>交易信息：</p>
            <ul>
                <li>商品：{transaction.item.title}</li>
                <li>价格：¥{transaction.price}</li>
                <li>卖家：{transaction.seller.username}</li>
                <li>发货时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</li>
                {f'<li>发货备注：{shipping_notes}</li>' if shipping_notes else ''}
            </ul>
            <p>请及时确认收货，如有问题请联系卖家。</p>
            <p><a href="{request.host_url}profile/transactions" style="background-color: #17a2b8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">查看交易详情</a></p>
            <hr>
            <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
        </body>
        </html>
        """
        
        email_service.send_email(buyer_email, subject, body)
        
        # 创建收货提醒定向推送公告
        from app.services.announcement_service import AnnouncementService
        announcement_service = AnnouncementService()
        announcement_service.create_transaction_announcement(transaction, 'delivery_reminder')
        
        return jsonify({
            'success': True,
            'message': '发货成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'发货失败: {str(e)}'
        }), 500

@transaction_api_bp.route('/<int:transaction_id>/deliver', methods=['POST'])
@login_required
def deliver_item(transaction_id):
    """确认收货API"""
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        
        # 检查权限
        if transaction.buyer_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '无权限操作此交易'
            }), 403
        
        # 检查交易状态
        if transaction.status != 'shipped':
            return jsonify({
                'success': False,
                'message': '交易状态不正确'
            }), 400
        
        data = request.get_json()
        delivery_notes = data.get('delivery_notes', '')
        
        # 标记为已收货并完成交易
        transaction.mark_delivered(delivery_notes)
        transaction.complete_transaction()
        db.session.commit()
        
        # 发送邮件通知卖家
        email_service = EmailService()
        
        seller_email = transaction.seller.email
        subject = '校园跳蚤市场 - 买家已确认收货'
        body = f"""
        <html>
        <body>
            <h2>✅ 买家已确认收货</h2>
            <p>亲爱的 {transaction.seller.username}，</p>
            <p>买家 {transaction.buyer.username} 已确认收货，交易完成！</p>
            <p>交易信息：</p>
            <ul>
                <li>商品：{transaction.item.title}</li>
                <li>价格：¥{transaction.price}</li>
                <li>买家：{transaction.buyer.username}</li>
                <li>确认收货时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</li>
                {f'<li>收货备注：{delivery_notes}</li>' if delivery_notes else ''}
            </ul>
            <p>感谢您使用校园跳蚤市场！</p>
            <hr>
            <p style="color: #666; font-size: 12px;">此邮件由系统自动发送，请勿回复。</p>
        </body>
        </html>
        """
        
        email_service.send_email(seller_email, subject, body)
        
        return jsonify({
            'success': True,
            'message': '确认收货成功'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'确认收货失败: {str(e)}'
        }), 500

@transaction_api_bp.route('/<int:transaction_id>', methods=['GET'])
@login_required
def get_transaction(transaction_id):
    """获取交易详情API"""
    try:
        transaction = Transaction.query.get_or_404(transaction_id)
        
        # 检查权限
        if transaction.buyer_id != current_user.id and transaction.seller_id != current_user.id:
            return jsonify({
                'success': False,
                'message': '无权限查看此交易'
            }), 403
        
        return jsonify({
            'success': True,
            'transaction': transaction.to_dict()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取交易详情失败: {str(e)}'
        }), 500

@transaction_api_bp.route('/my', methods=['GET'])
@login_required
def get_my_transactions():
    """获取我的交易记录API"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status = request.args.get('status')
        
        query = Transaction.query.filter(
            (Transaction.buyer_id == current_user.id) | 
            (Transaction.seller_id == current_user.id)
        )
        
        if status:
            query = query.filter(Transaction.status == status)
        
        transactions = query.order_by(Transaction.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'success': True,
            'transactions': [t.to_dict() for t in transactions.items],
            'total': transactions.total,
            'pages': transactions.pages,
            'current_page': page
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取交易记录失败: {str(e)}'
        }), 500
