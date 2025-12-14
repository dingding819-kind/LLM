"""
Question Generator - Creates personalized learning questions
"""
from typing import Optional, List, Dict
from models.llm_client import LLMClient
from config import NUM_QUESTIONS_PER_SESSION, SUBJECTS, SUBJECT_TOPICS


class QuestionGenerator:
    """Generate personalized questions based on student learning records"""

    def __init__(self, llm_client: LLMClient):
        """
        Initialize question generator
        
        Args:
            llm_client: LLM client instance
        """
        self.llm = llm_client
        self.question_count = 0

    def generate_questions(
        self,
        student_profile: Dict,
        num_questions: Optional[int] = None,
        subject: Optional[str] = None,
        difficulty: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Generate personalized questions
        
        Args:
            student_profile: Dictionary with student info
                {
                    "name": str,
                    "grade": int,
                    "weak_subjects": List[str],
                    "recent_scores": Dict[str, float],
                    "learning_style": str
                }
            num_questions: Number of questions to generate
            subject: Specific subject (if None, use weak subjects)
            difficulty: Difficulty level ("easy", "medium", "hard")
            
        Returns:
            List of question dictionaries
        """
        num_questions = num_questions or NUM_QUESTIONS_PER_SESSION
        
        # Determine subject focus
        if subject is None:
            weak_subjects = student_profile.get("weak_subjects", SUBJECTS[:2])
            subject = weak_subjects[0] if weak_subjects else "數學"
        
        difficulty = difficulty or self._determine_difficulty(student_profile)
        
        questions = []
        for i in range(num_questions):
            prompt = self._build_question_prompt(
                student_profile, subject, difficulty, i + 1
            )
            
            question_text = self.llm.generate_text(
                prompt,
                system_message="你是一位優秀的教師，設計教學問題。生成一個清晰、有趣且能幫助學生學習的題目，並嚴格依照指定格式輸出。"
            )
            
            if question_text:
                # Parse the response to extract question, options, and answer
                parsed = self._parse_multiple_choice(question_text)
                
                questions.append({
                    "id": self.question_count + i + 1,
                    "subject": subject,
                    "difficulty": difficulty,
                    "question": parsed.get("question", question_text),
                    "options": parsed.get("options", {}),
                    "standard_answer": parsed.get("answer", ""),
                    "explanation": parsed.get("explanation", ""),
                    "student_name": student_profile.get("name", "學生"),
                    "created_for_weak_point": True
                })
        
        self.question_count += num_questions
        return questions

    def generate_followup_question(
        self,
        original_question: str,
        student_answer: str,
        feedback: str
    ) -> Optional[Dict[str, str]]:
        """
        Generate a follow-up question based on student's answer and feedback
        
        Args:
            original_question: The original question
            student_answer: Student's answer to the question
            feedback: Feedback on the student's answer
            
        Returns:
            A follow-up question dictionary
        """
        prompt = f"""學生回答了以下問題：
    問題：{original_question}
    學生答案：{student_answer}
    回饋：{feedback}

    請生成一個後續問題，幫助學生更好地理解這個概念。該問題應該：
    1. 針對性地解決學生的誤解
    2. 逐步建立更深層的理解
    3. 與原始問題相關但從不同角度"""
        
        followup = self.llm.generate_text(prompt)
        
        if followup:
            return {
                "type": "followup",
                "original_question": original_question,
                "followup_question": followup
            }
        return None

    def generate_practice_questions(
        self,
        topic: str,
        num_questions: int = 5,
        difficulty: str = "medium"
    ) -> List[Dict[str, str]]:
        """
        Generate practice questions for a specific topic
        
        Args:
            topic: Learning topic
            num_questions: Number of questions
            difficulty: Difficulty level
            
        Returns:
            List of practice questions
        """
        questions = []
        
        prompt = f"""請生成{num_questions}個關於"{topic}"的學習問題。
    難度等級：{difficulty}

    要求：
    1. 問題應該逐步遞進
    2. 每個問題都應該幫助學生掌握"{topic}"的不同面向
    3. 格式清晰易讀
    4. 包含實際應用情境

    請以編號列表形式列出問題。"""
        
        response = self.llm.generate_text(prompt)
        
        if response:
            # Parse response to extract individual questions
            question_lines = response.split('\n')
            for line in question_lines:
                if line.strip():
                    questions.append({
                        "topic": topic,
                        "difficulty": difficulty,
                        "question": line.strip()
                    })
        
        return questions[:num_questions]

    def _build_question_prompt(
        self,
        student_profile: Dict,
        subject: str,
        difficulty: str,
        question_number: int
    ) -> str:
        """Build detailed prompt for question generation"""
        
        grade = student_profile.get("grade", "初一")
        learning_style = student_profile.get("learning_style", "普通")
        recent_topics = student_profile.get("recent_topics", [])
        
        # Choose a topic to diversify coverage
        available_topics = SUBJECT_TOPICS.get(subject, [])
        chosen_topic = (recent_topics[0] if recent_topics else None) or (available_topics[(question_number - 1) % len(available_topics)] if available_topics else "基礎知識")

        prompt = f"""為一名{grade}學生生成第{question_number}個{subject}選擇題，主題為「{chosen_topic}」。

    學生資訊：
    - 年級：{grade}
    - 學習風格：{learning_style}
    - 最近學習主題：{', '.join(recent_topics) if recent_topics else '基礎知識'}

    題目要求（必須遵守）：
    - 難度：{difficulty}
    - 科目：{subject}
    - 主題：{chosen_topic}
    - 題型：單選題（四個選項，其中一個正確答案）
    - 具體且能夠測試學生的理解
    - 適合{grade}學生的認知水準
    - 獨立的問題，不依賴其他問題

    請用以下格式生成題目：
    題目：[具體的選擇題問題]
    A. [選項A]
    B. [選項B]
    C. [選項C]
    D. [選項D]
    答案：[只寫一個字母 A 或 B 或 C 或 D，不要添加其他文字或解釋]
    解釋：[簡單說明為什麼這個答案正確]
    
    重要：答案行必須只包含單個字母（A/B/C/D），例如：
    答案：B
    而不是：答案：B (6) 或 答案：B，因為..."""
        
        return prompt

    def _determine_difficulty(self, student_profile: Dict) -> str:
        """Determine appropriate difficulty level based on student profile"""
        
        recent_scores = student_profile.get("recent_scores", {})
        
        if not recent_scores:
            return "medium"
        
        avg_score = sum(recent_scores.values()) / len(recent_scores)
        
        if avg_score >= 85:
            return "hard"
        elif avg_score >= 70:
            return "medium"
        else:
            return "easy"

    def generate_quiz(
        self,
        student_profile: Dict,
        num_questions: int = 5
    ) -> List[Dict[str, str]]:
        """
        Generate a full quiz session
        
        Args:
            student_profile: Student information
            num_questions: Total questions in quiz
            
        Returns:
            List of quiz questions
        """
        # Get weak subjects
        weak_subjects = student_profile.get("weak_subjects", SUBJECTS[:2])
        
        # Distribute questions across weak subjects
        questions_per_subject = max(1, num_questions // len(weak_subjects))
        remainder = num_questions % len(weak_subjects)
        
        all_questions = []
        
        for i, subject in enumerate(weak_subjects):
            # Add one extra question to first few subjects if there's remainder
            num_for_subject = questions_per_subject + (1 if i < remainder else 0)
            
            subject_questions = self.generate_questions(
                student_profile,
                num_questions=num_for_subject,
                subject=subject
            )
            all_questions.extend(subject_questions)
        
        return all_questions[:num_questions]

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
            
            # Support both simplified and traditional Chinese
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
                # Extract only the letter, ignore any explanation after it
                answer_text = line.replace('答案：', '').strip().upper()
                # Only keep the first occurrence of A/B/C/D
                for letter in ['A', 'B', 'C', 'D']:
                    if letter in answer_text:
                        result["answer"] = letter
                        break
            elif line.startswith('解释：') or line.startswith('解釋：'):
                result["explanation"] = line.replace('解释：', '').replace('解釋：', '').strip()
        
        # Validation: ensure answer is a valid letter
        if result["answer"] not in ['A', 'B', 'C', 'D']:
            print(f"⚠️  警告：答案格式不正確 - '{result['answer']}'，使用預設值 A")
            result["answer"] = "A"
        
        return result
