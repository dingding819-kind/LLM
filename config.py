"""
Configuration file for Knowledge Fuel Station
"""
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
# Provider can be: "openai", "vertexai", or "generativeai"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "vertexai")

# Service Account JSON file path for Vertex AI
SERVICE_ACCOUNT_JSON_PATH = os.getenv(
    "SERVICE_ACCOUNT_JSON_PATH",
    "knowledgefuelstation-d1be8ee129d2.json"
)

# Load service account credentials if available
SERVICE_ACCOUNT_INFO = None
if os.path.exists(SERVICE_ACCOUNT_JSON_PATH):
    try:
        with open(SERVICE_ACCOUNT_JSON_PATH, 'r') as f:
            SERVICE_ACCOUNT_INFO = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load service account JSON: {e}")

# OpenAI settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")

# Vertex AI (Gemini) settings
# Auto-detect project ID from service account if available
if SERVICE_ACCOUNT_INFO and "project_id" in SERVICE_ACCOUNT_INFO:
    GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", SERVICE_ACCOUNT_INFO["project_id"])
else:
    GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID", "")

GOOGLE_LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-2.0-flash")

# Google Generative AI settings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GENERATIVEAI_MODEL_NAME = os.getenv("GENERATIVEAI_MODEL_NAME", "gemini-2.0-flash")

TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "1000"))

# Learning Configuration
SUBJECTS = [
    "數學",
    "英語",
    "自然",
    "社會",
    "語文"
]

# Subject-specific topic catalogs to diversify question coverage
SUBJECT_TOPICS = {
    "數學": [
        "數與數線", "數與數線／數的大小與絕對值", "數與數線／整數的加減運算", 
        "數與數線/整數的四則運算/應用問題", "整數的四則運算", "整數的四則運算/應用問題",
        "負數與數線", "一元一次方程式", "一元一次方程式／以符號代表數", 
        "一元一次方程式/解一元一次方程式(含等量公理)", "數學／第1冊／一元一次方程式／式子的化簡",
        "分數的運算／正負分數的加減運算", "分數的運算／正負分數的乘除與四則運算", 
        "分數的運算／最大公因數與最小公倍數", "指數律與科學記號"
    ],
    "英語": [
        "時態與語法", "詞彙搭配", "閱讀理解", "完形填空",
        "翻譯與改錯", "寫作技巧", "口語表達"
    ],
    "自然": [
        "元素與化合物", "化學方程式", "酸鹼與鹽", "有機化學基礎"
    ],
    "社會": [
        "歷史:臺灣的歷史-史前時代", "歷史:臺灣的歷史-國際競爭時期", 
        "歷史:臺灣的歷史-鄭氏治臺時期", "歷史:臺灣的歷史-清領時代前期", "歷史:臺灣的歷史-清領時代後期",
        "地理:臺灣的自然環境-地圖運用", "地理:臺灣的自然環境-相對位置", 
        "地理:臺灣的自然環境-地形", "地理:臺灣的自然環境-海岸與離島",
        "地理:臺灣的自然環境-天氣", "地理:臺灣的自然環境-天氣與氣候", "地理:臺灣的自然環境-氣候",
        "地理:臺灣的自然環境-水文", "地理:臺灣的自然環境-生態系統與環境問題",
        "公民:個人成長與群體-自我與成長", "公民:個人成長與群體-性別關係", 
        "公民:個人成長與群體-家庭生活", "公民:個人成長與群體-學校生活", 
        "公民:個人成長與群體-社區生活", "公民:個人成長與群體-生命教育"
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
