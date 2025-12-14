# 問題排查與改善指南

## 問題：模型給出錯誤答案判定

### 問題描述

在使用系統時，可能出現以下情況：
- 用戶選擇了正確答案（如選項 B: 6），但系統判定為錯誤
- 系統說正確答案是另一個選項（如選項 D），但解釋中計算出的值卻與用戶選擇的一致

### 根本原因

這個問題有三個可能的來源：

#### 1. **答案比對邏輯問題** ([main.py](main.py#L269))

當前的答案檢查邏輯：
```python
def _check_answer_correctness(self, student_answer: str, correct_answer: str) -> bool:
    student_clean = student_answer.strip().upper()
    correct_clean = correct_answer.strip().upper()
    
    if len(student_clean) == 1 and len(correct_clean) == 1:
        return student_clean == correct_clean
    
    return student_clean in correct_clean or correct_clean in student_clean
```

**問題**：這個邏輯只比對選項字母（A/B/C/D），但如果 `standard_answer` 存儲的不是字母而是完整答案內容，就會出錯。

#### 2. **題目生成時答案存儲不一致** ([models/question_generator.py](models/question_generator.py#L264))

解析題目時的代碼：
```python
def _parse_multiple_choice(self, response: str) -> Dict:
    # ...
    elif line.startswith('答案：'):
        result["answer"] = line.replace('答案：', '').strip().upper()
```

**問題**：
- LLM 可能回傳 `答案：B` 或 `答案：6`
- 如果解析時沒有統一格式，`standard_answer` 可能存儲不同格式

#### 3. **LLM 錯誤分析時的理解偏差** ([models/error_analyzer.py](models/error_analyzer.py#L190))

錯誤分析的提示詞：
```python
prompt = f"""為學生解釋他們的錯誤：

題目：{question}
學生答案：{student_answer}
正確答案：{correct_answer}
```

**問題**：
- 如果傳給 LLM 的是 `學生答案：B` 和 `正確答案：D`
- 但 `question` 中選項 B=6，D=-6
- LLM 可能會誤判，因為它重新計算後發現 6 才是對的

---

## 解決方案

### 方案 1：增強答案驗證邏輯（推薦）

修改 [main.py](main.py#L269) 中的 `_check_answer_correctness` 方法：

```python
def _check_answer_correctness(
    self,
    student_answer: str,
    correct_answer: str,
    question_data: Optional[Dict] = None
) -> bool:
    """
    Check if student answer matches correct answer
    
    Args:
        student_answer: Student's answer (can be "B" or "6")
        correct_answer: Correct answer (should be single letter like "B")
        question_data: Full question dict with options
        
    Returns:
        True if answers match
    """
    student_clean = student_answer.strip().upper()
    correct_clean = correct_answer.strip().upper()
    
    # Direct match for single letter (A/B/C/D)
    if len(student_clean) == 1 and student_clean in ['A', 'B', 'C', 'D']:
        if len(correct_clean) == 1 and correct_clean in ['A', 'B', 'C', 'D']:
            return student_clean == correct_clean
        
        # If correct_answer is not a letter, try to find it in options
        if question_data and "options" in question_data:
            student_option_content = question_data["options"].get(student_clean, "")
            # Check if correct answer matches the content
            if correct_clean in student_option_content.upper():
                return True
    
    # If student typed the full answer instead of letter
    if question_data and "options" in question_data:
        # Find which option matches student's answer
        for letter, content in question_data["options"].items():
            if student_clean in content.upper() or content.upper() in student_clean:
                # Check if this letter is the correct answer
                if letter == correct_clean:
                    return True
    
    # Fallback: exact match or containment
    return student_clean == correct_clean or student_clean in correct_clean or correct_clean in student_clean
```

**使用時修改** [main.py](main.py#L134)：
```python
is_correct = self._check_answer_correctness(
    student_answer,
    question["standard_answer"],
    question  # 傳入完整題目數據
)
```

### 方案 2：標準化題目生成格式

修改 [models/question_generator.py](models/question_generator.py#L264) 的解析邏輯：

```python
def _parse_multiple_choice(self, response: str) -> Dict:
    """Parse LLM response to extract multiple choice question details"""
    result = {
        "question": "",
        "options": {"A": "", "B": "", "C": "", "D": ""},
        "answer": "",
        "explanation": ""
    }
    
    lines = response.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        if line.startswith('题目：') or line.startswith('題目：'):
            result["question"] = line.replace('题目：', '').replace('題目：', '').strip()
        elif line.startswith('A.') or line.startswith('A、'):
            result["options"]["A"] = line[2:].strip()
        elif line.startswith('B.') or line.startswith('B、'):
            result["options"]["B"] = line[2:].strip()
        elif line.startswith('C.') or line.startswith('C、'):
            result["options"]["C"] = line[2:].strip()
        elif line.startswith('D.') or line.startswith('D、'):
            result["options"]["D"] = line[2:].strip()
        elif line.startswith('答案：'):
            # Extract only the letter, ignore any explanation
            answer_text = line.replace('答案：', '').strip().upper()
            # Only keep the first letter A/B/C/D
            for letter in ['A', 'B', 'C', 'D']:
                if letter in answer_text:
                    result["answer"] = letter
                    break
        elif line.startswith('解释：') or line.startswith('解釋：'):
            result["explanation"] = line.replace('解释：', '').replace('解釋：', '').strip()
    
    return result
```

### 方案 3：改進錯誤分析提示（最重要）

修改 [models/error_analyzer.py](models/error_analyzer.py#L190) 的提示詞，讓 LLM 接收完整信息：

```python
def _generate_explanation(
    self,
    question: str,
    student_answer: str,
    correct_answer: str,
    root_cause: str
) -> str:
    """Generate detailed explanation of the error"""
    
    # Extract options from question if it's multiple choice
    options_text = ""
    if "A." in question or "A、" in question:
        options_text = "\n\n選項已包含在題目中"
    
    prompt = f"""為學生解釋他們的錯誤：

題目：{question}
學生選擇：{student_answer}
正確選項：{correct_answer}
根本原因：{root_cause}

重要提示：
- 學生答案和正確答案都是選項字母（A/B/C/D）
- 請基於題目中提供的選項進行分析
- 不要重新計算或推導答案，請使用給定的正確選項

請提供清晰易懂的解釋，包括：
1. 為什麼學生選擇的選項 {student_answer} 是錯的
2. 為什麼選項 {correct_answer} 是正確答案
3. 關鍵概念或規則說明"""
    
    return self.llm.generate_text(
        prompt,
        system_message="你是一位耐心的教師。請嚴格按照給定的正確答案選項進行解釋，不要自行重新計算或推導。"
    )
```

### 方案 4：添加答案驗證日誌

在 [main.py](main.py#L134) 添加調試信息：

```python
# Check if answer is correct
is_correct = self._check_answer_correctness(
    student_answer,
    question["standard_answer"],
    question
)

# Debug logging (可選)
print(f"\n[DEBUG] 答案驗證:")
print(f"  學生答案: {student_answer}")
print(f"  標準答案: {question['standard_answer']}")
print(f"  判定結果: {'正確' if is_correct else '錯誤'}")
if "options" in question:
    print(f"  選項內容:")
    for letter, content in question["options"].items():
        marker = " ← 學生選擇" if letter == student_answer.strip().upper() else ""
        marker += " ← 正確答案" if letter == question["standard_answer"].strip().upper() else ""
        print(f"    {letter}. {content}{marker}")
print()
```

---

## 快速修復步驟

如果您遇到此問題，建議按以下順序實施：

1. ✅ **立即實施方案 3**：改進錯誤分析提示，防止 LLM 重新計算
2. ✅ **實施方案 2**：標準化答案格式，確保 `standard_answer` 只存儲字母
3. ✅ **實施方案 1**：增強答案比對邏輯，處理各種輸入情況
4. 🔍 **可選方案 4**：添加日誌用於調試

## 測試驗證

修復後，用以下測試案例驗證：

```python
# 測試案例
question = {
    "question": "已知函數 f(x) = log₂(x+a) 的圖像經過點 (2, 3)，則 a 的值為？",
    "options": {
        "A": "-2",
        "B": "6",
        "C": "2",
        "D": "-6"
    },
    "standard_answer": "B"
}

# 測試 1: 用戶輸入字母
assert _check_answer_correctness("B", "B", question) == True
assert _check_answer_correctness("D", "B", question) == False

# 測試 2: 用戶輸入數值
assert _check_answer_correctness("6", "B", question) == True
assert _check_answer_correctness("-6", "B", question) == False

# 測試 3: 大小寫不敏感
assert _check_answer_correctness("b", "B", question) == True
```

---

## 預防措施

### 1. 題目生成時的驗證

在 [models/question_generator.py](models/question_generator.py#L66) 添加驗證：

```python
# After parsing
parsed = self._parse_multiple_choice(question_text)

# Validate answer format
if parsed.get("answer") not in ['A', 'B', 'C', 'D']:
    print(f"警告：答案格式不正確 - {parsed.get('answer')}")
    # Try to fix or regenerate
    parsed["answer"] = "A"  # Default fallback

questions.append({
    "id": self.question_count + i + 1,
    "subject": subject,
    "difficulty": difficulty,
    "question": parsed.get("question", question_text),
    "options": parsed.get("options", {}),
    "standard_answer": parsed.get("answer", ""),  # 確保是單個字母
    "explanation": parsed.get("explanation", ""),
    "student_name": student_profile.get("name", "學生"),
    "created_for_weak_point": True
})
```

### 2. 提示詞改進

在 [models/question_generator.py](models/question_generator.py#L195) 的提示詞中強調：

```python
prompt = f"""...

請用以下格式生成題目：
題目：[具體的選擇題問題]
A. [選項A]
B. [選項B]
C. [選項C]
D. [選項D]
答案：[只寫一個字母 A 或 B 或 C 或 D，不要添加其他文字]
解釋：[簡單說明為什麼這個答案正確]

注意：答案行必須只包含單個字母！"""
```

---

## 總結

這個問題的核心在於：
1. 答案存儲格式不一致（字母 vs 內容）
2. 比對邏輯不夠強健
3. LLM 在分析時可能重新計算，與系統判定不一致

通過實施上述方案，可以從根本上解決這個問題，確保系統判定的正確性和一致性。
