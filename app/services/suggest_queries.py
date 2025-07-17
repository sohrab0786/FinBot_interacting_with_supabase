# app/services/suggest_queries.py

from typing import List

SAMPLE_QUERIES = [
    "What was Apple's revenue in 2022?",
    "Show me the net income and gross profit for Microsoft for the last 3 years.",
    "Give me the ebit margin of Tesla for FY2021.",
    "What is Google's gross profit margin over the past 2 years?",
    "Show the quarterly revenue for Amazon in 2023.",
]

def suggest_queries(original_question: str) -> List[dict]:
    return [{
        "agent": "suggestion",
        "message": (
            "Your query seems incomplete or unclear. Please include a valid company name or ticker, "
            "and mention at least one financial metric.\n\n"
            "Here are some example queries you can try:"
        ),
        "suggestions": SAMPLE_QUERIES,
        "original_question": original_question
    }]
