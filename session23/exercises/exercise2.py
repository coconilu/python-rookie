#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session23 练习2：代码格式化和工具配置练习

任务：
1. 配置代码质量检查工具
2. 使用工具自动格式化代码
3. 修复工具检测出的问题

工具使用步骤：
1. 安装工具：pip install ruff black mypy bandit
2. 运行检查：ruff check exercise2.py
3. 自动修复：ruff check exercise2.py --fix
4. 格式化代码：black exercise2.py
5. 类型检查：mypy exercise2.py
6. 安全检查：bandit exercise2.py

请创建配置文件并修复所有检测到的问题。
"""

# 这个文件包含各种格式和质量问题，需要使用工具修复

import json,os,sys,re
from typing import Dict,List,Optional,Any
import hashlib,secrets
from pathlib import Path

class DataProcessor:
    def __init__(self,config_file:str,debug:bool=False):
        self.config_file=config_file
        self.debug=debug
        self.data=[]
        self.processed_count=0
        
    def load_config(self):
        try:
            with open(self.config_file,'r')as f:config=json.load(f)
            return config
        except FileNotFoundError:return{"default":True}
        except json.JSONDecodeError:return{"error":True}
    
    def validate_data(self,item):
        if not isinstance(item,dict):return False
        required_fields=['id','name','value']
        for field in required_fields:
            if field not in item:return False
        return True
    
    def process_item(self,item,config):
        if not self.validate_data(item):return None
        
        result={'id':item['id'],'name':item['name'],'value':item['value'],'processed':True}
        
        if config.get('transform',False):
            if isinstance(item['value'],str):result['value']=item['value'].upper()
            elif isinstance(item['value'],(int,float)):result['value']=item['value']*2
        
        if config.get('add_hash',False):
            hash_input=f"{item['id']}{item['name']}{item['value']}"
            result['hash']=hashlib.md5(hash_input.encode()).hexdigest()
        
        return result
    
    def process_batch(self,data_batch,config):
        results=[]
        for item in data_batch:
            processed=self.process_item(item,config)
            if processed:results.append(processed)
            self.processed_count+=1
        return results
    
    def save_results(self,results,output_file):
        with open(output_file,'w')as f:json.dump(results,f)
    
    def generate_report(self,results):
        total=len(results)
        valid=sum(1 for r in results if r.get('processed',False))
        report={'total_items':total,'valid_items':valid,'invalid_items':total-valid,'processing_rate':valid/total if total>0 else 0}
        return report

def create_sample_data():
    return[
        {'id':1,'name':'item1','value':'test'},
        {'id':2,'name':'item2','value':42},
        {'id':3,'name':'item3','value':3.14},
        {'id':4,'name':'','value':'invalid'},
        {'name':'item5','value':'missing_id'},
    ]

def create_config_file(filename):
    config={'transform':True,'add_hash':True,'debug':False}
    with open(filename,'w')as f:json.dump(config,f,indent=2)

def main():
    config_file='config.json'
    output_file='results.json'
    
    create_config_file(config_file)
    
    processor=DataProcessor(config_file,debug=True)
    config=processor.load_config()
    
    sample_data=create_sample_data()
    
    results=processor.process_batch(sample_data,config)
    
    processor.save_results(results,output_file)
    
    report=processor.generate_report(results)
    
    print(f"处理完成，共处理{processor.processed_count}个项目")
    print(f"报告：{report}")
    
    # 清理临时文件
    if os.path.exists(config_file):os.remove(config_file)
    if os.path.exists(output_file):os.remove(output_file)

if __name__=='__main__':main()

# 练习要求：
# 1. 创建 pyproject.toml 配置文件，配置 ruff 和 black
# 2. 创建 mypy.ini 配置文件，配置类型检查
# 3. 使用工具修复所有格式问题
# 4. 添加缺失的类型注解
# 5. 修复安全问题（如使用MD5哈希）
# 6. 改善代码结构和可读性
# 7. 添加适当的异常处理
# 8. 确保代码通过所有质量检查