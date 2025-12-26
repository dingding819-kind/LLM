"""
Web API Server for Knowledge Fuel Station
提供 AI 詳解功能給前端使用
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# 確保可以 import 專案模組
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 初始化 Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    print("✅ Gemini API 已初始化")
else:
    model = None
    print("⚠️ GOOGLE_API_KEY 未設定，AI 詳解功能將無法使用")


@app.route('/api/explain', methods=['POST'])
def explain():
    """
    生成 AI 詳解
    
    請求格式:
    {
        "question": "題目內容",
        "options": {"A": "選項A", "B": "選項B", ...},
        "correct_answer": "B",
        "student_answer": "A",
        "subject": "數學",
        "scope": "一元一次方程式"  (可選)
    }
    """
    if not model:
        return jsonify({
            "success": False,
            "error": "AI 服務未初始化"
        }), 500
    
    try:
        data = request.json
        
        question = data.get('question', '')
        options = data.get('options', {})
        correct_answer = data.get('correct_answer', '')
        student_answer = data.get('student_answer', '')
        subject = data.get('subject', '')
        scope = data.get('scope', '')
        
        # 構建選項文字
        options_text = "\n".join([f"{k}. {v}" for k, v in options.items()])
        
        # 構建 prompt
        prompt = f"""你是一位專業的{subject}老師，請幫助學生理解這道題目。

題目：{question}

選項：
{options_text}

正確答案：{correct_answer}
學生選擇：{student_answer}
{'範圍：' + scope if scope else ''}

請用簡潔親切的語氣，為這位學生提供詳細解釋：
1. 首先說明為什麼學生的答案是錯的（簡短說明錯誤原因）
2. 然後解釋正確答案的思路和原理
3. 最後給一個小提示，幫助學生記住這個知識點

請用繁體中文回答，語氣要友善鼓勵，像是在跟學生對話一樣。回答不要太長，控制在 150 字以內。"""

        # 呼叫 Gemini API
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500,
            )
        )
        
        explanation = response.text.strip()
        
        return jsonify({
            "success": True,
            "explanation": explanation
        })
        
    except Exception as e:
        print(f"Error generating explanation: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health():
    """健康檢查"""
    return jsonify({
        "status": "ok",
        "ai_enabled": model is not None
    })


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚀 知識加油站 API Server")
    print("=" * 50)
    print(f"API 服務運行於: http://localhost:5001")
    print(f"AI 功能: {'✅ 已啟用' if model else '❌ 未啟用'}")
    print("=" * 50 + "\n")
    
    app.run(host='0.0.0.0', port=5001, debug=True)
