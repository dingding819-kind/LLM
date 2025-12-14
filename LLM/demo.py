"""
Demo Script - Demonstrates Knowledge Fuel Station without API calls
This script shows the system structure and workflow without requiring OpenAI API
"""

from models import QuestionGenerator, ErrorAnalyzer
from utils import DataProcessor, ReportGenerator
from sample_data import SAMPLE_STUDENTS, SAMPLE_QUESTIONS, SAMPLE_LEARNING_RECORDS
import json


class MockLLMClient:
    """Mock LLM client for demonstration without API calls"""
    
    def generate_text(self, prompt, system_message=None, **kwargs):
        """Return mock response"""
        if "问题" in prompt or "题目" in prompt:
            return "這是一個示例問題：請計算 3 × 4 的結果。"
        elif "错误" in prompt or "分析" in prompt:
            return "學生可能在計算基本乘法時出現錯誤。"
        elif "提示" in prompt:
            return "1. 回顧乘法表\n2. 逐步計算\n3. 檢查答案"
        else:
            return "這是一個示例回應。"
    
    def chat(self, messages, **kwargs):
        """Return mock chat response"""
        return "這是一個多輪對話的示例回應。"


def demo_data_management():
    """Demo 1: Student Data Management"""
    print("\n" + "="*60)
    print("示範 1: 學生資料管理")
    print("="*60 + "\n")
    
    processor = DataProcessor()
    
    # Save sample students
    for student in SAMPLE_STUDENTS:
        processor.save_student_profile(student["student_id"], student)
        print(f"✅ 已保存學生資料: {student['name']} ({student['student_id']})")
    
    # Load and display student info
    print("\n載入學生資訊：\n")
    for student in SAMPLE_STUDENTS:
        profile = processor.load_student_profile(student["student_id"])
        if profile:
            print(f"👤 {profile['name']}")
            print(f"   年級: {profile['grade']}")
            print(f"   薄弱科目: {', '.join(profile['weak_subjects'])}")
            print()


def demo_learning_records():
    """Demo 2: Learning Records and Progress Tracking"""
    print("\n" + "="*60)
    print("示範 2: 學習記錄與進度追蹤")
    print("="*60 + "\n")
    
    processor = DataProcessor()
    student_id = SAMPLE_STUDENTS[0]["student_id"]
    
    # Save sample learning records
    print(f"為學生 {SAMPLE_STUDENTS[0]['name']} 保存學習記錄...\n")
    
    learning_records = [
        {"question_id": 1, "subject": "數學", "correct": True},
        {"question_id": 2, "subject": "數學", "correct": False},
        {"question_id": 3, "subject": "英語", "correct": True},
        {"question_id": 4, "subject": "英語", "correct": False},
        {"question_id": 5, "subject": "英語", "correct": True},
        {"question_id": 6, "subject": "物理", "correct": False},
        {"question_id": 7, "subject": "數學", "correct": True},
    ]
    
    for record in learning_records:
        processor.update_student_progress(
            student_id=student_id,
            question_id=record["question_id"],
            correct=record["correct"],
            subject=record["subject"],
            time_spent=120
        )
    
    print(f"✅ 已保存 {len(learning_records)} 條學習記錄\n")
    
    # Get progress summary
    summary = processor.get_progress_summary(student_id, num_records=20)
    
    print("📊 學習進度摘要：\n")
    print(f"  總練習題數: {summary['total_questions']}")
    print(f"  正確答案數: {summary['correct_answers']}")
    print(f"  總體正確率: {summary['accuracy']:.1f}%")
    
    print("\n📈 科目分析：")
    for subject, data in summary['subjects'].items():
        print(f"  {subject}: {data['correct']}/{data['total']} " +
              f"(正確率: {data['accuracy']:.1f}%)")
    
    if summary['weak_areas']:
        print(f"\n⚠️ 薄弱科目（按優先級）：")
        for i, subject in enumerate(summary['weak_areas'], 1):
            print(f"  {i}. {subject}")


def demo_report_generation():
    """Demo 3: Report Generation"""
    print("\n" + "="*60)
    print("示範 3: 學習報告生成")
    print("="*60 + "\n")
    
    processor = DataProcessor()
    report_gen = ReportGenerator()
    
    student_id = SAMPLE_STUDENTS[0]["student_id"]
    student_name = SAMPLE_STUDENTS[0]["name"]
    
    # Get progress summary
    summary = processor.get_progress_summary(student_id, num_records=20)
    
    # Generate report
    report = report_gen.generate_learning_report(student_name, summary)
    print(report)
    
    # Generate chart
    print("\n📊 性能對比圖：\n")
    chart = report_gen.generate_performance_chart(summary)
    print(chart)
    
    # Generate recommendations
    print("\n💡 學習建議：\n")
    recommendations = report_gen.generate_recommendations(summary)
    print(recommendations)
    
    # Save report to file
    filename = f"demo_report_{student_id}.txt"
    full_report = report + "\n" + chart + "\n" + recommendations
    if ReportGenerator.export_report_to_file(full_report, filename):
        print(f"\n✅ 報告已保存到: {filename}")


def demo_question_structure():
    """Demo 4: Question Structure and Types"""
    print("\n" + "="*60)
    print("示範 4: 問題結構示範")
    print("="*60 + "\n")
    
    print("📝 範例問題結構：\n")
    
    for question in SAMPLE_QUESTIONS:
        print(f"題目 ID: {question['id']}")
        print(f"科目: {question['subject']}")
        print(f"難度: {question['difficulty']}")
        print(f"問題: {question['question']}")
        print(f"標準答案: {question['standard_answer']}")
        print()


def demo_error_analysis_structure():
    """Demo 5: Error Analysis Structure"""
    print("\n" + "="*60)
    print("示範 5: 錯誤分析結構示範")
    print("="*60 + "\n")
    
    # Simulated error analysis result
    mock_analysis = {
        "question": "2 + 2 = ?",
        "student_answer": "5",
        "correct_answer": "4",
        "root_cause": "學生在計算兩個數字之和時出現算術錯誤",
        "explanation": "2加2等於4，而不是5。正確的計算方法是將兩個2相加: 2+2=4",
        "hints": [
            "數一下你手指上的2個加2個",
            "使用數軸從2開始向後數2步",
            "檢查你的計算，2加2應該等於多少？"
        ],
        "similar_problems": [
            "計算 3 + 3 = ?",
            "計算 1 + 1 = ?"
        ]
    }
    
    print("❌ 學生錯誤分析：\n")
    print(f"題目: {mock_analysis['question']}")
    print(f"學生答案: {mock_analysis['student_answer']}")
    print(f"正確答案: {mock_analysis['correct_answer']}")
    print(f"\n根本原因: {mock_analysis['root_cause']}")
    print(f"\n詳細解釋:\n{mock_analysis['explanation']}")
    
    print(f"\n💡 改進提示:")
    for i, hint in enumerate(mock_analysis['hints'], 1):
        print(f"  {i}. {hint}")
    
    print(f"\n📚 相似練習題:")
    for i, problem in enumerate(mock_analysis['similar_problems'], 1):
        print(f"  {i}. {problem}")


def demo_learning_workflow():
    """Demo 6: Complete Learning Workflow"""
    print("\n" + "="*60)
    print("示範 6: 完整學習工作流程")
    print("="*60 + "\n")
    
    processor = DataProcessor()
    report_gen = ReportGenerator()
    
    # 1. Create student profile
    print("1️⃣ 建立學生資料")
    student = {
        "student_id": "S_DEMO_001",
        "name": "示範學生",
        "grade": "初二",
        "weak_subjects": ["數學", "英語"],
        "learning_style": "visual",
        "recent_scores": {}
    }
    processor.save_student_profile(student["student_id"], student)
    print(f"✅ 已建立: {student['name']}\n")
    
    # 2. Simulate learning session
    print("2️⃣ 模擬學習會話")
    session_data = [
        {"question": "2×3=?", "answer": "6", "correct": True, "subject": "數學"},
        {"question": "3×4=?", "answer": "10", "correct": False, "subject": "數學"},
        {"question": "He __ to school", "answer": "goes", "correct": True, "subject": "英語"},
        {"question": "What is ...?", "answer": "不確定", "correct": False, "subject": "英語"},
        {"question": "牛頓定律是什麼?", "answer": "不知道", "correct": False, "subject": "物理"},
    ]
    
    for i, item in enumerate(session_data, 1):
        processor.update_student_progress(
            student_id=student["student_id"],
            question_id=i,
            correct=item["correct"],
            subject=item["subject"]
        )
        status = "✅" if item["correct"] else "❌"
        print(f"  {status} {item['subject']}: {item['question']}")
    
    print()
    
    # 3. Generate report
    print("3️⃣ 生成學習報告")
    summary = processor.get_progress_summary(student["student_id"])
    report = report_gen.generate_learning_report(student["name"], summary)
    print(report)
    
    # 4. Recommendations
    print("4️⃣ 生成學習建議")
    recommendations = report_gen.generate_recommendations(summary)
    print(recommendations)


def run_all_demos():
    """Run all demonstrations"""
    
    print("\n" + "="*60)
    print("知識加油站 - 功能示範")
    print("Knowledge Fuel Station - Feature Demo")
    print("="*60)
    print("\n本示範無需 API 金鑰，展示系統的主要功能與工作流程。\n")
    
    try:
        demo_data_management()
    except Exception as e:
        print(f"⚠️ 示範1出錯: {e}\n")
    
    try:
        demo_learning_records()
    except Exception as e:
        print(f"⚠️ 示範2出錯: {e}\n")
    
    try:
        demo_report_generation()
    except Exception as e:
        print(f"⚠️ 示範3出錯: {e}\n")
    
    try:
        demo_question_structure()
    except Exception as e:
        print(f"⚠️ 示範4出錯: {e}\n")
    
    try:
        demo_error_analysis_structure()
    except Exception as e:
        print(f"⚠️ 示範5出錯: {e}\n")
    
    try:
        demo_learning_workflow()
    except Exception as e:
        print(f"⚠️ 示範6出錯: {e}\n")
    
    print("\n" + "="*60)
    print("✅ 所有示範完成！")
    print("="*60)
    print("\n📚 下一步:")
    print("1. 設定 OpenAI API 金鑰（在 config.py 或 .env 中）")
    print("2. 執行: python main.py （互動式學習會話）")
    print("3. 查看: example_usage.py（更多功能示例）")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_demos()
