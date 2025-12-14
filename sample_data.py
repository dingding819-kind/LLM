"""
Sample data for testing Knowledge Fuel Station
"""

SAMPLE_STUDENTS = [
    {
        "student_id": "S001",
        "name": "李明",
        "grade": "初二",
        "weak_subjects": ["數學", "英語"],
        "learning_style": "visual",
        "recent_scores": {
            "數學": 72,
            "英語": 68,
            "語文": 82,
            "物理": 75
        },
        "recent_topics": ["代數基礎", "英文時態"]
    },
    {
        "student_id": "S002",
        "name": "王芳",
        "grade": "初一",
        "weak_subjects": ["物理", "化學"],
        "learning_style": "kinesthetic",
        "recent_scores": {
            "物理": 60,
            "化學": 58,
            "數學": 85,
            "語文": 88
        },
        "recent_topics": ["基本力學", "元素週期表"]
    }
]

SAMPLE_QUESTIONS = [
    {
        "id": 1,
        "subject": "數學",
        "difficulty": "medium",
        "question": "求方程 2x + 5 = 13 的解",
        "standard_answer": "x = 4"
    },
    {
        "id": 2,
        "subject": "英語",
        "difficulty": "easy",
        "question": "將句子改為過去式：'He goes to school every day'",
        "standard_answer": "He went to school every day"
    },
    {
        "id": 3,
        "subject": "物理",
        "difficulty": "hard",
        "question": "一個物體從高度h處自由落下，不計空氣阻力。求它撞擊地面時的速度。",
        "standard_answer": "v = √(2gh)"
    }
]

SAMPLE_LEARNING_RECORDS = [
    {
        "student_id": "S001",
        "question_id": 1,
        "subject": "數學",
        "correct": True,
        "time_spent": 120,
        "score": 100
    },
    {
        "student_id": "S001",
        "question_id": 2,
        "subject": "英語",
        "correct": False,
        "time_spent": 180,
        "score": 0
    }
]
