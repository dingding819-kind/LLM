#!/usr/bin/env python3
"""
Setup verification script for Google Cloud Service Account configuration
验证 Google Cloud Service Account 配置的脚本
"""

import os
import json
import sys
from pathlib import Path

def verify_setup():
    """Verify the API configuration setup"""
    print("=" * 60)
    print("API 配置验证 | API Configuration Verification")
    print("=" * 60)
    
    issues = []
    
    # 1. Check .env file
    print("\n[1/5] 检查 .env 文件...")
    env_path = Path(".env")
    if env_path.exists():
        print("✓ .env 文件存在")
        try:
            with open(".env", "r") as f:
                env_content = f.read()
                if "LLM_PROVIDER" in env_content:
                    # Extract provider
                    for line in env_content.split('\n'):
                        if line.startswith("LLM_PROVIDER="):
                            provider = line.split("=")[1].strip()
                            print(f"  - 使用的提供商: {provider}")
                else:
                    issues.append(".env 中没有设置 LLM_PROVIDER")
        except Exception as e:
            issues.append(f".env 读取错误: {e}")
    else:
        issues.append(".env 文件不存在")
    
    # 2. Check Service Account JSON
    print("\n[2/5] 检查 Service Account JSON 文件...")
    try:
        from config import SERVICE_ACCOUNT_JSON_PATH, SERVICE_ACCOUNT_INFO
        
        if SERVICE_ACCOUNT_JSON_PATH:
            print(f"  - 配置的路径: {SERVICE_ACCOUNT_JSON_PATH}")
            
            if os.path.exists(SERVICE_ACCOUNT_JSON_PATH):
                print("✓ Service Account JSON 文件存在")
                
                if SERVICE_ACCOUNT_INFO:
                    print("✓ Service Account JSON 成功加载")
                    
                    # Check required fields
                    required_fields = ["project_id", "private_key", "client_email"]
                    for field in required_fields:
                        if field in SERVICE_ACCOUNT_INFO:
                            if field == "private_key":
                                print(f"  - {field}: [已设置]")
                            else:
                                print(f"  - {field}: {SERVICE_ACCOUNT_INFO[field]}")
                        else:
                            issues.append(f"Service Account JSON 缺少字段: {field}")
                else:
                    issues.append("Service Account JSON 无法解析")
            else:
                issues.append(f"Service Account JSON 文件不存在: {SERVICE_ACCOUNT_JSON_PATH}")
        else:
            issues.append("SERVICE_ACCOUNT_JSON_PATH 未配置")
    except Exception as e:
        issues.append(f"导入配置错误: {e}")
    
    # 3. Check Google Cloud credentials
    print("\n[3/5] 检查 Google Cloud 配置...")
    try:
        from config import GOOGLE_PROJECT_ID, GOOGLE_LOCATION, GEMINI_MODEL_NAME
        
        if GOOGLE_PROJECT_ID:
            print(f"✓ Google Project ID: {GOOGLE_PROJECT_ID}")
        else:
            issues.append("GOOGLE_PROJECT_ID 未设置")
        
        print(f"  - Google Location: {GOOGLE_LOCATION}")
        print(f"  - Gemini Model: {GEMINI_MODEL_NAME}")
    except Exception as e:
        issues.append(f"获取 Google Cloud 配置错误: {e}")
    
    # 4. Check dependencies
    print("\n[4/5] 检查必需的依赖库...")
    dependencies = {
        "vertexai": "Google Vertex AI",
        "google.cloud.aiplatform": "Google Cloud AI Platform",
        "google.auth": "Google Authentication",
        "dotenv": "Python Dotenv"
    }
    
    for module, description in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {description} 已安装")
        except ImportError:
            issues.append(f"{description} 未安装: pip install {module.split('.')[0]}")
    
    # 5. Test LLM Client initialization
    print("\n[5/5] 测试 LLM Client 初始化...")
    try:
        from models.llm_client import LLMClient
        client = LLMClient()
        print("✓ LLM Client 初始化成功")
        print(f"  - 使用的提供商: {client.provider}")
        print(f"  - 使用的模型: {client.model}")
    except Exception as e:
        issues.append(f"LLM Client 初始化失败: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    if not issues:
        print("✓ 所有检查通过！配置正确。")
        print("=" * 60)
        print("\n下一步: 可以开始使用程序了！")
        return 0
    else:
        print("✗ 发现以下问题:")
        print("=" * 60)
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        print("\n请修复上述问题后重试。")
        return 1

def test_api_connection():
    """Test actual API connection"""
    print("\n" + "=" * 60)
    print("API 连接测试 | API Connection Test")
    print("=" * 60)
    
    try:
        from models.llm_client import LLMClient
        
        print("\n尝试初始化 LLM Client...")
        client = LLMClient()
        
        if client.provider == "vertexai":
            print("✓ Vertex AI Client 初始化成功")
            print("\n尝试生成测试响应...")
            
            test_prompt = "你好，请简洁地介绍自己。"
            response = client.generate_text(test_prompt)
            
            if response:
                print("✓ API 调用成功！")
                print(f"\n响应预览: {response[:100]}...")
                return 0
            else:
                print("✗ API 调用返回空响应")
                return 1
        else:
            print(f"配置的提供商: {client.provider}")
            print("注意: 跳过 API 连接测试（当前提供商非 Vertex AI）")
            return 0
            
    except Exception as e:
        print(f"✗ API 连接测试失败: {e}")
        print("\n请确保:")
        print("1. Service Account JSON 文件有效")
        print("2. Google Cloud 项目已启用 Vertex AI API")
        print("3. 网络连接正常")
        return 1

if __name__ == "__main__":
    # Run verification
    result = verify_setup()
    
    if result == 0:
        # Ask if user wants to test API connection
        print("\n是否要测试 API 连接? (y/n): ", end="")
        try:
            if input().lower() == 'y':
                test_api_connection()
        except KeyboardInterrupt:
            print("\n已取消")
    
    sys.exit(result)
