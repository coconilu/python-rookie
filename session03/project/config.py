#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BMI计算器配置文件

这个文件包含了BMI计算器项目中使用的所有常量、配置参数和标准值。
将这些值集中管理，便于维护和修改。

配置内容：
1. BMI分类标准
2. 单位转换常量
3. 数据验证范围
4. 用户界面文本
5. 文件路径配置

作者：Python学习者
日期：2024年
"""

# =============================================================================
# BMI分类标准
# =============================================================================

# WHO（世界卫生组织）BMI分类标准
WHO_BMI_CATEGORIES = {
    'underweight': (0, 18.5),      # 偏瘦
    'normal': (18.5, 25.0),        # 正常
    'overweight': (25.0, 30.0),    # 偏胖
    'obese': (30.0, float('inf'))  # 肥胖
}

# 亚洲人群BMI分类标准
ASIAN_BMI_CATEGORIES = {
    'underweight': (0, 18.5),      # 偏瘦
    'normal': (18.5, 23.0),        # 正常
    'overweight': (23.0, 27.5),    # 偏胖
    'obese': (27.5, float('inf'))  # 肥胖
}

# BMI分类中文名称
BMI_CATEGORY_NAMES = {
    'underweight': '偏瘦',
    'normal': '正常',
    'overweight': '偏胖',
    'obese': '肥胖'
}

# BMI分类英文名称
BMI_CATEGORY_NAMES_EN = {
    'underweight': 'Underweight',
    'normal': 'Normal',
    'overweight': 'Overweight',
    'obese': 'Obese'
}

# =============================================================================
# 单位转换常量
# =============================================================================

# 重量转换
POUND_TO_KG = 0.453592          # 1磅 = 0.453592公斤
KG_TO_POUND = 2.20462           # 1公斤 = 2.20462磅

# 长度转换
INCH_TO_METER = 0.0254          # 1英寸 = 0.0254米
METER_TO_INCH = 39.3701         # 1米 = 39.3701英寸
FOOT_TO_METER = 0.3048          # 1英尺 = 0.3048米
METER_TO_FOOT = 3.28084         # 1米 = 3.28084英尺

# =============================================================================
# 数据验证范围
# =============================================================================

# 公制单位验证范围
METRIC_WEIGHT_RANGE = (1, 1000)     # 体重范围：1-1000公斤
METRIC_HEIGHT_RANGE = (0.5, 3.0)    # 身高范围：0.5-3.0米

# 英制单位验证范围
IMPERIAL_WEIGHT_RANGE = (2, 2200)   # 体重范围：2-2200磅
IMPERIAL_HEIGHT_RANGE = (20, 120)   # 身高范围：20-120英寸

# 年龄验证范围
AGE_RANGE = (1, 150)                # 年龄范围：1-150岁

# BMI合理范围
BMI_RANGE = (10, 100)               # BMI范围：10-100

# =============================================================================
# 用户界面文本
# =============================================================================

# 应用程序信息
APP_NAME = "BMI健康计算器"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Python学习者"
APP_DESCRIPTION = "基于Python的BMI计算和健康评估工具"

# 菜单选项
MENU_OPTIONS = {
    'unit_metric': "1-公制(kg/m)",
    'unit_imperial': "2-英制(lb/in)",
    'gender_male': "1-男性",
    'gender_female': "2-女性",
    'activity_low': "1-低活动量",
    'activity_moderate': "2-中等活动量",
    'activity_high': "3-高活动量",
    'standard_who': "1-WHO标准",
    'standard_asian': "2-亚洲标准"
}

# 输入提示文本
INPUT_PROMPTS = {
    'username': "请输入您的用户名（用于保存记录）: ",
    'unit_system': "请选择单位系统 (1-公制kg/m, 2-英制lb/in): ",
    'weight_metric': "请输入您的体重（公斤）: ",
    'height_metric': "请输入您的身高（米）: ",
    'weight_imperial': "请输入您的体重（磅）: ",
    'height_imperial': "请输入您的身高（英寸）: ",
    'age': "请输入您的年龄: ",
    'gender': "请选择性别 (1-男性, 2-女性): ",
    'activity_level': "请选择活动水平 (1-低, 2-中等, 3-高): ",
    'bmi_standard': "请选择BMI标准 (1-WHO标准, 2-亚洲标准): ",
    'continue': "是否继续计算？(y/n): "
}

# 错误消息
ERROR_MESSAGES = {
    'invalid_number': "请输入有效的数字",
    'invalid_age': "请输入有效的年龄（1-150）",
    'invalid_choice': "请输入有效的选项",
    'invalid_weight_height': "输入的体重或身高数值无效",
    'save_failed': "记录保存失败",
    'load_failed': "数据加载失败",
    'calculation_error': "计算过程中出现错误"
}

# 成功消息
SUCCESS_MESSAGES = {
    'record_saved': "✅ 记录已保存",
    'calculation_complete': "✅ 计算完成",
    'data_loaded': "✅ 数据加载成功"
}

# 警告消息
WARNING_MESSAGES = {
    'health_risk': "⚠️  健康风险提醒",
    'consult_doctor': "⚠️  建议咨询医生",
    'data_insufficient': "⚠️  数据不足"
}

# =============================================================================
# 健康建议模板
# =============================================================================

# 通用健康建议
GENERAL_ADVICE = {
    'underweight': "您的体重偏轻，建议适当增重以达到健康体重范围。",
    'normal': "恭喜！您的体重在健康范围内，请继续保持良好的生活习惯。",
    'overweight': "您的体重略高于正常范围，建议适当减重以降低健康风险。",
    'obese': "您的体重超出健康范围较多，强烈建议咨询医生制定减重计划。"
}

# 饮食建议
DIET_TIPS = {
    'underweight': [
        "增加健康的高热量食物摄入",
        "多吃坚果、牛油果、全谷物",
        "少食多餐，增加营养密度",
        "适当补充蛋白质"
    ],
    'normal': [
        "保持均衡饮食",
        "多吃蔬菜水果",
        "控制加工食品摄入",
        "保持规律的饮食时间"
    ],
    'overweight': [
        "控制总热量摄入",
        "减少高糖高脂食物",
        "增加蔬菜和蛋白质比例",
        "注意饮食份量控制"
    ],
    'obese': [
        "严格控制热量摄入",
        "避免高热量密度食物",
        "增加膳食纤维摄入",
        "考虑寻求营养师指导"
    ]
}

# 运动建议
EXERCISE_TIPS = {
    'underweight': [
        "进行力量训练增加肌肉量",
        "避免过度有氧运动",
        "注重核心肌群训练"
    ],
    'normal': [
        "每周至少150分钟中等强度运动",
        "结合有氧运动和力量训练",
        "保持运动的多样性"
    ],
    'overweight': [
        "增加有氧运动时间",
        "每周至少300分钟中等强度运动",
        "加入力量训练维持肌肉量"
    ],
    'obese': [
        "从低强度运动开始",
        "逐步增加运动时间和强度",
        "选择对关节友好的运动",
        "建议在专业指导下运动"
    ]
}

# 健康风险
HEALTH_RISKS = {
    'underweight': [
        "免疫力下降风险",
        "骨质疏松风险",
        "营养不良风险"
    ],
    'normal': [],
    'overweight': [
        "心血管疾病风险增加",
        "2型糖尿病风险上升"
    ],
    'obese': [
        "心血管疾病高风险",
        "2型糖尿病高风险",
        "高血压风险",
        "睡眠呼吸暂停风险",
        "某些癌症风险增加"
    ]
}

# =============================================================================
# 年龄和性别特定建议
# =============================================================================

# 年龄特定建议
AGE_SPECIFIC_ADVICE = {
    'elderly': {  # 65岁以上
        'exercise': "注重平衡性训练预防跌倒",
        'diet': "确保充足的钙和维生素D摄入"
    },
    'youth': {    # 18岁以下
        'general': "建议在家长和医生指导下进行任何体重管理。"
    }
}

# 性别特定建议
GENDER_SPECIFIC_ADVICE = {
    'female': {
        'diet': "注意铁质和叶酸的摄入"
    },
    'male': {
        'exercise': "可以适当增加力量训练强度"
    }
}

# =============================================================================
# 文件和路径配置
# =============================================================================

# 数据文件配置
DATA_CONFIG = {
    'data_directory': 'data',
    'user_data_file': 'data/user_data.json',
    'backup_directory': 'data/backup',
    'log_file': 'data/app.log'
}

# 导出文件配置
EXPORT_CONFIG = {
    'csv_encoding': 'utf-8-sig',
    'json_encoding': 'utf-8',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'decimal_places': 2
}

# =============================================================================
# 应用程序设置
# =============================================================================

# 默认设置
DEFAULT_SETTINGS = {
    'use_asian_standard': False,
    'default_unit': 'metric',
    'save_history': True,
    'show_detailed_advice': True,
    'decimal_places': 2
}

# 性能设置
PERFORMANCE_CONFIG = {
    'max_records_per_user': 1000,
    'max_users': 10000,
    'backup_frequency_days': 7,
    'cleanup_old_records_days': 365
}

# =============================================================================
# 数学常量
# =============================================================================

# BMI计算相关常量
BMI_CONSTANTS = {
    'height_power': 2,              # 身高的幂次（BMI公式中的平方）
    'rounding_precision': 2,        # BMI值保留小数位数
    'trend_threshold': 0.5          # 趋势判断阈值
}

# 统计分析常量
STATISTICS_CONFIG = {
    'min_records_for_trend': 2,     # 趋势分析最少记录数
    'percentile_ranges': [25, 50, 75, 90, 95],  # 百分位数范围
    'moving_average_window': 5      # 移动平均窗口大小
}

# =============================================================================
# 颜色和样式配置（用于未来的GUI版本）
# =============================================================================

# BMI分类颜色
BMI_COLORS = {
    'underweight': '#3498db',       # 蓝色
    'normal': '#2ecc71',           # 绿色
    'overweight': '#f39c12',       # 橙色
    'obese': '#e74c3c'             # 红色
}

# 界面主题色
THEME_COLORS = {
    'primary': '#3498db',
    'secondary': '#2c3e50',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}

# =============================================================================
# 调试和开发配置
# =============================================================================

# 调试设置
DEBUG_CONFIG = {
    'enable_debug': False,
    'log_level': 'INFO',
    'show_performance_metrics': False,
    'enable_test_mode': False
}

# 测试数据
TEST_DATA = {
    'sample_users': [
        {'weight': 70, 'height': 1.75, 'age': 30, 'gender': 'male'},
        {'weight': 60, 'height': 1.65, 'age': 25, 'gender': 'female'},
        {'weight': 80, 'height': 1.80, 'age': 35, 'gender': 'male'},
        {'weight': 55, 'height': 1.60, 'age': 28, 'gender': 'female'}
    ],
    'boundary_cases': [
        {'weight': 1, 'height': 0.5, 'unit': 'metric'},
        {'weight': 1000, 'height': 3.0, 'unit': 'metric'},
        {'weight': 2, 'height': 20, 'unit': 'imperial'},
        {'weight': 2200, 'height': 120, 'unit': 'imperial'}
    ]
}

# =============================================================================
# 版本信息
# =============================================================================

VERSION_INFO = {
    'major': 1,
    'minor': 0,
    'patch': 0,
    'build': '20241201',
    'release_date': '2024-12-01',
    'python_version_required': '3.7+'
}

# 更新日志
CHANGELOG = {
    '1.0.0': [
        "初始版本发布",
        "实现基本BMI计算功能",
        "支持WHO和亚洲标准",
        "提供个性化健康建议",
        "实现历史记录管理",
        "支持公制和英制单位"
    ]
}

# =============================================================================
# 帮助文档
# =============================================================================

HELP_TEXT = {
    'bmi_explanation': """
BMI（身体质量指数）是评估体重与身高关系的常用指标。
计算公式：BMI = 体重(kg) / 身高²(m²)

BMI分类标准：
- 偏瘦：BMI < 18.5
- 正常：18.5 ≤ BMI < 25.0（WHO标准）或 18.5 ≤ BMI < 23.0（亚洲标准）
- 偏胖：25.0 ≤ BMI < 30.0（WHO标准）或 23.0 ≤ BMI < 27.5（亚洲标准）
- 肥胖：BMI ≥ 30.0（WHO标准）或 BMI ≥ 27.5（亚洲标准）
""",
    
    'usage_instructions': """
使用说明：
1. 选择合适的单位系统（公制或英制）
2. 输入准确的体重和身高数据
3. 提供年龄、性别等个人信息
4. 选择适合的BMI评估标准
5. 查看计算结果和健康建议
6. 可选择保存记录以跟踪变化趋势
""",
    
    'health_disclaimer': """
健康声明：
本工具仅供参考，不能替代专业医疗建议。
BMI指标有一定局限性，不适用于：
- 孕妇
- 18岁以下儿童青少年
- 肌肉发达的运动员
- 65岁以上老年人

如有健康问题，请咨询专业医生。
"""
}