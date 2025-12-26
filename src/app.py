import streamlit as st
import sys
import os
from datetime import datetime

# パス設定 (モジュールが見つからないエラー防止)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from tier1_engine import SolalendarTier1
from tier3_engine import SolalendarTier3

# --- Page Config ---
st.set_page_config(
    page_title="Solalendar Core v4.6",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS Injection ---
st.markdown("""
<style>
    .main { background-color: #0E1117; color: #FAFAFA; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; }
    .stButton>button { width: 100%; border-radius: 5px; font-weight: bold; }
    
    /* Layer Box Styling */
    .layer-box {
        background-color: #262730;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #444;
    }
    .layer-title {
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #AAA;
        margin-bottom: 5px;
    }
    .layer-value {
        font-size: 1.4em;
        font-weight: bold;
    }
    .oriental-tag {
        display: inline-block;
        background-color: #333;
        color: #DDD;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        margin-right: 5px;
        border: 1px solid #555;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar: System Access ---
with st.sidebar:
    st.title("🔑 System Access")
    api_key = st.text_input("OpenAI API Key", type="password")
    
    st.markdown("---")
    st.subheader("📍 Tier 1 Coordinates")
    name = st.text_input("Name", value="Haruki")
    
    c1, c2, c3 = st.columns(3)
    with c1: year = st.number_input("Year", 1900, 2100, 1974)
    with c2: month = st.number_input("Month", 1, 12, 11)
    with c3: day = st.number_input("Day", 1, 31, 4)
    
    c4, c5 = st.columns(2)
    with c4: hour = st.number_input("Hour", 0, 23, 7)
    with c5: minute = st.number_input("Minute", 0, 59, 1)

    tier1_btn = st.button("Decode Tier 1 (PSC) 🚀")

# --- Main Area ---
st.title("🌌 Solalendar Core v4.6")
st.caption("Integrated Fate Architecture: Tier 1 (Nature), Tier 2 (Observation), Tier 3 (Wisdom)")

tab1, tab2, tab3 = st.tabs(["🧬 Tier 1: Nature", "🔭 Tier 2: Observation", "💎 Tier 3: Wisdom"])

# --- TAB 1: Tier 1 (Nature) ---
with tab1:
    if tier1_btn:
        engine = SolalendarTier1(name, year, month, day, hour, minute)
        st.session_state['psc_data'] = engine.analyze()
        
    if 'psc_data' in st.session_state:
        d = st.session_state['psc_data']
        
        # Evidence Dictionary
        evidence = {
            "L0": "【根拠: 天文学】NASA JPL等のデータに基づく「ユリウス通日(JDN)」。宇宙共通の絶対時間座標。",
            "L1": "【根拠: ピタゴラス数秘術】生年月日の数列が生み出す固有の振動数を計算。西洋における「魂のOS」定義。",
            "L1_Ext": "【根拠: 六十干支】東洋思想における時間座標。天の気(十干)と地の気(十二支)の組み合わせにより、魂の「質感・素材」を定義する。",
            "L5": "【根拠: 西洋占星術】出生地の緯度経度において、生まれた瞬間に東の地平線を上昇していた星座。他者との境界線（インターフェース）。",
            "L2": "【根拠: ピナクル】数秘術において人生を4つの章に分割し、各ステージごとの「メインクエスト」を定義する構造設計図。",
            "L3": "【根拠: 二十四節気 & 9年周期】太陽黄経に基づく「季節の呼吸」と、数秘術の「螺旋周期」を統合。現在、どのような「気候」の中にいるかを定義。",
            "L4": "【根拠: 日干支 & パーソナルマンス】日々の微細なエネルギー変化。東洋の干支クロックが示す「今日の色彩」。"
        }

        col_trait, col_state = st.columns(2)
        
        # --- LEFT: TRAIT AXIS ---
        with col_trait:
            st.subheader("🧬 Trait Axis (本質)")
            st.caption("あなたの「機体性能」。一生変わることのない初期スペック。")
            
            t = d['trait_axis']
            l1b = t['layer_1b_library']
            l5 = t['layer_5_skin']
            l0_ext = t.get('layer_0_extended', {})
            
            # L1: BIOS
            st.markdown(f"""
            <div class='layer-box' style='border-left: 5px solid #00ADB5;'>
                <div class='layer-title'>L1: BIOS (Numerology Code)</div>
                <div class='layer-value' style='color:#00ADB5;'>{l1b['label']}</div>
                <div style='font-size:0.9em; color:#CCC;'>Keyword: {l1b['keyword']} / Element: {l1b['element']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # L1+: Roots
            birth_year_ganzhi = l0_ext.get('birth_year_ganzhi', 'Unknown')
            birth_day_ganzhi = l0_ext.get('birth_day_ganzhi', 'Unknown')
            st.markdown(f"""
            <div class='layer-box' style='border-left: 5px solid #00ADB5;'>
                <div class='layer-title'>L1+: Roots (Oriental Matrix)</div>
                <div class='layer-value' style='font-size: 1.1em;'>
                    Year: <span class='oriental-tag'>{birth_year_ganzhi}</span> 
                    Day: <span class='oriental-tag'>{birth_day_ganzhi}</span>
                </div>
                <div style='font-size:0.9em; color:#CCC;'>Eastern Texture & Material</div>
            </div>
            """, unsafe_allow_html=True)
            
            # L5: Skin
            st.markdown(f"""
            <div class='layer-box' style='border-left: 5px solid #E91E63;'>
                <div class='layer-title'>L5: Skin (Interface)</div>
                <div class='layer-value' style='color:#E91E63;'>{l5['ascendant']}</div>
                <div style='font-size:0.9em; color:#CCC;'>First Impression / Social Mask</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"<div class='layer-box'><div class='layer-title'>L0: Kernel</div><div class='layer-value'>{t['layer_0_kernel']['jdn']:.2f} JDN</div></div>", unsafe_allow_html=True)

        # --- RIGHT: STATE AXIS ---
        with col_state:
            st.subheader("🔭 State Axis (状態)")
            st.caption("「現在の環境」。季節や周期によって変動する実行条件。")
            
            s = d['state_axis']
            l2 = s['layer_2_infra']
            l3 = s.get('layer_3_env', {})
            l4 = s['layer_4_clock']
            stge = l2['stage']
            
            # L2: Infra
            st.markdown(f"""
            <div class='layer-box' style='border-left: 5px solid #9C27B0;'>
                <div class='layer-title'>L2: Infrastructure (Life Stage)</div>
                <div class='layer-value' style='color:#9C27B0;'>Phase {stge['phase']}: {stge['name']}</div>
                <div style='font-size:0.9em; color:#CCC;'>Quest: {stge['desc']}</div>
            </div>
            """, unsafe_allow_html=True)

            if l2['saturn_return']:
                st.warning("🪐 SATURN RETURN: 約29.5年周期の土星回帰。人生の再定義期間です。")

            # L3: Environment
            solar_term = l3.get('solar_term', {'name': 'Unknown'})
            year_ganzhi = l3.get('year_ganzhi', 'Unknown')
            current_phase = l3.get('current_year_phase', '?')
            st.markdown(f"""
            <div class='layer-box' style='border-left: 5px solid #F39C12;'>
                <div class='layer-title'>L3: Environment (Season & Flow)</div>
                <div style='display:flex; justify-content:space-between; align_items:center;'>
                    <div>
                        <div style='font-size:0.8em; color:#AAA;'>SOLAR TERM (節気)</div>
                        <div class='layer-value' style='color:#F39C12;'>{solar_term['name']}</div>
                    </div>
                    <div style='text-align:right;'>
                        <div style='font-size:0.8em; color:#AAA;'>YEAR GANZHI</div>
                        <div class='layer-value'>{year_ganzhi}</div>
                    </div>
                </div>
                <div style='margin-top:10px; border-top:1px solid #444; padding-top:5px;'>
                    <span style='color:#CCC;'>Numerology Cycle: Year {current_phase}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # L4: Runtime
            day_ganzhi = l4.get('day_ganzhi', 'Unknown')
            st.markdown(f"""
            <div class='layer-box' style='border-left: 5px solid #F39C12;'>
                <div class='layer-title'>L4: Runtime (Current Texture)</div>
                <div class='layer-value' style='color:#F39C12;'>{l4['label']}</div>
                <div style='font-size:0.9em; color:#CCC;'>Theme: {l4['keyword']}</div>
                <div style='margin-top:5px;'>
                    <span class='oriental-tag'>Day: {day_ganzhi}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.info(f"現在は「{solar_term['name']}」の季節、「{l4['label']}」のエネルギー下にあります。")

# --- TAB 2: Observation (Implementation) ---
with tab2:
    st.header("🔭 Tier 2: Observation Module")
    st.caption("Record your subjective reality (User Input). This bridges the gap to Tier 1.")

    with st.form("tier2_input_form"):
        col_mood, col_energy = st.columns(2)
        
        with col_mood:
            anxiety_level = st.slider("😰 Anxiety / Tension Level (不安・緊張)", 0, 100, 30, help="0=Calm, 100=Panic")
        
        with col_energy:
            energy_level = st.slider("🔋 Physical Energy (体力・気力)", 0, 100, 70, help="0=Exhausted, 100=Full Power")

        st.markdown("---")
        
        action_log = st.text_area("📝 Today's Action & Feelings (今日の行動と感情)", 
                                  placeholder="例: 今日は新しいプロジェクトの提案書を作ったが、自信がなくて少し疲れた。冬至だからか眠い。")
        
        submitted = st.form_submit_button("💾 Save Observation Data")
        
        if submitted:
            # データをセッションステートに保存
            st.session_state['tier2_data'] = {
                "anxiety": anxiety_level,
                "energy": energy_level,
                "log": action_log,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.success("Observation data saved! Now go to Tier 3 to generate Wisdom.")

    # 保存されたデータの確認
    if 'tier2_data' in st.session_state:
        st.info(f"✅ Current Tier 2 Data Loaded: {st.session_state['tier2_data']}")

# --- TAB 3: Wisdom (Integration) ---
with tab3:
    st.header("💎 Tier 3: Wisdom Engine")
    st.caption("Tier 1 (Fate) + Tier 2 (Observation) = Wisdom")
    
    # Check Requirements
    has_tier1 = 'psc_data' in st.session_state
    has_tier2 = 'tier2_data' in st.session_state
    
    if not has_tier1:
        st.warning("⚠️ Step 1: Please run [Decode Tier 1] in the Sidebar first.")
    
    if not has_tier2:
        st.warning("⚠️ Step 2: Please input your status in [Tier 2: Observation] tab.")
        
    if has_tier1 and has_tier2:
        st.success("All Systems Ready. Connecting to Core AI...")
        
        if st.button("Generate Wisdom (Real-Time Integration) ✨"):
            if not api_key:
                st.error("Please enter OpenAI API Key in the sidebar.")
            else:
                with st.spinner("Analyzing Gap between Fate (Tier 1) and Reality (Tier 2)..."):
                    t3 = SolalendarTier3(api_key)
                    
                    # リアルデータを渡す
                    tier1_data = st.session_state['psc_data']
                    tier2_data = st.session_state['tier2_data']
                    
                    result = t3.integrate(tier1_data, tier2_data)
                    
                    # Display Result
                    gap = result.get('gap_analysis', {})
                    msg = result.get('wisdom_message', {})
                    
                    st.markdown("---")
                    st.subheader("📊 System Diagnostics")
                    st.info(f"Analysis: Tier 1 Element vs Tier 2 State = {gap.get('relationship_type')} (Stress: {gap.get('stress_level')})")
                    
                    st.markdown(f"""
                    <div style='background-color:#2D1E3E; padding:25px; border-radius:15px; border: 1px solid #9C27B0; margin-top:20px;'>
                        <h2 style='color:#E0B0FF; text-align:center; margin-bottom:20px;'>{msg.get('headline')}</h2>
                        <p style='line-height:1.8; font-size:1.05em;'>{msg.get('narrative')}</p>
                        <hr style='border-color:#9C27B0; margin:20px 0;'>
                        <div style='background-color:#1E112A; padding:15px; border-radius:10px; border-left:5px solid #00E5FF;'>
                            <p style='font-weight:bold; color:#00E5FF; margin:0;'>💡 ACTIONABLE ADVICE:</p>
                            <p style='margin-top:5px; color:#DDD;'>{msg.get('actionable_advice')}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)