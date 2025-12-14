# 📖 如何使用知识加油站 - 完整教程

## 🎯 三种主要使用方式

### 方式1️⃣: 演示模式（最简单 - 推荐初次使用）

**命令**:
```bash
python demo.py
```

**这个演示会**:
- ✅ 展示所有6个主要功能
- ✅ 生成示例学生数据
- ✅ 创建学习记录
- ✅ 生成完整报告
- ✅ 演示性能图表
- ✅ **无需 API 密钥**

**输出示例**:
```
【学生 李明 的学习摘要】
  总练习题数: 14
  正确答案数: 8
  总体正确率: 57.1%

【科目分析】
  数学: 4/6 (66.7%)
  英语: 4/6 (66.7%)
  物理: 0/2 (0.0%)

【薄弱科目】
  1. 物理 - 需要重点改进
  2. 英语 - 需要加强
  3. 数学 - 继续努力
```

---

### 方式2️⃣: 使用示例（实际应用）

**命令**:
```bash
python usage_examples.py
```

**这个脚本演示**:
1. 创建学生资料
2. 记录学习会话
3. 生成学习报告
4. 创建性能图表
5. 生成学习建议
6. 导出报告到文件
7. 加载已保存的数据
8. 自定义数据分析

**代码示例**:
```python
from utils import DataProcessor, ReportGenerator

# 创建学生
processor = DataProcessor()
student = {"student_id": "S001", "name": "李明", "grade": "初二"}
processor.save_student_profile(student["student_id"], student)

# 记录练习
processor.update_student_progress(
    student_id="S001",
    question_id=1,
    correct=True,
    subject="数学",
    time_spent=120
)

# 生成报告
progress = processor.get_progress_summary("S001")
reporter = ReportGenerator()
report = reporter.generate_learning_report("李明", progress)
print(report)
```

---

### 方式3️⃣: 交互式学习（完整功能 - 需要API密钥）

**命令**:
```bash
python main.py
```

**交互流程**:

```
1. 输入学生ID
   → "S001"

2. 输入学生信息
   → 名字: 李明
   → 年级: 初二
   → 薄弱科目: 数学, 英语

3. 系统生成5道问题
   → 根据学生资料自适应生成

4. 开始答题
   问题1: 求方程 2x + 5 = 13 的解
   你的答案: x = 4
   ✅ 正确！很好地掌握了这个知识点

5. 获得详细反馈
   ├── 是否正确
   ├── 解释说明
   ├── 改进提示
   └── 相似练习题

6. 查看报告
   ├── 总体表现
   ├── 科目分析
   ├── 薄弱领域
   └── 学习建议
```

---

## 🚀 快速开始（5分钟）

### 第1步: 安装

```bash
cd c:\Users\user\Desktop\LLM
pip install -r requirements.txt
```

### 第2步: 运行演示

```bash
python demo.py
```

看到完整的功能演示输出！

### 第3步: 尝试使用示例

```bash
python usage_examples.py
```

查看如何创建学生资料和生成报告。

### 第4步: 配置API（可选）

如果要使用完整的问题生成功能：

```bash
# 方法1: 编辑 .env 文件
copy .env.example .env
# 然后编辑 .env，添加你的 API 密钥
OPENAI_API_KEY=sk-your-key-here

# 方法2: 直接编辑 config.py
# 找到这行：OPENAI_API_KEY = "sk-your-key-here"
# 替换为你的实际密钥
```

### 第5步: 运行交互式应用

```bash
python main.py
```

---

## 📚 五个实际场景

### 场景1: 为学生创建资料并追踪学习

```python
from utils import DataProcessor

processor = DataProcessor()

# 创建学生
student = {
    "student_id": "S_CLASS_001",
    "name": "张三",
    "grade": "初一",
    "weak_subjects": ["数学"],
    "learning_style": "visual"
}
processor.save_student_profile(student["student_id"], student)

# 记录一周的练习
for day in range(7):
    processor.update_student_progress(
        student_id="S_CLASS_001",
        question_id=day+1,
        correct=day % 2 == 0,  # 奇偶天数
        subject="数学",
        time_spent=120
    )

# 查看进度
progress = processor.get_progress_summary("S_CLASS_001")
print(f"一周学习成果: {progress['accuracy']:.1f}% 正确率")
```

---

### 场景2: 为多个班级的学生生成报告

```python
from utils import DataProcessor, ReportGenerator

processor = DataProcessor()
reporter = ReportGenerator()

# 班级中的学生ID列表
students = ["S_MATH_01", "S_MATH_02", "S_MATH_03"]

for student_id in students:
    # 获取学生进度
    progress = processor.get_progress_summary(student_id)
    
    if progress['total_questions'] > 0:
        # 生成报告
        student_name = processor.load_student_profile(student_id)['name']
        report = reporter.generate_learning_report(student_name, progress)
        
        # 导出到文件
        filename = f"报告_{student_id}.txt"
        reporter.export_report_to_file(report, filename)
        print(f"✅ 已为 {student_name} 生成报告")
```

---

### 场景3: 识别班级中的薄弱领域

```python
from utils import DataProcessor

processor = DataProcessor()

# 分析整个班级
class_weak_areas = {}

for student_id in ["S001", "S002", "S003"]:
    weak_subjects = processor.calculate_weak_subjects(student_id)
    for subject in weak_subjects:
        class_weak_areas[subject] = class_weak_areas.get(subject, 0) + 1

# 找出最需要帮助的科目
priority = sorted(class_weak_areas.items(), key=lambda x: x[1], reverse=True)
print("班级最需要加强的科目：")
for subject, count in priority:
    print(f"  {subject}: {count} 名学生需要帮助")
```

---

### 场景4: 使用LLM生成个性化问题（需要API）

```python
from models import LLMClient, QuestionGenerator

llm = LLMClient()
generator = QuestionGenerator(llm)

# 为薄弱学生生成补习问题
student = {
    "name": "李明",
    "grade": "初二",
    "weak_subjects": ["数学"],
    "learning_style": "visual"
}

# 生成10道数学题用于加强
questions = generator.generate_questions(
    student,
    num_questions=10,
    subject="数学",
    difficulty="easy"  # 从简单开始
)

print("为李明生成的补习题目：\n")
for i, q in enumerate(questions, 1):
    print(f"{i}. {q['question']}")
    print(f"   答案: {q['standard_answer']}\n")
```

---

### 场景5: 分析错误模式并生成补习计划（需要API）

```python
from models import LLMClient, ErrorAnalyzer

llm = LLMClient()
analyzer = ErrorAnalyzer(llm)

# 学生最近犯的错误
errors = [
    {"q": "2+2", "a": "5", "c": "4", "s": "数学"},
    {"q": "3+3", "a": "7", "c": "6", "s": "数学"},
    {"q": "5+2", "a": "8", "c": "7", "s": "数学"},
]

# 转换格式
error_cases = [
    {
        "question": e["q"],
        "student_answer": e["a"],
        "correct_answer": e["c"],
        "subject": e["s"]
    }
    for e in errors
]

# 分析模式
result = analyzer.analyze_multiple_errors(error_cases)
print(f"错误模式分析：")
print(f"  发现 {result['total_errors']} 个错误")
print(f"  主要问题: {list(result['error_patterns'].keys())}")

# 生成补习计划
plan = analyzer.generate_remedial_plan("李明", result)
print(f"\n补习计划：\n{plan['remedial_plan']}")
```

---

## 📊 输出示例

### 学习报告示例

```
==================================================
学习进度报告
==================================================

学生姓名：李明
生成日期：2025-12-14 15:13:18

【整体表现】
总练习题数：14
正确答案数：8
正确率：57.1%

【科目分析】

数学:
  练习题数：6
  正确数：4
  正确率：66.7%

英语:
  练习题数：6
  正确数：4
  正确率：66.7%

物理:
  练习题数：2
  正确数：0
  正确率：0.0%

【需要改进的科目】(按优先级)
1. 物理
2. 英语
3. 数学

==================================================
```

### 性能图表

```
【正确率对比】
数学 | █████████████░░░░░░░ 66.7%
英语 | █████████████░░░░░░░ 66.7%
物理 | ░░░░░░░░░░░░░░░░░░░░ 0.0%
```

### 学习建议

```
【学习建议】

⚠️ 整体表现需要显著改进
   • 建议每天花更多时间学习基础知识
   • 针对正确率最低的科目进行重点复习
   • 考虑寻求额外的学习资源或辅导

针对薄弱科目的建议：

1. 物理 (正确率: 0.0%)
   • 进行10次练习
   • 重点复习基础知识
   • 在练习中记录常见错误
```

---

## 🔑 API 快速参考

### 创建学生和记录学习

```python
from utils import DataProcessor

processor = DataProcessor()

# 保存学生
processor.save_student_profile("S001", {
    "student_id": "S001",
    "name": "李明",
    "grade": "初二"
})

# 记录练习
processor.update_student_progress(
    student_id="S001",
    question_id=1,
    correct=True,
    subject="数学"
)

# 获取进度
progress = processor.get_progress_summary("S001")
```

### 生成报告

```python
from utils import ReportGenerator

reporter = ReportGenerator()

# 生成报告
report = reporter.generate_learning_report("李明", progress)

# 生成图表
chart = reporter.generate_performance_chart(progress)

# 生成建议
recommendations = reporter.generate_recommendations(progress)

# 导出文件
reporter.export_report_to_file(report + chart + recommendations, "report.txt")
```

### 生成问题和分析错误（需要API）

```python
from models import LLMClient, QuestionGenerator, ErrorAnalyzer

llm = LLMClient()

# 生成问题
generator = QuestionGenerator(llm)
questions = generator.generate_questions(student_profile)

# 分析错误
analyzer = ErrorAnalyzer(llm)
analysis = analyzer.analyze_error(
    question="问题文本",
    student_answer="学生答案",
    correct_answer="正确答案"
)
```

---

## 📁 项目文件速查

| 文件 | 用途 |
|------|------|
| `demo.py` | 演示脚本（无API）|
| `main.py` | 交互式应用（需API）|
| `usage_examples.py` | 使用示例 |
| `quick_reference.py` | 快速参考 |
| `config.py` | 配置文件 |
| `models/` | 核心模块 |
| `utils/` | 工具模块 |
| `students/` | 学生数据 |

---

## 💡 提示和技巧

1. **快速测试**: 用 `demo.py` 快速了解系统
2. **学习代码**: 看 `usage_examples.py` 学习如何使用
3. **自定义**: 编辑 `config.py` 调整参数
4. **数据查看**: 打开 `students/` 目录查看JSON文件
5. **生成报告**: 用 `ReportGenerator` 生成文件

---

## 🎓 开始使用

```bash
# 1. 进入项目目录
cd c:\Users\user\Desktop\LLM

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行演示
python demo.py

# 4. 查看示例
python usage_examples.py

# 5. 查看快速参考
python quick_reference.py
```

**就这样！你已经准备好使用知识加油站了！** 🎉

---

**需要帮助？** 查看文档或参考示例代码！
