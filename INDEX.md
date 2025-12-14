# 📑 知识加油站 - 完整索引指南

欢迎使用知识加油站！本文档帮助你快速找到需要的信息。

---

## 🚀 我想要...

### 立即看演示
**→ 运行**: `python demo.py`  
**→ 文档**: 无需任何配置，直接看结果！

### 快速了解系统
**→ 文档**: [QUICKSTART.md](QUICKSTART.md)  
**→ 或看**: [HOW_TO_USE.md](HOW_TO_USE.md)

### 安装和配置
**→ 文档**: [INSTALL.md](INSTALL.md)  
**→ 依赖**: `pip install -r requirements.txt`

### 学习如何使用
**→ 运行**: `python usage_examples.py`  
**→ 文档**: [HOW_TO_USE.md](HOW_TO_USE.md)

### 查看快速参考
**→ 运行**: `python quick_reference.py`  
**→ 或看**: 下面的 "🔧 API参考" 部分

### 了解系统架构
**→ 文档**: [ARCHITECTURE.md](ARCHITECTURE.md)

### 使用完整功能（需要API）
**→ 运行**: `python main.py`  
**→ 指南**: [INSTALL.md](INSTALL.md#获取-openai-api-密钥)

### 查看项目完成情况
**→ 文档**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)  
**→ 或看**: [CHECKLIST.md](CHECKLIST.md)

---

## 📚 文档地图

```
┌─ 🚀 快速开始
│  ├─ QUICKSTART.md          ← 5分钟快速入门
│  ├─ HOW_TO_USE.md          ← 详细使用教程
│  └─ INSTALL.md             ← 安装和配置
│
├─ 📖 深入了解
│  ├─ README.md              ← 项目功能概述
│  ├─ ARCHITECTURE.md        ← 系统设计原理
│  ├─ PROJECT_SUMMARY.md     ← 项目完成总结
│  └─ CHECKLIST.md           ← 项目验收清单
│
├─ 💻 代码示例
│  ├─ demo.py                ← 功能演示（推荐首先运行）
│  ├─ usage_examples.py      ← 8个使用场景
│  ├─ example_usage.py       ← 高级用法示例
│  ├─ quick_reference.py     ← 快速参考指南
│  └─ sample_data.py         ← 示例数据
│
├─ ⚙️ 配置文件
│  ├─ config.py              ← 全局配置选项
│  ├─ requirements.txt       ← Python依赖
│  └─ .env.example           ← API密钥配置模板
│
├─ 🧠 核心模块 (models/)
│  ├─ llm_client.py          ← LLM API客户端
│  ├─ question_generator.py  ← 问题生成引擎
│  └─ error_analyzer.py      ← 错误分析器
│
├─ 📊 工具模块 (utils/)
│  ├─ data_processor.py      ← 学生数据管理
│  └─ report_generator.py    ← 报告生成器
│
└─ 💾 数据目录 (students/)
   ├─ student_*.json         ← 学生资料
   ├─ records_*.json         ← 学习记录
   └─ *.txt                 ← 导出的报告
```

---

## 🎯 按场景选择

### 场景1: 我是新手，想快速了解系统
```
1. 运行: python demo.py
2. 阅读: HOW_TO_USE.md
3. 尝试: python usage_examples.py
4. 参考: quick_reference.py
```

### 场景2: 我想为学生创建学习记录
```
1. 查看: HOW_TO_USE.md - 场景1
2. 参考: quick_reference.py 的【场景1】部分
3. 运行: python usage_examples.py 查看实际例子
4. 代码示例: 下面的【为学生创建资料】部分
```

### 场景3: 我想生成学习报告
```
1. 查看: HOW_TO_USE.md - 场景2
2. 参考: quick_reference.py 的【场景2】部分
3. 代码示例: 下面的【生成学习报告】部分
4. 运行: python usage_examples.py
```

### 场景4: 我想使用AI生成问题（需要API）
```
1. 获取API密钥: INSTALL.md - 获取API密钥部分
2. 配置API: INSTALL.md - 配置步骤
3. 参考: quick_reference.py 的【场景3】部分
4. 运行: python main.py
```

### 场景5: 我想自定义系统功能
```
1. 了解架构: ARCHITECTURE.md
2. 查看代码: models/ 和 utils/ 目录
3. 修改配置: config.py
4. 参考: PROJECT_SUMMARY.md - 扩展方向部分
```

---

## 🔧 快速代码参考

### 创建学生资料
```python
from utils import DataProcessor

processor = DataProcessor()
processor.save_student_profile("S001", {
    "student_id": "S001",
    "name": "李明",
    "grade": "初二",
    "weak_subjects": ["数学", "英语"]
})
```

### 记录学习进度
```python
processor.update_student_progress(
    student_id="S001",
    question_id=1,
    correct=True,
    subject="数学",
    time_spent=120
)
```

### 生成学习报告
```python
from utils import ReportGenerator

processor = DataProcessor()
reporter = ReportGenerator()

progress = processor.get_progress_summary("S001")
report = reporter.generate_learning_report("李明", progress)
print(report)
```

### 导出报告到文件
```python
reporter.export_report_to_file(report_content, "学生报告.txt")
```

### 生成个性化问题（需要API）
```python
from models import LLMClient, QuestionGenerator

llm = LLMClient()
gen = QuestionGenerator(llm)

questions = gen.generate_questions(
    student_profile,
    num_questions=5
)
```

### 分析错误（需要API）
```python
from models import ErrorAnalyzer

analyzer = ErrorAnalyzer(llm)
analysis = analyzer.analyze_error(
    question="2+2=?",
    student_answer="5",
    correct_answer="4"
)
```

---

## 📊 生成的示例文件

运行演示后，这些文件已经生成：

| 文件 | 内容 |
|------|------|
| `demo_report_S001.txt` | 学生李明的学习报告 |
| `学生报告_S_USER_001.txt` | 学生张三的学习报告 |
| `students/student_S001.json` | 学生李明的资料 |
| `students/student_S002.json` | 学生王芳的资料 |
| `students/records_S001.json` | 学生李明的学习记录 |

---

## ⚙️ 配置选项速查

在 `config.py` 中修改：

```python
# LLM配置
OPENAI_API_KEY = "sk-..."      # 你的API密钥
MODEL_NAME = "gpt-3.5-turbo"   # 模型选择
TEMPERATURE = 0.7              # 创意度

# 学习配置
SUBJECTS = ["数学", "英语", ...] # 支持的科目
NUM_QUESTIONS_PER_SESSION = 5  # 每次会话题数

# 错误分析
ERROR_ANALYSIS_DEPTH = "detailed"  # 分析深度
INCLUDE_HINTS = True           # 是否包含提示
INCLUDE_SIMILAR_PROBLEMS = True # 是否推荐练习
```

---

## 🐛 常见问题速答

| 问题 | 答案 |
|------|------|
| 需要API密钥吗？ | 演示和示例不需要，完整功能需要 |
| 第一步应该做什么？ | 运行 `python demo.py` |
| 如何获取API密钥？ | 查看 [INSTALL.md](INSTALL.md#获取-openai-api-密钥) |
| 数据保存在哪里？ | `students/` 目录 |
| 如何修改设置？ | 编辑 `config.py` |
| 支持离线使用吗？ | 演示功能支持，完整功能需要网络 |
| 可以添加新科目吗？ | 可以，在 `config.py` 的 `SUBJECTS` 中添加 |

查看 [INSTALL.md](INSTALL.md) 获取更多帮助。

---

## 📈 功能清单

### 已实现 ✅
- [x] 学生数据管理
- [x] 学习记录追踪
- [x] 进度分析统计
- [x] 报告生成和可视化
- [x] 学习建议生成
- [x] LLM集成
- [x] 问题生成（需API）
- [x] 错误分析（需API）

### 演示功能 ✅
- [x] 无API演示
- [x] 使用示例脚本
- [x] 快速参考指南
- [x] 完整文档

---

## 🎓 学习路径

### 初级（30分钟）
1. 运行 `python demo.py` ← 5分钟
2. 阅读 [HOW_TO_USE.md](HOW_TO_USE.md) ← 10分钟
3. 运行 `python usage_examples.py` ← 5分钟
4. 查看生成的报告文件 ← 10分钟

### 中级（1小时）
1. 阅读 [QUICKSTART.md](QUICKSTART.md)
2. 研究 `usage_examples.py` 代码
3. 修改 `config.py` 尝试自定义
4. 为自己的学生创建资料并生成报告

### 高级（2小时）
1. 阅读 [ARCHITECTURE.md](ARCHITECTURE.md)
2. 研究 `models/` 和 `utils/` 源代码
3. 获取API密钥并配置
4. 运行 `python main.py` 体验完整功能
5. 尝试扩展系统功能

---

## 📞 获得帮助

### 快速帮助
- 📖 查看相关文档（见上面的文档地图）
- 🚀 运行示例脚本查看实际效果
- 📋 查看快速参考指南

### 详细帮助
- 🏗️ 系统设计 → [ARCHITECTURE.md](ARCHITECTURE.md)
- ⚙️ 安装配置 → [INSTALL.md](INSTALL.md)
- 💻 代码示例 → 各 `.py` 文件

### 问题排查
1. 检查依赖是否安装: `pip install -r requirements.txt`
2. 检查配置是否正确: 查看 `config.py`
3. 查看错误信息: 运行脚本时查看输出
4. 参考相关文档或 FAQ

---

## 🚀 立即开始

```bash
# 最简单的方法 - 直接看演示
python demo.py

# 或学习如何使用
python usage_examples.py

# 或查看快速参考
python quick_reference.py
```

---

## 📋 检查清单

在深入使用之前：

- [ ] 已安装 Python 3.8+
- [ ] 已运行 `pip install -r requirements.txt`
- [ ] 已运行 `python demo.py` 查看演示
- [ ] 已阅读 [QUICKSTART.md](QUICKSTART.md) 或 [HOW_TO_USE.md](HOW_TO_USE.md)
- [ ] 理解三种使用方式（演示、示例、交互）
- [ ] 知道在哪里找到帮助（本文档）

---

## 📚 按主题的完整资源

### 快速开始
- [QUICKSTART.md](QUICKSTART.md) - 5分钟快速开始
- [HOW_TO_USE.md](HOW_TO_USE.md) - 详细使用教程
- [INSTALL.md](INSTALL.md) - 安装和配置

### 理解系统
- [README.md](README.md) - 项目功能
- [ARCHITECTURE.md](ARCHITECTURE.md) - 系统设计
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - 项目总结

### 代码和示例
- [demo.py](demo.py) - 功能演示
- [usage_examples.py](usage_examples.py) - 使用示例
- [quick_reference.py](quick_reference.py) - 快速参考

### 验证和项目信息
- [CHECKLIST.md](CHECKLIST.md) - 验收清单
- [USAGE_DEMO_SUMMARY.md](USAGE_DEMO_SUMMARY.md) - 演示总结

---

## 🎉 你现在已准备好使用知识加油站！

选择你的下一步：

- 🏃 **快速体验**: 运行 `python demo.py`
- 📚 **详细学习**: 读 [HOW_TO_USE.md](HOW_TO_USE.md)
- 💻 **查看代码**: 阅读 [usage_examples.py](usage_examples.py)
- 🔍 **快速查询**: 运行 `python quick_reference.py`
- 🏗️ **深入理解**: 读 [ARCHITECTURE.md](ARCHITECTURE.md)

---

**版本**: 1.0  
**最后更新**: 2025-12-14  
**状态**: ✅ 完全就绪

祝你使用愉快！ 🌟
