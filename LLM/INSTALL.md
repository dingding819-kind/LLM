# 安装和运行指南

## 前置要求

- **Python**: 3.8 或更高版本
- **pip**: Python 包管理器
- **OpenAI API 密钥**: 用于访问 GPT 模型（可选，演示模式无需）

## 快速开始（3步）

### 1. 安装依赖

```bash
# 进入项目目录
cd c:\Users\user\Desktop\LLM

# 安装依赖包
pip install -r requirements.txt
```

### 2. 配置 API（可选）

如果要使用完整功能，需要配置 OpenAI API：

**方法A: 使用 .env 文件**
```bash
# 复制示例文件
copy .env.example .env

# 编辑 .env，填入你的 API 密钥
OPENAI_API_KEY=sk-your-actual-key-here
```

**方法B: 直接编辑 config.py**
```python
# 在 config.py 中
OPENAI_API_KEY = "sk-your-actual-key-here"
```

### 3. 运行程序

**演示模式**（无需 API 密钥）：
```bash
python demo.py
```

**交互式学习**（需要 API 密钥）：
```bash
python main.py
```

**查看示例**（需要 API 密钥）：
```bash
python example_usage.py
```

## 详细安装步骤

### Windows 系统

1. **打开 PowerShell**
   ```powershell
   # 进入项目目录
   cd "c:\Users\user\Desktop\LLM"
   ```

2. **创建虚拟环境（推荐）**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **安装依赖**
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **验证安装**
   ```powershell
   python -c "import openai; print('OpenAI 库已安装')"
   ```

5. **获取 API 密钥**
   - 访问 https://platform.openai.com/api-keys
   - 创建新的 API 密钥
   - 复制密钥

6. **配置 API 密钥**
   ```powershell
   # 创建 .env 文件
   notepad .env
   
   # 添加内容
   OPENAI_API_KEY=sk-your-key-here
   ```

7. **运行演示**
   ```powershell
   python demo.py
   ```

### macOS/Linux 系统

1. **打开终端**
   ```bash
   cd ~/Desktop/LLM  # 或你的项目路径
   ```

2. **创建虚拟环境**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **安装依赖**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **配置 API 密钥**
   ```bash
   cp .env.example .env
   nano .env  # 或用你喜欢的编辑器
   
   # 编辑 OPENAI_API_KEY 值
   ```

5. **运行演示**
   ```bash
   python demo.py
   ```

## 获取 OpenAI API 密钥

### 步骤

1. **创建 OpenAI 账户**
   - 访问 https://platform.openai.com/signup
   - 使用邮箱注册或登录

2. **创建 API 密钥**
   - 访问 https://platform.openai.com/api-keys
   - 点击 "Create new secret key"
   - 复制生成的密钥（只显示一次！）

3. **保管密钥**
   - 不要将密钥提交到 Git 仓库
   - 使用 .env 文件存储（已在 .gitignore 中）
   - 定期更新密钥以提高安全性

## 运行程序

### 模式1: 演示模式（推荐新手）

```bash
python demo.py
```

**功能**:
- ✅ 学生数据管理演示
- ✅ 学习记录追踪
- ✅ 报告生成
- ✅ 无需 API 密钥

### 模式2: 交互式学习

```bash
python main.py
```

**流程**:
1. 输入学生 ID
2. 创建或加载学生资料
3. 选择学习科目和难度
4. 回答问题并获得实时反馈
5. 查看学习报告和建议

### 模式3: 示例代码

```bash
python example_usage.py
```

**包含示例**:
- 问题生成
- 错误分析
- 学习记录追踪
- 报告生成
- 补习计划制定

## 文件结构

```
c:\Users\user\Desktop\LLM\
├── main.py                          # 主应用程序
├── demo.py                          # 演示脚本（无需API）
├── example_usage.py                 # 使用示例
├── config.py                        # 配置文件
├── sample_data.py                   # 样本数据
├── requirements.txt                 # 依赖列表
├── .env.example                     # 环境变量示例
│
├── models/                          # 核心模块
│   ├── __init__.py
│   ├── llm_client.py               # LLM API 客户端
│   ├── question_generator.py       # 问题生成器
│   └── error_analyzer.py           # 错误分析器
│
├── utils/                           # 工具模块
│   ├── __init__.py
│   ├── data_processor.py           # 数据处理
│   └── report_generator.py         # 报告生成
│
├── students/                        # 学生数据目录（自动创建）
│   ├── student_*.json
│   └── records_*.json
│
├── README.md                        # 项目说明
├── QUICKSTART.md                    # 快速开始指南
├── ARCHITECTURE.md                  # 架构设计文档
└── INSTALL.md                       # 本文件
```

## 常见问题

### Q1: ImportError: No module named 'openai'

**解决方案**:
```bash
pip install openai
```

或重新安装所有依赖：
```bash
pip install -r requirements.txt
```

### Q2: ModuleNotFoundError: No module named 'dotenv'

**解决方案**:
```bash
pip install python-dotenv
```

### Q3: 获得 "api key not found" 错误

**解决方案**:
1. 确认 API 密钥已复制
2. 检查 .env 文件中的密钥格式
3. 确保没有多余的空格或引号
4. 重启程序加载新的环境变量

### Q4: 请求超时

**解决方案**:
1. 检查网络连接
2. 增加超时时间（在 config.py 中）
3. 尝试使用不同的 LLM 模型

### Q5: 如何离线使用？

**解决方案**:
- 使用 `demo.py` 进行本地演示
- 集成本地 LLM（如 Llama）
- 参考 ARCHITECTURE.md 中的扩展指南

## 性能优化建议

### 1. 使用虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
.\venv\Scripts\Activate.ps1
# macOS/Linux:
source venv/bin/activate
```

### 2. 升级 pip

```bash
pip install --upgrade pip
```

### 3. 使用更快的 LLM

在 config.py 中：
```python
MODEL_NAME = "gpt-3.5-turbo"  # 更快但不如 GPT-4 准确
# vs
MODEL_NAME = "gpt-4"          # 更准确但更慢和更贵
```

## 安全最佳实践

### ✅ 推荐做法

- 使用 .env 文件存储敏感信息
- 定期轮换 API 密钥
- 在 .gitignore 中排除 .env 文件
- 限制 API 密钥的访问权限

### ❌ 不要做

- 不要在代码中硬编码 API 密钥
- 不要将 .env 文件提交到 Git
- 不要与他人共享 API 密钥
- 不要在日志中输出 API 密钥

## 数据备份

学生数据存储在 `./students/` 目录：

```bash
# 备份数据
cp -r students students_backup

# macOS/Linux
tar -czf students_backup.tar.gz students/

# Windows PowerShell
Compress-Archive -Path students -DestinationPath students_backup.zip
```

## 卸载

如果要完全移除项目：

```bash
# 停用虚拟环境
deactivate

# 删除虚拟环境
rm -r venv  # macOS/Linux
rmdir /s venv  # Windows

# 删除项目目录
cd ..
rm -r LLM  # macOS/Linux
rmdir /s LLM  # Windows
```

## 获取帮助

### 查看文档

- [README.md](README.md) - 项目概述
- [QUICKSTART.md](QUICKSTART.md) - 快速开始
- [ARCHITECTURE.md](ARCHITECTURE.md) - 系统架构

### 常见错误排查

1. **导入错误**：重新安装依赖
2. **API 错误**：检查密钥和网络
3. **数据错误**：检查 students/ 目录权限
4. **性能问题**：降低 NUM_QUESTIONS_PER_SESSION

### 获取 API 错误详情

在 config.py 中启用详细输出：
```python
VERBOSE_OUTPUT = True
```

## 下一步

1. ✅ 运行 `python demo.py` 看看系统如何工作
2. ✅ 阅读 [ARCHITECTURE.md](ARCHITECTURE.md) 了解系统设计
3. ✅ 配置 API 密钥运行 `python main.py`
4. ✅ 查看 [example_usage.py](example_usage.py) 学习 API 用法
5. ✅ 自定义系统以适应你的需求

## 支持

如有问题：
1. 查看 [README.md](README.md) FAQ 部分
2. 检查错误日志输出
3. 参考 [ARCHITECTURE.md](ARCHITECTURE.md) 了解系统设计

---

**最后更新**: 2025-01-01  
**版本**: 1.0
