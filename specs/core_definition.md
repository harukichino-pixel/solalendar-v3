# Solalendar Tier 1 Core Definition (v4.0)

## 1. Mission Statement
**Decode the Personal Source Code (PSC)**
パーソナル・ソースコードの解読

Solalendar Tier 1のミッションは、宇宙現象としての「周期性（Cycle）」と「不可逆な時間（Linear Time）」を統合し、個人の出生データ（数と角度）に基づく**「変更不可能な初期スペック」を定義することである。これを「パーソナル・ソースコード（PSC）」**と呼び、システムアーキテクチャとして以下の6階層（Layer 0 - Layer 5）に構造化する。

---

## 2. Tier 1 Stack Architecture

ユーザーという存在を一つの「高度な演算システム」に見立てた階層定義。

### Layer 0: Kernel (核・物理階層)
* **Metaphor:** Hardware (ハードウェア)
* **Components:** Space-Time Coordinate (ユリウス通日 / 緯度・経度)
* **System Definition:** [The Absolute: 絶対座標]
    * 物理的実体（不可視・不変）。
    * 人間的な解釈が入る前の、純粋な「時間と空間の物理座標」。NASAや国立天文台の観測データそのもの（Truth）。

### Layer 1: BIOS (基本入出力システム)
* **Metaphor:** Codec / Logic (翻訳・変換ロジック)
* **Components:** Source Numerology (9年周期 / 1-9の振動数)
* **System Definition:** [Translation Protocol: 翻訳規約]
    * 基本入出力システム。
    * Layer 0 の物理座標データを、人間が理解可能な「意味（運命のコード）」に変換するための基礎言語およびアルゴリズム。

### Layer 2: Infra (社会基盤)
* **Metaphor:** Operating System (基本ソフトウェア)
* **Components:** Saturn Cycle (土星: 29.5年) / Jupiter Cycle (木星: 12年)
* **System Definition:** [System Update: システム更新]
    * インフラ・構造。
    * 社会的な「制限（仕様の策定）」と「拡張（機能の追加）」を司る、長期的なバージョン管理（ライフステージ）のスケジュール。

### Layer 3: Env (環境)
* **Metaphor:** GUI / Desktop (視覚的な操作画面)
* **Components:** Sun Cycle (太陽: 365日) / 24 Solar Terms (二十四節気)
* **System Definition:** [Display Environment: 表示環境]
    * 環境・季節。
    * ユーザーが視覚的に認識している「風景」や「背景画」。生命力や意欲を映し出すメイン画面。

### Layer 4: Runtime (実行環境)
* **Metaphor:** System Clock (システム時計)
* **Components:** Eastern Root (日干支: 60日) / Moon Cycle (月: 28日)
* **System Definition:** [Process Timing: 処理タイミング]
    * クロック・質感。
    * 日々の処理タイミングと、その瞬間のエネルギーの「テクスチャ（五行の性質）」や感情のバイオリズム。

### Layer 5: Skin (外装)
* **Metaphor:** Interface (接点)
* **Components:** Ascendant (アセンダント)
* **System Definition:** [External Interface: 外部接続端子]
    * アバター・外装。
    * 対外的な第一印象や、社会との接点となるインターフェース（スキン）。

---

## 3. Architectural Strategy

### 🛡️ 1. 「絶対」と「解釈」の分離 (Scalability)
**Layer 0 (Physics) vs Layer 1 (Protocol)**
* 構造: 「宇宙に嘘はない（L0: 物理座標）」と、「それを読むためのプロトコル（L1: 数秘）」を明確にレイヤー分けした。
* メリット: 科学的整合性（NASAデータへの準拠）を保ちつつ、将来的に解釈ロジック（L1）をアップデートしてもカーネル（L0）を傷つけない**「システムとしての拡張性」**を担保する。

### 🧬 2. 「線形」と「円環」の統合 (Philosophy)
**Linear Time (Progress) & Cycles (Rhythm)**
* 構造: 相反する時間の概念を役割分担させた。
    * リニアタイム (L0, L2): 不可逆な時の流れ、進歩、バージョンアップ。
    * サイクル (L3, L4): 繰り返される季節、代謝、リズム。
* メリット: 「人生は同じ場所を回っているようでいて、実は螺旋階段のように上昇している」という哲学的な命題をシステムロジックとして実装する。

### 🌿 3. ユーザー視点の「手触り」 (UX / Psychology)
**Logic (Hidden) to Emotion (Visible)**
* 構造: 下層（L0-L2）で堅牢な計算ロジックを組みつつ、上層（L3-L5）ではあえて**「風景」「質感」「アバター」**という情緒的なメタファーを採用。
* メリット: テックに詳しくないユーザーに対し、複雑な運命論を「直感的な安らぎ（Weather Forecast）」として提供する。UXのゴールは「計算が正しいか」ではなく**「その風景に納得できるか」**とする。