# 火星端資料交接

本輪只處理火星資料。地球端下載、QA、特徵處理與配對交由隊友。
profiles.json 保留單位、缺值、來源及方法；這些描述值不是綜合相似度或任務成功率。

| 目標 | 火星 lat, lon | 地形 | TES 排除插值後有效比例 | SWIM 0–1 m 平均一致性 | MY34 / MY35 平均 CDOD |
|---|---|---|---|---|---|
| jezero | 18.44, 77.45 | available | 0.9861 | -0.2776 | 0.3153 / 0.1920 |
| gale | -4.59, 137.44 | available | 0.9775 | 0.0813 | 0.2971 / 0.1700 |
| arcadia | 40.0, -170.0 | available | 0.9439 | 0.1145 | 0.2194 / 0.1604 |

## MEDA 日夜亮溫

狀態：quality_incomplete。詳見 profiles.json 的 rover_temperature_context 與 ../mars_temperature/summary.json。
Jezero 探測車局部亮溫不代表 100 km 區域或全球動力地表溫度；探索摘要不進相似度評分。

## 接軌規則

- Match terrain at the declared physical scale.
- Keep MODIS LST distinct from TES thermal inertia.
- Keep Earth precipitation/moisture/permafrost distinct from SWIM ice consistency.
- Keep 550 nm extinction AOT distinct from 9.3 micron Mars absorption CDOD.

## 仍缺的火星資料／定義

- Comparable Mars surface day/night temperature and temporal definition
- Mission-specific material, mineral and operational thresholds
- Site-level ground validation and finer terrain where needed

沙塵以最近的原始 3° 網格呈現，並附 669-sol 序列與 Ls 分季摘要；不能說是 100 km 場址內的細尺度觀測。
TES 熱慣量排除原始遮罩為 0 的插值填補值，另列包含填補的摘要。SWIM 值不是冰含量或機率；0 不能當作未知或證明有冰。
Arcadia 目標中心是專案設計假設，不是官方選定登陸點。所有目標仍需任務需求與地面證據查證。
