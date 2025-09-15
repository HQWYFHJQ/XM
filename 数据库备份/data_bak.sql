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

 Date: 15/09/2025 17:45:30
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
) ENGINE = InnoDB AUTO_INCREMENT = 237 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ai_chat_messages
-- ----------------------------
INSERT INTO `ai_chat_messages` VALUES (26, 1, 'assistant', '我为您找到了充电设备相关的商品：\n1. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：标题包含\'充电\'、标题包含\'宝\'\n2. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：优质商品推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：成色良好\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:49:24');
INSERT INTO `ai_chat_messages` VALUES (27, 1, 'user', '推荐一些手机', 'text', NULL, '2025-09-06 16:49:24');
INSERT INTO `ai_chat_messages` VALUES (28, 1, 'assistant', '我为您找到了手机相关的商品：\n1. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：属于手机分类\n2. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：优质商品推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：成色良好\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:49:24');
INSERT INTO `ai_chat_messages` VALUES (29, 1, 'user', '我需要笔记本电脑', 'text', NULL, '2025-09-06 16:49:24');
INSERT INTO `ai_chat_messages` VALUES (30, 1, 'assistant', '我为您找到了电脑相关的商品：\n1. MacBook Air M1 8GB+256GB - ¥4500.00\n   推荐理由：属于电脑分类\n2. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：优质商品推荐\n3. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：优质商品推荐\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:49:24');
INSERT INTO `ai_chat_messages` VALUES (31, 1, 'user', '有什么好的耳机推荐吗', 'text', NULL, '2025-09-06 16:49:25');
INSERT INTO `ai_chat_messages` VALUES (32, 1, 'assistant', '我为您找到了耳机相关的商品：\n1. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：描述包含\'有\'、描述包含\'的\'\n2. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：描述包含\'好\'\n3. MacBook Air M1 8GB+256GB - ¥4500.00\n   推荐理由：描述包含\'好\'\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:49:25');
INSERT INTO `ai_chat_messages` VALUES (33, 1, 'user', '我想要一个充电宝', 'text', NULL, '2025-09-06 16:49:55');
INSERT INTO `ai_chat_messages` VALUES (34, 1, 'assistant', '我为您找到了充电设备相关的商品：\n1. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：标题包含\'充电\'、标题包含\'宝\'\n2. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：优质商品推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：成色良好\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:49:55');
INSERT INTO `ai_chat_messages` VALUES (35, 1, 'user', '推荐一些手机', 'text', NULL, '2025-09-06 16:49:55');
INSERT INTO `ai_chat_messages` VALUES (36, 1, 'assistant', '我为您找到了手机相关的商品：\n1. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：属于手机分类\n2. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：优质商品推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：成色良好\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:49:55');
INSERT INTO `ai_chat_messages` VALUES (37, 1, 'user', '我需要笔记本电脑', 'text', NULL, '2025-09-06 16:49:55');
INSERT INTO `ai_chat_messages` VALUES (38, 1, 'assistant', '我为您找到了电脑相关的商品：\n1. MacBook Air M1 8GB+256GB - ¥4500.00\n   推荐理由：属于电脑分类\n2. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：优质商品推荐\n3. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：优质商品推荐\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:49:55');
INSERT INTO `ai_chat_messages` VALUES (39, 1, 'user', '有什么好的耳机推荐吗', 'text', NULL, '2025-09-06 16:49:55');
INSERT INTO `ai_chat_messages` VALUES (40, 1, 'assistant', '我为您找到了耳机相关的商品：\n1. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：描述包含\'有\'、描述包含\'的\'\n2. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：描述包含\'好\'\n3. MacBook Air M1 8GB+256GB - ¥4500.00\n   推荐理由：描述包含\'好\'\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:49:55');
INSERT INTO `ai_chat_messages` VALUES (41, 3, 'user', '我想要一个充电宝', 'text', NULL, '2025-09-06 16:51:41');
INSERT INTO `ai_chat_messages` VALUES (42, 3, 'assistant', '我为您找到了充电设备相关的商品：\n1. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：标题包含\'充电\'、标题包含\'宝\'\n2. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：优质商品推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：成色良好\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:51:41');
INSERT INTO `ai_chat_messages` VALUES (43, 3, 'user', '推荐一些手机', 'text', NULL, '2025-09-06 16:51:41');
INSERT INTO `ai_chat_messages` VALUES (44, 3, 'assistant', '我为您找到了手机相关的商品：\n1. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：属于手机分类\n2. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：优质商品推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：成色良好\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:51:41');
INSERT INTO `ai_chat_messages` VALUES (45, 3, 'user', '我需要笔记本电脑', 'text', NULL, '2025-09-06 16:51:42');
INSERT INTO `ai_chat_messages` VALUES (46, 3, 'assistant', '我为您找到了电脑相关的商品：\n1. MacBook Air M1 8GB+256GB - ¥4500.00\n   推荐理由：属于电脑分类\n2. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：优质商品推荐\n3. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：优质商品推荐\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:51:42');
INSERT INTO `ai_chat_messages` VALUES (47, 3, 'user', '有什么好的耳机推荐吗', 'text', NULL, '2025-09-06 16:51:42');
INSERT INTO `ai_chat_messages` VALUES (48, 3, 'assistant', '我为您找到了耳机相关的商品：\n1. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：描述包含\'有\'、描述包含\'的\'\n2. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：描述包含\'好\'\n3. MacBook Air M1 8GB+256GB - ¥4500.00\n   推荐理由：描述包含\'好\'\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-06 16:51:42');
INSERT INTO `ai_chat_messages` VALUES (49, 4, 'assistant', '您好！我是您的AI商品推荐助手。请告诉我您想要什么类型的商品，我会为您推荐最合适的二手电子产品。', 'text', NULL, '2025-09-07 06:43:12');
INSERT INTO `ai_chat_messages` VALUES (50, 4, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-07 06:43:12');
INSERT INTO `ai_chat_messages` VALUES (51, 5, 'assistant', '您好！我是您的AI商品推荐助手。请告诉我您想要什么类型的商品，我会为您推荐最合适的二手电子产品。', 'text', NULL, '2025-09-07 06:43:53');
INSERT INTO `ai_chat_messages` VALUES (52, 5, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-07 06:43:53');
INSERT INTO `ai_chat_messages` VALUES (53, 5, 'assistant', '我为您推荐以下商品：\n1. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：基于商品特征和热度的推荐\n2. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：基于商品特征和热度的推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：基于商品特征和热度的推荐\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-07 06:43:54');
INSERT INTO `ai_chat_messages` VALUES (54, 6, 'assistant', '您好！我是您的AI商品推荐助手。请告诉我您想要什么类型的商品，我会为您推荐最合适的二手电子产品。', 'text', NULL, '2025-09-07 06:50:27');
INSERT INTO `ai_chat_messages` VALUES (55, 6, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-07 06:50:27');
INSERT INTO `ai_chat_messages` VALUES (56, 6, 'assistant', '我为您推荐以下商品：\n1. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：基于商品特征和热度的推荐\n2. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：基于商品特征和热度的推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：基于商品特征和热度的推荐\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-07 06:50:27');
INSERT INTO `ai_chat_messages` VALUES (57, 7, 'assistant', '您好！我是您的AI商品推荐助手。请告诉我您想要什么类型的商品，我会为您推荐最合适的二手电子产品。', 'text', NULL, '2025-09-07 06:50:27');
INSERT INTO `ai_chat_messages` VALUES (58, 7, 'user', '推荐手机', 'text', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (59, 7, 'assistant', '我为您找到了手机相关的商品：\n1. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：基于商品特征和热度的推荐\n2. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：基于商品特征和热度的推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：基于商品特征和热度的推荐\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (60, 8, 'assistant', '您好！我是您的AI商品推荐助手。请告诉我您想要什么类型的商品，我会为您推荐最合适的二手电子产品。', 'text', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (61, 8, 'user', '推荐电脑', 'text', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (62, 8, 'assistant', '我为您找到了电脑相关的商品：\n1. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：基于商品特征和热度的推荐\n2. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：基于商品特征和热度的推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：基于商品特征和热度的推荐\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (63, 9, 'assistant', '您好！我是您的AI商品推荐助手。请告诉我您想要什么类型的商品，我会为您推荐最合适的二手电子产品。', 'text', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (64, 9, 'user', '推荐便宜的商品', 'text', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (65, 9, 'assistant', '我为您找到了低价的商品：\n1. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：基于商品特征和热度的推荐\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (66, 10, 'assistant', '您好！我是您的AI商品推荐助手。请告诉我您想要什么类型的商品，我会为您推荐最合适的二手电子产品。', 'text', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (67, 10, 'user', '推荐1000元以下的商品', 'text', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (68, 10, 'assistant', '我为您推荐以下商品：\n1. 小米充电宝 10000mAh - ¥80.00\n   推荐理由：基于商品特征和热度的推荐\n2. 小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环 - ¥300.00\n   推荐理由：基于商品特征和热度的推荐\n3. 测试商品_修改 - ¥150.00\n   推荐理由：基于商品特征和热度的推荐\n还有2个商品推荐，您可以点击查看详情。\n\n您可以点击商品查看详情，或者告诉我您想要什么类型的商品。', 'recommendation', NULL, '2025-09-07 06:50:28');
INSERT INTO `ai_chat_messages` VALUES (69, 11, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 06:00:56');
INSERT INTO `ai_chat_messages` VALUES (70, 12, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 06:22:57');
INSERT INTO `ai_chat_messages` VALUES (71, 13, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 06:24:23');
INSERT INTO `ai_chat_messages` VALUES (72, 14, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-08 06:25:41');
INSERT INTO `ai_chat_messages` VALUES (73, 15, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 06:27:05');
INSERT INTO `ai_chat_messages` VALUES (74, 15, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 06:27:13');
INSERT INTO `ai_chat_messages` VALUES (75, 15, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 06:27:20');
INSERT INTO `ai_chat_messages` VALUES (76, 15, 'user', '你好', 'text', NULL, '2025-09-08 06:27:45');
INSERT INTO `ai_chat_messages` VALUES (77, 16, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 06:28:46');
INSERT INTO `ai_chat_messages` VALUES (78, 16, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 06:28:53');
INSERT INTO `ai_chat_messages` VALUES (79, 16, 'user', '你好', 'text', NULL, '2025-09-08 06:29:00');
INSERT INTO `ai_chat_messages` VALUES (80, 16, 'assistant', '您好！看到您在找充电宝，不过目前二手商城里充电宝类商品比较少呢。我为您推荐几款实用的电子产品：\n\n🔋 **测试商品_修改** ¥150\n虽然是测试商品，但价格实惠，适合日常应急使用\n\n建议您可以：\n1️⃣ 尝试搜索\"移动电源\"等其他关键词\n2️⃣ 过段时间再来看看新品上架\n3️⃣ 如果需要急用，也可以考虑发布求购信息\n\n需要我帮您看看其他类型的电子产品吗？比如笔记本电脑或游戏机都很受欢迎哦！', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 06:29:08');
INSERT INTO `ai_chat_messages` VALUES (81, 16, 'assistant', '你好呀！😊 为你推荐这款 **小米充电宝 10000mAh**，只要 ¥80！它支持快充，充电速度快，而且体积小巧、携带方便，特别适合上课、自习或外出使用。成色很新，性价比超高哦～\n\n如果你经常需要长时间续航，这款10000mAh的容量完全够用！感兴趣的话可以尽快联系卖家，好东西不等人啦！需要看看其它款式也可以告诉我~ 🔋', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 06:29:14');
INSERT INTO `ai_chat_messages` VALUES (82, 17, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 06:29:49');
INSERT INTO `ai_chat_messages` VALUES (83, 18, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-08 06:30:45');
INSERT INTO `ai_chat_messages` VALUES (84, 19, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 06:33:29');
INSERT INTO `ai_chat_messages` VALUES (85, 20, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 06:34:39');
INSERT INTO `ai_chat_messages` VALUES (86, 21, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-08 06:36:21');
INSERT INTO `ai_chat_messages` VALUES (87, 22, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-08 06:37:13');
INSERT INTO `ai_chat_messages` VALUES (88, 23, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 06:39:19');
INSERT INTO `ai_chat_messages` VALUES (89, 24, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 06:42:26');
INSERT INTO `ai_chat_messages` VALUES (90, 24, 'user', '你好，我想买一个手机', 'text', NULL, '2025-09-08 06:42:36');
INSERT INTO `ai_chat_messages` VALUES (91, 24, 'assistant', '你好呀！看到你想买手机，不过目前我们二手商城手机类商品暂时缺货呢 😢  \n\n不过我发现有一款**小米手环9Pro**可能你会感兴趣～虽然不是手机，但作为智能穿戴设备真的很实用！✨  \n\n🌟 **推荐理由**：  \n- 只要¥300，性价比超高  \n- 支持心率、血氧监测和睡眠呼吸暂停分析，健康功能很全面  \n- 操作简单表盘多，做工细腻佩戴舒服  \n- 适合运动或日常使用，尤其适合学生党  \n\n如果你暂时不需要换手机，也可以试试用手环搭配现在的手机～或者告诉我你的具体预算和需求，我再帮你看看其他商品哦！ 😊', 'recommendation', '{\"recommended_items\": [6]}', '2025-09-08 06:42:53');
INSERT INTO `ai_chat_messages` VALUES (92, 24, 'user', '测试', 'text', NULL, '2025-09-08 06:42:56');
INSERT INTO `ai_chat_messages` VALUES (93, 25, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 06:46:57');
INSERT INTO `ai_chat_messages` VALUES (94, 26, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 06:58:38');
INSERT INTO `ai_chat_messages` VALUES (95, 26, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 06:58:48');
INSERT INTO `ai_chat_messages` VALUES (96, 26, 'assistant', '您好！看到您需要充电宝，不过我这边暂时没有合适的二手充电宝推荐呢 😅\n\n目前商城里有几款不错的其他商品，比如：\n- MacBook Air M1，学习办公都很流畅\n- Nintendo Switch，课余时间放松一下很棒\n\n建议您可以：\n1️⃣ 试试搜索“移动电源”或“充电宝”看看\n2️⃣ 留意商城更新，经常有新商品上架哦\n\n需要其他帮助随时找我~', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 06:59:03');
INSERT INTO `ai_chat_messages` VALUES (97, 27, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 07:04:45');
INSERT INTO `ai_chat_messages` VALUES (98, 27, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 07:04:54');
INSERT INTO `ai_chat_messages` VALUES (99, 27, 'assistant', '你好呀！看到你在找充电宝，不过我暂时没有找到合适的充电宝类商品呢 😅  \n\n目前商城里有几款不错的电子产品，虽然不是充电宝，但可能你也感兴趣：  \n- **MacBook Air M1**（¥4500）：性能强、续航好，适合学习办公，自带长续航不用频繁充电～  \n- **Nintendo Switch 续航版**（¥1800）：游戏神器，本身续航也不错，出门带它娱乐学习两不误！  \n\n如果你坚持想要充电宝，可以试试调整关键词（比如“移动电源”），或者稍后再来逛逛，经常有新货上架哦！ ✨', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 07:05:12');
INSERT INTO `ai_chat_messages` VALUES (100, 27, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 07:05:21');
INSERT INTO `ai_chat_messages` VALUES (101, 27, 'assistant', '太棒了！我找到一款很适合你的充电宝 🔋  \n\n**小米充电宝 10000mAh**（¥80）  \n👉 支持快充，出门携带超方便，10000mAh容量足够手机充满2-3次！  \n👉 成色很新，性价比高，学生党闭眼入～  \n\n建议早点联系卖家，这种实用小物件很抢手哦！如果有其他需求也可以随时告诉我呀 😊', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 07:05:36');
INSERT INTO `ai_chat_messages` VALUES (102, 28, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 07:41:42');
INSERT INTO `ai_chat_messages` VALUES (103, 28, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 07:42:09');
INSERT INTO `ai_chat_messages` VALUES (104, 28, 'assistant', '🔋找到一款很不错的充电宝推荐给你！\n\n**小米充电宝 10000mAh** 仅需 ¥80 \n- 支持快充，充电速度很给力\n- 10000mAh大容量，足够手机充满2-3次\n- 便携轻巧，上课外出携带无压力\n- 成色良好，性价比超高\n\n适合学生日常使用，续航一整天没问题！建议尽快联系卖家查看实物哦，好货不等人～需要我帮你看看其他款式也可以随时说！', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 07:42:25');
INSERT INTO `ai_chat_messages` VALUES (105, 29, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 07:42:37');
INSERT INTO `ai_chat_messages` VALUES (106, 29, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 07:42:37');
INSERT INTO `ai_chat_messages` VALUES (107, 29, 'assistant', '🔋 发现一款超值的小米充电宝！这款10000mAh的移动电源3支持快充，充电速度快而且便携性超棒，上课外出都能轻松带上。只要80元，性价比很高，成色也很不错～ \n\n如果你经常需要长时间使用手机或平板，这个容量完全够用，而且小米的品质很可靠。建议尽快联系卖家哦，好东西不等人！需要看更多细节的话可以让我帮你查～', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 07:42:51');
INSERT INTO `ai_chat_messages` VALUES (108, 30, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 08:02:22');
INSERT INTO `ai_chat_messages` VALUES (109, 30, 'user', '我需要一个充电宝', 'text', NULL, '2025-09-08 08:02:28');
INSERT INTO `ai_chat_messages` VALUES (110, 31, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 08:03:49');
INSERT INTO `ai_chat_messages` VALUES (111, 31, 'user', '我想要一个充电宝', 'text', NULL, '2025-09-08 08:04:17');
INSERT INTO `ai_chat_messages` VALUES (112, 31, 'assistant', '你好！看到你在找充电宝，不过我这边暂时没有合适的二手充电宝推荐呢 😅\n\n目前商城里有几款不错的电子产品，比如性价比高的MacBook Air M1，适合学习办公，还有Switch游戏机可以放松娱乐～如果你对它们感兴趣，我可以帮你详细介绍！\n\n或者你可以试试调整搜索条件，比如筛选“数码配件”类别，说不定能找到刚刚上新的充电宝哦！需要的话我随时帮你留意 👍', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 08:04:33');
INSERT INTO `ai_chat_messages` VALUES (113, 32, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 08:08:03');
INSERT INTO `ai_chat_messages` VALUES (114, 33, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 08:08:26');
INSERT INTO `ai_chat_messages` VALUES (115, 33, 'user', '我想要一个充电宝', 'text', NULL, '2025-09-08 08:08:26');
INSERT INTO `ai_chat_messages` VALUES (116, 33, 'assistant', '您好！虽然目前二手商城里的充电宝选择比较少，但我为您找到了几款很不错的数码产品，同样实用且性价比高哦～\n\n特别是这款MacBook Air M1，性能强劲又便携，续航能力出色，非常适合校园学习使用。Switch续航版也很棒，课余时间放松娱乐很不错！\n\n建议您可以调整搜索条件，或者稍后再来看看，经常有新商品上架呢！想了解哪款的详细信息，我都很乐意为您介绍 😊', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 08:08:40');
INSERT INTO `ai_chat_messages` VALUES (117, 34, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 08:09:17');
INSERT INTO `ai_chat_messages` VALUES (118, 34, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 08:09:24');
INSERT INTO `ai_chat_messages` VALUES (119, 34, 'assistant', '找到了充电宝！推荐这款小米充电宝10000mAh，只要¥80。它支持快充，充电速度快，而且10000mAh的容量足够一天使用，非常便携实用。成色良好，性价比很高，先到先得哦！建议你尽快联系卖家了解更多详情，避免错过好货～', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 08:09:37');
INSERT INTO `ai_chat_messages` VALUES (120, 35, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 08:39:06');
INSERT INTO `ai_chat_messages` VALUES (121, 36, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 09:55:33');
INSERT INTO `ai_chat_messages` VALUES (122, 36, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 09:55:34');
INSERT INTO `ai_chat_messages` VALUES (123, 36, 'assistant', '找到了充电宝！推荐这款小米充电宝 10000mAh，只要¥80。它支持快充，出门携带很方便，电量足够一天使用，而且成色很新～如果你经常需要外出或者上课，这款真的很实用！建议尽快联系卖家，先到先得哦。想了解更多细节的话，可以看看商品详情或者直接和卖家沟通～', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 09:55:48');
INSERT INTO `ai_chat_messages` VALUES (124, 36, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 09:56:08');
INSERT INTO `ai_chat_messages` VALUES (125, 36, 'assistant', '找到了充电宝！推荐这款小米充电宝 10000mAh，只要¥80。它支持快充，出门携带很方便，电量足够一天使用，而且成色很新～如果你经常需要外出或者上课，这款真的很实用！建议尽快联系卖家，先到先得哦。想了解更多细节的话，可以看看商品详情或者直接和卖家沟通～', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 09:56:22');
INSERT INTO `ai_chat_messages` VALUES (126, 36, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 10:01:40');
INSERT INTO `ai_chat_messages` VALUES (127, 36, 'assistant', '找到了充电宝！推荐这款小米充电宝 10000mAh，只要¥80。它支持快充，出门携带很方便，电量足够一天使用，而且成色很新～如果你经常需要外出或者上课，这款真的很实用！建议尽快联系卖家，先到先得哦。想了解更多细节的话，可以看看商品详情或者直接和卖家沟通～', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 10:01:54');
INSERT INTO `ai_chat_messages` VALUES (128, 36, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 10:02:33');
INSERT INTO `ai_chat_messages` VALUES (129, 36, 'assistant', '找到了充电宝！推荐这款小米充电宝 10000mAh，只要¥80。它支持快充，出门携带很方便，电量足够一天使用，而且成色很新～如果你经常需要外出或者上课，这款真的很实用！建议尽快联系卖家，先到先得哦。想了解更多细节的话，可以看看商品详情或者直接和卖家沟通～', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 10:02:45');
INSERT INTO `ai_chat_messages` VALUES (130, 37, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 10:11:08');
INSERT INTO `ai_chat_messages` VALUES (131, 37, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 10:11:08');
INSERT INTO `ai_chat_messages` VALUES (132, 37, 'assistant', '找到了充电宝！推荐这款小米充电宝 10000mAh，只要¥80。它支持快充，出门携带很方便，电量足够一天使用，而且成色很新～如果你经常需要外出或者上课，这款真的很实用。建议尽快联系卖家，先到先得哦！需要的话我可以帮你看看更多细节。', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 10:11:22');
INSERT INTO `ai_chat_messages` VALUES (133, 38, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 10:12:20');
INSERT INTO `ai_chat_messages` VALUES (134, 38, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 10:12:21');
INSERT INTO `ai_chat_messages` VALUES (135, 38, 'assistant', '找到了充电宝！推荐这款小米充电宝10000mAh，只要¥80。它支持快充，充电速度快，而且很便携，带出门特别方便。成色良好，性价比很高，适合日常使用和外出携带。感兴趣的话可以看看商品详情哦！', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 10:12:33');
INSERT INTO `ai_chat_messages` VALUES (136, 39, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-08 12:11:00');
INSERT INTO `ai_chat_messages` VALUES (137, 39, 'user', '推荐一个手环', 'text', NULL, '2025-09-08 12:11:00');
INSERT INTO `ai_chat_messages` VALUES (138, 39, 'assistant', '您好！虽然目前没有找到手环类商品，但我为您精选了几款很不错的二手电子产品：\n\n1. 💻 MacBook Air M1 - ¥4500\n   2020款M1芯片，性能强劲续航久，学习办公都很合适\n\n2. 🎮 Nintendo Switch续航版 - ¥1800\n   包含原装手柄，游戏体验很棒，课余时间放松神器\n\n这几款都是校园生活中很实用的设备哦！如果您想找手环，建议可以稍后再来看看，或者告诉我您的预算范围，我帮您多留意一下～', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 12:11:16');
INSERT INTO `ai_chat_messages` VALUES (139, 40, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 12:29:43');
INSERT INTO `ai_chat_messages` VALUES (140, 40, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 12:29:44');
INSERT INTO `ai_chat_messages` VALUES (141, 40, 'assistant', '找到了充电宝！推荐这款小米充电宝10000mAh，只要¥80。它支持快充，充电速度快，而且10000mAh的容量足够一天外出使用，非常便携实用。成色良好，性价比很高，适合学生日常携带。建议尽快联系卖家，先到先得哦！需要的话可以看看商品详情～', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 12:29:58');
INSERT INTO `ai_chat_messages` VALUES (142, 41, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 12:33:01');
INSERT INTO `ai_chat_messages` VALUES (143, 41, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 12:33:01');
INSERT INTO `ai_chat_messages` VALUES (144, 41, 'assistant', '太好了！找到了充电宝！🔋\n\n强烈推荐这款 **小米充电宝 10000mAh**，只要 ¥80！它支持快充，电量足又便携，上课外出带着都方便，而且成色很新～性价比超高！\n\n感兴趣的话可以看看商品详情，早点下手免得被抢走哦！', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 12:33:14');
INSERT INTO `ai_chat_messages` VALUES (145, 42, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-08 13:05:24');
INSERT INTO `ai_chat_messages` VALUES (146, 42, 'user', '推荐一个智能手环', 'text', NULL, '2025-09-08 13:05:24');
INSERT INTO `ai_chat_messages` VALUES (147, 42, 'assistant', '您好！我为您找到了几款不错的二手电子产品，不过目前智能手环类商品暂时缺货呢。让我为您推荐几款其他超值的电子产品吧：\n\n📱 MacBook Air M1 仅售4500元！M1芯片性能强劲，特别适合学习和办公使用，成色很新哦～\n\n🎮 Nintendo Switch 续航版1800元！包含原装手柄，课余时间玩玩游戏放松一下很不错呢！\n\n建议您可以稍后再来看看，或者告诉我您的预算范围，我帮您留意新上架的智能手环！', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 13:05:41');
INSERT INTO `ai_chat_messages` VALUES (148, 43, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 13:13:42');
INSERT INTO `ai_chat_messages` VALUES (149, 43, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 13:13:42');
INSERT INTO `ai_chat_messages` VALUES (150, 43, 'assistant', '太好了！找到了充电宝！🔋\n\n这款小米充电宝10000mAh真的很实用，支持快充，出门一天完全够用，而且非常便携。只要80元，性价比很高，成色也很不错！\n\n如果你需要更大容量或者更小巧的，也可以告诉我，我再帮你找找看！要不要看看详情？😊', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 13:13:57');
INSERT INTO `ai_chat_messages` VALUES (151, 43, 'user', '推荐一个手环', 'text', NULL, '2025-09-08 13:14:21');
INSERT INTO `ai_chat_messages` VALUES (152, 43, 'assistant', '您好！我为您找到了几款不错的商品，不过目前没有专门的手环类商品。您可以看看这些实用的选择：\n\n1. **MacBook Air M1** - ¥4500.00  \n   2020款，M1芯片性能强，适合学习和办公，成色良好，性价比很高！\n\n2. **Nintendo Switch 续航版** - ¥1800.00  \n   包含原装手柄，游戏体验很棒，适合课余放松。\n\n如果您特别想要手环，可以调整搜索条件，或者告诉我更多偏好，我再帮您找找！要不要看看这些商品的详情？😊', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 13:14:37');
INSERT INTO `ai_chat_messages` VALUES (153, 44, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 13:56:17');
INSERT INTO `ai_chat_messages` VALUES (154, 44, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 13:57:13');
INSERT INTO `ai_chat_messages` VALUES (155, 44, 'assistant', '找到了充电宝！推荐这款小米充电宝10000mAh，只要¥80。它支持快充，充电速度快，而且很便携，上课外出带着都很方便。成色良好，性价比高，先到先得哦～建议你尽快联系卖家查看实物，确认一下使用情况再入手！', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 13:57:26');
INSERT INTO `ai_chat_messages` VALUES (156, 44, 'user', '推荐一个U盘', 'text', NULL, '2025-09-08 13:58:27');
INSERT INTO `ai_chat_messages` VALUES (157, 44, 'assistant', '找到了U盘！推荐这款金士顿16G U盘，只要¥45。它采用伸缩式设计不怕丢盖子，USB3.2传输速度很快，材质耐用还支持刻字定制哦～适合日常学习办公使用。建议联系卖家确认下实际读写速度，二手U盘记得测试下稳定性再入手！', 'recommendation', '{\"recommended_items\": [10, 11]}', '2025-09-08 13:58:40');
INSERT INTO `ai_chat_messages` VALUES (158, 45, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 13:59:40');
INSERT INTO `ai_chat_messages` VALUES (159, 46, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 14:00:11');
INSERT INTO `ai_chat_messages` VALUES (160, 45, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 14:00:14');
INSERT INTO `ai_chat_messages` VALUES (161, 45, 'assistant', '找到了充电宝！推荐这款小米充电宝10000mAh，只要¥80。它支持快充，出门一天完全够用，而且很便携，上课或自习带着都方便。成色也很不错，性价比高，建议尽快联系卖家看看实物哦！', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 14:00:27');
INSERT INTO `ai_chat_messages` VALUES (162, 47, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 14:00:52');
INSERT INTO `ai_chat_messages` VALUES (163, 47, 'user', '帮我推荐一个合适的手环', 'text', NULL, '2025-09-08 14:01:00');
INSERT INTO `ai_chat_messages` VALUES (164, 47, 'assistant', '您好！虽然目前没有专门的手环类商品，不过我看到商城里有几款不错的电子产品值得考虑哦～\n\n✨推荐看看这款MacBook Air M1，学习办公都很合适，轻便耐用；如果喜欢玩游戏的话，Switch续航版也是超棒的选择，课余时间放松超赞！\n\n建议您可以稍后再来看看，或者调整搜索关键词，说不定就能遇到心仪的手环啦！想了解哪件商品详情可以随时问我哦～', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 14:01:16');
INSERT INTO `ai_chat_messages` VALUES (165, 45, 'user', '推荐一个智能手环', 'text', NULL, '2025-09-08 14:02:20');
INSERT INTO `ai_chat_messages` VALUES (166, 45, 'assistant', '目前没有找到匹配的商品，建议您：1）尝试不同的关键词 2）调整价格范围 3）选择相关商品类别，或者告诉我您更详细的需求。', 'text', '{\"recommended_items\": []}', '2025-09-08 14:02:27');
INSERT INTO `ai_chat_messages` VALUES (167, 47, 'user', '帮我推荐一个充电宝', 'text', NULL, '2025-09-08 14:02:53');
INSERT INTO `ai_chat_messages` VALUES (168, 47, 'assistant', '太棒了！找到了您需要的充电宝！🔋\n\n强烈推荐这款 **小米充电宝 10000mAh**，只要¥80！它支持快充，电量足又便携，上课外出带着都很方便，而且成色很新～ \n\n这款性价比很高，校内转手也很靠谱，建议尽快联系卖家看看哦！还有其他想了解的可以随时问我 😊', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 14:03:07');
INSERT INTO `ai_chat_messages` VALUES (169, 48, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-08 14:05:50');
INSERT INTO `ai_chat_messages` VALUES (170, 48, 'user', '推荐充电宝', 'text', NULL, '2025-09-08 14:05:50');
INSERT INTO `ai_chat_messages` VALUES (171, 48, 'assistant', '找到了充电宝！推荐这款小米充电宝10000mAh，只要¥80。它支持快充，充电速度快，而且很便携，带出门特别方便。成色良好，性价比很高，适合日常使用和外出携带。建议你尽快联系卖家看看实物哦，好货不等人！', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 14:06:02');
INSERT INTO `ai_chat_messages` VALUES (172, 49, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 14:08:56');
INSERT INTO `ai_chat_messages` VALUES (173, 49, 'user', '帮我分析充电宝价格', 'text', NULL, '2025-09-08 14:08:56');
INSERT INTO `ai_chat_messages` VALUES (174, 49, 'assistant', '您好！我查看了当前的二手商品，不过暂时没有找到专门的充电宝呢。目前有几款不错的电子产品在售，比如MacBook Air M1适合学习办公，Switch续航版适合娱乐。如果您需要充电宝，可以调整一下搜索条件，或者稍后再来看看，经常有新品上架哦！有什么其他需求我也可以帮您推荐~ 😊', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 14:09:11');
INSERT INTO `ai_chat_messages` VALUES (175, 50, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 14:10:19');
INSERT INTO `ai_chat_messages` VALUES (176, 51, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 14:10:31');
INSERT INTO `ai_chat_messages` VALUES (177, 52, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 14:10:44');
INSERT INTO `ai_chat_messages` VALUES (178, 53, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 14:11:02');
INSERT INTO `ai_chat_messages` VALUES (179, 54, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-08 14:13:24');
INSERT INTO `ai_chat_messages` VALUES (180, 55, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 14:13:43');
INSERT INTO `ai_chat_messages` VALUES (181, 55, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-08 14:13:56');
INSERT INTO `ai_chat_messages` VALUES (182, 55, 'assistant', '找到了充电宝！推荐这款小米充电宝10000mAh，只要¥80。它支持快充，充电速度快，而且体积小巧便携，上课外出带着都很方便。成色良好，性价比很高，适合学生日常使用。建议尽快联系卖家，好货不等人哦！需要的话我可以帮你看看更多细节～', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-08 14:14:10');
INSERT INTO `ai_chat_messages` VALUES (183, 56, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 14:45:21');
INSERT INTO `ai_chat_messages` VALUES (184, 57, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-08 14:47:57');
INSERT INTO `ai_chat_messages` VALUES (185, 58, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-08 15:11:50');
INSERT INTO `ai_chat_messages` VALUES (186, 59, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-08 15:13:53');
INSERT INTO `ai_chat_messages` VALUES (187, 59, 'user', '推荐充电宝', 'text', NULL, '2025-09-08 15:14:01');
INSERT INTO `ai_chat_messages` VALUES (188, 59, 'assistant', '您好！我为您找到了几款实用的充电宝选择 🔋\n\n目前商城里有几款不错的移动电源：\n- **测试商品_修改** ¥150：便携设计，适合日常随身携带\n- 还有其他高性价比的数码配件\n\n推荐理由：\n✅ 轻巧便携，上课外出都很方便  \n✅ 性价比高，学生价很实惠  \n✅ 即买即用，省去等待快递时间\n\n建议您点击查看商品详情，了解具体容量和充电速度。校园交易还可以当面验货，确保满意再入手哦！需要看更多细节可以随时问我~', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-08 15:14:18');
INSERT INTO `ai_chat_messages` VALUES (189, 60, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-09 02:20:01');
INSERT INTO `ai_chat_messages` VALUES (190, 60, 'user', '推荐充电宝', 'text', NULL, '2025-09-09 02:20:02');
INSERT INTO `ai_chat_messages` VALUES (191, 60, 'assistant', '太好了！找到了几款实用的充电宝推荐给你 🔋\n\n推荐这款 **15000mAh 快充充电宝**，只要 ¥150！支持双向快充，轻薄便携，上课外出都能用，手机充满电大概只要1小时左右，特别适合学生党日常使用。\n\n选购时记得注意：\n✓ 确认充电接口是否匹配\n✓ 查看电池健康度（循环次数）\n✓ 建议面交时实际测试一下充电效果\n\n想了解更多细节的话，我可以帮你联系卖家查看实物照片哦！', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-09 02:20:18');
INSERT INTO `ai_chat_messages` VALUES (192, 61, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-09 02:20:34');
INSERT INTO `ai_chat_messages` VALUES (193, 61, 'user', '推荐充电宝', 'text', NULL, '2025-09-09 02:20:42');
INSERT INTO `ai_chat_messages` VALUES (194, 61, 'assistant', '您好！虽然目前二手商城的充电宝选择比较少，但我为您找到了几款很不错的电子产品：有高性能的MacBook Air适合学习办公，还有娱乐性强的Switch游戏机。建议您可以稍后再来看看，或者调整搜索条件，说不定很快就有同学发布闲置的充电宝哦！想了解哪件商品详情我可以为您介绍~ 🔋', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-09 02:20:56');
INSERT INTO `ai_chat_messages` VALUES (195, 62, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-09 02:33:08');
INSERT INTO `ai_chat_messages` VALUES (196, 63, 'assistant', '您好！我是您的AI商品推荐助手，专门为您推荐最合适的二手电子产品。请告诉我您想要什么类型的商品，我会为您精心挑选！', 'text', NULL, '2025-09-09 02:47:44');
INSERT INTO `ai_chat_messages` VALUES (197, 64, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-09 02:52:29');
INSERT INTO `ai_chat_messages` VALUES (198, 65, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-09 03:10:15');
INSERT INTO `ai_chat_messages` VALUES (199, 65, 'user', '推荐充电宝', 'text', NULL, '2025-09-09 03:10:15');
INSERT INTO `ai_chat_messages` VALUES (200, 65, 'assistant', '您好！虽然目前二手商城里的充电宝选择还不多，但我为您找到了几款同样很受欢迎的实用数码产品！\n\n比如这款MacBook Air M1，性能强劲又便携，非常适合学生党学习办公；还有Nintendo Switch续航版，学习之余也能放松娱乐。\n\n建议您可以稍后再来看看，或者尝试搜索“移动电源”等关键词，可能会有新发现的充电宝上架哦！想了解哪件商品的详细信息，我随时为您介绍 😊', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-09 03:10:31');
INSERT INTO `ai_chat_messages` VALUES (201, 66, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-09 03:11:32');
INSERT INTO `ai_chat_messages` VALUES (202, 66, 'user', '推荐充电宝', 'text', NULL, '2025-09-09 03:11:44');
INSERT INTO `ai_chat_messages` VALUES (203, 66, 'assistant', '您好！虽然目前二手商城里的充电宝选择还不多，但我为您找到了几款同样很受欢迎的电子产品，说不定您也会感兴趣呢！\n\n比如这款MacBook Air M1，性能强劲又便携，续航也很不错，特别适合学生党。还有性价比很高的Switch游戏机，课余时间放松一下很棒！\n\n建议您可以稍后再来看看，或者调整一下搜索条件，经常会有新宝贝上架哦！想了解哪件的详细信息，我随时为您解答～', 'recommendation', '{\"recommended_items\": [1, 2, 3, 4, 6]}', '2025-09-09 03:11:59');
INSERT INTO `ai_chat_messages` VALUES (204, 67, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-09 08:21:04');
INSERT INTO `ai_chat_messages` VALUES (205, 68, 'assistant', '欢迎使用AI推荐服务！我可以帮您找到心仪的二手商品。无论是学习用品、娱乐设备还是生活用品，我都能为您推荐最合适的选择。', 'text', NULL, '2025-09-09 08:21:11');
INSERT INTO `ai_chat_messages` VALUES (206, 68, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-09 08:21:11');
INSERT INTO `ai_chat_messages` VALUES (207, 68, 'assistant', '找到了充电宝！推荐这款小米充电宝10000mAh，只要¥80。它支持快充，充电速度快，而且10000mAh的容量足够一天外出使用，非常便携实用。成色良好，性价比很高，适合学生日常携带。建议尽快联系卖家，先到先得哦！想了解更多详情可以随时问我~', 'recommendation', '{\"recommended_items\": [4]}', '2025-09-09 08:21:25');
INSERT INTO `ai_chat_messages` VALUES (208, 68, 'user', '推荐一个智能手环', 'text', NULL, '2025-09-09 08:21:48');
INSERT INTO `ai_chat_messages` VALUES (209, 68, 'assistant', '抱歉，没有找到完全符合您要求的商品。您可以尝试调整搜索条件，比如扩大价格范围或选择相关类别，或者告诉我您更具体的需求。', 'text', '{\"recommended_items\": []}', '2025-09-09 08:21:54');
INSERT INTO `ai_chat_messages` VALUES (210, 69, 'assistant', '您好！我是智能推荐助手，了解您的需求后，我会从海量商品中为您推荐最匹配的选择。请告诉我您想要什么吧！', 'text', NULL, '2025-09-09 08:33:56');
INSERT INTO `ai_chat_messages` VALUES (211, 70, 'user', '我想要一个2000-3000元的华为手机', 'text', NULL, '2025-09-09 10:17:25');
INSERT INTO `ai_chat_messages` VALUES (212, 71, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-09 10:18:31');
INSERT INTO `ai_chat_messages` VALUES (213, 71, 'assistant', '嘿同学！🔋 想找充电宝是吧？在校园里确实超实用——上课记笔记、图书馆刷题、社团活动，随时都可能需要应急充电呢！\n\n给你推荐这款 **小米充电宝 10000mAh** ⚡，只要¥80，性价比很高！小米的移动电源口碑一直不错，这款支持快充，充电速度快，特别适合赶课间隙快速补电。10000mAh 的容量大概可以给手机充满2-3次，带去图书馆或外出一天完全够用～而且体积小巧，放书包侧袋完全不占地方。\n\n成色良好，入手很划算！如果你经常外出或课程多，这种中等容量+快充的组合真的很实用。记得选个轻便一点的，平时通勤才不会觉得累赘哦！需要的话尽快联系卖家，好货不等人啦 😉～', 'recommendation', '{\"requirements\": {\"category\": \"生活辅助类\", \"subcategory\": \"便携充电宝\", \"price_range\": null, \"brand\": null, \"features\": null, \"condition\": null, \"other_requirements\": null, \"confidence\": 0.9}, \"products_count\": 1, \"products\": [{\"id\": 4, \"title\": \"小米充电宝 10000mAh\", \"description\": \"小米移动电源3 10000mAh，支持快充，便携实用，成色良好，先到先得\", \"price\": 80.0, \"original_price\": 180.0, \"condition\": \"good\", \"images\": \"[\\\"5_20250904_034620_1_png\\\"]\", \"tags\": null, \"location\": \"学校图书馆门口\", \"contact_method\": \"wechat\", \"contact_info\": \"test_wechat_123\", \"view_count\": 21, \"like_count\": 1, \"created_at\": \"2025-09-03T03:05:02\", \"category_name\": \"便携充电宝\", \"seller_name\": \"test_user\"}]}', '2025-09-09 10:18:50');
INSERT INTO `ai_chat_messages` VALUES (214, 72, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-09 10:21:58');
INSERT INTO `ai_chat_messages` VALUES (215, 73, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-09 10:22:07');
INSERT INTO `ai_chat_messages` VALUES (216, 73, 'assistant', '你好呀！😊 想找一款充电宝是吗？我为你推荐这款 **小米充电宝 10000mAh**，只要 ¥80，成色还很不错哦！\n\n🔋 **推荐理由：**  \n- **大容量 + 快充**：10000mAh 的电量足够给手机充满 2-3 次，还支持快充，课间或图书馆休息时快速回血！  \n- **轻巧便携**：巴掌大小，轻松塞进书包侧袋，上课、自习、外出探店都不占地方～  \n- **小米品质靠谱**：用起来稳定又安全，校园日常使用完全足够！\n\n💡 **使用小贴士：**  \n自习或外出时带着它，再也不担心手机没电失联啦！建议搭配一条快充线，效率更高哦 ✨\n\n如果还需要更大容量或者更小巧的款式，也可以告诉我！', 'recommendation', '{\"requirements\": {\"category\": \"生活辅助类\", \"subcategory\": \"便携充电宝\", \"price_range\": null, \"brand\": null, \"features\": null, \"condition\": null, \"other_requirements\": null, \"confidence\": 0.9}, \"products_count\": 1, \"products\": [{\"id\": 4, \"title\": \"小米充电宝 10000mAh\", \"description\": \"小米移动电源3 10000mAh，支持快充，便携实用，成色良好，先到先得\", \"price\": 80.0, \"original_price\": 180.0, \"condition\": \"good\", \"images\": \"[\\\"5_20250904_034620_1_png\\\"]\", \"tags\": null, \"location\": \"学校图书馆门口\", \"contact_method\": \"wechat\", \"contact_info\": \"test_wechat_123\", \"view_count\": 22, \"like_count\": 1, \"created_at\": \"2025-09-03T03:05:02\", \"category_name\": \"便携充电宝\", \"seller_name\": \"test_user\"}]}', '2025-09-09 10:22:27');
INSERT INTO `ai_chat_messages` VALUES (217, 74, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-09 12:31:36');
INSERT INTO `ai_chat_messages` VALUES (218, 75, 'user', '推荐一个U盘', 'text', NULL, '2025-09-09 12:34:32');
INSERT INTO `ai_chat_messages` VALUES (219, 75, 'assistant', '嘿同学！😊 目前二手平台暂时没有合适的U盘在售，不过别着急，U盘确实是校园生活中超实用的小物件！📚✨ 平时可以用来存课件、交作业、备份资料，特别方便～\n\n如果你急需的话，可以考虑这几个方向：\n1️⃣ **校内超市或数码店**：通常有基础款U盘，价格适中即买即用\n2️⃣ **线上平台急送**：京东/天猫超市有时1小时就能送到校门口\n3️⃣ **问问身边同学**：有时候毕业的学长学姐会出闲置哦\n\n💡 小建议：选U盘可以关注USB3.0以上接口（传输快）、64GB左右容量（课件+视频都够用），金属外壳更耐用！平时记得重要资料多备份一份哈～\n\n需要的话我可以帮你留意，有上新随时通知你！🎯', 'recommendation', '{\"requirements\": {\"category\": \"生活辅助类\", \"subcategory\": \"存储设备\", \"price_range\": null, \"brand\": null, \"features\": null, \"condition\": null, \"other_requirements\": null, \"confidence\": 0.9}, \"products_count\": 0, \"products\": []}', '2025-09-09 12:34:52');
INSERT INTO `ai_chat_messages` VALUES (220, 75, 'user', '推荐一个固态硬盘', 'text', NULL, '2025-09-09 12:36:15');
INSERT INTO `ai_chat_messages` VALUES (221, 75, 'assistant', '哎呀同学，目前二手平台上暂时没有合适的固态硬盘呢 😢 不过别着急，SSD确实是校园学习的神器！💻✨\n\n如果你是想要提升电脑运行速度，可以考虑这几个方向：\n1️⃣ 优先选择M.2接口的固态，读写速度更快，装系统、开软件都会飞起\n2️⃣ 容量建议至少512GB，既能装系统又能存学习资料\n3️⃣ 三星、西部数据、金士顿这些品牌都比较靠谱\n\n最近可以多刷刷校园二手群，毕业季经常有学长学姐出闲置的电脑配件哦～也可以看看【电子配件/耗材】分类下的其他好东西：https://example.com/category/electronics\n\n需要的话我可以帮你留意着，有合适的固态硬盘随时通知你！📲', 'recommendation', '{\"requirements\": {\"category\": \"专业工具类\", \"subcategory\": \"存储设备\", \"price_range\": null, \"brand\": null, \"features\": null, \"condition\": null, \"other_requirements\": null, \"confidence\": 0.9}, \"products_count\": 0, \"products\": []}', '2025-09-09 12:36:33');
INSERT INTO `ai_chat_messages` VALUES (222, 75, 'user', '推荐一个固态硬盘', 'text', NULL, '2025-09-09 12:39:30');
INSERT INTO `ai_chat_messages` VALUES (223, 76, 'user', '推荐一个固态硬盘', 'text', NULL, '2025-09-09 12:41:49');
INSERT INTO `ai_chat_messages` VALUES (224, 77, 'user', '推荐一个固态硬盘', 'text', NULL, '2025-09-09 12:42:38');
INSERT INTO `ai_chat_messages` VALUES (225, 78, 'user', '推荐一个固态硬盘', 'text', NULL, '2025-09-09 12:43:39');
INSERT INTO `ai_chat_messages` VALUES (226, 79, 'user', '我想买一个U盘', 'text', NULL, '2025-09-09 12:43:46');
INSERT INTO `ai_chat_messages` VALUES (227, 80, 'user', '推荐一个固态硬盘', 'text', NULL, '2025-09-09 12:44:06');
INSERT INTO `ai_chat_messages` VALUES (228, 81, 'user', '推荐一个固态硬盘', 'text', NULL, '2025-09-09 12:47:15');
INSERT INTO `ai_chat_messages` VALUES (229, 82, 'user', '推荐一个充电宝', 'text', NULL, '2025-09-09 12:56:55');
INSERT INTO `ai_chat_messages` VALUES (230, 82, 'assistant', '同学你好！😊 为你推荐这款 **小米充电宝 10000mAh**，绝对是校园生活的必备神器！🔋\n\n这款充电宝容量适中，支持快充功能，特别适合日常上课、图书馆自习或者外出时使用。10000mAh 的电量足够给手机充满 2-3 次，轻薄便携，放在书包里完全不占地方。成色良好，性价比超高，只要 **¥80**，真的很划算！\n\n在校园里，不管是赶论文还是刷课，随时都能保持电量满满，再也不用担心手机或平板没电啦～⚡\n\n感兴趣的话可以点击链接查看详情哦：  \nhttp://113.45.53.114:8000/item/4\n\n如果还需要更大容量或者更多功能（比如无线充电），也可以告诉我，我再帮你找找！✨', 'recommendation', '{\"requirements\": {\"category\": \"生活辅助类\", \"subcategory\": \"便携充电宝\", \"price_range\": null, \"brand\": null, \"features\": null, \"condition\": null, \"other_requirements\": null, \"confidence\": 0.9}, \"products_count\": 1, \"products\": [{\"id\": 4, \"title\": \"小米充电宝 10000mAh\", \"description\": \"小米移动电源3 10000mAh，支持快充，便携实用，成色良好，先到先得\", \"price\": 80.0, \"original_price\": 180.0, \"condition\": \"good\", \"images\": \"[\\\"5_20250904_034620_1_png\\\"]\", \"tags\": null, \"location\": \"学校图书馆门口\", \"contact_method\": \"wechat\", \"contact_info\": \"test_wechat_123\", \"view_count\": 22, \"like_count\": 1, \"created_at\": \"2025-09-03T03:05:02\", \"category_name\": \"便携充电宝\", \"seller_name\": \"test_user\"}]}', '2025-09-09 12:57:15');
INSERT INTO `ai_chat_messages` VALUES (231, 83, 'user', '推荐一个智能手环', 'text', NULL, '2025-09-09 13:06:24');
INSERT INTO `ai_chat_messages` VALUES (232, 83, 'assistant', '嘿同学！👋 想找一款智能手环的话，我强烈推荐这款 **小米手环9Pro**，特别适合校园生活使用哦～✨\n\n这款手环属于生活辅助类，银色外观非常时尚百搭，不管是上课、运动还是日常佩戴都很合适。它支持高精度运动监测、睡眠呼吸监测、心率和血氧检测，特别适合经常熬夜赶作业或者喜欢运动的你！😴🏃‍♂️ 灵敏度高、操作简单，表盘还可以自定义，超级实用。\n\n成色良好，只要¥300，性价比很高！小米的品质也很可靠，适合学生党入手。课间记录步数、晚上监测睡眠，甚至考试周帮你关注健康状态都很方便～ \n\n感兴趣的话可以看看详情：  \n👉 http://113.45.53.114:8000/item/6\n\n如果还想看看其他品牌或者更多功能（比如GPS或防水更强），也可以告诉我哟！', 'recommendation', '{\"requirements\": {\"category\": \"生活辅助类\", \"subcategory\": \"智能手环\", \"price_range\": null, \"brand\": null, \"features\": [], \"condition\": null, \"other_requirements\": null, \"confidence\": 0.9}, \"products_count\": 1, \"products\": [{\"id\": 6, \"title\": \"小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环\", \"description\": \"灵敏度：很灵敏，抬手即亮\\r\\n准确性：一点不差\\r\\n操作难易：简单易用，表盘百变\\r\\n做工质量：细腻丝滑\\r\\n外形外观：非常漂亮，美观大方\\r\\n其他特色：表带比以前有了很大的改进，结实可靠，再也不用担心丢掉了\", \"price\": 300.0, \"original_price\": null, \"condition\": \"good\", \"images\": \"[\\\"1_20250905_083411_1_Snipaste_2025-09-05_16-30-12.png\\\", \\\"1_20250905_083411_2_Snipaste_2025-09-05_16-31-40.png\\\", \\\"1_20250905_083411_3_Snipaste_2025-09-05_16-30-34.png\\\", \\\"1_20250905_083411_4_Snipaste_2025-09-05_16-30-56.png\\\", \\\"1_20250905_083411_5_Snipaste_2025-09-05_16-31-06.png\\\"]\", \"tags\": null, \"location\": \"学校图书馆门口\", \"contact_method\": \"message\", \"contact_info\": \"\", \"view_count\": 16, \"like_count\": 1, \"created_at\": \"2025-09-05T08:34:11\", \"category_name\": \"手机及周边\", \"seller_name\": \"admin\"}]}', '2025-09-09 13:06:46');
INSERT INTO `ai_chat_messages` VALUES (233, 84, 'user', '推荐一个U盘', 'text', NULL, '2025-09-09 13:12:30');
INSERT INTO `ai_chat_messages` VALUES (234, 84, 'assistant', '嘿同学！👋 想找U盘的话，我帮你看了下，目前校园二手平台上有这款很不错的——**金士顿DTX U盘**（16G）✨！虽然是生活辅助类的小物件，但在校园里真的超级实用～\n\n这款U盘是USB 3.2接口的，传输速度很快📂，拷贝课件、交作业或者存复习资料都很方便。伸缩设计不怕丢盖子，体积小巧适合随身带，上课、去图书馆都不用担心占地方。重点是全新成色+品牌保修，用着更省心～价格只要¥45，性价比很高！\n\n🔗 商品详情：http://113.45.53.114:8000/item/10\n\n💡 小建议：如果你经常存大文件（比如视频或设计素材），也可以考虑加点预算买更大容量的～平时记得定期备份数据哦，校园网盘+U盘双保险更安全！需要其他类型的存储设备（比如移动硬盘）也可以告诉我，我再帮你找找～ 😊', 'recommendation', '{\"requirements\": {\"category\": \"生活辅助类\", \"subcategory\": \"存储设备\", \"price_range\": null, \"brand\": null, \"features\": null, \"condition\": null, \"other_requirements\": null, \"confidence\": 0.9}, \"products_count\": 3, \"products\": [{\"id\": 11, \"title\": \"三星（SAMSUNG）1TB SSD固态硬盘 M.2接口(NVMe协议PCIe4.0*4/5.0*2)读速7150MB/S 990 EVO Plus\", \"description\": \"非常不错，拿到之后就给笔记本升级了硬盘，速度很快，三星大厂颗粒值得信赖，最好的是这个无缓，发热量很低，很适合笔记本加装，而且是单面颗粒，拿来做数据盘非常好，寿命也长，推荐\", \"price\": 600.0, \"original_price\": null, \"condition\": \"new\", \"images\": \"[\\\"1_20250908_134630_1_Snipaste_2025-09-08_21-42-29.png\\\", \\\"1_20250908_134630_2_Snipaste_2025-09-08_21-43-01.png\\\", \\\"1_20250908_134630_3_Snipaste_2025-09-08_21-43-22.png\\\", \\\"1_20250908_134630_4_Snipaste_2025-09-08_21-44-02.png\\\", \\\"1_20250908_134630_5_Snipaste_2025-09-08_21-44-28.png\\\"]\", \"tags\": null, \"location\": \"学校图书馆门口\", \"contact_method\": \"message\", \"contact_info\": \"\", \"view_count\": 1, \"like_count\": 0, \"created_at\": \"2025-09-08T13:46:31\", \"category_name\": \"台式机及配件\", \"seller_name\": \"admin\"}, {\"id\": 10, \"title\": \"金士顿（Kingston） u盘 商务办公U盘 定制刻字 高速USB3.2 DTX 投标车载优盘 16G\", \"description\": \"品质有保修，买的还是用伸缩式的，盖子不会丢，材质很好，小巧但插拔很方便，试了一下，数据传输很快。\", \"price\": 45.0, \"original_price\": null, \"condition\": \"new\", \"images\": \"[\\\"1_20250908_133826_1_Snipaste_2025-09-08_21-35-13.png\\\", \\\"1_20250908_133826_2_Snipaste_2025-09-08_21-35-29.png\\\", \\\"1_20250908_133826_3_Snipaste_2025-09-08_21-35-47.png\\\", \\\"1_20250908_133826_4_Snipaste_2025-09-08_21-36-17.png\\\", \\\"1_20250908_133826_5_Snipaste_2025-09-08_21-36-43.png\\\"]\", \"tags\": null, \"location\": \"学校图书馆门口\", \"contact_method\": \"message\", \"contact_info\": \"\", \"view_count\": 1, \"like_count\": 0, \"created_at\": \"2025-09-08T13:38:26\", \"category_name\": \"台式机及配件\", \"seller_name\": \"admin\"}, {\"id\": 1, \"title\": \"MacBook Air M1 8GB+256GB\", \"description\": \"2020款MacBook Air，M1芯片，8GB内存，256GB存储，成色良好，适合学习办公\", \"price\": 4500.0, \"original_price\": 4200.0, \"condition\": \"good\", \"images\": \"[\\\"5_20250904_043815_1_MacBook_Air_M1_8GB256GB.png\\\"]\", \"tags\": null, \"location\": \"学校图书馆门口\", \"contact_method\": \"wechat\", \"contact_info\": \"test_wechat_123\", \"view_count\": 4, \"like_count\": 1, \"created_at\": \"2025-09-03T03:05:02\", \"category_name\": \"笔记本电脑\", \"seller_name\": \"test_user\"}]}', '2025-09-09 13:12:51');
INSERT INTO `ai_chat_messages` VALUES (235, 84, 'user', '推荐一个智能手环', 'text', NULL, '2025-09-09 13:13:45');
INSERT INTO `ai_chat_messages` VALUES (236, 84, 'assistant', 'Hey同学！👋 想找一款智能手环的话，我强烈推荐这款 **小米手环9Pro**，特别适合咱们校园党日常使用～✨\n\n它属于生活辅助类，主打高精度健康监测和实用功能，银色外观简约又百搭📱。灵敏度超高，抬手就亮屏；续航也很顶，上课、跑步、自习都不用总充电。特别实用的是睡眠呼吸监测和心率血氧检测功能——熬夜复习或者体测前后，随时关注自己的身体状态，健康学习两不误💤🏃。\n\n成色良好，只要300元，性价比真的很高！小米手环的表带这次也升级了，更牢固不容易丢，适合经常在教室、操场、宿舍之间穿梭的你。课间换一个表盘风格，还能小小个性一下😎。\n\n感兴趣的话可以看看详情：  \n🔗 http://113.45.53.114:8000/item/6\n\n如果还想要更多选择，也可以告诉我偏好功能或者预算，我再帮你找找看哦！', 'recommendation', '{\"requirements\": {\"category\": \"生活辅助类\", \"subcategory\": \"智能手环\", \"price_range\": null, \"brand\": null, \"features\": null, \"condition\": null, \"other_requirements\": null, \"confidence\": 0.9}, \"products_count\": 1, \"products\": [{\"id\": 6, \"title\": \"小米（MI）手环9Pro银色 智能手环 高精度运动健康 睡眠呼吸暂停监测 心率血氧监测运动手环\", \"description\": \"灵敏度：很灵敏，抬手即亮\\r\\n准确性：一点不差\\r\\n操作难易：简单易用，表盘百变\\r\\n做工质量：细腻丝滑\\r\\n外形外观：非常漂亮，美观大方\\r\\n其他特色：表带比以前有了很大的改进，结实可靠，再也不用担心丢掉了\", \"price\": 300.0, \"original_price\": null, \"condition\": \"good\", \"images\": \"[\\\"1_20250905_083411_1_Snipaste_2025-09-05_16-30-12.png\\\", \\\"1_20250905_083411_2_Snipaste_2025-09-05_16-31-40.png\\\", \\\"1_20250905_083411_3_Snipaste_2025-09-05_16-30-34.png\\\", \\\"1_20250905_083411_4_Snipaste_2025-09-05_16-30-56.png\\\", \\\"1_20250905_083411_5_Snipaste_2025-09-05_16-31-06.png\\\"]\", \"tags\": null, \"location\": \"学校图书馆门口\", \"contact_method\": \"message\", \"contact_info\": \"\", \"view_count\": 16, \"like_count\": 1, \"created_at\": \"2025-09-05T08:34:11\", \"category_name\": \"手机及周边\", \"seller_name\": \"admin\"}]}', '2025-09-09 13:14:07');

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
) ENGINE = InnoDB AUTO_INCREMENT = 85 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ai_chat_sessions
-- ----------------------------
INSERT INTO `ai_chat_sessions` VALUES (1, 1, 'test_session_123', NULL, 'active', '2025-09-06 16:45:29', '2025-09-06 16:49:55', '2025-09-06 16:49:55');
INSERT INTO `ai_chat_sessions` VALUES (2, 1, 'debug_session_123', NULL, 'active', '2025-09-06 16:46:46', '2025-09-06 16:46:46', NULL);
INSERT INTO `ai_chat_sessions` VALUES (3, 1, 'final_test_session', NULL, 'active', '2025-09-06 16:51:41', '2025-09-06 16:51:42', '2025-09-06 16:51:42');
INSERT INTO `ai_chat_sessions` VALUES (4, 1, '8be1a996-76ca-4381-9654-54e74129220a', 'AI商品推荐助手', 'active', '2025-09-07 06:43:12', '2025-09-07 06:43:12', NULL);
INSERT INTO `ai_chat_sessions` VALUES (5, 1, '075c92c2-1d4e-49d8-9d28-7493d63de4e6', 'AI商品推荐助手', 'active', '2025-09-07 06:43:53', '2025-09-07 06:43:54', '2025-09-07 06:43:54');
INSERT INTO `ai_chat_sessions` VALUES (6, 1, '394613d7-a2ca-44fd-ba32-e663e6b894c3', 'AI商品推荐助手', 'active', '2025-09-07 06:50:27', '2025-09-07 06:50:27', '2025-09-07 06:50:27');
INSERT INTO `ai_chat_sessions` VALUES (7, 1, '305bd459-c021-47a8-89d6-b3fac3fe0f7a', 'AI商品推荐助手', 'active', '2025-09-07 06:50:27', '2025-09-07 06:50:28', '2025-09-07 06:50:28');
INSERT INTO `ai_chat_sessions` VALUES (8, 1, '9803010b-088f-4c5f-aab6-6b2c82a5fdfe', 'AI商品推荐助手', 'active', '2025-09-07 06:50:28', '2025-09-07 06:50:28', '2025-09-07 06:50:28');
INSERT INTO `ai_chat_sessions` VALUES (9, 1, 'bd886072-22ef-47d8-b95f-378759f92376', 'AI商品推荐助手', 'active', '2025-09-07 06:50:28', '2025-09-07 06:50:28', '2025-09-07 06:50:28');
INSERT INTO `ai_chat_sessions` VALUES (10, 1, '6a72ffc6-9cf5-4b20-b8b5-d8152cd37e70', 'AI商品推荐助手', 'active', '2025-09-07 06:50:28', '2025-09-07 06:50:28', '2025-09-07 06:50:28');
INSERT INTO `ai_chat_sessions` VALUES (11, 1, '5d98605b-2ac6-4fdc-ace6-767f2d403eb6', 'AI商品推荐助手', 'active', '2025-09-08 06:00:55', '2025-09-08 06:00:55', NULL);
INSERT INTO `ai_chat_sessions` VALUES (12, 1, '91956385-ff40-4a2b-9cc6-3863926249b2', 'AI商品推荐助手', 'active', '2025-09-08 06:22:57', '2025-09-08 06:22:57', NULL);
INSERT INTO `ai_chat_sessions` VALUES (13, 1, '79eb490b-8acc-4d46-820f-3bd705ad4bfb', 'AI商品推荐助手', 'active', '2025-09-08 06:24:23', '2025-09-08 06:24:23', NULL);
INSERT INTO `ai_chat_sessions` VALUES (14, 1, '09b32faa-3f5a-4ae8-a084-165e8708efd7', 'AI商品推荐助手', 'active', '2025-09-08 06:25:41', '2025-09-08 06:25:41', NULL);
INSERT INTO `ai_chat_sessions` VALUES (15, 1, '7169d46c-e16d-4784-aac3-8554baf75dc6', 'AI商品推荐助手', 'active', '2025-09-08 06:27:05', '2025-09-08 06:27:05', NULL);
INSERT INTO `ai_chat_sessions` VALUES (16, 1, 'fded38e4-36d1-4b5f-b404-747c06a42e66', 'AI商品推荐助手', 'active', '2025-09-08 06:28:46', '2025-09-08 06:29:14', '2025-09-08 06:29:14');
INSERT INTO `ai_chat_sessions` VALUES (17, 1, '5cfbd095-6690-4f93-bfeb-bfd0486872ac', 'AI商品推荐助手', 'active', '2025-09-08 06:29:49', '2025-09-08 06:29:49', NULL);
INSERT INTO `ai_chat_sessions` VALUES (18, 1, '4ada893e-9899-4920-8f5c-a58eac503fb5', 'AI商品推荐助手', 'active', '2025-09-08 06:30:45', '2025-09-08 06:30:45', NULL);
INSERT INTO `ai_chat_sessions` VALUES (19, 1, 'e7df796e-dd86-43be-9236-05fcb95e1f83', 'AI商品推荐助手', 'active', '2025-09-08 06:33:29', '2025-09-08 06:33:29', NULL);
INSERT INTO `ai_chat_sessions` VALUES (20, 1, '7ab05c3e-910b-4d7e-88df-03d204d61c4d', 'AI商品推荐助手', 'active', '2025-09-08 06:34:39', '2025-09-08 06:34:39', NULL);
INSERT INTO `ai_chat_sessions` VALUES (21, 1, '30fe6e44-bd61-416e-81a9-50f726dd08bf', 'AI商品推荐助手', 'active', '2025-09-08 06:36:21', '2025-09-08 06:36:21', NULL);
INSERT INTO `ai_chat_sessions` VALUES (22, 1, '624b25cf-828b-4494-8f26-896cb430e1ac', 'AI商品推荐助手', 'active', '2025-09-08 06:37:13', '2025-09-08 06:37:13', NULL);
INSERT INTO `ai_chat_sessions` VALUES (23, 1, 'ffe7c2ba-3b24-4062-906b-63e227cbd09a', 'AI商品推荐助手', 'active', '2025-09-08 06:39:19', '2025-09-08 06:39:19', NULL);
INSERT INTO `ai_chat_sessions` VALUES (24, 1, '64974c26-937e-423d-8b5f-a33cfa6536e1', 'AI商品推荐助手', 'active', '2025-09-08 06:42:26', '2025-09-08 06:42:53', '2025-09-08 06:42:53');
INSERT INTO `ai_chat_sessions` VALUES (25, 1, 'f4ee5ff3-49aa-4dff-9c35-eba59a174bf8', 'AI商品推荐助手', 'active', '2025-09-08 06:46:57', '2025-09-08 06:46:57', NULL);
INSERT INTO `ai_chat_sessions` VALUES (26, 1, '147675d3-a1a7-41de-a236-5b0c277842c0', 'AI商品推荐助手', 'active', '2025-09-08 06:58:38', '2025-09-08 06:59:03', '2025-09-08 06:59:03');
INSERT INTO `ai_chat_sessions` VALUES (27, 1, 'f984d480-92bb-45ea-b1da-b60950ac6737', 'AI商品推荐助手', 'active', '2025-09-08 07:04:45', '2025-09-08 07:05:36', '2025-09-08 07:05:36');
INSERT INTO `ai_chat_sessions` VALUES (28, 1, '26e6fd27-f0f1-4aba-b34c-3b0775c429e8', 'AI商品推荐助手', 'active', '2025-09-08 07:41:42', '2025-09-08 07:42:25', '2025-09-08 07:42:25');
INSERT INTO `ai_chat_sessions` VALUES (29, 1, '64da9333-3bea-42cb-8eb0-c3b93f122e99', 'AI商品推荐助手', 'active', '2025-09-08 07:42:37', '2025-09-08 07:42:51', '2025-09-08 07:42:51');
INSERT INTO `ai_chat_sessions` VALUES (30, 1, 'c51b9c8d-a6f6-4229-91c4-e5c93f378a3d', 'AI商品推荐助手', 'active', '2025-09-08 08:02:22', '2025-09-08 08:02:22', NULL);
INSERT INTO `ai_chat_sessions` VALUES (31, 1, '69bdec33-0954-41fa-b778-d139eb4ea138', 'AI商品推荐助手', 'active', '2025-09-08 08:03:49', '2025-09-08 08:04:33', '2025-09-08 08:04:33');
INSERT INTO `ai_chat_sessions` VALUES (32, 1, '717cfaa2-dbfa-463e-9215-99cef15bd1c9', 'AI商品推荐助手', 'active', '2025-09-08 08:08:03', '2025-09-08 08:08:03', NULL);
INSERT INTO `ai_chat_sessions` VALUES (33, 1, '73bcfe83-3e83-4363-b838-a09c56f580cc', 'AI商品推荐助手', 'active', '2025-09-08 08:08:26', '2025-09-08 08:08:40', '2025-09-08 08:08:40');
INSERT INTO `ai_chat_sessions` VALUES (34, 1, '2395dc88-2ffd-4234-b179-bb0ff50a68c2', 'AI商品推荐助手', 'active', '2025-09-08 08:09:17', '2025-09-08 08:09:37', '2025-09-08 08:09:37');
INSERT INTO `ai_chat_sessions` VALUES (35, 1, '250aad98-5934-4a53-bfa2-b64ef4631c18', 'AI商品推荐助手', 'active', '2025-09-08 08:39:06', '2025-09-08 08:39:06', NULL);
INSERT INTO `ai_chat_sessions` VALUES (36, 1, '3dcfda9c-861f-42a9-a0ff-c5807cacb976', 'AI商品推荐助手', 'active', '2025-09-08 09:55:33', '2025-09-08 10:02:45', '2025-09-08 10:02:45');
INSERT INTO `ai_chat_sessions` VALUES (37, 1, 'd272826c-d369-4d80-9124-0ffb0ad7f32a', 'AI商品推荐助手', 'active', '2025-09-08 10:11:08', '2025-09-08 10:11:22', '2025-09-08 10:11:22');
INSERT INTO `ai_chat_sessions` VALUES (38, 1, '3b7a8f1d-f15d-48b5-bc4e-2be7da46295a', 'AI商品推荐助手', 'active', '2025-09-08 10:12:20', '2025-09-08 10:12:33', '2025-09-08 10:12:33');
INSERT INTO `ai_chat_sessions` VALUES (39, 1, 'ab7b46e7-dc83-473c-adea-06ceeec7f479', 'AI商品推荐助手', 'active', '2025-09-08 12:11:00', '2025-09-08 12:11:16', '2025-09-08 12:11:16');
INSERT INTO `ai_chat_sessions` VALUES (40, 1, '70cf036c-3f43-4cb0-9c86-fe17f5bdc320', 'AI商品推荐助手', 'active', '2025-09-08 12:29:43', '2025-09-08 12:29:58', '2025-09-08 12:29:58');
INSERT INTO `ai_chat_sessions` VALUES (41, 1, 'f62db017-4463-47bb-883b-eb5f77d63835', 'AI商品推荐助手', 'active', '2025-09-08 12:33:01', '2025-09-08 12:33:14', '2025-09-08 12:33:14');
INSERT INTO `ai_chat_sessions` VALUES (42, 1, 'e7f2e0e4-7da6-486f-91b0-144e36f3585d', 'AI商品推荐助手', 'active', '2025-09-08 13:05:24', '2025-09-08 13:05:41', '2025-09-08 13:05:41');
INSERT INTO `ai_chat_sessions` VALUES (43, 1, 'd0144ffb-76aa-429c-8fb4-0e0b0248f23b', 'AI商品推荐助手', 'active', '2025-09-08 13:13:42', '2025-09-08 13:14:37', '2025-09-08 13:14:37');
INSERT INTO `ai_chat_sessions` VALUES (44, 1, '84b9a1cd-7e62-4e49-a42f-19fe3c82d313', 'AI商品推荐助手', 'active', '2025-09-08 13:56:16', '2025-09-08 13:58:40', '2025-09-08 13:58:40');
INSERT INTO `ai_chat_sessions` VALUES (45, 1, '7caf9db8-22c7-4a0c-aaec-a05810d8ec6c', 'AI商品推荐助手', 'active', '2025-09-08 13:59:40', '2025-09-08 14:02:27', '2025-09-08 14:02:27');
INSERT INTO `ai_chat_sessions` VALUES (46, 1, '1848ca33-2efa-4801-a0ec-51d33f8d44dd', 'AI商品推荐助手', 'active', '2025-09-08 14:00:11', '2025-09-08 14:00:11', NULL);
INSERT INTO `ai_chat_sessions` VALUES (47, 1, 'e824ad6a-306e-4feb-83f7-eee380597f72', 'AI商品推荐助手', 'active', '2025-09-08 14:00:52', '2025-09-08 14:03:07', '2025-09-08 14:03:07');
INSERT INTO `ai_chat_sessions` VALUES (48, 1, '038fac0d-82bb-4a0c-ace5-7215ef3b7e23', 'AI商品推荐助手', 'active', '2025-09-08 14:05:50', '2025-09-08 14:06:02', '2025-09-08 14:06:02');
INSERT INTO `ai_chat_sessions` VALUES (49, 1, 'cfeda349-5f1f-4b1a-bcb7-747402f975f7', 'AI商品推荐助手', 'active', '2025-09-08 14:08:56', '2025-09-08 14:09:11', '2025-09-08 14:09:11');
INSERT INTO `ai_chat_sessions` VALUES (50, 1, '43caf9c3-dbaf-4e43-9d27-72ad51cc7382', 'AI商品推荐助手', 'active', '2025-09-08 14:10:19', '2025-09-08 14:10:19', NULL);
INSERT INTO `ai_chat_sessions` VALUES (51, 1, 'ba621bd3-bcc4-400b-9b00-ed9f7fc03a17', 'AI商品推荐助手', 'active', '2025-09-08 14:10:31', '2025-09-08 14:10:31', NULL);
INSERT INTO `ai_chat_sessions` VALUES (52, 1, 'c5291efc-4213-40b7-a11c-69671baac206', 'AI商品推荐助手', 'active', '2025-09-08 14:10:44', '2025-09-08 14:10:44', NULL);
INSERT INTO `ai_chat_sessions` VALUES (53, 1, '763a2a76-3412-4d0a-83d0-c8c928b6ebe7', 'AI商品推荐助手', 'active', '2025-09-08 14:11:02', '2025-09-08 14:11:02', NULL);
INSERT INTO `ai_chat_sessions` VALUES (54, 1, '694581d0-0e93-4289-8d11-3de3400937aa', 'AI商品推荐助手', 'active', '2025-09-08 14:13:24', '2025-09-08 14:13:24', NULL);
INSERT INTO `ai_chat_sessions` VALUES (55, 1, '21f8b91b-5888-48df-9866-a6879a9f05af', 'AI商品推荐助手', 'active', '2025-09-08 14:13:43', '2025-09-08 14:14:10', '2025-09-08 14:14:10');
INSERT INTO `ai_chat_sessions` VALUES (56, 1, 'b958cfe7-cc9f-4ac7-9110-c15b2e36fd0a', 'AI商品推荐助手', 'active', '2025-09-08 14:45:21', '2025-09-08 14:45:21', NULL);
INSERT INTO `ai_chat_sessions` VALUES (57, 1, '267aed32-1a4e-42ef-93c2-9e3798c61eee', 'AI商品推荐助手', 'active', '2025-09-08 14:47:57', '2025-09-08 14:47:57', NULL);
INSERT INTO `ai_chat_sessions` VALUES (58, 1, 'dcdfa62e-9b66-46db-94e4-a6f8d69c0cba', 'AI商品推荐助手', 'active', '2025-09-08 15:11:50', '2025-09-08 15:11:50', NULL);
INSERT INTO `ai_chat_sessions` VALUES (59, 1, 'c9d17ad8-9ead-4c98-ac8a-b495497b65a1', 'AI商品推荐助手', 'active', '2025-09-08 15:13:53', '2025-09-08 15:14:18', '2025-09-08 15:14:18');
INSERT INTO `ai_chat_sessions` VALUES (60, 1, '9ea83507-5555-423f-8f1c-bb6a01599e4c', 'AI商品推荐助手', 'active', '2025-09-09 02:20:01', '2025-09-09 02:20:18', '2025-09-09 02:20:18');
INSERT INTO `ai_chat_sessions` VALUES (61, 1, '343c0d1b-f024-4945-ab87-c6d59b97e4ea', 'AI商品推荐助手', 'active', '2025-09-09 02:20:34', '2025-09-09 02:20:56', '2025-09-09 02:20:56');
INSERT INTO `ai_chat_sessions` VALUES (62, 1, '3ccf8578-91fc-43f9-b5c1-7eefc2be3c30', 'AI商品推荐助手', 'active', '2025-09-09 02:33:08', '2025-09-09 02:33:08', NULL);
INSERT INTO `ai_chat_sessions` VALUES (63, 1, '8fefa8b6-d064-4189-a545-3e136ecf3801', 'AI商品推荐助手', 'active', '2025-09-09 02:47:44', '2025-09-09 02:47:44', NULL);
INSERT INTO `ai_chat_sessions` VALUES (64, 1, 'ff7fa435-37cc-48dc-992f-d6170b3df00f', 'AI商品推荐助手', 'active', '2025-09-09 02:52:29', '2025-09-09 02:52:29', NULL);
INSERT INTO `ai_chat_sessions` VALUES (65, 1, 'ce9618e8-5060-45d6-b60e-fc00ba6796fc', 'AI商品推荐助手', 'active', '2025-09-09 03:10:15', '2025-09-09 03:10:31', '2025-09-09 03:10:31');
INSERT INTO `ai_chat_sessions` VALUES (66, 1, '46fe1fa8-7c7e-4284-8147-8ebc46d57c78', 'AI商品推荐助手', 'active', '2025-09-09 03:11:32', '2025-09-09 03:11:59', '2025-09-09 03:11:59');
INSERT INTO `ai_chat_sessions` VALUES (67, 1, '68439abe-cb26-4ea9-ac43-61623ac51bea', 'AI商品推荐助手', 'active', '2025-09-09 08:21:04', '2025-09-09 08:21:04', NULL);
INSERT INTO `ai_chat_sessions` VALUES (68, 1, '28dfffb3-0864-4b05-b73a-0597d672b9ff', 'AI商品推荐助手', 'active', '2025-09-09 08:21:11', '2025-09-09 08:21:54', '2025-09-09 08:21:54');
INSERT INTO `ai_chat_sessions` VALUES (69, 1, 'ca658011-9fd9-492d-93d8-b069953eb3ef', 'AI商品推荐助手', 'active', '2025-09-09 08:33:56', '2025-09-09 08:33:56', NULL);
INSERT INTO `ai_chat_sessions` VALUES (70, 1, 'f2a272d1-532f-4cd9-a15f-a6460d01ea64', '新对话', 'active', '2025-09-09 10:17:25', '2025-09-09 10:17:25', '2025-09-09 10:17:25');
INSERT INTO `ai_chat_sessions` VALUES (71, 1, 'a5cdf149-c22b-4a17-94e4-ff263b52d5ed', '新对话', 'active', '2025-09-09 10:18:31', '2025-09-09 10:18:50', '2025-09-09 10:18:50');
INSERT INTO `ai_chat_sessions` VALUES (72, 1, '4a2a2e67-11b4-4f17-b4da-176708f0716b', '新对话', 'active', '2025-09-09 10:21:58', '2025-09-09 10:21:58', '2025-09-09 10:21:58');
INSERT INTO `ai_chat_sessions` VALUES (73, 1, '365a725b-7fc5-4907-931c-91ccbcca0ddf', '新对话', 'active', '2025-09-09 10:22:07', '2025-09-09 10:22:27', '2025-09-09 10:22:27');
INSERT INTO `ai_chat_sessions` VALUES (74, 1, '652afcda-2cdb-43aa-9bee-6f5cc242b23a', '新对话', 'active', '2025-09-09 12:31:36', '2025-09-09 12:31:36', '2025-09-09 12:31:36');
INSERT INTO `ai_chat_sessions` VALUES (75, 1, 'e218e2dc-c354-4ed2-a677-d1f7ef697202', '新对话', 'active', '2025-09-09 12:34:32', '2025-09-09 12:39:30', '2025-09-09 12:39:30');
INSERT INTO `ai_chat_sessions` VALUES (76, 1, '309fdf58-a59b-4918-9b34-0910103da451', '新对话', 'active', '2025-09-09 12:41:49', '2025-09-09 12:41:49', '2025-09-09 12:41:49');
INSERT INTO `ai_chat_sessions` VALUES (77, 1, '7b142fab-e4db-4deb-b76f-fab988743a17', '新对话', 'active', '2025-09-09 12:42:38', '2025-09-09 12:42:38', '2025-09-09 12:42:38');
INSERT INTO `ai_chat_sessions` VALUES (78, 1, '51a0b89d-595e-4195-be7a-9788231d15dc', '新对话', 'active', '2025-09-09 12:43:39', '2025-09-09 12:43:39', '2025-09-09 12:43:39');
INSERT INTO `ai_chat_sessions` VALUES (79, 1, 'b3efb8c4-cd99-4318-8a23-894f546ed055', '新对话', 'active', '2025-09-09 12:43:46', '2025-09-09 12:43:46', '2025-09-09 12:43:46');
INSERT INTO `ai_chat_sessions` VALUES (80, 1, '03c0aeef-17b2-4cc7-8d3a-6dcb0f92f5b6', '新对话', 'active', '2025-09-09 12:44:06', '2025-09-09 12:44:06', '2025-09-09 12:44:06');
INSERT INTO `ai_chat_sessions` VALUES (81, 1, '39981e63-1f4c-4152-9e2b-3dd197f448c8', '新对话', 'active', '2025-09-09 12:47:15', '2025-09-09 12:47:15', '2025-09-09 12:47:15');
INSERT INTO `ai_chat_sessions` VALUES (82, 1, '751132b2-a394-40d0-adc6-d2765fb23a53', '新对话', 'active', '2025-09-09 12:56:55', '2025-09-09 12:57:15', '2025-09-09 12:57:15');
INSERT INTO `ai_chat_sessions` VALUES (83, 1, 'd61e0317-25ba-4aa7-976e-9b838dc42a7f', '新对话', 'active', '2025-09-09 13:06:24', '2025-09-09 13:06:46', '2025-09-09 13:06:46');
INSERT INTO `ai_chat_sessions` VALUES (84, 1, 'c9ca039a-6b27-4069-9eb7-cd8d7e2c9c2d', '新对话', 'active', '2025-09-09 13:12:30', '2025-09-09 13:14:07', '2025-09-09 13:14:07');

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
) ENGINE = InnoDB AUTO_INCREMENT = 200 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ai_recommendations
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of ai_user_preferences
-- ----------------------------
INSERT INTO `ai_user_preferences` VALUES (1, 1, NULL, '[\"推荐一个智能手环\", \"推荐一个固态硬盘\", \"推荐一个U盘\", \"推荐一个充电宝\", {\"query\": \"推荐 充电宝\", \"category\": \"充电宝\", \"timestamp\": \"2025-09-08T12:33:14.344716\"}, {\"query\": \"\", \"category\": null, \"timestamp\": \"2025-09-08T13:05:40.735950\"}, {\"query\": \"充电宝 推荐\", \"category\": \"充电宝\", \"timestamp\": \"2025-09-08T13:13:57.473131\"}, {\"query\": \"\", \"category\": null, \"timestamp\": \"2025-09-08T13:14:37.113966\"}, {\"query\": \"推荐 充电宝\", \"category\": \"充电宝\", \"timestamp\": \"2025-09-08T13:57:26.483530\"}, {\"query\": \"U盘 推荐\", \"category\": \"U盘\", \"timestamp\": \"2025-09-08T13:58:40.228017\"}, {\"query\": \"推荐 充电宝\", \"category\": \"充电宝\", \"timestamp\": \"2025-09-08T14:00:27.462027\"}, {\"query\": \"\", \"category\": null, \"timestamp\": \"2025-09-08T14:01:15.951664\"}, {\"query\": \"推荐 智能手环\", \"category\": \"智能手环\", \"timestamp\": \"2025-09-08T14:02:26.975442\"}, {\"query\": \"充电宝 推荐\", \"category\": \"充电宝\", \"timestamp\": \"2025-09-08T14:03:07.489709\"}, {\"query\": \"充电宝 推荐\", \"category\": \"充电宝\", \"timestamp\": \"2025-09-08T14:06:01.948937\"}, {\"query\": \"\", \"category\": null, \"timestamp\": \"2025-09-08T14:09:10.666942\"}, {\"query\": \"推荐 充电宝\", \"category\": \"充电宝\", \"timestamp\": \"2025-09-08T14:14:09.512837\"}, {\"query\": \"\", \"category\": null, \"timestamp\": \"2025-09-08T15:14:17.589443\"}, {\"query\": \"\", \"category\": null, \"timestamp\": \"2025-09-09T02:20:17.977196\"}, {\"query\": \"\", \"category\": null, \"timestamp\": \"2025-09-09T02:20:55.656206\"}]', '{\"充电宝\": 22, \"手机\": 1, \"U盘\": 1, \"智能手环\": 2, \"生活辅助类\": 7, \"专业工具类\": 1}', NULL, '2025-09-09 13:14:07');

-- ----------------------------
-- Table structure for announcement_reads
-- ----------------------------
DROP TABLE IF EXISTS `announcement_reads`;
CREATE TABLE `announcement_reads`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL COMMENT '用户ID',
  `announcement_id` int NOT NULL COMMENT '公告ID',
  `read_at` datetime NULL DEFAULT NULL COMMENT '阅读时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `unique_user_announcement_read`(`user_id` ASC, `announcement_id` ASC) USING BTREE,
  INDEX `idx_announcement_read_user`(`user_id` ASC) USING BTREE,
  INDEX `idx_announcement_read_time`(`read_at` ASC) USING BTREE,
  INDEX `idx_announcement_read_announcement`(`announcement_id` ASC) USING BTREE,
  CONSTRAINT `announcement_reads_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `announcement_reads_ibfk_2` FOREIGN KEY (`announcement_id`) REFERENCES `announcements` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 15 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of announcement_reads
-- ----------------------------
INSERT INTO `announcement_reads` VALUES (13, 1, 1, '2025-09-15 08:12:29');
INSERT INTO `announcement_reads` VALUES (14, 10, 1, '2025-09-15 08:45:50');

-- ----------------------------
-- Table structure for announcements
-- ----------------------------
DROP TABLE IF EXISTS `announcements`;
CREATE TABLE `announcements`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告标题',
  `content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '公告内容',
  `type` enum('system','maintenance','notice','warning') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '公告类型',
  `priority` enum('low','normal','high','urgent') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '优先级',
  `is_active` tinyint(1) NULL DEFAULT NULL COMMENT '是否启用',
  `is_pinned` tinyint(1) NULL DEFAULT NULL COMMENT '是否置顶',
  `start_time` datetime NULL DEFAULT NULL COMMENT '开始显示时间',
  `end_time` datetime NULL DEFAULT NULL COMMENT '结束显示时间',
  `created_by` int NOT NULL COMMENT '创建者ID',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `target_type` enum('all','buyer','seller','specific') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'all',
  `target_user_ids` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `target_conditions` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL,
  `is_direct_push` tinyint(1) NULL DEFAULT 0,
  `push_sent` tinyint(1) NULL DEFAULT 0,
  `push_sent_at` datetime NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `created_by`(`created_by` ASC) USING BTREE,
  CONSTRAINT `announcements_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of announcements
-- ----------------------------
INSERT INTO `announcements` VALUES (1, '系统试运行公告', '亲爱的同学们：\r\n​		大家好！为了方便同学们高效处理闲置电子产品，实现资源的循环利用，同时为大家提供智能化的交易体验，我们精心打造的校园二手电子产品交易系统即将开启试运行！本系统集成了丰富功能与前沿智能推荐技术，期待能为大家带来便捷、高效、智能的二手交易新体验！\r\n\r\n**一、系统核心功能：**\r\n- 便捷注册登录：邮箱验证码快速注册，设置安全密码，轻松开启二手交易之旅。\r\n- 自由商品发布：简单几步即可上传二手电子产品信息，附上高清图片、详细描述与合理价格，让你的闲置好物快速找到新主人。\r\n- 即时沟通卖家：通过站内聊天功能，随时与卖家沟通商品详情、交易方式等，让交易更顺畅。\r\n\r\n**二、智能推荐体系：**\r\n- Gemini 智能推荐：借助先进的 Gemini 模型，精准分析你的浏览与交易记录，为你推荐最契合需求的商品。\r\n- 系统自带智能推荐：结合大数据与机器学习算法，提供个性化商品推荐。\r\n- 协同过滤推荐：依据相似用户的购买行为，发现你可能感兴趣的商品。\r\n- 内容推荐：基于商品属性与关键词，匹配符合你偏好的电子产品。\r\n- 热门推荐：实时展示当前最受欢迎的热门二手电子产品，不错过任何优质好物。\r\n\r\n**三、试运行安排**\r\n- 时间：2025年09月12日- 2025年12月12日\r\n- 参与方式：连接校园网后访问系统内网地址:http://172.16.0.100:8000\r\n**四、意见反馈**\r\n		在试运行期间，我们非常期待大家分享使用体验。若遇到任何问题，或对系统功能有宝贵建议，欢迎发送邮件至21641685@qq.com。你的每一条反馈都对我们至关重要，将帮助我们进一步优化系统，为大家提供更优质的服务。\r\n​		感谢大家对本系统的支持与信任！让我们携手开启校园智能二手交易新时代，期待你的参与。\r\n\r\n\r\n202202074168\r\n2025年09月12日', 'system', 'normal', 1, 1, '2025-09-12 09:00:00', '2025-11-13 09:26:00', 1, '2025-09-12 09:07:24', '2025-09-15 06:31:15', 'all', NULL, NULL, 0, 0, NULL);

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
) ENGINE = InnoDB AUTO_INCREMENT = 121 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of categories
-- ----------------------------
INSERT INTO `categories` VALUES (1, '学习办公类电子产品', '学生刚需，交易频率最高，直接服务于课堂学习、作业提交、论文写作等核心场景', 'fas fa-laptop', NULL, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (2, '娱乐影音类电子产品', '校园生活高频需求，满足学生课余娱乐、社交分享需求', 'fas fa-music', NULL, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (3, '生活辅助类电子产品', '校园场景刚需，实用性强，覆盖学生宿舍生活、日常出行需求', 'fas fa-home', NULL, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (4, '专业工具类电子产品', '对应特定专业，精准需求，针对细分专业学生', 'fas fa-tools', NULL, 4, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (5, '笔记本电脑', '轻薄本、性能本、二合一笔记本等', 'fas fa-laptop', 1, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (6, '轻薄本', '适合日常办公、文档处理，如MacBook Air、联想小新系列', 'fas fa-laptop', 5, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (7, '性能本', '适合设计、编程、建模，如拯救者、华硕天选', 'fas fa-desktop', 5, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (8, '二合一笔记本', '带触控/手写笔，适合记笔记、绘画，如微软Surface系列', 'fas fa-tablet-alt', 5, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (9, '其他笔记本', '其他品牌和型号的笔记本电脑', 'fas fa-laptop', 5, 4, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (10, '台式机及配件', '整机、显示器、键盘、鼠标等配件', 'fas fa-desktop', 1, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (11, '台式机整机', '入门办公机、游戏主机、设计主机', 'fas fa-desktop', 10, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (12, '显示器', '网课、双屏办公刚需', 'fas fa-tv', 10, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (13, '键盘鼠标', '机械键盘、静音键盘、无线鼠标', 'fas fa-keyboard', 10, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (14, '主机配件', '主机箱、内存条、硬盘等', 'fas fa-microchip', 10, 4, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (15, '平板及学习辅助设备', '平板电脑、电子阅读器等学习辅助设备', 'fas fa-tablet-alt', 1, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (16, '学习平板', '带手写笔，如iPad + Apple Pencil、华为MatePad', 'fas fa-tablet-alt', 15, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (17, '娱乐平板', '无笔，仅用于看视频、轻度办公', 'fas fa-tablet', 15, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (18, '电子阅读器', '如Kindle、掌阅iReader，护眼阅读', 'fas fa-book-open', 15, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (19, '打印扫描设备', '便携打印机、桌面扫描仪等', 'fas fa-print', 1, 4, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (20, '便携打印机', '错题打印机、小型喷墨打印机', 'fas fa-print', 19, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (21, '扫描仪', '桌面扫描仪，扫描笔记、文献', 'fas fa-scanner', 19, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (22, '手机及周边', '智能手机、手机配件等', 'fas fa-mobile-alt', 2, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (23, 'iPhone', '苹果手机系列，校园保有量高', 'fas fa-mobile-alt', 22, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (24, '安卓手机', '华为、小米、OPPO、vivo等', 'fas fa-mobile-alt', 22, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (25, '手机配件', '充电器、数据线、手机壳、保护膜等', 'fas fa-plug', 22, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (26, '蓝牙耳机', '半入耳式、头戴式耳机', 'fas fa-headphones', 22, 4, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (27, '音频设备', '耳机、音箱等音频设备', 'fas fa-headphones', 2, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (28, '头戴式耳机', '降噪耳机，适合图书馆、宿舍学习', 'fas fa-headphones', 27, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (29, '入耳式耳机', '便携耳机，运动、通勤用', 'fas fa-headphones', 27, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (30, '骨传导耳机', '运动防水，适合跑步场景', 'fas fa-headphones', 27, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (31, '音箱', '桌面小音箱、蓝牙音箱', 'fas fa-volume-up', 27, 4, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (32, '游戏设备', '游戏主机、游戏配件等', 'fas fa-gamepad', 2, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (33, 'Switch', '便携游戏主机，宿舍多人联机', 'fas fa-gamepad', 32, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (34, 'PS5/Xbox', '高性能游戏主机', 'fas fa-gamepad', 32, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (35, '游戏配件', '手柄、游戏卡带、方向盘等', 'fas fa-gamepad', 32, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (36, '影像设备', '相机、运动相机等影像设备', 'fas fa-camera', 2, 4, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (37, '卡片机', '便携相机，日常拍照记录', 'fas fa-camera', 36, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (38, '微单/单反', '入门款，适合摄影社团、传媒专业', 'fas fa-camera', 36, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (39, '运动相机', '如GoPro，户外、运动场景拍摄', 'fas fa-video', 36, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (40, '相机配件', '镜头、三脚架、内存卡等', 'fas fa-camera', 36, 4, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (41, '充电储能设备', '充电宝、插线板等充电设备', 'fas fa-battery-full', 3, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (42, '便携充电宝', '1万毫安内，可带上高铁', 'fas fa-battery-half', 41, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (43, '大容量充电宝', '2万毫安以上，宿舍断电应急', 'fas fa-battery-full', 41, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (44, '插线板', '带USB接口、便携迷你款', 'fas fa-plug', 41, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (45, '智能穿戴设备', '智能手表、手环等穿戴设备', 'fas fa-clock', 3, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (46, '智能手表', 'Apple Watch、华为Watch等', 'fas fa-clock', 45, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (47, '智能手环', '小米手环等基础款', 'fas fa-clock', 45, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (48, '运动手环', '续航长、价格低，运动记录', 'fas fa-running', 45, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (49, '其他生活电子', '台灯、小型家电、存储设备等', 'fas fa-lightbulb', 3, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (50, '台灯', '可充电护眼台灯、桌面台灯', 'fas fa-lightbulb', 49, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (51, '小型家电', '加湿器、桌面风扇、电动牙刷等', 'fas fa-home', 49, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (52, '存储设备', 'U盘、移动硬盘等', 'fas fa-hdd', 49, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (53, '设计/创作工具', '数位板、录音笔、投影仪等创作工具', 'fas fa-palette', 4, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (54, '数位板/数位屏', '如Wacom，美术、设计专业绘图刚需', 'fas fa-tablet-alt', 53, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (55, '录音笔', '如索尼、爱国者，新闻、中文专业采访记录', 'fas fa-microphone', 53, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (56, '投影仪', '迷你款，宿舍投墙看电影或小组作业展示', 'fas fa-video', 53, 3, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (57, '电子配件/耗材', '计算器、电池、数据线等配件耗材', 'fas fa-cogs', 4, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (58, '计算器', '科学计算器、金融计算器', 'fas fa-calculator', 57, 1, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (59, '电池', '五号/七号电池，设备通用', 'fas fa-battery-quarter', 57, 2, 1, '2025-09-03 17:41:29');
INSERT INTO `categories` VALUES (60, '数据线/转接头', 'Type-C转HDMI、USB转Type-C等', 'fas fa-plug', 57, 3, 1, '2025-09-03 17:41:29');

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of chat_sessions
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of conversations
-- ----------------------------
INSERT INTO `conversations` VALUES (15, '[1, 5]', 'item_chat', NULL, '2025-09-08 14:45:45', '2025-09-08 14:16:51', '2025-09-10 03:25:05', 1);
INSERT INTO `conversations` VALUES (17, '[1, 10]', 'item_chat', 20, '2025-09-15 08:40:29', '2025-09-15 08:40:29', '2025-09-15 08:40:29', 0);

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
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of item_audits
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of item_image_audits
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of item_profile_audits
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 25 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of items
-- ----------------------------
INSERT INTO `items` VALUES (17, '铠侠（Kioxia）2TB SSD固态硬盘 NVMe M.2接口 EXCERIA PLUS G4 VD10 系列（PCIE5.0*4 读速10000MB/s)', '用来做笔记本的固态硬盘。整体使用下来感觉的确不错，大文件传输速度很稳定，而且发热真的偏低。东芝原装颗粒还是非常值得冲的。', 1000.00, NULL, 10, 1, 'new', '[\"1_20250910_061716_1_Snipaste_2025-09-10_14-15-46.png\", \"1_20250910_061716_2_Snipaste_2025-09-10_14-16-04.png\", \"1_20250910_061716_3_Snipaste_2025-09-10_14-16-36.png\"]', NULL, '学校图书馆门口', 'message', '', 'sold', 'approved', 2, 0, '2025-09-10 06:17:17', '2025-09-15 09:40:44', '2025-09-15 08:41:07');
INSERT INTO `items` VALUES (18, '梵想（FANXIANG）512GB SSD固态硬盘 M.2接口NVMe协议 精选TLC颗粒 一体机台式机笔记本电脑AI PC存储配件 S500Pro', '满足海量存储需求。M.2接口，NVMe协议，PCIe 4.0x4高速读写。', 299.00, NULL, 10, 1, 'new', '[\"1_20250910_061931_1_Snipaste_2025-09-10_14-17-50.png\", \"1_20250910_061931_2_Snipaste_2025-09-10_14-18-04.png\", \"1_20250910_061931_3_Snipaste_2025-09-10_14-18-36.png\"]', NULL, '学校图书馆门口', 'message', '', 'active', 'approved', 3, 1, '2025-09-10 06:19:32', '2025-09-15 09:41:01', NULL);
INSERT INTO `items` VALUES (19, 'Apple/苹果 iPad11英寸 A16芯片2025年款 平板电脑 (128GB WLAN版/学习办公娱乐)银色', '系统超级顺滑，用多久都不卡，操作简单顺手。團颜值高：机身质感一流，手感轻薄，屏幕清晰又护眼。拍照绝了：照片色彩真实，夜 景也超亮，视频防抖很稳。续航不错：一天够用，快充很快，出门不焦虑。', 2699.00, NULL, 15, 1, 'new', '[\"1_20250910_062129_1_Snipaste_2025-09-10_14-20-42.png\", \"1_20250910_062129_2_Snipaste_2025-09-10_14-20-57.png\", \"1_20250910_062129_3_Snipaste_2025-09-10_14-21-07.png\"]', NULL, '学校图书馆门口', 'message', '', 'active', 'approved', 1, 0, '2025-09-10 06:21:30', '2025-09-12 09:44:43', NULL);
INSERT INTO `items` VALUES (20, 'REDMI Pad 2 红米平板电脑', '效果非常好，很清晰，使用时候很流畅，性价比还是很高的', 999.00, NULL, 15, 1, 'new', '[\"1_20250910_062736_1_Snipaste_2025-09-10_14-27-20.png\"]', NULL, '学校图书馆门口', 'message', '', 'sold', 'approved', 18, 1, '2025-09-10 06:27:36', '2025-09-15 09:31:33', '2025-09-15 08:38:48');
INSERT INTO `items` VALUES (21, 'MIUI/小米 Redmi Pad Pro', '流畅好用', 1499.00, NULL, 15, 1, 'new', '[\"1_20250910_062913_1_Snipaste_2025-09-10_14-28-51.png\", \"1_20250910_062913_2_Snipaste_2025-09-10_14-28-45.png\"]', NULL, '学校图书馆门口', 'message', '', 'active', 'approved', 3, 0, '2025-09-10 06:29:14', '2025-09-15 03:37:14', NULL);
INSERT INTO `items` VALUES (22, '华为手环10NFC智能运动手环', '支持遥控自拍 微信支付 计步 健康监测 心率监测  血氧检测 久坐提醒 等', 200.00, NULL, 45, 1, 'new', '[\"1_20250910_063647_1_Snipaste_2025-09-10_14-34-51.png\", \"1_20250910_063647_2_Snipaste_2025-09-10_14-35-18.png\"]', NULL, '学校图书馆门口', 'message', '', 'active', 'approved', 1, 0, '2025-09-10 06:36:48', '2025-09-12 09:45:10', NULL);
INSERT INTO `items` VALUES (23, '狼途（LANGTU）L15星海98键 有线静音键盘 Gasket结构 RGB灯效 人体工学', '按键回弹舒服，久敲不累手。静音效果超惊喜，深夜打字不吵人。简约颜值百搭桌面，性价比直接拉满，学生党和办公族闭眼入，灯光效果丰富。', 66.00, NULL, 10, 1, 'good', '[\"1_20250912_023318_1_Snipaste_2025-09-12_10-32-05.png\", \"1_20250912_023318_2_Snipaste_2025-09-12_10-32-21.png\", \"1_20250912_023318_3_Snipaste_2025-09-12_10-32-28.png\", \"1_20250912_023318_4_Snipaste_2025-09-12_10-32-34.png\"]', NULL, '学校图书馆门口', 'message', '', 'active', 'approved', 0, 0, '2025-09-12 02:33:19', '2025-09-12 02:33:19', NULL);
INSERT INTO `items` VALUES (24, '牧马人K200电竞有线 线机械键盘', '键盘颜色好看不贵，可以调自己喜欢的颜色。手感很舒服。黑轴，没有声音晚上也不吵。', 185.00, NULL, 10, 1, 'like_new', '[\"1_20250912_023729_1_Snipaste_2025-09-12_10-36-24.png\", \"1_20250912_023729_2_Snipaste_2025-09-12_10-36-31.png\", \"1_20250912_023729_3_Snipaste_2025-09-12_10-36-39.png\"]', NULL, '学校图书馆门口', 'message', '', 'active', 'approved', 2, 0, '2025-09-12 02:37:30', '2025-09-12 09:44:22', NULL);

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
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of message_cleanup_logs
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 31 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of message_notifications
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 32 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of messages
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 325 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of recommendations
-- ----------------------------
INSERT INTO `recommendations` VALUES (1, 10, 20, 'collaborative_filtering', 1.53494, '基于相似用户喜好推荐，预测评分: 1.53', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (2, 10, 17, 'collaborative_filtering', 1.2752, '基于相似用户喜好推荐，预测评分: 1.28', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (3, 10, 23, 'collaborative_filtering', 1.2752, '基于相似用户喜好推荐，预测评分: 1.28', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (4, 10, 21, 'collaborative_filtering', 1.23081, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (5, 10, 19, 'collaborative_filtering', 1.18645, '基于相似用户喜好推荐，预测评分: 1.19', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (6, 10, 22, 'collaborative_filtering', 1.17237, '基于相似用户喜好推荐，预测评分: 1.17', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (7, 10, 18, 'collaborative_filtering', 1.16215, '基于相似用户喜好推荐，预测评分: 1.16', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (8, 10, 24, 'collaborative_filtering', 1.12819, '基于相似用户喜好推荐，预测评分: 1.13', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (9, 10, 20, 'hybrid', 0.613976, '混合推荐，综合分数: 0.61', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (10, 10, 17, 'hybrid', 0.510082, '混合推荐，综合分数: 0.51', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (11, 10, 23, 'hybrid', 0.510082, '混合推荐，综合分数: 0.51', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (12, 10, 21, 'hybrid', 0.492323, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (13, 10, 19, 'hybrid', 0.47458, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (14, 10, 22, 'hybrid', 0.468949, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (15, 10, 18, 'hybrid', 0.46486, '混合推荐，综合分数: 0.46', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (16, 10, 24, 'hybrid', 0.451276, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-12 09:48:53', NULL, NULL);
INSERT INTO `recommendations` VALUES (17, 10, 20, 'collaborative_filtering', 1.53494, '基于相似用户喜好推荐，预测评分: 1.53', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (18, 10, 17, 'collaborative_filtering', 1.2752, '基于相似用户喜好推荐，预测评分: 1.28', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (19, 10, 23, 'collaborative_filtering', 1.2752, '基于相似用户喜好推荐，预测评分: 1.28', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (20, 10, 21, 'collaborative_filtering', 1.23081, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (21, 10, 19, 'collaborative_filtering', 1.18645, '基于相似用户喜好推荐，预测评分: 1.19', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (22, 10, 22, 'collaborative_filtering', 1.17237, '基于相似用户喜好推荐，预测评分: 1.17', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (23, 10, 18, 'collaborative_filtering', 1.16215, '基于相似用户喜好推荐，预测评分: 1.16', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (24, 10, 24, 'collaborative_filtering', 1.12819, '基于相似用户喜好推荐，预测评分: 1.13', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (25, 10, 20, 'hybrid', 0.613976, '混合推荐，综合分数: 0.61', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (26, 10, 17, 'hybrid', 0.510082, '混合推荐，综合分数: 0.51', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (27, 10, 23, 'hybrid', 0.510082, '混合推荐，综合分数: 0.51', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (28, 10, 21, 'hybrid', 0.492323, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (29, 10, 19, 'hybrid', 0.47458, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (30, 10, 22, 'hybrid', 0.468949, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (31, 10, 18, 'hybrid', 0.46486, '混合推荐，综合分数: 0.46', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (32, 10, 24, 'hybrid', 0.451276, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-12 09:50:52', NULL, NULL);
INSERT INTO `recommendations` VALUES (33, 1, 20, 'collaborative_filtering', 1.47167, '基于相似用户喜好推荐，预测评分: 1.47', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (34, 1, 19, 'collaborative_filtering', 1.36136, '基于相似用户喜好推荐，预测评分: 1.36', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (35, 1, 18, 'collaborative_filtering', 1.24874, '基于相似用户喜好推荐，预测评分: 1.25', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (36, 1, 17, 'collaborative_filtering', 1.23357, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (37, 1, 23, 'collaborative_filtering', 1.23357, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (38, 1, 24, 'collaborative_filtering', 1.13313, '基于相似用户喜好推荐，预测评分: 1.13', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (39, 1, 21, 'collaborative_filtering', 1.13153, '基于相似用户喜好推荐，预测评分: 1.13', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (40, 1, 22, 'collaborative_filtering', 1.06314, '基于相似用户喜好推荐，预测评分: 1.06', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (41, 1, 20, 'hybrid', 0.588669, '混合推荐，综合分数: 0.59', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (42, 1, 19, 'hybrid', 0.544542, '混合推荐，综合分数: 0.54', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (43, 1, 18, 'hybrid', 0.499494, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (44, 1, 17, 'hybrid', 0.493429, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (45, 1, 23, 'hybrid', 0.493429, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (46, 1, 24, 'hybrid', 0.45325, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (47, 1, 21, 'hybrid', 0.452614, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (48, 1, 22, 'hybrid', 0.425255, '混合推荐，综合分数: 0.43', 0, 0, '2025-09-12 09:54:44', NULL, NULL);
INSERT INTO `recommendations` VALUES (49, 1, 20, 'collaborative_filtering', 1.47167, '基于相似用户喜好推荐，预测评分: 1.47', 0, 0, '2025-09-12 09:55:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (50, 1, 19, 'collaborative_filtering', 1.36136, '基于相似用户喜好推荐，预测评分: 1.36', 0, 0, '2025-09-12 09:55:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (51, 1, 18, 'collaborative_filtering', 1.24874, '基于相似用户喜好推荐，预测评分: 1.25', 0, 0, '2025-09-12 09:55:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (52, 1, 17, 'collaborative_filtering', 1.23357, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 09:55:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (53, 1, 23, 'collaborative_filtering', 1.23357, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 09:55:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (54, 1, 24, 'collaborative_filtering', 1.13313, '基于相似用户喜好推荐，预测评分: 1.13', 0, 0, '2025-09-12 09:55:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (55, 1, 20, 'hybrid', 0.588669, '混合推荐，综合分数: 0.59', 0, 0, '2025-09-12 09:55:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (56, 1, 19, 'hybrid', 0.544542, '混合推荐，综合分数: 0.54', 0, 0, '2025-09-12 09:55:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (57, 1, 18, 'hybrid', 0.499494, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-12 09:55:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (58, 1, 20, 'collaborative_filtering', 1.47167, '基于相似用户喜好推荐，预测评分: 1.47', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (59, 1, 19, 'collaborative_filtering', 1.36136, '基于相似用户喜好推荐，预测评分: 1.36', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (60, 1, 18, 'collaborative_filtering', 1.24874, '基于相似用户喜好推荐，预测评分: 1.25', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (61, 1, 17, 'collaborative_filtering', 1.23357, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (62, 1, 23, 'collaborative_filtering', 1.23357, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (63, 1, 24, 'collaborative_filtering', 1.13313, '基于相似用户喜好推荐，预测评分: 1.13', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (64, 1, 21, 'collaborative_filtering', 1.13153, '基于相似用户喜好推荐，预测评分: 1.13', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (65, 1, 22, 'collaborative_filtering', 1.06314, '基于相似用户喜好推荐，预测评分: 1.06', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (66, 1, 20, 'hybrid', 0.588669, '混合推荐，综合分数: 0.59', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (67, 1, 19, 'hybrid', 0.544542, '混合推荐，综合分数: 0.54', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (68, 1, 18, 'hybrid', 0.499494, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (69, 1, 17, 'hybrid', 0.493429, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (70, 1, 23, 'hybrid', 0.493429, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (71, 1, 24, 'hybrid', 0.45325, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (72, 1, 21, 'hybrid', 0.452614, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (73, 1, 22, 'hybrid', 0.425255, '混合推荐，综合分数: 0.43', 0, 0, '2025-09-12 10:20:58', NULL, NULL);
INSERT INTO `recommendations` VALUES (74, 1, 20, 'collaborative_filtering', 1.47167, '基于相似用户喜好推荐，预测评分: 1.47', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (75, 1, 19, 'collaborative_filtering', 1.36136, '基于相似用户喜好推荐，预测评分: 1.36', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (76, 1, 18, 'collaborative_filtering', 1.24874, '基于相似用户喜好推荐，预测评分: 1.25', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (77, 1, 17, 'collaborative_filtering', 1.23357, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (78, 1, 23, 'collaborative_filtering', 1.23357, '基于相似用户喜好推荐，预测评分: 1.23', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (79, 1, 24, 'collaborative_filtering', 1.13313, '基于相似用户喜好推荐，预测评分: 1.13', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (80, 1, 21, 'collaborative_filtering', 1.13153, '基于相似用户喜好推荐，预测评分: 1.13', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (81, 1, 22, 'collaborative_filtering', 1.06314, '基于相似用户喜好推荐，预测评分: 1.06', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (82, 1, 20, 'hybrid', 0.588669, '混合推荐，综合分数: 0.59', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (83, 1, 19, 'hybrid', 0.544542, '混合推荐，综合分数: 0.54', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (84, 1, 18, 'hybrid', 0.499494, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (85, 1, 17, 'hybrid', 0.493429, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (86, 1, 23, 'hybrid', 0.493429, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (87, 1, 24, 'hybrid', 0.45325, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (88, 1, 21, 'hybrid', 0.452614, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (89, 1, 22, 'hybrid', 0.425255, '混合推荐，综合分数: 0.43', 0, 0, '2025-09-12 10:26:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (90, 1, 20, 'collaborative_filtering', 1.44444, '基于相似用户喜好推荐，预测评分: 1.44', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (91, 1, 19, 'collaborative_filtering', 1.33732, '基于相似用户喜好推荐，预测评分: 1.34', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (92, 1, 18, 'collaborative_filtering', 1.22464, '基于相似用户喜好推荐，预测评分: 1.22', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (93, 1, 17, 'collaborative_filtering', 1.20899, '基于相似用户喜好推荐，预测评分: 1.21', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (94, 1, 23, 'collaborative_filtering', 1.20899, '基于相似用户喜好推荐，预测评分: 1.21', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (95, 1, 24, 'collaborative_filtering', 1.10982, '基于相似用户喜好推荐，预测评分: 1.11', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (96, 1, 21, 'collaborative_filtering', 1.10745, '基于相似用户喜好推荐，预测评分: 1.11', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (97, 1, 22, 'collaborative_filtering', 1.03908, '基于相似用户喜好推荐，预测评分: 1.04', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (98, 1, 20, 'hybrid', 0.577776, '混合推荐，综合分数: 0.58', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (99, 1, 19, 'hybrid', 0.534927, '混合推荐，综合分数: 0.53', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (100, 1, 18, 'hybrid', 0.489856, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (101, 1, 17, 'hybrid', 0.483595, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (102, 1, 23, 'hybrid', 0.483595, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (103, 1, 24, 'hybrid', 0.443926, '混合推荐，综合分数: 0.44', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (104, 1, 21, 'hybrid', 0.442982, '混合推荐，综合分数: 0.44', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (105, 1, 22, 'hybrid', 0.415631, '混合推荐，综合分数: 0.42', 0, 0, '2025-09-15 03:24:08', NULL, NULL);
INSERT INTO `recommendations` VALUES (106, 1, 20, 'collaborative_filtering', 1.44444, '基于相似用户喜好推荐，预测评分: 1.44', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (107, 1, 19, 'collaborative_filtering', 1.33732, '基于相似用户喜好推荐，预测评分: 1.34', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (108, 1, 18, 'collaborative_filtering', 1.22464, '基于相似用户喜好推荐，预测评分: 1.22', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (109, 1, 17, 'collaborative_filtering', 1.20899, '基于相似用户喜好推荐，预测评分: 1.21', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (110, 1, 23, 'collaborative_filtering', 1.20899, '基于相似用户喜好推荐，预测评分: 1.21', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (111, 1, 24, 'collaborative_filtering', 1.10982, '基于相似用户喜好推荐，预测评分: 1.11', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (112, 1, 21, 'collaborative_filtering', 1.10745, '基于相似用户喜好推荐，预测评分: 1.11', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (113, 1, 22, 'collaborative_filtering', 1.03908, '基于相似用户喜好推荐，预测评分: 1.04', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (114, 1, 20, 'hybrid', 0.577776, '混合推荐，综合分数: 0.58', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (115, 1, 19, 'hybrid', 0.534927, '混合推荐，综合分数: 0.53', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (116, 1, 18, 'hybrid', 0.489856, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (117, 1, 17, 'hybrid', 0.483595, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (118, 1, 23, 'hybrid', 0.483595, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (119, 1, 24, 'hybrid', 0.443926, '混合推荐，综合分数: 0.44', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (120, 1, 21, 'hybrid', 0.442982, '混合推荐，综合分数: 0.44', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (121, 1, 22, 'hybrid', 0.415631, '混合推荐，综合分数: 0.42', 0, 0, '2025-09-15 03:34:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (122, 1, 20, 'collaborative_filtering', 1.5641, '协同过滤推荐，预测评分: 1.56', 0, 0, '2025-09-15 03:46:34', NULL, NULL);
INSERT INTO `recommendations` VALUES (123, 1, 18, 'collaborative_filtering', 1.55316, '协同过滤推荐，预测评分: 1.55', 0, 0, '2025-09-15 03:46:34', NULL, NULL);
INSERT INTO `recommendations` VALUES (124, 1, 19, 'collaborative_filtering', 1.47535, '协同过滤推荐，预测评分: 1.48', 0, 0, '2025-09-15 03:46:34', NULL, NULL);
INSERT INTO `recommendations` VALUES (125, 1, 17, 'collaborative_filtering', 1.35484, '协同过滤推荐，预测评分: 1.35', 0, 0, '2025-09-15 03:46:34', NULL, NULL);
INSERT INTO `recommendations` VALUES (126, 1, 23, 'collaborative_filtering', 1.35484, '协同过滤推荐，预测评分: 1.35', 0, 0, '2025-09-15 03:46:34', NULL, NULL);
INSERT INTO `recommendations` VALUES (127, 1, 24, 'collaborative_filtering', 1.23133, '协同过滤推荐，预测评分: 1.23', 0, 0, '2025-09-15 03:46:34', NULL, NULL);
INSERT INTO `recommendations` VALUES (128, 1, 21, 'collaborative_filtering', 1.18427, '协同过滤推荐，预测评分: 1.18', 0, 0, '2025-09-15 03:46:34', NULL, NULL);
INSERT INTO `recommendations` VALUES (129, 1, 22, 'collaborative_filtering', 1.17622, '协同过滤推荐，预测评分: 1.18', 0, 0, '2025-09-15 03:46:34', NULL, NULL);
INSERT INTO `recommendations` VALUES (130, 1, 20, 'hybrid', 0.625641, '混合推荐，综合分数: 0.63', 0, 0, '2025-09-15 03:48:28', NULL, NULL);
INSERT INTO `recommendations` VALUES (131, 1, 18, 'hybrid', 0.621266, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 03:48:28', NULL, NULL);
INSERT INTO `recommendations` VALUES (132, 1, 19, 'hybrid', 0.59014, '混合推荐，综合分数: 0.59', 0, 0, '2025-09-15 03:48:28', NULL, NULL);
INSERT INTO `recommendations` VALUES (133, 1, 17, 'hybrid', 0.541934, '混合推荐，综合分数: 0.54', 0, 0, '2025-09-15 03:48:28', NULL, NULL);
INSERT INTO `recommendations` VALUES (134, 1, 23, 'hybrid', 0.541934, '混合推荐，综合分数: 0.54', 0, 0, '2025-09-15 03:48:28', NULL, NULL);
INSERT INTO `recommendations` VALUES (135, 1, 20, 'popularity', 0.588, '热门商品推荐，热度分数: 0.59', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (136, 1, 19, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (137, 1, 22, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (138, 1, 17, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (139, 1, 23, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (140, 1, 20, 'popularity', 0.588, '热门商品推荐，热度分数: 0.59', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (141, 1, 19, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (142, 1, 22, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (143, 1, 17, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (144, 1, 23, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (145, 1, 20, 'popularity', 0.588, '热门商品推荐，热度分数: 0.59', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (146, 1, 19, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (147, 1, 22, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (148, 1, 17, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (149, 1, 23, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:49:31', NULL, NULL);
INSERT INTO `recommendations` VALUES (150, 1, 20, 'hybrid', 0.913406, '混合推荐，综合分数: 0.91', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (151, 1, 19, 'hybrid', 0.683837, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (152, 1, 17, 'hybrid', 0.635734, '混合推荐，综合分数: 0.64', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (153, 1, 23, 'hybrid', 0.622815, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (154, 1, 18, 'hybrid', 0.621266, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (155, 1, 20, 'popularity', 0.588, '热门商品推荐，热度分数: 0.59', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (156, 1, 19, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (157, 1, 22, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (158, 1, 17, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (159, 1, 23, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (160, 1, 20, 'popularity', 0.588, '热门商品推荐，热度分数: 0.59', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (161, 1, 19, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (162, 1, 22, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (163, 1, 17, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (164, 1, 23, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (165, 1, 20, 'popularity', 0.588, '热门商品推荐，热度分数: 0.59', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (166, 1, 19, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (167, 1, 22, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (168, 1, 17, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (169, 1, 23, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:50:51', NULL, NULL);
INSERT INTO `recommendations` VALUES (170, 1, 20, 'collaborative_filtering', 1.5641, '协同过滤推荐，预测评分: 1.56', 0, 0, '2025-09-15 03:51:03', NULL, NULL);
INSERT INTO `recommendations` VALUES (171, 1, 18, 'collaborative_filtering', 1.55316, '协同过滤推荐，预测评分: 1.55', 0, 0, '2025-09-15 03:51:03', NULL, NULL);
INSERT INTO `recommendations` VALUES (172, 1, 19, 'collaborative_filtering', 1.47535, '协同过滤推荐，预测评分: 1.48', 0, 0, '2025-09-15 03:51:03', NULL, NULL);
INSERT INTO `recommendations` VALUES (173, 1, 17, 'collaborative_filtering', 1.35484, '协同过滤推荐，预测评分: 1.35', 0, 0, '2025-09-15 03:51:03', NULL, NULL);
INSERT INTO `recommendations` VALUES (174, 1, 23, 'collaborative_filtering', 1.35484, '协同过滤推荐，预测评分: 1.35', 0, 0, '2025-09-15 03:51:03', NULL, NULL);
INSERT INTO `recommendations` VALUES (175, 1, 20, 'content_based', 0.371217, '内容推荐，相似度: 0.37', 0, 0, '2025-09-15 03:51:03', NULL, NULL);
INSERT INTO `recommendations` VALUES (176, 1, 17, 'content_based', 0.312667, '内容推荐，相似度: 0.31', 0, 0, '2025-09-15 03:51:03', NULL, NULL);
INSERT INTO `recommendations` VALUES (177, 1, 23, 'content_based', 0.269601, '内容推荐，相似度: 0.27', 0, 0, '2025-09-15 03:51:03', NULL, NULL);
INSERT INTO `recommendations` VALUES (178, 1, 19, 'content_based', 0.214322, '内容推荐，相似度: 0.21', 0, 0, '2025-09-15 03:51:03', NULL, NULL);
INSERT INTO `recommendations` VALUES (179, 1, 20, 'hybrid', 0.913406, '混合推荐，综合分数: 0.91', 0, 0, '2025-09-15 03:51:35', NULL, NULL);
INSERT INTO `recommendations` VALUES (180, 1, 19, 'hybrid', 0.683837, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 03:51:35', NULL, NULL);
INSERT INTO `recommendations` VALUES (181, 1, 17, 'hybrid', 0.635734, '混合推荐，综合分数: 0.64', 0, 0, '2025-09-15 03:51:35', NULL, NULL);
INSERT INTO `recommendations` VALUES (182, 1, 23, 'hybrid', 0.622815, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 03:51:35', NULL, NULL);
INSERT INTO `recommendations` VALUES (183, 1, 18, 'hybrid', 0.621266, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 03:51:35', NULL, NULL);
INSERT INTO `recommendations` VALUES (184, 1, 22, 'hybrid', 0.499887, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-15 03:51:35', NULL, NULL);
INSERT INTO `recommendations` VALUES (185, 1, 24, 'hybrid', 0.492532, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 03:51:35', NULL, NULL);
INSERT INTO `recommendations` VALUES (186, 1, 21, 'hybrid', 0.47371, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 03:51:35', NULL, NULL);
INSERT INTO `recommendations` VALUES (187, 1, 20, 'collaborative_filtering', 1.5641, '协同过滤推荐，预测评分: 1.56', 0, 0, '2025-09-15 03:51:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (188, 1, 18, 'collaborative_filtering', 1.55316, '协同过滤推荐，预测评分: 1.55', 0, 0, '2025-09-15 03:51:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (189, 1, 19, 'collaborative_filtering', 1.47535, '协同过滤推荐，预测评分: 1.48', 0, 0, '2025-09-15 03:51:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (190, 1, 17, 'collaborative_filtering', 1.35484, '协同过滤推荐，预测评分: 1.35', 0, 0, '2025-09-15 03:51:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (191, 1, 23, 'collaborative_filtering', 1.35484, '协同过滤推荐，预测评分: 1.35', 0, 0, '2025-09-15 03:51:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (192, 1, 24, 'collaborative_filtering', 1.23133, '协同过滤推荐，预测评分: 1.23', 0, 0, '2025-09-15 03:51:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (193, 1, 21, 'collaborative_filtering', 1.18427, '协同过滤推荐，预测评分: 1.18', 0, 0, '2025-09-15 03:51:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (194, 1, 22, 'collaborative_filtering', 1.17622, '协同过滤推荐，预测评分: 1.18', 0, 0, '2025-09-15 03:51:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (195, 1, 20, 'content_based', 0.371217, '内容推荐，相似度: 0.37', 0, 0, '2025-09-15 03:51:38', NULL, NULL);
INSERT INTO `recommendations` VALUES (196, 1, 17, 'content_based', 0.312667, '内容推荐，相似度: 0.31', 0, 0, '2025-09-15 03:51:38', NULL, NULL);
INSERT INTO `recommendations` VALUES (197, 1, 23, 'content_based', 0.269601, '内容推荐，相似度: 0.27', 0, 0, '2025-09-15 03:51:38', NULL, NULL);
INSERT INTO `recommendations` VALUES (198, 1, 19, 'content_based', 0.214322, '内容推荐，相似度: 0.21', 0, 0, '2025-09-15 03:51:38', NULL, NULL);
INSERT INTO `recommendations` VALUES (199, 1, 20, 'popularity', 0.588, '热门商品推荐，热度分数: 0.59', 0, 0, '2025-09-15 03:51:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (200, 1, 19, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:51:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (201, 1, 22, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 03:51:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (202, 1, 17, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:51:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (203, 1, 23, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 03:51:39', NULL, NULL);
INSERT INTO `recommendations` VALUES (204, 1, 20, 'hybrid', 0.913406, '混合推荐，综合分数: 0.91', 0, 0, '2025-09-15 03:56:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (205, 1, 19, 'hybrid', 0.683837, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 03:56:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (206, 1, 17, 'hybrid', 0.635734, '混合推荐，综合分数: 0.64', 0, 0, '2025-09-15 03:56:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (207, 1, 23, 'hybrid', 0.622815, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 03:56:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (208, 1, 18, 'hybrid', 0.621266, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 03:56:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (209, 1, 22, 'hybrid', 0.499887, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-15 03:56:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (210, 1, 24, 'hybrid', 0.492532, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 03:56:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (211, 1, 21, 'hybrid', 0.47371, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 03:56:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (212, 10, 20, 'hybrid', 0.612832, '混合推荐，综合分数: 0.61', 0, 0, '2025-09-15 05:09:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (213, 10, 17, 'hybrid', 0.585049, '混合推荐，综合分数: 0.59', 0, 0, '2025-09-15 05:09:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (214, 10, 23, 'hybrid', 0.577586, '混合推荐，综合分数: 0.58', 0, 0, '2025-09-15 05:09:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (215, 10, 18, 'hybrid', 0.511422, '混合推荐，综合分数: 0.51', 0, 0, '2025-09-15 05:09:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (216, 10, 21, 'hybrid', 0.481162, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 05:09:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (217, 10, 19, 'hybrid', 0.478376, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 05:09:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (218, 10, 22, 'hybrid', 0.473932, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 05:09:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (219, 10, 24, 'hybrid', 0.45184, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-15 05:09:09', NULL, NULL);
INSERT INTO `recommendations` VALUES (220, 1, 20, 'hybrid', 0.913406, '混合推荐，综合分数: 0.91', 0, 0, '2025-09-15 05:12:13', NULL, NULL);
INSERT INTO `recommendations` VALUES (221, 1, 19, 'hybrid', 0.683837, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 05:12:13', NULL, NULL);
INSERT INTO `recommendations` VALUES (222, 1, 17, 'hybrid', 0.635734, '混合推荐，综合分数: 0.64', 0, 0, '2025-09-15 05:12:13', NULL, NULL);
INSERT INTO `recommendations` VALUES (223, 1, 23, 'hybrid', 0.622815, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 05:12:13', NULL, NULL);
INSERT INTO `recommendations` VALUES (224, 1, 18, 'hybrid', 0.621266, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 05:12:13', NULL, NULL);
INSERT INTO `recommendations` VALUES (225, 1, 22, 'hybrid', 0.499887, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-15 05:12:13', NULL, NULL);
INSERT INTO `recommendations` VALUES (226, 1, 24, 'hybrid', 0.492532, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 05:12:13', NULL, NULL);
INSERT INTO `recommendations` VALUES (227, 1, 21, 'hybrid', 0.47371, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 05:12:13', NULL, NULL);
INSERT INTO `recommendations` VALUES (228, 8, 18, 'hybrid', 0.969369, '混合推荐，综合分数: 0.97', 0, 0, '2025-09-15 05:16:54', NULL, NULL);
INSERT INTO `recommendations` VALUES (229, 8, 20, 'hybrid', 0.921448, '混合推荐，综合分数: 0.92', 0, 0, '2025-09-15 05:16:54', NULL, NULL);
INSERT INTO `recommendations` VALUES (230, 8, 21, 'hybrid', 0.675118, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 05:16:54', NULL, NULL);
INSERT INTO `recommendations` VALUES (231, 8, 24, 'hybrid', 0.626503, '混合推荐，综合分数: 0.63', 0, 0, '2025-09-15 05:16:54', NULL, NULL);
INSERT INTO `recommendations` VALUES (232, 8, 22, 'hybrid', 0.575979, '混合推荐，综合分数: 0.58', 0, 0, '2025-09-15 05:16:54', NULL, NULL);
INSERT INTO `recommendations` VALUES (233, 8, 19, 'hybrid', 0.575917, '混合推荐，综合分数: 0.58', 0, 0, '2025-09-15 05:16:54', NULL, NULL);
INSERT INTO `recommendations` VALUES (234, 8, 17, 'hybrid', 0.526667, '混合推荐，综合分数: 0.53', 0, 0, '2025-09-15 05:16:54', NULL, NULL);
INSERT INTO `recommendations` VALUES (235, 8, 23, 'hybrid', 0.526667, '混合推荐，综合分数: 0.53', 0, 0, '2025-09-15 05:16:54', NULL, NULL);
INSERT INTO `recommendations` VALUES (236, 1, 20, 'hybrid', 0.913406, '混合推荐，综合分数: 0.91', 0, 0, '2025-09-15 06:03:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (237, 1, 19, 'hybrid', 0.683837, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 06:03:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (238, 1, 17, 'hybrid', 0.635734, '混合推荐，综合分数: 0.64', 0, 0, '2025-09-15 06:03:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (239, 1, 23, 'hybrid', 0.622815, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 06:03:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (240, 1, 18, 'hybrid', 0.621266, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 06:03:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (241, 1, 22, 'hybrid', 0.499887, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-15 06:03:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (242, 1, 24, 'hybrid', 0.492532, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 06:03:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (243, 1, 21, 'hybrid', 0.47371, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 06:03:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (244, 8, 18, 'hybrid', 0.969369, '混合推荐，综合分数: 0.97', 0, 0, '2025-09-15 06:04:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (245, 8, 20, 'hybrid', 0.921448, '混合推荐，综合分数: 0.92', 0, 0, '2025-09-15 06:04:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (246, 8, 21, 'hybrid', 0.675118, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 06:04:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (247, 8, 24, 'hybrid', 0.626503, '混合推荐，综合分数: 0.63', 0, 0, '2025-09-15 06:04:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (248, 8, 22, 'hybrid', 0.575979, '混合推荐，综合分数: 0.58', 0, 0, '2025-09-15 06:04:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (249, 8, 19, 'hybrid', 0.575917, '混合推荐，综合分数: 0.58', 0, 0, '2025-09-15 06:04:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (250, 8, 17, 'hybrid', 0.526667, '混合推荐，综合分数: 0.53', 0, 0, '2025-09-15 06:04:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (251, 8, 23, 'hybrid', 0.526667, '混合推荐，综合分数: 0.53', 0, 0, '2025-09-15 06:04:05', NULL, NULL);
INSERT INTO `recommendations` VALUES (252, 1, 20, 'hybrid', 0.912506, '混合推荐，综合分数: 0.91', 0, 0, '2025-09-15 06:29:12', NULL, NULL);
INSERT INTO `recommendations` VALUES (253, 1, 19, 'hybrid', 0.683687, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 06:29:12', NULL, NULL);
INSERT INTO `recommendations` VALUES (254, 1, 17, 'hybrid', 0.635734, '混合推荐，综合分数: 0.64', 0, 0, '2025-09-15 06:29:12', NULL, NULL);
INSERT INTO `recommendations` VALUES (255, 1, 23, 'hybrid', 0.622815, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 06:29:12', NULL, NULL);
INSERT INTO `recommendations` VALUES (256, 1, 18, 'hybrid', 0.621266, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 06:29:12', NULL, NULL);
INSERT INTO `recommendations` VALUES (257, 1, 22, 'hybrid', 0.499887, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-15 06:29:12', NULL, NULL);
INSERT INTO `recommendations` VALUES (258, 1, 24, 'hybrid', 0.492532, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 06:29:12', NULL, NULL);
INSERT INTO `recommendations` VALUES (259, 1, 21, 'hybrid', 0.47371, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 06:29:12', NULL, NULL);
INSERT INTO `recommendations` VALUES (260, 1, 20, 'collaborative_filtering', 1.5641, '协同过滤推荐，预测评分: 1.56', 0, 0, '2025-09-15 06:29:23', NULL, NULL);
INSERT INTO `recommendations` VALUES (261, 1, 18, 'collaborative_filtering', 1.55316, '协同过滤推荐，预测评分: 1.55', 0, 0, '2025-09-15 06:29:23', NULL, NULL);
INSERT INTO `recommendations` VALUES (262, 1, 19, 'collaborative_filtering', 1.47535, '协同过滤推荐，预测评分: 1.48', 0, 0, '2025-09-15 06:29:23', NULL, NULL);
INSERT INTO `recommendations` VALUES (263, 1, 17, 'collaborative_filtering', 1.35484, '协同过滤推荐，预测评分: 1.35', 0, 0, '2025-09-15 06:29:23', NULL, NULL);
INSERT INTO `recommendations` VALUES (264, 1, 23, 'collaborative_filtering', 1.35484, '协同过滤推荐，预测评分: 1.35', 0, 0, '2025-09-15 06:29:23', NULL, NULL);
INSERT INTO `recommendations` VALUES (265, 1, 24, 'collaborative_filtering', 1.23133, '协同过滤推荐，预测评分: 1.23', 0, 0, '2025-09-15 06:29:23', NULL, NULL);
INSERT INTO `recommendations` VALUES (266, 1, 21, 'collaborative_filtering', 1.18427, '协同过滤推荐，预测评分: 1.18', 0, 0, '2025-09-15 06:29:23', NULL, NULL);
INSERT INTO `recommendations` VALUES (267, 1, 22, 'collaborative_filtering', 1.17622, '协同过滤推荐，预测评分: 1.18', 0, 0, '2025-09-15 06:29:23', NULL, NULL);
INSERT INTO `recommendations` VALUES (268, 1, 20, 'content_based', 0.371217, '内容推荐，相似度: 0.37', 0, 0, '2025-09-15 06:29:38', NULL, NULL);
INSERT INTO `recommendations` VALUES (269, 1, 17, 'content_based', 0.312667, '内容推荐，相似度: 0.31', 0, 0, '2025-09-15 06:29:38', NULL, NULL);
INSERT INTO `recommendations` VALUES (270, 1, 23, 'content_based', 0.269601, '内容推荐，相似度: 0.27', 0, 0, '2025-09-15 06:29:38', NULL, NULL);
INSERT INTO `recommendations` VALUES (271, 1, 19, 'content_based', 0.214322, '内容推荐，相似度: 0.21', 0, 0, '2025-09-15 06:29:38', NULL, NULL);
INSERT INTO `recommendations` VALUES (272, 1, 20, 'popularity', 0.585, '热门商品推荐，热度分数: 0.58', 0, 0, '2025-09-15 06:29:46', NULL, NULL);
INSERT INTO `recommendations` VALUES (273, 1, 22, 'popularity', 0.098, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 06:29:46', NULL, NULL);
INSERT INTO `recommendations` VALUES (274, 1, 19, 'popularity', 0.0975, '热门商品推荐，热度分数: 0.10', 0, 0, '2025-09-15 06:29:46', NULL, NULL);
INSERT INTO `recommendations` VALUES (275, 1, 17, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 06:29:46', NULL, NULL);
INSERT INTO `recommendations` VALUES (276, 1, 23, 'popularity', 0, '热门商品推荐，热度分数: 0.00', 0, 0, '2025-09-15 06:29:46', NULL, NULL);
INSERT INTO `recommendations` VALUES (277, 1, 20, 'hybrid', 0.912506, '混合推荐，综合分数: 0.91', 0, 0, '2025-09-15 07:31:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (278, 1, 19, 'hybrid', 0.683687, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 07:31:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (279, 1, 17, 'hybrid', 0.635734, '混合推荐，综合分数: 0.64', 0, 0, '2025-09-15 07:31:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (280, 1, 23, 'hybrid', 0.622815, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 07:31:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (281, 1, 18, 'hybrid', 0.621266, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 07:31:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (282, 1, 22, 'hybrid', 0.499737, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-15 07:31:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (283, 1, 24, 'hybrid', 0.492532, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 07:31:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (284, 1, 21, 'hybrid', 0.47371, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 07:31:10', NULL, NULL);
INSERT INTO `recommendations` VALUES (285, 1, 20, 'hybrid', 0.911886, '混合推荐，综合分数: 0.91', 0, 0, '2025-09-15 08:18:04', NULL, NULL);
INSERT INTO `recommendations` VALUES (286, 1, 19, 'hybrid', 0.683011, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 08:18:04', NULL, NULL);
INSERT INTO `recommendations` VALUES (287, 1, 17, 'hybrid', 0.635022, '混合推荐，综合分数: 0.64', 0, 0, '2025-09-15 08:18:04', NULL, NULL);
INSERT INTO `recommendations` VALUES (288, 1, 23, 'hybrid', 0.622102, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 08:18:04', NULL, NULL);
INSERT INTO `recommendations` VALUES (289, 1, 18, 'hybrid', 0.620502, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 08:18:04', NULL, NULL);
INSERT INTO `recommendations` VALUES (290, 1, 22, 'hybrid', 0.499071, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-15 08:18:04', NULL, NULL);
INSERT INTO `recommendations` VALUES (291, 1, 24, 'hybrid', 0.491302, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 08:18:04', NULL, NULL);
INSERT INTO `recommendations` VALUES (292, 1, 21, 'hybrid', 0.473262, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 08:18:04', NULL, NULL);
INSERT INTO `recommendations` VALUES (293, 10, 20, 'hybrid', 0.612455, '混合推荐，综合分数: 0.61', 0, 0, '2025-09-15 08:18:33', NULL, NULL);
INSERT INTO `recommendations` VALUES (294, 10, 17, 'hybrid', 0.584418, '混合推荐，综合分数: 0.58', 0, 0, '2025-09-15 08:18:33', NULL, NULL);
INSERT INTO `recommendations` VALUES (295, 10, 23, 'hybrid', 0.576955, '混合推荐，综合分数: 0.58', 0, 0, '2025-09-15 08:18:33', NULL, NULL);
INSERT INTO `recommendations` VALUES (296, 10, 18, 'hybrid', 0.510371, '混合推荐，综合分数: 0.51', 0, 0, '2025-09-15 08:18:33', NULL, NULL);
INSERT INTO `recommendations` VALUES (297, 10, 21, 'hybrid', 0.480723, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 08:18:33', NULL, NULL);
INSERT INTO `recommendations` VALUES (298, 10, 19, 'hybrid', 0.47788, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 08:18:33', NULL, NULL);
INSERT INTO `recommendations` VALUES (299, 10, 22, 'hybrid', 0.473419, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 08:18:33', NULL, NULL);
INSERT INTO `recommendations` VALUES (300, 10, 24, 'hybrid', 0.451034, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-15 08:18:33', NULL, NULL);
INSERT INTO `recommendations` VALUES (301, 1, 20, 'hybrid', 1.36493, '混合推荐，综合分数: 1.36', 0, 0, '2025-09-15 09:02:21', NULL, NULL);
INSERT INTO `recommendations` VALUES (302, 1, 19, 'hybrid', 0.68222, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 09:02:21', NULL, NULL);
INSERT INTO `recommendations` VALUES (303, 1, 17, 'hybrid', 0.642019, '混合推荐，综合分数: 0.64', 0, 0, '2025-09-15 09:02:21', NULL, NULL);
INSERT INTO `recommendations` VALUES (304, 1, 23, 'hybrid', 0.620147, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 09:02:21', NULL, NULL);
INSERT INTO `recommendations` VALUES (305, 1, 18, 'hybrid', 0.620144, '混合推荐，综合分数: 0.62', 0, 0, '2025-09-15 09:02:21', NULL, NULL);
INSERT INTO `recommendations` VALUES (306, 1, 22, 'hybrid', 0.498206, '混合推荐，综合分数: 0.50', 0, 0, '2025-09-15 09:02:21', NULL, NULL);
INSERT INTO `recommendations` VALUES (307, 1, 24, 'hybrid', 0.490829, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 09:02:21', NULL, NULL);
INSERT INTO `recommendations` VALUES (308, 1, 21, 'hybrid', 0.472988, '混合推荐，综合分数: 0.47', 0, 0, '2025-09-15 09:02:21', NULL, NULL);
INSERT INTO `recommendations` VALUES (309, 10, 20, 'hybrid', 0.565546, '混合推荐，综合分数: 0.57', 0, 0, '2025-09-15 09:06:07', NULL, NULL);
INSERT INTO `recommendations` VALUES (310, 10, 23, 'hybrid', 0.561393, '混合推荐，综合分数: 0.56', 0, 0, '2025-09-15 09:06:07', NULL, NULL);
INSERT INTO `recommendations` VALUES (311, 10, 17, 'hybrid', 0.508745, '混合推荐，综合分数: 0.51', 0, 0, '2025-09-15 09:06:07', NULL, NULL);
INSERT INTO `recommendations` VALUES (312, 10, 18, 'hybrid', 0.493886, '混合推荐，综合分数: 0.49', 0, 0, '2025-09-15 09:06:07', NULL, NULL);
INSERT INTO `recommendations` VALUES (313, 10, 21, 'hybrid', 0.460869, '混合推荐，综合分数: 0.46', 0, 0, '2025-09-15 09:06:07', NULL, NULL);
INSERT INTO `recommendations` VALUES (314, 10, 19, 'hybrid', 0.457789, '混合推荐，综合分数: 0.46', 0, 0, '2025-09-15 09:06:07', NULL, NULL);
INSERT INTO `recommendations` VALUES (315, 10, 22, 'hybrid', 0.454564, '混合推荐，综合分数: 0.45', 0, 0, '2025-09-15 09:06:07', NULL, NULL);
INSERT INTO `recommendations` VALUES (316, 10, 24, 'hybrid', 0.431583, '混合推荐，综合分数: 0.43', 0, 0, '2025-09-15 09:06:07', NULL, NULL);
INSERT INTO `recommendations` VALUES (317, 1, 19, 'hybrid', 0.684595, '混合推荐，综合分数: 0.68', 0, 0, '2025-09-15 09:40:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (318, 1, 18, 'hybrid', 0.608148, '混合推荐，综合分数: 0.61', 0, 0, '2025-09-15 09:40:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (319, 1, 17, 'hybrid', 0.607923, '混合推荐，综合分数: 0.61', 0, 0, '2025-09-15 09:40:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (320, 1, 23, 'hybrid', 0.589902, '混合推荐，综合分数: 0.59', 0, 0, '2025-09-15 09:40:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (321, 1, 20, 'hybrid', 0.564847, '混合推荐，综合分数: 0.56', 0, 0, '2025-09-15 09:40:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (322, 1, 22, 'hybrid', 0.481106, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 09:40:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (323, 1, 24, 'hybrid', 0.475912, '混合推荐，综合分数: 0.48', 0, 0, '2025-09-15 09:40:37', NULL, NULL);
INSERT INTO `recommendations` VALUES (324, 1, 21, 'hybrid', 0.459276, '混合推荐，综合分数: 0.46', 0, 0, '2025-09-15 09:40:37', NULL, NULL);

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
  `status` enum('pending','paid','shipped','delivered','completed','cancelled','timeout') CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'pending',
  `payment_method` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `meeting_location` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL,
  `meeting_time` datetime NULL DEFAULT NULL,
  `buyer_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `seller_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `created_at` datetime NULL DEFAULT NULL,
  `updated_at` datetime NULL DEFAULT NULL,
  `completed_at` datetime NULL DEFAULT NULL,
  `payment_confirmed_at` datetime NULL DEFAULT NULL,
  `shipped_at` datetime NULL DEFAULT NULL,
  `delivered_at` datetime NULL DEFAULT NULL,
  `timeout_at` datetime NULL DEFAULT NULL,
  `shipping_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `delivery_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `dispute_reason` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  `admin_notes` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `item_id`(`item_id` ASC) USING BTREE,
  INDEX `buyer_id`(`buyer_id` ASC) USING BTREE,
  INDEX `seller_id`(`seller_id` ASC) USING BTREE,
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `transactions_ibfk_2` FOREIGN KEY (`buyer_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `transactions_ibfk_3` FOREIGN KEY (`seller_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of transactions
-- ----------------------------
INSERT INTO `transactions` VALUES (1, 20, 10, 1, 999.00, 'shipped', 'wechat', NULL, NULL, NULL, NULL, '2025-09-15 08:38:48', '2025-09-15 09:08:04', NULL, '2025-09-15 08:59:46', '2025-09-15 09:08:04', NULL, NULL, '', NULL, NULL, NULL);
INSERT INTO `transactions` VALUES (2, 17, 10, 1, 1000.00, 'shipped', 'wechat', NULL, NULL, NULL, NULL, '2025-09-15 08:41:07', '2025-09-15 09:07:43', NULL, '2025-09-15 09:01:27', '2025-09-15 09:07:43', NULL, NULL, '已经发货咯', NULL, NULL, NULL);

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
) ENGINE = InnoDB AUTO_INCREMENT = 11 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_audits
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_avatar_audits
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 107 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_behaviors
-- ----------------------------
INSERT INTO `user_behaviors` VALUES (83, 1, 24, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-12 07:33:52');
INSERT INTO `user_behaviors` VALUES (84, 10, 18, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-12 07:36:39');
INSERT INTO `user_behaviors` VALUES (85, 10, 24, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-12 09:44:22');
INSERT INTO `user_behaviors` VALUES (86, 10, 19, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-12 09:44:43');
INSERT INTO `user_behaviors` VALUES (87, 10, 20, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-12 09:44:46');
INSERT INTO `user_behaviors` VALUES (88, 10, 20, 'like', NULL, '117.189.225.22', NULL, '2025-09-12 09:44:50');
INSERT INTO `user_behaviors` VALUES (89, 10, 21, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-12 09:44:59');
INSERT INTO `user_behaviors` VALUES (90, 10, 22, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-12 09:45:10');
INSERT INTO `user_behaviors` VALUES (91, 1, 21, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 03:37:02');
INSERT INTO `user_behaviors` VALUES (92, 1, 21, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 03:37:14');
INSERT INTO `user_behaviors` VALUES (93, 1, 18, 'like', NULL, '117.189.225.22', NULL, '2025-09-15 03:37:28');
INSERT INTO `user_behaviors` VALUES (94, 1, 18, 'view', NULL, '117.189.225.22', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 03:37:29');
INSERT INTO `user_behaviors` VALUES (95, 10, 20, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 08:18:40');
INSERT INTO `user_behaviors` VALUES (96, 10, 20, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 08:23:19');
INSERT INTO `user_behaviors` VALUES (97, 10, 20, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 08:26:01');
INSERT INTO `user_behaviors` VALUES (98, 10, 20, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 08:29:45');
INSERT INTO `user_behaviors` VALUES (99, 10, 20, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 08:31:44');
INSERT INTO `user_behaviors` VALUES (100, 10, 20, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 08:33:47');
INSERT INTO `user_behaviors` VALUES (101, 10, 20, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 08:35:35');
INSERT INTO `user_behaviors` VALUES (102, 10, 20, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 08:40:23');
INSERT INTO `user_behaviors` VALUES (103, 10, 20, 'contact', NULL, '1.49.101.162', NULL, '2025-09-15 08:40:29');
INSERT INTO `user_behaviors` VALUES (104, 10, 17, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 08:40:47');
INSERT INTO `user_behaviors` VALUES (105, 1, 20, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 09:31:33');
INSERT INTO `user_behaviors` VALUES (106, 1, 17, 'view', NULL, '1.49.101.162', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36', '2025-09-15 09:40:44');

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
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_profile_audits
-- ----------------------------

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
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'admin', 'admin@campus-market.com', 'scrypt:32768:8:1$C2Gbwmw1S83lgN3Q$4381b67bcc48236d4c0d34167bbe3cb4fba250be89330105739045c21ff62f8a574fa882381cc987bc96b3b804070596784fb34757e9ef192c3c7cdc6581d16e', '管理员', '', '', '1_20250910_014643_logo.jpg', '', '[\"服装配饰\", \"生活用品\"]', 1, 1, 'approved', '2025-09-02 16:31:39', '2025-09-15 09:09:42', '2025-09-15 09:09:42');
INSERT INTO `users` VALUES (3, 'lxm', '2164168518@qq.com', 'scrypt:32768:8:1$GhW2En365tRAZ8NG$2f7f6a5fda3d2a4c3b3294be9b177268002a13336ac5417e79cc48eb8c1bd2c08ca6b5bf715d99ee161dd9aa7247055e2f7ec10fcdf5bdf63518db5bac75df7c', '李先梅', NULL, '202202074168', NULL, NULL, NULL, 1, 0, 'approved', '2025-09-03 02:18:11', '2025-09-03 02:23:53', '2025-09-03 02:23:53');
INSERT INTO `users` VALUES (5, 'test_user', 'test@example.com', 'scrypt:32768:8:1$vQmp36Oa1g6jUVt1$9b097446dfba509dff9c51bae5fb6267e9d81f14fcfe61a994bafcb57738e23ca9d5a98ac8de9f471b24e3c08f931300bc1bb8b36293ce6ee358236a3c0295d8', NULL, NULL, NULL, NULL, NULL, NULL, 1, 0, 'approved', '2025-09-03 03:05:02', '2025-09-08 09:54:08', NULL);
INSERT INTO `users` VALUES (7, 'testuser1', 'testuser1@gmail.com', 'scrypt:32768:8:1$ykcX09Jv0hPB77md$f0b4670a823d1274caee93dd90583a4861eed1a6ea2066fc5c504f4f4e032f21f420f8fab52edf10cba9be714e9d365f985b304e6d84b206992d5a495c56db39', 'testuser1', NULL, '202103124003', NULL, NULL, NULL, 1, 0, 'approved', '2025-09-03 04:33:16', '2025-09-03 04:33:16', NULL);
INSERT INTO `users` VALUES (8, 'testuser2', 'testuser2@gmail.com', 'scrypt:32768:8:1$WjPpeKdMG7geO7dZ$186ad6f127e15b6eef2b5167e14aefc9199760a6237e31b6ea759a88c37daba4564def6c5c80b905aac71908921f80045760523b340f07d1ea7e177d9c95979f', 'testuser2', '', '202103124003', NULL, '', NULL, 1, 0, 'approved', '2025-09-03 04:43:31', '2025-09-15 06:04:04', '2025-09-15 06:04:04');
INSERT INTO `users` VALUES (10, 'luner11', 'lzyzy527@gmail.com', 'scrypt:32768:8:1$xHRrn274G2zCNdcC$1cbc48987b0ee3732a23ba2b68f8ffb6ce28086a2019ed206b36a3a8d9a46c5f1d940d70d93adf4221cd071aa55d9bbfb9fcee9c1a4de76151f1570cee772a12', '卢正勇', '17684184742', '202103124001', '10_20250912_073758_2023-10-14_22-35-18.png', '', '[\"电子产品\", \"图书教材\", \"运动健身\", \"音乐\"]', 1, 0, 'approved', '2025-09-04 15:08:45', '2025-09-15 09:08:22', '2025-09-15 09:08:22');
INSERT INTO `users` VALUES (13, 'xiaoTxn', '2127316700@qq.com', 'scrypt:32768:8:1$kzYvJLVdCfErVJVn$193d847992f95be453a8947d899ef0ea756804abf2fdfc5423b2000669e6f5a2d153860912f1b560524da7acee4e8ffc7c3797bbfb22a47d8b2caa99f1b4af64', '田栩宁', '15772357814', '202202070919', NULL, NULL, NULL, 1, 0, 'approved', '2025-09-09 03:28:22', '2025-09-09 08:44:15', '2025-09-09 08:44:15');

SET FOREIGN_KEY_CHECKS = 1;
