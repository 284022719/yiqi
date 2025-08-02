#!/usr/bin/env python3
"""
魔兽世界公会网站项目主程序
重构后的统一入口
"""

import argparse
import sys
from pathlib import Path

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.crawler.mounts_crawler import create_mounts_crawler
from src.stats.generator import create_stats_generator
from src.utils.logger import get_logger


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="魔兽世界公会网站项目")
    parser.add_argument(
        "command", 
        choices=["crawl", "stats", "all"],
        help="执行命令: crawl(爬取数据), stats(生成统计), all(全部执行)"
    )
    parser.add_argument(
        "--workers", 
        type=int, 
        default=4,
        help="并发工作线程数 (默认: 4)"
    )
    parser.add_argument(
        "--headless", 
        action="store_true",
        help="使用无头模式运行浏览器"
    )
    
    args = parser.parse_args()
    
    logger = get_logger("main")
    logger.info("=" * 60)
    logger.info("魔兽世界公会网站项目启动")
    logger.info("=" * 60)
    
    try:
        if args.command == "crawl":
            run_crawler(args.workers)
        elif args.command == "stats":
            run_stats_generator()
        elif args.command == "all":
            run_crawler(args.workers)
            run_stats_generator()
        
        logger.info("=" * 60)
        logger.info("程序执行完成")
        logger.info("=" * 60)
        
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序执行失败: {e}")
        sys.exit(1)


def run_crawler(max_workers: int):
    """运行爬虫"""
    logger = get_logger("main")
    logger.info("开始执行爬虫任务...")
    
    crawler = create_mounts_crawler(max_workers)
    results = crawler.crawl_mounts_data()
    
    if results:
        logger.info(f"爬虫任务完成，共处理 {len(results)} 个角色")
    else:
        logger.warning("爬虫任务未返回结果")


def run_stats_generator():
    """运行统计生成器"""
    logger = get_logger("main")
    logger.info("开始生成统计数据...")
    
    generator = create_stats_generator()
    
    # 生成基础统计
    basic_stats = generator.generate_basic_stats()
    if basic_stats:
        logger.info("基础统计数据生成完成")
    
    # 生成扩展统计
    extended_stats = generator.generate_extended_stats()
    if extended_stats:
        logger.info("扩展统计数据生成完成")


if __name__ == "__main__":
    main() 