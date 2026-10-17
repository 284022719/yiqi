#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试并发坐骑爬取功能
"""

import time
from mounts_crawler import MountsCrawler
from config import config

def test_concurrent_crawling():
    """测试并发爬取功能"""
    print("=== 测试并发坐骑爬取功能 ===")
    
    # 设置并发数为12
    config.set("crawler.max_concurrent", 12)
    config.set("crawler.delay_between_requests", 1)  # 减少延迟以加快测试
    
    # 创建爬虫实例（数据库路径由 paths.py 解析）
    crawler = MountsCrawler()
    
    # 获取前10个角色进行测试
    characters = crawler.db_manager.get_all_characters()[:10]
    
    if not characters:
        print("❌ 没有找到角色数据")
        return False
    
    print(f"测试角色数量: {len(characters)}")
    print(f"并发数: {crawler.max_concurrent}")
    print("开始测试...")
    
    start_time = time.time()
    
    # 使用线程池进行并发爬取
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    completed_count = 0
    with ThreadPoolExecutor(max_workers=crawler.max_concurrent) as executor:
        # 提交所有任务
        future_to_character = {
            executor.submit(crawler.crawl_character_mounts, character): character 
            for character in characters
        }
        
        # 处理完成的任务
        for future in as_completed(future_to_character):
            character = future_to_character[future]
            completed_count += 1
            
            try:
                success = future.result()
                character_name = character.get('name', 'Unknown')
                status = "✅" if success else "❌"
                print(f"{status} {completed_count}/{len(characters)} - {character_name}")
                
            except Exception as e:
                print(f"❌ 处理角色 {character.get('name', 'Unknown')} 时发生异常: {e}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n测试完成！")
    print(f"总耗时: {duration:.2f} 秒")
    print(f"平均每个角色: {duration/len(characters):.2f} 秒")
    print(f"并发效率提升: {(len(characters) * 2) / duration:.1f}x")  # 假设串行每个角色2秒
    
    return True

if __name__ == '__main__':
    test_concurrent_crawling() 