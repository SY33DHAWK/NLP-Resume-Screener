from typing import Dict, List


# ── Skill Priority Tiers ───────────────────────────────────────
# Defines how critical each skill category is
SKILL_PRIORITY = {
    "programming_languages": "critical",
    "ml_frameworks":         "critical",
    "data_science":          "important",
    "data_tools":            "important",
    "databases":             "moderate",
    "cloud_devops":          "moderate",
    "soft_skills":           "nice_to_have"
}

PRIORITY_LABELS = {
    "critical":     "🔴 Critical",
    "important":    "🟠 Important",
    "moderate":     "🟡 Moderate",
    "nice_to_have": "🟢 Nice to Have"
}


# ── Core Gap Analysis ──────────────────────────────────────────

def analyze_skill_gaps(
    resume_skills: Dict[str, List[str]],
    jd_skills: Dict[str, List[str]]
) -> Dict:
    """
    Compares resume skills vs JD skills category by category.
    Returns matched, missing, and extra skills with priorities.
    """
    matched_skills  = {}
    missing_skills  = {}
    extra_skills    = {}

    # Get all categories from both
    all_categories = set(list(resume_skills.keys()) +
                         list(jd_skills.keys()))

    for category in all_categories:
        resume_set = set(resume_skills.get(category, []))
        jd_set     = set(jd_skills.get(category, []))

        matched = resume_set.intersection(jd_set)
        missing = jd_set - resume_set      # in JD but not resume
        extra   = resume_set - jd_set      # in resume but not JD

        if matched:
            matched_skills[category] = list(matched)
        if missing:
            missing_skills[category] = list(missing)
        if extra:
            extra_skills[category] = list(extra)

    return {
        "matched": matched_skills,
        "missing": missing_skills,
        "extra":   extra_skills
    }


def prioritize_gaps(missing_skills: Dict[str, List[str]]) -> List[Dict]:
    """
    Takes missing skills and ranks them by priority.
    Returns a sorted list — critical gaps first.
    """
    priority_order = {
        "critical":     0,
        "important":    1,
        "moderate":     2,
        "nice_to_have": 3
    }

    gaps = []
    for category, skills in missing_skills.items():
        priority = SKILL_PRIORITY.get(category, "nice_to_have")
        gaps.append({
            "category": category,
            "skills":   skills,
            "priority": priority,
            "label":    PRIORITY_LABELS[priority]
        })

    # Sort by priority — critical first
    gaps.sort(key=lambda x: priority_order[x["priority"]])
    return gaps


def compute_category_coverage(
    resume_skills: Dict[str, List[str]],
    jd_skills: Dict[str, List[str]]
) -> List[Dict]:
    """
    For each skill category in the JD,
    compute what % the resume covers.
    Useful for radar/bar chart in UI.
    """
    coverage = []

    for category, jd_skill_list in jd_skills.items():
        if not jd_skill_list:
            continue

        resume_set = set(resume_skills.get(category, []))
        jd_set     = set(jd_skill_list)
        matched    = resume_set.intersection(jd_set)

        pct = round(len(matched) / len(jd_set) * 100, 1)

        coverage.append({
            "category":      category,
            "required":      list(jd_set),
            "matched":       list(matched),
            "coverage_pct":  pct,
            "priority":      SKILL_PRIORITY.get(category, "nice_to_have"),
            "label":         PRIORITY_LABELS.get(
                                SKILL_PRIORITY.get(
                                    category, "nice_to_have"), "🟢 Nice to Have"
                             )
        })

    # Sort by coverage ascending — worst gaps first
    coverage.sort(key=lambda x: x["coverage_pct"])
    return coverage


def generate_gap_summary(gap_report: Dict) -> str:
    """
    Generates a plain English summary
    of the gap analysis for display in UI.
    """
    missing = gap_report.get("missing", {})
    matched = gap_report.get("matched", {})

    total_missing = sum(len(v) for v in missing.values())
    total_matched = sum(len(v) for v in matched.values())
    total         = total_missing + total_matched

    if total == 0:
        return "No skills data found to analyze."

    match_pct = round(total_matched / total * 100)

    # Build summary text
    lines = []
    lines.append(
        f"You match {total_matched} out of {total} required skills ({match_pct}%)."
    )

    if total_missing == 0:
        lines.append("Great news — no critical skill gaps detected!")
    else:
        lines.append(
            f"You are missing {total_missing} skills mentioned in the job description."
        )

        # Highlight critical missing
        critical_missing = missing.get("programming_languages", []) + \
                           missing.get("ml_frameworks", [])
        if critical_missing:
            lines.append(
                f"Critical gaps to address: {', '.join(critical_missing)}."
            )

    return " ".join(lines)


def run_full_gap_analysis(
    resume_skills: Dict[str, List[str]],
    jd_skills: Dict[str, List[str]]
) -> Dict:
    """
    Master function — runs complete gap analysis
    and returns everything in one unified report.
    """
    # Core gap analysis
    gap_report = analyze_skill_gaps(resume_skills, jd_skills)

    # Prioritized missing skills
    prioritized = prioritize_gaps(gap_report["missing"])

    # Category coverage percentages
    coverage = compute_category_coverage(resume_skills, jd_skills)

    # Plain English summary
    summary = generate_gap_summary(gap_report)

    return {
        "gap_report":   gap_report,
        "prioritized_gaps": prioritized,
        "coverage":     coverage,
        "summary":      summary
    }