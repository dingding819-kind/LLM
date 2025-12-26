"""
Question Bank Parser - 將題庫轉換為 JSON 格式供網頁使用
"""
import re
import json
from pathlib import Path

def parse_question_bank(file_path: str, subject: str) -> list:
    """解析題庫文件，返回題目列表"""
    questions = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 以 ======== 分隔每道題目
    blocks = re.split(r'={10,}', content)
    
    for block in blocks:
        block = block.strip()
        if not block or '【題目】' not in block:
            continue
        
        try:
            # 提取範圍
            scope_match = re.search(r'【範圍】(.+?)(?=【|$)', block, re.DOTALL)
            scope = scope_match.group(1).strip() if scope_match else ""
            
            # 提取題目
            question_match = re.search(r'【題目】(.+?)【答案】', block, re.DOTALL)
            if not question_match:
                continue
            question_text = question_match.group(1).strip()
            
            # 提取答案
            answer_match = re.search(r'【答案】\s*[（(]([A-Da-d])[)）]', block)
            if not answer_match:
                continue
            answer = answer_match.group(1).upper()
            
            # 解析題目和選項
            # 移除題號 (如 "（）1、" 或 "（）1." 等)
            question_text = re.sub(r'^[（(）)\s]*\d+[、.．]?\s*', '', question_text)
            
            # 分離選項
            options = {}
            # 嘗試多種選項格式
            option_patterns = [
                r'\(([A-D])\)\s*([^(]+?)(?=\([A-D]\)|$)',  # (A) text
                r'([A-D])\.\s*([^A-D]+?)(?=[A-D]\.|$)',     # A. text
            ]
            
            for pattern in option_patterns:
                matches = re.findall(pattern, question_text, re.DOTALL)
                if matches and len(matches) >= 2:
                    for letter, text in matches:
                        options[letter.upper()] = text.strip()
                    break
            
            # 如果找不到標準選項格式，嘗試按行分割
            if len(options) < 2:
                lines = question_text.split('\n')
                for line in lines:
                    line = line.strip()
                    match = re.match(r'^\s*[（(]?([A-D])[)）]?\s*[、.．]?\s*(.+)', line)
                    if match:
                        options[match.group(1).upper()] = match.group(2).strip()
            
            # 清理題目文本（移除選項部分）
            clean_question = question_text
            for pattern in [r'\([A-D]\)[^(]+', r'[A-D]\.[^A-D]+']:
                clean_question = re.sub(pattern, '', clean_question, flags=re.DOTALL)
            clean_question = clean_question.strip()
            
            # 如果清理後題目太短，使用第一行
            if len(clean_question) < 10:
                clean_question = question_text.split('\n')[0].strip()
                clean_question = re.sub(r'^[（(）)\s]*\d+[、.．]?\s*', '', clean_question)
            
            if len(options) >= 2:
                questions.append({
                    "subject": subject,
                    "scope": scope,
                    "question": clean_question,
                    "options": options,
                    "answer": answer
                })
        except Exception as e:
            print(f"解析錯誤: {e}")
            continue
    
    return questions


def main():
    base_dir = Path(__file__).parent
    
    # 題庫對應
    bank_files = {
        "國語": base_dir / "question_banks" / "chinese.txt",
        "數學": base_dir / "question_banks" / "math.txt",
        "英語": base_dir / "question_banks" / "english.txt",
        "社會": base_dir / "question_banks" / "society.txt",
        "自然": base_dir / "question_banks" / "science.txt",
    }
    
    all_questions = {}
    
    for subject, file_path in bank_files.items():
        if file_path.exists():
            questions = parse_question_bank(str(file_path), subject)
            all_questions[subject] = questions
            print(f"✓ {subject}: 解析 {len(questions)} 題")
        else:
            print(f"✗ {subject}: 檔案不存在 ({file_path})")
    
    # 輸出 JSON
    output_path = base_dir / "web" / "question_bank.js"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("// 自動生成的題庫資料\n")
        f.write("const questionBank = ")
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    
    print(f"\n✅ 題庫已匯出至: {output_path}")
    
    # 統計
    total = sum(len(qs) for qs in all_questions.values())
    print(f"📊 總題數: {total}")


if __name__ == "__main__":
    main()
