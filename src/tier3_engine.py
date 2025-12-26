import openai
import json
import streamlit as st

class SolalendarTier3:
    def __init__(self, api_key):
        self.client = openai.OpenAI(api_key=api_key)

    def integrate(self, tier1_data, tier2_result):
        """
        Tier 1 (Trait/State Axis) + Tier 2 (Action) -> Tier 3 Wisdom
        """
        
        # --- 1. Tier 1 データの解凍 (New Axis Structure) ---
        # 安全にデータを取り出す
        t_axis = tier1_data.get('trait_axis', {})
        s_axis = tier1_data.get('state_axis', {})
        
        # [Trait Axis] 本質的なスペック
        l1_bios = t_axis.get('layer_1b_library', {})
        l5_skin = t_axis.get('layer_5_skin', {})
        
        trait_desc = (
            f"Inner Core (L1): {l1_bios.get('label', 'Unknown')} "
            f"[Keywords: {l1_bios.get('keyword', '')} / Element: {l1_bios.get('element', '')}]\n"
            f"Outer Mask (L5): {l5_skin.get('ascendant', 'Unknown')} "
            f"(First Impression/Social Interface)"
        )

        # [State Axis] 現在の環境・時期
        l2_infra = s_axis.get('layer_2_infra', {})
        l4_runtime = s_axis.get('layer_4_clock', {})
        
        life_stage_info = l2_infra.get('stage', {})
        saturn_status = "ACTIVE (Crisis/Re-structuring)" if l2_infra.get('saturn_return') else "Inactive (Normal Orbit)"
        
        state_desc = (
            f"Life Stage (L2): Phase {life_stage_info.get('phase', '?')} - {life_stage_info.get('name', 'Unknown')}\n"
            f"   > Context: {life_stage_info.get('desc', '')}\n"
            f"   > Saturn Return: {saturn_status}\n"
            f"Current Year Mode (L4): {l4_runtime.get('label', 'Unknown')} "
            f"[Theme: {l4_runtime.get('keyword', '')}]"
        )

        # --- 2. Tier 2 データの解凍 (Behavior) ---
        # Tier 2の結果を要約テキストとして整形
        tier2_summary = "Tier 2 Analysis Result: " + str(tier2_result)

        # --- 3. Prompt Engineering ---
        # システム管理者としてのペルソナ定義
        system_prompt = """
        You are 'The System Administrator of Fate' (Solalendar Core). 
        Your mission is to eliminate user anxiety by explaining the structural relationship between their innate specs (Trait), their current environment (State), and their observed behavior (Tier 2).

        Analyze the gap between:
        1. Inner Core (What they are) vs Outer Mask (How they appear)
        2. Life Stage (Long-term goal) vs Current Year Mode (Short-term task)
        
        Output ONLY valid JSON:
        {
            "gap_analysis": {
                "tier1_element": "Primary Element of L1 (e.g. Air, Water)",
                "tier2_element": "Inferred Element of L2 behavior",
                "relationship_type": "Conflict / Harmony / Complement / Suppression",
                "stress_level": "High / Medium / Low"
            },
            "wisdom_message": {
                "headline": "A short, poetic, and reassuring title (Japanese)",
                "narrative": "Empathetic explanation of their current situation. Explain why they might feel conflict between their inner self, social mask, and current life stage. (Japanese)",
                "actionable_advice": "One concrete, philosophical yet practical action to align their path. (Japanese)"
            }
        }
        """

        user_prompt = f"""
        # SYSTEM DIAGNOSTICS REQUEST
        
        ## [UNIT: TRAIT AXIS (Immutable Specs)]
        {trait_desc}
        
        ## [ENV: STATE AXIS (Current Variables)]
        {state_desc}
        
        ## [LOG: TIER 2 BEHAVIOR (Observed)]
        {tier2_summary}
        
        Generate the integration report.
        """

        # --- 4. Call LLM ---
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {"error": f"Tier 3 Integration Error: {str(e)}"}