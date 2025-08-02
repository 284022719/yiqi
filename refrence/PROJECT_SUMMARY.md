# 魔兽世界公会成员信息获取工具 - 项目总结

## 项目概述

本项目是一个完整的魔兽世界公会成员信息获取工具，使用魔兽世界官方API获取公会成员的详细信息，包括装备等级、成就点数、专精等数据。

## 项目文件结构

```
├── data/
│   └── guildmember.csv              # 公会成员CSV数据文件
├── get_guild_members_info.py        # 主要功能脚本
├── test_api.py                      # API测试脚本
├── run_guild_tool.py                # 快速启动脚本
├── requirements.txt                  # Python依赖文件
├── wow-armory-api-docs.md           # API文档
├── README_guild_members.md          # 详细使用说明
└── PROJECT_SUMMARY.md               # 项目总结（本文件）
```

## 核心功能

### 1. 公会成员信息获取
- 从CSV文件读取公会成员基本信息
- 使用魔兽世界API获取详细角色信息
- 支持批量获取多个成员信息
- 自动保存结果到JSON文件

### 2. API连接测试
- 验证API连接是否正常
- 测试cookie token是否有效
- 显示详细的请求和响应信息

### 3. 用户友好的界面
- 菜单式操作界面
- 详细的使用说明
- 完善的错误处理

## 技术特点

### API集成
- 使用魔兽世界官方角色信息API
- 支持cookie认证
- 完整的请求头设置
- 错误处理和重试机制

### 数据处理
- CSV文件读取和解析
- JSON数据格式化和保存
- 中文字符编码处理
- 数据验证和清洗

### 用户体验
- 详细的控制台输出
- 进度显示和状态反馈
- 配置参数可调整
- 完整的错误提示

## 使用方法

### 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **获取Cookie Token**
   - 访问 https://wow.blizzard.cn/
   - 登录账号
   - 从浏览器开发者工具中获取 `blizzard_user_info` cookie值

3. **运行工具**
   ```bash
   python run_guild_tool.py
   ```

### 功能选择

- **选项1**: 测试API连接
- **选项2**: 获取公会成员详细信息
- **选项3**: 查看使用说明
- **选项4**: 退出程序

## 配置说明

### 主要配置参数

```python
CSV_FILE = "data/guildmember.csv"      # 公会成员CSV文件路径
OUTPUT_FILE = "guild_members_detailed.json"  # 输出文件路径
REALM_SLUG = "arthas"                  # 服务器标识符
MEMBER_LIMIT = 10                      # 获取成员数量限制
```

### API配置

```python
BASE_URL = "https://webapi.blizzard.cn/wow-armory-server/api/index"
REQUEST_TIMEOUT = 10                   # 请求超时时间
REQUEST_DELAY = 1                      # 请求间隔时间
```

## 输出格式

### JSON输出示例

```json
[
  {
    "name": "快来骑我吧",
    "rank": "暗索高级特工",
    "level": "80",
    "class": "唤魔师",
    "race": "龙希尔",
    "sex": "Female",
    "last_online": "0.02",
    "faction": "Horde",
    "detailed_info": {
      "character_summary": {
        "name": "快来骑我吧",
        "level": 80,
        "average_item_level": 676,
        "equipped_item_level": 675,
        "achievement_points": 19840,
        "active_spec": {
          "name": "湮灭"
        },
        "guild": {
          "name": "一起"
        }
      }
    }
  }
]
```

## 获取的信息类型

### 基本信息（来自CSV）
- 角色名称
- 公会职位
- 等级
- 职业
- 种族
- 性别
- 最后在线时间
- 阵营

### 详细信息（来自API）
- 平均装备等级
- 已装备装备等级
- 成就点数
- 当前专精
- 公会信息
- 最后登录时间戳
- 盟约进度
- 称号信息

## 错误处理

### 网络错误
- 请求超时处理
- 连接失败重试
- 网络异常提示

### API错误
- 认证失败处理
- 角色不存在处理
- 权限不足处理

### 数据错误
- CSV文件格式验证
- JSON解析错误处理
- 编码问题处理

## 性能优化

### 请求优化
- 会话复用
- 请求间隔控制
- 超时设置

### 内存优化
- 流式处理
- 及时释放资源
- 批量处理

## 安全考虑

### 认证安全
- Cookie token验证
- 请求头完整性
- 域名限制

### 数据安全
- 本地文件存储
- 敏感信息保护
- 错误信息脱敏

## 扩展性

### 功能扩展
- 支持更多API端点
- 添加数据分析功能
- 支持更多数据格式

### 配置扩展
- 支持配置文件
- 环境变量支持
- 命令行参数

## 维护说明

### 定期维护
- 检查API变更
- 更新依赖版本
- 测试功能完整性

### 问题排查
- 查看错误日志
- 验证网络连接
- 检查认证状态

## 技术支持

### 常见问题
1. Cookie token过期
2. 网络连接问题
3. 文件权限问题
4. 编码问题

### 解决方案
- 重新获取cookie token
- 检查网络连接
- 确认文件权限
- 使用UTF-8编码

## 更新日志

### v1.0.0 (当前版本)
- 初始版本发布
- 支持基础角色信息获取
- 完整的错误处理机制
- 用户友好的界面

### 计划功能
- 支持更多服务器
- 添加数据分析功能
- 支持导出更多格式
- 添加图形界面

## 许可证

本项目仅供学习和研究使用，请遵守魔兽世界官方服务条款。

## 联系方式

如有问题或建议，请通过以下方式联系：
- 项目仓库：GitHub
- 邮箱：support@example.com

---

**注意**: 使用本工具时请确保遵守魔兽世界官方服务条款和相关法律法规。 