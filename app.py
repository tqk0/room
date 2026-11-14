import streamlit as st

st.set_page_config(page_title="キャブセッティング診断", page_icon="🏍️", layout="centered")

# ==========================================
# 【Part 1】マスタデータ定義（ここをコピペして増やせます！）
# ==========================================

# default_cc_index の対応番号:
#   0: 50cc (ノーマル)
#   1: 60〜88cc (原付ボアアップ)
#   2: 100〜110cc (4miniミドル)
#   3: 115〜125cc (4miniハイチューン)
#   4: 200〜250cc (単気筒)
#   5: 250cc マルチ (2気筒等)
#   6: 400cc マルチ (4気筒等)
#   7: 750〜1000cc+ マルチ

BIKE_DATA = {
    # --- 4mini (4st) ---
    "モンキー / ゴリラ (Z50J/AB27)": {
        "engine_type": "4st横型",
        "default_cc_index": 1,
        "note": "横型エンジンの王道。フレーム内にキャブが収まるためマニホールド角度とタンク干渉に注意。"
    },
    "スーパーカブ50 / リトルカブ": {
        "engine_type": "4st横型",
        "default_cc_index": 0,
        "note": "レッグシールドを残す場合、大型キャブやパワフィルは干渉しやすいためマニホールド選びが重要です。"
    },
    "スーパーカブ70 / 90 (HA02)": {
        "engine_type": "4st横型",
        "default_cc_index": 1,
        "note": "純正でビッグフィン・ロングクランク(90)。PC20やPB18〜PD22との相性が抜群です。"
    },
    "ダックス / シャリー (ST50/CF50)": {
        "engine_type": "4st横型",
        "default_cc_index": 1,
        "note": "プレスフレーム構造のため、キャブが横出しになる専用インマニを使うケースが多いです。"
    },
    "マグナ50 / JAZZ": {
        "engine_type": "4st横型",
        "default_cc_index": 1,
        "note": "12V横型エンジン。車格が大きくロングツーリング向きなので実用域（中間開度）のセッティングが鍵。"
    },
    "モトラ / CT50 / モンキーR": {
        "engine_type": "4st横型",
        "default_cc_index": 1,
        "note": "モンキーRは純正でヘッドが優秀。フレーム構造上、キャブのクリアランス確認が必須です。"
    },
    "エイプ50(AC16) / XR50モタード": {
        "engine_type": "4st縦型",
        "default_cc_index": 0,
        "note": "縦型エンジン。80ccボアアップ＋PC20やPD22が街乗り定番仕様です。"
    },
    "エイプ100 / XR100モタード": {
        "engine_type": "4st縦型",
        "default_cc_index": 2,
        "note": "縦型100ccベース。PD22、PE24、TM-MJN24、FCR28など幅広いキャブが選べます。"
    },
    "NSF100": {
        "engine_type": "4st縦型",
        "default_cc_index": 2,
        "note": "スポーツ走行・サーキット志向。高回転域の伸びとパーシャルからのツキを重視したセッティングが人気。"
    },
    "CB50 / ドリーム50": {
        "engine_type": "4st縦型",
        "default_cc_index": 0,
        "note": "高回転型の縦型エンジン（ドリーム50はDOHC）。薄め焼き付きに注意し、高回転のMJを丁寧に合わせます。"
    },

    # --- 2スト (2st) ---
    "NS-1 (AC12) [2st]": {
        "engine_type": "2st水冷単気筒",
        "default_cc_index": 0,
        "is_2st": True,
        "note": "純正キャブはMJ#95(前期)/#100(後期)・SJ#40。PE20〜PE24やPWK28化が定番ですが、パワフィルより直キャブ/BOX加工の方がセッティングが出やすい傾向です。"
    },
    "ペリカンジョグ / JOG (27V) [2st]": {
        "engine_type": "2st空冷スクーター",
        "default_cc_index": 0,
        "is_2st": True,
        "note": "初期縦型ジョグ（純正MJ#84付近・TK丸大）。スクーターはキャブだけでなくプーリー/WR等駆動系の変速回転数も吹け上がりに影響します。"
    },
    "ライブDio ZX (AF34/AF35) [2st]": {
        "engine_type": "2st空冷スクーター",
        "default_cc_index": 0,
        "is_2st": True,
        "note": "前期・後期でキャブが異なり純正MJ#78〜#82・SJ#38〜#40付近。社外PE20/24化時は分離給油オイルポンプやオートチョーク処理に注意。"
    },

    # --- 250cc 単気筒 (4st) ---
    "ボルティー250 (NJ47A)": {
        "engine_type": "250cc単気筒",
        "default_cc_index": 4,
        "note": "スズキの空冷250cc単気筒（グラストラッカー/ST250系）。社外キャブ化ではスロットルワイヤー変更やパワフィル化・2次エアキャンセルの確認が定番。"
    },
    "FTR223 (MC34)": {
        "engine_type": "223cc単気筒",
        "default_cc_index": 4,
        "note": "ホンダ空冷単気筒（純正VEキャブはMJ#118・SJ#35〜38付近）。社外パワフィル＋マフラー仕様ではMJ#130〜135前後やPWK28/34・FCR化も人気です。"
    },

    # --- マルチ・2気筒/4気筒（※情報不足のため目安程度） ---
    "VT250FE (MC08) [マルチ/2気筒]": {
        "engine_type": "250cc水冷V型2気筒",
        "default_cc_index": 5,
        "is_multi": True,
        "note": "【目安程度】純正キャブは前後バンクで番手が異なる設計(例:フロント#92/リア#90, SJ#38)。マルチ車は情報が不足しているため基準値は参考程度とし、同調もご確認ください。"
    },
    "GSX-R400 (GK71B/73A/76A) [マルチ/4気筒]": {
        "engine_type": "400cc水冷直列4気筒",
        "default_cc_index": 6,
        "is_multi": True,
        "note": "【目安程度】年式・型式によりミクニ/ケイヒン/アイサン製など純正キャブが大きく異なります。マルチ車は情報不足のため数値はあくまで目安程度です。"
    },
    "TRX850 (4NX) [マルチ/2気筒]": {
        "engine_type": "850cc水冷並列2気筒",
        "default_cc_index": 7,
        "is_multi": True,
        "note": "【目安程度】純正はミクニBDST(ダウンドラフト)、社外はFCR39/41等が定番。マルチ車は情報不足のため数値はあくまで目安程度です。"
    },
    "CB1000SF (SC30) [マルチ/4気筒]": {
        "engine_type": "1000cc水冷直列4気筒",
        "default_cc_index": 7,
        "is_multi": True,
        "note": "【目安程度】純正CVキャブはMJ#105・SJ#38付近、社外FCR39ではMJ#145〜160前後が多め。マルチ車は情報不足のため数値はあくまで目安程度です。"
    },
}

# screw_type:
#   "AS" = エアスクリュー（空気調整：締める＝濃く、緩める＝薄く）
#   "PS" = パイロットスクリュー（混合気調整：緩める＝濃く、締める＝薄く）
CARB_DATA = {
    "KEIHIN 純正 PB14 (エイプ50等)": {
        "maker": "ケイヒン",
        "base_mj": 72.0,
        "base_sj": 38.0,
        "mj_step": 3.0,
        "sj_step": 3.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "エイプ50(AC16)純正キャブ。50ccフルノーマルでMJ#60・SJ#35が基準です。ASはD型ドライバーが必要（全ネジ大MJ・APE用PJ使用／純正ニードルは3段調整）。"
    },
    "KEIHIN 純正 PB16 / PC18": {
        "maker": "ケイヒン",
        "base_mj": 75.0,
        "base_sj": 35.0,
        "mj_step": 3.0,
        "sj_step": 3.0,
        "base_screw": 1.5,
        "screw_type": "PS",
        "note": "ノーマル〜ライトボアアップ向け。エンジン側下のD型スクリュー（PS）は緩めると濃くなります。"
    },
    "KEIHIN PC20": {
        "maker": "ケイヒン",
        "base_mj": 85.0,
        "base_sj": 35.0,
        "mj_step": 5.0,
        "sj_step": 3.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "4miniの定番。エアクリ側のマイナスネジがAS（締めると濃くなる）です。"
    },
    "KEIHIN PE20": {
        "maker": "ケイヒン",
        "base_mj": 90.0,
        "base_sj": 42.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "2st原付(NS-1/ジョグ/ディオ)や4mini定番の強制開閉キャブ。ケイヒン丸大MJ使用。※デイトナ製タイプ1/2のエアブリード付SJの場合は#55〜65付近と番手が大きく異なります。"
    },
    "KEIHIN PE21 (汎用/社外等)": {
        "maker": "ケイヒン/社外",
        "base_mj": 95.0,
        "base_sj": 42.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "2stボアアップ車(TZR50R/JOG/NS-1等)や4miniで使われる21φクラスPE系キャブ。本体仕様(エアブリード有無)によりSJの基準が変わるため現車の番手も要確認。"
    },
    "KEIHIN PD22": {
        "maker": "ケイヒン",
        "base_mj": 95.0,
        "base_sj": 38.0,
        "mj_step": 5.0,
        "sj_step": 3.0,
        "base_screw": 1.5,
        "screw_type": "PS",
        "note": "エイプ100や90cc系に定番。下側のパイロットスクリュー(PS)は緩めると濃くなります（※一部年式でAS仕様あり）。"
    },
    "KEIHIN PE24": {
        "maker": "ケイヒン",
        "base_mj": 105.0,
        "base_sj": 40.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "4miniボアアップや2st(NS-1/スクーターチューン)の超定番。ケイヒン丸大MJを使用。2stに使う場合は焼き付き防止のため濃いめから試してください。"
    },
    "KEIHIN PE28": {
        "maker": "ケイヒン",
        "base_mj": 125.0,
        "base_sj": 40.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "100cc超のハイチューンや2stビッグボア向け大口径丸型バルブ。中速のツキと高回転の伸びのバランスが良いです。"
    },
    "KEIHIN PWK28": {
        "maker": "ケイヒン",
        "base_mj": 120.0,
        "base_sj": 38.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "フラットバルブでレスポンス抜群。低開度（SJ〜ニードル）の合わせ込みがシビアになりやすいです。"
    },
    "PWK34 (KOSO / DIPPER / 汎用)": {
        "maker": "ケイヒンタイプ",
        "base_mj": 115.0,
        "base_sj": 40.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "carb_scale": "250_single",
        "note": "250cc単気筒等に人気のφ34ビッグキャブ（ケイヒン用MJ/SJ互換）。実走ではMJ#110〜115付近で合う例が多いです。パワージェット付きは高回転が濃くなりやすいため注意。"
    },
    "KEIHIN CR-mini22": {
        "maker": "ケイヒン",
        "base_mj": 95.0,
        "base_sj": 45.0,
        "mj_step": 5.0,
        "sj_step": 3.0,
        "base_screw": 1.75,
        "screw_type": "AS",
        "note": "4ストミニレース定番のCRキャブ。ジェット類はPEと共通です。ASの効きが良く微調整しやすいです。"
    },
    "KEIHIN FCR28": {
        "maker": "ケイヒン",
        "base_mj": 110.0,
        "base_sj": 45.0,
        "mj_step": 5.0,
        "sj_step": 3.0,
        "base_screw": 1.5,
        "screw_type": "PS",
        "note": "4mini〜250単気筒にも人気のレーシングキャブ（加速ポンプ付）。基本は下側のPS（緩めると濃く）でアイドリング〜極低開度を合わせます。"
    },
    "KEIHIN FCR39 (ラージボディ)": {
        "maker": "ケイヒン",
        "base_mj": 150.0,
        "base_sj": 48.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "PS",
        "carb_scale": "big_multi",
        "note": "大型マルチ(CB1000SF/TRX850等)やビッグシングル向けFCRラージボディ。PS（下側・緩めると濃く）とAS（エアクリ側・緩めると薄く）の両方を持ちます。"
    },
    "MIKUNI VM22 (汎用/中華キット等)": {
        "maker": "ミクニ",
        "base_mj": 95.0,
        "base_sj": 15.0,
        "mj_step": 5.0,
        "sj_step": 2.5,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "手軽な中華キットやライトチューン定番。本体ロットによってAS仕様とPS仕様が混在するため、ネジ位置を要確認。"
    },
    "MIKUNI VM26 (キタコ仕様)": {
        "maker": "ミクニ",
        "base_mj": 150.0,
        "base_sj": 15.0,
        "mj_step": 5.0,
        "sj_step": 2.5,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "キタコVM26（4J13ニードル等）基準。ミクニ丸大MJ・VM22/210型SJを使用。"
    },
    "MIKUNI VM26 (武川仕様)": {
        "maker": "ミクニ",
        "base_mj": 190.0,
        "base_sj": 22.5,
        "mj_step": 10.0,
        "sj_step": 2.5,
        "base_screw": 1.25,
        "screw_type": "AS",
        "note": "武川VM26（5E75ニードル等）基準。インナーパーツの違いでキタコ製よりMJ番号が大きくなります。"
    },
    "YOSHIMURA TM-MJN24": {
        "maker": "ヨシムラ(ミクニ)",
        "base_mj": 95.0,
        "base_sj": 25.0,
        "mj_step": 2.5,
        "sj_step": 2.5,
        "base_screw": 0.75,
        "screw_type": "AS",
        "note": "フラットバルブ×MJN。ミクニ六角大MJを使用。ASは全閉から3/4回転付近が基準とシビアめです。"
    },
    "YOSHIMURA YD-MJN24": {
        "maker": "ヨシムラ",
        "base_mj": 85.0,
        "base_sj": 42.0,
        "mj_step": 2.5,
        "sj_step": 3.0,
        "base_screw": 1.0,
        "screw_type": "AS",
        "note": "モンキー用ダウンドラフトMJN。MJNノズルは標準3段目が基準、MJはミクニ六角大、SJはケイヒン系に近い番手体系です。"
    },
    "YOSHIMURA YD-MJN28": {
        "maker": "ヨシムラ",
        "base_mj": 100.0,
        "base_sj": 45.0,
        "mj_step": 2.5,
        "sj_step": 3.0,
        "base_screw": 1.0,
        "screw_type": "AS",
        "note": "大排気量ヘッド（88〜124cc+ビッグバルブ）向けダウンドラフトMJN。急開よりもスムーズなスロットルワーク向き。"
    },
}

CC_LIST = [
    "50cc (ノーマル)",
    "60〜88cc (原付ボアアップ)",
    "100〜110cc (4miniミドル)",
    "115〜125cc (4miniハイチューン)",
    "200〜250cc (単気筒・ボルティー/FTR等)",
    "250cc マルチ (VT250FE等)",
    "400cc マルチ (GSX-R400等)",
    "750〜1000cc+ マルチ (CB1000SF/TRX850等)"
]

def fmt(val):
    return str(int(val)) if val == int(val) else str(round(val, 2))


# ==========================================
# 【Part 2】推論ロジック（ベース算出 & 症状診断）
# ==========================================

def calc_base_setting(carb_name, cc_class, head_spec, air_filter, exhaust, season, is_2st=False):
    carb = CARB_DATA[carb_name]
    mj = carb["base_mj"]
    sj = carb["base_sj"]
    clip = 3
    screw_turn = carb["base_screw"]
    scale = carb.get("carb_scale", "mini")

    # 1. キャブの想定クラスごとの排気量補正
    if scale == "250_single":
        # PWK34（250cc単気筒基準）
        if cc_class == CC_LIST[0]:
            mj -= carb["mj_step"] * 4
            sj -= carb["sj_step"] * 2
        elif cc_class == CC_LIST[1]:
            mj -= carb["mj_step"] * 3
            sj -= carb["sj_step"]
        elif cc_class == CC_LIST[2]:
            mj -= carb["mj_step"] * 2
            sj -= carb["sj_step"] * 0.5
        elif cc_class == CC_LIST[3]:
            mj -= carb["mj_step"]
        elif cc_class == CC_LIST[4]:
            pass
        elif cc_class == CC_LIST[5]:
            mj -= carb["mj_step"]
        elif cc_class == CC_LIST[6]:
            mj += carb["mj_step"]
        elif cc_class == CC_LIST[7]:
            mj += carb["mj_step"] * 3
            sj += carb["sj_step"] * 2

    elif scale == "big_multi":
        # FCR39（大型マルチ基準：150 / 48）
        if cc_class in [CC_LIST[0], CC_LIST[1], CC_LIST[2], CC_LIST[3]]:
            mj -= carb["mj_step"] * 8
            sj -= carb["sj_step"] * 4
        elif cc_class == CC_LIST[4]:
            mj -= carb["mj_step"] * 2
            sj -= carb["sj_step"]
        elif cc_class == CC_LIST[5]:
            mj -= carb["mj_step"] * 6
            sj -= carb["sj_step"] * 4
        elif cc_class == CC_LIST[6]:
            mj -= carb["mj_step"] * 4
            sj -= carb["sj_step"] * 2
        elif cc_class == CC_LIST[7]:
            pass

    else:
        # 4mini基準のキャブ（PE20/21/24, PC20, PWK28等）
        if is_2st:
            # 2ストは同排気量でも4ストより濃め（+1〜2ランク）が必要
            if cc_class == CC_LIST[0]:
                mj += carb["mj_step"]
                sj += carb["sj_step"]
            elif cc_class == CC_LIST[1]:
                mj += carb["mj_step"] * 2.5
                sj += carb["sj_step"] * 2
            else:
                mj += carb["mj_step"] * 3
                sj += carb["sj_step"] * 2
        else:
            if cc_class == CC_LIST[0]:
                mj -= carb["mj_step"] * 2
                sj -= carb["sj_step"]
            elif cc_class == CC_LIST[1]:
                pass
            elif cc_class == CC_LIST[2]:
                mj += carb["mj_step"]
                sj += carb["sj_step"] * 0.5
            elif cc_class == CC_LIST[3]:
                mj += carb["mj_step"] * 2
                sj += carb["sj_step"]
            elif cc_class == CC_LIST[4]:
                mj += carb["mj_step"] * 3
                sj += carb["sj_step"] * 1.5
            elif cc_class == CC_LIST[5]:
                mj += carb["mj_step"]
                sj += carb["sj_step"] * 0.5
            elif cc_class == CC_LIST[6]:
                mj += carb["mj_step"] * 2
                sj += carb["sj_step"]
            elif cc_class == CC_LIST[7]:
                mj += carb["mj_step"] * 5
                sj += carb["sj_step"] * 2

    # 2. ヘッド・カム / 2stポート補正
    if "スポーツカム" in head_spec:
        mj += carb["mj_step"] * 0.5
    elif "ビッグバルブ" in head_spec:
        mj += carb["mj_step"]
        sj += carb["sj_step"] * 0.5

    # 3. エアクリーナー補正
    if air_filter == "純正エアクリーナーBOX":
        mj -= carb["mj_step"]
    elif air_filter == "パワーフィルター":
        pass
    elif air_filter == "ファンネル / 直キャブ":
        mj += carb["mj_step"]

    # 4. マフラー / チャンバー補正
    if exhaust == "純正マフラー":
        mj -= carb["mj_step"]
    elif "ストリート" in exhaust:
        pass
    elif "レーシング" in exhaust:
        mj += carb["mj_step"]

    # 5. 季節補正
    if season == "夏（暑い・25℃以上）":
        mj -= carb["mj_step"]
    elif season == "冬（寒い・10℃以下）":
        mj += carb["mj_step"]

    # 入力欄の最小・最大範囲に安全に丸める
    mj = min(300.0, max(50.0, round(mj * 2) / 2))
    sj = min(80.0, max(10.0, round(sj * 2) / 2))
    return mj, sj, clip, screw_turn


def diagnose_symptoms(carb_name, cur_mj, cur_sj, cur_clip, cur_screw, sym_low, sym_mid, sym_high, sym_other, plug_color, is_2st=False):
    carb = CARB_DATA[carb_name]
    s_type = carb["screw_type"]  # "AS" or "PS"
    new_mj = cur_mj
    new_sj = cur_sj
    new_clip = cur_clip
    new_screw = cur_screw
    advices = []
    warnings = []

    # 1. 全開域（3/4〜全開）→ MJ
    if sym_high == "濃い（ボコつく・重い・黒煙・頭打ち）":
        new_mj -= carb["mj_step"]
        advices.append(f"🔺 **全開域が濃い症状**：MJを1ランク下げます（`#{fmt(cur_mj)}` → `#{fmt(new_mj)}`）。")
    elif sym_high == "薄い（息継ぎ・ガス欠感・高回転が伸びない）":
        new_mj += carb["mj_step"]
        advices.append(f"🔻 **全開域が薄い症状**：焼き付き防止のためMJを上げます（`#{fmt(cur_mj)}` → `#{fmt(new_mj)}`）。")

    # 2. 中間域（1/4〜3/4）→ クリップ位置
    if sym_mid == "濃い（ボコつく・吹け上がりが重い）":
        if cur_clip > 1:
            new_clip -= 1
            advices.append(f"🔺 **中間域が濃い症状**：クリップを1段「上げ」てニードルを下げます（`{cur_clip}段目` → `{new_clip}段目`）。")
        else:
            advices.append("⚠️ **中間域が濃い**ですが、クリップが既に最上段（1段目）です。MJを下げるか、より太いニードルを検討してください。")
    elif sym_mid == "薄い（ツキが悪い・パーシャルで息継ぎ）":
        if cur_clip < 5:
            new_clip += 1
            advices.append(f"🔻 **中間域が薄い症状**：クリップを1段「下げ」てニードルを上げます（`{cur_clip}段目` → `{new_clip}段目`）。")
        else:
            advices.append("⚠️ **中間域が薄い**ですが、クリップが既に最下段（5段目）です。MJを上げるか、より細いニードルを検討してください。")

    # 3. 低開度・アイドリング（0〜1/4）→ SJ & AS/PS自動分岐
    if s_type == "AS":
        if sym_low == "濃い（アイドリング不安定・生ガス臭い・カブる）":
            new_screw += 0.5
            advices.append(f"🔺 **低開度が濃い症状（AS仕様）**：エアスクリューを半回転「開け（緩め）」ます（`{cur_screw}回転` → `{new_screw}回転戻し`）。")
            if new_screw > 2.5:
                new_sj -= carb["sj_step"]
                new_screw = carb["base_screw"]
                advices.append(f"💡 ASが2.5回転以上開くため、**SJを1ランク下げて**ASを基準(`{new_screw}回転`)に戻すのがベストです（SJ `#{fmt(cur_sj)}` → `#{fmt(new_sj)}`）。")
        elif sym_low == "薄い（発進で息継ぎ・回転の落ちが遅い）":
            new_screw -= 0.5
            advices.append(f"🔻 **低開度が薄い症状（AS仕様）**：エアスクリューを半回転「締め」ます（`{cur_screw}回転` → `{max(0.25, new_screw)}回転戻し`）。")
            if new_screw < 0.5:
                new_sj += carb["sj_step"]
                new_screw = carb["base_screw"]
                advices.append(f"💡 ASが0.5回転未満まで締まるため、**SJを1ランク上げて**ASを基準(`{new_screw}回転`)に戻すのがベストです（SJ `#{fmt(cur_sj)}` → `#{fmt(new_sj)}`）。")
    else:
        if sym_low == "濃い（アイドリング不安定・生ガス臭い・カブる）":
            new_screw -= 0.5
            advices.append(f"🔺 **低開度が濃い症状（PS仕様）**：パイロットスクリューを半回転「締め」て混合気を減らします（`{cur_screw}回転` → `{max(0.25, new_screw)}回転戻し`）。")
            if new_screw < 0.75:
                new_sj -= carb["sj_step"]
                new_screw = carb["base_screw"]
                advices.append(f"💡 PSが0.75回転未満まで締まるため、**SJを1ランク下げて**PSを基準(`{new_screw}回転`)に戻すのがベストです（SJ `#{fmt(cur_sj)}` → `#{fmt(new_sj)}`）。")
        elif sym_low == "薄い（発進で息継ぎ・回転の落ちが遅い）":
            new_screw += 0.5
            advices.append(f"🔻 **低開度が薄い症状（PS仕様）**：パイロットスクリューを半回転「開け（緩め）」て混合気を増やします（`{cur_screw}回転` → `{new_screw}回転戻し`）。")
            if new_screw > 2.5:
                new_sj += carb["sj_step"]
                new_screw = carb["base_screw"]
                advices.append(f"💡 PSが2.5回転以上開くため、**SJを1ランク上げて**PSを基準(`{new_screw}回転`)に戻すのがベストです（SJ `#{fmt(cur_sj)}` → `#{fmt(new_sj)}`）。")

    # 4. その他症状
    if "アクセルオフでアフターファイア（パンパン鳴る）" in sym_other:
        if sym_low == "特になし（良好）":
            new_sj += carb["sj_step"]
            advices.append(f"💥 **アフターファイア対策**：エンブレ時のスロー燃料不足が疑われるためSJを上げます（`#{fmt(cur_sj)}` → `#{fmt(new_sj)}`）。※マフラー排気漏れでも鳴るのでフランジ要確認！")
        else:
            advices.append("💥 **アフターファイア**：低開度の燃料不足、またはマフラー接続部の排気漏れの可能性があります。")

    if "急開すると一瞬息継ぎする（ツキが悪い）" in sym_other:
        if "FCR" in carb_name:
            advices.append("⚡ **急開時の息継ぎ（FCR）**：加速ポンプの噴射量・タイミング（ダイヤフラムやロッド調整）を見直すと劇的に改善することがあります。")
        else:
            advices.append("⚡ **急開時の息継ぎ**：大口径キャブは急開すると流速が落ちて薄くなりがちです。少しクリップを下げるか、スロー系を濃くすると改善します。")

    if "エンジンが温まると調子が悪くなる" in sym_other:
        if is_2st:
            warnings.append("2stで温間時のみ不調・力がない場合、抱きつき前兆やオイル不足・熱ダレ、または濃すぎ（カブり）の可能性があります。")
        else:
            warnings.append("温間時のみの不調は、濃すぎ（カブり）か、「タペットクリアランス不良」「イグニッションコイル熱ダレ」の可能性もあります。")

    # 5. プラグの焼け色チェック
    if plug_color == "真っ白・電極が溶け気味（かなり薄い）":
        if sym_high == "特になし（良好）":
            new_mj += carb["mj_step"]
            advices.append(f"🔥 **プラグが真っ白なため補正**：体感の症状がなくても焼け色が薄いため、安全のためMJを上げます（`#{fmt(cur_mj)}` → `#{fmt(new_mj)}`）。")
        warnings.append("🚨 **プラグが真っ白です！** 全開走行を続けると焼き付き・ピストン溶損の危険があります。まずMJを上げて様子を見てください。")
    elif plug_color == "真っ黒で湿っている（かなり濃い）":
        warnings.append("⚫ **プラグが黒く湿っています。** セッティング前に新品プラグへ交換するか清掃してから再テストしてください。")

    if not advices:
        advices.append(f"✅ 大きな不調はありません。{s_type}を1/4回転ずつ回して最もアイドリングが高く安定する位置を探してみてください。")

    new_mj = min(300.0, max(50.0, new_mj))
    new_sj = min(80.0, max(10.0, new_sj))
    return new_mj, new_sj, new_clip, max(0.25, new_screw), advices, warnings


# ==========================================
# 【Part 3】画面UI
# ==========================================

st.title("🏍️ キャブセッティング診断")
st.caption("個人制作の非公式ツール｜4mini・2st原付・250単気筒・マルチ対応（全19車種 × 人気19キャブ）")

# --- 1. マシン仕様入力 ---
st.header("1. 車体・エンジン・吸排気の仕様")
col1, col2 = st.columns(2)
with col1:
    bike_model = st.selectbox("車種", list(BIKE_DATA.keys()))
    bike_info = BIKE_DATA[bike_model]
    is_2st = bike_info.get("is_2st", False)
    is_multi = bike_info.get("is_multi", False)

    cc_class = st.selectbox(
        "排気量",
        CC_LIST,
        index=bike_info["default_cc_index"],
        key=f"cc_{bike_model}"
    )
    head_spec = st.selectbox("エンジン詳細", [
        "純正仕様（ノーマル/ライトボア）",
        "社外スポーツカム / 2stライトチューン",
        "ビッグバルブ+ハイカム / 2stポート加工"
    ])

with col2:
    carb_name = st.selectbox("キャブレター", list(CARB_DATA.keys()))
    air_filter = st.selectbox("エアクリーナー", ["純正エアクリーナーBOX", "パワーフィルター", "ファンネル / 直キャブ"], index=1)
    exhaust = st.selectbox("エキパイ・サイレンサー", ["純正マフラー", "社外マフラー/チャンバー（ストリート）", "社外レーシング / 抜け重視・直管系"], index=1)

season = st.radio("現在の気温環境", ["夏（暑い・25℃以上）", "春・秋（標準・10〜25℃）", "冬（寒い・10℃以下）"], index=1, horizontal=True)

screw_label = CARB_DATA[carb_name]["screw_type"]
st.info(f"🏍️ **{bike_info['engine_type']}**：{bike_info['note']}\n\n🔧 **{carb_name}**：{CARB_DATA[carb_name]['note']}")

# 2st・マルチ専用バナー
if is_multi:
    st.warning("⚠️ **マルチ（多気筒）車について**：マルチ車は年式・純正キャブ種別・社外キャブの情報がまだ不足しているため、以下の基準値は**あくまで目安程度**にご参考ください。現車に現在付いている番手をもとに下の「症状診断」を使うのがおすすめです。")

if is_2st:
    st.warning("💨 **2ストローク車の注意**：2stは燃料が薄いと即焼き付き・抱きつきを起こします！特にパワーフィルターは流速が乱れてセッティングが出にくい車種（NS-1等）があるためご注意ください。")

# ベースセッティング計算
base_mj, base_sj, base_clip, base_screw = calc_base_setting(carb_name, cc_class, head_spec, air_filter, exhaust, season, is_2st=is_2st)

with st.expander("📊 この仕様の「基準（初期）セッティング」目安を見る", expanded=True):
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("基準 MJ", f"#{fmt(base_mj)}")
    b2.metric("基準 SJ", f"#{fmt(base_sj)}")
    b3.metric("クリップ(上から)", f"{base_clip}段目")
    b4.metric(f"{screw_label} 戻し", f"{base_screw} 回転")
    st.caption("※あくまでスタート地点の目安です。迷ったら基準より少し濃いめ（MJ+5〜10）から始めると安全です。")

st.divider()

# --- 2. 現状セッティング＆症状入力 ---
st.header("2. 現状のセッティングと症状")

state_key = f"{bike_model}_{carb_name}_{cc_class}_{air_filter}_{exhaust}_{season}"
c1, c2, c3, c4 = st.columns(4)
with c1:
    cur_mj = st.number_input("現在の MJ (#)", min_value=50.0, max_value=300.0, value=float(base_mj), step=2.5, key=f"mj_{state_key}")
with c2:
    cur_sj = st.number_input("現在の SJ (#)", min_value=10.0, max_value=80.0, value=float(base_sj), step=0.5, key=f"sj_{state_key}")
with c3:
    cur_clip = st.selectbox("クリップ位置（上から）", [1, 2, 3, 4, 5], index=2)
with c4:
    cur_screw = st.number_input(f"{screw_label} 戻し回転数", min_value=0.0, max_value=4.0, value=float(base_screw), step=0.25, key=f"sc_{state_key}")

st.subheader("出ている症状を選択してください")
sym_low = st.selectbox("【低開度 0〜1/4】アイドリング〜発進", [
    "特になし（良好）",
    "濃い（アイドリング不安定・生ガス臭い・カブる）",
    "薄い（発進で息継ぎ・回転の落ちが遅い）"
])
sym_mid = st.selectbox("【中開度 1/4〜3/4】巡航・加速中", [
    "特になし（良好）",
    "濃い（ボコつく・吹け上がりが重い）",
    "薄い（ツキが悪い・パーシャルで息継ぎ）"
])
sym_high = st.selectbox("【全開域 3/4〜全開】最高速付近", [
    "特になし（良好）",
    "濃い（ボコつく・重い・黒煙・頭打ち）",
    "薄い（息継ぎ・ガス欠感・高回転が伸びない）"
])

sym_other = st.multiselect("その他の症状（複数選択可）", [
    "アクセルオフでアフターファイア（パンパン鳴る）",
    "急開すると一瞬息継ぎする（ツキが悪い）",
    "エンジンが温まると調子が悪くなる"
])

plug_color = st.selectbox("プラグの焼け色（確認できた場合）", [
    "未確認 / きつね色（良好）",
    "真っ白・電極が溶け気味（かなり薄い）",
    "真っ黒で湿っている（かなり濃い）"
])

# --- 3. 診断結果 ---
if st.button("🔍 次の推奨セッティングを診断する", type="primary", use_container_width=True):
    new_mj, new_sj, new_clip, new_screw, advices, warnings = diagnose_symptoms(
        carb_name, cur_mj, cur_sj, cur_clip, cur_screw,
        sym_low, sym_mid, sym_high, sym_other, plug_color, is_2st=is_2st
    )

    st.divider()
    st.header("🎯 次の推奨セッティング案")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("推奨 MJ", f"#{fmt(new_mj)}", delta=fmt(new_mj - cur_mj) if new_mj != cur_mj else None)
    r2.metric("推奨 SJ", f"#{fmt(new_sj)}", delta=fmt(new_sj - cur_sj) if new_sj != cur_sj else None)
    r3.metric("クリップ(上から)", f"{new_clip}段目", delta=f"{new_clip - cur_clip}段" if new_clip != cur_clip else None)
    r4.metric(f"{screw_label} 戻し", f"{new_screw} 回転", delta=f"{round(new_screw - cur_screw, 2)}" if new_screw != cur_screw else None)

    st.subheader("📝 調整のポイント")
    for adv in advices:
        st.markdown(f"- {adv}")

    if warnings:
        for warn in warnings:
            st.error(warn)

    st.warning("⚠️ **セッティングの鉄則**：ジェット類は「1箇所ずつ」変更して試走すると原因が迷子になりにくいです。2次エア吸いやフロート油面の狂い、リードバルブ/タペット状態にもご注意ください。")

# --- フッター（免責事項） ---
st.divider()
st.caption("""
**【免責事項・ご利用にあたって】**
- 本アプリはバイク好きの個人が制作した非公式の参考ツールです。各メーカー様とは一切関係ありません。
- 提示される番手や調整値は一般的な目安です。特にマルチ車や2st車は車両の個体差、気候、経年劣化等により最適値が大きく異なります。
- 本アプリを参考にした作業・走行によるエンジンの焼き付きや故障等のトラブルについて、制作者は一切の責任を負いかねます。必ず自己責任のもと、安全に配慮してセッティングを行ってください。
""")
