class BikeInfo {
  final String engineType;
  final int defaultCcIndex;
  final String note;
  const BikeInfo({required this.engineType, required this.defaultCcIndex, required this.note});
}

class CarbInfo {
  final String maker;
  final double baseMj;
  final double baseSj;
  final double mjStep;
  final double sjStep;
  final double baseScrew;
  final String screwType;
  final bool baseFor250;
  final String note;
  const CarbInfo({
    required this.maker, required this.baseMj, required this.baseSj,
    required this.mjStep, required this.sjStep, required this.baseScrew,
    required this.screwType, this.baseFor250 = false, required this.note,
  });
}

const List<String> ccList = [
  "50cc (ノーマル)",
  "75〜88cc (定番ボアアップ)",
  "100〜110cc (ミドルチューン)",
  "115〜125cc (ハイチューン/中華125等)",
  "200〜250cc (単気筒・FTR/ボルティー等)",
];

const Map<String, BikeInfo> bikeData = {
  "モンキー / ゴリラ (Z50J/AB27)": BikeInfo(engineType: "4st横型", defaultCcIndex: 1, note: "横型エンジンの王道。フレーム内にキャブが収まるためマニホールド角度とタンク干渉に注意。"),
  "スーパーカブ50 / リトルカブ": BikeInfo(engineType: "4st横型", defaultCcIndex: 0, note: "レッグシールドを残す場合、大型キャブやパワフィルは干渉しやすいためマニホールド選びが重要です。"),
  "スーパーカブ70 / 90 (HA02)": BikeInfo(engineType: "4st横型", defaultCcIndex: 1, note: "純正でビッグフィン・ロングクランク(90)。PC20やPB18〜PD22との相性が抜群です。"),
  "ダックス / シャリー (ST50/CF50)": BikeInfo(engineType: "4st横型", defaultCcIndex: 1, note: "プレスフレーム構造のため、キャブが横出しになる専用インマニを使うケースが多いです。"),
  "マグナ50 / JAZZ": BikeInfo(engineType: "4st横型", defaultCcIndex: 1, note: "12V横型エンジン。車格が大きくロングツーリング向きなので実用域（中間開度）のセッティングが鍵。"),
  "モトラ / CT50 / モンキーR": BikeInfo(engineType: "4st横型", defaultCcIndex: 1, note: "モンキーRは純正でヘッドが優秀。フレーム構造上、キャブのクリアランス確認が必須です。"),
  "エイプ50(AC16) / XR50モタード": BikeInfo(engineType: "4st縦型", defaultCcIndex: 0, note: "縦型エンジン。80ccボアアップ＋PC20やPD22が街乗り定番仕様です。"),
  "エイプ100 / XR100モタード": BikeInfo(engineType: "4st縦型", defaultCcIndex: 2, note: "縦型100ccベース。PD22、PE24、TM-MJN24、FCR28など幅広いキャブが選べます。"),
  "NSF100": BikeInfo(engineType: "4st縦型", defaultCcIndex: 2, note: "スポーツ走行・サーキット志向。高回転域の伸びとパーシャルからのツキを重視したセッティングが人気。"),
  "CB50 / ドリーム50": BikeInfo(engineType: "4st縦型", defaultCcIndex: 0, note: "高回転型の縦型エンジン（ドリーム50はDOHC）。薄め焼き付きに注意し、高回転のMJを丁寧に合わせます。"),
  "FTR223 (MC34)": BikeInfo(engineType: "223cc単気筒", defaultCcIndex: 4, note: "ホンダ空冷単気筒（純正VEキャブはMJ#118・SJ#35〜38付近）。社外パワフィル＋マフラー仕様ではMJ#130〜135前後やPWK28/34・FCR化も人気です。"),
  "ボルティー250 (NJ47A)": BikeInfo(engineType: "250cc単気筒", defaultCcIndex: 4, note: "スズキ空冷250cc単気筒。社外キャブ化ではスロットルワイヤー変更やパワフィル化・2次エアキャンセルの確認が定番です。"),
};

const Map<String, CarbInfo> carbData = {
  "KEIHIN 純正 PB14 (エイプ50等)": CarbInfo(maker: "ケイヒン", baseMj: 78.0, baseSj: 38.0, mjStep: 4.0, sjStep: 3.0, baseScrew: 1.5, screwType: "AS", note: "エイプ50(AC16)純正キャブ。50ccフルノーマルでMJ#62・SJ#35前後、80ccボアアップ+パワフィル等で#78〜82前後が目安。ASはD型ドライバーが必要（純正ニードルは3段調整）。"),
  "KEIHIN 純正 PB16 / PC18": CarbInfo(maker: "ケイヒン", baseMj: 85.0, baseSj: 38.0, mjStep: 5.0, sjStep: 3.0, baseScrew: 1.5, screwType: "PS", note: "エイプ80〜88ccボアアップ＋パワフィル等でMJ#85前後が目安（50ccノーマルは#65前後）。下側のD型スクリュー（PS）は緩めると濃くなります。"),
  "KEIHIN PC20": CarbInfo(maker: "ケイヒン", baseMj: 85.0, baseSj: 35.0, mjStep: 5.0, sjStep: 3.0, baseScrew: 1.5, screwType: "AS", note: "4miniの定番。エアクリ側のマイナスネジがAS（締めると濃くなる）です。"),
  "KEIHIN PE20": CarbInfo(maker: "ケイヒン", baseMj: 90.0, baseSj: 42.0, mjStep: 5.0, sjStep: 2.0, baseScrew: 1.5, screwType: "AS", note: "4mini定番の強制開閉キャブ。ケイヒン丸大MJ使用。※デイトナ製タイプ1/2のエアブリード付SJの場合は#55〜65付近と番手が大きく異なります。"),
  "KEIHIN PE21 (汎用/社外等)": CarbInfo(maker: "ケイヒン/社外", baseMj: 95.0, baseSj: 42.0, mjStep: 5.0, sjStep: 2.0, baseScrew: 1.5, screwType: "AS", note: "21φクラスPE系キャブ。本体仕様（エアブリード有無）によりSJの基準が変わるため現車の番手も要確認。"),
  "KEIHIN PD22": CarbInfo(maker: "ケイヒン", baseMj: 95.0, baseSj: 38.0, mjStep: 5.0, sjStep: 3.0, baseScrew: 1.5, screwType: "PS", note: "エイプ100や90cc系に定番。下側のパイロットスクリュー(PS)は緩めると濃くなります（※一部年式でAS仕様あり）。"),
  "KEIHIN PE24": CarbInfo(maker: "ケイヒン", baseMj: 105.0, baseSj: 38.0, mjStep: 5.0, sjStep: 2.0, baseScrew: 1.5, screwType: "AS", note: "ボアアップ車の超定番。ケイヒン丸大MJを使用。セッティングが出しやすく扱いやすいキャブです。"),
  "KEIHIN PE28": CarbInfo(maker: "ケイヒン", baseMj: 125.0, baseSj: 40.0, mjStep: 5.0, sjStep: 2.0, baseScrew: 1.5, screwType: "AS", note: "100cc超のハイチューン〜250単気筒向け大口径丸型バルブ。中速のツキと高回転の伸びのバランスが良いです。"),
  "KEIHIN PWK28": CarbInfo(maker: "ケイヒン", baseMj: 120.0, baseSj: 38.0, mjStep: 5.0, sjStep: 2.0, baseScrew: 1.5, screwType: "AS", note: "フラットバルブでレスポンス抜群。低開度（SJ〜ニードル）の合わせ込みがシビアになりやすいです。"),
  "PWK34 (KOSO / DIPPER / 汎用)": CarbInfo(maker: "ケイヒンタイプ", baseMj: 115.0, baseSj: 40.0, mjStep: 5.0, sjStep: 2.0, baseScrew: 1.5, screwType: "AS", baseFor250: true, note: "250cc単気筒等に人気のφ34ビッグキャブ（ケイヒン用MJ/SJ互換）。実走ではMJ#110〜115付近で合う例が多いです。パワージェット付きは高回転が濃くなりやすいため注意。"),
  "KEIHIN CR-mini22": CarbInfo(maker: "ケイヒン", baseMj: 95.0, baseSj: 45.0, mjStep: 5.0, sjStep: 3.0, baseScrew: 1.75, screwType: "AS", note: "4ストミニレース定番のCRキャブ。ジェット類はPEと共通です。ASの効きが良く微調整しやすいです。"),
  "KEIHIN FCR28": CarbInfo(maker: "ケイヒン", baseMj: 110.0, baseSj: 45.0, mjStep: 5.0, sjStep: 3.0, baseScrew: 1.5, screwType: "PS", note: "4mini〜250単気筒にも人気のレーシングキャブ（加速ポンプ付）。基本は下側のPS（緩めると濃く）でアイドリング〜極低開度を合わせます。"),
  "MIKUNI VM22 (汎用/中華キット等)": CarbInfo(maker: "ミクニ", baseMj: 95.0, baseSj: 15.0, mjStep: 5.0, sjStep: 2.5, baseScrew: 1.5, screwType: "AS", note: "手軽な中華キットやライトチューン定番。本体ロットによってAS仕様とPS仕様が混在するため、ネジ位置を要確認。"),
  "MIKUNI VM26 (キタコ仕様)": CarbInfo(maker: "ミクニ", baseMj: 150.0, baseSj: 15.0, mjStep: 5.0, sjStep: 2.5, baseScrew: 1.5, screwType: "AS", note: "キタコVM26（4J13ニードル等）基準。ミクニ丸大MJ・VM22/210型SJを使用。"),
  "MIKUNI VM26 (武川仕様)": CarbInfo(maker: "ミクニ", baseMj: 190.0, baseSj: 22.5, mjStep: 10.0, sjStep: 2.5, baseScrew: 1.25, screwType: "AS", note: "武川VM26（5E75ニードル等）基準。インナーパーツの違いでキタコ製よりMJ番号が大きくなります。"),
  "YOSHIMURA TM-MJN24": CarbInfo(maker: "ヨシムラ(ミクニ)", baseMj: 95.0, baseSj: 25.0, mjStep: 2.5, sjStep: 2.5, baseScrew: 0.75, screwType: "AS", note: "フラットバルブ×MJN。ミクニ六角大MJを使用。ASは全閉から3/4回転付近が基準とシビアめです。"),
  "YOSHIMURA YD-MJN24": CarbInfo(maker: "ヨシムラ", baseMj: 85.0, baseSj: 42.0, mjStep: 2.5, sjStep: 3.0, baseScrew: 1.0, screwType: "AS", note: "モンキー用ダウンドラフトMJN。MJNノズルは標準3段目が基準、MJはミクニ六角大、SJはケイヒン系に近い番手体系です。"),
  "YOSHIMURA YD-MJN28": CarbInfo(maker: "ヨシムラ", baseMj: 100.0, baseSj: 45.0, mjStep: 2.5, sjStep: 3.0, baseScrew: 1.0, screwType: "AS", note: "大排気量ヘッド（88〜124cc+ビッグバルブ）向けダウンドラフトMJN。急開よりもスムーズなスロットルワーク向き。"),
};

String fmt(double val) {
  if (val == val.roundToDouble()) return val.toInt().toString();
  return double.parse(val.toStringAsFixed(2)).toString();
}

class BaseSetting {
  final double mj;
  final double sj;
  final int clip;
  final double screw;
  BaseSetting({required this.mj, required this.sj, required this.clip, required this.screw});
}

class DiagnoseResult {
  final double curMj, curSj, curScrew, newMj, newSj, newScrew;
  final int curClip, newClip;
  final String screwLabel;
  final List<String> advices, warnings;
  DiagnoseResult({
    required this.curMj, required this.curSj, required this.curClip, required this.curScrew,
    required this.newMj, required this.newSj, required this.newClip, required this.newScrew,
    required this.screwLabel, required this.advices, required this.warnings,
  });
}

BaseSetting calcBaseSetting({
  required String carbName, required String ccClass, required String headSpec,
  required String airFilter, required String exhaust, required String season,
}) {
  final carb = carbData[carbName]!;
  double mj = carb.baseMj;
  double sj = carb.baseSj;
  const int clip = 3;
  final double screwTurn = carb.baseScrew;

  if (carb.baseFor250) {
    if (ccClass == ccList[0]) { mj -= carb.mjStep * 4; sj -= carb.sjStep * 2; }
    else if (ccClass == ccList[1]) { mj -= carb.mjStep * 3; sj -= carb.sjStep; }
    else if (ccClass == ccList[2]) { mj -= carb.mjStep * 2; sj -= carb.sjStep * 0.5; }
    else if (ccClass == ccList[3]) { mj -= carb.mjStep; }
  } else {
    if (ccClass == ccList[0]) { mj -= carb.mjStep * 2; sj -= carb.sjStep; }
    else if (ccClass == ccList[2]) { mj += carb.mjStep; sj += carb.sjStep * 0.5; }
    else if (ccClass == ccList[3]) { mj += carb.mjStep * 2; sj += carb.sjStep; }
    else if (ccClass == ccList[4]) { mj += carb.mjStep * 3; sj += carb.sjStep * 1.5; }
  }

  if (headSpec == "社外スポーツカムのみ") { mj += carb.mjStep * 0.5; }
  else if (headSpec == "社外ビッグバルブヘッド + ハイカム") { mj += carb.mjStep; sj += carb.sjStep * 0.5; }

  if (airFilter == "純正エアクリーナーBOX") { mj -= carb.mjStep; }
  else if (airFilter == "ファンネル / 直キャブ") { mj += carb.mjStep; }

  if (exhaust == "純正マフラー") { mj -= carb.mjStep; }
  else if (exhaust == "社外レーシング / 抜け重視・直管系") { mj += carb.mjStep; }

  if (season == "夏（暑い・25℃以上）") { mj -= carb.mjStep; }
  else if (season == "冬（寒い・10℃以下）") { mj += carb.mjStep; }

  mj = ((mj * 2).roundToDouble() / 2).clamp(50.0, 300.0);
  sj = ((sj * 2).roundToDouble() / 2).clamp(10.0, 80.0);
  return BaseSetting(mj: mj, sj: sj, clip: clip, screw: screwTurn);
}

DiagnoseResult diagnoseSymptoms({
  required String carbName, required double curMj, required double curSj,
  required int curClip, required double curScrew, required String symLow,
  required String symMid, required String symHigh, required bool otherAfterfire,
  required bool otherSuddenOpen, required bool otherWarmIssue, required String plugColor,
}) {
  final carb = carbData[carbName]!;
  final sType = carb.screwType;
  double newMj = curMj, newSj = curSj, newScrew = curScrew;
  int newClip = curClip;
  final List<String> advices = [], warnings = [];

  if (symHigh.startsWith("濃い")) {
    newMj -= carb.mjStep;
    advices.add("🔺 全開域が濃い症状：MJを1ランク下げます（#${fmt(curMj)} → #${fmt(newMj)}）。");
  } else if (symHigh.startsWith("薄い")) {
    newMj += carb.mjStep;
    advices.add("🔻 全開域が薄い症状：焼き付き防止のためMJを上げます（#${fmt(curMj)} → #${fmt(newMj)}）。");
  }

  if (symMid.startsWith("濃い")) {
    if (curClip > 1) {
      newClip -= 1;
      advices.add("🔺 中間域が濃い症状：クリップを1段「上げ」てニードルを下げます（$curClip段目 → $newClip段目）。");
    } else {
      advices.add("⚠️ 中間域が濃いですが、クリップが既に最上段（1段目）です。MJを下げるか太いニードルを検討してください。");
    }
  } else if (symMid.startsWith("薄い")) {
    if (curClip < 5) {
      newClip += 1;
      advices.add("🔻 中間域が薄い症状：クリップを1段「下げ」てニードルを上げます（$curClip段目 → $newClip段目）。");
    } else {
      advices.add("⚠️ 中間域が薄いですが、クリップが既に最下段（5段目）です。MJを上げるか細いニードルを検討してください。");
    }
  }

  if (sType == "AS") {
    if (symLow.startsWith("濃い")) {
      newScrew += 0.5;
      advices.add("🔺 低開度が濃い症状（AS仕様）：エアスクリューを半回転「開け（緩め）」ます（$curScrew回転 → $newScrew回転戻し）。");
      if (newScrew > 2.5) {
        newSj -= carb.sjStep; newScrew = carb.baseScrew;
        advices.add("💡 ASが2.5回転以上開くため、SJを1ランク下げてASを基準($newScrew回転)に戻すのがベストです（SJ #${fmt(curSj)} → #${fmt(newSj)}）。");
      }
    } else if (symLow.startsWith("薄い")) {
      newScrew -= 0.5;
      final clamped = newScrew < 0.25 ? 0.25 : newScrew;
      advices.add("🔻 低開度が薄い症状（AS仕様）：エアスクリューを半回転「締め」ます（$curScrew回転 → $clamped回転戻し）。");
      if (newScrew < 0.5) {
        newSj += carb.sjStep; newScrew = carb.baseScrew;
        advices.add("💡 ASが0.5回転未満まで締まるため、SJを1ランク上げてASを基準($newScrew回転)に戻すのがベストです（SJ #${fmt(curSj)} → #${fmt(newSj)}）。");
      }
    }
  } else {
    if (symLow.startsWith("濃い")) {
      newScrew -= 0.5;
      final clamped = newScrew < 0.25 ? 0.25 : newScrew;
      advices.add("🔺 低開度が濃い症状（PS仕様）：パイロットスクリューを半回転「締め」ます（$curScrew回転 → $clamped回転戻し）。");
      if (newScrew < 0.75) {
        newSj -= carb.sjStep; newScrew = carb.baseScrew;
        advices.add("💡 PSが0.75回転未満まで締まるため、SJを1ランク下げてPSを基準($newScrew回転)に戻すのがベストです（SJ #${fmt(curSj)} → #${fmt(newSj)}）。");
      }
    } else if (symLow.startsWith("薄い")) {
      newScrew += 0.5;
      advices.add("🔻 低開度が薄い症状（PS仕様）：パイロットスクリューを半回転「開け（緩め）」ます（$curScrew回転 → $newScrew回転戻し）。");
      if (newScrew > 2.5) {
        newSj += carb.sjStep; newScrew = carb.baseScrew;
        advices.add("💡 PSが2.5回転以上開くため、SJを1ランク上げてPSを基準($newScrew回転)に戻すのがベストです（SJ #${fmt(curSj)} → #${fmt(newSj)}）。");
      }
    }
  }

  if (otherAfterfire) {
    if (symLow.startsWith("特になし")) {
      newSj += carb.sjStep;
      advices.add("💥 アフターファイア対策：エンブレ時のスロー燃料不足が疑われるためSJを上げます（#${fmt(curSj)} → #${fmt(newSj)}）。※排気漏れでも鳴るのでフランジ要確認！");
    } else {
      advices.add("💥 アフターファイア：低開度の燃料不足、またはマフラー接続部の排気漏れの可能性があります。");
    }
  }

  if (otherSuddenOpen) {
    if (carbName.contains("FCR")) {
      advices.add("⚡ 急開時の息継ぎ（FCR）：加速ポンプの噴射量・タイミングを見直すと劇的に改善することがあります。");
    } else {
      advices.add("⚡ 急開時の息継ぎ：大口径キャブは急開すると流速が落ちて薄くなりがちです。少しクリップを下げるかスロー系を濃くすると改善します。");
    }
  }

  if (otherWarmIssue) {
    warnings.add("温間時のみの不調は、濃すぎ（カブり）か、「タペットクリアランス不良」「イグニッションコイル熱ダレ」の可能性もあります。");
  }

  if (plugColor.startsWith("真っ白")) {
    if (symHigh.startsWith("特になし")) {
      newMj += carb.mjStep;
      advices.add("🔥 プラグが真っ白なため補正：体感症状がなくても焼け色が薄いため、安全のためMJを上げます（#${fmt(curMj)} → #${fmt(newMj)}）。");
    }
    warnings.add("🚨 プラグが真っ白です！全開走行を続けると焼き付き・ピストン溶損の危険があります。まずMJを上げて様子を見てください。");
  } else if (plugColor.startsWith("真っ黒")) {
    warnings.add("⚫ プラグが黒く湿っています。セッティング前に新品プラグへ交換するか清掃してから再テストしてください。");
  }

  if (advices.isEmpty) {
    advices.add("✅ 大きな不調はありません。$sTypeを1/4回転ずつ回して最もアイドリングが高く安定する位置を探してみてください。");
  }

  newMj = newMj.clamp(50.0, 300.0);
  newSj = newSj.clamp(10.0, 80.0);
  if (newScrew < 0.25) newScrew = 0.25;

  return DiagnoseResult(
    curMj: curMj, curSj: curSj, curClip: curClip, curScrew: curScrew,
    newMj: newMj, newSj: newSj, newClip: newClip, newScrew: newScrew,
    screwLabel: sType, advices: advices, warnings: warnings,
  );
}
