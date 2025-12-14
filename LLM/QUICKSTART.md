# 知识加油站 - 快速开始指南

## 功能概览

知识加油站是一个AI驱动的个性化学习辅助系统，专为中小学生设计。

### 核心功能：

1. **📝 个性化问题生成**
   - 根据学生的薄弱科目和学习水平生成定制化问题
   - 支持多个科目和难度等级
   - 循序渐进的学习进度

2. **❌ 错误分析与反馈**
   - 分析学生错误的根本原因
   - 提供详细的解释和学习建议
   - 生成相似题目进行强化练习

3. **📊 学习进度追踪**
   - 记录每次练习的成绩
   - 追踪多个科目的学习进度
   - 识别需要改进的领域

4. **📈 智能报告生成**
   - 生成个性化学习报告
   - 提供针对性的学习建议
   - 制定补习计划

## 快速开始

### 前置条件

- Python 3.8 或更高版本
- OpenAI API 密钥（或其他兼容的LLM API）

### 安装步骤

1. **克隆/下载项目**
   ```bash
   cd c:\Users\user\Desktop\LLM
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **配置API密钥**
   - 复制 `.env.example` 为 `.env`
   - 在 `.env` 中填入你的 OpenAI API 密钥
   
   或者在 `config.py` 中直接设置：
   ```python
   OPENAI_API_KEY = "sk-your-api-key"
   ```

### 运行应用

#### 方式1: 交互式学习会话

```bash
python main.py
```

这将启动一个交互式会话，你可以：
- 创建或加载学生资料
- 参加学习测试
- 获取实时反馈和建议

#### 方式2: 运行示例

```bash
python example_usage.py
```

查看各种功能的使用示例。

#### 方式3: 在你的代码中使用

```python
from models import LLMClient, QuestionGenerator, ErrorAnalyzer
from utils import DataProcessor, ReportGenerator

# 初始化
llm = LLMClient()
question_gen = QuestionGenerator(llm)
analyzer = ErrorAnalyzer(llm)
data_proc = DataProcessor()

# 创建学生资料
student_profile = {
    "name": "李明",
    "grade": "初二",
    "weak_subjects": ["数学", "英语"],
    "learning_style": "visual"
}

# 生成问题
questions = question_gen.generate_questions(student_profile, num_questions=5)

# 分析错误
analysis = analyzer.analyze_error(
    question="2 + 2 = ?",
    student_answer="5",
    correct_answer="4"
)
```

## 主要模块

### models/
- **llm_client.py**: LLM API 集成
- **question_generator.py**: 问题生成引擎
- **error_analyzer.py**: 错误分析和反馈

### utils/
- **data_processor.py**: 学生数据管理
- **report_generator.py**: 报告生成

### main.py
- 交互式学习应用程序

### config.py
- 全局配置和参数设置

## 配置选项

在 `config.py` 中可以自定义：

```python
# LLM 配置
OPENAI_API_KEY = "your-key"
MODEL_NAME = "gpt-3.5-turbo"  # 或 "gpt-4"
TEMPERATURE = 0.7  # 生成文本的创意度

# 学习配置
SUBJECTS = ["数学", "英语", "物理", ...]
NUM_QUESTIONS_PER_SESSION = 5
DIFFICULTY_LEVELS = {"easy": 1, "medium": 2, "hard": 3}

# 错误分析
ERROR_ANALYSIS_DEPTH = "detailed"
INCLUDE_HINTS = True
INCLUDE_SIMILAR_PROBLEMS = True
```

## 工作流程示例

### 1. 创建学生资料

```python
from main import KnowledgeFuelStation

app = KnowledgeFuelStation()
student = app.create_student_profile(
    student_id="S001",
    name="张三",
    grade="初一",
    weak_subjects=["数学", "英语"]
)
```

### 2. 开始学习会话

```python
session = app.start_learning_session()
```

### 3. 处理答案并获得反馈

```python
feedback = app.process_answer(
    session=session,
    question_index=0,
    student_answer="用户的答案"
)
print(feedback['feedback'])
```

### 4. 结束会话并生成报告

```python
summary = app.end_session(session)
print(summary['report'])
print(summary['recommendations'])
```

## 数据存储

学生数据存储在 `./students/` 目录下：
- `student_{id}.json`: 学生资料
- `records_{id}.json`: 学习记录

## API 概览

### LLMClient
- `generate_text()`: 生成文本
- `generate_multiple()`: 生成多个变体
- `chat()`: 对话式交互

### QuestionGenerator
- `generate_questions()`: 生成个性化问题
- `generate_quiz()`: 生成完整测试
- `generate_followup_question()`: 生成后续问题

### ErrorAnalyzer
- `analyze_error()`: 分析单个错误
- `analyze_multiple_errors()`: 分析多个错误
- `generate_remedial_plan()`: 制定补习计划

### DataProcessor
- `save_student_profile()`: 保存学生信息
- `load_student_profile()`: 加载学生信息
- `save_learning_record()`: 保存学习记录
- `get_progress_summary()`: 获取进度摘要
- `calculate_weak_subjects()`: 计算薄弱科目

### ReportGenerator
- `generate_learning_report()`: 生成学习报告
- `generate_recommendations()`: 生成学习建议
- `generate_performance_chart()`: 生成表现图表

## 常见问题

### Q: 如何更改LLM模型？
A: 在 `config.py` 中修改 `MODEL_NAME`，或在初始化 LLMClient 时指定：
```python
llm = LLMClient(model="gpt-4")
```

### Q: 可以离线使用吗？
A: 目前不可以，需要API连接。但可以修改代码集成本地LLM。

### Q: 如何扩展系统？
A: 
1. 继承现有类（如 `QuestionGenerator`）
2. 添加新的分析方法
3. 实现自定义反馈逻辑

### Q: 支持哪些科目？
A: 默认支持数学、英语、物理、化学等。可在 `config.py` 的 `SUBJECTS` 中修改。

## 系统架构

```
┌─────────────────────────────────────┐
│  Interactive Learning Interface     │
│         (main.py)                   │
└────────────────┬────────────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────┐  ┌──────────┐  ┌──────────┐
│LLMClie │  │Question  │  │Error     │
│nt      │  │Generator │  │Analyzer  │
└────────┘  └──────────┘  └──────────┘
    │            │            │
    └────────────┼────────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
    ▼            ▼            ▼
┌────────────┐ ┌──────────┐ ┌─────────────┐
│DataProcess │ │Report    │ │Config/Utils │
│ор         │ │Generator │ │             │
└────────────┘ └──────────┘ └─────────────┘
```

## 开发计划

- [ ] 支持更多LLM提供商（Claude, Gemini等）
- [ ] 添加图像识别用于题目辅助
- [ ] 实现语音交互
- [ ] 开发Web界面
- [ ] 添加教师管理面板
- [ ] 支持本地LLM集成

## 许可证

MIT License

## 支持和贡献

欢迎提交问题和拉取请求！

## 更新日志

### v1.0.0 (2025-01-01)
- 初始发布
- 核心功能完成
- 基本的交互式学习支持
