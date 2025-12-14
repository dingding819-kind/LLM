"""
Configuration file for Knowledge Fuel Station
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
# Provider can be: "openai" or "vertexai"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "vertexai")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")

# Vertex AI (Gemini) settings
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "")
GOOGLE_LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash")

# Google Generative AI settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GENERATIVEAI_MODEL_NAME = os.getenv("GENERATIVEAI_MODEL_NAME", "gemini-2.0-flash")

TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1000"))

# Learning Configuration
SUBJECTS = [
    "數學",
    "英語",
    "物理",
    "化學",
    "歷史",
    "地理",
    "生物",
    "語文"
]

# Subject-specific topic catalogs to diversify question coverage
SUBJECT_TOPICS = {
    "數學": [
        "集合與運算", "代數方程", "函數與圖像", "幾何與證明",
        "概率與統計", "數列與遞推", "指數與對數", "不等式"
    ],
    "英語": [
        "時態與語法", "詞彙搭配", "閱讀理解", "完形填空",
        "翻譯與改錯", "寫作技巧", "口語表達"
    ],
    "物理": [
        "力學基礎", "電學與電路", "熱學", "光學", "波動與聲學"
    ],
    "化學": [
        "元素與化合物", "化學方程式", "酸鹼與鹽", "有機化學基礎"
    ],
    "歷史": [
        "中國古代史", "近代史", "世界史", "文化與制度"
    ],
    "地理": [
        "自然地理", "人文地理", "區域地理", "地理圖像判讀"
    ],
    "生物": [
        "細胞與組織", "遺傳與演化", "生態學", "人體生理"
    ],
    "語文": [
        "標點與語法", "文言文理解", "修辭與表達", "閱讀理解",
        "作文與寫作技巧", "詩詞鑑賞", "雅量"
    ]
}

# Subject name correction mapping (common typos)
SUBJECT_CORRECTIONS = {
    "樹學": "數學",
    "数学": "數學",
    "数學": "數學",
    "英文": "英語",
    "应语": "英語",
    "英语": "英語",
    "物里": "物理",
    "物理": "物理",
    "化学": "化學",
    "历史": "歷史",
    "地里": "地理",
    "生物": "生物",
    "语文": "語文",
    "國文": "語文",
    "中文": "語文"
}

# Difficulty Levels
DIFFICULTY_LEVELS = {
    "easy": 1,
    "medium": 2,
    "hard": 3
}

# Question Generation Settings
NUM_QUESTIONS_PER_SESSION = 5
QUESTIONS_PER_SUBJECT = 3
QUESTION_TIMEOUT = 30

# Error Analysis Settings
ERROR_ANALYSIS_DEPTH = "detailed"  # "simple" or "detailed"
INCLUDE_HINTS = True
INCLUDE_SIMILAR_PROBLEMS = True

# Learning Data Settings
STUDENT_DATA_DIR = "./students"
LEARNING_RECORDS_FILE = "learning_records.json"
PROGRESS_TRACKING = True

# Feedback Settings
FEEDBACK_LOOP_ENABLED = True
AUTO_ADJUST_DIFFICULTY = True
MIN_CONFIDENCE_SCORE = 0.5

# UI Settings
VERBOSE_OUTPUT = True
LANGUAGE = "zh"  # "zh" for Chinese, "en" for English
