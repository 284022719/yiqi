"""
项目配置文件
包含所有配置项和常量
"""

import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
ASSETS_DIR = PROJECT_ROOT / "assets"

# 确保目录存在
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# 爬虫配置
CRAWLER_CONFIG = {
    "max_workers": 4,  # 并发数
    "timeout": 10,     # 请求超时时间
    "retry_times": 3,  # 重试次数
    "wait_time": 3,    # 页面等待时间
    "headless": True,  # 无头模式
}

# 浏览器配置
BROWSER_CONFIG = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "window_size": "1920,1080",
    "chrome_options": [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--disable-web-security",
        "--disable-features=VizDisplayCompositor"
    ]
}

# 数据文件配置
DATA_FILES = {
    "csv_primary": DATA_DIR / "1.csv",
    "csv_extended": DATA_DIR / "guildmember.csv",
    "json_mounts": DATA_DIR / "guildmember.json",
    "json_stats": DATA_DIR / "recent_stats.json",
    "json_extended_stats": DATA_DIR / "extended_stats.json",
    "json_server_mapping": DATA_DIR / "server_mapping.json"
}

# 服务器映射配置
SERVER_MAPPING = {
    '阿尔萨斯': 'arthas',
    '死亡之翼': 'deathwing',
    '阿克蒙德': 'archimonde',
    '国王之谷': 'king\'s-valley',
    '凤凰之神': 'phoenix',
    '白银之手': 'silver-hand',
    '冬泉谷': 'winterspring',
    '塞拉摩': 'theramore',
    '克尔苏加德': 'kel\'thuzad',
    '符文图腾': 'runetotem',
    '暴风祭坛': 'altar-of-storms',
    '伊利丹': 'illidan',
    '安苏': 'anzu',
    '红龙军团': 'red-dragonflight',
    '苏拉玛': 'suramar',
    '瓦里安': 'varian',
    '斯克提斯': 'skettis',
    '恶魔之翼': 'demon-wing',
    '黑暗魅影': 'dark-shadow',
    '丽丽（四川）': 'lili-sichuan'
}

# 网站配置
WEBSITE_CONFIG = {
    "title": "魔兽世界公会网站",
    "description": "公会统计、攻略分享、成员管理",
    "base_url": "https://wow.blizzard.cn",
    "character_url_template": "https://wow.blizzard.cn/character/#/{server}/{name}/collections/mounts"
}

# 日志配置
LOGGING_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file_format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
}

# 统计配置
STATS_CONFIG = {
    "max_online_days": 150,  # 最大上线天数
    "min_level": 80,         # 最小等级
    "top_ranking_count": 10, # 排行榜显示数量
    "chart_colors": {
        "primary": "#4CAF50",
        "secondary": "#2196F3",
        "accent": "#FF9800",
        "success": "#4CAF50",
        "warning": "#FF9800",
        "error": "#F44336"
    }
} 