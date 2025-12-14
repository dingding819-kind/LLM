"""
Error Analyzer - Analyzes student errors and provides detailed explanations
"""
from typing import Optional, Dict, List
from models.llm_client import LLMClient
from config import ERROR_ANALYSIS_DEPTH, INCLUDE_HINTS, INCLUDE_SIMILAR_PROBLEMS


class ErrorAnalyzer:
    """Analyze student errors and provide comprehensive feedback"""

    def __init__(self, llm_client: LLMClient):
        """
        Initialize error analyzer
        
        Args:
            llm_client: LLM client instance
        """
        self.llm = llm_client

    def analyze_error(
        self,
        question: str,
        student_answer: str,
        correct_answer: str,
        subject: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Analyze student error and provide explanation
        
        Args:
            question: The question asked
            student_answer: Student's incorrect answer
            correct_answer: The correct answer
            subject: Subject area
            
        Returns:
            Dictionary with analysis, explanation, hints, etc.
        """
        analysis = {
            "question": question,
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "analysis": "",
            "explanation": "",
            "root_cause": "",
            "hints": [],
            "similar_problems": []
        }
        
        # Step 1: Identify the root cause
        analysis["root_cause"] = self._identify_root_cause(
            question, student_answer, correct_answer, subject
        )
        
        # Step 2: Provide explanation
        analysis["explanation"] = self._generate_explanation(
            question, student_answer, correct_answer, analysis["root_cause"]
        )
        
        # Step 3: Generate hints for improvement
        if INCLUDE_HINTS:
            analysis["hints"] = self._generate_hints(
                question, student_answer, analysis["root_cause"]
            )
        
        # Step 4: Suggest similar problems
        if INCLUDE_SIMILAR_PROBLEMS:
            analysis["similar_problems"] = self._generate_similar_problems(
                question, subject
            )
        
        # Step 5: Overall analysis summary
        analysis["analysis"] = self._create_analysis_summary(analysis)
        
        return analysis

    def analyze_multiple_errors(
        self,
        error_cases: List[Dict]
    ) -> Dict[str, any]:
        """
        Analyze multiple errors to identify patterns
        
        Args:
            error_cases: List of error dictionaries with keys:
                - question
                - student_answer
                - correct_answer
                - subject
                
        Returns:
            Pattern analysis with recommendations
        """
        analyses = []
        error_patterns = {}
        subject_performance = {}
        
        # Analyze each error
        for error_case in error_cases:
            analysis = self.analyze_error(
                error_case.get("question"),
                error_case.get("student_answer"),
                error_case.get("correct_answer"),
                error_case.get("subject")
            )
            analyses.append(analysis)
            
            # Track patterns
            root_cause = analysis["root_cause"]
            error_patterns[root_cause] = error_patterns.get(root_cause, 0) + 1
            
            # Track subject performance
            subject = error_case.get("subject", "Unknown")
            subject_performance[subject] = subject_performance.get(subject, 0) + 1
        
        # Generate summary
        summary = self._generate_error_pattern_summary(
            error_patterns, subject_performance, len(error_cases)
        )
        
        return {
            "total_errors": len(error_cases),
            "analyses": analyses,
            "error_patterns": error_patterns,
            "subject_performance": subject_performance,
            "summary": summary
        }

    def generate_remedial_plan(
        self,
        student_name: str,
        error_analysis_result: Dict
    ) -> Dict[str, any]:
        """
        Generate a remedial learning plan based on error analysis
        
        Args:
            student_name: Student's name
            error_analysis_result: Result from analyze_multiple_errors
            
        Returns:
            Personalized remedial plan
        """
        prompt = f"""根據以下錯誤分析結果，為{student_name}制定個性化補習計畫：

    錯誤模式：{error_analysis_result.get('error_patterns', {})}
    科目表現：{error_analysis_result.get('subject_performance', {})}
    總錯誤數：{error_analysis_result.get('total_errors', 0)}

    請提供：
    1. 主要需要改進的領域（按優先級）
    2. 對每個領域的具體學習建議
    3. 推薦的練習題類型
    4. 預期改進時間表
    5. 學習資源建議"""
        
        plan_text = self.llm.generate_text(
            prompt,
            system_message="你是一位有經驗的教學規劃師。基於學生的錯誤模式，設計一個有針對性且可執行的學習改進計畫。"
        )
        
        return {
            "student_name": student_name,
            "remedial_plan": plan_text,
            "based_on_errors": error_analysis_result.get('total_errors'),
            "focus_areas": list(error_analysis_result.get('error_patterns', {}).keys())
        }

    def _identify_root_cause(
        self,
        question: str,
        student_answer: str,
        correct_answer: str,
        subject: Optional[str]
    ) -> str:
        """Identify the root cause of the error"""
        
        prompt = f"""分析以下錯誤的根本原因：

    題目：{question}
    學生答案：{student_answer}
    正確答案：{correct_answer}
    科目：{subject or '未指定'}

    請用一句話簡潔地指出根本原因。"""
        
        return self.llm.generate_text(prompt)

    def _generate_explanation(
        self,
        question: str,
        student_answer: str,
        correct_answer: str,
        root_cause: str
    ) -> str:
        """Generate detailed explanation of the error"""
        
        prompt = f"""為學生解釋他們的錯誤：

題目：{question}
學生選擇：{student_answer}
正確答案：{correct_answer}

請提供清晰易懂的解釋，說明：
1. 為什麼選項 {correct_answer} 是正確的
2. 關鍵概念或規則說明

解釋要直接、簡潔，避免反覆推導。"""
        
        return self.llm.generate_text(
            prompt,
            system_message="你是一位耐心的教師。根據給定的正確答案提供簡潔的解釋，不要提出假設性問題或要求提供信息。"
        )

    def _generate_hints(
        self,
        question: str,
        student_answer: str,
        root_cause: str
    ) -> List[str]:
        """Generate helpful hints for improvement"""
        
        prompt = f"""為幫助學生改正錯誤，請生成3個循序漸進的提示：

    題目：{question}
    學生答案：{student_answer}
    錯誤原因：{root_cause}

    提示應該從簡單到複雜，引導學生獨立找到正確答案。
    請以編號列表形式列出。"""
        
        response = self.llm.generate_text(prompt)
        
        # Parse hints from response
        hints = []
        for line in response.split('\n'):
            if line.strip():
                hints.append(line.strip())
        
        return hints[:3]

    def _generate_similar_problems(
        self,
        question: str,
        subject: Optional[str]
    ) -> List[str]:
        """Generate similar problems for practice"""
        
        subject_str = subject or "相关"
        
        prompt = f"""基於以下題目，生成2個類似的練習題目：

    原題：{question}

    這些練習題應該：
    1. 考察相同的知識點和概念
    2. 難度相近
    3. 幫助學生鞏固理解
    4. 題目獨立完整

    請以編號列表形式列出。"""
        
        response = self.llm.generate_text(prompt)
        
        # Parse problems from response
        problems = []
        for line in response.split('\n'):
            if line.strip():
                problems.append(line.strip())
        
        return problems[:2]

    def _create_analysis_summary(self, analysis: Dict) -> str:
        """Create a comprehensive analysis summary"""
        
        summary = f"""錯誤分析總結：

    錯誤根源：{analysis['root_cause']}

    詳細解釋：
    {analysis['explanation']}"""
        
        if analysis['hints']:
            summary += "\n\n改進提示：\n"
            for i, hint in enumerate(analysis['hints'], 1):
                summary += f"{i}. {hint}\n"
        
        if analysis['similar_problems']:
            summary += "\n\n推薦練習題：\n"
            for i, problem in enumerate(analysis['similar_problems'], 1):
                summary += f"{i}. {problem}\n"
        
        return summary

    def _generate_error_pattern_summary(
        self,
        error_patterns: Dict[str, int],
        subject_performance: Dict[str, int],
        total_errors: int
    ) -> str:
        """Generate summary of error patterns"""
        
        # Find most common error
        most_common_error = max(error_patterns, key=error_patterns.get) if error_patterns else "未知"
        
        # Find weakest subject
        weakest_subject = max(subject_performance, key=subject_performance.get) if subject_performance else "未知"
        
        summary = f"""學生學習分析彙總：

    總錯誤數：{total_errors}
    最常見的錯誤類型：{most_common_error}（發生{error_patterns.get(most_common_error, 0)}次）
    最薄弱的科目：{weakest_subject}（錯誤{subject_performance.get(weakest_subject, 0)}次）

    建議重點關注：
    1. 加強{weakest_subject}的基礎知識學習
    2. 針對"{most_common_error}"這一錯誤類型進行專項練習
    3. 透過反覆練習相關題目來鞏固理解"""
        
        return summary
