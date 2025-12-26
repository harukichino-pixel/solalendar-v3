class Tier1Codec:
    """
    L1a: Codec (Encoding)
    物理座標(L0)を数理的カテゴリ(1-9等)へ正規化する計算式。
    """
    @staticmethod
    def reduce_to_single_digit(n):
        """数秘術の基本計算：一桁になるまで足す（Codecの基本ルール）"""
        if n == 0: return 0
        return (n - 1) % 9 + 1

    @staticmethod
    def calculate_lpn(year, month, day):
        """生年月日を1-9のフェーズにマッピングする"""
        s = sum(int(d) for d in f"{year:04d}{month:02d}{day:02d}")
        return Tier1Codec.reduce_to_single_digit(s)

    @staticmethod
    def calculate_phase(current_year, birth_month, birth_day):
        """現在の年におけるパーソナル・イヤー・フェーズを算出"""
        s = sum(int(d) for d in f"{current_year:04d}{birth_month:02d}{birth_day:02d}")
        return Tier1Codec.reduce_to_single_digit(s)