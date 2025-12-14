"""
使用示例 - 實際應用場景
Practical Usage Examples - Real-world Applications
"""

from utils import DataProcessor, ReportGenerator
from sample_data import SAMPLE_STUDENTS

print("\n" + "="*70)
print("知識加油站 - 實際使用示例")
print("="*70 + "\n")

# ============================================================
# 示例1: 為學生建立資料並追蹤學習
# ============================================================
print("【示例1】建立學生資料並追蹤學習進度\n")

processor = DataProcessor()

# 為學生建立資料
student_info = {
    "student_id": "S_USER_001",
    "name": "張三",
    "grade": "初二",
    "weak_subjects": ["數學", "英語"],
    "learning_style": "visual",
    "recent_scores": {},
    "recent_topics": []
}

processor.save_student_profile(student_info["student_id"], student_info)
print(f"✅ 已為 {student_info['name']} 建立學生資料")
print(f"   學生ID: {student_info['student_id']}")
print(f"   年級: {student_info['grade']}")
print(f"   薄弱科目: {', '.join(student_info['weak_subjects'])}\n")

# ============================================================
# 示例2: 保存學習記錄
# ============================================================
print("【示例2】記錄學生的學習會話\n")

# 模擬一次學習會話
session_results = [
    ("Q1: 2×5=?", "10", True, "數學", 45),
    ("Q2: 3×7=?", "20", False, "數學", 60),
    ("Q3: What is...?", "correct", True, "英語", 75),
    ("Q4: He goes...", "went", False, "英語", 90),
]

print("學習會話記錄：\n")
for i, (question, answer, correct, subject, time) in enumerate(session_results, 1):
    processor.update_student_progress(
        student_id=student_info["student_id"],
        question_id=i,
        correct=correct,
        subject=subject,
        time_spent=time
    )
    status = "✅" if correct else "❌"
    print(f"  {status} {subject}: {question}")
    print(f"     學生答案: {answer}, 耗時: {time}秒")

# ============================================================
# 示例3: 生成學習進度報告
# ============================================================
print("\n【示例3】生成學習進度報告\n")

# 獲取學生的學習摘要
progress = processor.get_progress_summary(student_info["student_id"])

print(f"📊 學生 {student_info['name']} 的學習摘要：\n")
print(f"  總練習題數: {progress['total_questions']}")
print(f"  正確答案數: {progress['correct_answers']}")
print(f"  總體正確率: {progress['accuracy']:.1f}%\n")

print("科目分析：")
for subject, data in progress['subjects'].items():
    print(f"  • {subject}: {data['correct']}/{data['total']} " +
          f"(正確率: {data['accuracy']:.1f}%)")

if progress['weak_areas']:
    print(f"\n需要改進的科目（按優先級）：")
    for i, subject in enumerate(progress['weak_areas'], 1):
        print(f"  {i}. {subject}")

# ============================================================
# 示例4: 生成詳細報告
# ============================================================
print("\n【示例4】生成詳細的學習報告\n")

report_gen = ReportGenerator()

# 生成完整報告
report = report_gen.generate_learning_report(student_info['name'], progress)
print(report)

# 生成性能對比圖
chart = report_gen.generate_performance_chart(progress)
print("\n" + chart)

# 生成學習建議
recommendations = report_gen.generate_recommendations(progress)
print(recommendations)

# ============================================================
# 示例5: 載入已保存的學生數據
# ============================================================
print("【示例5】載入已保存的學生數據\n")

# 從已保存的樣本數據載入
for sample_student in SAMPLE_STUDENTS:
    loaded_profile = processor.load_student_profile(sample_student["student_id"])
    if loaded_profile:
        print(f"✅ 已載入學生資料: {loaded_profile['name']}")
        print(f"   年級: {loaded_profile['grade']}")
        print(f"   學習風格: {loaded_profile['learning_style']}")
        print()

# ============================================================
# 示例6: 比較多個學生的表現
# ============================================================
print("【示例6】比較多個學生的表現\n")

print("學生表現對比：\n")
print(f"{'學生':<10} {'科目':<15} {'正確率':<10}")
print("-" * 35)

for sample_student in SAMPLE_STUDENTS:
    student_id = sample_student["student_id"]
    student_progress = processor.get_progress_summary(student_id)
    
    if student_progress['subjects']:
        for subject, data in student_progress['subjects'].items():
            print(f"{sample_student['name']:<10} {subject:<15} {data['accuracy']:.1f}%")

# ============================================================
# 示例7: 導出報告到文件
# ============================================================
print("\n【示例7】導出報告到文件\n")

# 生成完整报告内容
full_report = report + "\n" + chart + "\n" + recommendations

# 導出到文件
filename = f"學生報告_{student_info['student_id']}.txt"
if ReportGenerator.export_report_to_file(full_report, filename):
    print(f"✅ 報告已成功導出到: {filename}\n")

# ============================================================
# 示例8: 使用Python代碼進行自訂分析
# ============================================================
print("【示例8】自訂數據分析\n")

# 獲取學生的所有學習記錄
all_records = processor.get_learning_records(student_info["student_id"])

print(f"學生 {student_info['name']} 的完整學習記錄：\n")
print(f"{'題目':<5} {'科目':<10} {'正確':<6} {'耗時(秒)':<10}")
print("-" * 40)

for record in all_records:
    question_id = record.get("question_id", "?")
    subject = record.get("subject", "未知")
    correct = "✅" if record.get("correct", False) else "❌"
    time_spent = record.get("time_spent", 0)
    print(f"{question_id:<5} {subject:<10} {correct:<6} {time_spent:<10}")

# 計算平均耗時
if all_records:
    avg_time = sum(r.get("time_spent", 0) for r in all_records) / len(all_records)
    print(f"\n平均每題耗時: {avg_time:.1f}秒")

# 按科目統計
print("\n按科目統計：")
subject_stats = {}
for record in all_records:
    subject = record.get("subject", "未知")
    if subject not in subject_stats:
        subject_stats[subject] = {"total": 0, "correct": 0, "time": 0}
    subject_stats[subject]["total"] += 1
    if record.get("correct", False):
        subject_stats[subject]["correct"] += 1
    subject_stats[subject]["time"] += record.get("time_spent", 0)

for subject, stats in subject_stats.items():
    avg_time_subject = stats["time"] / stats["total"] if stats["total"] > 0 else 0
    accuracy = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
    print(f"  • {subject}: {stats['correct']}/{stats['total']} " +
          f"(準確率 {accuracy:.1f}%, 平均耗時 {avg_time_subject:.1f}秒)")

# ============================================================
# 总结
# ============================================================
print("\n" + "="*70)
print("✅ 使用示例完成！")
print("="*70)

print("""
📚 這些示例展示了如何：
    1. 建立與管理學生資料
    2. 記錄學習會話數據
    3. 生成學習進度報告
    4. 建立數據視覺化
    5. 生成個性化建議
    6. 導出報告到文件
    7. 載入並分析已保存數據
    8. 執行自訂數據分析

💡 更多功能請查看：
    • main.py - 互動式學習應用
    • example_usage.py - 更多進階示例
    • ARCHITECTURE.md - 系統架構文檔
""")

print("="*70 + "\n")
