#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
答案驗證測試腳本
用於測試修復後的答案比對邏輯
"""

from main import KnowledgeFuelStation

def test_answer_checking():
    """測試各種答案輸入情況"""
    
    print("=" * 60)
    print("答案驗證測試")
    print("=" * 60)
    
    # 創建系統實例
    system = KnowledgeFuelStation()
    
    # 測試用的題目
    test_question = {
        "question": "已知函數 f(x) = log₂(x+a) 的圖像經過點 (2, 3)，則 a 的值為？",
        "options": {
            "A": "-2",
            "B": "6",
            "C": "2",
            "D": "-6"
        },
        "standard_answer": "B"
    }
    
    test_cases = [
        # (學生輸入, 期望結果, 描述)
        ("B", True, "輸入正確字母 B"),
        ("b", True, "輸入小寫 b（大小寫不敏感）"),
        ("6", True, "輸入答案內容 6"),
        ("A", False, "輸入錯誤字母 A"),
        ("D", False, "輸入錯誤字母 D"),
        ("-6", False, "輸入錯誤內容 -6"),
        ("2", False, "輸入錯誤內容 2"),
    ]
    
    print("\n測試題目：")
    print(f"  {test_question['question']}")
    print(f"\n選項：")
    for letter, content in test_question["options"].items():
        marker = " ← 正確答案" if letter == test_question["standard_answer"] else ""
        print(f"  {letter}. {content}{marker}")
    
    print(f"\n標準答案：{test_question['standard_answer']}")
    print("\n" + "=" * 60)
    
    passed = 0
    failed = 0
    
    for student_input, expected, description in test_cases:
        result = system._check_answer_correctness(
            student_input,
            test_question["standard_answer"],
            test_question
        )
        
        status = "✅ PASS" if result == expected else "❌ FAIL"
        emoji = "✅" if result else "❌"
        
        print(f"\n測試：{description}")
        print(f"  輸入：{student_input}")
        print(f"  判定：{emoji} {'正確' if result else '錯誤'}")
        print(f"  期望：{'✅ 正確' if expected else '❌ 錯誤'}")
        print(f"  結果：{status}")
        
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"測試總結：")
    print(f"  通過：{passed}/{len(test_cases)}")
    print(f"  失敗：{failed}/{len(test_cases)}")
    print(f"  成功率：{(passed/len(test_cases)*100):.1f}%")
    print("=" * 60)
    
    if failed == 0:
        print("\n🎉 所有測試通過！答案驗證邏輯運作正常。")
    else:
        print(f"\n⚠️  有 {failed} 個測試失敗，請檢查邏輯。")
    
    return failed == 0


def test_answer_parsing():
    """測試答案解析邏輯"""
    
    print("\n\n" + "=" * 60)
    print("答案解析測試")
    print("=" * 60)
    
    from models.question_generator import QuestionGenerator
    from models.llm_client import LLMClient
    
    llm_client = LLMClient()
    generator = QuestionGenerator(llm_client)
    
    # 測試各種 LLM 回應格式
    test_responses = [
        # (LLM回應, 期望的答案字母, 描述)
        ("""題目：測試題目
A. 選項A
B. 選項B
C. 選項C
D. 選項D
答案：B
解釋：這是解釋""", "B", "標準格式"),
        
        ("""題目：測試題目
A. 選項A
B. 選項B
C. 選項C
D. 選項D
答案：B (這是正確答案)
解釋：這是解釋""", "B", "答案後有括號說明"),
        
        ("""題目：測試題目
A. 選項A
B. 選項B
C. 選項C
D. 選項D
答案：選項B是正確的
解釋：這是解釋""", "B", "答案包含額外文字"),
        
        ("""題目：測試題目
A. 選項A
B. 選項B
C. 選項C
D. 選項D
答案：d
解釋：這是解釋""", "D", "小寫答案"),
    ]
    
    passed = 0
    failed = 0
    
    for response, expected_answer, description in test_responses:
        parsed = generator._parse_multiple_choice(response)
        result = parsed.get("answer", "")
        
        status = "✅ PASS" if result == expected_answer else "❌ FAIL"
        
        print(f"\n測試：{description}")
        print(f"  期望答案：{expected_answer}")
        print(f"  解析結果：{result}")
        print(f"  狀態：{status}")
        
        if result == expected_answer:
            passed += 1
        else:
            failed += 1
            print(f"  ⚠️  解析失敗！")
    
    print("\n" + "=" * 60)
    print(f"解析測試總結：")
    print(f"  通過：{passed}/{len(test_responses)}")
    print(f"  失敗：{failed}/{len(test_responses)}")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    print("\n🧪 開始測試答案驗證系統...\n")
    
    test1_passed = test_answer_checking()
    test2_passed = test_answer_parsing()
    
    print("\n\n" + "=" * 60)
    print("總體測試結果")
    print("=" * 60)
    
    if test1_passed and test2_passed:
        print("✅ 所有測試通過！系統運作正常。")
        exit(0)
    else:
        if not test1_passed:
            print("❌ 答案驗證測試失敗")
        if not test2_passed:
            print("❌ 答案解析測試失敗")
        print("\n請檢查並修復相關邏輯。")
        exit(1)
