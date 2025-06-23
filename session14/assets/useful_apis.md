# 有用的免费API列表

以下是一些适合学习和练习的免费API，大部分不需要注册即可使用。

## 测试和学习API

### HTTPBin
- **网址**: http://httpbin.org
- **用途**: 测试HTTP请求
- **特点**: 返回发送的请求信息，适合学习
- **示例**: 
  - GET请求: http://httpbin.org/get
  - POST请求: http://httpbin.org/post

### JSONPlaceholder
- **网址**: https://jsonplaceholder.typicode.com
- **用途**: 模拟REST API
- **特点**: 提供假数据，支持所有HTTP方法
- **示例**: 
  - 获取文章: https://jsonplaceholder.typicode.com/posts
  - 获取用户: https://jsonplaceholder.typicode.com/users

## 数据API

### 随机用户生成器
- **网址**: https://randomuser.me/api/
- **用途**: 生成随机用户信息
- **特点**: 包含姓名、地址、照片等
- **示例**: https://randomuser.me/api/?results=5

### 天气API

#### OpenWeatherMap
- **网址**: https://openweathermap.org/api
- **用途**: 天气数据
- **特点**: 需要免费注册获取API Key
- **限制**: 60次/分钟

#### wttr.in
- **网址**: https://wttr.in
- **用途**: 简单天气查询
- **特点**: 无需注册，支持命令行
- **示例**: https://wttr.in/Beijing?format=j1

## 娱乐API

### 笑话API
- **网址**: https://v2.jokeapi.dev
- **用途**: 获取编程笑话
- **特点**: 支持多种类别和语言
- **示例**: https://v2.jokeapi.dev/joke/Programming

### 名言API
- **网址**: https://api.quotable.io
- **用途**: 获取名人名言
- **特点**: 支持标签和作者筛选
- **示例**: https://api.quotable.io/random

## 开发相关API

### GitHub API
- **网址**: https://api.github.com
- **用途**: 获取GitHub数据
- **特点**: 公开数据无需认证
- **示例**: 
  - 用户信息: https://api.github.com/users/torvalds
  - 公开事件: https://api.github.com/events

### Hacker News API
- **网址**: https://hacker-news.firebaseio.com/v0
- **用途**: 获取Hacker News数据
- **特点**: 完全免费，无需注册
- **示例**: 
  - 热门故事: https://hacker-news.firebaseio.com/v0/topstories.json

## 金融数据API

### 汇率API
- **网址**: https://api.exchangerate-api.com/v4/latest/USD
- **用途**: 获取实时汇率
- **特点**: 免费，无需注册
- **示例**: 基于美元的汇率

### 加密货币API
- **网址**: https://api.coingecko.com/api/v3
- **用途**: 加密货币价格
- **特点**: 免费层足够学习使用
- **示例**: https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd

## 地理信息API

### IP地理位置
- **网址**: https://ipapi.co
- **用途**: 根据IP获取地理位置
- **特点**: 每月1000次免费
- **示例**: https://ipapi.co/json/

### 国家信息
- **网址**: https://restcountries.com/v3.1
- **用途**: 获取国家详细信息
- **特点**: 完全免费
- **示例**: https://restcountries.com/v3.1/name/china

## 使用提示

1. **阅读文档**: 使用前先阅读API文档
2. **注意限制**: 了解请求频率限制
3. **错误处理**: 始终处理可能的错误
4. **缓存数据**: 避免重复请求相同数据
5. **遵守条款**: 遵守API的使用条款

## 练习建议

1. 从HTTPBin开始，理解HTTP请求
2. 使用JSONPlaceholder练习CRUD操作
3. 尝试组合多个API创建有趣的应用
4. 学习处理不同的数据格式（JSON、XML等）
5. 实践错误处理和重试机制 