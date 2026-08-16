import html
import streamlit as st
from src.config import DEFAULT_CHAMPIONS, BATTLEFIELDS
from src.models.combatant import Champion, FactionType
from src.models.battlefield import Battlefield
from src.models.battle import BattleResult, Chronicle, CodexEntry
from src.ui.components import (
    render_battlefield_banner,
    render_vs_row,
    render_weapons_and_flaws,
    render_prophecy,
    render_verdict_strip,
    render_score_totals,
    render_scorecard,
    render_tactical_advantage,
    render_decisive_blows
)
from src.services.orchestrator import ArenaOrchestrator
from src.services.codex import CodexService
import uuid
from datetime import datetime

class ArenaViews:
    def __init__(self):
        self.orchestrator = ArenaOrchestrator()

    def render_setup_view(self):
        """
        Renders the battle configuration form (fighters, fields, grudge matches).
        """
        st.markdown(
            "<h1 style='font-family: \"Cinzel Decorative\", serif; text-align: center; "
            "color: var(--ember); margin-bottom: 6px; text-shadow: 0 0 18px rgba(217,164,65,0.35);'>"
            "CLOUD BLOODBATH</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: var(--bone-dim); font-family: \"IBM Plex Mono\", monospace; "
            "letter-spacing: 0.04em; margin-bottom: 30px;'>Real cloud architecture. Mythic violence. "
            "No survivors left unscarred.</p>",
            unsafe_allow_html=True
        )

        # 1. Fighter selection mode — grudge match OR custom A vs B, never both at
        # once. Keeping these on mutually exclusive branches (rather than trying to
        # sync defaults into the same widgets) avoids Streamlit's keyed-widget state
        # sticking to a stale value when you switch between the two.
        st.markdown("### Summon your champions")
        fighter_mode = st.segmented_control(
            "Fighter selection mode",
            options=["Ancient Grudge", "Choose Your Champions"],
            default="Choose Your Champions",
            required=True,
            label_visibility="collapsed",
            key="fighter_mode"
        )

        grudge_matches = [
            ("GPU Rebellion (CoreWeave vs AWS)", ("CoreWeave", "AWS", "AI Training Killing Fields")),
            ("Edge Skirmish (Cloudflare vs GCP)", ("Cloudflare", "GCP", "Edge Ambush Terrain")),
            ("Sovereignty Clash (OVHcloud vs Azure)", ("OVHcloud", "Azure", "Sovereignty Fortress")),
            ("Cost Bleedout (Exadata vs AWS)", ("Exadata", "AWS", "Cost Wasteland")),
        ]
        all_champion_names = [c.name for c in DEFAULT_CHAMPIONS] + ["Forge a new challenger..."]
        default_field = "AI Training Killing Fields"

        if fighter_mode == "Ancient Grudge":
            selected_grudge_idx = st.selectbox(
                "Revisit a feud already written into legend:",
                range(len(grudge_matches)),
                format_func=lambda i: grudge_matches[i][0],
                key="grudge_idx"
            )
            grudge_a, grudge_b, default_field = grudge_matches[selected_grudge_idx][1]
            champion_a = next(c for c in DEFAULT_CHAMPIONS if c.name == grudge_a)
            champion_b = next(c for c in DEFAULT_CHAMPIONS if c.name == grudge_b)
            st.markdown(f"**{champion_a.name}** vs **{champion_b.name}**")

        else:
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**First Champion**")
                choice_a = st.selectbox(
                    "Summon your first champion:",
                    all_champion_names,
                    key="choice_a"
                )

                if choice_a == "Forge a new challenger...":
                    name_a = st.text_input("Give them a name:", value="Custom Warlord A", key="name_a")
                    faction_a = st.selectbox("Their allegiance:", [f.value for f in FactionType], key="fac_a")
                    desc_a = st.text_area("Their legend so far:", "A nameless challenger entering the arena.", key="desc_a")
                    champion_a = Champion(name=name_a, faction=FactionType(faction_a), description=desc_a)
                else:
                    champion_a = next(c for c in DEFAULT_CHAMPIONS if c.name == choice_a)

            with col2:
                st.markdown("**Rival Champion**")
                choice_b = st.selectbox(
                    "Summon their rival:",
                    all_champion_names,
                    index=all_champion_names.index("CoreWeave") if "CoreWeave" in all_champion_names else 1,
                    key="choice_b"
                )

                if choice_b == "Forge a new challenger...":
                    name_b = st.text_input("Give them a name:", value="Custom Warlord B", key="name_b")
                    faction_b = st.selectbox("Their allegiance:", [f.value for f in FactionType], key="fac_b")
                    desc_b = st.text_area("Their legend so far:", "A nameless challenger entering the arena.", key="desc_b")
                    champion_b = Champion(name=name_b, faction=FactionType(faction_b), description=desc_b)
                else:
                    champion_b = next(c for c in DEFAULT_CHAMPIONS if c.name == choice_b)

        st.markdown("<hr style='border-color: var(--line);'/>", unsafe_allow_html=True)

        # 2. Battlefield Selection — always independent of fighter mode. Suggests
        # the grudge match's usual terrain as a starting point, but you're always
        # free to override it either way.
        st.markdown("### Choose the battleground")
        field_names = [b.name for b in BATTLEFIELDS]
        field_choice = st.selectbox(
            "The terrain writes its own laws of war:",
            field_names,
            index=field_names.index(default_field) if default_field in field_names else 0
        )
        battlefield = next(b for b in BATTLEFIELDS if b.name == field_choice)

        st.markdown(f"**This ground decrees:** _Favors {battlefield.rewards}_ | _Suffers {battlefield.suffers}_")

        st.write("")
        trigger_battle = st.button("Stage the slaughter", width="stretch")

        if trigger_battle:
            if champion_a.name == champion_b.name:
                st.error("A realm cannot wage war upon itself. Choose two distinct champions.")
                return

            st.session_state["battle_state"] = "fighting"
            st.session_state["champion_a"] = champion_a
            st.session_state["champion_b"] = champion_b
            st.session_state["battlefield"] = battlefield
            st.rerun()

    def render_fight_view(self):
        """
        Renders the active duel stage, loading research, displaying profiles, 
        showing results, and handling dynamic Second Wind buttons.
        """
        champion_a = st.session_state["champion_a"]
        champion_b = st.session_state["champion_b"]
        battlefield = st.session_state["battlefield"]
        
        render_battlefield_banner(battlefield)
        
        # Check if we have pre-computed values
        if "ritual_executed" not in st.session_state:
            with st.spinner("⚔️ The War Council convenes... War Scout rides ahead, Myth Weaver forges the legend..."):
                try:
                    c_a, c_b, notes_a, notes_b, result, chronicle = self.orchestrator.perform_ritual(
                        champion_a, champion_b, battlefield
                    )

                    st.session_state["champion_a"] = c_a
                    st.session_state["champion_b"] = c_b
                    st.session_state["notes_a"] = notes_a
                    st.session_state["notes_b"] = notes_b
                    st.session_state["battle_result"] = result
                    st.session_state["battle_chronicle"] = chronicle
                    st.session_state["ritual_executed"] = True
                except Exception as e:
                    st.error(f"The War Council has faltered: {e}")
                    if st.button("Retreat to the War Room"):
                        self._reset_battle_state()
                    return
                    
        # Load local states
        notes_a = st.session_state["notes_a"]
        notes_b = st.session_state["notes_b"]
        result = st.session_state["battle_result"]
        chronicle = st.session_state["battle_chronicle"]
        
        # Render dynamic versus row (diagonal fighter panels, victor/defeated states)
        render_vs_row(champion_a, champion_b, result, battlefield)
        render_weapons_and_flaws(champion_a, champion_b)

        st.write("")
        render_prophecy(champion_a, champion_b)

        # Render the non-negotiable, plain-language verdict
        render_verdict_strip(chronicle.verdict)
        render_score_totals(result, champion_a, champion_b)

        # Render Second Wind interactives
        st.markdown("### Desperate counter-strike")

        is_triggered = result.second_wind_triggered

        if not is_triggered:
            st.markdown(
                f"The fallen (**{result.loser_name}**) may still call upon **one Second Wind** — "
                "a last, research-forged strike that could yet turn the tide."
            )

            # Click action triggers comeback recalculation
            if st.button(f"Call {result.loser_name}'s Second Wind", width="stretch"):
                with st.spinner("Drawing strength from the old records..."):
                    updated_result, updated_chronicle = self.orchestrator.apply_second_wind(
                        champion_a, champion_b, battlefield, result
                    )
                    st.session_state["battle_result"] = updated_result
                    st.session_state["battle_chronicle"] = updated_chronicle
                    st.rerun()
        else:
            st.markdown(
                f'<div class="second-wind-banner"><strong>Second Wind activated:</strong> '
                f'{result.loser_name} rallied using the research fact: '
                f'<em>&quot;{result.second_wind_fact}&quot;</em> '
                f'(+{result.second_wind_impact} points impact).</div>',
                unsafe_allow_html=True
            )

        # Render scorecard underneath — one scroll away from the theater above
        st.write("")
        render_scorecard(result, champion_a, champion_b, battlefield)

        # Tactical Advantage and Decisive Blows — the researched material behind
        # the verdict, styled as battle beats rather than an engineering readout.
        render_tactical_advantage(result, champion_a, champion_b, battlefield)
        render_decisive_blows(result.decisive_blows)

        st.markdown("---")

        # Render narrative chronicle
        st.markdown("### The chronicle saga")
        st.markdown(f"<div class='saga-box'>{html.escape(chronicle.saga)}</div>", unsafe_allow_html=True)

        # Inspectable Backbone details (Fidelity Law verification)
        st.markdown("---")
        with st.expander("Peer behind the myth (Fidelity Law)"):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**What the Scouts uncovered — {champion_a.name}:**")
                st.json({
                    "capabilities": notes_a.capabilities,
                    "limitations": notes_a.limitations,
                    "pricing": notes_a.pricing_signal,
                    "sources": notes_a.source_links
                })
            with col_b:
                st.markdown(f"**What the Scouts uncovered — {champion_b.name}:**")
                st.json({
                    "capabilities": notes_b.capabilities,
                    "limitations": notes_b.limitations,
                    "pricing": notes_b.pricing_signal,
                    "sources": notes_b.source_links
                })

        # Navigation / Storage actions
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("Inscribe this battle into the Codex", width="stretch"):
                entry = CodexEntry(
                    id=str(uuid.uuid4())[:8],
                    timestamp=datetime.utcnow(),
                    combatant_a=champion_a.name,
                    combatant_b=champion_b.name,
                    battlefield=battlefield.name,
                    result=result,
                    chronicle=chronicle
                )
                CodexService.save_entry(entry)
                st.success("The battle is etched into the Codex.")
        with col_nav2:
            if st.button("Stage another fight", width="stretch"):
                self._reset_battle_state()
                st.rerun()

    def render_codex_view(self):
        """
        Renders the Hall of Fame & Graveyard of past cloud battles.
        """
        st.markdown(
            "<h1 style='font-family: \"Cinzel Decorative\", serif; text-align: center; "
            "color: var(--ember); text-shadow: 0 0 18px rgba(217,164,65,0.35);'>THE CODEX REALM</h1>",
            unsafe_allow_html=True
        )
        st.markdown(
            "<p style='text-align: center; color: var(--bone-dim); font-family: \"IBM Plex Mono\", monospace;'>"
            "The chronicles of past cloud wars, stored in stone.</p>",
            unsafe_allow_html=True
        )
        
        entries = CodexService.load_entries()
        
        if not entries:
            st.info("The archives are empty. Stage and save duels to fill the chronicle walls.")
            if st.button("Return to the War Room"):
                st.session_state["app_tab"] = "Arena"
                st.rerun()
            return
            
        # Display summary calculations (Hall of Fame vs Graveyard)
        st.markdown("### Hall of fame")

        # Calculate win frequencies, both overall and per-battlefield — the
        # whole point of the battlefield mechanic is that a champion's total
        # win count can hide "wins the war but loses this terrain" splits.
        win_freq = {}
        win_by_battlefield = {}
        for e in entries:
            w = e.result.winner_name
            win_freq[w] = win_freq.get(w, 0) + 1
            win_by_battlefield.setdefault(w, {})
            win_by_battlefield[w][e.battlefield] = win_by_battlefield[w].get(e.battlefield, 0) + 1
        sorted_wins = sorted(win_freq.items(), key=lambda x: x[1], reverse=True)

        # Render Hall of Fame leaderboard columns
        st.write("Warlords ranked by decisive conquests:")
        cols = st.columns(min(len(sorted_wins), 4))
        for idx, (champion_name, win_count) in enumerate(sorted_wins[:4]):
            with cols[idx]:
                st.metric(label=f"Rank #{idx+1} {champion_name}", value=f"{win_count} Wins")
                breakdown = sorted(win_by_battlefield[champion_name].items(), key=lambda x: x[1], reverse=True)
                st.caption(" · ".join(f"{field} ({count})" for field, count in breakdown))
                
        st.markdown("### Graveyard of fallen clouds")
        for entry in entries:
            st.markdown(
                f"- **{entry.result.loser_name}** fell in **{entry.battlefield}** against **{entry.result.winner_name}** "
                f"(_decisive blows: {', '.join(entry.result.decisive_blows[:2])}_)"
            )
            
        st.markdown("---")
        st.markdown("### The archive halls")

        for e in reversed(entries):
            with st.expander(f"{e.combatant_a} vs {e.combatant_b} on {e.battlefield} ({e.timestamp.strftime('%Y-%m-%d %H:%M')})"):
                st.markdown(f"**Verdict:** {e.chronicle.verdict}")
                second_wind_text = "Called upon" if e.result.second_wind_triggered else "Not needed"
                st.markdown(f"**Second Wind:** {second_wind_text}")
                st.markdown(f"_Saga:_ {e.chronicle.saga}")

        if st.button("Burn the archives"):
            CodexService.clear_codex()
            st.success("The archives are ash.")
            st.rerun()

    def _reset_battle_state(self):
        st.session_state.pop("ritual_executed", None)
        st.session_state.pop("notes_a", None)
        st.session_state.pop("notes_b", None)
        st.session_state.pop("battle_result", None)
        st.session_state.pop("battle_chronicle", None)
        st.session_state["battle_state"] = "setup"
