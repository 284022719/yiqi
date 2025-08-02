# 公会Mythic+ Score分析工具

这个项目包含两个Python脚本，用于分析公会成员中Mythic+ Score最高的角色信息。

## 文件说明

- `data/guildmember.csv` - 公会成员数据文件
- `get_top_mplus_players_simple.py` - 简化版本，无需API密钥，只显示CSV中的基础信息
- `get_top_mplus_players.py` - 完整版本，需要Battle.net API密钥，可获取详细角色信息
- `requirements.txt` - Python依赖包列表

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行简化版本（推荐）

```bash
python3 get_top_mplus_players_simple.py
```

这个版本会：
- 读取CSV文件中的公会成员数据
- 按Mythic+ Score排序，显示前10名角色
- 提供详细的统计信息
- 将结果保存到 `top_mplus_players_result.csv`

### 3. 运行完整版本（需要API密钥）

```bash
python3 get_top_mplus_players.py
```

这个版本会：
- 要求输入Battle.net API密钥
- 通过mythic-keystone-api获取每个角色的详细信息
- 显示角色的装备、专精、Mythic+记录等
- 将结果保存到 `top_mplus_players_result.json`

## 当前分析结果

根据最新的公会数据，Mythic+ Score最高的10个角色是：

| 排名 | 角色名 | 职业 | 种族 | 分数 | 阵营 | 公会职位 |
|------|--------|------|------|------|------|----------|
| 1 | Meteorra | 法师 | 矮人 | 3798 | Alliance | 暗索高级特工 |
| 2 | 西途 | 德鲁伊 | 暗夜精灵 | 3647 | Alliance | 暗索高级特工 |
| 3 | 妙不可言 | 猎人 | 玛格汉兽人 | 3593 | Horde | 加乐宫白金会员 |
| 4 | 华师傅 | 死亡骑士 | 血精灵 | 3577 | Horde | 加乐宫白金会员 |
| 5 | 白鯨 | 牧师 | 幻容 | 3567 | Alliance | 加乐宫白金会员 |
| 6 | 久世 | 法师 | 玛格汉兽人 | 3552 | Horde | 加乐宫白金会员 |
| 7 | 你也曾心动吧 | 圣骑士 | 牛头人 | 3544 | Horde | 锈水财阀合同工 |
| 8 | 狮萨 | 死亡骑士 | 血精灵 | 3535 | Horde | 加乐宫白金会员 |
| 9 | Pro | 潜行者 | 亡灵 | 3532 | Horde | 锈水财阀合同工 |
| 10 | 樱桃牛奶酱 | 牧师 | 血精灵 | 3492 | Horde | 安德麦滴滴司机 |

## 统计信息

- **公会总成员数**: 956人
- **有Mythic+ Score的成员**: 275人
- **平均Mythic+ Score**: 563.18
- **最高Mythic+ Score**: 3798

### 前10名职业分布
- 法师: 2人
- 死亡骑士: 2人
- 牧师: 2人
- 德鲁伊: 1人
- 猎人: 1人
- 圣骑士: 1人
- 潜行者: 1人

### 前10名阵营分布
- Horde: 7人
- Alliance: 3人

## 获取Battle.net API密钥

如需使用完整版本获取详细角色信息，需要：

1. 访问 [Battle.net Developer Portal](https://develop.battle.net/)
2. 创建应用程序
3. 获取Client ID和Client Secret
4. 使用OAuth2流程获取访问令牌

## 注意事项

- 简化版本无需任何API密钥，可直接运行
- 完整版本需要有效的Battle.net API访问令牌
- API调用有频率限制，脚本已添加延迟以避免超限
- 结果文件会保存在当前目录下

## 输出文件

- `top_mplus_players_result.csv` - 简化版本的结果（CSV格式）
- `top_mplus_players_result.json` - 完整版本的结果（JSON格式，包含API数据） 