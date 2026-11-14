#!/usr/bin/env python3
"""Build a Chinese review report from the new, isolated Mars rescreen outputs.

Reads accepted numerical outputs and a bounded literature register. Does not
alter original data, old candidates, weights, EH, the workbook, or website.
"""
from __future__ import annotations

import hashlib
import json
import math
import unicodedata
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle
import numpy as np
import pandas as pd
import xarray as xr

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs/research/mars_reselection_20261114"
VERSION = "MARS-RESELECT-20261114-v1"
FONT = FontProperties(fname="/Library/Fonts/Arial Unicode.ttf")
BLUE, INK, GREY, LIGHT = "#173f59", "#172b3a", "#526575", "#edf3f6"
SPECS = [
    dict(id="MS-01", review="A", name="72°E 北部低地扇區", role="雙深度冰線索與低起伏並存",
         why="兩深度冰一致性都相對高，區域坡度與高差低；適合提出覆土與冰相關熱訊號的後續探查問題。",
         trade="三點中熱慣量最高，但這不等於較硬、較好鑽或冰較多。TES有27個插值格被排除；局部材料與冰界面仍未知。",
         question="在兩深度冰線索均較強、較高熱慣量的區域，哪些局部影像、雷達與熱觀測能區分表層材料和地下冰的影響？"),
    dict(id="MS-02", review="D", name="168°E 北部低地扇區", role="較低緯度的冰探查取捨",
         why="三點中最靠近赤道，兩深度冰線索均為正且相對高，TES原生有效格比例最高；適合比較緯度、熱背景與冰線索的取捨。",
         trade="三點中區域高差較大，MY34沙塵p95及最大值也最高。較低緯度不等於已證明供電、熱控或登陸可行。Phlegra大區已有研究。",
         question="較低緯度但較高沙塵背景的候選，能否用新增局部觀測釐清淺層冰線索與季節熱背景，而不借用南方既有場址真值？"),
    dict(id="MS-03", review="C", name="242°E 北部低地扇區", role="較低沙塵、低坡度與強近表層線索",
         why="三點中區域平均坡度最低，MY34與MY35的沙塵均值及p95也最低，近表層SWIM線索較強；提供不同熱性質背景的探查對照。",
         trade="1-5m指標低於另外兩點；TES僅79/100原生格有效，熱慣量範圍較寬。溫度粗格偏北且缺測多；不能推論冰量、硬度或設備性能。",
         question="較低熱慣量與較強近表層冰線索並存時，覆土與地表材料可能造成哪些判讀歧義，應先取得什麼局部證據？"),
]

SOURCES = [
    ("S1", "MOLA PDS 原生高程與標籤", "https://pds-geosciences.wustl.edu/mgs/urn-nasa-pds-mgs_mola_topography_derived/meg016/", "本機原檔及標籤；來源hash已核對"),
    ("S2", "TES 夜間熱慣量與插值遮罩", "https://pds-geosciences.wustl.edu/mgs/mgs-m-tes-5-timap-v1/mgst_9001/data/", "本機IMG/LBL；排除mask=0"),
    ("S3", "SWIM 2.0 提供者產品說明", "https://swim.psi.edu/SWIM2Products.php", "提供者頁與本機兩深度GeoTIFF；2021產品"),
    ("S4", "Montabone 火星沙塵重建產品", "https://doi.org/10.1029/2019JE006111", "本機MY34/MY35 v2.5；3°、669 sols/年"),
    ("S5", "Wang/Jin MCS 校時溫度資料", "https://doi.org/10.5281/zenodo.17947556", "版本固定；本機MD5/SHA；5°背景"),
    ("S6", "MEDA/PDS 儀器與品質參照", "https://doi.org/10.17189/1522849", "既有159418列QA紀錄；不移植至新點"),
    ("N1", "NASA EMC EZMars 2015提案目錄", "https://trek.nasa.gov/mars/trekarcgis/rest/services/EZMars/MapServer", "沿用已查381 ROI/51 EZ幾何北界；本輪端點重取失敗"),
    ("N2", "SWIM4MIM 已選冰探查RZ", "https://swim.psi.edu/SWIM4MIMProducts.php", "本輪提供者頁；幾何北界沿用已驗快照"),
    ("N3", "Mashal等2025優先探索區", "https://doi.org/10.3847/PSJ/ade30e", "原文索引§2、Figure2/8及TableA3；23區限±50°"),
    ("N4", "Morgan等2025已知露冰點", "https://doi.org/10.3847/PSJ/ad9b24", "原文索引Table2完整26行；不是全文讀取"),
    ("N5", "Dundas等2014露冰撞擊點", "https://doi.org/10.1002/2013JE004482", "原文Table1的20點"),
    ("N6", "Dundas等2021冰暴露研究", "https://doi.org/10.1029/2020JE006617", "本文具體點/圖說；S1-S4補表未取得"),
    ("N7", "NASA SkyFall 2026參考場址", "https://science.nasa.gov/wp-content/uploads/2026/09/skyfall-mission-information-package-final.pdf", "9頁原始文件；SectionVII AP-105"),
    ("N8", "2015 Phlegra基地提案1002", "https://www.hou.usra.edu/meetings/explorationzone2015/pdf/1002.pdf", "原始2頁；39N172E及列明高緯備選"),
    ("N9", "2020 Phlegra候選研究6008", "https://www.hou.usra.edu/meetings/marspolar2020/pdf/6008.pdf", "原始2頁；具體搜尋與圖例點在更南方"),
    ("N10", "NASA ODE既有/擬議著陸點", "https://ode.rsl.wustl.edu/mars/pagehelp/Content/Missions_Instruments/Landing_Sites.htm", "公開座標頁；不是最新所有任務完整足跡目錄"),
    ("N11", "2015冰資源提案1018", "https://ntrs.nasa.gov/api/citations/20150020456/downloads/20150020456.pdf?attachment=true", "原始1頁；ROI40-50N、160-190E"),
]

USAGE = [
    ["地形", "MOLA高程、坡度、高差", "比較/原生核對", "約3.7km；不能判米級障礙或安全"],
    ["熱性質", "TES熱慣量及插值遮罩", "背景/有效比例", "約3km；沒有單調最佳值；不是溫度/硬度"],
    ["水/冰", "SWIM 0-1m與1-5m", "兩個探索目標", "共享原始證據；不是冰量或獨立互證"],
    ["大氣/沙塵", "MY34/MY35均值、p95、極值、分季、可靠度", "p95比較；其餘作背景", "原生3°重建；不是局部風、沉積或氣壓"],
    ["溫度", "MCS MY29-36；03/15 LTST", "粗背景/缺值揭露", "5°校時衍生值；QA/不確定度/樣本數缺失"],
    ["探測車", "MEDA局部亮溫等159418列", "品質與尺度參照", "Jezero局部且完整QA合格0列；不移植"],
    ["未取得", "局部風壓、材料、冰真值、細地形等", "明列未知", "沒有數值，不補造或視為條件通過"],
]


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def wrap(text, capacity=52):
    lines, line, width = [], "", 0.0
    for ch in str(text):
        if ch == "\n":
            lines.append(line); line, width = "", 0.0; continue
        w = 1.0 if unicodedata.east_asian_width(ch) in "WF" else .53
        if width + w > capacity and line:
            lines.append(line); line, width = "", 0.0
        line += ch; width += w
    if line: lines.append(line)
    return lines or [""]


def fmt(v, n=3):
    return f"{v:.{n}f}"


class Page:
    def __init__(self, pdf, number, title, subtitle=""):
        self.pdf = pdf; self.number = number
        self.fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        self.ax = self.fig.add_axes([0, 0, 1, 1]); self.ax.set_xlim(0, 8.27); self.ax.set_ylim(0, 11.69); self.ax.axis("off")
        self.ax.add_patch(Rectangle((0, 11.48), 8.27, .21, color=BLUE))
        self.text(.55, 11.13, "TEAM ZASA / NASA SPACE APPS 2026", 9, GREY)
        self.text(.55, 10.73, title, 20, BLUE)
        if subtitle: self.text(.55, 10.36, subtitle, 9.5, GREY)
        self.y = 9.98

    def text(self, x, y, value, size=10.5, color=INK, url=None):
        return self.ax.text(x, y, value, fontproperties=FONT, fontsize=size, color=color, va="top", url=url)

    def para(self, value, size=10.5, color=INK, gap=.14):
        lines = wrap(value, capacity=7.16 * 72 / size)
        self.text(.55, self.y, "\n".join(lines), size, color)
        self.y -= len(lines)*size/72*1.48 + gap

    def heading(self, value):
        self.y -= .04; self.text(.55, self.y, value, 13, BLUE); self.y -= .35

    def table(self, headers, rows, widths, size=9.1):
        for ri, row in enumerate([headers]+rows):
            texts = [wrap(v, max(4, w*72/size-1.3)) for v, w in zip(row, widths)]
            height = max(len(x) for x in texts)*size/72*1.48+.16
            x = .55
            for col, w in enumerate(widths):
                face = BLUE if ri == 0 else (LIGHT if ri%2 else "white")
                self.ax.add_patch(Rectangle((x, self.y-height), w, height, facecolor=face, edgecolor="#d5e1e8", linewidth=.5))
                self.text(x+.07, self.y-.08, "\n".join(texts[col]), size, "white" if ri==0 else INK)
                x += w
            self.y -= height
        self.y -= .19

    def finish(self):
        if self.y < .82:
            raise ValueError(f"PDF page {self.number} overflows: y={self.y}")
        self.ax.plot([.55,7.72],[.61,.61], color="#d5e1e8", lw=.7)
        self.text(.55,.44,"MARS-RESELECT-20261114-v1 | 條件式研究候選 / 限定範圍查核",8,GREY)
        self.text(7.42,.44,str(self.number),8,GREY)
        self.pdf.savefig(self.fig); plt.close(self.fig)


def map_figure(records, points):
    with xr.open_dataset(ROOT/"data/processed/mars_stack_0p5deg.nc",engine="scipy") as ds:
        v=ds.ice_shallow.load()
    fig, ax=plt.subplots(figsize=(10,3.8),layout="constrained")
    im=ax.imshow(v.values,extent=[-180,180,-90,90],cmap="coolwarm",vmin=-1,vmax=1,interpolation="nearest",aspect="auto")
    for spec,r in records:
        lat,lon=r["center"]["lat"],r["center"]["lon"]
        ax.scatter(lon,lat,s=65,c="#ffe184",edgecolors="#132e43",linewidths=1.1,zorder=5)
        ax.annotate(spec["id"],(lon,lat),xytext=(4,8),textcoords="offset points",fontsize=10,color="#132e43",weight="bold")
    if points:
        ax.scatter([((p["lonE"]+180)%360)-180 for p in points],[p["lat"] for p in points],s=9,c="black",alpha=.55,label="Published ice-exposing impact points (Morgan 2025 Table 2)")
    ax.set(xlabel="East longitude (degrees; -180 to 180)",ylabel="Planetocentric latitude (degrees)",ylim=(-65,70))
    ax.set_title("Three regional research candidates - SWIM 2.0 shallow-ice context",fontsize=12)
    ax.grid(alpha=.15);ax.legend(loc="lower left",fontsize=7)
    fig.colorbar(im,ax=ax,shrink=.75,label="Ice consistency (-1 to +1), not ice fraction")
    p=OUT/"candidate_map.png";fig.savefig(p,dpi=180);plt.close(fig)
    return p


def build():
    native=json.loads((OUT/"candidate_native_evidence.json").read_text())
    method=json.loads((OUT/"method.json").read_text())
    audit=json.loads((OUT/"bounded_prior_site_audit.json").read_text())
    byid={r["review_id"]:r for r in native["records"]}
    records=[(s,byid[s["review"]]) for s in SPECS]
    metrics=pd.read_csv(OUT/"candidate_metrics.csv").set_index("candidate_id")
    map_path=map_figure(records,audit["morgan_2025_table2"]["points"])
    selected=[]
    for spec,r in records:
        selected.append({**spec,"center":r["center"],"lon_east_0_360":r["center"]["lon"]%360,"bounds":r["nominal_cell_bounds"],"status":"retained_for_followup_with_bounded_prior_site_nonhit; not globally novelty-cleared","native_evidence_file":"candidate_native_evidence.json","native_review_id":spec["review"]})
    (OUT/"selected_targets.json").write_text(json.dumps({"version":VERSION,"parent_main":"e84da75d905ad43f260e74307752946862200dae","scope":"regional shallow-ice reconnaissance research, not landing/extraction approval","sites":selected},ensure_ascii=False,indent=2)+"\n")
    final=metrics.loc[[s["review"] for s in SPECS]].reset_index().rename(columns={"candidate_id":"input_review_id","status":"native_review_status"})
    final.insert(0,"candidate_id",[s["id"] for s in SPECS])
    final.insert(2,"final_selection_status","retained_after_bounded_review; not_globally_novelty_cleared")
    final.to_csv(OUT/"final_candidates.csv",index=False)
    pd.DataFrame(USAGE,columns=["theme","data","role","limit"]).to_csv(OUT/"all_data_usage.csv",index=False)

    summary=[]
    for spec,r in records:
        summary.append([spec["id"],f"{r['center']['lat']:.2f}N, {r['center']['lon']%360:.2f}E",spec["role"]])
    native_rows=[]
    for spec,r in records:
        native_rows.append([spec["id"],fmt(r["mola_slope_deg_3p7km_baseline"]["mean"]),str(int(r["mola_relief_m"])),f"{r['swim_0_1m_native']['mean']:.3f} / {r['swim_1_5m_native']['mean']:.3f}",fmt(r["tes_TI_native_excluding_infill"]["mean"],1)])
    pdf_path=OUT/"mars_three_candidates_report_zh.pdf"
    with PdfPages(pdf_path,metadata={"Title":"火星三點重新選址報告","Author":"Team zasa; AI-assisted analysis","Subject":VERSION}) as pdf:
        p=Page(pdf,1,"火星三點重新選址報告","全資料盤點、原生資料核對與有範圍的既有場址查核 | 2026-11-14")
        p.para("本輪重新選出三個值得後續覆核的火星區域候選，用於乾覆土下淺層冰探查研究。三點各有資料支持與取捨；它們是研究格，不是已確認冰藏、鑽孔或獲准登陸點。")
        p.table(["候選","中心座標","主要研究價值"],summary,[.8,2.25,4.12],9.7)
        p.para("在本報列明的目錄、原文座標表與具名提案範圍內，未確認三個名義格與已知具體場址重複。查核仍有覆蓋缺口，不能宣稱全世界從未研究或提出過這裡。",10.2)
        p.heading("先看結果：原生格資料，而非舊四項總分")
        p.table(["候選","平均坡度°","高差m","SWIM淺/深","TES熱慣量"],native_rows,[.8,1.05,.85,2.15,2.32],9.5)
        p.para("TES單位為 J m^-2 K^-1 s^-0.5；SWIM是無因次一致性，不是冰百分比。數據年代、尺度與物理量不同，沒有把它們當成一次受控實驗。",9.2,GREY)
        ax=p.fig.add_axes([.07,.13,.86,.235]);ax.imshow(plt.imread(map_path));ax.axis("off");p.y=1.19;p.finish()

        p=Page(pdf,2,"所有資料，分別用在哪裡？","考慮所有既有資料，不等於把每個欄位都硬塞進總分")
        p.table(["面向","已有資料","本輪角色","支撐與限制"],USAGE,[.7,2.15,1.55,2.77],9.2)
        p.heading("如何讀取「滿足資料要求」")
        p.para("可用的原生資料已逐點抽取並報告有效格數；有部分缺測或尺度不足的資料標為部分支持；沒有對應位置或品質不合格的資料保留為限制。沒有把未知當通過，也沒有補造風速、氣壓、冰深或冰量。")
        p.para("本輪可支持的是『值得進一步探查的資料條件』。尚無儀器、任務與工程門檻，因此不能據此核准基地、登陸、採冰或宣稱所有工程條件合格。",10.4)
        p.para("MOLA的64/64只表示格值有限；原MEGDR包含無軌跡處插值，本輪沒有雷射觀測密度遮罩，不能解讀為全部格都有直接量測。",9.8,GREY)
        p.para("三點皆高於50°N，不符合MCOA2025所用±50°或SkyFall目前0-45°N的緯度條件。這裡保留它們作冰探查研究候選；高緯熱控、供電與冬季限制仍需評估，不能直接提交為這兩組設計的合格場址。",9.8,GREY)
        p.finish()

        p=Page(pdf,3,"這次怎麼重新找？","獨立新版本；舊I-01/I-02、MR-v3、EH與Excel全部保留")
        counts=method["counts"]
        steps=[
            f"1. 在現有SWIM支撐範圍內，枚舉兩半球{counts['examined_grid_cells']:,}個0.5°名義格；沒有只沿用舊北緯30-60°結果。",
            f"2. 核對有效資料，加入1-5m冰指標、絕對高程、兩年沙塵完整摘要與MCS粗背景。兩深度SWIM>0只是探索方向，並非有冰驗證門檻。得到{counts['exploratory_pool']:,}個探索格。",
            f"3. 不設綜合分數：比較淺/深冰一致性較高、區域坡度/高差較低、MY34/MY35沙塵p95較低六項取捨，得到{counts['pareto_front']:,}個沒有被另一格全面壓過的候選。",
            "4. TES、絕對高程、溫度、季節與極值另列背景。沒有無據的『最佳熱慣量/溫度』；六項目標及探索條件仍是研究設計，不是官方任務規範。",
            "5. 抽取空間分散候選，對A/B/C/D四格做原生QA，再查具體場址先例。B靠近已知露冰點且完整研究足跡未取得，先不列最終三點；不直接判它重複。",
            "6. 最終保留A、D、C作MS-01、MS-02、MS-03：分別代表雙深度線索、較低緯度取捨、較低塵/低坡對照。這是透明的三案例取捨，沒有最佳性或成功率主張。",
        ]
        for t in steps:p.para(t,10.5,gap=.18)
        p.heading("重要的尺度界線")
        p.para("全球篩選用粗化/內插到共同網格的描述值；本報正式卡另列名義格內原生格心的統計，兩者不混用。MOLA約3.7km、TES/SWIM約3km，沙塵仍3°，MCS仍5°；0.5°顯示沒有創造細節。",10.2)
        p.finish()

        for num,(spec,r) in enumerate(records,4):
            p=Page(pdf,num,f"{spec['id']} | {spec['role']}",f"{r['center']['lat']:.2f}°N, {r['center']['lon']%360:.2f}°E | {spec['name']}")
            b=r["nominal_cell_bounds"];size=r["nominal_size_km_NS_EW"]
            p.para(f"研究範圍：{b['south']:.2f}-{b['north']:.2f}°N、{b['west']%360:.2f}-{b['east']%360:.2f}°E，名義大小約{size[0]:.2f} × {size[1]:.2f} km。座標是火星行星中心緯度、東經；範圍不是著陸橢圓或已勘查地面測區。",10.1)
            ti=r["tes_TI_native_excluding_infill"];a=r["swim_0_1m_native"];z=r["swim_1_5m_native"]
            rows=[
                ["地形",f"平均坡度 {r['mola_slope_deg_3p7km_baseline']['mean']:.4f}°；高差 {r['mola_relief_m']:.0f}m；平均高程 {r['mola_elevation_m_areoid']['mean']:.0f}m", "64/64原生格；只能描述區域地形"],
                ["熱性質",f"TES {ti['mean']:.1f}；範圍{ti['min']:.0f}-{ti['max']:.0f}",f"有效{ti['valid_cells']}/100；排除{r['tes_mask_zero_native_cells']}個插值格"],
                ["水/冰",f"0-1m {a['mean']:.4f}；1-5m {z['mean']:.4f}",f"各100/100有效；正值格{a['positive_cells']}/100、{z['positive_cells']}/100；非獨立互證"],
            ]
            for key,label in [("dust_my34","MY34沙塵"),("dust_my35","MY35沙塵")]:
                d=r["dust"][key];rows.append([label,f"均值{d['mean_cdodtot']:.4f}；p95 {d['p95_cdodtot']:.4f}；最大{d['max_cdodtot']:.4f}",f"669/669重建sol；3°最近格；非地面積塵"])
            m=r["MCS_context"];mr=metrics.loc[spec["review"]]
            rows.append(["溫度背景",f"03h {mr['MCS_populated_night_median_K']:.1f}K；15h {mr['MCS_populated_day_median_K']:.1f}K；配對差中位{m['paired_contrast_median_K']:.1f}K",f"最近粗格({m['selected_grid_coordinate']['lat']:.0f},{m['selected_grid_coordinate']['lon']:.0f})；配對{m['paired_bins']}/288；QA未知"])
            p.table(["面向","原生/背景數值","證據支撐"],rows,[.8,3.35,3.02],9.2)
            p.heading("為什麼值得保留")
            p.para(spec["why"],10.5)
            p.para("可研究的問題："+spec["question"],10.2)
            p.heading("缺點與未知")
            p.para(spec["trade"],10.2)
            p.para("冰是否存在、真實深度、純度、連續性、局部材料、風壓與細部危害均未確認。MCS有值時段中位數受缺測分布影響，不是全年平均、日最高減最低或研究格實測。",9.6,GREY)
            p.finish()

        p=Page(pdf,7,"已知點位與提案，查到哪裡？","以完整名義格查核；點表、範圍、廣域製圖分開")
        auditrows=[
            ["NASA EZMars", "381 ROI / 51 EZ快照北界≤47.8511N", "三格均在北界外；沿用既有幾何查核紀錄，本輪未重取"],
            ["SWIM4MIM RZ", "已驗釋出幾何北界51.217655N", "三格南界均更北；僅適用該快照，不代表所有未公開方案"],
            ["MCOA 2025", "23個優先區限±50°", "三格均在該緯帶外；不把此限制當本輪工程標準"],
            ["露冰點表", "Morgan2025 Table2共26點；Dundas2014 Table1", "未有表內點落入三格；不等於所有露冰研究足跡都排除"],
            ["具名提案", "SkyFall AP-105、Phlegra、1018冰資源ROI", "已讀具體點/明示範圍與三格分離；廣域研究脈絡仍存在"],
            ["既有任務", "NASA ODE列明著陸點及公開任務資料", "無已讀中心落入三格；不是所有歷史提案的完整足跡庫"],
        ]
        p.table(["查核範圍","已知內容","本輪能支持的結論"],auditrows,[1.15,2.65,3.37],9.3)
        p.heading("與已知露冰點的關係")
        p.para("26點表中最近已知點：MS-01距Site33約464.79km；MS-02距Site46約388.98km；MS-03距Site26約130.46km。這是中心距離背景，不用它代替研究範圍相交，也不把鄰點冰真值搬入新格。",10.2)
        p.heading("查核缺口仍保留")
        p.para("Dundas2021的S1-S4完整補表/ScienceBase資料本輪未取得；部分歷史替代EZ未有完整名稱與幾何對照，未公開提案無法查。座標非命中僅是檢索結果，不能證明從未研究。",10.2)
        p.para("本輪決定：保留三點作下一階段研究候選；新穎性只限本報列明資料範圍，不核發全球首創或『從沒人開發』保證。",10.5,BLUE)
        p.finish()

        p=Page(pdf,8,"來源、重現與交付界線","原觀測歸原資料作者；本輪是CPU資料篩選、提取與查核")
        p.para("本機Mars輸入已按manifest核對hash；既有MR-v3/EH檔另與固定main的Git blob對照，Excel符合既有驗收hash，見preservation_check.json。本輪程式只輸出新目錄；未合併、推送、GPU加速、模型訓練、新地面量測或正式提交。",10.0)
        p.heading("主要資料來源")
        for sid,title,url,scope in SOURCES[:6]:
            p.para(f"{sid}  {title} | {scope}",9.1,gap=.05)
            p.text(.65,p.y,url,7.7,BLUE,url=url);p.y-=.23
        p.heading("主要先例來源")
        for sid in ["N2","N3","N4","N6","N7","N8","N9"]:
            sid,title,url,scope=next(x for x in SOURCES if x[0]==sid)
            p.para(f"{sid}  {title} | {scope}",8.7,gap=.03)
            p.text(.65,p.y,url,7.3,BLUE,url=url);p.y-=.22
        p.para("完整來源/精確檢索字串見report.md及bounded_prior_site_audit.json；原生數值、系列、篩選母體、程式與驗證記錄隨附。資料使用條件各依原提供者；沙塵衍生部分保留Montabone CC-BY-SA-3.0。",9.0,GREY)
        p.finish()

    md=["# 火星三點重新選址報告",f"Team zasa | {VERSION} | 2026-11-14（Asia/Taipei）", "",
        "## 結論", "本輪重新選出三個供淺層冰探查研究的區域候選。已把全部既有火星資料分成選點比較、背景、品質不足或無對應位置四種角色；沒有把所有欄位硬合成總分。",
        "在本報列明的目錄、座標表與具名提案範圍內，未確認三個名義格與已知具體場址重複。完整補表及部分歷史提案幾何仍缺，不能保證全世界從未研究或提出過。三點不是已確認冰藏、採冰方案或獲准登陸/基地地點。", "",
        "| 候選 | 中心座標 | 用途價值 |", "|---|---|---|", *["| "+" | ".join(x)+" |" for x in summary], "", "![三個候選及已知露冰點](candidate_map.png)", "",
        "## 怎麼重新找",f"掃描{counts['examined_grid_cells']:,}個0.5°格；{counts['finite_core_cells']:,}格具有效核心描述；在兩深度SWIM>0、非舊八個候選格/舊排除框的探索規則下得{counts['exploratory_pool']:,}格。六目標非支配前緣有{counts['pareto_front']:,}格，抽22格供審查，再對4格做原生QA，選A/D/C為三案例。",
        "六目標為淺層/深層SWIM較高、區域坡度/高差較低、MY34/MY35沙塵p95較低。無權重、無總分；探索方向和目標仍屬本研究設計，不是經驗證的工程門檻。TES、高程、MCS、分季/極值/可靠度均有考慮，但因沒有單調最佳值或QA不足，保留背景而不強行評分。",
        "北緯51°以上只是待查候選的抽樣優先安排，不是物理限制或新穎性條件。三點最終以具體價值、資料及已列先例取捨選擇；不宣稱全域最佳。", "",
        "## 所有資料的使用帳", "| 面向 | 資料 | 本輪用途 | 限制 |", "|---|---|---|---|", *["| "+" | ".join(x)+" |" for x in USAGE], "",
        "## 三點比較（原生格）", "| 候選 | 平均坡度° | 高差m | SWIM 0-1m / 1-5m | TES熱慣量 |", "|---|---|---|---|---|", *["| "+" | ".join(x)+" |" for x in native_rows], "",
        "TES單位J m^-2 K^-1 s^-0.5；SWIM為一致性而非百分比。全球粗化/插值stack值與名義格內原生格統計不同，本表採後者。",
        "MOLA64/64只表示格值有限；MEGDR原產品含無軌跡處插值，本輪未取得雷射觀測密度遮罩，不能把有效格當成全部直接量測或品質全面合格。",
        "三點皆高於50°N，不符合MCOA2025所用±50°或SkyFall目前0-45°N的緯度條件。本輪定位為冰探查研究候選；高緯熱控、供電與冬季限制仍需評估，不能直接提交為這兩組設計的合格場址。"]
    for spec,r in records:
        b=r["nominal_cell_bounds"];ti=r["tes_TI_native_excluding_infill"];m=r["MCS_context"];mr=metrics.loc[spec["review"]]
        md += ["",f"## {spec['id']}：{spec['role']}",f"位置：{r['center']['lat']}°N、{r['center']['lon']%360}°E。範圍：{b['south']}-{b['north']}°N、{b['west']%360}-{b['east']%360}°E，約{r['nominal_size_km_NS_EW'][0]:.2f}×{r['nominal_size_km_NS_EW'][1]:.2f} km。這是分析單元，不是實地測區/鑽孔/著陸橢圓。", "", "**為什麼選：**"+spec["why"], "", "**要研究什麼：**"+spec["question"], "", "**缺點與未知：**"+spec["trade"], "", "| 面向 | 數值與有效支撐 | 能說到哪裡 |", "|---|---|---|",
            f"| 地形 | MOLA64/64；平均高程{r['mola_elevation_m_areoid']['mean']:.1f}m；坡度{r['mola_slope_deg_3p7km_baseline']['mean']:.6f}°；高差{r['mola_relief_m']:.0f}m | 約3.7km尺度；非局部障礙/安全 |",
            f"| 熱性質 | TES {ti['mean']:.4f}；有效{ti['valid_cells']}/100；範圍{ti['min']:.0f}-{ti['max']:.0f} | 排除插值；非溫度/硬度 |",
            f"| 冰線索 | 0-1m {r['swim_0_1m_native']['mean']:.6f}；1-5m {r['swim_1_5m_native']['mean']:.6f}；各100/100有效 | 共享來源，非獨立互證；無真實冰量/冰深 |"]
        for key,label in [("dust_my34","MY34"),("dust_my35","MY35")]:
            d=r["dust"][key]
            md += [f"| {label}沙塵 | 均值{d['mean_cdodtot']:.6f}；p95 {d['p95_cdodtot']:.6f}；最大{d['max_cdodtot']:.6f}；可靠度均值{d['reliability_mean']:.6f} | 669/669重建sol；最近3°格({d['native_cell_lat']},{d['native_cell_lon']})；可靠度非機率 |"]
        md += [f"| MCS溫度背景 | 最近5°格({m['selected_grid_coordinate']['lat']},{m['selected_grid_coordinate']['lon']})；15h/03h有值中位{mr['MCS_populated_day_median_K']:.2f}/{mr['MCS_populated_night_median_K']:.2f}K；配對差中位{m['paired_contrast_median_K']:.2f}K | 日{m['valid_day_bins']}/288、夜{m['valid_night_bins']}/288、共同{m['paired_bins']}/288；非同sol/全年/局部實測，QA與不確定度未知 |", "", "**資料仍不能回答：**冰存在/深度/純度/連續性、風壓、地面承載力/岩石率、礦物及細地形真值、可採能耗、設備性能與現況。"]
        md += ["", "### 沙塵季節背景", "| Ls區間 | MY34均值/sol數 | MY35均值/sol數 |", "|---|---|---|"]
        for season in ["0_90","90_180","180_270","270_360"]:
            q0=r["dust"]["dust_my34"]["seasons_by_Ls"][season];q1=r["dust"]["dust_my35"]["seasons_by_Ls"][season]
            md.append(f"| {season} | {q0['mean_cdodtot']:.6f} / {q0['valid_sols']} | {q1['mean_cdodtot']:.6f} / {q1['valid_sols']} |")
    md += ["", "## 有範圍的既有場址查核", "| 來源 | 本輪判定及範圍 |", "|---|---|"]
    for row in audit["catalog_checks"]:md.append(f"| {row['source_id']} {row['name']} | {row['finding']}；{row['limit']} |")
    md += ["", "26個已知露冰點的同格檢查與中心距離計算保存於bounded_prior_site_audit.json；距離只作背景，不取代範圍相交。B不列三點是保守取捨，沒有因近29km就宣判重複。", "", "### 精確檢索字串與停止範圍"]
    for rid,queries in audit["queries"].items():md += ["",f"- {rid}："+"；".join(queries)]
    md += ["", "完成上述具名目錄/指定表格與每候選一輪座標、區域別名、用途查詢後停止。非命中不升格為從未研究；完整補表、歷史替代EZ與未公開提案仍有缺口。", "", "## 重現與交付", "- 篩選：.venv/bin/python -m scripts.research.mars_reselection_20261114", "- 原生提取：.venv/bin/python -m scripts.research.mars_reselection_20261114 --finalize-targets outputs/research/mars_reselection_20261114/fixed_targets.json", "- 報告：.venv/bin/python -m scripts.reporting.build_mars_reselection_report", "- 驗證見numerical_validation.json、report_validation.json；輸入hash見method.json及candidate_native_evidence.json。", "- 本輪結果僅本機生成；未合併、推送、部署或正式提交。既有MR-v3/EH/Excel未重做或覆寫。", "- 原量測歸原資料作者。本輪AI協助程式、資料盤點與文字，實際以Mac CPU運算，未使用GPU、模型訓練或新地面觀測。", "- 沙塵衍生部分依Montabone來源CC-BY-SA-3.0；其他資料依各提供者條款，不替整個專案另行授權。", "- 本報完成的是火星候選重選；Earth↔Mars的新地球類比場址目標仍需另行完成。", "", "## 來源與實際閱讀範圍"]
    i=md.index("## 來源與實際閱讀範圍")
    md[i:i]=["- preservation_check.json另核對既有MR-v3/EH檔與固定main Git blob、Excel與既有驗收hash；與Mars輸入manifest的保護範圍分開。", "- final_candidates.csv的native_review_status保留原生QA交接狀態；final_selection_status才表示本報完成限定查核後保留，不回寫原生輸入狀態。", ""]
    for sid,title,url,scope in SOURCES:md += [f"- [{sid} {title}]({url})：{scope}。"]
    (OUT/"report.md").write_text("\n".join(md)+"\n")
    manifest={"version":VERSION,"created_taipei":datetime.now(ZoneInfo("Asia/Taipei")).isoformat(),"status":"local_report_built_pending_visual_QA","selected_review_ids":[s["review"] for s in SPECS],"selected_ids":[s["id"] for s in SPECS],"files":[]}
    for name in ["mars_three_candidates_report_zh.pdf","report.md","candidate_map.png","final_candidates.csv","selected_targets.json","all_data_usage.csv","bounded_prior_site_audit.json"]:
        q=OUT/name;manifest["files"].append({"path":q.relative_to(ROOT).as_posix(),"bytes":q.stat().st_size,"sha256":sha(q)})
    (OUT/"report_manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
    print(pdf_path);print(OUT/"report.md")


if __name__=="__main__":build()
