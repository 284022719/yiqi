import os
import glob
from datetime import datetime

def list_log_files():
    """列出所有日志文件"""
    if not os.path.exists('logs'):
        print("❌ logs文件夹不存在，请先运行爬虫程序")
        return []
    
    log_files = glob.glob('logs/*.log')
    log_files.sort(reverse=True)  # 按时间倒序排列
    
    if not log_files:
        print("❌ 没有找到日志文件")
        return []
    
    print("📝 可用的日志文件：")
    print("=" * 50)
    for i, log_file in enumerate(log_files, 1):
        file_size = os.path.getsize(log_file)
        file_time = datetime.fromtimestamp(os.path.getmtime(log_file))
        print(f"{i}. {log_file}")
        print(f"   大小: {file_size} 字节")
        print(f"   时间: {file_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
    
    return log_files

def view_log_file(log_file):
    """查看指定日志文件的内容"""
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"📖 日志文件内容：{log_file}")
        print("=" * 60)
        print(content)
        
    except Exception as e:
        print(f"❌ 读取日志文件失败：{e}")

def analyze_log_file(log_file):
    """分析日志文件，提取关键信息"""
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"📊 日志分析：{log_file}")
        print("=" * 60)
        
        # 统计信息
        total_lines = len(lines)
        error_lines = [line for line in lines if 'ERROR' in line]
        warning_lines = [line for line in lines if 'WARNING' in line]
        info_lines = [line for line in lines if 'INFO' in line]
        
        print(f"总行数：{total_lines}")
        print(f"错误数：{len(error_lines)}")
        print(f"警告数：{len(warning_lines)}")
        print(f"信息数：{len(info_lines)}")
        print()
        
        # 显示错误信息
        if error_lines:
            print("🚨 错误信息：")
            print("-" * 30)
            for error in error_lines[-5:]:  # 显示最后5个错误
                print(error.strip())
            print()
        
        # 显示警告信息
        if warning_lines:
            print("⚠️ 警告信息：")
            print("-" * 30)
            for warning in warning_lines[-3:]:  # 显示最后3个警告
                print(warning.strip())
            print()
        
        # 显示成功/失败统计
        success_count = 0
        failed_count = 0
        for line in lines:
            if '处理完成，状态：成功' in line:
                success_count += 1
            elif '处理完成，状态：失败' in line:
                failed_count += 1
        
        if success_count > 0 or failed_count > 0:
            print("📈 处理结果统计：")
            print("-" * 30)
            print(f"成功：{success_count} 个角色")
            print(f"失败：{failed_count} 个角色")
            if success_count + failed_count > 0:
                success_rate = success_count / (success_count + failed_count) * 100
                print(f"成功率：{success_rate:.1f}%")
        
    except Exception as e:
        print(f"❌ 分析日志文件失败：{e}")

def main():
    """主函数"""
    print("🔍 魔兽世界坐骑爬虫日志查看器")
    print("=" * 50)
    
    # 列出日志文件
    log_files = list_log_files()
    
    if not log_files:
        return
    
    while True:
        print("\n请选择操作：")
        print("1. 查看最新日志文件")
        print("2. 查看指定日志文件")
        print("3. 分析最新日志文件")
        print("4. 分析指定日志文件")
        print("5. 退出")
        
        choice = input("\n请输入选择 (1-5): ").strip()
        
        if choice == '1':
            if log_files:
                view_log_file(log_files[0])
        
        elif choice == '2':
            if log_files:
                print("\n请输入日志文件编号：")
                for i, log_file in enumerate(log_files, 1):
                    print(f"{i}. {os.path.basename(log_file)}")
                
                try:
                    file_num = int(input("编号: ")) - 1
                    if 0 <= file_num < len(log_files):
                        view_log_file(log_files[file_num])
                    else:
                        print("❌ 无效的编号")
                except ValueError:
                    print("❌ 请输入有效的数字")
        
        elif choice == '3':
            if log_files:
                analyze_log_file(log_files[0])
        
        elif choice == '4':
            if log_files:
                print("\n请输入日志文件编号：")
                for i, log_file in enumerate(log_files, 1):
                    print(f"{i}. {os.path.basename(log_file)}")
                
                try:
                    file_num = int(input("编号: ")) - 1
                    if 0 <= file_num < len(log_files):
                        analyze_log_file(log_files[file_num])
                    else:
                        print("❌ 无效的编号")
                except ValueError:
                    print("❌ 请输入有效的数字")
        
        elif choice == '5':
            print("👋 再见！")
            break
        
        else:
            print("❌ 无效的选择，请重新输入")

if __name__ == "__main__":
    main() 