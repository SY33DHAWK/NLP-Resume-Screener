import os
from groq import Groq
from dotenv import load_dotenv
from typing import Dict, List

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Best free model on Groq for this task
MODEL = "llama-3.3-70b-versatile"


# ── Prompt Builder ─────────────────────────────────────────────

def build_prompt(
    match_score: float,
    match_label: str,
    summary: str,
    prioritized_gaps: List[Dict],
    matched_skills: Dict,
    job_title: str = "the target role"
) -> str:
    """
    Builds a structured, context-rich prompt
    for the LLM to generate useful feedback.
    """

    # Flatten matched skills
    matched_flat = []
    for category, skills in matched_skills.items():
        matched_flat.extend(skills)

    # Sort gaps by priority
    critical_gaps  = []
    important_gaps = []
    moderate_gaps  = []

    for gap in prioritized_gaps:
        if gap["priority"] == "critical":
            critical_gaps.extend(gap["skills"])
        elif gap["priority"] == "important":
            important_gaps.extend(gap["skills"])
        elif gap["priority"] == "moderate":
            moderate_gaps.extend(gap["skills"])

    prompt = f"""
You are an expert career coach and technical recruiter with
10+ years of experience in the tech industry.

A candidate has just had their resume analyzed against a
job description for: {job_title}

Here is their analysis report:

MATCH SCORE: {match_score}% — {match_label}

SUMMARY: {summary}

SKILLS THEY ALREADY HAVE:
{', '.join(matched_flat) if matched_flat else 'None detected'}

CRITICAL SKILL GAPS (must fix):
{', '.join(critical_gaps) if critical_gaps else 'None'}

IMPORTANT SKILL GAPS (should fix):
{', '.join(important_gaps) if important_gaps else 'None'}

MODERATE SKILL GAPS (nice to fix):
{', '.join(moderate_gaps) if moderate_gaps else 'None'}

Based on this analysis, provide personalized feedback in
exactly this structure:

1. OVERALL ASSESSMENT (2-3 sentences)
   Honest assessment of where they stand for this role.

2. STRENGTHS TO HIGHLIGHT (3 bullet points)
   What they should emphasize in their resume and interview.

3. CRITICAL ACTION PLAN (bullet points)
   Specific, actionable steps to close the critical gaps.
   Include learning resources where relevant.

4. QUICK WINS (2-3 bullet points)
   Things they can add to their resume or portfolio fast
   to improve their chances immediately.

5. HONEST ADVICE (2-3 sentences)
   One piece of honest, direct career advice based on
   their current profile vs the role requirements.

Keep the tone encouraging but honest. Be specific,
not generic. Avoid filler advice like "keep learning."
    """
    return prompt.strip()


# ── Groq API Call ──────────────────────────────────────────────

def get_ai_feedback(
    match_score: float,
    match_label: str,
    summary: str,
    prioritized_gaps: List[Dict],
    matched_skills: Dict,
    job_title: str = "the target role"
) -> str:
    """
    Sends gap analysis to Groq LLaMA 3 and returns
    personalized career feedback.
    """
    prompt = build_prompt(
        match_score=match_score,
        match_label=match_label,
        summary=summary,
        prioritized_gaps=prioritized_gaps,
        matched_skills=matched_skills,
        job_title=job_title
    )

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert career coach and technical "
                        "recruiter. Give honest, specific, actionable "
                        "feedback. Never be generic."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"AI feedback unavailable at this time. Error: {str(e)}"


# ── Feedback Section Parser ────────────────────────────────────

def parse_feedback_sections(feedback_text: str) -> Dict[str, str]:
    """
    Parses LLM response into named sections
    for cleaner display in the Streamlit UI.
    """
    sections = {
        "overall_assessment": "",
        "strengths":          "",
        "action_plan":        "",
        "quick_wins":         "",
        "honest_advice":      ""
    }

    section_markers = {
        "overall_assessment": "1. OVERALL ASSESSMENT",
        "strengths":          "2. STRENGTHS TO HIGHLIGHT",
        "action_plan":        "3. CRITICAL ACTION PLAN",
        "quick_wins":         "4. QUICK WINS",
        "honest_advice":      "5. HONEST ADVICE"
    }

    lines = feedback_text.split("\n")
    current_section = None
    buffer = []

    for line in lines:
        matched_section = None
        for key, marker in section_markers.items():
            if marker in line.upper():
                matched_section = key
                break

        if matched_section:
            if current_section:
                sections[current_section] = "\n".join(buffer).strip()
            current_section = matched_section
            buffer = []
        else:
            if current_section:
                buffer.append(line)

    # Save last section
    if current_section:
        sections[current_section] = "\n".join(buffer).strip()

    return sections


# ── Master Function ────────────────────────────────────────────

def generate_full_feedback(
    similarity_result: Dict,
    gap_analysis: Dict,
    job_title: str = "the target role"
) -> Dict:
    """
    Master function — takes outputs from
    similarity.py and gap_analyzer.py directly
    and returns complete structured feedback.
    """
    raw_feedback = get_ai_feedback(
        match_score=similarity_result["final_score"],
        match_label=similarity_result["match_label"],
        summary=gap_analysis["summary"],
        prioritized_gaps=gap_analysis["prioritized_gaps"],
        matched_skills=gap_analysis["gap_report"]["matched"],
        job_title=job_title
    )

    parsed = parse_feedback_sections(raw_feedback)

    return {
        "raw_feedback":    raw_feedback,
        "parsed_sections": parsed,
        "job_title":       job_title
    }