-- 校园跳蚤市场数据库清理脚本
-- 删除多余的表，保留核心功能表

SET FOREIGN_KEY_CHECKS = 0;

-- 删除AI相关的多余表
DROP TABLE IF EXISTS `ai_chat_messages`;
DROP TABLE IF EXISTS `ai_chat_sessions`;
DROP TABLE IF EXISTS `ai_recommendations`;
DROP TABLE IF EXISTS `ai_user_preferences`;

SET FOREIGN_KEY_CHECKS = 1;

-- 显示剩余的表
SHOW TABLES;
