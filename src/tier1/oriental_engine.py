import swisseph as swe

class OrientalEngine:
    """
    Tier 1 Class C & B Engine
    - Class C: Sexagenary Cycle (六十干支) for Year/Day
    - Class B: 24 Solar Terms (二十四節気) using Astronomical Logic
    """

    # 六十干支データ
    HEAVENLY_STEMS = ["甲 (Wood+)", "乙 (Wood-)", "丙 (Fire+)", "丁 (Fire-)", "戊 (Earth+)", "己 (Earth-)", "庚 (Metal+)", "辛 (Metal-)", "壬 (Water+)", "癸 (Water-)"]
    EARTHLY_BRANCHES = ["子 (Rat)", "丑 (Ox)", "寅 (Tiger)", "卯 (Rabbit)", "辰 (Dragon)", "巳 (Snake)", "午 (Horse)", "未 (Sheep)", "申 (Monkey)", "酉 (Rooster)", "戌 (Dog)", "亥 (Boar)"]
    
    # 二十四節気データ (太陽黄経基準)
    # 0度=春分, 15度=清明... 315度=立春
    SOLAR_TERMS = {
        0: "春分 (Vernal Equinox)", 15: "清明 (Clear and Bright)", 30: "穀雨 (Grain Rain)",
        45: "立夏 (Start of Summer)", 60: "小満 (Grain Full)", 75: "芒種 (Grain in Ear)",
        90: "夏至 (Summer Solstice)", 105: "小暑 (Minor Heat)", 120: "大暑 (Major Heat)",
        135: "立秋 (Start of Autumn)", 150: "処暑 (Limit of Heat)", 165: "白露 (White Dew)",
        180: "秋分 (Autumnal Equinox)", 195: "寒露 (Cold Dew)", 210: "霜降 (Frost Descent)",
        225: "立冬 (Start of Winter)", 240: "小雪 (Minor Snow)", 255: "大雪 (Major Snow)",
        270: "冬至 (Winter Solstice)", 285: "小寒 (Minor Cold)", 300: "大寒 (Major Cold)",
        315: "立春 (Start of Spring)", 330: "雨水 (Rain Water)", 345: "啓蟄 (Awakening of Insects)"
    }

    @staticmethod
    def get_sexagenary_cycle(year, month, day):
        """
        年・日の干支を計算
        """
        # 年干支 (1984年 = 甲子(0) を基準とする簡易計算)
        y_offset = (year - 1984) % 60
        year_ganzhi = OrientalEngine._index_to_ganzhi(y_offset)

        # 日干支 (JDNを使用)
        # JDN計算時には正午(12.0)を指定して日付ズレを防ぐ
        jd = swe.julday(year, month, day, 12.0)
        # 基準値の補正 (この定数は暦の連続性に基づく)
        d_offset = int(jd - 11) % 60
        day_ganzhi = OrientalEngine._index_to_ganzhi(d_offset)

        return {"year_ganzhi": year_ganzhi, "day_ganzhi": day_ganzhi}

    @staticmethod
    def _index_to_ganzhi(index):
        if index < 0: index += 60
        stem = OrientalEngine.HEAVENLY_STEMS[index % 10]
        branch = OrientalEngine.EARTHLY_BRANCHES[index % 12]
        return f"{stem}{branch}"

    @staticmethod
    def get_solar_term(year, month, day):
        """
        指定された日付の二十四節気を取得 (Class B Logic)
        """
        # 今日の太陽黄経を計算
        jd = swe.julday(year, month, day, 12.0)
        
        # 【修正点】swe.calc_ut は ((long, lat, dist...), flags) というタプルを返す
        # [0]で座標タプルを取り出し、さらに[0]で黄経(longitude)を取り出す
        res = swe.calc_ut(jd, swe.SUN)
        sun_longitude = res[0][0] 
        
        # 太陽黄経(0-360)に基づいて、直前の節気を探す
        # 辞書のキー(角度)を昇順にソート
        sorted_keys = sorted(OrientalEngine.SOLAR_TERMS.keys())
        
        # デフォルト（該当なしの場合の安全策）
        current_term_name = "Unknown"
        
        # 0度から順に見ていき、現在の黄経を超えない最大の角度を採用する
        # 例: sun=10 なら 0(春分)を採用。 sun=350 なら 345(啓蟄)を採用。
        target_angle = 0
        for k in sorted_keys:
            if sun_longitude >= k:
                target_angle = k
                current_term_name = OrientalEngine.SOLAR_TERMS[k]
            else:
                break
        
        return {"name": current_term_name, "longitude": sun_longitude}