#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Session20 API开发项目配置文件
存储项目常量、配置信息和默认值

作者: Python学习教程
日期: 2024
"""

from datetime import timedelta
import os

# =============================================================================
# 应用基础配置
# =============================================================================

class Config:
    """基础配置类"""
    
    # 应用基础信息
    APP_NAME = "Session20 图书管理API"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "基于Flask-RESTful的图书管理系统API"
    
    # 安全配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string-change-in-production'
    
    # JWT配置
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORITHM = 'HS256'
    
    # 数据库配置
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///books.db'
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Redis配置（用于限流）
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # CORS配置
    CORS_ORIGINS = ['http://localhost:3000', 'http://127.0.0.1:3000']
    
    # 分页配置
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    
    # 限流配置
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "100 per hour"
    
    # API文档配置
    SWAGGER_CONFIG = {
        'title': APP_NAME,
        'version': APP_VERSION,
        'description': APP_DESCRIPTION,
        'termsOfService': '',
        'contact': {
            'name': 'API Support',
            'email': 'support@example.com'
        },
        'license': {
            'name': 'MIT',
            'url': 'https://opensource.org/licenses/MIT'
        }
    }

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    SQLALCHEMY_ECHO = True
    RATELIMIT_ENABLED = False

class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    RATELIMIT_ENABLED = True
    
    # 生产环境安全配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    RATELIMIT_ENABLED = False
    WTF_CSRF_ENABLED = False

# =============================================================================
# API响应状态码
# =============================================================================

class StatusCode:
    """HTTP状态码常量"""
    
    # 成功状态码
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    
    # 客户端错误状态码
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONFLICT = 409
    UNPROCESSABLE_ENTITY = 422
    TOO_MANY_REQUESTS = 429
    
    # 服务器错误状态码
    INTERNAL_SERVER_ERROR = 500
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503

# =============================================================================
# API响应消息
# =============================================================================

class Messages:
    """API响应消息常量"""
    
    # 成功消息
    SUCCESS = "操作成功"
    CREATED_SUCCESS = "创建成功"
    UPDATED_SUCCESS = "更新成功"
    DELETED_SUCCESS = "删除成功"
    
    # 认证相关消息
    LOGIN_SUCCESS = "登录成功"
    LOGOUT_SUCCESS = "登出成功"
    REGISTER_SUCCESS = "注册成功"
    TOKEN_REFRESH_SUCCESS = "Token刷新成功"
    
    # 错误消息
    INVALID_REQUEST = "请求参数无效"
    UNAUTHORIZED_ACCESS = "未授权访问"
    FORBIDDEN_ACCESS = "权限不足"
    RESOURCE_NOT_FOUND = "资源不存在"
    INTERNAL_ERROR = "服务器内部错误"
    
    # 验证错误消息
    MISSING_REQUIRED_FIELD = "缺少必需字段"
    INVALID_EMAIL_FORMAT = "邮箱格式无效"
    INVALID_PASSWORD_FORMAT = "密码格式无效"
    USERNAME_EXISTS = "用户名已存在"
    EMAIL_EXISTS = "邮箱已被注册"
    
    # 图书相关消息
    BOOK_NOT_FOUND = "图书不存在"
    BOOK_CREATED = "图书创建成功"
    BOOK_UPDATED = "图书更新成功"
    BOOK_DELETED = "图书删除成功"
    
    # 用户相关消息
    USER_NOT_FOUND = "用户不存在"
    USER_CREATED = "用户创建成功"
    USER_UPDATED = "用户更新成功"
    USER_DELETED = "用户删除成功"
    ACCOUNT_DISABLED = "账户已被禁用"
    
    # Token相关消息
    TOKEN_EXPIRED = "Token已过期"
    TOKEN_INVALID = "Token无效"
    TOKEN_REVOKED = "Token已被撤销"
    TOKEN_MISSING = "缺少访问令牌"

# =============================================================================
# 图书分类常量
# =============================================================================

class BookCategories:
    """图书分类常量"""
    
    FICTION = "小说"
    NON_FICTION = "非小说"
    SCIENCE = "科学"
    TECHNOLOGY = "技术"
    HISTORY = "历史"
    BIOGRAPHY = "传记"
    SELF_HELP = "自助"
    BUSINESS = "商业"
    EDUCATION = "教育"
    CHILDREN = "儿童"
    ROMANCE = "言情"
    MYSTERY = "悬疑"
    FANTASY = "奇幻"
    HORROR = "恐怖"
    POETRY = "诗歌"
    DRAMA = "戏剧"
    PHILOSOPHY = "哲学"
    RELIGION = "宗教"
    ART = "艺术"
    MUSIC = "音乐"
    SPORTS = "体育"
    TRAVEL = "旅行"
    COOKING = "烹饪"
    HEALTH = "健康"
    OTHER = "其他"
    
    # 所有分类列表
    ALL_CATEGORIES = [
        FICTION, NON_FICTION, SCIENCE, TECHNOLOGY, HISTORY, BIOGRAPHY,
        SELF_HELP, BUSINESS, EDUCATION, CHILDREN, ROMANCE, MYSTERY,
        FANTASY, HORROR, POETRY, DRAMA, PHILOSOPHY, RELIGION,
        ART, MUSIC, SPORTS, TRAVEL, COOKING, HEALTH, OTHER
    ]

# =============================================================================
# 用户角色常量
# =============================================================================

class UserRoles:
    """用户角色常量"""
    
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"
    
    # 所有角色列表
    ALL_ROLES = [ADMIN, USER, MODERATOR]
    
    # 角色权限映射
    PERMISSIONS = {
        ADMIN: ['read', 'write', 'delete', 'manage_users'],
        MODERATOR: ['read', 'write', 'delete'],
        USER: ['read']
    }

# =============================================================================
# 验证规则常量
# =============================================================================

class ValidationRules:
    """验证规则常量"""
    
    # 用户名验证
    USERNAME_MIN_LENGTH = 3
    USERNAME_MAX_LENGTH = 20
    USERNAME_PATTERN = r'^[a-zA-Z0-9_]+$'
    
    # 密码验证
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_MAX_LENGTH = 128
    PASSWORD_REQUIRE_DIGIT = True
    PASSWORD_REQUIRE_LETTER = True
    PASSWORD_REQUIRE_SPECIAL = False
    
    # 邮箱验证
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # 图书验证
    BOOK_TITLE_MIN_LENGTH = 1
    BOOK_TITLE_MAX_LENGTH = 200
    BOOK_AUTHOR_MIN_LENGTH = 1
    BOOK_AUTHOR_MAX_LENGTH = 100
    BOOK_ISBN_PATTERN = r'^(?:ISBN(?:-1[03])?:? )?(?=[0-9X]{10}$|(?=(?:[0-9]+[- ]){3})[- 0-9X]{13}$|97[89][0-9]{10}$|(?=(?:[0-9]+[- ]){4})[- 0-9]{17}$)(?:97[89][- ]?)?[0-9]{1,5}[- ]?[0-9]+[- ]?[0-9]+[- ]?[0-9X]$'
    BOOK_PRICE_MIN = 0
    BOOK_PRICE_MAX = 99999.99
    BOOK_STOCK_MIN = 0
    BOOK_STOCK_MAX = 999999

# =============================================================================
# 限流配置常量
# =============================================================================

class RateLimits:
    """限流配置常量"""
    
    # 全局限流
    GLOBAL_LIMIT = "1000 per hour"
    
    # 认证相关限流
    LOGIN_LIMIT = "5 per minute"
    REGISTER_LIMIT = "3 per minute"
    REFRESH_TOKEN_LIMIT = "10 per minute"
    
    # API操作限流
    READ_LIMIT = "100 per minute"
    WRITE_LIMIT = "30 per minute"
    DELETE_LIMIT = "10 per minute"
    
    # 搜索限流
    SEARCH_LIMIT = "50 per minute"
    
    # 管理员操作限流
    ADMIN_LIMIT = "200 per minute"

# =============================================================================
# 缓存配置常量
# =============================================================================

class CacheConfig:
    """缓存配置常量"""
    
    # 缓存过期时间（秒）
    DEFAULT_TIMEOUT = 300  # 5分钟
    SHORT_TIMEOUT = 60     # 1分钟
    LONG_TIMEOUT = 3600    # 1小时
    
    # 缓存键前缀
    BOOK_PREFIX = "book:"
    USER_PREFIX = "user:"
    SEARCH_PREFIX = "search:"
    STATS_PREFIX = "stats:"
    
    # 缓存键模板
    BOOK_DETAIL_KEY = BOOK_PREFIX + "detail:{book_id}"
    BOOK_LIST_KEY = BOOK_PREFIX + "list:{page}:{per_page}:{category}:{search}"
    USER_PROFILE_KEY = USER_PREFIX + "profile:{user_id}"
    SEARCH_RESULT_KEY = SEARCH_PREFIX + "result:{query}:{page}"
    STATS_KEY = STATS_PREFIX + "general"

# =============================================================================
# 日志配置常量
# =============================================================================

class LogConfig:
    """日志配置常量"""
    
    # 日志级别
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"
    
    # 日志格式
    DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    DETAILED_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
    
    # 日志文件配置
    LOG_FILE = "app.log"
    MAX_BYTES = 10 * 1024 * 1024  # 10MB
    BACKUP_COUNT = 5

# =============================================================================
# 环境配置映射
# =============================================================================

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# =============================================================================
# 获取配置函数
# =============================================================================

def get_config(config_name=None):
    """获取配置类
    
    Args:
        config_name (str): 配置名称，如果为None则从环境变量获取
        
    Returns:
        Config: 配置类
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, DevelopmentConfig)

def get_database_url(config_name=None):
    """获取数据库URL
    
    Args:
        config_name (str): 配置名称
        
    Returns:
        str: 数据库URL
    """
    config_class = get_config(config_name)
    return config_class.SQLALCHEMY_DATABASE_URI

def is_debug_mode(config_name=None):
    """检查是否为调试模式
    
    Args:
        config_name (str): 配置名称
        
    Returns:
        bool: 是否为调试模式
    """
    config_class = get_config(config_name)
    return getattr(config_class, 'DEBUG', False)

def get_secret_key(config_name=None):
    """获取密钥
    
    Args:
        config_name (str): 配置名称
        
    Returns:
        str: 密钥
    """
    config_class = get_config(config_name)
    return config_class.SECRET_KEY