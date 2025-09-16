#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中文字符统计工具
用于统计txt文件中的中文字符数量
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import os
from tkinter.scrolledtext import ScrolledText

class ChineseCharCounter:
    def __init__(self, root):
        self.root = root
        self.root.title("中文字符统计工具")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="中文字符统计工具", 
                               font=('Microsoft YaHei', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="10")
        file_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        file_frame.columnconfigure(1, weight=1)
        
        ttk.Button(file_frame, text="选择文件", command=self.select_file).grid(row=0, column=0, padx=(0, 10))
        
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ttk.Entry(file_frame, textvariable=self.file_path_var, state='readonly')
        self.file_path_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(file_frame, text="开始统计", command=self.count_characters).grid(row=0, column=2)
        
        # 统计结果区域
        result_frame = ttk.LabelFrame(main_frame, text="统计结果", padding="10")
        result_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        result_frame.columnconfigure(1, weight=1)
        
        # 结果显示
        ttk.Label(result_frame, text="总字符数:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.total_chars_var = tk.StringVar(value="0")
        ttk.Label(result_frame, textvariable=self.total_chars_var, font=('Consolas', 12, 'bold')).grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(result_frame, text="中文字符数:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.chinese_chars_var = tk.StringVar(value="0")
        ttk.Label(result_frame, textvariable=self.chinese_chars_var, font=('Consolas', 12, 'bold'), foreground='blue').grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(result_frame, text="中文字符占比:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.percentage_var = tk.StringVar(value="0%")
        ttk.Label(result_frame, textvariable=self.percentage_var, font=('Consolas', 12, 'bold'), foreground='green').grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        ttk.Label(result_frame, text="文件大小:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.file_size_var = tk.StringVar(value="0 字节")
        ttk.Label(result_frame, textvariable=self.file_size_var, font=('Consolas', 12)).grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # 详细信息区域
        detail_frame = ttk.LabelFrame(main_frame, text="详细信息", padding="10")
        detail_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        detail_frame.columnconfigure(0, weight=1)
        
        self.detail_text = ScrolledText(detail_frame, height=6, width=70, font=('Consolas', 10))
        self.detail_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 文件内容预览区域
        preview_frame = ttk.LabelFrame(main_frame, text="文件内容预览 (前500字符)", padding="10")
        preview_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        
        self.preview_text = ScrolledText(preview_frame, height=8, width=70, font=('Microsoft YaHei', 10))
        self.preview_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 状态栏
        self.status_var = tk.StringVar(value="请选择要统计的txt文件")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_label.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
    def select_file(self):
        """选择文件"""
        file_path = filedialog.askopenfilename(
            title="选择txt文件",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            self.status_var.set(f"已选择文件: {os.path.basename(file_path)}")
            
    def count_characters(self):
        """统计字符"""
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showwarning("警告", "请先选择一个文件！")
            return
            
        if not os.path.exists(file_path):
            messagebox.showerror("错误", "文件不存在！")
            return
            
        try:
            # 尝试不同的编码方式读取文件
            content = None
            encoding_used = None
            
            for encoding in ['utf-8', 'gbk', 'gb2312', 'utf-16']:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    encoding_used = encoding
                    break
                except UnicodeDecodeError:
                    continue
                    
            if content is None:
                messagebox.showerror("错误", "无法读取文件，可能是编码问题！")
                return
                
            # 统计字符
            total_chars = len(content)
            
            # 使用正则表达式匹配中文字符（包括中文标点符号）
            chinese_pattern = r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff\u3000-\u303f\uff00-\uffef]'
            chinese_chars = re.findall(chinese_pattern, content)
            chinese_count = len(chinese_chars)
            
            # 计算占比
            percentage = (chinese_count / total_chars * 100) if total_chars > 0 else 0
            
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            file_size_str = self.format_file_size(file_size)
            
            # 更新显示
            self.total_chars_var.set(f"{total_chars:,}")
            self.chinese_chars_var.set(f"{chinese_count:,}")
            self.percentage_var.set(f"{percentage:.2f}%")
            self.file_size_var.set(file_size_str)
            
            # 显示详细信息
            detail_info = f"""统计完成！

文件路径: {file_path}
文件编码: {encoding_used}
文件大小: {file_size_str}

字符统计:
- 总字符数: {total_chars:,}
- 中文字符数: {chinese_count:,}
- 中文字符占比: {percentage:.2f}%
- 非中文字符数: {total_chars - chinese_count:,}

提示: 此统计结果可用于评估文本交给大模型处理时的token消耗量。
一般来说，中文字符的token消耗比英文字符更高。
"""
            
            self.detail_text.delete(1.0, tk.END)
            self.detail_text.insert(1.0, detail_info)
            
            # 显示文件内容预览
            preview_content = content[:500]
            if len(content) > 500:
                preview_content += "\n\n... (内容已截断，仅显示前500字符)"
                
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_content)
            
            self.status_var.set(f"统计完成 - 中文字符: {chinese_count:,} / 总字符: {total_chars:,}")
            
        except Exception as e:
            messagebox.showerror("错误", f"处理文件时出错: {str(e)}")
            self.status_var.set("处理文件时出错")
            
    def format_file_size(self, size_bytes):
        """格式化文件大小"""
        if size_bytes < 1024:
            return f"{size_bytes} 字节"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.2f} MB"
        else:
            return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"

def main():
    root = tk.Tk()
    app = ChineseCharCounter(root)
    root.mainloop()

if __name__ == "__main__":
    main()