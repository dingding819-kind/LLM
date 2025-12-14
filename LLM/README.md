# Knowledge Fuel Station - AI Learning Assistant

一个基于大语言模型(LLM)的交互式学习辅助系统，专为农村地区的中小学生设计。

## 功能特性

### 1. 个性化问题生成
- 根据学生的学习记录和薄弱领域生成定制化问题
- 帮助学生识别和加强知识漏洞

### 2. 错误分析与解释
- 分析学生的错误答案
- 提供详细的错误原因解释
- 通过重复练习强化知识点

### 3. 交互式学习反馈
- 实时的Q&A反馈循环
- 根据学生反馈动态调整教学内容
- 追踪学习进度

### 4. 学习分析
- 识别学生需要加强的主题
- 生成学习报告和建议

## 项目结构

```
knowledge-fuel-station/
├── main.py                 # 主应用程序
├── config.py              # 配置文件
├── students/              # 学生数据存储
│   └── sample_data.json   # 样本学生数据
├── models/                # LLM模块
│   ├── question_generator.py     # 问题生成器
│   ├── error_analyzer.py         # 错误分析器
│   └── llm_client.py             # LLM客户端
├── utils/
│   ├── data_processor.py   # 数据处理
│   └── report_generator.py # 报告生成
└── requirements.txt       # 依赖项
```

## 安装与运行

### 环境配置

1. 确保已安装 Python 3.8+
2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置 OpenAI API 密钥（在 `config.py` 中）：
```python
OPENAI_API_KEY = "your-api-key-here"
```

### 运行应用

```bash
python main.py
```

## 使用示例

### 交互式问答

```python
from models.llm_client import LLMClient
from models.question_generator import QuestionGenerator

# 初始化
llm = LLMClient()
generator = QuestionGenerator(llm)

# 生成问题
student_progress = {
    "weak_subjects": ["数学", "英语"],
    "last_test": "数学竞赛",
    "score": 75
}

questions = generator.generate_questions(student_progress, num_questions=5)
```

### 错误分析

```python
from models.error_analyzer import ErrorAnalyzer

analyzer = ErrorAnalyzer(llm)

error_context = {
    "question": "2+2=?",
    "student_answer": "5",
    "correct_answer": "4"
}

explanation = analyzer.analyze_error(error_context)
print(explanation)
```

## 核心算法

### 问题生成流程
1. 分析学生学习记录
2. 识别薄弱领域
3. 使用LLM生成针对性问题
4. 评估难度等级

### 错误分析流程
1. 收集错误信息
2. 使用LLM分析根本原因
3. 生成解释和建议
4. 记录学习数据

## 配置选项

查看 `config.py` 以自定义：
- LLM 模型选择
- 问题难度级别
- 学习主题
- 反馈循环参数

## 数据隐私

所有学生数据存储在本地，遵守教育数据保护规范。

## 贡献

欢迎提交 PR 或报告问题！

## 许可证

MIT License
