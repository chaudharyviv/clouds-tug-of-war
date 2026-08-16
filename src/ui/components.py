import html
import streamlit as st
from src.models.combatant import Champion
from src.models.battlefield import Battlefield
from src.models.battle import BattleResult
from src.config import BATTLE_DIMENSIONS

# The three dimensions surfaced on each fighter's stat block in the VS row.
# Kept small on purpose (spec 2.3: readable subset, not all ten every time).
STAT_BLOCK_DIMENSIONS = [
    "AI / GPU War Power",
    "Economic Blood Cost",
    "Raw Scale & Gravity",
]


def _render_html(fragment: str):
    # Streamlit's markdown treats lines indented 4+ spaces as a code block,
    # which breaks nested <div> HTML — collapse everything to one line first.
    st.markdown(" ".join(line.strip() for line in fragment.strip().splitlines()), unsafe_allow_html=True)


def _stat_rows(scorecard, dimensions):
    rows = []
    for dim in dimensions:
        score = scorecard.scores.get(dim, 50.0) if scorecard else 50.0
        rows.append((dim, max(0.0, min(100.0, score))))
    return rows


def render_battlefield_banner(battlefield: Battlefield):
    """
    Renders the terrain banner: eyebrow, mythic name, and a plain one-line
    statement of what it rewards/who suffers — set before the fight starts.
    """
    _render_html(f"""
        <div class="battlefield-banner">
            <div class="eyebrow">Battlefield</div>
            <div class="name">{html.escape(battlefield.name)}</div>
            <div class="terrain">
                Favors <strong style="color:var(--ember);">{html.escape(battlefield.rewards)}</strong>
                &nbsp;&middot;&nbsp; Suffers <strong style="color:var(--blood);">{html.escape(battlefield.suffers)}</strong>
            </div>
            <div class="rule"></div>
        </div>
    """)


def render_vs_row(champion_a: Champion, champion_b: Champion, result: BattleResult = None):
    """
    Renders the two fighter panels with diagonal-cut edges and a VS mark
    between them, matching the fight-card mockup. Victor/defeated states
    (glow / desaturate) are redundant with the verdict strip on purpose.
    """
    state_a, state_b = "", ""
    if result:
        if result.winner_name == champion_a.name:
            state_a, state_b = "victor", "defeated"
        else:
            state_a, state_b = "defeated", "victor"

    scorecard_a = result.scorecards.get(champion_a.name) if result else None
    scorecard_b = result.scorecards.get(champion_b.name) if result else None

    def fighter_html(champion: Champion, side: str, state: str, scorecard):
        prof = champion.mythic_profile
        epithet = prof.epithet if prof else "The Challenger"
        stat_rows = _stat_rows(scorecard, STAT_BLOCK_DIMENSIONS)
        stats_html = "".join(
            f'<div class="stat-row"><div class="stat-label">{html.escape(dim)}</div>'
            f'<div class="bar-track"><div class="bar-fill" style="width:{score:.0f}%"></div></div></div>'
            for dim, score in stat_rows
        )
        return (
            f'<div class="fighter {side} {state}">'
            f'<div class="faction-tag">{html.escape(champion.faction.value)}</div>'
            f'<div class="epithet">{html.escape(epithet)}</div>'
            f'<div class="champ-name">{html.escape(champion.name)}</div>'
            f'<div class="stat-block">{stats_html}</div>'
            f'</div>'
        )

    fragment = (
        '<div class="vs-row">'
        + fighter_html(champion_a, "left", state_a, scorecard_a)
        + '<div class="vs-center"><div class="vs-crack"></div><div class="vs-mark">VS</div></div>'
        + fighter_html(champion_b, "right", state_b, scorecard_b)
        + '</div>'
    )
    _render_html(fragment)


def render_weapons_and_flaws(champion_a: Champion, champion_b: Champion):
    """
    Renders the mythic weapons/curses list for both fighters side by side,
    below the VS row (kept separate from the stat block so that panel stays
    uncluttered and matches the mockup's clean fighter cards).
    """
    col1, col2 = st.columns(2)
    for col, champion, align in ((col1, champion_a, "left"), (col2, champion_b, "right")):
        prof = champion.mythic_profile
        weapons = "".join(f"<li>{html.escape(w)}</li>" for w in prof.weapons) if prof else "<li>Awaiting forge...</li>"
        flaws = "".join(f"<li>{html.escape(f)}</li>" for f in prof.fatal_flaws) if prof else "<li>Awaiting analysis...</li>"
        pad_side = "left" if align == "left" else "right"
        list_style = "list-style-position:inside;" if align == "right" else ""
        with col:
            _render_html(
                f'<div style="text-align:{align};">'
                f'<div class="stat-label" style="margin-top:8px;">Weapons of strength</div>'
                f'<ul style="padding-{pad_side}:20px; color:var(--bone); margin:6px 0; {list_style}">{weapons}</ul>'
                f'<div class="stat-label">Fatal curses</div>'
                f'<ul style="padding-{pad_side}:20px; color:var(--blood); margin:6px 0; {list_style}">{flaws}</ul>'
                f'</div>'
            )


def render_prophecy(champion_a: Champion, champion_b: Champion):
    """
    Renders the short mythic prophecy line above the verdict strip — pure
    flavor text, not a factual claim, so it stays outside the Fidelity Law.
    """
    epithet_a = champion_a.mythic_profile.epithet if champion_a.mythic_profile else champion_a.name
    epithet_b = champion_b.mythic_profile.epithet if champion_b.mythic_profile else champion_b.name
    _render_html(
        '<div class="prophecy">'
        f'{html.escape(champion_a.name)}, {html.escape(epithet_a)}.<br>'
        f'{html.escape(champion_b.name)}, {html.escape(epithet_b)}.<br>'
        'Only one leaves the cluster unburnt.'
        '</div>'
    )


def render_score_totals(result: BattleResult, champion_a: Champion, champion_b: Champion):
    """
    Renders the two combatants' actual battle-score totals side by side —
    the number that Second Wind moves, so activating it has something
    visible to change.
    """
    a_win = result.winner_name == champion_a.name
    left_class = "dim-val win" if a_win else "dim-val"
    right_class = "dim-val right-val win" if not a_win else "dim-val right-val"
    _render_html(f"""
        <div class="dim-row" style="margin-top:4px;">
            <div class="{left_class}" style="font-size:20px;">{result.score_a:.1f}</div>
            <div class="dim-name" style="margin-bottom:0;">Battle score</div>
            <div class="{right_class}" style="font-size:20px;">{result.score_b:.1f}</div>
        </div>
    """)


def render_verdict_strip(verdict_text: str):
    """
    Renders the non-negotiable, plain-language verdict — the myth never
    replaces this. Sticky and oversized on purpose: this is the one element
    that must survive a 3-second glance (spec success criterion #6), so it
    stays pinned and legible while the reader scrolls through the theater
    below it.
    """
    _render_html(
        '<div class="verdict-strip">'
        '<div class="verdict-label">Verdict</div>'
        f'<div class="verdict-text">{html.escape(verdict_text)}</div>'
        '</div>'
    )


def render_scorecard(result: BattleResult, champion_a: Champion, champion_b: Champion, battlefield: Battlefield = None):
    """
    Renders dimension-by-dimension tug-of-war bars, one scroll below the
    theater above it, so the numeric truth stays inspectable. Each dimension
    is tagged with the battlefield's weight for it, since that weight — not
    the raw score alone — is what actually decided the fight.
    """
    scorecard_a = result.scorecards.get(champion_a.name)
    scorecard_b = result.scorecards.get(champion_b.name)

    if not scorecard_a or not scorecard_b:
        st.warning("Scorecard data missing.")
        return

    weights = battlefield.active_dimensions() if battlefield else {}

    rows_html = ""
    for dim in BATTLE_DIMENSIONS:
        if dim not in scorecard_a.scores and dim not in scorecard_b.scores:
            continue
        score_a = scorecard_a.scores.get(dim, 50.0)
        score_b = scorecard_b.scores.get(dim, 50.0)
        total = score_a + score_b
        pct_a = (score_a / total * 100) if total > 0 else 50.0

        left_class = "dim-val win" if score_a >= score_b else "dim-val"
        right_class = "dim-val right-val win" if score_b > score_a else "dim-val right-val"

        weight = weights.get(dim)
        weight_html = f' <span class="dim-weight">&times;{weight:.1f}</span>' if weight else ""

        rows_html += (
            '<div class="dim-row">'
            f'<div class="{left_class}">{score_a:.0f}</div>'
            f'<div class="tug-track"><div class="tug-fill" style="width:{pct_a:.0f}%"></div></div>'
            f'<div class="{right_class}">{score_b:.0f}</div>'
            '</div>'
            f'<div class="dim-name">{html.escape(dim)}{weight_html}</div>'
        )

    _render_html(
        '<div class="scorecard">'
        '<div class="scorecard-title">Tug-of-war &mdash; dimension pulls</div>'
        f'{rows_html}'
        '</div>'
    )
