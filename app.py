import streamlit as st
from datetime import datetime
import csv
import io

st.set_page_config(page_title="4mini キャブセッティング診断", page_icon="🏍️", layout="centered")

# ==========================================
# 【Part 1】マスタデータ定義（4mini & 250単気筒特化）
# ==========================================

# default_cc_index の対応番号:
#   0: 50cc (ノーマル)
#   1: 75〜88cc (定番ボアアップ)
#   2: 100〜110cc (ミドルチューン)
#   3: 115〜125cc (ハイチューン/中華125等)
#   4: 200〜250cc (単気筒・FTR/ボルティー等)

BIKE_DATA = {
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
    "FTR223 (MC34)": {
        "engine_type": "223cc単気筒",
        "default_cc_index": 4,
        "note": "ホンダ空冷単気筒（純正VEキャブはMJ#118・SJ#35〜38付近）。社外パワフィル＋マフラー仕様ではMJ#130〜135前後やPWK28/34・FCR化も人気です。"
    },
    "ボルティー250 (NJ47A)": {
        "engine_type": "250cc単気筒",
        "default_cc_index": 4,
        "note": "スズキ空冷250cc単気筒。社外キャブ化ではスロットルワイヤー変更やパワフィル化・2次エアキャンセルの確認が定番です。"
    },
}

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
        "note": "4mini定番の強制開閉キャブ。ケイヒン丸大MJ使用。※デイトナ製タイプ1/2のエアブリード付SJの場合は#55〜65付近と番手が大きく異なります。"
    },
    "KEIHIN PE21 (汎用/社外等)": {
        "maker": "ケイヒン/社外",
        "base_mj": 95.0,
        "base_sj": 42.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "21φクラスPE系キャブ。本体仕様（エアブリード有無）によりSJの基準が変わるため現車の番手も要確認。"
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
        "base_sj": 38.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "ボアアップ車の超定番。ケイヒン丸大MJを使用。セッティングが出しやすく扱いやすいキャブです。"
    },
    "KEIHIN PE28": {
        "maker": "ケイヒン",
        "base_mj": 125.0,
        "base_sj": 40.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_screw": 1.5,
        "screw_type": "AS",
        "note": "100cc超のハイチューン〜250単気筒向け大口径丸型バルブ。中速のツキと高回転の伸びのバランスが良いです。"
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
        "base_for_250": True,
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
    "75〜88cc (定番ボアアップ)",
    "100〜110cc (ミドルチューン)",
    "115〜125cc (ハイチューン/中華125等)",
    "200〜250cc (単気筒・FTR等)"
]

def fmt(val):
    return str(int(val)) if val == int(val) else str(round(val, 2))


# ==========================================
# 【Part 2】推論ロジック（ベース算出 & 症状診断）
# ==========================================

def calc_base_setting(carb_name, cc_class, head_spec, air_filter, exhaust, season):
    carb = CARB_DATA[carb_name]
    mj = carb["base_mj"]
    sj = carb["base_sj"]
    clip = 3
    screw_turn = carb["base_screw"]
    is_250_carb = carb.get("base_for_250", False)

    if is_250_carb:
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

    # ヘッド・カム補正
    if head_spec == "社外スポーツカムのみ":
        mj += carb["mj_step"] * 0.5
    elif head_spec == "社外ビッグバルブヘッド + ハイカム":
        mj += carb["mj_step"]
        sj += carb["sj_step"] * 0.5

    # エアクリーナー補正
    if air_filter == "純正エアクリーナーBOX":
        mj -= carb["mj_step"]
    elif air_filter == "パワーフィルター":
        pass
    elif air_filter == "ファンネル / 直キャブ":
        mj += carb["mj_step"]

    # マフラー補正
    if exhaust == "純正マフラー":
        mj -= carb["mj_step"]
    elif exhaust == "社外マフラー（ストリート/静かめ）":
        pass
    elif exhaust == "社外レーシング / 抜け重視・直管系":
        mj += carb["mj_step"]

    # 季節補正
    if season == "夏（暑い・25℃以上）":
        mj -= carb["mj_step"]
    elif season == "冬（寒い・10℃以下）":
        mj += carb["mj_step"]

    mj = min(300.0, max(50.0, round(mj * 2) / 2))
    sj = min(80.0, max(10.0, round(sj * 2) / 2))
    return mj, sj, clip, screw_turn


def diagnose_symptoms(carb_name, cur_mj, cur_sj, cur_clip, cur_screw, sym_low, sym_mid, sym_high, sym_other, plug_color):
    carb = CARB_DATA[carb_name]
    s_type = carb["screw_type"]
    new_mj = cur_mj
    new_sj = cur_sj
    new_clip = cur_clip
    new_screw = cur_screw
    advices = []
    warnings = []

    if sym_high == "濃い（ボコつく・重い・黒煙・頭打ち）":
        new_mj -= carb["mj_step"]
        advices.append(f"🔺 **全開域が濃い症状**：MJを1ランク下げます（`#{fmt(cur_mj)}` → `#{fmt(new_mj)}`）。")
    elif sym_high == "薄い（息継ぎ・ガス欠感・高回転が伸びない）":
        new_mj += carb["mj_step"]
        advices.append(f"🔻 **全開域が薄い症状**：焼き付き防止のためMJを上げます（`#{fmt(cur_mj)}` → `#{fmt(new_mj)}`）。")

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
        warnings.append("温間時のみの不調は、濃すぎ（カブり）か、「タペットクリアランス不良」「イグニッションコイル熱ダレ」の可能性もあります。")

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
# 【Part 3】画面UI & 履歴管理
# ==========================================

if "history" not in st.session_state:
    st.session_state["history"] = []
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

st.title("🏍️ 4mini キャブセッティング診断")
st.caption("個人制作の非公式ツール｜4mini（10車種）＋ FTR223 / ボルティー250 × 人気18キャブ対応")

# --- 1. マシン仕様入力 ---
st.header("1. 車体・エンジン・吸排気の仕様")
col1, col2 = st.columns(2)
with col1:
    bike_model = st.selectbox("車種", list(BIKE_DATA.keys()))
    bike_info = BIKE_DATA[bike_model]
    cc_class = st.selectbox(
        "排気量",
        CC_LIST,
        index=bike_info["default_cc_index"],
        key=f"cc_{bike_model}"
    )
    head_spec = st.selectbox("ヘッド・カム詳細", [
        "純正ヘッド・純正カム",
        "社外スポーツカムのみ",
        "社外ビッグバルブヘッド + ハイカム"
    ])

with col2:
    carb_name = st.selectbox("キャブレター", list(CARB_DATA.keys()))
    air_filter = st.selectbox("エアクリーナー", ["純正エアクリーナーBOX", "パワーフィルター", "ファンネル / 直キャブ"], index=1)
    exhaust = st.selectbox("エキパイ・サイレンサー", ["純正マフラー", "社外マフラー（ストリート/静かめ）", "社外レーシング / 抜け重視・直管系"], index=1)

season = st.radio("現在の気温環境", ["夏（暑い・25℃以上）", "春・秋（標準・10〜25℃）", "冬（寒い・10℃以下）"], index=1, horizontal=True)

screw_label = CARB_DATA[carb_name]["screw_type"]
st.info(f"🏍️ **{bike_info['engine_type']}**：{bike_info['note']}\n\n🔧 **{carb_name}**：{CARB_DATA[carb_name]['note']}")

base_mj, base_sj, base_clip, base_screw = calc_base_setting(carb_name, cc_class, head_spec, air_filter, exhaust, season)

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

# --- 3. 診断実行 ---
if st.button("🔍 次の推奨セッティングを診断する", type="primary", use_container_width=True):
    new_mj, new_sj, new_clip, new_screw, advices, warnings = diagnose_symptoms(
        carb_name, cur_mj, cur_sj, cur_clip, cur_screw,
        sym_low, sym_mid, sym_high, sym_other, plug_color
    )
    st.session_state["last_result"] = {
        "bike": bike_model,
        "cc": cc_class,
        "carb": carb_name,
        "air": air_filter,
        "exhaust": exhaust,
        "season": season,
        "cur_mj": cur_mj,
        "cur_sj": cur_sj,
        "cur_clip": cur_clip,
        "cur_screw": cur_screw,
        "new_mj": new_mj,
        "new_sj": new_sj,
        "new_clip": new_clip,
        "new_screw": new_screw,
        "screw_label": screw_label,
        "plug": plug_color,
        "advices": advices,
        "warnings": warnings,
    }

# --- 診断結果表示 & 履歴保存 ---
if st.session_state["last_result"]:
    res = st.session_state["last_result"]
    st.divider()
    st.header("🎯 次の推奨セッティング案")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("推奨 MJ", f"#{fmt(res['new_mj'])}", delta=fmt(res['new_mj'] - res['cur_mj']) if res['new_mj'] != res['cur_mj'] else None)
    r2.metric("推奨 SJ", f"#{fmt(res['new_sj'])}", delta=fmt(res['new_sj'] - res['cur_sj']) if res['new_sj'] != res['cur_sj'] else None)
    r3.metric("クリップ(上から)", f"{res['new_clip']}段目", delta=f"{res['new_clip'] - res['cur_clip']}段" if res['new_clip'] != res['cur_clip'] else None)
    r4.metric(f"{res['screw_label']} 戻し", f"{res['new_screw']} 回転", delta=f"{round(res['new_screw'] - res['cur_screw'], 2)}" if res['new_screw'] != res['cur_screw'] else None)

    st.subheader("📝 調整のポイント")
    for adv in res["advices"]:
        st.markdown(f"- {adv}")

    if res["warnings"]:
        for warn in res["warnings"]:
            st.error(warn)

    st.warning("⚠️ **セッティングの鉄則**：ジェット類は「1箇所ずつ」変更して試走すると原因が迷子になりにくいです。2次エア吸いやフロート油面の狂い、タペット調整不良にもご注意ください。")

    # 履歴へのメモ追加フォーム
    with st.form("save_history_form"):
        memo = st.text_input("試走メモ（任意）", placeholder="例：MJ110に変えたら谷が消えてきつね色になった！")
        if st.form_submit_button("📒 このセッティングを履歴メモに記録する"):
            st.session_state["history"].append({
                "日時": datetime.now().strftime("%Y/%m/%d %H:%M"),
                "車種": res["bike"],
                "キャブ": res["carb"],
                "現状": f"MJ#{fmt(res['cur_mj'])} / SJ#{fmt(res['cur_sj'])} / {res['cur_clip']}段 / {res['screw_label']}{res['cur_screw']}",
                "推奨": f"MJ#{fmt(res['new_mj'])} / SJ#{fmt(res['new_sj'])} / {res['new_clip']}段 / {res['screw_label']}{res['new_screw']}",
                "プラグ": res["plug"],
                "メモ": memo,
            })
            st.success("履歴に記録しました！（下のセッティング履歴から確認・CSV保存できます）")

# --- 4. セッティング履歴表示（Web版簡易版） ---
if st.session_state["history"]:
    st.divider()
    st.header("📒 今回のセッティング履歴メモ")
    st.caption("※現在のWeb版ではページを閉じるとリセットされます。残したい場合は下のCSVボタンで保存してください。")
    st.dataframe(st.session_state["history"], use_container_width=True)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=st.session_state["history"][0].keys())
    writer.writeheader()
    writer.writerows(st.session_state["history"])
    st.download_button(
        label="📥 履歴をCSVファイルで保存する",
        data=output.getvalue().encode("utf-8-sig"),
        file_name=f"carb_setting_log_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# --- フッター（免責事項） ---
st.divider()
st.caption("""
**【免責事項・ご利用にあたって】**
- 本アプリはバイク好きの個人が制作した非公式の参考ツールです。各メーカー様とは一切関係ありません。
- 提示される番手や調整値は一般的な目安です。車両の個体差、気候、経年劣化等により最適値は異なります。
- 本アプリを参考にした作業・走行によるエンジンの焼き付きや故障等のトラブルについて、制作者は一切の責任を負いかねます。必ず自己責任のもと、安全に配慮してセッティングを行ってください。
""")
