# 目前採用的研究資料與處置（2026-11-15）

- 正式報告由人類撰寫；本頁只提供引用次序、資料狀態及條列修正，不生成正文、摘要或結論。
- 固定來源 main：`08d2740a23694a54bcc11cabf7120114d2e120fc`。三個研究 PR #6、#7、#8均已合併；本頁的完整來源SHA與檔案定位見機讀快照。
- 引用順序：本頁／current_snapshot → MS-02完整16項修正清單 → 各點最新local_validation與後續補充 → 僅作歷史參考的舊報告。
- 舊驗收與舊整合的自動檢查只對當時版本有效；本次不宣稱已重跑全部原始資料、完成冰偵測或部署成功。

| 點 | 已有條件式模型冰深 | 最新取得狀態 | 仍未知／不得引用 |
|---|---|---|---|
| MS-01 | 約0.427m | 6景THEMIS與共同格點支持、16格TES反照率、64欄雷達回波／雜波窗口 | 投影原點、觀測條件與材料仍混淆；無唯一冰界面，真實冰存在／深度／含量未知 |
| MS-02 | 約0.45m | 原始GIS全格mAl；3雷達段194欄；CRISM912個中心；5CTX browse | 雷達冰解釋、光譜完整校正與CTX配準未完成；不把CS-1/ADE/WISDOM拼同址 |
| MS-03 | 約0.10m | 原始GIS為AHv；兩組局部CRISM+DDR+WA；基本QA通過966／8516個中心 | 基本QA不是冰檢出；雲霜／大氣校正、冰指數與可靠閉合形貌邊界尚缺，AD1維持降級 |

- 三個模型值均以假設下層為冰為前提，不是實測冰深，也不能由SWIM換成含量／機率。
- MS-01原三景中心無有效值與後續新取得景的中心有效，是不同取得範圍；不可繼續泛稱所有景中心皆無效。
- MS-02 Beacon僅Liu2018熱學／材料子案例，沒有原始序列；Haughton僅挖除約0.9m活動層後的同測線GPR／岩芯方法子案例，不是未擾動覆土或SHARAD驗證。
- MS-03原「CRISM只有標籤、無cube」已被兩組局部原始光譜取代；不能因此寫成已取得完整全條帶、已校正或已確認冰。
- University Valley獨立物性與合格無冰控制仍缺；W站42cm冰表與約15cm活動層不同；S/D座標與跨logger時鐘問題仍未解。
- MCS來源為校時地表溫度產品，變數tsurf_correct；舊稿將其叫大氣溫度須刪改。5°粗尺度背景仍不能當MS-01～03當地實測，配對差中位數也不是同sol日夜振幅。來源：https://zenodo.org/records/17947556 。
- MS-02 PR #12為另行文件修正，尚未合併時不可稱其8檔修正已在main；不影響本頁對科學未知的保留。
- 禁用：地球衰減直接換火星冰深；Adventdalen跨址拼接；AD1恢復具體MS-03配對；一致性當機率／冰量；搜尋無命中當從未研究；未取得或未檢出當無冰。
- 手寫報告清理清單：先逐項對照MS-02的16項修正；清除「只剩標籤」「地質單元皆未知」「handoff兩檔尚未進main」「MCS大氣溫度」的過時概括。舊報告保留歷史身份，不直接當本輪人類正式稿。

- MS-01來源：https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/08d2740a23694a54bcc11cabf7120114d2e120fc/docs/research/MS-01/local_validation/research_notes.md；https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/08d2740a23694a54bcc11cabf7120114d2e120fc/docs/research/MS-01/local_validation/constraints_followup_notes.md

- MS-02來源：https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/08d2740a23694a54bcc11cabf7120114d2e120fc/docs/research/MS-02/local_validation/research_notes.md；https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/08d2740a23694a54bcc11cabf7120114d2e120fc/outputs/research/MS-02/local_validation/claim_corrections.csv

- MS-03來源：https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei/blob/08d2740a23694a54bcc11cabf7120114d2e120fc/docs/research/MS-03/local_validation/research_notes.md
