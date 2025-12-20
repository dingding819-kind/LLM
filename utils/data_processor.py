"""
Data Processor - Handle student data and learning records
"""
import json
import hashlib
from typing import Dict, List, Optional
from pathlib import Path
from config import STUDENT_DATA_DIR
from utils.question_bank_parser import load_question_bank


class DataProcessor:
    """Process and manage student learning data"""

    def __init__(self, data_dir: str = STUDENT_DATA_DIR):
        """
        Initialize data processor
        
        Args:
            data_dir: Directory for storing student data
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.question_bank = []  # 題庫

    def save_student_profile(
        self,
        student_id: str,
        profile: Dict
    ) -> bool:
        """
        Save student profile
        
        Args:
            student_id: Student identifier
            profile: Student profile dictionary
            
        Returns:
            True if successful
        """
        try:
            file_path = self.data_dir / f"student_{student_id}.json"
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(profile, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving student profile: {e}")
            return False

    def load_student_profile(self, student_id: str) -> Optional[Dict]:
        """
        Load student profile
        
        Args:
            student_id: Student identifier
            
        Returns:
            Student profile dictionary or None
        """
        try:
            file_path = self.data_dir / f"student_{student_id}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading student profile: {e}")
        return None

    def save_learning_record(
        self,
        student_id: str,
        record: Dict
    ) -> bool:
        """
        Save a learning session record
        
        Args:
            student_id: Student identifier
            record: Learning record dictionary
            
        Returns:
            True if successful
        """
        try:
            file_path = self.data_dir / f"records_{student_id}.json"
            
            records = []
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    records = json.load(f)
            
            records.append(record)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(records, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error saving learning record: {e}")
            return False

    def get_learning_records(
        self,
        student_id: str,
        limit: Optional[int] = None
    ) -> List[Dict]:
        """
        Get student's learning records
        
        Args:
            student_id: Student identifier
            limit: Maximum number of records to return
            
        Returns:
            List of learning records
        """
        try:
            file_path = self.data_dir / f"records_{student_id}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    records = json.load(f)
                    if limit:
                        return records[-limit:]
                    return records
        except Exception as e:
            print(f"Error loading learning records: {e}")
        return []

    def calculate_weak_subjects(
        self,
        student_id: str,
        num_records: int = 10
    ) -> List[str]:
        """
        Calculate weak subjects based on recent records
        
        Args:
            student_id: Student identifier
            num_records: Number of recent records to analyze
            
        Returns:
            List of weak subjects sorted by weakness
        """
        records = self.get_learning_records(student_id, limit=num_records)
        
        subject_scores = {}
        
        for record in records:
            subject = record.get("subject", "Unknown")
            score = record.get("score", 0)
            
            if subject not in subject_scores:
                subject_scores[subject] = []
            subject_scores[subject].append(score)
        
        # Calculate average score per subject
        subject_averages = {}
        for subject, scores in subject_scores.items():
            subject_averages[subject] = sum(scores) / len(scores)
        
        # Sort by average score (ascending)
        weak_subjects = sorted(
            subject_averages.items(),
            key=lambda x: x[1]
        )
        
        return [subject for subject, _ in weak_subjects]

    def update_student_progress(
        self,
        student_id: str,
        question_id: int,
        correct: bool,
        subject: str,
        time_spent: float = 0.0,
        concept_to_reinforce: str = "",
        scope: str = ""
    ) -> bool:
        """
        Update student progress for a specific question
        
        Args:
            student_id: Student identifier
            question_id: Question identifier
            correct: Whether answer was correct
            subject: Subject area
            time_spent: Time spent on question (seconds)
                        concept_to_reinforce: Key concept that needs reinforcement (for incorrect answers)
            
        Returns:
            True if successful
        """
        from datetime import datetime
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "question_id": question_id,
            "correct": correct,
            "subject": subject,
            "time_spent": time_spent,
            "score": 100 if correct else 0,
            "concept_to_reinforce": concept_to_reinforce,
            "scope": scope
        }
        
        return self.save_learning_record(student_id, record)

    def get_progress_summary(
        self,
        student_id: str,
        num_records: int = 20
    ) -> Dict:
        """
        Get summary of student's progress
        
        Args:
            student_id: Student identifier
            num_records: Number of records to analyze
            
        Returns:
            Progress summary dictionary
        """
        records = self.get_learning_records(student_id, limit=num_records)
        
        if not records:
            return {
                "total_questions": 0,
                "correct_answers": 0,
                "accuracy": 0.0,
                "subjects": {},
                "weak_areas": [],
                "concepts_to_reinforce": []
            }
        
        total_questions = len(records)
        correct_answers = sum(1 for r in records if r.get("correct", False))
        accuracy = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Subject-wise analysis and concepts to reinforce
        subjects = {}
        concepts_to_reinforce = []
        for record in records:
            subject = record.get("subject", "Unknown")
            concept = record.get("scope") or record.get("concept_to_reinforce", "")
            # Collect concepts (or scopes) from incorrect answers
            if concept and not record.get("correct", False):
                concepts_to_reinforce.append(concept)
            if subject not in subjects:
                subjects[subject] = {"total": 0, "correct": 0}
            subjects[subject]["total"] += 1
            if record.get("correct", False):
                subjects[subject]["correct"] += 1
        
        # Calculate subject accuracies
        for subject in subjects:
            total = subjects[subject]["total"]
            correct = subjects[subject]["correct"]
            subjects[subject]["accuracy"] = (correct / total * 100) if total > 0 else 0
        
        return {
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy": round(accuracy, 2),
            "subjects": subjects,
            "weak_areas": self.calculate_weak_subjects(student_id),
            "concepts_to_reinforce": concepts_to_reinforce
        }

    def load_question_bank_file(self, file_path: str, subject: str) -> int:
        """
        載入題庫文件
        
        Args:
            file_path: 題庫文件路徑
            subject: 科目名稱
            
        Returns:
            成功載入的題目數量
        """
        try:
            questions = load_question_bank(file_path, subject)
            self.question_bank.extend(questions)
            print(f"成功載入 {len(questions)} 題題庫")
            return len(questions)
        except Exception as e:
            print(f"載入題庫失敗: {e}")
            return 0

    def _get_question_hash(self, question: Dict) -> str:
        """
        計算題目的唯一雜湊值
        
        Args:
            question: 題目字典
            
        Returns:
            雜湊值
        """
        q_text = question.get('question', '')
        q_subject = question.get('subject', '')
        combined = f"{q_subject}:{q_text}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get_question_from_bank(self, subject: Optional[str] = None, used_questions: Optional[List[str]] = None) -> Optional[Dict]:
        """
        從題庫中取得題目（避免重複）
        
        Args:
            subject: 指定科目（可選）
            used_questions: 已使用題目的雜湊值列表
            
        Returns:
            題目字典或None
        """
        if not self.question_bank:
            return None
        
        used_questions = used_questions or []
        
        # 如果指定科目，篩選該科目的題目
        if subject:
            subject_questions = [q for q in self.question_bank if q.get('subject') == subject]
        else:
            subject_questions = self.question_bank
        
        if not subject_questions:
            return None
        
        # 過濾掉已使用的題目
        available_questions = [
            q for q in subject_questions 
            if self._get_question_hash(q) not in used_questions
        ]
        
        # 如果沒有未使用的題目，返回None（表示已出完）
        if not available_questions:
            return None
        
        # 隨機選擇一個未使用的題目
        import random
        return random.choice(available_questions)

    def get_questions_by_scope(
        self,
        scope: str,
        subject: Optional[str] = None,
        used_questions: Optional[List[str]] = None,
        limit: int = 1
    ) -> List[Dict]:
        """
        根據範圍（可選科目）從題庫取得題目
        
        Args:
            scope: 題目範圍（與題庫中的 scope 欄位匹配）
            subject: 限定科目（可選）
            used_questions: 已使用題目的雜湊值列表（避免重複）
            limit: 需要取得的題目數量
        
        Returns:
            題目列表（長度不超過 limit）
        """
        results: List[Dict] = []
        if not self.question_bank or not scope:
            return results
        used_questions = used_questions or []
        
        # 篩選範圍與科目
        candidates = [
            q for q in self.question_bank
            if (q.get('scope') == scope) and (subject is None or q.get('subject') == subject)
        ]
        if not candidates:
            return results
        
        # 過濾掉已使用的
        available = [q for q in candidates if self._get_question_hash(q) not in used_questions]
        if not available:
            available = candidates  # 若都用過，允許重複
        
        import random
        random.shuffle(available)
        for q in available:
            results.append(q)
            if len(results) >= limit:
                break
        return results

    def has_question_bank(self, subject: Optional[str] = None) -> bool:
        """
        檢查是否有題庫可用
        
        Args:
            subject: 指定科目（可選）
            
        Returns:
            是否有題庫
        """
        if not self.question_bank:
            return False
        
        if subject:
            return any(q.get('subject') == subject for q in self.question_bank)
        
        return True

    def get_question_bank_count(self, subject: Optional[str] = None) -> int:
        """
        取得題庫數量
        
        Args:
            subject: 指定科目（可選）
            
        Returns:
            題目數量
        """
        if not self.question_bank:
            return 0
        
        if subject:
            return sum(1 for q in self.question_bank if q.get('subject') == subject)
        
        return len(self.question_bank)
