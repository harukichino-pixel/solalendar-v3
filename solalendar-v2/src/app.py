import streamlit as st
import json
from tier1_engine import SolalendarTier1
from tier2_b5v import SolalendarB5V

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Solalendar v3.0", page_icon="🌌", layout="wide")

# ---------------------------------------------------------
# Logic: Gap Analysis for v3.0
# ---------------------------------------------------------
def analyze_gap_v3(t1_data, b5_scores):
    """
    v3.0の多層データを用いて、ユーザーの役割疲労を解析する。
    Compare: Earthly Sun (Social Role) vs BigFive (Current Behavior)
    """
    gaps = []
    
    # データ抽出 (Safety Get)
    solar = t1_data.get('class_b_solar_earthly', {})
    sun_sign = solar.get('Sun', {}).get('sign', 'Unknown')
    
    # 4元素判定
    elem_map = {
        "Fire": ["Aries", "Leo", "Sagittarius"],
        "Earth": ["Taurus", "Virgo", "Capricorn"],
        "Air": ["Gemini", "Libra", "Aquarius"],
        "Water": ["Cancer", "Scorpio", "Pisces"]
    }
    my_element = "Unknown"
    for elem, signs in elem_map.items():
        if sun_sign in signs:
            my_element = elem
            break

    # --- Conflict Logic ---
    # 1. Fire Conflict (火なのに消極的)
    if my_element == "Fire" and b5_scores.get("Extraversion", 50) < 45:
        gaps.append({"title": "🔥 火の鎮火 (Suppressed Fire)", "desc": f"あなたの社会OS（{sun_sign}）は『情熱と自己主張』を求めていますが、現状は周囲に配慮しすぎて不完全燃焼を起こしています。"})
    
    # 2. Earth Conflict (地なのに不安定)
    if my_element == "Earth" and b5_scores.get("Conscientiousness", 50) < 45:
        gaps.append({"title": "⛰ 地の崩落 (Unstable Ground)", "desc": f"あなたの社会OS（{sun_sign}）は『確実性と成果』を求めていますが、現状はルーズな環境や計画性のなさに強いストレスを感じています。"})
        
    # 3. Air Conflict (風なのに停滞)
    if my_element == "Air" and b5_scores.get("Openness", 50) < 45:
        gaps.append({"title": "🌬 風の停滞 (Stagnant Air)", "desc": f"あなたの社会OS（{sun_sign}）は『知性と移動』を求めていますが、現状はルーチンワークにより思考が窒息しています。"})
        
    # 4. Water Conflict (水なのにドライ)
    if my_element == "Water" and b5_scores.get("Agreeableness", 50) < 45:
        gaps.append({"title": "💧 水の枯渇 (Dried Emotion)", "desc": f"あなたの社会OS（{sun_sign}）は『共感と融合』を求めていますが、現状は心を閉ざして戦闘モードになっています。ドライに振る舞うことに疲れ果てています。"})

    # --- Advanced: Sidereal Conflict (Soul Gap) ---
    # もし「社会OS(Tropical)」と「魂OS(Sidereal)」が違うエレメントで、かつストレスが高い場合
    sidereal = t1_data.get('class_b_sidereal_soul', {})
    true_sun = sidereal.get('Sun', {}).get('sign', 'Unknown')
    
    if sun_sign != true_sun:
        gaps.append({
            "title": f"🎭 Mask vs Soul ({sun_sign} vs {true_sun})",
            "desc": f"重要：あなたは社会的には「{sun_sign}」として振る舞っていますが、魂の本質は「{true_sun}」です。このギャップが、理由のない虚無感の原因かもしれません。"
        })

    # Default
    if not gaps:
        gaps.append({"title": "✨ 完全同期 (Perfect Sync)", "desc": "素晴らしい状態です。あなたの星（本質）と現在の行動様式が一致しており、ストレスなく能力を発揮できています。"})
        
    return gaps

# ---------------------------------------------------------
# UI Implementation
# ---------------------------------------------------------
st.title("🌌 Solalendar Core Engine v3.0")
st.caption("Full Spec Architecture: Solar(Earthly) / Sidereal(Soul) / Heliocentric(Mission)")

# Sidebar
with st.sidebar:
    st.header("Profile Coordinates")
    name = st.text_input("Name", "Haruki")
    c1, c2, c3 = st.columns(3)
    year = c1.number_input("Year", 1900, 2100, 1974)
    month = c2.number_input("Month", 1, 12, 11)
    day = c3.number_input("Day", 1, 31, 4)
    tc1, tc2 = st.columns(2)
    hour = tc1.number_input("Hour", 0, 23, 7)
    minute = tc2.number_input("Minute", 0, 59, 0)
    run_btn = st.button("Initialize Full-Spec System 🚀", type="primary")

# Execution
if run_btn:
    try:
        t1_engine = SolalendarTier1(name, year, month, day, hour, minute)
        data = t1_engine.analyze()
        st.session_state['t1_data'] = data
        st.rerun()
    except Exception as e:
        st.error(f"Engine Error: {e}")

if 't1_data' in st.session_state:
    d = st.session_state['t1_data']
    
    # --- Layer 1 Display ---
    st.header("🌍 Layer 1: Earthly OS (Tropical)")
    c1, c2, c3 = st.columns(3)
    
    numerology = d.get('class_d_archetypal', {}).get('numerology', {})
    solar = d.get('class_b_solar_earthly', {})
    mayan = d.get('class_d_archetypal', {}).get('mayan', {})

    with c1:
        st.info(f"**LPN (Ver):** {numerology.get('lpn', 'N/A')}")
        st.write(f"**Sun (Core):** {solar.get('Sun', {}).get('sign', 'N/A')}")
    with c2:
        st.write(f"**Moon (Bios):** {solar.get('Moon', {}).get('sign', 'N/A')}")
        st.write(f"**Asc (Body):** {solar.get('Ascendant', 'N/A')}")
    with c3:
        st.write(f"**Mayan:** {mayan.get('seal', 'N/A')}")
        st.write(f"**Tone:** {mayan.get('tone', 'N/A')}")

    # --- Layer 2 Display ---
    with st.expander("🌌 Layer 2: Soul & Mission (Deep Analysis)", expanded=False):
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("### 🧘 Soul (Sidereal/Vedic)")
            sid = d.get('class_b_sidereal_soul', {})
            s_sun = sid.get('Sun', {})
            st.write(f"**True Sun:** {s_sun.get('sign')} (Nakshatra: {s_sun.get('nakshatra')})")
            
        with sc2:
            st.markdown("### ☀️ Mission (Heliocentric)")
            hel = d.get('class_b_helio_mission', {})
            h_earth = hel.get('Earth', {})
            st.write(f"**Earth (Role):** {h_earth.get('sign')}")

    # --- Tier 2 Probe & Tier 3 Report ---
    st.divider()
    st.header("📡 Tier 2: The Dynamic Probe")
    
    t2_engine = SolalendarB5V()
    trop_sun = solar.get('Sun', {}).get('sign', 'Unknown')
    st.info(f"🤖 **AI Prediction:** Your Earthly Sun is **{trop_sun}**. How is your current status?")

    with st.form("b5v_form"):
        user_answers = {}
        cols = st.columns(2)
        idx = 0
        for cat, qs in t2_engine.bigfive_questions.items():
            for q in qs:
                with cols[idx%2]:
                    val = st.slider(f"**[{cat}]** {q['text']}", 1, 5, 3, key=q['id'])
                    user_answers[q['id']] = val
                idx += 1
        
        submitted = st.form_submit_button("Run Analysis 🧠")
        
    if submitted:
        # Calculate
        scores = t2_engine.calculate_bigfive(user_answers)
        
        # Visualize
        st.subheader("📊 Psychometric Status")
        st.bar_chart(scores)
        
        # Analyze Gap (Tier 3)
        st.divider()
        st.header("📜 Tier 3: Metacognition Report")
        
        gaps = analyze_gap_v3(d, scores)
        
        for gap in gaps:
            if "Perfect" in gap['title']:
                st.success(f"### {gap['title']}\n{gap['desc']}")
            elif "Mask vs Soul" in gap['title']:
                st.info(f"### {gap['title']}\n{gap['desc']}")
            else:
                st.warning(f"### {gap['title']}\n{gap['desc']}")
                
        st.caption("Generated by Solalendar Advanced Protocol v3.0")