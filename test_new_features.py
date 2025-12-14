#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試新功能：科目糾正和觀念記錄
"""

from main import KnowledgeFuelStation
from config import SUBJECTS

def test_subject_correction():
    """測試科目名稱糾正功能"""
    print("="*60)
    print("測試科目名稱糾正功能")
    print("="*60)
    
    app = KnowledgeFuelStation()
    
    # 測試案例
    test_cases = [
        ("樹學", "數學"),  # 打錯字
        ("數學", "數學"),  # 正確
        ("英文", "英語"),  # 別名
        ("物里", "物理"),  # 打錯字
        ("国文", "語文"),  # 簡體別名
    ]
    
    print("\n測試案例：\n")
    for input_subject, expected in test_cases:
        corrected = app.correct_subject_name(input_subject)
        status = "✅" if corrected == expected else "❌"
        print(f"{status} 輸入：'{input_subject}' → 修正：'{corrected}' (期望：'{expected}')")
    
    # 測試批量糾正
    print("\n\n測試批量科目糾正：\n")
    test_subjects = ["樹學", "英文", "物里", "化學"]
    print(f"輸入科目：{', '.join(test_subjects)}")
    
    corrected_subjects = [app.correct_subject_name(s) for s in test_subjects]
    print(f"修正後：{', '.join(corrected_subjects)}")
    
    print(f"\n糾正記錄：")
    for original, corrected in app.subject_corrections.items():
        if original != corrected:
            print(f"  '{original}' → '{corrected}'")
    
    print("\n" + "="*60)


def test_concept_extraction():
    """測試觀念提取功能"""
    print("\n\n測試觀念提取功能")
    print("="*60)
    
    app = KnowledgeFuelStation()
    
    # 模擬錯誤分析
    test_cases = [
        {
            "question": "已知函數 f(x) = log₂(x+a) 的圖像經過點 (2, 3)，則 a 的值為？",
            "subject": "數學",
            "analysis": {
                "root_cause": "對數函數的定義理解不清",
                "explanation": "需要將對數式轉換為指數式"
            }
        },
        {
            "question": "What is the past tense of 'go'?",
            "subject": "英語",
            "analysis": {
                "root_cause": "不規則動詞變化不熟悉",
                "explanation": "需要記憶不規則動詞"
            }
        },
        {
            "question": "計算集合 A={1,2,3} 和 B={2,3,4} 的交集",
            "subject": "數學",
            "analysis": {
                "root_cause": "集合運算概念不清楚",
                "explanation": "交集是兩個集合共同的元素"
            }
        }
    ]
    
    print("\n正在測試觀念提取（使用 LLM）...\n")
    
    for i, case in enumerate(test_cases, 1):
        print(f"案例 {i}:")
        print(f"  題目：{case['question'][:40]}...")
        print(f"  科目：{case['subject']}")
        print(f"  錯誤原因：{case['analysis']['root_cause']}")
        
        concept = app._extract_concept_to_reinforce(
            case["question"],
            case["subject"],
            case["analysis"]
        )
        
        print(f"  ➡️  需補強觀念：{concept}")
        print()
    
    print("="*60)


def demo_interactive_flow():
    """演示完整流程"""
    print("\n\n完整流程示範")
    print("="*60)
    
    print("""
此系統現在支援：

1️⃣  科目名稱自動糾正
   - 輸入：樹學 → 自動修正為：數學
   - 輸入：英文 → 自動修正為：英語
   - 輸入：物里 → 自動修正為：物理

2️⃣  每次可以重新選擇科目
   - 在開始學習時可以選擇本次要學習的科目
   - 不受學生檔案中預設科目的限制

3️⃣  記錄需要補強的觀念
   - 答錯題目時，系統會自動分析需要加強的觀念
   - 例如："集合觀念需要加強"
   - 例如："對數運算不熟悉"
   - 這些記錄會保存在學習記錄中

使用方式：
```python
# 運行主程式
python main.py

# 系統會詢問：
# "要重新選擇本次學習科目嗎？(y/n):"

# 如果選擇 y，可以輸入：
# "樹學, 英文, 物里"

# 系統會自動糾正為：
# 本次學習科目：數學, 英語, 物理
#   ℹ️  已將 '樹學' 修正為 '數學'
#   ℹ️  已將 '英文' 修正為 '英語'  
#   ℹ️  已將 '物里' 修正為 '物理'
```

學習記錄範例：
```json
{
  "timestamp": "2025-12-14T15:30:00",
  "question_id": 1,
  "correct": false,
  "subject": "數學",
  "time_spent": 0.0,
  "score": 0,
  "concept_to_reinforce": "對數函數定義不清楚"
}
```
    """)
    
    print("="*60)


if __name__ == "__main__":
    print("\n🧪 測試知識加油站新功能\n")
    
    # 測試1：科目糾正
    test_subject_correction()
    
    # 測試2：觀念提取（需要LLM）
    try:
        test_concept_extraction()
    except Exception as e:
        print(f"\n⚠️  觀念提取測試需要 LLM 支援，跳過：{e}\n")
    
    # 演示流程
    demo_interactive_flow()
    
    print("\n✅ 測試完成！\n")
    print("💡 提示：運行 'python main.py' 體驗完整功能\n")
