#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session07 示例5：目录操作和文件管理

本示例演示了Python中的目录操作和文件管理，包括：
- 目录的创建、删除和遍历
- 文件的复制、移动和重命名
- 批量文件操作
- 文件权限和属性管理
- 目录树的操作

作者: Python教程团队
创建日期: 2024-12-22
"""

import os
import shutil
import glob
from pathlib import Path
from datetime import datetime
import stat
import tempfile


def create_directory_structure():
    """
    创建示例目录结构
    """
    print("=== 创建目录结构 ===")
    
    # 使用os.makedirs创建多级目录
    base_dir = 'file_management_demo'
    directories = [
        'documents/reports/2024',
        'documents/templates',
        'images/photos/vacation',
        'images/graphics',
        'backup/daily',
        'backup/weekly',
        'temp/processing',
        'logs/application',
        'logs/system'
    ]
    
    print(f"创建基础目录: {base_dir}")
    
    for directory in directories:
        full_path = os.path.join(base_dir, directory)
        os.makedirs(full_path, exist_ok=True)
        print(f"✓ 创建目录: {full_path}")
    
    # 使用pathlib创建目录
    pathlib_dirs = [
        'config/database',
        'config/security',
        'data/input',
        'data/output',
        'scripts/automation'
    ]
    
    for directory in pathlib_dirs:
        full_path = Path(base_dir) / directory
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ 创建目录(pathlib): {full_path}")
    
    return base_dir


def create_sample_files(base_dir):
    """
    创建示例文件
    """
    print(f"\n=== 在 {base_dir} 中创建示例文件 ===")
    
    # 创建不同类型的文件
    files_to_create = [
        ('documents/reports/2024/annual_report.txt', '2024年度报告\n这是年度总结报告的内容。'),
        ('documents/reports/2024/monthly_report.txt', '月度报告\n这是月度报告的内容。'),
        ('documents/templates/letter_template.txt', '信件模板\n尊敬的[姓名]，\n\n[内容]\n\n此致\n敬礼'),
        ('config/database/db_config.txt', 'host=localhost\nport=5432\ndatabase=myapp'),
        ('config/security/security_config.txt', 'encryption=AES256\ntimeout=3600'),
        ('data/input/data1.csv', 'name,age,city\n张三,25,北京\n李四,30,上海'),
        ('data/input/data2.csv', 'product,price,stock\n笔记本,5999,50\n鼠标,199,100'),
        ('logs/application/app.log', f'{datetime.now()}: 应用启动\n{datetime.now()}: 用户登录'),
        ('logs/system/system.log', f'{datetime.now()}: 系统启动\n{datetime.now()}: 内存使用率: 45%'),
        ('scripts/automation/backup.py', '#!/usr/bin/env python3\nprint("备份脚本")'),
        ('temp/processing/temp_data.txt', '临时处理数据\n这是临时文件内容。')
    ]
    
    created_files = []
    
    for file_path, content in files_to_create:
        full_path = os.path.join(base_dir, file_path)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # 创建文件
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        created_files.append(full_path)
        print(f"✓ 创建文件: {file_path}")
    
    # 创建一些二进制文件（模拟）
    binary_files = [
        'images/photos/vacation/photo1.jpg',
        'images/photos/vacation/photo2.jpg',
        'images/graphics/logo.png'
    ]
    
    for file_path in binary_files:
        full_path = os.path.join(base_dir, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # 创建模拟的二进制文件
        with open(full_path, 'wb') as f:
            f.write(b'\x89PNG\r\n\x1a\n' + b'模拟图片数据' * 100)
        
        created_files.append(full_path)
        print(f"✓ 创建二进制文件: {file_path}")
    
    print(f"\n总共创建了 {len(created_files)} 个文件")
    return created_files


def explore_directory_structure(base_dir):
    """
    探索目录结构
    """
    print(f"\n=== 探索目录结构: {base_dir} ===")
    
    # 方法1: 使用os.walk遍历
    print("\n使用 os.walk() 遍历:")
    total_dirs = 0
    total_files = 0
    
    for root, dirs, files in os.walk(base_dir):
        level = root.replace(base_dir, '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")
            total_files += 1
        
        total_dirs += len(dirs)
    
    print(f"\n统计: {total_dirs} 个目录, {total_files} 个文件")
    
    # 方法2: 使用pathlib遍历
    print("\n使用 pathlib 遍历:")
    base_path = Path(base_dir)
    
    def print_tree(path, prefix=""):
        """递归打印目录树"""
        if path.is_dir():
            print(f"{prefix}{path.name}/")
            children = sorted(path.iterdir())
            for i, child in enumerate(children):
                is_last = i == len(children) - 1
                new_prefix = prefix + ("    " if is_last else "│   ")
                child_prefix = prefix + ("└── " if is_last else "├── ")
                
                if child.is_dir():
                    print(f"{child_prefix}{child.name}/")
                    print_tree(child, new_prefix)
                else:
                    print(f"{child_prefix}{child.name}")
        else:
            print(f"{prefix}{path.name}")
    
    print_tree(base_path)
    
    # 方法3: 使用glob模式匹配
    print("\n使用 glob 模式匹配:")
    
    # 查找所有.txt文件
    txt_files = glob.glob(os.path.join(base_dir, '**', '*.txt'), recursive=True)
    print(f"找到 {len(txt_files)} 个.txt文件:")
    for file in txt_files:
        rel_path = os.path.relpath(file, base_dir)
        print(f"  {rel_path}")
    
    # 查找所有日志文件
    log_files = glob.glob(os.path.join(base_dir, '**', '*.log'), recursive=True)
    print(f"\n找到 {len(log_files)} 个.log文件:")
    for file in log_files:
        rel_path = os.path.relpath(file, base_dir)
        print(f"  {rel_path}")
    
    # 查找特定目录下的文件
    config_files = glob.glob(os.path.join(base_dir, 'config', '**', '*'), recursive=True)
    config_files = [f for f in config_files if os.path.isfile(f)]
    print(f"\n配置目录下有 {len(config_files)} 个文件:")
    for file in config_files:
        rel_path = os.path.relpath(file, base_dir)
        print(f"  {rel_path}")


def file_operations_demo(base_dir):
    """
    文件操作演示
    """
    print(f"\n=== 文件操作演示: {base_dir} ===")
    
    # 1. 文件复制
    print("\n1. 文件复制操作:")
    
    source_file = os.path.join(base_dir, 'documents', 'templates', 'letter_template.txt')
    
    # 复制到backup目录
    backup_file = os.path.join(base_dir, 'backup', 'daily', 'letter_template_backup.txt')
    shutil.copy2(source_file, backup_file)
    print(f"✓ 复制文件: {os.path.relpath(source_file, base_dir)} -> {os.path.relpath(backup_file, base_dir)}")
    
    # 复制整个目录
    source_dir = os.path.join(base_dir, 'documents', 'reports')
    backup_reports_dir = os.path.join(base_dir, 'backup', 'weekly', 'reports_backup')
    shutil.copytree(source_dir, backup_reports_dir)
    print(f"✓ 复制目录: {os.path.relpath(source_dir, base_dir)} -> {os.path.relpath(backup_reports_dir, base_dir)}")
    
    # 2. 文件移动和重命名
    print("\n2. 文件移动和重命名:")
    
    # 创建一个临时文件用于移动
    temp_file = os.path.join(base_dir, 'temp', 'temp_file.txt')
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write('这是一个临时文件')
    
    # 移动文件
    moved_file = os.path.join(base_dir, 'documents', 'moved_file.txt')
    shutil.move(temp_file, moved_file)
    print(f"✓ 移动文件: {os.path.relpath(temp_file, base_dir)} -> {os.path.relpath(moved_file, base_dir)}")
    
    # 重命名文件
    renamed_file = os.path.join(base_dir, 'documents', 'renamed_document.txt')
    os.rename(moved_file, renamed_file)
    print(f"✓ 重命名文件: {os.path.relpath(moved_file, base_dir)} -> {os.path.relpath(renamed_file, base_dir)}")
    
    # 3. 文件删除
    print("\n3. 文件删除操作:")
    
    # 删除单个文件
    if os.path.exists(renamed_file):
        os.remove(renamed_file)
        print(f"✓ 删除文件: {os.path.relpath(renamed_file, base_dir)}")
    
    # 删除空目录
    empty_dir = os.path.join(base_dir, 'temp', 'empty_dir')
    os.makedirs(empty_dir, exist_ok=True)
    os.rmdir(empty_dir)
    print(f"✓ 删除空目录: {os.path.relpath(empty_dir, base_dir)}")
    
    # 4. 批量文件操作
    print("\n4. 批量文件操作:")
    
    # 批量重命名文件（添加前缀）
    images_dir = os.path.join(base_dir, 'images', 'photos', 'vacation')
    for filename in os.listdir(images_dir):
        if filename.endswith('.jpg'):
            old_path = os.path.join(images_dir, filename)
            new_filename = f"vacation_{filename}"
            new_path = os.path.join(images_dir, new_filename)
            os.rename(old_path, new_path)
            print(f"✓ 重命名: {filename} -> {new_filename}")
    
    # 批量创建文件
    batch_dir = os.path.join(base_dir, 'data', 'batch_files')
    os.makedirs(batch_dir, exist_ok=True)
    
    for i in range(1, 6):
        batch_file = os.path.join(batch_dir, f"batch_file_{i:02d}.txt")
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(f"这是批量创建的文件 #{i}\n创建时间: {datetime.now()}")
        print(f"✓ 创建批量文件: batch_file_{i:02d}.txt")


def file_attributes_demo(base_dir):
    """
    文件属性和权限演示
    """
    print(f"\n=== 文件属性和权限演示: {base_dir} ===")
    
    # 选择一个文件进行演示
    demo_file = os.path.join(base_dir, 'documents', 'reports', '2024', 'annual_report.txt')
    
    if os.path.exists(demo_file):
        print(f"\n分析文件: {os.path.relpath(demo_file, base_dir)}")
        
        # 获取文件统计信息
        file_stat = os.stat(demo_file)
        
        print(f"文件大小: {file_stat.st_size} 字节")
        print(f"创建时间: {datetime.fromtimestamp(file_stat.st_ctime)}")
        print(f"修改时间: {datetime.fromtimestamp(file_stat.st_mtime)}")
        print(f"访问时间: {datetime.fromtimestamp(file_stat.st_atime)}")
        
        # 文件权限（在Windows上可能不完全适用）
        mode = file_stat.st_mode
        print(f"文件模式: {oct(mode)}")
        print(f"是否为文件: {stat.S_ISREG(mode)}")
        print(f"是否为目录: {stat.S_ISDIR(mode)}")
        
        # 使用pathlib获取信息
        path_obj = Path(demo_file)
        print(f"\n使用pathlib获取信息:")
        print(f"文件名: {path_obj.name}")
        print(f"文件扩展名: {path_obj.suffix}")
        print(f"父目录: {path_obj.parent}")
        print(f"绝对路径: {path_obj.absolute()}")
        print(f"是否存在: {path_obj.exists()}")
        print(f"是否为文件: {path_obj.is_file()}")
        print(f"是否为目录: {path_obj.is_dir()}")
        
        # 修改文件时间戳
        print(f"\n修改文件时间戳:")
        current_time = datetime.now().timestamp()
        os.utime(demo_file, (current_time, current_time))
        print(f"✓ 更新文件访问和修改时间")
        
        # 再次检查修改时间
        new_stat = os.stat(demo_file)
        print(f"新的修改时间: {datetime.fromtimestamp(new_stat.st_mtime)}")


def directory_size_analysis(base_dir):
    """
    目录大小分析
    """
    print(f"\n=== 目录大小分析: {base_dir} ===")
    
    def get_directory_size(path):
        """计算目录总大小"""
        total_size = 0
        file_count = 0
        
        for dirpath, dirnames, filenames in os.walk(path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                try:
                    file_size = os.path.getsize(file_path)
                    total_size += file_size
                    file_count += 1
                except (OSError, FileNotFoundError):
                    # 处理无法访问的文件
                    pass
        
        return total_size, file_count
    
    def format_size(size_bytes):
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
    
    # 分析各个子目录
    subdirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    print("各子目录大小分析:")
    total_size = 0
    total_files = 0
    
    dir_sizes = []
    
    for subdir in subdirs:
        subdir_path = os.path.join(base_dir, subdir)
        size, file_count = get_directory_size(subdir_path)
        dir_sizes.append((subdir, size, file_count))
        total_size += size
        total_files += file_count
        
        print(f"  {subdir:15} : {format_size(size):>10} ({file_count} 个文件)")
    
    print(f"\n总计: {format_size(total_size)} ({total_files} 个文件)")
    
    # 按大小排序
    print("\n按大小排序（从大到小）:")
    dir_sizes.sort(key=lambda x: x[1], reverse=True)
    for dirname, size, file_count in dir_sizes:
        percentage = (size / total_size * 100) if total_size > 0 else 0
        print(f"  {dirname:15} : {format_size(size):>10} ({percentage:5.1f}%)")


def file_search_demo(base_dir):
    """
    文件搜索演示
    """
    print(f"\n=== 文件搜索演示: {base_dir} ===")
    
    # 1. 按文件名搜索
    print("\n1. 按文件名搜索:")
    
    def find_files_by_name(directory, pattern):
        """按文件名模式搜索文件"""
        found_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if pattern.lower() in file.lower():
                    found_files.append(os.path.join(root, file))
        return found_files
    
    # 搜索包含"report"的文件
    report_files = find_files_by_name(base_dir, "report")
    print(f"包含'report'的文件 ({len(report_files)}个):")
    for file in report_files:
        rel_path = os.path.relpath(file, base_dir)
        print(f"  {rel_path}")
    
    # 2. 按文件扩展名搜索
    print("\n2. 按文件扩展名搜索:")
    
    def find_files_by_extension(directory, extension):
        """按扩展名搜索文件"""
        pattern = f"**/*{extension}"
        return glob.glob(os.path.join(directory, pattern), recursive=True)
    
    # 搜索所有.txt文件
    txt_files = find_files_by_extension(base_dir, ".txt")
    print(f"所有.txt文件 ({len(txt_files)}个):")
    for file in txt_files:
        rel_path = os.path.relpath(file, base_dir)
        file_size = os.path.getsize(file)
        print(f"  {rel_path} ({file_size} 字节)")
    
    # 3. 按文件大小搜索
    print("\n3. 按文件大小搜索:")
    
    def find_files_by_size(directory, min_size=0, max_size=float('inf')):
        """按文件大小搜索文件"""
        found_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    if min_size <= file_size <= max_size:
                        found_files.append((file_path, file_size))
                except OSError:
                    pass
        return found_files
    
    # 搜索大于1KB的文件
    large_files = find_files_by_size(base_dir, min_size=1024)
    print(f"大于1KB的文件 ({len(large_files)}个):")
    for file_path, file_size in large_files:
        rel_path = os.path.relpath(file_path, base_dir)
        print(f"  {rel_path} ({file_size} 字节)")
    
    # 4. 按修改时间搜索
    print("\n4. 按修改时间搜索:")
    
    def find_recent_files(directory, hours=24):
        """查找最近修改的文件"""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        recent_files = []
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    mtime = os.path.getmtime(file_path)
                    if mtime > cutoff_time:
                        recent_files.append((file_path, mtime))
                except OSError:
                    pass
        
        return recent_files
    
    # 查找最近24小时修改的文件
    recent_files = find_recent_files(base_dir, hours=24)
    print(f"最近24小时修改的文件 ({len(recent_files)}个):")
    for file_path, mtime in recent_files:
        rel_path = os.path.relpath(file_path, base_dir)
        mod_time = datetime.fromtimestamp(mtime)
        print(f"  {rel_path} (修改时间: {mod_time.strftime('%Y-%m-%d %H:%M:%S')})")


def temporary_files_demo():
    """
    临时文件和目录演示
    """
    print("\n=== 临时文件和目录演示 ===")
    
    # 1. 创建临时文件
    print("\n1. 临时文件操作:")
    
    # 使用tempfile.NamedTemporaryFile
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', prefix='demo_', delete=False, encoding='utf-8') as temp_file:
        temp_file.write("这是一个临时文件的内容\n")
        temp_file.write(f"创建时间: {datetime.now()}\n")
        temp_filename = temp_file.name
        print(f"✓ 创建临时文件: {temp_filename}")
    
    # 读取临时文件
    with open(temp_filename, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"临时文件内容:\n{content}")
    
    # 删除临时文件
    os.unlink(temp_filename)
    print(f"✓ 删除临时文件: {temp_filename}")
    
    # 2. 创建临时目录
    print("\n2. 临时目录操作:")
    
    with tempfile.TemporaryDirectory(prefix='demo_dir_') as temp_dir:
        print(f"✓ 创建临时目录: {temp_dir}")
        
        # 在临时目录中创建文件
        temp_files = []
        for i in range(3):
            temp_file_path = os.path.join(temp_dir, f"temp_file_{i}.txt")
            with open(temp_file_path, 'w', encoding='utf-8') as f:
                f.write(f"临时文件 {i} 的内容")
            temp_files.append(temp_file_path)
            print(f"  ✓ 创建: {os.path.basename(temp_file_path)}")
        
        # 列出临时目录内容
        print(f"临时目录内容:")
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                print(f"  文件: {item} ({size} 字节)")
            else:
                print(f"  目录: {item}/")
    
    print("✓ 临时目录已自动清理")
    
    # 3. 获取系统临时目录
    print("\n3. 系统临时目录信息:")
    
    system_temp_dir = tempfile.gettempdir()
    print(f"系统临时目录: {system_temp_dir}")
    
    # 创建唯一的临时文件名
    temp_fd, temp_path = tempfile.mkstemp(suffix='.log', prefix='app_')
    print(f"唯一临时文件: {temp_path}")
    
    # 写入临时文件
    with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
        f.write(f"应用日志\n时间: {datetime.now()}\n")
    
    # 读取并删除
    with open(temp_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"临时日志内容: {content.strip()}")
    
    os.unlink(temp_path)
    print(f"✓ 清理临时文件: {temp_path}")


def cleanup_demo_files(base_dir):
    """
    清理演示文件
    """
    print(f"\n=== 清理演示文件: {base_dir} ===")
    
    if os.path.exists(base_dir):
        # 计算要删除的文件和目录数量
        total_files = 0
        total_dirs = 0
        
        for root, dirs, files in os.walk(base_dir):
            total_files += len(files)
            total_dirs += len(dirs)
        
        print(f"准备删除: {total_files} 个文件, {total_dirs} 个目录")
        
        # 删除整个目录树
        shutil.rmtree(base_dir)
        print(f"✓ 已删除目录: {base_dir}")
    else:
        print(f"目录不存在: {base_dir}")


def main():
    """
    主函数
    """
    print("Session07 示例5：目录操作和文件管理")
    print("=" * 50)
    
    try:
        # 1. 创建目录结构
        base_dir = create_directory_structure()
        
        # 2. 创建示例文件
        created_files = create_sample_files(base_dir)
        
        # 3. 探索目录结构
        explore_directory_structure(base_dir)
        
        # 4. 文件操作演示
        file_operations_demo(base_dir)
        
        # 5. 文件属性演示
        file_attributes_demo(base_dir)
        
        # 6. 目录大小分析
        directory_size_analysis(base_dir)
        
        # 7. 文件搜索演示
        file_search_demo(base_dir)
        
        # 8. 临时文件演示
        temporary_files_demo()
        
        print("\n" + "=" * 50)
        print("✅ 示例5演示完成！")
        print("\n💡 重要提示：")
        print("- 使用os.makedirs()创建多级目录")
        print("- 使用shutil模块进行高级文件操作")
        print("- 使用glob模块进行模式匹配搜索")
        print("- 使用tempfile模块处理临时文件")
        print("- 注意处理文件操作中的异常")
        print("- pathlib提供了更现代的路径操作方式")
        
        # 询问是否清理文件
        response = input("\n是否清理演示文件和目录？(y/n): ").lower().strip()
        if response == 'y':
            cleanup_demo_files(base_dir)
        else:
            print(f"演示文件已保留在: {base_dir}")
            print("你可以手动探索和分析这些文件。")
            
    except Exception as e:
        print(f"\n❌ 示例运行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()