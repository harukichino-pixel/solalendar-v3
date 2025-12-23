import datetime
import math
import pytz
import swisseph as swe
from kerykeion import AstrologicalSubject
from lunar_python import Solar, Lunar

class SolalendarTier1:
    """
    Solalendar Core Engine v3.0 (Full Spec)
    Implementation of Class A, B, C, D requirements.
    - Class A: JDN, Absolute Coordinates
    - Class B: Tropical (Geo), Sidereal (Geo), Heliocentric
    - Class C: Lunar, Gan-Zhi, Sukuyokyo (27 Mansions)
    - Class D: Mayan, Numerology
    """

    def __init__(self, name, year, month, day, hour, minute, lat=35.6895, lng=139.6917, tz_str="Asia/Tokyo"):
        self.name = name
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.lat = lat
        self.lng = lng
        self.tz_str = tz_str
        
        # Datetime handling
        local = pytz.timezone(tz_str)
        local_dt = local.localize(datetime.datetime(year, month, day, hour, minute))
        self.utc_dt = local_dt.astimezone(pytz.utc)
        
        # Class A: JDN Calculation (UT)
        self.jul_day_ut = swe.julday(year, month, day, hour + minute/60.0 - 9.0) # JST -> UT conversion approx
        
    # ---------------------------------------------------------
    # Helper: Zodiac Mapper
    # ---------------------------------------------------------
    def _get_zodiac_sign(self, lon):
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        idx = int(lon // 30) % 12
        return signs[idx]

    # ---------------------------------------------------------
    # Class D: Numerology (LPN)
    # ---------------------------------------------------------
    def _calculate_lpn(self):
        def reduce_to_lpn(num):
            while num > 9 and num not in [11, 22, 33]:
                num = sum(int(d) for d in str(num))
            return num
        sum_a = sum(int(d) for d in f"{self.year}{self.month}{self.day}")
        lpn_a = reduce_to_lpn(sum_a)
        sum_b = self.year + self.month + self.day
        lpn_b = reduce_to_lpn(sum_b)
        return lpn_b if lpn_b in [11, 22, 33] else lpn_a

    # ---------------------------------------------------------
    # Class B: Western (Tropical / Sidereal / Helio)
    # ---------------------------------------------------------
    def _get_planetary_data(self):
        # 1. Tropical (Geo) - "Earthly OS"
        subj = AstrologicalSubject(self.name, self.year, self.month, self.day, self.hour, self.minute, lat=self.lat, lng=self.lng, tz_str=self.tz_str, online=False)
        
        tropical = {
            "Sun": {"sign": subj.sun.sign, "lon": subj.sun.position},
            "Moon": {"sign": subj.moon.sign, "lon": subj.moon.position},
            "Mercury": {"sign": subj.mercury.sign, "lon": subj.mercury.position},
            "Mars": {"sign": subj.mars.sign, "lon": subj.mars.position},
            "Ascendant": subj.first_house.sign
        }

        # 2. Sidereal (Geo) - "Galactic/Soul OS"
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        
        sidereal = {}
        for p_name, p_id in [("Sun", swe.SUN), ("Moon", swe.MOON), ("Mars", swe.MARS)]:
            res = swe.calc_ut(self.jul_day_ut, p_id, swe.FLG_SIDEREAL)
            lon = res[0][0]
            sidereal[p_name] = {
                "sign": self._get_zodiac_sign(lon),
                "lon": round(lon, 2),
                "nakshatra": int(lon * 27 / 360) + 1 
            }

        # 3. Heliocentric - "Purpose/Mission"
        helio = {}
        # Earth from Sun perspective
        res_earth = swe.calc_ut(self.jul_day_ut, swe.EARTH, swe.FLG_HELCTR)
        lon_earth = res_earth[0][0]
        helio["Earth"] = {"sign": self._get_zodiac_sign(lon_earth), "lon": round(lon_earth, 2)}
        
        # Mars (Action) from Sun perspective
        res_mars = swe.calc_ut(self.jul_day_ut, swe.MARS, swe.FLG_HELCTR)
        lon_mars = res_mars[0][0]
        helio["Mars"] = {"sign": self._get_zodiac_sign(lon_mars), "lon": round(lon_mars, 2)}

        return tropical, sidereal, helio

    # ---------------------------------------------------------
    # Class C: Eastern (Lunar / Gan-Zhi / Sukuyokyo)
    # ---------------------------------------------------------
    def _get_eastern_data(self, moon_sidereal_lon):
        # 1. Lunar / Gan-Zhi
        solar = Solar.fromYmd(self.year, self.month, self.day)
        lunar = solar.getLunar()
        
        # 2. Sukuyokyo (27 Mansions)
        m_idx = int(moon_sidereal_lon * 27 / 360)
        
        return {
            "eto_day": lunar.getDayInGanZhi(),
            "nayin": lunar.getDayNaYin(),
            "lunar_date": f"{lunar.getYear()}年{lunar.getMonth()}月{lunar.getDay()}日",
            "shuku": f"Moon Station {m_idx + 1}"
        }

    # ---------------------------------------------------------
    # Class D: Mayan
    # ---------------------------------------------------------
    def _get_mayan_data(self):
        a = (14 - self.month) // 12
        y = self.year + 4800 - a
        m = self.month + 12 * a - 3
        jdn = self.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
        kin = (jdn - 584283) % 260 + 1
        seals = ["Red Dragon", "White Wind", "Blue Night", "Yellow Seed", "Red Serpent", "White Worldbridger", "Blue Hand", "Yellow Star", "Red Moon", "White Dog", "Blue Monkey", "Yellow Human", "Red Skywalker", "White Wizard", "Blue Eagle", "Yellow Warrior", "Red Earth", "White Mirror", "Blue Storm", "Yellow Sun"]
        tones = ["Magnetic (1)", "Lunar (2)", "Electric (3)", "Self-Existing (4)", "Overtone (5)", "Rhythmic (6)", "Resonant (7)", "Galactic (8)", "Solar (9)", "Planetary (10)", "Spectral (11)", "Crystal (12)", "Cosmic (13)"]
        return {"kin": kin, "seal": seals[(kin-1)%20], "tone": tones[(kin-1)%13]}

    # ---------------------------------------------------------
    # MAIN ANALYZE
    # ---------------------------------------------------------
    def analyze(self):
        lpn = self._calculate_lpn()
        trop, sid, helio = self._get_planetary_data()
        east = self._get_eastern_data(sid['Moon']['lon'])
        mayan = self._get_mayan_data()
        
        # Mapping Abbr to Full
        z_map = {"Ari":"Aries", "Tau":"Taurus", "Gem":"Gemini", "Can":"Cancer", "Leo":"Leo", "Vir":"Virgo", "Lib":"Libra", "Sco":"Scorpio", "Sag":"Sagittarius", "Cap":"Capricorn", "Aqu":"Aquarius", "Pis":"Pisces"}
        for planet in trop:
            if isinstance(trop[planet], dict) and 'sign' in trop[planet]:
                s = trop[planet]['sign']
                trop[planet]['sign'] = z_map.get(s, s)

        return {
            "meta": {"version": "Solalendar Tier1 v3.0 (Full Spec)", "subject": self.name},
            "class_a_absolute": {"jdn": self.jul_day_ut},
            "class_b_solar_earthly": trop,
            "class_b_sidereal_soul": sid,
            "class_b_helio_mission": helio,
            "class_c_eastern": east,
            "class_d_archetypal": {"mayan": mayan, "numerology": {"lpn": lpn}}
        }