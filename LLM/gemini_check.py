#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick check for Gemini connectivity (Vertex AI or Google Generative AI).
Reads env via dotenv and tries a small generation.
"""
import os
from dotenv import load_dotenv

load_dotenv()

provider = os.getenv("LLM_PROVIDER", "generativeai").lower()
api_key = os.getenv("GOOGLE_API_KEY", "")
model_name = os.getenv("GENERATIVEAI_MODEL_NAME", "gemini-2.0-flash")

print(f"Provider: {provider}")
print(f"API Key: {'***' + api_key[-5:] if api_key else 'NOT SET'}")
print(f"Model: {model_name}")

if provider == "generativeai":
    if not api_key:
        print("❌ GOOGLE_API_KEY not set. Get one from https://aistudio.google.com/app/apikey")
        raise SystemExit(1)
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        print("✅ Google Generative AI configured")
    except Exception as e:
        print(f"❌ Failed to configure Google Generative AI: {e}")
        raise
    
    try:
        model = genai.GenerativeModel(model_name)
        resp = model.generate_content("請用一句話介紹你自己，並說明你能提供什麼學習幫助。",
                                     generation_config=genai.types.GenerationConfig(
                                         temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
                                         max_output_tokens=int(os.getenv("LLM_MAX_TOKENS", "256"))
                                     ))
        print("✅ Gemini 回覆：")
        print((resp.text or "").strip())
    except Exception as e:
        print(f"❌ Gemini generation failed: {e}")
        raise
else:
    print(f"❌ Provider '{provider}' not supported in this check. Use 'generativeai'.")
    raise SystemExit(1)
    print(f"❌ Gemini generation failed: {e}")
    raise
