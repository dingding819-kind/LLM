"""
Knowledge Fuel Station - Main Application
Interactive learning assistant using LLM
"""

import json
from typing import Dict, List, Optional
from models import LLMClient, QuestionGenerator, ErrorAnalyzer
from utils import DataProcessor, ReportGenerator
from config import SUBJECTS, SUBJECT_CORRECTIONS


class KnowledgeFuelStation:
    """Main application class for Knowledge Fuel Station"""

    def __init__(self):
        """Initialize the application"""
        self.llm = LLMClient()
        self.question_generator = QuestionGenerator(self.llm)
        self.error_analyzer = ErrorAnalyzer(self.llm)
        self.data_processor = DataProcessor()
        self.report_generator = ReportGenerator()
        self.current_student = None
        self.subject_corrections = {}  # Track corrected subjects in this session

    def load_student(self, student_id: str) -> Optional[Dict]:
        """
        Load a student profile
        
        Args:
            student_id: Student identifier
            
        Returns:
            Student profile or None
        """
        profile = self.data_processor.load_student_profile(student_id)
        if profile:
            self.current_student = profile
        return profile
    
    def correct_subject_name(self, subject_input: str) -> str:
        """
        Correct subject name based on input (handles typos)
        
        Args:
            subject_input: User input for subject name
            
        Returns:
            Corrected subject name
        """
        subject_clean = subject_input.strip()
        
        # Check if already correct
        if subject_clean in SUBJECTS:
            return subject_clean
        
        # Check correction mapping
        if subject_clean in SUBJECT_CORRECTIONS:
            corrected = SUBJECT_CORRECTIONS[subject_clean]
            self.subject_corrections[subject_clean] = corrected
            return corrected
        
        # Fuzzy match (simple similarity check)
        for correct_subject in SUBJECTS:
            # Check if input is substring or similar
            if subject_clean in correct_subject or correct_subject in subject_clean:
                self.subject_corrections[subject_clean] = correct_subject
                return correct_subject
        
        # If no match found, return original
        return subject_clean

    def create_student_profile(
        self,
        student_id: str,
        name: str,
        grade: str,
        weak_subjects: List[str],
        learning_style: str = "visual"
    ) -> Dict:
        """
        Create a new student profile
        
        Args:
            student_id: Unique student identifier
            name: Student's name
            grade: Grade level (e.g., "初一", "初二")
            weak_subjects: List of subjects needing improvement
            learning_style: Learning style preference
            
        Returns:
            Created student profile
        """
        profile = {
            "student_id": student_id,
            "name": name,
            "grade": grade,
            "weak_subjects": weak_subjects,
            "learning_style": learning_style,
            "recent_scores": {},
            "recent_topics": [],
            "total_sessions": 0,
            "used_questions": [],
            "creation_date": str(__import__('datetime').datetime.now())
        }
        
        self.data_processor.save_student_profile(student_id, profile)
        self.current_student = profile
        return profile

    def start_learning_session(
        self,
        selected_subjects: Optional[List[str]] = None,
        use_hybrid: bool = True,
        num_questions_per_subject: Optional[int] = None
    ) -> Dict:
        """
        Start an interactive learning session
        
                Args:
                    selected_subjects: Optional list of subjects for this session
                    use_hybrid: Use hybrid mode (question bank + LLM) if True
        
        Returns:
            Session with generated questions
        """
        if not self.current_student:
            print("請先載入或建立學生資料")
            return {}
        
        student_profile = self.current_student.copy()
        
        # Use selected subjects for this session if provided
        if selected_subjects:
            corrected_subjects = [self.correct_subject_name(s) for s in selected_subjects]
            student_profile["weak_subjects"] = corrected_subjects
            print(f"\n本次學習科目：{', '.join(corrected_subjects)}")
            
            # Show corrections if any
            for original, corrected in self.subject_corrections.items():
                if original != corrected:
                    print(f"  ℹ️  已將 '{original}' 修正為 '{corrected}'")
        
        # Generate questions using hybrid mode
        questions = []
        
        if use_hybrid and self.data_processor.has_question_bank():
            # Hybrid mode: use question bank + LLM
            questions = self._generate_hybrid_questions(
                student_profile,
                num_questions_per_subject=num_questions_per_subject
            )
        else:
            # Pure LLM mode
            questions = self.question_generator.generate_quiz(
                student_profile,
                num_questions=num_questions_per_subject or 3
            )
        
        session = {
            "student_id": student_profile["student_id"],
            "student_name": student_profile["name"],
            "questions": questions,
            "responses": [],
            "session_start": str(__import__('datetime').datetime.now())
        }
        
        return session
    
    def _generate_hybrid_questions(
        self,
        student_profile: Dict,
        num_questions_per_subject: Optional[int] = None
    ) -> List[Dict]:
        """
        Generate questions using hybrid mode (question bank + LLM)
        
        Args:
            student_profile: Student profile dictionary
            
        Returns:
            List of questions
        """
        questions = []
        weak_subjects = student_profile.get("weak_subjects", [])
        num_questions_per_subject = num_questions_per_subject or 3  # Default
        
        used_questions = student_profile.get("used_questions", [])
        
        for subject in weak_subjects:
            # Check if question bank has questions for this subject
            bank_count = self.data_processor.get_question_bank_count(subject)
            
            if bank_count > 0:
                # Use questions from bank (up to num_questions_per_subject)
                for _ in range(min(num_questions_per_subject, bank_count)):
                    bank_question = self.data_processor.get_question_from_bank(subject, used_questions)
                    if bank_question:
                        # Format bank question to match expected structure
                        formatted_q = {
                            "id": len(questions) + 1,
                            "subject": bank_question.get("subject", subject),
                            "difficulty": "中等",  # Default difficulty for bank questions
                            "question": bank_question.get("question", ""),
                            "options": bank_question.get("options", {}),
                            "standard_answer": bank_question.get("correct_answer", "A"),
                            "explanation": bank_question.get("explanation", ""),
                            "topic": bank_question.get("scope", ""),
                            "source": "question_bank"
                        }
                        questions.append(formatted_q)
                        # Track this question to avoid repetition
                        q_hash = self.data_processor._get_question_hash(bank_question)
                        used_questions.append(q_hash)
                        print(f"  📚 從題庫取得 {subject} 題目")
                
                # If bank questions < desired, fill with LLM
                remaining = num_questions_per_subject - len([q for q in questions if q["subject"] == subject])
                if remaining > 0:
                    print(f"  🤖 生成 {remaining} 題 {subject} LLM問題補充")
                    # Create a temporary profile for this subject only
                    temp_profile = student_profile.copy()
                    temp_profile["weak_subjects"] = [subject]
                    llm_questions = self.question_generator.generate_quiz(temp_profile, num_questions=remaining)
                    questions.extend(llm_questions)
            else:
                # No bank questions, use pure LLM
                print(f"  🤖 生成 {num_questions_per_subject} 題 {subject} LLM問題")
                temp_profile = student_profile.copy()
                temp_profile["weak_subjects"] = [subject]
                llm_questions = self.question_generator.generate_quiz(temp_profile, num_questions=num_questions_per_subject)
                questions.extend(llm_questions)
        
        return questions

    def process_answer(
        self,
        session: Dict,
        question_index: int,
        student_answer: str
    ) -> Dict:
        """
        Process student's answer and provide feedback
        
        Args:
            session: Current learning session
            question_index: Index of the question
            student_answer: Student's answer
            
        Returns:
            Feedback and analysis
        """
        if question_index >= len(session["questions"]):
            return {"error": "Invalid question index"}
        
        question = session["questions"][question_index]
        
        # Analyze the answer
        analysis = self.error_analyzer.analyze_error(
            question=question["question"],
            student_answer=student_answer,
            correct_answer=question["standard_answer"],
            subject=question.get("subject")
        )
        
        # Check if answer is correct (enhanced check with option matching)
        is_correct = self._check_answer_correctness(
            student_answer,
            question["standard_answer"],
            question  # Pass full question data for option matching
        )
        
        # Debug info (optional, can be disabled by setting DEBUG=False in config)
        if hasattr(self, 'debug') and self.debug:
            print(f"\n[答案驗證]")
            print(f"  學生輸入: {student_answer}")
            print(f"  標準答案: {question['standard_answer']}")
            print(f"  判定結果: {'✅ 正確' if is_correct else '❌ 錯誤'}")
            if "options" in question and question["options"]:
                print(f"  選項對照:")
                for letter, content in question["options"].items():
                    marker = ""
                    if letter == student_answer.strip().upper():
                        marker += " ← 學生選擇"
                    if letter == question["standard_answer"].strip().upper():
                        marker += " ← 正確答案"
                    print(f"    {letter}. {content}{marker}")
        
        response = {
            "question_index": question_index,
            "question": question["question"],
            "student_answer": student_answer,
            "correct_answer": question["standard_answer"],
            "is_correct": is_correct,
            "analysis": analysis,
            "feedback": self._generate_feedback(analysis, is_correct)
        }
        
        session["responses"].append(response)
        
        # Extract concept to reinforce if answer is incorrect
        concept_to_reinforce = ""
        scope_tag = question.get("topic") or question.get("scope") or ""
        if not is_correct:
            concept_to_reinforce = scope_tag or self._extract_concept_to_reinforce(
                question["question"],
                question.get("subject", ""),
                analysis
            )
        
        # Update student progress
        self.data_processor.update_student_progress(
            student_id=session["student_id"],
            question_id=question["id"],
            correct=is_correct,
            subject=question.get("subject"),
            concept_to_reinforce=concept_to_reinforce,
            scope=scope_tag
        )
        
        return response

    def generate_followup_question(
        self,
        session: Dict,
        question_index: int
    ) -> Optional[Dict]:
        """
        Generate a follow-up question based on student response
        
        Args:
            session: Current learning session
            question_index: Index of the original question
            
        Returns:
            Follow-up question or None
        """
        if question_index >= len(session["responses"]):
            return None
        
        response = session["responses"][question_index]
        
        if response["is_correct"]:
            return None  # No follow-up needed for correct answers
        
        followup = self.question_generator.generate_followup_question(
            original_question=response["question"],
            student_answer=response["student_answer"],
            feedback=response.get("feedback", "")
        )
        
        return followup

    def end_session(self, session: Dict) -> Dict:
        """
        End learning session and generate report
        
        Args:
            session: Completed learning session
            
        Returns:
            Session summary with score and recommendations
        """
        if not session.get("responses"):
            return {"error": "No responses in session"}
        
        # Calculate scores
        correct_count = sum(1 for r in session["responses"] if r["is_correct"])
        total_count = len(session["responses"])
        accuracy = (correct_count / total_count * 100) if total_count > 0 else 0
        
        # Update student's used_questions list
        if self.current_student:
            student_profile = self.data_processor.load_student_profile(session["student_id"])
            if student_profile:
                # Get all questions from this session
                for i, question in enumerate(session.get("questions", [])):
                    if i < len(session.get("responses", [])):
                        q_hash = self.data_processor._get_question_hash(question)
                        if q_hash not in student_profile.get("used_questions", []):
                            student_profile.setdefault("used_questions", []).append(q_hash)
                
                # Save updated profile
                self.data_processor.save_student_profile(session["student_id"], student_profile)
                self.current_student = student_profile
        
        # Get progress summary
        progress = self.data_processor.get_progress_summary(
            session["student_id"],
            num_records=20
        )
        
        # Generate report
        report = self.report_generator.generate_learning_report(
            session["student_name"],
            progress
        )
        
        recommendations = self.report_generator.generate_recommendations(progress)
        
        summary = {
            "session_id": session.get("student_id") + "_" + str(__import__('datetime').datetime.now().timestamp()),
            "student_name": session["student_name"],
            "correct_answers": correct_count,
            "total_questions": total_count,
            "accuracy": round(accuracy, 2),
            "report": report,
            "recommendations": recommendations,
            "session_end": str(__import__('datetime').datetime.now())
        }
        
        return summary

    def get_student_report(self) -> Optional[Dict]:
        """
        Get comprehensive report for current student
        
        Returns:
            Student report dictionary
        """
        if not self.current_student:
            return None
        
        student_id = self.current_student["student_id"]
        progress = self.data_processor.get_progress_summary(
            student_id,
            num_records=50
        )
        
        report = self.report_generator.generate_learning_report(
            self.current_student["name"],
            progress
        )
        
        chart = self.report_generator.generate_performance_chart(progress)
        recommendations = self.report_generator.generate_recommendations(progress)
        
        return {
            "student_name": self.current_student["name"],
            "report": report,
            "chart": chart,
            "recommendations": recommendations,
            "progress_summary": progress
        }

    def _check_answer_correctness(
        self,
        student_answer: str,
        correct_answer: str,
        question_data: Optional[Dict] = None
    ) -> bool:
        """
        Check if student answer matches correct answer
        
        Args:
            student_answer: Student's answer (can be letter like "B" or content like "6")
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
            
            # If correct_answer is not a letter, try to find match in options
            if question_data and "options" in question_data:
                student_option_content = question_data["options"].get(student_clean, "")
                if correct_clean in student_option_content.upper():
                    return True
        
        # If student typed the full answer content instead of letter
        if question_data and "options" in question_data and len(correct_clean) == 1:
            for letter, content in question_data["options"].items():
                # Check if student's answer matches this option's content
                if student_clean in content.upper() or content.upper().strip() == student_clean:
                    # Check if this letter is the correct answer
                    if letter == correct_clean:
                        return True
        
        # Fallback: exact match or containment
        return student_clean == correct_clean or student_clean in correct_clean or correct_clean in student_clean

    def _generate_feedback(self, analysis: Dict, is_correct: bool) -> str:
        """
        Generate user-friendly feedback
        
        Args:
            analysis: Error analysis dictionary
            is_correct: Whether answer was correct
            
        Returns:
            Feedback message
        """
        if is_correct:
            return "✅ 正確！很好地掌握了這個知識點。"
        
        feedback = "❌ 答案不正確。\n\n"
        feedback += analysis.get("explanation", "")
        
        if analysis.get("hints"):
            feedback += "\n\n📝 改進建議：\n"
            for hint in analysis["hints"][:2]:
                feedback += f"• {hint}\n"
        
        return feedback

    def _extract_concept_to_reinforce(self, question: str, subject: str, analysis: Dict) -> str:
        """
        Extract key concept that needs reinforcement based on the error
        
        Args:
            question: The question text
            subject: Subject area
            analysis: Error analysis from analyzer
            
        Returns:
            Brief description of concept to reinforce
        """
        prompt = f"""根據以下題目和錯誤分析，用一句簡短的話（5-10字）指出學生需要加強的核心觀念。

科目：{subject}
題目：{question}
錯誤分析：{analysis.get('root_cause', '')}

請只回答需要加強的觀念名稱，例如：
- 集合觀念需要加強
- 函數圖像理解不足
- 對數運算不熟悉
- 時態運用需加強

觀念："""
        
        try:
            concept = self.llm.generate_text(
                prompt,
                system_message="你是一位教學分析專家。請用最簡潔的方式指出學生需要補強的核心觀念。",
                max_tokens=50
            )
            return concept.strip() if concept else ""
        except Exception:
            # Fallback: use root cause or generic message
            return (analysis.get('root_cause') or '基礎觀念需加強')[:20]


def interactive_learning_session():
    """Interactive learning session with user input"""
    
    print("\n" + "="*50)
    print("歡迎來到知識加油站 Knowledge Fuel Station")
    print("="*50 + "\n")
    
    app = KnowledgeFuelStation()
    
    # Get student info
    student_id = input("請輸入學生ID: ").strip()
    
    # Try to load existing student or create new one
    student = app.load_student(student_id)
    
    if not student:
        print("\n沒有找到該學生，建立新資料...\n")
        name = input("學生姓名: ").strip()
        grade = input("年級（如：初一）: ").strip()
        
        print(f"\n可選科目：{', '.join(SUBJECTS)}\n")
        weak_subjects_input = input("請輸入需要改進的科目（用逗號分隔）: ").strip()
        weak_subjects = [s.strip() for s in weak_subjects_input.split(',') if s.strip()]
        
        if not weak_subjects:
            print("沒有選擇任何科目，使用預設科目：數學")
            weak_subjects = ["數學"]
        
        student = app.create_student_profile(
            student_id=student_id,
            name=name,
            grade=grade,
            weak_subjects=weak_subjects
        )
        print(f"\n✅ 已建立學生資料：{name}")
    else:
        print(f"\n科目：{', '.join(student.get('weak_subjects', ['未設定']))}")
    
    print(f"\n歡迎，{student['name']}！")
    
    # Auto-load question banks for selected subjects
    print("\n" + "="*50)
    print("自動載入題庫...\n")
    
    # Map subjects to question bank files
    subject_to_file = {
        "國文": "question_banks/chinese.txt",
        "英語": "question_banks/english.txt",
        "數學": "question_banks/math.txt",
        "社會": "question_banks/society.txt",
        "自然": "question_banks/science.txt"
    }
    
    import os
    weak_subjects = student.get('weak_subjects', [])
    loaded_count = 0
    
    for subject in weak_subjects:
        bank_file = subject_to_file.get(subject)
        if bank_file:
            full_path = os.path.join(os.getcwd(), bank_file)
            if os.path.exists(full_path):
                count = app.data_processor.load_question_bank_file(full_path, subject)
                if count > 0:
                    print(f"  ✓ {subject}: 載入 {count} 題")
                    loaded_count += count
            else:
                print(f"  ⚠ {subject}: 題庫文件不存在 ({bank_file})")
        else:
            print(f"  ⚠ {subject}: 無對應題庫")
    
    if loaded_count > 0:
        print(f"\n✅ 共載入 {loaded_count} 題題庫\n")
    else:
        print(f"\n⚠ 未能載入任何題庫，將使用AI生成\n")
    
    # Ask if user wants to change subjects for this session
    print("\n" + "="*50)
    change_subjects = input("要重新選擇本次學習科目嗎？(y/n): ").strip().lower()
    
    selected_subjects = None
    if change_subjects in ['y', 'yes', '是']:
        print(f"\n可選科目：{', '.join(SUBJECTS)}\n")
        subjects_input = input("請輸入本次要學習的科目（用逗號分隔）: ").strip()
        if subjects_input:
            selected_subjects = [s.strip() for s in subjects_input.split(',') if s.strip()]

        # Optional: topic selection per subject
        choose_topics = input("\n是否要為本次科目指定主題範圍？(y/n): ").strip().lower()
        if choose_topics in ['y', 'yes', '是']:
            from config import SUBJECT_TOPICS
            student['recent_topics'] = []
            for subj in selected_subjects:
                corrected = subj
                # Show available topics for corrected subject
                from_subject = corrected
                topics = SUBJECT_TOPICS.get(from_subject, [])
                if topics:
                    print(f"\n{subj} 可選主題：{', '.join(topics)}")
                    t_input = input(f"請輸入要練習的主題（可多個，用逗號分隔；留空表示使用預設）：").strip()
                    if t_input:
                        chosen = [t.strip() for t in t_input.split(',') if t.strip()]
                        # Save first chosen topic as recent focus
                        if chosen:
                            student['recent_topics'].append(chosen[0])
                else:
                    print(f"\n{subj} 暫無主題目錄，將使用基礎知識。")
    
    print("="*50)
    # Let user choose number of questions per subject for this session
    num_q_input = input("本次每科要出幾題？(預設 3): ").strip()
    num_questions_per_subject = None
    if num_q_input.isdigit() and int(num_q_input) > 0:
        num_questions_per_subject = int(num_q_input)

    
    # Start learning session
    print("\n正在生成問題...\n")
    session = app.start_learning_session(
        selected_subjects,
        num_questions_per_subject=num_questions_per_subject
    )
    
    if not session:
        print("無法生成問題")
        return
    
    print(f"已生成 {len(session['questions'])} 道題目\n")
    
    # Interactive Q&A loop
    for i, question in enumerate(session['questions'], 1):
        source_label = "📚 題庫" if question.get('source') == 'question_bank' else "🤖 AI生成"
        print(f"\n【第 {i}/{len(session['questions'])} 題】{source_label}")
        print(f"科目：{question['subject']}")
        print(f"\n題目：{question['question']}\n")
        
        # Display options
        options = question.get('options', {})
        if options:
            for key in ['A', 'B', 'C', 'D']:
                if key in options:
                    print(f"{key}. {options[key]}")
        
        student_answer = input("\n請選擇答案 (A/B/C/D): ").strip().upper()
        
        # Validate answer
        if student_answer not in ['A', 'B', 'C', 'D']:
            print("❌ 請輸入有效的選項 (A/B/C/D)")
            continue
        
        # Process answer
        feedback = app.process_answer(session, i-1, student_answer)
        
        print(f"\n{feedback['feedback']}")
        
        # Show correct answer and explanation
        correct_answer = question.get('standard_answer', '')
        if student_answer != correct_answer:
            print(f"\n正確答案：{correct_answer}")
            if question.get('explanation'):
                print(f"解釋：{question['explanation']}")
        
        # Offer follow-up question
        input("\n按 Enter 繼續下一題...")
    
    # End session and show results
    print("\n" + "="*50)
    print("學習會話結束")
    print("="*50 + "\n")
    
    summary = app.end_session(session)
    # Graceful handling if LLM failed to generate questions
    total_questions = summary.get('total_questions', 0)
    correct_answers = summary.get('correct_answers', 0)
    accuracy = summary.get('accuracy', 0.0)
    print(f"題目完成率：{correct_answers}/{total_questions}")
    print(f"正確率：{accuracy:.1f}%\n")
    if 'report' in summary:
        print(summary['report'])
    if 'recommendations' in summary:
        print(summary['recommendations'])
    
    # Save results
    report_text = (summary.get('report', '') + "\n" + summary.get('recommendations', '')).strip()
    if report_text:
        ReportGenerator.export_report_to_file(
            report_text,
            f"report_{student_id}_{summary.get('session_id','session')[:10]}.txt"
        )
        print(f"✅ 報告已保存")
    print(f"✅ 報告已保存")


if __name__ == "__main__":
    interactive_learning_session()
