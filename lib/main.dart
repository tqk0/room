import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'carb_data.dart';

void main() => runApp(const CarbSettingApp());

class CarbSettingApp extends StatelessWidget {
  const CarbSettingApp({super.key});
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: '4miniキャブ診断',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepOrange), useMaterial3: true),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _tabIndex = 0;
  String _bikeModel = bikeData.keys.first;
  String _ccClass = ccList[1];
  String _headSpec = "純正ヘッド・純正カム";
  String _carbName = "KEIHIN PC20";
  String _airFilter = "パワーフィルター";
  String _exhaust = "社外マフラー（ストリート/静かめ）";
  String _season = "春・秋（標準・10〜25℃）";

  final _mjCtrl = TextEditingController();
  final _sjCtrl = TextEditingController();
  final _screwCtrl = TextEditingController();
  final _memoCtrl = TextEditingController();
  int _curClip = 3;

  String _symLow = "特になし（良好）";
  String _symMid = "特になし（良好）";
  String _symHigh = "特になし（良好）";
  bool _otherAfterfire = false;
  bool _otherSuddenOpen = false;
  bool _otherWarmIssue = false;
  String _plugColor = "未確認 / きつね色（良好）";

  DiagnoseResult? _lastResult;
  List<Map<String, dynamic>> _history = [];

  static const _symLowList = ["特になし（良好）", "濃い（アイドリング不安定・生ガス臭い・カブる）", "薄い（発進で息継ぎ・回転の落ちが遅い）"];
  static const _symMidList = ["特になし（良好）", "濃い（ボコつく・吹け上がりが重い）", "薄い（ツキが悪い・パーシャルで息継ぎ）"];
  static const _symHighList = ["特になし（良好）", "濃い（ボコつく・重い・黒煙・頭打ち）", "薄い（息継ぎ・ガス欠感・高回転が伸びない）"];
  static const _plugList = ["未確認 / きつね色（良好）", "真っ白・電極が溶け気味（かなり薄い）", "真っ黒で湿っている（かなり濃い）"];

  @override
  void initState() {
    super.initState();
    _syncBaseInputs();
    _loadHistory();
  }

  @override
  void dispose() {
    _mjCtrl.dispose(); _sjCtrl.dispose(); _screwCtrl.dispose(); _memoCtrl.dispose();
    super.dispose();
  }

  BaseSetting _getBase() => calcBaseSetting(
    carbName: _carbName, ccClass: _ccClass, headSpec: _headSpec,
    airFilter: _airFilter, exhaust: _exhaust, season: _season,
  );

  void _syncBaseInputs() {
    final base = _getBase();
    _mjCtrl.text = fmt(base.mj);
    _sjCtrl.text = fmt(base.sj);
    _screwCtrl.text = fmt(base.screw);
    _curClip = base.clip;
  }

  Future<void> _loadHistory() async {
    final prefs = await SharedPreferences.getInstance();
    final raw = prefs.getString('carb_history_v1');
    if (raw != null) {
      try {
        final decoded = jsonDecode(raw) as List<dynamic>;
        setState(() => _history = decoded.map((e) => Map<String, dynamic>.from(e)).toList());
      } catch (_) {}
    }
  }

  Future<void> _saveHistoryToDevice() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('carb_history_v1', jsonEncode(_history));
  }

  void _stepController(TextEditingController ctrl, double delta, double min, double max) {
    final current = double.tryParse(ctrl.text) ?? min;
    setState(() => ctrl.text = fmt((current + delta).clamp(min, max)));
  }

  void _runDiagnosis() {
    FocusScope.of(context).unfocus();
    final base = _getBase();
    final res = diagnoseSymptoms(
      carbName: _carbName,
      curMj: double.tryParse(_mjCtrl.text) ?? base.mj,
      curSj: double.tryParse(_sjCtrl.text) ?? base.sj,
      curClip: _curClip,
      curScrew: double.tryParse(_screwCtrl.text) ?? base.screw,
      symLow: _symLow, symMid: _symMid, symHigh: _symHigh,
      otherAfterfire: _otherAfterfire, otherSuddenOpen: _otherSuddenOpen,
      otherWarmIssue: _otherWarmIssue, plugColor: _plugColor,
    );
    setState(() => _lastResult = res);
  }

  Future<void> _addHistory() async {
    if (_lastResult == null) return;
    final r = _lastResult!;
    final now = DateTime.now();
    final dateStr = "${now.year}/${now.month.toString().padLeft(2, '0')}/${now.day.toString().padLeft(2, '0')} ${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}";
    setState(() {
      _history.insert(0, {
        "date": dateStr, "bike": _bikeModel, "cc": _ccClass, "carb": _carbName,
        "air": _airFilter, "exhaust": _exhaust,
        "cur": "MJ#${fmt(r.curMj)} / SJ#${fmt(r.curSj)} / ${r.curClip}段 / ${r.screwLabel}${fmt(r.curScrew)}",
        "rec": "MJ#${fmt(r.newMj)} / SJ#${fmt(r.newSj)} / ${r.newClip}段 / ${r.screwLabel}${fmt(r.newScrew)}",
        "plug": _plugColor, "memo": _memoCtrl.text.trim(),
      });
      _memoCtrl.clear();
    });
    await _saveHistoryToDevice();
    if (mounted) {
      FocusScope.of(context).unfocus();
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text("スマホにセッティング履歴を保存しました！")));
    }
  }

  Future<void> _deleteHistory(int idx) async {
    setState(() => _history.removeAt(idx));
    await _saveHistoryToDevice();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_tabIndex == 0 ? "🏍️ 4miniキャブ診断" : "📒 セッティング履歴 (${_history.length})"),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
      ),
      body: _tabIndex == 0 ? _buildDiagnosisTab() : _buildHistoryTab(),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _tabIndex,
        onDestinationSelected: (idx) => setState(() => _tabIndex = idx),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.build_outlined), selectedIcon: Icon(Icons.build), label: "診断"),
          NavigationDestination(icon: Icon(Icons.history_outlined), selectedIcon: Icon(Icons.history), label: "履歴メモ"),
        ],
      ),
    );
  }

  Widget _buildDiagnosisTab() {
    final bikeInfo = bikeData[_bikeModel]!;
    final carbInfo = carbData[_carbName]!;
    final base = _getBase();
    final screwLabel = carbInfo.screwType;

    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          const Text("1. 車体・エンジン・吸排気の仕様", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          _buildDropdown("車種", _bikeModel, bikeData.keys.toList(), (val) {
            if (val == null) return;
            setState(() { _bikeModel = val; _ccClass = ccList[bikeData[val]!.defaultCcIndex]; _syncBaseInputs(); });
          }),
          const SizedBox(height: 10),
          _buildDropdown("排気量", _ccClass, ccList, (val) {
            if (val == null) return;
            setState(() { _ccClass = val; _syncBaseInputs(); });
          }),
          const SizedBox(height: 10),
          _buildDropdown("ヘッド・カム詳細", _headSpec, const ["純正ヘッド・純正カム", "社外スポーツカムのみ", "社外ビッグバルブヘッド + ハイカム"], (val) {
            if (val == null) return;
            setState(() { _headSpec = val; _syncBaseInputs(); });
          }),
          const SizedBox(height: 10),
          _buildDropdown("キャブレター", _carbName, carbData.keys.toList(), (val) {
            if (val == null) return;
            setState(() { _carbName = val; _syncBaseInputs(); });
          }),
          const SizedBox(height: 10),
          _buildDropdown("エアクリーナー", _airFilter, const ["純正エアクリーナーBOX", "パワーフィルター", "ファンネル / 直キャブ"], (val) {
            if (val == null) return;
            setState(() { _airFilter = val; _syncBaseInputs(); });
          }),
          const SizedBox(height: 10),
          _buildDropdown("エキパイ・サイレンサー", _exhaust, const ["純正マフラー", "社外マフラー（ストリート/静かめ）", "社外レーシング / 抜け重視・直管系"], (val) {
            if (val == null) return;
            setState(() { _exhaust = val; _syncBaseInputs(); });
          }),
          const SizedBox(height: 12),
          const Text("現在の気温環境", style: TextStyle(fontSize: 13, color: Colors.black54)),
          const SizedBox(height: 6),
          Wrap(
            spacing: 8,
            children: ["夏（暑い・25℃以上）", "春・秋（標準・10〜25℃）", "冬（寒い・10℃以下）"].map((s) => ChoiceChip(
              label: Text(s, style: const TextStyle(fontSize: 12)),
              selected: _season == s,
              onSelected: (_) => setState(() { _season = s; _syncBaseInputs(); }),
            )).toList(),
          ),
          const SizedBox(height: 12),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(color: Colors.blue.shade50, borderRadius: BorderRadius.circular(10), border: Border.all(color: Colors.blue.shade200)),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text("🏍️ ${bikeInfo.engineType}：${bikeInfo.note}", style: const TextStyle(fontSize: 13)),
                const SizedBox(height: 6),
                Text("🔧 $_carbName：${carbInfo.note}", style: const TextStyle(fontSize: 13)),
              ],
            ),
          ),
          const SizedBox(height: 12),
          Card(
            color: Colors.orange.shade50,
            child: Padding(
              padding: const EdgeInsets.all(14),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text("📊 この仕様の「基準セッティング」目安", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
                  const SizedBox(height: 10),
                  Row(children: [
                    Expanded(child: _metricBox("基準 MJ", "#${fmt(base.mj)}")),
                    const SizedBox(width: 8),
                    Expanded(child: _metricBox("基準 SJ", "#${fmt(base.sj)}")),
                  ]),
                  const SizedBox(height: 8),
                  Row(children: [
                    Expanded(child: _metricBox("クリップ(上から)", "${base.clip}段目")),
                    const SizedBox(width: 8),
                    Expanded(child: _metricBox("$screwLabel 戻し", "${fmt(base.screw)} 回転")),
                  ]),
                ],
              ),
            ),
          ),
          const Divider(height: 32),
          const Text("2. 現状のセッティングと症状", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          Row(children: [
            Expanded(child: _stepperInput("現在の MJ (#)", _mjCtrl, carbInfo.mjStep, 50, 300)),
            const SizedBox(width: 10),
            Expanded(child: _stepperInput("現在の SJ (#)", _sjCtrl, carbInfo.sjStep, 10, 80)),
          ]),
          const SizedBox(height: 10),
          Row(
            crossAxisAlignment: CrossAxisAlignment.end,
            children: [
              Expanded(
                child: InputDecorator(
                  decoration: const InputDecoration(labelText: "クリップ(上から)", border: OutlineInputBorder(), isDense: true, contentPadding: EdgeInsets.symmetric(horizontal: 12, vertical: 6)),
                  child: DropdownButtonHideUnderline(
                    child: DropdownButton<int>(
                      value: _curClip, isExpanded: true, isDense: true,
                      items: [1, 2, 3, 4, 5].map((e) => DropdownMenuItem(value: e, child: Text("$e段目"))).toList(),
                      onChanged: (val) { if (val != null) setState(() => _curClip = val); },
                    ),
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(child: _stepperInput("$screwLabel 戻し回転", _screwCtrl, 0.25, 0, 4)),
            ],
          ),
          const SizedBox(height: 14),
          _buildDropdown("【低開度 0〜1/4】アイドリング〜発進", _symLow, _symLowList, (v) { if (v != null) setState(() => _symLow = v); }),
          const SizedBox(height: 10),
          _buildDropdown("【中開度 1/4〜3/4】巡航・加速中", _symMid, _symMidList, (v) { if (v != null) setState(() => _symMid = v); }),
          const SizedBox(height: 10),
          _buildDropdown("【全開域 3/4〜全開】最高速付近", _symHigh, _symHighList, (v) { if (v != null) setState(() => _symHigh = v); }),
          const SizedBox(height: 8),
          CheckboxListTile(title: const Text("アクセルオフでアフターファイア（パンパン鳴る）", style: TextStyle(fontSize: 14)), value: _otherAfterfire, dense: true, contentPadding: EdgeInsets.zero, onChanged: (v) => setState(() => _otherAfterfire = v ?? false)),
          CheckboxListTile(title: const Text("急開すると一瞬息継ぎする（ツキが悪い）", style: TextStyle(fontSize: 14)), value: _otherSuddenOpen, dense: true, contentPadding: EdgeInsets.zero, onChanged: (v) => setState(() => _otherSuddenOpen = v ?? false)),
          CheckboxListTile(title: const Text("エンジンが温まると調子が悪くなる", style: TextStyle(fontSize: 14)), value: _otherWarmIssue, dense: true, contentPadding: EdgeInsets.zero, onChanged: (v) => setState(() => _otherWarmIssue = v ?? false)),
          const SizedBox(height: 8),
          _buildDropdown("プラグの焼け色", _plugColor, _plugList, (v) { if (v != null) setState(() => _plugColor = v); }),
          const SizedBox(height: 16),
          FilledButton.icon(
            onPressed: _runDiagnosis, icon: const Icon(Icons.search),
            label: const Padding(padding: EdgeInsets.symmetric(vertical: 14), child: Text("次の推奨セッティングを診断する", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold))),
          ),
          if (_lastResult != null) ...[
            const Divider(height: 36),
            const Text("🎯 次の推奨セッティング案", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 10),
            Row(children: [
              Expanded(child: _resultBox("推奨 MJ", "#${fmt(_lastResult!.newMj)}", _deltaStr(_lastResult!.newMj - _lastResult!.curMj, ""))),
              const SizedBox(width: 8),
              Expanded(child: _resultBox("推奨 SJ", "#${fmt(_lastResult!.newSj)}", _deltaStr(_lastResult!.newSj - _lastResult!.curSj, ""))),
            ]),
            const SizedBox(height: 8),
            Row(children: [
              Expanded(child: _resultBox("クリップ(上から)", "${_lastResult!.newClip}段目", _deltaStr((_lastResult!.newClip - _lastResult!.curClip).toDouble(), "段"))),
              const SizedBox(width: 8),
              Expanded(child: _resultBox("${_lastResult!.screwLabel} 戻し", "${fmt(_lastResult!.newScrew)}回転", _deltaStr(_lastResult!.newScrew - _lastResult!.curScrew, "回転"))),
            ]),
            const SizedBox(height: 14),
            const Text("📝 調整のポイント", style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15)),
            const SizedBox(height: 6),
            ..._lastResult!.advices.map((a) => Padding(padding: const EdgeInsets.only(bottom: 6), child: Text("• $a", style: const TextStyle(fontSize: 14)))),
            if (_lastResult!.warnings.isNotEmpty) ...[
              const SizedBox(height: 8),
              ..._lastResult!.warnings.map((w) => Container(
                margin: const EdgeInsets.only(bottom: 8), padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: Colors.red.shade50, borderRadius: BorderRadius.circular(8), border: Border.all(color: Colors.red.shade300)),
                child: Text(w, style: TextStyle(color: Colors.red.shade900, fontWeight: FontWeight.w500)),
              )),
            ],
            const SizedBox(height: 12),
            TextField(controller: _memoCtrl, decoration: const InputDecoration(labelText: "試走メモ（任意）", hintText: "例：MJ85にしたら中〜高回転が綺麗に吹けた！", border: OutlineInputBorder())),
            const SizedBox(height: 10),
            OutlinedButton.icon(onPressed: _addHistory, icon: const Icon(Icons.save_alt), label: const Padding(padding: EdgeInsets.symmetric(vertical: 12), child: Text("このセッティングをスマホの履歴に保存する"))),
          ],
          const SizedBox(height: 24),
          const Text("※本アプリの提示値は目安です。実際のセッティングや走行は自己責任で行ってください（2次エア吸い・油面狂いにもご注意）。", style: TextStyle(fontSize: 12, color: Colors.black54)),
          const SizedBox(height: 20),
        ],
      ),
    );
  }

  Widget _buildHistoryTab() {
    if (_history.isEmpty) {
      return const Center(child: Padding(padding: EdgeInsets.all(24), child: Text("まだ保存された履歴がありません。\n「診断」タブで診断したあとに保存ボタンを押すと、ここにずっと残ります！", textAlign: TextAlign.center, style: TextStyle(color: Colors.black54, fontSize: 15))));
    }
    return ListView.builder(
      padding: const EdgeInsets.all(12),
      itemCount: _history.length,
      itemBuilder: (context, idx) {
        final item = _history[idx];
        return Card(
          margin: const EdgeInsets.only(bottom: 10),
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(children: [
                  Expanded(child: Text("${item['date']}  |  ${item['bike']}", style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13))),
                  IconButton(icon: const Icon(Icons.delete_outline, color: Colors.grey), onPressed: () => _deleteHistory(idx), tooltip: "削除"),
                ]),
                Text("${item['carb']} (${item['cc']})", style: const TextStyle(fontSize: 13, color: Colors.black87)),
                Text("${item['air']} / ${item['exhaust']}", style: const TextStyle(fontSize: 12, color: Colors.black54)),
                const SizedBox(height: 6),
                Text("現状：${item['cur']}", style: const TextStyle(fontSize: 13)),
                Text("推奨：${item['rec']}", style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: Colors.deepOrange)),
                Text("プラグ：${item['plug']}", style: const TextStyle(fontSize: 12, color: Colors.black54)),
                if ((item['memo'] ?? "").toString().isNotEmpty) ...[
                  const SizedBox(height: 6),
                  Container(width: double.infinity, padding: const EdgeInsets.all(8), decoration: BoxDecoration(color: Colors.grey.shade100, borderRadius: BorderRadius.circular(6)), child: Text("メモ：${item['memo']}", style: const TextStyle(fontSize: 13))),
                ],
              ],
            ),
          ),
        );
      },
    );
  }

  String _deltaStr(double diff, String unit) => diff.abs() < 0.01 ? "" : "${diff > 0 ? '+' : ''}${fmt(diff)}$unit";

  Widget _buildDropdown(String label, String value, List<String> items, ValueChanged<String?> onChanged) {
    return InputDecorator(
      decoration: InputDecoration(labelText: label, border: const OutlineInputBorder(), isDense: true, contentPadding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6)),
      child: DropdownButtonHideUnderline(
        child: DropdownButton<String>(
          value: value, isExpanded: true, isDense: true,
          items: items.map((e) => DropdownMenuItem(value: e, child: Text(e, overflow: TextOverflow.ellipsis))).toList(),
          onChanged: onChanged,
        ),
      ),
    );
  }

  Widget _metricBox(String label, String value) => Container(
    padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 10),
    decoration: BoxDecoration(color: Colors.white, borderRadius: BorderRadius.circular(8), border: Border.all(color: Colors.orange.shade200)),
    child: Column(children: [Text(label, style: const TextStyle(fontSize: 12, color: Colors.black54)), const SizedBox(height: 2), Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold))]),
  );

  Widget _resultBox(String label, String value, String delta) => Container(
    padding: const EdgeInsets.symmetric(vertical: 10, horizontal: 10),
    decoration: BoxDecoration(color: Colors.deepOrange.shade50, borderRadius: BorderRadius.circular(8), border: Border.all(color: Colors.deepOrange.shade200)),
    child: Column(children: [Text(label, style: const TextStyle(fontSize: 12, color: Colors.black54)), const SizedBox(height: 2), Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.deepOrange)), if (delta.isNotEmpty) Text("($delta)", style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold))]),
  );

  Widget _stepperInput(String label, TextEditingController ctrl, double step, double min, double max) => Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text(label, style: const TextStyle(fontSize: 12, color: Colors.black54)),
      const SizedBox(height: 4),
      Row(children: [
        SizedBox(width: 36, height: 40, child: OutlinedButton(style: OutlinedButton.styleFrom(padding: EdgeInsets.zero), onPressed: () => _stepController(ctrl, -step, min, max), child: const Icon(Icons.remove, size: 18))),
        const SizedBox(width: 4),
        Expanded(child: TextField(controller: ctrl, keyboardType: const TextInputType.numberWithOptions(decimal: true), textAlign: TextAlign.center, decoration: const InputDecoration(border: OutlineInputBorder(), isDense: true, contentPadding: EdgeInsets.symmetric(vertical: 10, horizontal: 4)))),
        const SizedBox(width: 4),
        SizedBox(width: 36, height: 40, child: OutlinedButton(style: OutlinedButton.styleFrom(padding: EdgeInsets.zero), onPressed: () => _stepController(ctrl, step, min, max), child: const Icon(Icons.add, size: 18))),
      ]),
    ],
  );
}
