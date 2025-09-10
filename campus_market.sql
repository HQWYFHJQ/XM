/*
 Navicat Premium Dump SQL

 Source Server         : 广州华为云
 Source Server Type    : MySQL
 Source Server Version : 80042 (8.0.42-0ubuntu0.20.04.1)
 Source Host           : 113.45.53.114:5081
 Source Schema         : campus_market

 Target Server Type    : MySQL
 Target Server Version : 80042 (8.0.42-0ubuntu0.20.04.1)
 File Encoding         : 65001

 Date: 09/09/2025 10:04:47
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for ai_chat_messages
-- ----------------------------
DROP TABLE IF EXISTS `ai_chat_messages`;
CREATE TABLE `ai_chat_messages`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` int NOT NULL,
  `role` enum('user','assistant') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `message_type` enum('text','recommendation','error') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `message_metadata` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `session_id`(`session_id` ASC) USING BTREE,
  INDEX `ix_ai_chat_messages_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `ai_chat_messages_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `ai_chat_sessions` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 189 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ai_chat_sessions
-- ----------------------------
DROP TABLE IF EXISTS `ai_chat_sessions`;
CREATE TABLE `ai_chat_sessions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `session_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `status` enum('active','closed') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `last_message_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_ai_chat_sessions_session_id`(`session_id` ASC) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `ix_ai_chat_sessions_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `ai_chat_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 60 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ai_recommendations
-- ----------------------------
DROP TABLE IF EXISTS `ai_recommendations`;
CREATE TABLE `ai_recommendations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_id` int NOT NULL,
  `message_id` int NOT NULL,
  `item_id` int NOT NULL,
  `recommendation_type` enum('direct','similar','category','price_range') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `confidence_score` float NOT NULL,
  `reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `is_clicked` tinyint(1) NULL DEFAULT NULL,
  `is_contacted` tinyint(1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `clicked_at` datetime NULL DEFAULT NULL,
  `contacted_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `session_id`(`session_id` ASC) USING BTREE,
  INDEX `message_id`(`message_id` ASC) USING BTREE,
  INDEX `item_id`(`item_id` ASC) USING BTREE,
  INDEX `ix_ai_recommendations_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `ai_recommendations_ibfk_1` FOREIGN KEY (`session_id`) REFERENCES `ai_chat_sessions` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ai_recommendations_ibfk_2` FOREIGN KEY (`message_id`) REFERENCES `ai_chat_messages` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `ai_recommendations_ibfk_3` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 171 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for ai_user_preferences
-- ----------------------------
DROP TABLE IF EXISTS `ai_user_preferences`;
CREATE TABLE `ai_user_preferences`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `preferences` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `search_history` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `category_preferences` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `price_preferences` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `last_updated` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  CONSTRAINT `ai_user_preferences_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for categories
-- ----------------------------
DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `icon` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `parent_id` int NULL DEFAULT NULL,
  `sort_order` int NULL DEFAULT NULL,
  `is_active` tinyint(1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name` ASC) USING BTREE,
  INDEX `parent_id`(`parent_id` ASC) USING BTREE,
  CONSTRAINT `categories_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 121 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for chat_sessions
-- ----------------------------
DROP TABLE IF EXISTS `chat_sessions`;
CREATE TABLE `chat_sessions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `session_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_online` tinyint(1) NULL DEFAULT NULL,
  `last_active_at` datetime NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `idx_chat_session_user`(`user_id` ASC) USING BTREE,
  INDEX `idx_chat_session_online`(`is_online` ASC) USING BTREE,
  INDEX `idx_chat_session_active`(`last_active_at` ASC) USING BTREE,
  CONSTRAINT `chat_sessions_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for conversations
-- ----------------------------
DROP TABLE IF EXISTS `conversations`;
CREATE TABLE `conversations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `participants` json NOT NULL,
  `conversation_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `item_id` int NULL DEFAULT NULL,
  `last_message_at` datetime NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `is_deleted` tinyint(1) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_conversation_last_message`(`last_message_at` ASC) USING BTREE,
  INDEX `idx_conversation_type`(`conversation_type` ASC) USING BTREE,
  INDEX `idx_conversation_item`(`item_id` ASC) USING BTREE,
  CONSTRAINT `conversations_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for item_audits
-- ----------------------------
DROP TABLE IF EXISTS `item_audits`;
CREATE TABLE `item_audits`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending',
  `admin_id` int NULL DEFAULT NULL,
  `admin_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `rejection_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `reviewed_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `item_id`(`item_id` ASC) USING BTREE,
  INDEX `admin_id`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `item_audits_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `item_audits_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for item_image_audits
-- ----------------------------
DROP TABLE IF EXISTS `item_image_audits`;
CREATE TABLE `item_image_audits`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `admin_id` int NULL DEFAULT NULL,
  `admin_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `rejection_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `reviewed_at` datetime NULL DEFAULT NULL,
  `old_images` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `new_images` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `item_id`(`item_id` ASC) USING BTREE,
  INDEX `admin_id`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `item_image_audits_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `item_image_audits_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for item_profile_audits
-- ----------------------------
DROP TABLE IF EXISTS `item_profile_audits`;
CREATE TABLE `item_profile_audits`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `admin_id` int NULL DEFAULT NULL,
  `admin_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `rejection_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `reviewed_at` datetime NULL DEFAULT NULL,
  `old_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `new_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `item_status` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '单项审核状态JSON',
  `item_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '单项审核备注JSON',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `item_id`(`item_id` ASC) USING BTREE,
  INDEX `admin_id`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `item_profile_audits_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `item_profile_audits_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for items
-- ----------------------------
DROP TABLE IF EXISTS `items`;
CREATE TABLE `items`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `original_price` decimal(10, 2) NULL DEFAULT NULL,
  `category_id` int NOT NULL,
  `seller_id` int NOT NULL,
  `condition` enum('new','like_new','good','fair','poor') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `images` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `tags` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `contact_method` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `contact_info` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `status` enum('active','sold','inactive','deleted') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `audit_status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'approved',
  `view_count` int NULL DEFAULT NULL,
  `like_count` int NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `sold_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `category_id`(`category_id` ASC) USING BTREE,
  INDEX `seller_id`(`seller_id` ASC) USING BTREE,
  INDEX `ix_items_title`(`title` ASC) USING BTREE,
  INDEX `ix_items_created_at`(`created_at` ASC) USING BTREE,
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `items_ibfk_2` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 13 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for message_cleanup_logs
-- ----------------------------
DROP TABLE IF EXISTS `message_cleanup_logs`;
CREATE TABLE `message_cleanup_logs`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `cleanup_time` datetime NULL DEFAULT NULL,
  `messages_deleted` int NULL DEFAULT NULL,
  `conversations_deleted` int NULL DEFAULT NULL,
  `retention_days` int NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for message_notifications
-- ----------------------------
DROP TABLE IF EXISTS `message_notifications`;
CREATE TABLE `message_notifications`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `conversation_id` int NOT NULL,
  `message_id` int NOT NULL,
  `notification_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_read` tinyint(1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `message_id`(`message_id` ASC) USING BTREE,
  INDEX `idx_notification_read`(`is_read` ASC) USING BTREE,
  INDEX `idx_notification_created`(`created_at` ASC) USING BTREE,
  INDEX `idx_notification_user`(`user_id` ASC) USING BTREE,
  INDEX `idx_notification_conversation`(`conversation_id` ASC) USING BTREE,
  CONSTRAINT `message_notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `message_notifications_ibfk_2` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `message_notifications_ibfk_3` FOREIGN KEY (`message_id`) REFERENCES `messages` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for messages
-- ----------------------------
DROP TABLE IF EXISTS `messages`;
CREATE TABLE `messages`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `conversation_id` int NOT NULL,
  `sender_id` int NOT NULL,
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `message_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `attachment_url` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `is_read` tinyint(1) NULL DEFAULT NULL,
  `is_deleted` tinyint(1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_message_created`(`created_at` ASC) USING BTREE,
  INDEX `idx_message_read`(`is_read` ASC) USING BTREE,
  INDEX `idx_message_conversation`(`conversation_id` ASC) USING BTREE,
  INDEX `idx_message_sender`(`sender_id` ASC) USING BTREE,
  CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversations` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`sender_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for recommendations
-- ----------------------------
DROP TABLE IF EXISTS `recommendations`;
CREATE TABLE `recommendations`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `item_id` int NOT NULL,
  `algorithm_type` enum('collaborative_filtering','content_based','hybrid','popularity') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `score` float NOT NULL,
  `reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `is_clicked` tinyint(1) NULL DEFAULT NULL,
  `is_purchased` tinyint(1) NULL DEFAULT NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `clicked_at` datetime NULL DEFAULT NULL,
  `purchased_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `item_id`(`item_id` ASC) USING BTREE,
  INDEX `idx_user_recommendation`(`user_id` ASC, `created_at` ASC) USING BTREE,
  INDEX `ix_recommendations_created_at`(`created_at` ASC) USING BTREE,
  INDEX `idx_algorithm_score`(`algorithm_type` ASC, `score` ASC) USING BTREE,
  CONSTRAINT `recommendations_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `recommendations_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for transactions
-- ----------------------------
DROP TABLE IF EXISTS `transactions`;
CREATE TABLE `transactions`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `buyer_id` int NOT NULL,
  `seller_id` int NOT NULL,
  `price` decimal(10, 2) NOT NULL,
  `status` enum('pending','confirmed','completed','cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `payment_method` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `meeting_location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `meeting_time` datetime NULL DEFAULT NULL,
  `buyer_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `seller_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `completed_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `item_id`(`item_id` ASC) USING BTREE,
  INDEX `buyer_id`(`buyer_id` ASC) USING BTREE,
  INDEX `seller_id`(`seller_id` ASC) USING BTREE,
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`buyer_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `transactions_ibfk_3` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_audits
-- ----------------------------
DROP TABLE IF EXISTS `user_audits`;
CREATE TABLE `user_audits`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending',
  `admin_id` int NULL DEFAULT NULL,
  `admin_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `rejection_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT CURRENT_TIMESTAMP,
  `reviewed_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `admin_id`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `user_audits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE RESTRICT,
  CONSTRAINT `user_audits_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_avatar_audits
-- ----------------------------
DROP TABLE IF EXISTS `user_avatar_audits`;
CREATE TABLE `user_avatar_audits`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `admin_id` int NULL DEFAULT NULL,
  `admin_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `rejection_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `reviewed_at` datetime NULL DEFAULT NULL,
  `old_avatar` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `new_avatar` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `admin_id`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `user_avatar_audits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_avatar_audits_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_behaviors
-- ----------------------------
DROP TABLE IF EXISTS `user_behaviors`;
CREATE TABLE `user_behaviors`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `item_id` int NOT NULL,
  `behavior_type` enum('view','like','favorite','contact','purchase') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `duration` int NULL DEFAULT NULL,
  `ip_address` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `user_agent` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `item_id`(`item_id` ASC) USING BTREE,
  INDEX `idx_user_behavior_time`(`user_id` ASC, `behavior_type` ASC, `created_at` ASC) USING BTREE,
  INDEX `ix_user_behaviors_created_at`(`created_at` ASC) USING BTREE,
  INDEX `idx_user_item_behavior`(`user_id` ASC, `item_id` ASC, `behavior_type` ASC) USING BTREE,
  CONSTRAINT `user_behaviors_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_behaviors_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 73 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user_profile_audits
-- ----------------------------
DROP TABLE IF EXISTS `user_profile_audits`;
CREATE TABLE `user_profile_audits`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `admin_id` int NULL DEFAULT NULL,
  `admin_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `rejection_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `reviewed_at` datetime NULL DEFAULT NULL,
  `old_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `new_data` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `item_status` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `item_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id` ASC) USING BTREE,
  INDEX `admin_id`(`admin_id` ASC) USING BTREE,
  CONSTRAINT `user_profile_audits_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `user_profile_audits_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(80) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(120) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `real_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `student_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `avatar` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `bio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `interests` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `is_active` tinyint(1) NULL DEFAULT NULL,
  `is_admin` tinyint(1) NULL DEFAULT NULL,
  `audit_status` enum('pending','approved','rejected') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'approved',
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `last_login` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `ix_users_email`(`email` ASC) USING BTREE,
  UNIQUE INDEX `ix_users_username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
