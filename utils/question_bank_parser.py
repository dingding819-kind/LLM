"""
題庫解析器 - 解析文本格式的題目和解答
"""
import re
from typing import List, Dict, Optional

class QuestionBankParser:
    """解析題庫文本文件"""
    
    def __init__(self):
        self.questions = []
    
    def parse_file(self, file_path: str, subject: str) -> List[Dict]:
        """
        解析題庫文件
        
        Args:
            file_path: 題庫文件路徑
            subject: 科目名稱
            
        Returns:
            解析後的題目列表
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return self._parse_content(content, subject)
        except Exception as e:
            print(f"解析題庫文件時發生錯誤: {e}")
            return []
    
    def _parse_content(self, content: str, subject: str) -> List[Dict]:
        """
        解析題庫內容（支持多題目）
        
        格式範例（單題）:
        （）1、問題文本...
        (A) 選項A
        (B) 選項B
        (C) 選項C
        (D) 選項D
        
        解答
        （A）1、解析文本...
        
        多題目用【題目】【答案】分隔
        """
        questions = []
        
        # 檢查是否是多題目格式（用【題目】和【答案】分隔）
        if '【題目】' in content and '【答案】' in content:
            return self._parse_multi_questions_format(content, subject)
        
        # 原有格式：單一問題和解答的分割
        parts = content.split('解答')
        if len(parts) != 2:
            print("警告: 題庫格式不正確，應該包含「解答」分隔符")
            return []
        
        question_section = parts[0].strip()
        answer_section = parts[1].strip()
        
        # 解析問題和選項
        question_data = self._parse_question_section(question_section)
        if not question_data:
            return []
        
        # 解析答案
        answer_data = self._parse_answer_section(answer_section)
        if not answer_data:
            return []
        
        # 合併成完整題目
        question = {
            'subject': subject,
            'question': question_data['question'],
            'options': question_data['options'],
            'correct_answer': answer_data['correct_answer'],
            'explanation': answer_data['explanation'],
            'source': 'question_bank'
        }
        
        questions.append(question)
        return questions
    
    def _parse_question_section(self, section: str) -> Optional[Dict]:
        """解析問題段落，支援【範圍】標記"""
        lines = section.strip().split('\n')
        scope = ""
        question_lines = []
        options = {}
        fullwidth_map = {'Ａ': 'A', 'Ｂ': 'B', 'Ｃ': 'C', 'Ｄ': 'D'}

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 範圍標記
            scope_match = re.match(r'【範圍】(.+)', line)
            if scope_match:
                scope = scope_match.group(1).strip()
                continue

            # 選項行
            opt_match = re.match(r'[（(]?\s*([A-DＡＢＣＤ])[）)]?\s*(.+)', line)
            if opt_match:
                letter = opt_match.group(1)
                letter = fullwidth_map.get(letter, letter)
                options[letter] = opt_match.group(2).strip()
                continue

            # 問題文本
            clean_line = re.sub(r'^\s*[（(][）)]?\d+、', '', line)
            if clean_line:
                question_lines.append(clean_line)

        if not question_lines or len(options) < 1:
            return None

        return {
            'question': '\n'.join(question_lines),
            'options': options,
            'scope': scope
        }
    
    def _parse_answer_section(self, section: str) -> Optional[Dict]:
        """解析解答段落（解釋可選）"""
        # 找出答案選項（A/B/C/D）
        answer_match = re.search(r'[（(]([A-D])[）)]', section)
        if not answer_match:
            print("警告: 無法找到正確答案")
            return None
        
        correct_answer = answer_match.group(1)
        
        # 移除答案部分後的剩餘內容作為解釋（可為空）
        lines = section.strip().split('\n')
        explanation_lines = []
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            # 跳過包含正確答案標記的行
            if re.match(r'[（(][A-D][）)]\d*、?', line):
                continue
            # 其他行作為解釋
            explanation_lines.append(line)
        
        # 如果沒有解釋，使用空字符串而不是整個section
        explanation = '\n'.join(explanation_lines)
        
        return {
            'correct_answer': correct_answer,
            'explanation': explanation
        }
    
    def _parse_multi_questions_format(self, content: str, subject: str) -> List[Dict]:
        """
        解析多題目格式（用【題目】和【答案】分隔）
        
        格式:
        【題目】
        （）1、問題文本...
        (A) 選項A
        ...
        
        【答案】
        （A）1、解析文本...
        
        【題目】
        ...（下一題）
        """
        questions = []
        
        # 以分隔線區分題目區塊，支援【範圍】
        blocks = [b.strip() for b in content.split('========================================') if '【題目】' in b and '【答案】' in b]

        for block in blocks:
            scope_text = ""
            scope_match = re.search(r'【範圍】(.+)', block)
            if scope_match:
                scope_text = scope_match.group(1).strip()

            # 拆分題目與答案
            try:
                q_part, a_part = block.split('【答案】', 1)
            except ValueError:
                continue
            if '【題目】' not in q_part:
                continue
            question_text = q_part.split('【題目】', 1)[1].strip()
            answer_text = a_part.strip()

            if not question_text or not answer_text:
                continue

            # 解析題目部分
            q_parsed = self._parse_question_section(question_text)
            if not q_parsed or not q_parsed.get('options'):
                continue

            # 解析答案部分
            a_parsed = self._parse_answer_section(answer_text)
            if not a_parsed:
                continue

            # 合併成完整題目
            question = {
                'subject': subject,
                'question': q_parsed['question'],
                'options': q_parsed['options'],
                'correct_answer': a_parsed['correct_answer'],
                'explanation': a_parsed['explanation'],
                'scope': q_parsed.get('scope') or scope_text,
                'source': 'question_bank'
            }

            questions.append(question)
        
        return questions

def load_question_bank(file_path: str, subject: str) -> List[Dict]:
    """
    載入題庫文件
    
    Args:
        file_path: 題庫文件路徑
        subject: 科目名稱
        
    Returns:
        題目列表
    """
    parser = QuestionBankParser()
    return parser.parse_file(file_path, subject)
    # --- 新增執行區塊 ---
if __name__ == '__main__':
    import os
    
    file_path = 'question_banks/math.txt'
    subject_name = '數學'
    
    # 檢查檔案是否存在
    if not os.path.exists(file_path):
        print(f"錯誤: 找不到檔案 '{file_path}'")
        print(f"當前工作目錄: {os.getcwd()}")
    else:
        print(f"檔案存在: {file_path}")
        
        # 顯示檔案內容前100字元
        with open(file_path, 'r', encoding='utf-8') as f:
            preview = f.read(100)
            print(f"檔案預覽:\n{preview}\n...")
    # 1. 載入並解析題庫
    math_questions = load_question_bank(file_path, subject_name)
    
    # 2. 輸出檢查結果
    if math_questions:
        print(f"成功載入 {len(math_questions)} 題 {subject_name} 題目。")
        
        # 輸出第一個題目進行格式檢查
        print("\n--- 第一題檢查 ---")
        first_q = math_questions[0]
        print(f"科目: {first_q.get('subject')}")
        print(f"範圍: {first_q.get('scope')}")
        print(f"題目: {first_q.get('question')}")
        print(f"選項: {first_q.get('options')}")
        print(f"答案: {first_q.get('correct_answer')}")
        print(f"解析: {first_q.get('explanation')}")
    else:
        print("載入題目失敗或文件內容為空。請檢查文件路徑和格式。")
