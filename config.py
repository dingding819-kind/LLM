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
        "英語第一冊 語言學習結構內容 招呼語及專有名詞",
        "What 引導的問句及答句",
        "Be V 句型（肯定、否定、疑問），人稱代名詞主格，不定冠詞，指示詞（this, that）",
        "Who 引導的問句及答句",
        "祁使句，定冠詞 the",
        "Where 引導的問句及答句，問地方，場所介詞，介紹國家",
        "助動詞 can 的用法",
        "現在進行式",
        "基數（0–9），人稱代名詞複數，名詞單複數，these，those"
    ],
    "自然": [
        "時間與空間的量度",
        "物質是由微小的粒子所組成",
        "物質的三態與變化",
        "溶液與溶解度",
        "酸與鹼",
        "物質的分離與純化",
        "生物的基本單位—細胞",
        "生物的分類",
        "生物的生命現象",
        "生物的遺傳與變異",
        "生物與環境",
        "能量的形式與轉換",
        "力與運動",
        "地球的構造與變動",
        "天氣與氣候",
        "地球上的水",
        "地球上的生物",
        "地球的資源與永續發展"
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
        "雅量",
        "母親的教誨",
        "飲水思源",
        "生之歌選",
        "心囚",
        "月光餅",
        "音樂家與職籃明星",
        "不要怕失敗",
        "那默默的一群",
        "兒時記趣",
        "賣油翁",
        "王冕的少年時代",
        "論語選",
        "登鶴雀樓",
        "黃鶴樓送孟浩然之廣陵",
        "題西林壁",
        "楓橋夜泊",
        "夏夜"
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
