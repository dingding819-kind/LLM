#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
互動式學生學習體驗腳本
用戶可以像學生一樣逐步體驗知識加油站系統

運行方式: python interactive_student_experience.py
"""

import json
import os
import sys
from datetime import datetime
from utils.data_processor import DataProcessor
from utils.report_generator import ReportGenerator

def print_header(title):
    """打印標題"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def print_instruction(step, instruction):
    """打印指令"""
    print(f"📍 步驟 {step}: {instruction}")
    print("-" * 60)

def get_input_with_hint(prompt, hint=""):
    """獲取用戶輸入"""
    if hint:
        print(f"💡 提示: {hint}")
    user_input = input(f"👉 {prompt}: ").strip()
    return user_input

def confirm_choice(prompt):
    """確認選擇"""
    while True:
        choice = input(f"\n❓ {prompt} (是/否): ").strip().lower()
        if choice in ['是', 'y', 'yes']:
            return True
        elif choice in ['否', 'n', 'no']:
            return False
        else:
            print("❌ 請輸入 '是' 或 '否'")

def run_student_experience():
    """運行互動式學生體驗"""
    
    print_header("🎓 知識加油站 - 學生體驗模式")
    
    print("歡迎來到知識加油站！")
    print("這是一個個性化學習系統，會根據你的學習情況生成客製化的問題和建議。")
    print("現在讓我們開始吧！請按照以下步驟一步步操作。\n")
    
    input("按 Enter 開始第一步...")
    
    # ===== 第一步：輸入學生資訊 =====
    print_instruction(1, "建立你的學生檔案")
    
    student_name = get_input_with_hint(
        "你的名字是什麼",
        "例如: 張三、李四"
    )
    
    student_id = f"STU_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    print(f"✅ 你的學號: {student_id}")
    
    grade = get_input_with_hint(
        "你現在是幾年級",
        "例如: 初一、初二、高一"
    )
    
    print(f"\n✅ 檔案已建立!")
    print(f"   姓名: {student_name}")
    print(f"   學號: {student_id}")
    print(f"   年級: {grade}")
    
    input("\n按 Enter 繼續下一步...")
    
    # ===== 第二步：選擇學習科目 =====
    print_instruction(2, "選擇你要學習的科目")
    
    print("可選科目:")
    subjects = ["數學", "英語", "物理", "化學", "語文"]
    for i, subject in enumerate(subjects, 1):
        print(f"  {i}. {subject}")
    
    selected_subjects = []
    while True:
        choice = get_input_with_hint(
            "輸入科目編號(可以輸入多個，用逗號分隔，例如: 1,2,3)",
            "至少選擇1個科目"
        )
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            selected_subjects = [subjects[i] for i in indices if 0 <= i < len(subjects)]
            if selected_subjects:
                break
            else:
                print("❌ 無效的選擇，請重試")
        except:
            print("❌ 輸入格式不正確，請重試")
    
    print(f"\n✅ 選定科目: {', '.join(selected_subjects)}")
    
    input("\n按 Enter 繼續下一步...")
    
    # ===== 第三步：開始作答 =====
    print_instruction(3, "開始作答 - 回答問題")
    
    print("現在我會向你提出4道題目，請認真回答。")
    print("這些題目會根據你的答案難度自動調整。\n")
    
    input("按 Enter 開始作答...")
    
    questions_data = [
        {
            "subject": "數學",
            "content": "如果 2x + 3 = 11，求 x 的值是多少？",
            "difficulty": "簡單",
            "correct_answer": "4"
        },
        {
            "subject": "英語",
            "content": "What is the past tense of 'go'?",
            "difficulty": "簡單",
            "correct_answer": "went"
        },
        {
            "subject": "數學",
            "content": "計算: (a + b)² 的展開式是？",
            "difficulty": "中等",
            "correct_answer": "a² + 2ab + b²"
        },
        {
            "subject": "英語",
            "content": "Choose the correct form: She ___ (have/has) finished her homework.",
            "difficulty": "中等",
            "correct_answer": "has"
        }
    ]
    
    answers = []
    correct_count = 0
    
    for i, question in enumerate(questions_data, 1):
        print(f"\n📝 第 {i} 題 (科目: {question['subject']}, 難度: {question['difficulty']})")
        print(f"問題: {question['content']}")
        
        user_answer = get_input_with_hint(
            "你的答案是",
            f"請輸入你的答案"
        )
        
        is_correct = user_answer.lower().strip() == question['correct_answer'].lower().strip()
        answers.append({
            "number": i,
            "subject": question['subject'],
            "question": question['content'],
            "user_answer": user_answer,
            "correct_answer": question['correct_answer'],
            "is_correct": is_correct
        })
        
        if is_correct:
            print("✅ 正確！")
            correct_count += 1
        else:
            print(f"❌ 答案不對")
            print(f"   正確答案: {question['correct_answer']}")
        
        if i < len(questions_data):
            input("\n按 Enter 繼續下一題...")
    
    accuracy = (correct_count / len(questions_data)) * 100
    print(f"\n📊 作答完成!")
    print(f"   總題數: {len(questions_data)}")
    print(f"   正確: {correct_count}")
    print(f"   錯誤: {len(questions_data) - correct_count}")
    print(f"   準確率: {accuracy:.1f}%")
    
    input("\n按 Enter 繼續下一步...")
    
    # ===== 第四步：查看答題分析 =====
    print_instruction(4, "查看你的答題分析")
    
    print("錯題分析:")
    print("-" * 60)
    
    wrong_questions = [a for a in answers if not a['is_correct']]
    if wrong_questions:
        for q in wrong_questions:
            print(f"\n❌ 第 {q['number']} 題 ({q['subject']})")
            print(f"   你的答案: {q['user_answer']}")
            print(f"   正確答案: {q['correct_answer']}")
    else:
        print("🎉 太棒了！全部答對！")
    
    input("\n按 Enter 繼續下一步...")
    
    # ===== 第五步：生成學習報告 =====
    print_instruction(5, "生成你的學習報告")
    
    # 使用 DataProcessor 保存數據
    data_processor = DataProcessor()
    student_profile = {
        "student_id": student_id,
        "name": student_name,
        "grade": grade,
        "subjects": selected_subjects,
        "created_at": datetime.now().isoformat()
    }
    
    data_processor.save_student_profile(student_id, student_profile)
    
    # 紀錄學習活動
    for idx, answer in enumerate(answers, 1):
        data_processor.update_student_progress(
            student_id=student_id,
            question_id=idx,
            correct=answer['is_correct'],
            subject=answer['subject'],
            time_spent=15.0
        )
    
    # 生成報告
    report_generator = ReportGenerator()
    progress_summary = data_processor.get_progress_summary(student_id)
    
    report = ReportGenerator.generate_learning_report(
        student_name=student_name,
        progress_summary=progress_summary
    )
    
    # 保存報告到文件
    report_filename = f"學生報告_{student_id}.txt"
    ReportGenerator.export_report_to_file(report, report_filename)
    
    print(f"✅ 報告已生成！")
    print(f"   文件名: {report_filename}\n")
    
    # 顯示報告的關鍵部分
    print("📋 學習報告摘要:")
    print("=" * 60)
    print(report)
    print("=" * 60)
    
    input("\n按 Enter 繼續...")
    
    # ===== 第六步：個性化建議 =====
    print_instruction(6, "獲取個性化學習建議")
    
    print("基於你的學習表現，以下是針對你的建議:\n")
    
    weak_subjects = data_processor.calculate_weak_subjects(student_id)
    strong_subjects = [s for s in selected_subjects if s not in weak_subjects]
    
    print("📍 強項科目:")
    if strong_subjects:
        for subject in strong_subjects:
            print(f"   ✅ {subject} - 保持現有學習節奏")
    else:
        print("   (待提升)")
    
    print("\n📍 需要加強的科目:")
    if weak_subjects:
        for subject in weak_subjects:
            print(f"   ⚠️  {subject} - 建議增加練習時間")
    else:
        print("   (全部掌握)")
    
    print("\n📍 學習建議:")
    suggestions = [
        "1. 每天花30分鐘複習薄弱科目",
        "2. 完成課後練習題",
        "3. 與同學討論不懂的問題",
        "4. 定期參加測試檢查進度"
    ]
    for suggestion in suggestions:
        print(f"   {suggestion}")
    
    print("\n📍 下一步行動:")
    print("   - 明天繼續作答")
    print("   - 重點關注薄弱科目")
    print("   - 下周查看學習進度報告")
    
    input("\n按 Enter 完成體驗...")
    
    # ===== 完成 =====
    print_header("🎉 體驗完成")
    
    print(f"親愛的 {student_name}，")
    print("\n你已經完成了知識加油站的完整學習體驗流程！")
    print("\n這次體驗包括:")
    print("  ✓ 建立學生檔案")
    print("  ✓ 選擇學習科目")
    print("  ✓ 回答4道測試題目")
    print("  ✓ 獲得答題分析")
    print("  ✓ 生成個人學習報告")
    print("  ✓ 獲得個性化建議")
    
    print(f"\n📁 你的學習數據已保存在: students/{student_id}/")
    print(f"📄 你的學習報告已生成在: 學生報告_{student_id}.txt")
    
    print("\n💡 下一次學習建議:")
    print("  1. 重點複習錯題")
    print("  2. 明天再來做新的題目")
    print("  3. 一週後查看學習進度")
    
    print("\n祝你學習進步！🚀\n")

if __name__ == "__main__":
    try:
        run_student_experience()
    except KeyboardInterrupt:
        print("\n\n⏹️  體驗已中斷")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 發生錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
