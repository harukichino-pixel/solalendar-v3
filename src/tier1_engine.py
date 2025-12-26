import swisseph as swe
from datetime import datetime
from tier1.codec_engine import Tier1Codec
from tier1.semantic_library import PYTHAGOREAN_LIBRARY
# ▼▼▼ 追加1: 新しいエンジンのインポート ▼▼▼
from tier1.oriental_engine import OrientalEngine

class SolalendarTier1:
    def __init__(self, name, year, month, day, hour=12, minute=0, lat=35.68, lon=139.76):
        self.name = name
        self.year, self.month, self.day = year, month, day
        self.hour, self.minute = hour, minute
        self.lat, self.lon = lat, lon
        self.codec = Tier1Codec()

    def _get_zodiac_sign(self, degree):
        signs = [
            "Aries (牡羊座)", "Taurus (牡牛座)", "Gemini (双子座)", "Cancer (蟹座)", 
            "Leo (獅子座)", "Virgo (乙女座)", "Libra (天秤座)", "Scorpio (蠍座)", 
            "Sagittarius (射手座)", "Capricorn (山羊座)", "Aquarius (水瓶座)", "Pisces (魚座)"
        ]
        return signs[int(degree / 30) % 12]

    def _calculate_life_stage(self, age, lpn):
        """年齢と運命数(LPN)から、人生の4つの頂点（Pinnacles）を算出"""
        p1_end = 36 - lpn
        p2_end = p1_end + 9
        p3_end = p2_end + 9
        
        if age <= p1_end:
            return {"phase": 1, "name": "Development (種まき)", "desc": "自我の形成と試行錯誤の時期"}
        elif age <= p2_end:
            return {"phase": 2, "name": "Creation (開花)", "desc": "責任ある行動と建設の時期"}
        elif age <= p3_end:
            return {"phase": 3, "name": "Expansion (収穫)", "desc": "影響力の拡大と成熟の時期"}
        else:
            return {"phase": 4, "name": "Reflection (継承)", "desc": "智慧の統合と社会還元"}

    def analyze(self):
        # --- 基本計算 ---
        jd = swe.julday(self.year, self.month, self.day, self.hour + self.minute/60.0)
        now = datetime.now()
        age = now.year - self.year - ((now.month, now.day) < (self.month, self.day))

        # --- Axis 1: Trait (本質) ---
        lpn_phase = self.codec.calculate_lpn(self.year, self.month, self.day)
        trait_info = PYTHAGOREAN_LIBRARY.get(lpn_phase)

        # L5: Ascendant
        houses, ascmc = swe.houses(jd, self.lat, self.lon, b'P')
        asc_sign = self._get_zodiac_sign(ascmc[0])

        # --- Axis 2: State (状態) ---
        current_phase = self.codec.calculate_phase(now.year, self.month, self.day)
        state_info = PYTHAGOREAN_LIBRARY.get(current_phase)
        
        # L2 (Infrastructure)
        life_stage = self._calculate_life_stage(age, lpn_phase)
        is_saturn_return = (28 <= age <= 30) or (58 <= age <= 60)

        # ▼▼▼ 追加2: 東洋・季節エンジンの計算実行 ▼▼▼
        # 1. 生年月日時点の干支（Trait用）
        birth_oriental = OrientalEngine.get_sexagenary_cycle(self.year, self.month, self.day)
        
        # 2. 現在時点の干支と季節（State用）
        current_oriental = OrientalEngine.get_sexagenary_cycle(now.year, now.month, now.day)
        current_solar_term = OrientalEngine.get_solar_term(now.year, now.month, now.day)
        # ▲▲▲ ここまで ▲▲▲

        return {
            "metadata": {"name": self.name, "timestamp": now.isoformat(), "age": age},
            
            "trait_axis": {
                "layer_0_kernel": {"jdn": jd, "lat": self.lat, "lon": self.lon},
                # ▼▼▼ 追加3: Traitデータの拡張 ▼▼▼
                "layer_0_extended": {
                    "birth_year_ganzhi": birth_oriental['year_ganzhi'],
                    "birth_day_ganzhi": birth_oriental['day_ganzhi']
                },
                # ▲▲▲ ここまで ▲▲▲
                "layer_1a_codec": {"lpn_phase": lpn_phase},
                "layer_1b_library": trait_info,
                "layer_5_skin": {"ascendant": asc_sign}
            },
            
            "state_axis": {
                "layer_2_infra": {
                    "stage": life_stage, 
                    "saturn_return": is_saturn_return
                },
                # ▼▼▼ 追加4: Stateデータの拡張 (Layer 3 & 4) ▼▼▼
                "layer_3_env": {
                    "current_year_phase": current_phase,
                    "solar_term": current_solar_term,    # 二十四節気
                    "year_ganzhi": current_oriental['year_ganzhi'] # 年の干支
                },
                "layer_4_clock": {
                    **state_info, # 既存の数秘データ(Label/Keywordなど)を展開
                    "day_ganzhi": current_oriental['day_ganzhi'] # 日の干支
                }
                # ▲▲▲ ここまで ▲▲▲
            }
        }