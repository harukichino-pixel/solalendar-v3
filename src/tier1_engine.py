import swisseph as swe
from datetime import datetime
from tier1.codec_engine import Tier1Codec
from tier1.semantic_library import PYTHAGOREAN_LIBRARY

class SolalendarTier1:
    def __init__(self, name, year, month, day, hour=12, minute=0):
        self.name = name
        self.year, self.month, self.day = year, month, day
        self.hour, self.minute = hour, minute
        self.codec = Tier1Codec()

    def analyze(self):
        # --- Axis 1: Trait (本質：静的) ---
        lpn_phase = self.codec.calculate_lpn(self.year, self.month, self.day)
        trait_info = PYTHAGOREAN_LIBRARY.get(lpn_phase)

        # --- Axis 2: State (状態：動的) ---
        now = datetime.now()
        current_phase = self.codec.calculate_phase(now.year, self.month, self.day)
        state_info = PYTHAGOREAN_LIBRARY.get(current_phase)

        # --- L0: Kernel (Absolute) ---
        jd = swe.julday(self.year, self.month, self.day, self.hour + self.minute/60.0)

        return {
            "metadata": {"name": self.name, "timestamp": now.isoformat()},
            
            "trait_axis": {
                "layer_0_kernel": {"jdn": jd},
                "layer_1a_codec": {"lpn_phase": lpn_phase},
                "layer_1b_library": trait_info,
                "layer_5_skin": {"ascendant": "TBD"} # 後ほど実装
            },
            
            "state_axis": {
                "layer_3_env": {"current_year_phase": current_phase},
                "layer_4_clock": state_info
            }
        }