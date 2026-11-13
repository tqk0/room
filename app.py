import streamlit as st

# ページ設定（スマホでも見やすいレイアウト）
st.set_page_config(page_title="4mini キャブセッティング診断", page_icon="🏍️", layout="centered")

# ==========================================
# 【Part 1】マスタデータ定義（ここを増やせば対応車種・キャブが増えます）
# ==========================================

CARB_DATA = {
    "KEIHIN PC20": {
        "maker": "ケイヒン",
        "base_mj": 85.0,
        "base_sj": 35.0,
        "mj_step": 5.0,
        "sj_step": 3.0,  # 35 -> 38 -> 40 -> 42
        "base_as": 1.5,
        "screw_type": "AS",  # エアスクリュー（締める＝濃く、緩める＝薄く）
        "note": "4miniの定番。上側のエアクリ側マイナスネジがAS（締めると濃くなる）です。"
    },
    "KEIHIN PE24": {
        "maker": "ケイヒン",
        "base_mj": 105.0,
        "base_sj": 38.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_as": 1.5,
        "screw_type": "AS",
        "note": "ボアアップ車に人気。丸大メインジェットを使用します。"
    },
    "KEIHIN PWK28": {
        "maker": "ケイヒン",
        "base_mj": 120.0,
        "base_sj": 38.0,
        "mj_step": 5.0,
        "sj_step": 2.0,
        "base_as": 1.5,
        "screw_type": "AS",
        "note": "フラットバルブでレスポンス抜群。低開度(SJ〜ニードル)がシビアになりやすいです。"
    },
    "MIKUNI VM26 (キタコ仕様)": {
        "maker": "ミクニ",
        "base_mj": 150.0,
        "base_sj": 15.0,
        "mj_step": 5.0,
        "sj_step": 2.5,
        "base_as": 1.5,
        "screw_type": "AS",
        "note": "キタコVM26（4J13ニードル等）基準。ミクニ丸大MJ・VM22/210型SJを使用。"
    },
    "MIKUNI VM26 (武川仕様)": {
        "maker": "ミクニ",
        "base_mj": 190.0,
        "base_sj": 22.5,
        "mj_step": 10.0,
        "sj_step": 2.5,
        "base_as": 1.25,
        "screw_type": "AS",
        "note": "武川VM26（5E75ニードル等）基準。インナーパーツの違いでキタコ製よりMJ番号が大きくなります。"
    },
    "YOSHIMURA YD-MJN24": {
        "maker": "ヨシムラ(ミクニ)",
        "base_mj": 95.0,
        "base_sj": 42.0,
        "mj_step": 2.5,
        "sj_step": 2.5,
        "base_as": 1.5,
        "screw_type": "AS",
        "note": "ダウンドラフトMJN。MJNノズルは標準3段目を基準とし、MJはミクニ六角大を使用します。"
    },
}

# 数値フォーマット用（整数なら小数点を消す）
def fmt(val):
    return str(int(val)) if val == int(val) else str(round(val, 2))


# ==========================================
# 【Part 2】推論ロジック（ベース算出 & 症状診断）
# ==========================================

def calc_base_setting(carb_name, cc_class, head_spec, air_filter, exhaust, season):
    carb = CARB_DATA[carb_name]
    mj = carb["base_mj"]
    sj = carb["base_sj"]
    clip = 3  # 標準は上から3段目
    as_turn = carb["base_as"]

    # 排気量補正
    if cc_class == "50cc (ノーマル)":
        mj -= carb["mj_step"] * 2
        sj -= carb["sj_step"]
    elif cc_class == "75〜88cc (定番ボアアップ)":
        pass  # 基準値
    elif cc_class == "105〜124cc (ハイチューン/中華125等)":
        mj += carb["mj_step"] * 2
        sj += carb["sj_step"]

    # ヘッド・カム補正
    if head_spec == "社外ビッグバルブヘッド + ハイカム":
        mj += carb["mj_step"]
        sj += carb["sj_step"] * 0.5  # 少し濃いめ方向

    # エアクリーナー補正（空気の吸いやすさ）
    if air_filter == "純正エアクリーナーBOX":
        mj -= carb["mj_step"]
    elif air_filter == "パワーフィルター":
        pass  # 基準
    elif air_filter == "ファンネル / 直キャブ":
        mj += carb["mj_step"]

    # マフラー補正（排気の抜けやすさ）
    if exhaust == "純正マフラー":
        mj -= carb["mj_step"]
    elif exhaust == "社外マフラー（ストリート/静かめ）":
        pass  # 基準
    elif exhaust == "社外レーシング / 抜け重視・直管系":
        mj += carb["mj_step"]

    # 季節（気温）補正
    if season == "夏（暑い・25℃以上）":
        mj -= carb["mj_step"]
    elif season == "冬（寒い・10℃以下）":
        mj += carb["mj_step"]

    # SJは最小限の丸め処理
    sj = round(sj * 2) / 2  # 0.5刻みに丸める
    return mj, sj, clip, as_turn


def diagnose_symptoms(carb_name, cur_mj, cur_sj, cur_clip, cur_as, sym_low, sym_mid, sym_high, sym_other, plug_color):
    carb = CARB_DATA[carb_name]
    new_mj = cur_mj
    new_sj = cur_sj
    new_clip = cur_clip
    new_as = cur_as
    advices = []
    warnings = []

    # 1. 全開域（3/4〜全開）→ メインジェット (MJ)
    if sym_high == "濃い（ボコつく・重い・黒煙・頭打ち）":
        new_mj -= carb["mj_step"]
        advices.append(f"🔺 **全開域が濃い症状**：MJを1ランク下げます（`#{fmt(cur_mj)}` → `#{fmt(new_mj)}`）。")
    elif sym_high == "薄い（息継ぎ・ガス欠感・高回転が伸びない）":
        new_mj += carb["mj_step"]
        advices.append(f"🔻 **全開域が薄い症状**：焼き付き防止のためMJを上げます（`#{fmt(cur_mj)}` → `#{fmt(new_mj)}`）。")

    # 2. 中間域（1/4〜3/4）→ ジェットニードルクリップ位置
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

    # 3. 低開度・アイドリング（0〜1/4）→ SJ & エアスクリュー
    if sym_low == "濃い（アイドリング不安定・生ガス臭い・カブる）":
        new_as += 0.5
        advices.append(f"🔺 **低開度が濃い症状**：まずエアスクリューを半回転「開け（緩め）」ます（`{cur_as}回転` → `{new_as}回転戻し`）。")
        if new_as > 2.5:
            new_sj -= carb["sj_step"]
            new_as = carb["base_as"]
            advices.append(f"💡 ASが2.5回転以上開くため、**SJを1ランク下げて**ASを基準(`{new_as}回転`)に戻すのがベストです（SJ `#{fmt(cur_sj)}` → `#{fmt(new_sj)}`）。")
    elif sym_low == "薄い（発進で息継ぎ・回転の落ちが遅い）":
        new_as -= 0.5
        advices.append(f"🔻 **低開度が薄い症状**：まずエアスクリューを半回転「締め」ます（`{cur_as}回転` → `{max(0.25, new_as)}回転戻し`）。")
        if new_as < 0.75:
            new_sj += carb["sj_step"]
            new_as = carb["base_as"]
            advices.append(f"💡 ASが0.75回転未満まで締まるため、**SJを1ランク上げて**ASを基準(`{new_as}回転`)に戻すのがベストです（SJ `#{fmt(cur_sj)}` → `#{fmt(new_sj)}`）。")

    # 4. その他症状（アフターファイアなど）
    if "アクセルオフでアフターファイア（パンパン鳴る）" in sym_other:
        if sym_low == "特になし（良好）":
            new_sj += carb["sj_step"]
            advices.append(f"💥 **アフターファイア対策**：エンブレ時のスロー燃料不足が疑われます。SJを上げる提案をしています（`#{fmt(cur_sj)}` → `#{fmt(new_sj)}`）。※マフラーの排気漏れ（フランジ緩み）でもパンパン鳴るので要確認！")
        else:
            advices.append("💥 **アフターファイア**：低開度の燃料が薄い、またはマフラーの排気漏れの可能性があります。")

    if "エンジンが温まると調子が悪くなる" in sym_other:
        warnings.append("温間時のみの不調は、濃すぎ（カブり）か、または「タペットクリアランス不良」「イグニッションコイル熱ダレ」の可能性もあります。")

    # 5. プラグの焼け色チェック
    if plug_color == "真っ白・電極が溶け気味（かなり薄い）":
        warnings.append("🚨 **プラグが真っ白です！** そのまま全開走行すると焼き付き・ピストン穴あきの危険があります。まずMJを大きめ（+1〜2ランク）に振ってください。")
    elif plug_color == "真っ黒で湿っている（かなり濃い）":
        warnings.append("⚫ **プラグが黒く湿っています。** セッティング前に新しいプラグに交換するか綺麗に清掃してから再テストしてください（カブったままでは正確な診断ができません）。")

    if not advices:
        advices.append("✅ 大きな不調が選択されていません。微調整（ASを1/4回転ずつ回して最もアイドリングが高い位置を探す等）を行ってください。")

    return new_mj, new_sj, new_clip, max(0.25, new_as), advices, warnings


# ==========================================
# 【Part 3】画面UI（ブラウザ表示部分）
# ==========================================

st.title("🏍️ 4mini キャブセッティング診断アプリ")
st.caption("モンキー / ゴリラ / カブ / ダックス / シャリー / エイプ 対応プロトタイプ")

# --- 1. マシン仕様入力 ---
st.header("1. 車体・エンジン・吸排気の仕様")
col1, col2 = st.columns(2)
with col1:
    bike_model = st.selectbox("車種", ["モンキー / ゴリラ", "スーパーカブ系", "ダックス / シャリー", "エイプ (縦型)"])
    cc_class = st.selectbox("排気量", ["50cc (ノーマル)", "75〜88cc (定番ボアアップ)", "105〜124cc (ハイチューン/中華125等)"], index=1)
    head_spec = st.selectbox("ヘッド・カム詳細", ["純正ヘッド（ノーマル/ライトボア）", "社外ビッグバルブヘッド + ハイカム"])

with col2:
    carb_name = st.selectbox("キャブレター", list(CARB_DATA.keys()))
    air_filter = st.selectbox("エアクリーナー", ["純正エアクリーナーBOX", "パワーフィルター", "ファンネル / 直キャブ"], index=1)
    exhaust = st.selectbox("エキパイ・サイレンサー", ["純正マフラー", "社外マフラー（ストリート/静かめ）", "社外レーシング / 抜け重視・直管系"], index=1)

season = st.radio("現在の気温環境", ["夏（暑い・25℃以上）", "春・秋（標準・10〜25℃）", "冬（寒い・10℃以下）"], index=1, horizontal=True)

st.info(f"🔧 **キャブ豆知識**：{CARB_DATA[carb_name]['note']}")

# ベースセッティング計算・表示
base_mj, base_sj, base_clip, base_as = calc_base_setting(carb_name, cc_class, head_spec, air_filter, exhaust, season)

with st.expander("📊 この仕様の「基準（初期）セッティング」目安を見る", expanded=True):
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("基準 MJ", f"#{fmt(base_mj)}")
    b2.metric("基準 SJ", f"#{fmt(base_sj)}")
    b3.metric("ニードルクリップ", f"上から {base_clip}段目")
    b4.metric("AS 戻し", f"{base_as} 回転")
    st.caption("※あくまでスタート地点の目安です。安全のため、迷ったら基準より少し濃いめ（MJ+5〜10）から始めてください。")

st.divider()

# --- 2. 現状セッティング＆症状入力 ---
st.header("2. 現状のセッティングと症状")

c1, c2, c3, c4 = st.columns(4)
with c1:
    cur_mj = st.number_input("現在の MJ (#)", min_value=50.0, max_value=300.0, value=float(base_mj), step=2.5)
with c2:
    cur_sj = st.number_input("現在の SJ (#)", min_value=10.0, max_value=80.0, value=float(base_sj), step=0.5)
with c3:
    cur_clip = st.selectbox("クリップ位置（上から）", [1, 2, 3, 4, 5], index=2)
with c4:
    cur_as = st.number_input("AS戻し回転数", min_value=0.0, max_value=4.0, value=float(base_as), step=0.25)

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
    "エンジンが温まると調子が悪くなる"
])

plug_color = st.selectbox("プラグの焼け色（確認できた場合）", [
    "未確認 / きつね色（良好）",
    "真っ白・電極が溶け気味（かなり薄い）",
    "真っ黒で湿っている（かなり濃い）"
])

# --- 3. 診断ボタン＆結果表示 ---
if st.button("🔍 次の推奨セッティングを診断する", type="primary", use_container_width=True):
    new_mj, new_sj, new_clip, new_as, advices, warnings = diagnose_symptoms(
        carb_name, cur_mj, cur_sj, cur_clip, cur_as,
        sym_low, sym_mid, sym_high, sym_other, plug_color
    )

    st.divider()
    st.header("🎯 次の推奨セッティング案")

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("推奨 MJ", f"#{fmt(new_mj)}", delta=fmt(new_mj - cur_mj) if new_mj != cur_mj else None)
    r2.metric("推奨 SJ", f"#{fmt(new_sj)}", delta=fmt(new_sj - cur_sj) if new_sj != cur_sj else None)
    r3.metric("クリップ位置", f"{new_clip}段目", delta=f"{new_clip - cur_clip}段" if new_clip != cur_clip else None)
    r4.metric("AS 戻し", f"{new_as} 回転", delta=f"{round(new_as - cur_as, 2)}" if new_as != cur_as else None)

    st.subheader("📝 調整のポイント")
    for adv in advices:
        st.markdown(f"- {adv}")

    if warnings:
        for warn in warnings:
            st.error(warn)

    st.warning("⚠️ **セッティングの鉄則**：ジェット類は「1箇所ずつ」変更して試走すると原因が迷子になりにくいです。また、2次エア吸い（マニホールドの隙間）や油面狂いがあるとセッティングが出ないのでご注意ください。")