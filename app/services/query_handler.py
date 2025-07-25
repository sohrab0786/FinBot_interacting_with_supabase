# File: app/services/query_handler.py

from typing import Optional, List, Dict
from app.agents import financial, ratios, planner
from app.services.extract_metrics_llm import extract_metrics_llm, normalize_metrics_llm_output

async def query_handler(user_query: str, session_id: Optional[str] = None) -> List[Dict]:
    # Directly plan the steps needed to resolve the query
    raw_metrics = await extract_metrics_llm(user_query)
    print(f'raw metrics {raw_metrics}')
    metrics = normalize_metrics_llm_output(raw_metrics)
    if not metrics:
        return [{
            "agent": "suggestion",
            "message": "We couldn't recognize some of the financial metrics you mentioned.\nHere are some example queries you can try using supported metrics:",
            "suggestions": [
                "What was Apple's net income in 2022?",
                "Show me the cash and cash equivalents for Google for the last 2 years.",
                "How much was Tesla’s operating cash flow in FY2023?"
            ],
            "original_question": user_query
        }]
    plan_steps = await planner.plan(user_query, metrics)
    print("[DEBUG] planner returned:", plan_steps)
    results = []
    for step in plan_steps:
        agent = step.get("agent")
        # Remove 'agent' key before passing to the handler
        step_data = {k: v for k, v in step.items() if k != "agent"}
        if agent == "financial":
            result = await financial.run(**step_data)
            results.append({"agent": "financial", "content": result} if isinstance(result, list) else result)
        elif agent == "ratios":
            result = await ratios.run(**step_data)
            results.append({"agent": "ratios", "content": result} if isinstance(result, list) else result)
        elif agent == "suggestion":
            results.append(step)
        else:
            raise ValueError(f"Unknown agent: {agent}")
    return results
