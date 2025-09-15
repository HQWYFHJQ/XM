from datetime import datetime, timedelta
from app import db
from app.models import Transaction, Item, User
from app.services.email_service import EmailService
from app.services.announcement_service import AnnouncementService
from flask import current_app

class TransactionService:
    """交易服务类"""
    
    def __init__(self):
        self.email_service = EmailService()
        self.announcement_service = AnnouncementService()
    
    def process_timeout_transactions(self):
        """处理超时交易"""
        try:
            # 处理支付超时的交易（72小时）
            payment_timeout_transactions = Transaction.query.filter(
                Transaction.status == 'pending',
                Transaction.created_at < datetime.utcnow() - timedelta(hours=72)
            ).all()
            
            for transaction in payment_timeout_transactions:
                self._handle_payment_timeout(transaction)
            
            # 处理发货超时的交易（72小时）
            shipping_timeout_transactions = Transaction.query.filter(
                Transaction.status == 'paid',
                Transaction.payment_confirmed_at < datetime.utcnow() - timedelta(hours=72)
            ).all()
            
            for transaction in shipping_timeout_transactions:
                self._handle_shipping_timeout(transaction)
            
            # 处理收货超时的交易（72小时）
            delivery_timeout_transactions = Transaction.query.filter(
                Transaction.status == 'shipped',
                Transaction.shipped_at < datetime.utcnow() - timedelta(hours=72)
            ).all()
            
            for transaction in delivery_timeout_transactions:
                self._handle_delivery_timeout(transaction)
            
            return {
                'success': True,
                'message': f'处理了 {len(payment_timeout_transactions)} 个支付超时交易，{len(shipping_timeout_transactions)} 个发货超时交易，{len(delivery_timeout_transactions)} 个收货超时交易'
            }
            
        except Exception as e:
            current_app.logger.error(f"处理超时交易失败: {str(e)}")
            return {
                'success': False,
                'message': f'处理超时交易失败: {str(e)}'
            }
    
    def _handle_payment_timeout(self, transaction):
        """处理支付超时"""
        try:
            # 标记交易为超时
            transaction.timeout_transaction()
            
            # 恢复商品状态
            item = transaction.item
            item.status = 'active'
            item.sold_at = None
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_timeout_notification(transaction, 'payment')
            
            # 创建系统公告
            self._create_timeout_announcement(transaction, 'payment')
            
            # 创建定向推送公告
            announcement_service = AnnouncementService()
            announcement_service.create_transaction_announcement(transaction, 'timeout_notification')
            
        except Exception as e:
            current_app.logger.error(f"处理支付超时失败: {str(e)}")
            db.session.rollback()
    
    def _handle_shipping_timeout(self, transaction):
        """处理发货超时"""
        try:
            # 标记交易为超时
            transaction.timeout_transaction()
            
            # 恢复商品状态
            item = transaction.item
            item.status = 'active'
            item.sold_at = None
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_timeout_notification(transaction, 'shipping')
            
            # 创建系统公告
            self._create_timeout_announcement(transaction, 'shipping')
            
        except Exception as e:
            current_app.logger.error(f"处理发货超时失败: {str(e)}")
            db.session.rollback()
    
    def _handle_delivery_timeout(self, transaction):
        """处理收货超时"""
        try:
            # 自动确认收货
            transaction.complete_transaction()
            
            db.session.commit()
            
            # 发送邮件通知
            self._send_delivery_timeout_notification(transaction)
            
            # 创建系统公告
            self._create_delivery_timeout_announcement(transaction)
            
        except Exception as e:
            current_app.logger.error(f"处理收货超时失败: {str(e)}")
            db.session.rollback()
    
    def _send_timeout_notification(self, transaction, timeout_type):
        """发送超时通知邮件"""
        try:
            # 通知买家
            buyer_data = {
                'user_name': transaction.buyer.username,
                'item_title': transaction.item.title,
                'price': float(transaction.price),
                'timeout_reason': '支付超时' if timeout_type == 'payment' else '发货超时',
                'timeout_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.email_service.send_transaction_notification(
                transaction.buyer.email,
                'timeout',
                buyer_data
            )
            
            # 通知卖家
            seller_data = {
                'user_name': transaction.seller.username,
                'item_title': transaction.item.title,
                'price': float(transaction.price),
                'timeout_reason': '支付超时' if timeout_type == 'payment' else '发货超时',
                'timeout_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.email_service.send_transaction_notification(
                transaction.seller.email,
                'timeout',
                seller_data
            )
            
        except Exception as e:
            current_app.logger.error(f"发送超时通知邮件失败: {str(e)}")
    
    def _send_delivery_timeout_notification(self, transaction):
        """发送收货超时通知邮件"""
        try:
            # 通知买家
            buyer_data = {
                'user_name': transaction.buyer.username,
                'item_title': transaction.item.title,
                'price': float(transaction.price),
                'timeout_reason': '收货超时，系统自动确认',
                'timeout_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.email_service.send_transaction_notification(
                transaction.buyer.email,
                'timeout',
                buyer_data
            )
            
            # 通知卖家
            seller_data = {
                'user_name': transaction.seller.username,
                'item_title': transaction.item.title,
                'price': float(transaction.price),
                'timeout_reason': '收货超时，系统自动确认',
                'timeout_at': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            self.email_service.send_transaction_notification(
                transaction.seller.email,
                'timeout',
                seller_data
            )
            
        except Exception as e:
            current_app.logger.error(f"发送收货超时通知邮件失败: {str(e)}")
    
    def _create_timeout_announcement(self, transaction, timeout_type):
        """创建超时公告"""
        try:
            title = f"交易超时通知 - {transaction.item.title}"
            content = f"""
            <p>交易《{transaction.item.title}》已超时，系统已自动处理：</p>
            <ul>
                <li>商品：{transaction.item.title}</li>
                <li>价格：¥{transaction.price}</li>
                <li>买家：{transaction.buyer.username}</li>
                <li>卖家：{transaction.seller.username}</li>
                <li>超时原因：{'支付超时' if timeout_type == 'payment' else '发货超时'}</li>
                <li>处理时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <p>如有疑问，请联系系统管理员：21641685@qq.com</p>
            """
            
            self.announcement_service.create_announcement(
                title=title,
                content=content,
                announcement_type='notice',
                priority='normal',
                created_by=1  # 系统管理员ID
            )
            
        except Exception as e:
            current_app.logger.error(f"创建超时公告失败: {str(e)}")
    
    def _create_delivery_timeout_announcement(self, transaction):
        """创建收货超时公告"""
        try:
            title = f"交易自动确认 - {transaction.item.title}"
            content = f"""
            <p>交易《{transaction.item.title}》因收货超时，系统已自动确认完成：</p>
            <ul>
                <li>商品：{transaction.item.title}</li>
                <li>价格：¥{transaction.price}</li>
                <li>买家：{transaction.buyer.username}</li>
                <li>卖家：{transaction.seller.username}</li>
                <li>确认时间：{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}</li>
            </ul>
            <p>如有疑问，请联系系统管理员：21641685@qq.com</p>
            """
            
            self.announcement_service.create_announcement(
                title=title,
                content=content,
                announcement_type='notice',
                priority='normal',
                created_by=1  # 系统管理员ID
            )
            
        except Exception as e:
            current_app.logger.error(f"创建收货超时公告失败: {str(e)}")
    
    def get_transaction_stats(self):
        """获取交易统计信息"""
        try:
            stats = {
                'total_transactions': Transaction.query.count(),
                'pending_transactions': Transaction.query.filter_by(status='pending').count(),
                'paid_transactions': Transaction.query.filter_by(status='paid').count(),
                'shipped_transactions': Transaction.query.filter_by(status='shipped').count(),
                'delivered_transactions': Transaction.query.filter_by(status='delivered').count(),
                'completed_transactions': Transaction.query.filter_by(status='completed').count(),
                'cancelled_transactions': Transaction.query.filter_by(status='cancelled').count(),
                'timeout_transactions': Transaction.query.filter_by(status='timeout').count(),
            }
            
            # 计算今日交易
            today = datetime.utcnow().date()
            stats['today_transactions'] = Transaction.query.filter(
                db.func.date(Transaction.created_at) == today
            ).count()
            
            # 计算本周交易
            week_start = today - timedelta(days=today.weekday())
            stats['week_transactions'] = Transaction.query.filter(
                db.func.date(Transaction.created_at) >= week_start
            ).count()
            
            # 计算本月交易
            month_start = today.replace(day=1)
            stats['month_transactions'] = Transaction.query.filter(
                db.func.date(Transaction.created_at) >= month_start
            ).count()
            
            return {
                'success': True,
                'stats': stats
            }
            
        except Exception as e:
            current_app.logger.error(f"获取交易统计失败: {str(e)}")
            return {
                'success': False,
                'message': f'获取交易统计失败: {str(e)}'
            }
