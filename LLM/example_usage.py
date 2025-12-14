"""
Example Usage - Demonstrates Knowledge Fuel Station capabilities
"""

from models import LLMClient, QuestionGenerator, ErrorAnalyzer
from utils import DataProcessor, ReportGenerator
from sample_data import SAMPLE_STUDENTS


def example_1_question_generation():
    """Example 1: Generate personalized questions"""
    print("\n" + "="*60)
    print("示範 1: 生成個性化問題")
    print("="*60 + "\n")
    
    llm = LLMClient()
    question_gen = QuestionGenerator(llm)
    
    student = SAMPLE_STUDENTS[0]
    print(f"為學生 {student['name']} 生成問題...\n")
    
    # Generate 3 questions
    questions = question_gen.generate_questions(
        student_profile=student,
        num_questions=3
    )
    
    for i, q in enumerate(questions, 1):
        print(f"問題 {i}:")
        print(f"  科目：{q['subject']}")
        print(f"  難度：{q['difficulty']}")
        print(f"  問題：{q['question']}")
        print(f"  標準答案：{q['standard_answer']}\n")


def example_2_error_analysis():
    """Example 2: Analyze student errors"""
    print("\n" + "="*60)
    print("示範 2: 錯誤分析")
    print("="*60 + "\n")
    
    llm = LLMClient()
    analyzer = ErrorAnalyzer(llm)
    
    # Example error
    error_case = {
        "question": "2 + 2 = ?",
        "student_answer": "5",
        "correct_answer": "4",
        "subject": "數學"
    }
    
    print("分析錯誤中...\n")
    analysis = analyzer.analyze_error(
        question=error_case["question"],
        student_answer=error_case["student_answer"],
        correct_answer=error_case["correct_answer"],
        subject=error_case["subject"]
    )
    
    print("錯誤分析結果：")
    print(f"\nQ: {error_case['question']}")
    print(f"A: {error_case['student_answer']}")
    print(f"Correct: {error_case['correct_answer']}")
    print(f"\n根本原因：{analysis['root_cause']}")
    print(f"\n解釋：\n{analysis['explanation']}")
    
    if analysis['hints']:
        print(f"\n改進提示：")
        for i, hint in enumerate(analysis['hints'], 1):
            print(f"  {i}. {hint}")


def example_3_learning_records():
    """Example 3: Track and analyze learning records"""
    print("\n" + "="*60)
    print("示範 3: 學習記錄追蹤")
    print("="*60 + "\n")
    
    processor = DataProcessor()
    student = SAMPLE_STUDENTS[0]
    
    # Save student profile
    processor.save_student_profile(student["student_id"], student)
    print(f"✅ 已保存學生資料：{student['name']}")
    
    # Simulate some learning records
    records = [
        {"question_id": 1, "correct": True, "subject": "數學", "time_spent": 120},
        {"question_id": 2, "correct": True, "subject": "數學", "time_spent": 150},
        {"question_id": 3, "correct": False, "subject": "英語", "time_spent": 180},
        {"question_id": 4, "correct": True, "subject": "英語", "time_spent": 90},
        {"question_id": 5, "correct": False, "subject": "數學", "time_spent": 200},
    ]
    
    print(f"\n正在保存 {len(records)} 條學習記錄...\n")
    for record in records:
        processor.update_student_progress(
            student_id=student["student_id"],
            question_id=record["question_id"],
            correct=record["correct"],
            subject=record["subject"],
            time_spent=record["time_spent"]
        )
    
    # Get progress summary
    summary = processor.get_progress_summary(
        student["student_id"],
        num_records=10
    )
    
    print("學習進度摘要：")
    print(f"  總題數：{summary['total_questions']}")
    print(f"  正確數：{summary['correct_answers']}")
    print(f"  正確率：{summary['accuracy']:.1f}%")
    
    if summary['weak_areas']:
        print(f"  薄弱領域：{', '.join(summary['weak_areas'])}")


def example_4_generate_report():
    """Example 4: Generate learning report"""
    print("\n" + "="*60)
    print("示範 4: 生成學習報告")
    print("="*60 + "\n")
    
    processor = DataProcessor()
    report_gen = ReportGenerator()
    
    student = SAMPLE_STUDENTS[0]
    
    # Get progress summary
    summary = processor.get_progress_summary(
        student["student_id"],
        num_records=20
    )
    
    # Generate report
    report = report_gen.generate_learning_report(
        student['name'],
        summary
    )
    
    print(report)
    
    # Generate recommendations
    recommendations = report_gen.generate_recommendations(summary)
    print(recommendations)
    
    # Generate chart
    chart = report_gen.generate_performance_chart(summary)
    print(chart)


def example_5_remedial_plan():
    """Example 5: Generate remedial plan from errors"""
    print("\n" + "="*60)
    print("示範 5: 制定補習計畫")
    print("="*60 + "\n")
    
    llm = LLMClient()
    analyzer = ErrorAnalyzer(llm)
    
    # Multiple error cases
    error_cases = [
        {
            "question": "求 15 × 7 的值",
            "student_answer": "105",
            "correct_answer": "105",
            "subject": "數學"
        },
        {
            "question": "用英文列舉5種顏色",
            "student_answer": "Red, Blue",
            "correct_answer": "Red, Blue, Green, Yellow, Purple",
            "subject": "英語"
        },
        {
            "question": "牛頓第一運動定律是什麼？",
            "student_answer": "物體必須受力才能運動",
            "correct_answer": "物體在沒有受力或受合力為零時，保持靜止或勻速直線運動",
            "subject": "物理"
        }
    ]
    
    print("分析多個錯誤...\n")
    result = analyzer.analyze_multiple_errors(error_cases)
    
    # Generate remedial plan
    plan = analyzer.generate_remedial_plan(
        student_name=SAMPLE_STUDENTS[0]["name"],
        error_analysis_result=result
    )
    
    print(f"補習計畫（為 {plan['student_name']}）：\n")
    print(plan['remedial_plan'])


def run_all_examples():
    """Run all examples"""
    
    print("\n" + "="*60)
    print("知識加油站 - 使用示例")
    print("Knowledge Fuel Station - Usage Examples")
    print("="*60)
    
    try:
        example_1_question_generation()
    except Exception as e:
        print(f"⚠️ 示範1出錯：{e}")
    
    try:
        example_2_error_analysis()
    except Exception as e:
        print(f"⚠️ 示範2出錯：{e}")
    
    try:
        example_3_learning_records()
    except Exception as e:
        print(f"⚠️ 示範3出錯：{e}")
    
    try:
        example_4_generate_report()
    except Exception as e:
        print(f"⚠️ 示範4出錯：{e}")
    
    try:
        example_5_remedial_plan()
    except Exception as e:
        print(f"⚠️ 示範5出錯：{e}")
    
    print("\n" + "="*60)
    print("所有示例完成！")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("""
    注意：這些示例需要配置 OpenAI API 金鑰
    
    1. 在 config.py 中設定你的 API 金鑰，或
    2. 設定環境變數 OPENAI_API_KEY
    
    要運行示例，請確保已安裝依賴：
    pip install -r requirements.txt
    """)
    
    # Uncomment to run examples
    # run_all_examples()
