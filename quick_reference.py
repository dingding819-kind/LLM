#!/usr/bin/env python3
"""
快速参考指南 - 常见使用场景
Quick Reference Guide - Common Usage Scenarios
"""

print("""
╔════════════════════════════════════════════════════════════════════════╗
║           知識加油站 - 快速參考指南 v1.0                               ║
║        Knowledge Fuel Station - Quick Reference Guide                  ║
╚════════════════════════════════════════════════════════════════════════╝

📚 三種使用方式
═══════════════════════════════════════════════════════════════════════

【方式1】運行演示（推薦首次使用）
─────────────────────────────────
  $ python demo.py
  
  特點：
  ✅ 無需 API 金鑰
  ✅ 展示所有主要功能
  ✅ 生成示例數據和報告
  ✅ 5 分鐘快速了解系統

【方式2】互動式學習（需要API金鑰）
──────────────────────────────────
  $ python main.py
  
  流程：
  1. 輸入學生 ID
  2. 建立/載入學生資料
  3. 開始學習會話
  4. 回答系統生成的問題
  5. 獲取即時反饋
  6. 查看學習報告

【方式3】編程使用（完整自訂）
─────────────────────────────────
  $ python usage_examples.py
  
  或在你的代碼中：
  
  from models import LLMClient, QuestionGenerator
  from utils import DataProcessor, ReportGenerator
    
  # 初始化
  llm = LLMClient()
  gen = QuestionGenerator(llm)
  processor = DataProcessor()
    
  # 使用...


═══════════════════════════════════════════════════════════════════════
🎓 常見使用場景
═══════════════════════════════════════════════════════════════════════

【場景1】為學生建立學習記錄
─────────────────────────
from utils import DataProcessor

processor = DataProcessor()

# 建立學生資料
student = {
  "student_id": "S001",
  "name": "李明",
  "grade": "初二",
  "weak_subjects": ["數學", "英語"],
  "learning_style": "visual"
}
processor.save_student_profile(student["student_id"], student)

# 紀錄一次練習
processor.update_student_progress(
  student_id="S001",
  question_id=1,
  correct=True,
  subject="數學",
  time_spent=120
)

【場景2】生成學習報告
─────────────────────
from utils import DataProcessor, ReportGenerator

processor = DataProcessor()
reporter = ReportGenerator()

# 獲取學生進度
progress = processor.get_progress_summary("S001", num_records=20)

# 生成報告
report = reporter.generate_learning_report("李明", progress)
print(report)

# 生成建議
recommendations = reporter.generate_recommendations(progress)
print(recommendations)

【場景3】使用 API 生成個性化問題
─────────────────────────────────
from models import LLMClient, QuestionGenerator

llm = LLMClient()
generator = QuestionGenerator(llm)

student_profile = {
  "name": "李明",
  "grade": "初二",
  "weak_subjects": ["數學"],
  "learning_style": "visual"
}

# 生成 5 道數學問題
questions = generator.generate_questions(
  student_profile,
  num_questions=5,
  subject="數學",
  difficulty="medium"
)

for q in questions:
  print(f"問題: {q['question']}")
  print(f"答案: {q['standard_answer']}")

【場景4】分析學生錯誤
──────────────────────
from models import LLMClient, ErrorAnalyzer

llm = LLMClient()
analyzer = ErrorAnalyzer(llm)

# 分析一個錯誤
analysis = analyzer.analyze_error(
  question="2 + 2 = ?",
  student_answer="5",
  correct_answer="4",
  subject="數學"
)

print(f"根本原因: {analysis['root_cause']}")
print(f"解釋: {analysis['explanation']}")
print(f"提示: {analysis['hints']}")

【場景5】批量分析多個錯誤
──────────────────────────
from models import ErrorAnalyzer

error_cases = [
  {"question": "Q1", "student_answer": "A", "correct_answer": "B", "subject": "數學"},
  {"question": "Q2", "student_answer": "C", "correct_answer": "D", "subject": "英語"},
]

result = analyzer.analyze_multiple_errors(error_cases)
print(f"總錯誤數: {result['total_errors']}")
print(f"錯誤模式: {result['error_patterns']}")

# 生成補習計畫
plan = analyzer.generate_remedial_plan("李明", result)
print(plan['remedial_plan'])


═══════════════════════════════════════════════════════════════════════
⚙️ 配置選項
═══════════════════════════════════════════════════════════════════════

在 config.py 中自訂：

# LLM 設定
OPENAI_API_KEY = "sk-..."          # API 金鑰
MODEL_NAME = "gpt-3.5-turbo"       # 模型選擇
TEMPERATURE = 0.7                  # 創意度 (0-1)
MAX_TOKENS = 1000                  # 最大輸出長度

# 學習設定
SUBJECTS = ["數學", "英語", ...]   # 可用科目
NUM_QUESTIONS_PER_SESSION = 5      # 每次會話問題數
DIFFICULTY_LEVELS = {...}         # 難度級別

# 錯誤分析
ERROR_ANALYSIS_DEPTH = "detailed"  # 分析深度
INCLUDE_HINTS = True               # 是否包含提示
INCLUDE_SIMILAR_PROBLEMS = True    # 是否推薦練習

# 數據存儲
STUDENT_DATA_DIR = "./students"    # 學生數據目錄
PROGRESS_TRACKING = True           # 是否追蹤進度


═══════════════════════════════════════════════════════════════════════
📊 數據結構參考
═══════════════════════════════════════════════════════════════════════

【學生資料格式】
{
  "student_id": "S001",
  "name": "李明",
  "grade": "初二",
  "weak_subjects": ["數學", "英語"],
  "learning_style": "visual",
  "recent_scores": {"數學": 75, "英語": 68},
  "recent_topics": ["代數", "英文時態"]
}

【學習記錄格式】
{
  "timestamp": "2025-01-01T10:30:00",
  "question_id": 1,
  "correct": true,
  "subject": "數學",
  "time_spent": 120,
  "score": 100
}

【問題格式】
{
  "id": 1,
  "subject": "數學",
  "difficulty": "medium",
  "question": "求方程 2x + 5 = 13 的解",
  "standard_answer": "x = 4"
}


═══════════════════════════════════════════════════════════════════════
🔧 API 快速參考
═══════════════════════════════════════════════════════════════════════

【LLMClient】
──────────
client = LLMClient(api_key, model)
client.generate_text(prompt, system_message, temperature, max_tokens)
client.generate_multiple(prompt, num_variations)
client.chat(messages)

【QuestionGenerator】
─────────────────────
gen = QuestionGenerator(llm_client)
gen.generate_questions(student_profile, num_questions, subject, difficulty)
gen.generate_followup_question(question, student_answer, feedback)
gen.generate_practice_questions(topic, num_questions, difficulty)
gen.generate_quiz(student_profile, num_questions)

【ErrorAnalyzer】
─────────────────
analyzer = ErrorAnalyzer(llm_client)
analyzer.analyze_error(question, student_answer, correct_answer, subject)
analyzer.analyze_multiple_errors(error_cases)
analyzer.generate_remedial_plan(student_name, error_analysis_result)

【DataProcessor】
──────────────────
processor = DataProcessor(data_dir)
processor.save_student_profile(student_id, profile)
processor.load_student_profile(student_id)
processor.save_learning_record(student_id, record)
processor.get_learning_records(student_id, limit)
processor.get_progress_summary(student_id, num_records)
processor.calculate_weak_subjects(student_id, num_records)
processor.update_student_progress(student_id, question_id, correct, subject, time_spent)

【ReportGenerator】
────────────────────
gen = ReportGenerator()
gen.generate_learning_report(student_name, progress_summary)
gen.generate_performance_chart(progress_summary, text_based)
gen.generate_recommendations(progress_summary, error_patterns)
gen.generate_comparison_report(student_name, current_summary, previous_summary)
gen.export_report_to_file(report_content, filename)


═══════════════════════════════════════════════════════════════════════
🐛 常見問題解決
═══════════════════════════════════════════════════════════════════════

Q: 如何獲取 OpenAI API 金鑰？
A: 1. 訪問 https://platform.openai.com/api-keys
  2. 建立新金鑰
  3. 複製並保存到 .env 或 config.py

Q: 沒有 API 金鑰可以使用嗎？
A: 可以！運行 python demo.py 查看示範（無需金鑰）

Q: 如何修改難度等級？
A: 在 config.py 中修改 DIFFICULTY_LEVELS

Q: 如何添加新科目？
A: 在 config.py 的 SUBJECTS 列表中添加

Q: 數據保存在哪裡？
A: students/ 目錄中的 JSON 文件

Q: 如何導出學生數據？
A: 使用 ReportGenerator.export_report_to_file()

Q: 支持離線使用嗎？
A: 示範功能支持離線，完整功能需要 API


═══════════════════════════════════════════════════════════════════════
📖 文件導航
═══════════════════════════════════════════════════════════════════════
快速開始：
  → QUICKSTART.md          快速開始指南

詳細了解：
  → README.md              項目概述
  → ARCHITECTURE.md        系統設計
  → PROJECT_SUMMARY.md     完成總結

安裝運行：
  → INSTALL.md             安裝指南
  → demo.py                示範腳本
  → main.py                互動式應用
  → usage_examples.py      使用示例

源代碼：
  → models/                核心模組
  → utils/                 工具模組
  → config.py              配置文件


═══════════════════════════════════════════════════════════════════════
🚀 快速命令
═══════════════════════════════════════════════════════════════════════
# 安裝依賴
pip install -r requirements.txt

# 運行示範
python demo.py

# 運行使用示例
python usage_examples.py

# 運行互動式應用（需要API金鑰）
python main.py

# 查看設定
cat config.py

# 查看文檔
cat README.md
cat ARCHITECTURE.md


═══════════════════════════════════════════════════════════════════════
💡 最佳實踐
═══════════════════════════════════════════════════════════════════════
 
1. 始終為學生建立清晰的資料
2. 定期記錄學習數據
3. 定期生成進度報告
4. 根據報告調整學習計畫
5. 使用 demo.py 測試新功能
6. 在 .env 中存儲 API 金鑰
7. 定期備份 students/ 目錄
8. 查看日誌了解系統運行情況


═══════════════════════════════════════════════════════════════════════

需要幫助？查看文檔或運行示例腳本！

祝學習愉快！ 🎓

═══════════════════════════════════════════════════════════════════════
""")
