"""
Report Generator - Generate learning reports and insights
"""
from typing import Dict, List, Optional
from datetime import datetime


class ReportGenerator:
    """Generate comprehensive learning reports"""

    @staticmethod
    def generate_learning_report(
        student_name: str,
        progress_summary: Dict
    ) -> str:
        """
        Generate a comprehensive learning report
        
        Args:
            student_name: Student's name
            progress_summary: Progress summary from DataProcessor
            
        Returns:
            Formatted report string
        """
        report = f"""
{'='*50}
學習進度報告
{'='*50}

學生姓名：{student_name}
生成日期：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

【整體表現】
總練習題數：{progress_summary['total_questions']}
正確答案數：{progress_summary['correct_answers']}
正確率：{progress_summary['accuracy']:.1f}%

"""
        
        if progress_summary['subjects']:
            report += "【科目分析】\n"
            for subject, data in progress_summary['subjects'].items():
                report += f"\n{subject}:\n"
                report += f"  練習題數：{data['total']}\n"
                report += f"  正確數：{data['correct']}\n"
                report += f"  正確率：{data['accuracy']:.1f}%\n"
        
        if progress_summary['weak_areas']:
            report += "\n【需要改進的科目】(按優先級)\n"
            for i, subject in enumerate(progress_summary['weak_areas'], 1):
                report += f"{i}. {subject}\n"
        
        # Concepts to reinforce (from recent errors)
        concepts = progress_summary.get('concepts_to_reinforce', [])
        if concepts:
            report += "\n【需要補強的觀念】\n"
            concept_count = {}
            for concept in concepts:
                if concept:
                    concept_count[concept] = concept_count.get(concept, 0) + 1
            sorted_concepts = sorted(concept_count.items(), key=lambda x: x[1], reverse=True)
            for concept, count in sorted_concepts[:5]:
                marker = "⚠️" if count >= 2 else "•"
                extra = f" (出現 {count} 次)" if count > 1 else ""
                report += f"{marker} {concept}{extra}\n"
        
        report += "\n" + "="*50 + "\n"
        return report

    @staticmethod
    def generate_performance_chart(
        progress_summary: Dict,
        text_based: bool = True
    ) -> str:
        """
        Generate performance visualization
        
        Args:
            progress_summary: Progress summary dictionary
            text_based: If True, use text-based chart
            
        Returns:
            Chart representation
        """
        if not text_based:
            # Could integrate with matplotlib or plotly here
            return ""
        
        # Text-based bar chart
        chart = "【正確率對比】\n"
        
        max_subject_len = 0
        if progress_summary['subjects']:
            max_subject_len = max(len(s) for s in progress_summary['subjects'].keys())
        
        for subject, data in sorted(
            progress_summary['subjects'].items(),
            key=lambda x: x[1]['accuracy'],
            reverse=True
        ):
            accuracy = data['accuracy']
            bar_length = int(accuracy / 5)  # Scale for readability
            bar = "█" * bar_length + "░" * (20 - bar_length)
            
            chart += f"{subject:<{max_subject_len}} | {bar} {accuracy:.1f}%\n"
        
        return chart

    @staticmethod
    def generate_recommendations(
        progress_summary: Dict,
        error_patterns: Optional[Dict] = None
    ) -> str:
        """
        Generate personalized learning recommendations
        
        Args:
            progress_summary: Progress summary
            error_patterns: Error pattern analysis (optional)
            
        Returns:
            Recommendations text
        """
        recommendations = "【學習建議】\n\n"
        
        accuracy = progress_summary['accuracy']
        
        if accuracy < 60:
            recommendations += "⚠️ 整體表現需要顯著改進\n"
            recommendations += "   • 建議每天花更多時間學習基礎知識\n"
            recommendations += "   • 針對正確率最低的科目進行重點複習\n"
            recommendations += "   • 考慮尋求額外的學習資源或輔導\n\n"
        elif accuracy < 75:
            recommendations += "📈 表現良好，但仍有改進空間\n"
            recommendations += "   • 繼續加強弱科目的學習\n"
            recommendations += "   • 進行更多類似錯題的練習\n"
            recommendations += "   • 逐步增加題目難度\n\n"
        else:
            recommendations += "🌟 表現優秀，繼續保持\n"
            recommendations += "   • 可以嘗試更高難度的題目\n"
            recommendations += "   • 幫助其他同學學習相關知識點\n\n"
        
        # Subject-specific recommendations
        if progress_summary['weak_areas']:
            recommendations += "針對薄弱科目的建議：\n"
            for i, subject in enumerate(progress_summary['weak_areas'][:3], 1):
                if subject in progress_summary['subjects']:
                    data = progress_summary['subjects'][subject]
                    recommendations += f"\n{i}. {subject} (正確率: {data['accuracy']:.1f}%)\n"
                    recommendations += f"   • 進行{max(5, 10-int(data['accuracy']/10))}次練習\n"
                    recommendations += f"   • 重點複習基礎知識\n"
                    recommendations += f"   • 在練習中記錄常見錯誤\n"
        
        return recommendations

    @staticmethod
    def generate_comparison_report(
        student_name: str,
        current_summary: Dict,
        previous_summary: Optional[Dict] = None
    ) -> str:
        """
        Generate progress comparison report
        
        Args:
            student_name: Student's name
            current_summary: Current progress summary
            previous_summary: Previous progress summary for comparison
            
        Returns:
            Comparison report string
        """
        report = f"\n【進度對比報告】- {student_name}\n"
        report += "="*40 + "\n"
        
        if not previous_summary:
            report += "（無以前的數據用於比較）\n"
            return report
        
        # Calculate improvements
        current_accuracy = current_summary['accuracy']
        previous_accuracy = previous_summary['accuracy']
        improvement = current_accuracy - previous_accuracy
        
        report += f"\n上次正確率：{previous_accuracy:.1f}%\n"
        report += f"現在正確率：{current_accuracy:.1f}%\n"
        
        if improvement > 0:
            report += f"✅ 進步：+{improvement:.1f}%\n"
        elif improvement < 0:
            report += f"⚠️ 下降：{improvement:.1f}%\n"
        else:
            report += f"→ 無變化\n"
        
        report += "\n" + "="*40 + "\n"
        return report

    @staticmethod
    def export_report_to_file(
        report_content: str,
        filename: str
    ) -> bool:
        """
        Export report to file
        
        Args:
            report_content: Report content to save
            filename: Output filename
            
        Returns:
            True if successful
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            return True
        except Exception as e:
            print(f"Error exporting report: {e}")
            return False
