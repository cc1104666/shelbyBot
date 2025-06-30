# shelbyBot

自动批量提交邮箱到指定网站表单，支持 Cloudflare Turnstile 验证和代理池。

## 功能简介

- 支持批量邮箱自动提交
- 自动绕过 Cloudflare Turnstile 验证（集成 CapMonster）
- 支持 NSTProxy 代理池
- 支持自定义请求间隔

## 文件说明

- `autoshelby.py`：主程序，负责读取配置和邮箱，自动提交表单
- `cf_solver.py`：封装 CapMonster API，自动获取 Turnstile 验证 token
- `config.json`：配置文件，填写目标网站、API 密钥、代理等信息
- `emails.txt`：待提交的邮箱列表，每行一个邮箱
- `requirements.txt`：依赖包列表

## 安装依赖

建议使用 Python 3.8+，先安装依赖：

```bash
pip install -r requirements.txt
```

## 配置说明

请根据实际情况填写 `config.json`：

```json
{
  "capmonster_api_key": "你的capmonster密钥",
  "website_url": "https://shelby.xyz/",
  "turnstile_sitekey": "0x4AAAAAABievuLJEeerSHkD",
  "hubspot_api_url": "https://shelby.xyz/api/hubspot-contact",
  "default_emails": ["xxx@outlook.com"],
  "delay_between_requests": 15.0,
  "random_delay_range": [3.0, 8.0],
  "nstproxy_Channel": "通道id",
  "nstproxy_Password": "密码"
}
```

- `capmonster_api_key`：你的 CapMonster 平台 API 密钥
- `website_url`：目标网站地址
- `turnstile_sitekey`：Cloudflare Turnstile 的 sitekey
- `hubspot_api_url`：表单提交的 API 地址
- `delay_between_requests`：每次提交后的固定延迟（秒）
- `random_delay_range`：每次提交可选的随机延迟范围（秒）
- `nstproxy_Channel`/`nstproxy_Password`：NSTProxy 代理池的通道和密码
## 配置说明
nstproxy注册链接：https://app.nstproxy.com/register?i=EE0Ije
capmonster注册链接：https://capmonster.cloud/Dashboard
## 邮箱列表

将待提交的邮箱逐行写入 `emails.txt`，例如：

```
test1@example.com
test2@example.com
```

## 使用方法

1. 配置好 `config.json` 和 `emails.txt`
2. 运行主程序：

```bash
python autoshelby.py
```

程序会自动依次提交邮箱，自动处理验证码和代理。

## 依赖列表

- requests
- urllib3
- curl_cffi

