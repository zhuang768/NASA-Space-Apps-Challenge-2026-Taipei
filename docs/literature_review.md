# 既有方案與文獻搜尋紀錄

查核：2026-11-14。這是有限的公開網頁檢索，不是系統性文獻回顧。沒有新增候選地層／礦物查證。

## 可以確定的先行工作

| 來源 | 已解決什麼 | 本版怎麼使用／不能借用什麼 |
|---|---|---|
| [NASA Planetary Analog Explorer](https://science.nasa.gov/solar-system/analog-explorer/) | 已知場址的跨天體影像比較、科學問題與來源說明 | 對照產品定位；不能宣稱跨星球比較或已知類比展示是我們首創 |
| [NASA Solar System Treks](https://trek.nasa.gov/) | 行星觀測資料檢視、地表量測、3D探索 | 提供可供後續覆核的工具；不虛構它缺少某項功能 |
| [NASA Earth Observatory：Curiosity與Death Valley](https://science.nasa.gov/earth/earth-observatory/mars-rover-curiosity-on-a-familiar-landscape-78860/) | 描述Gale與Death Valley的沉積地貌參照，同時強調年代與活動性差異 | 支持選Death Valley作已知區域參照；不是任選窗口的DEM ground truth |
| [Salas et al., 2011，NTRS 20150005824](https://ntrs.nasa.gov/citations/20150005824) | Mojave／Death Valley的任務類比用途與環境多樣性 | 本輪讀取NTRS紀錄／摘要，紀錄無可下載全文；不冒稱全文驗證 |
| [Baldridge et al., 2004](https://doi.org/10.1029/2004JE002315) | 用地面礦物檢測核對Badwater遙測解釋，並測試空間尺度影響 | 已讀原始論文摘要與方法開頭；借用地面真值與尺度驗證原則，未重現其光譜分析 |

本版可主張的工程成果是公開可重現的稀疏地形搜尋、共同物理尺度與來源紀錄。優於既有工具的研究效益尚待對照，不由畫面推定。

## 實際檢索紀錄

工具：公開web search，多查詢批次回傳；回傳結果並非完整資料庫，不能把沒有命中說成沒有研究。日期均為2026-11-14。

| 查詢 | 本輪觀察 | 處理 |
|---|---|---|
| `site.nasa.gov "Death Valley" "analog" Mars` | NASA／JPL／NTRS及其他結果 | 只用上列原始機構與論文；作參照選擇依據 |
| `"Oytag" "Mars" analog`、`"Wuyitake" "Mars" analog` | 混合檢索未取得可確認的學術類比紀錄 | 僅作初步新穎性查核，非地質續查 |
| `"Oytag" "Mars"`、`"Oytagh" "Mars"`、`"Wuyitake" "Mars"`、`"Oytag" "planetary analog"` | 批次回傳以旅遊宣傳的Mars-like用語及無關同名資料為主，未取得可確認的同行評審類比研究 | 排除旅遊宣傳作科學證據；不排除以其他地名存在研究 |

未完成：中文別名（奥依塔克等）、Pamir／Tarim廣域詞、區域其他名稱、學術資料庫及引用追蹤的完整查核。因使用者暫停第三項候選深查，本輪不擴大。墨西哥與伊朗的既有類比研究史也未在這輪調查。

統一可用文字：**「本專案以資料流程提出、尚待進一步驗證的候選區域」**。不可用「從未研究」「全球首創」「新發現礦床」。

## 有限數值參照的結果

依[實際輸出](../outputs/research/reference_terrain_check.json)：

| 設計區域中心 | 坡度中位數 ° | 坡度P90 ° | 起伏 m | Gale D | Arcadia D |
|---|---:|---:|---:|---:|---:|
| Death Valley：36.25N,116.82W | 2.9660 | 7.6609 | 2455.70 | 3.0152 | 2.7490 |
| Amazon：3S,61W | 0.0610 | 0.1731 | 55.65 | 7.0775 | 1.3132 |

兩者取樣陸地比例均1.0，但粗陸地遮罩不會排除所有河湖。Mars三目標由原始MOLA重新計算，與儲存特徵在程式容許誤差內一致；距離分項加總也吻合。

Death Valley相對本輪低起伏對照的Gale D較低；Arcadia反而更接近低起伏對照。這符合地形指標只測地形的定義，不能解讀為Amazon是較佳的冰或火星環境類比。只有兩個參照，不足以校準閾值、宣稱辨識準確率或證明新候選優於已知場址。未新增或修改正式候選排名。
