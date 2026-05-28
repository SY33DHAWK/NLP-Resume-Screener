import streamlit as st


def render_score_card(score: float, label: str):
    """Renders the big match score card."""
    if score >= 80:
        color = "#10B981"   # green
    elif score >= 60:
        color = "#F59E0B"   # amber
    elif score >= 40:
        color = "#F97316"   # orange
    else:
        color = "#EF4444"   # red

    st.markdown(
        f"""
        <div style="
            background-color: #1E293B;
            border: 2px solid {color};
            border-radius: 16px;
            padding: 32px;
            text-align: center;
            margin: 16px 0;
        ">
            <h1 style="color: {color}; font-size: 64px; margin: 0;">
                {score}%
            </h1>
            <h3 style="color: #F1F5F9; margin: 8px 0 0 0;">
                {label}
            </h3>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_score_breakdown(
    tfidf: float,
    semantic: float,
    skill: float
):
    """Renders the three individual score metrics."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Keyword Match",
            value=f"{tfidf}%",
            help="How many exact keywords from the JD appear in your resume"
        )
    with col2:
        st.metric(
            label="Semantic Match",
            value=f"{semantic}%",
            help="How similar the overall meaning is between resume and JD"
        )
    with col3:
        st.metric(
            label="Skill Match",
            value=f"{skill}%",
            help="Percentage of required skills found in your resume"
        )


def render_skill_chips(skills: list, color: str = "#6366F1"):
    """Renders skills as colored chips/badges."""
    chips_html = ""
    for skill in skills:
        chips_html += f"""
        <span style="
            background-color: {color}22;
            border: 1px solid {color};
            color: #F1F5F9;
            padding: 4px 12px;
            border-radius: 20px;
            margin: 4px;
            display: inline-block;
            font-size: 13px;
        ">{skill}</span>
        """
    st.markdown(chips_html, unsafe_allow_html=True)


def render_gap_item(gap: dict):
    """Renders a single gap item with priority label."""
    priority_colors = {
        "critical":     "#EF4444",
        "important":    "#F97316",
        "moderate":     "#F59E0B",
        "nice_to_have": "#10B981"
    }
    color = priority_colors.get(gap["priority"], "#6366F1")

    st.markdown(
        f"""
        <div style="
            background: #1E293B;
            border-left: 4px solid {color};
            padding: 12px 16px;
            border-radius: 8px;
            margin: 8px 0;
        ">
            <span style="color: {color}; font-weight: bold;">
                {gap['label']}
            </span>
            <span style="color: #94A3B8; margin-left: 8px;">
                {gap['category'].replace('_', ' ').title()}
            </span>
            <br/>
            <span style="color: #F1F5F9;">
                {', '.join(gap['skills'])}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_coverage_bar(category: str, pct: float, label: str):
    """Renders a coverage progress bar per skill category."""
    if pct >= 75:
        color = "#10B981"
    elif pct >= 50:
        color = "#F59E0B"
    elif pct >= 25:
        color = "#F97316"
    else:
        color = "#EF4444"

    st.markdown(
        f"""
        <div style="margin: 8px 0;">
            <div style="
                display: flex;
                justify-content: space-between;
                margin-bottom: 4px;
            ">
                <span style="color: #F1F5F9; font-size: 13px;">
                    {category.replace('_', ' ').title()}
                </span>
                <span style="color: {color}; font-size: 13px;">
                    {pct}%
                </span>
            </div>
            <div style="
                background: #334155;
                border-radius: 8px;
                height: 8px;
                width: 100%;
            ">
                <div style="
                    background: {color};
                    border-radius: 8px;
                    height: 8px;
                    width: {pct}%;
                "></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_feedback_section(title: str, content: str, icon: str = "💡"):
    """Renders a single AI feedback section."""
    if not content.strip():
        return

    st.markdown(
        f"""
        <div style="
            background: #1E293B;
            border-radius: 12px;
            padding: 20px;
            margin: 12px 0;
        ">
            <h4 style="color: #6366F1; margin: 0 0 12px 0;">
                {icon} {title}
            </h4>
            <div style="color: #F1F5F9; line-height: 1.6;">
                {content.replace(chr(10), '<br/>')}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )