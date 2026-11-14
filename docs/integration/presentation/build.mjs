/** Build from fixed delivered results. Run from repo root; see README.md. */
import fs from 'node:fs/promises';
import path from 'node:path';
import {pathToFileURL} from 'node:url';
const runtime=process.env.ARTIFACT_NODE_MODULES??'/Users/clark/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
const {Presentation,PresentationFile}=await import(pathToFileURL(path.join(runtime,'@oai/artifact-tool/dist/artifact_tool.mjs')).href).catch(async()=>await import(pathToFileURL(path.join(runtime,'@oai/artifact-tool/index.js')).href));
const root=process.cwd(), out=path.join(root,'outputs/integration/presentation'),tmp=path.join(root,'.presentation-build');
const font='Heiti TC', C={ink:'#12283E',muted:'#536575',teal:'#117F83',orange:'#AC581B',line:'#D9E2E9',wash:'#F0F5F7'};
const p=Presentation.create({slideSize:{width:1280,height:720}});
const repo='https://github.com/zhuang768/NASA-Space-Apps-Challenge-2026-Taipei';
const shas={main:'3cc8488577535e2fa4d146021fde51f8ff6cc667',ms01:'b4b6929e890018668ef4faa9a74128a4ce5aa8df',ms02:'38b8fa0dea527b1cc47aeb02dc260e039da37122',ms03:'8fa07afac4a98096958880f6a5ece16f35abc4db'};
const blob=(sha,f)=>`${repo}/blob/${sha}/${f}`;
const sources={
 R01:{title:'MS-01 原報告',url:blob(shas.ms01,'docs/research/MS-01/report.md')},
 R01T:{title:'MS-01 熱訊號補充報告',url:blob(shas.ms01,'docs/research/MS-01/thermal_followup.md')},
 R02:{title:'MS-02 報告，§8B 最新 Adventdalen 處置',url:blob(shas.ms02,'docs/research/MS-02/report.md')},
 R03:{title:'MS-03 報告，最新形貌／索引查核與降級',url:blob(shas.ms03,'docs/research/MS-03/report.md')},
 D01:{title:'三個火星點的原生資料支撐紀錄',url:blob(shas.main,'outputs/research/mars_reselection_20261114/candidate_native_evidence.json')},
 D02:{title:'UV 固定窗口結果、有效列與敏感度',url:blob(shas.ms01,'outputs/research/MS-01/thermal_followup/comparison.json')},
 D03:{title:'Adventdalen 證據範圍表',url:blob(shas.ms02,'outputs/research/MS-02/footprint.csv')},
 D04:{title:'MS-03 影像產品、日期、足跡及品質',url:blob(shas.ms03,'outputs/research/MS-03/morphology/image_inventory.csv')},
 D05:{title:'AD1 幾何摘要',url:blob(shas.ms03,'outputs/research/MS-03/morphology/AD1_geometry_summary.json')},
 P01:{title:'Marinova et al. 2022（原始研究）',url:'https://doi.org/10.1017/S0954102022000025'},
 P02:{title:'UV 作者校準／篩選資料，固定 Zenodo v1',url:'https://zenodo.org/records/10553882'},
 P03:{title:'Rasmussen et al. 2023 作者稿，§§3.2–3.5／5.4',url:'https://backend.orbit.dtu.dk/ws/files/329047704/1_s2.0_S0277379123001853_main.pdf'},
 P04:{title:'Rotem et al. 2023，§§2–3',url:'https://tc.copernicus.org/articles/17/3363/2023/'},
 P05:{title:'Brighi et al. 2025，WISDOM 摘要，僅摘要',url:'https://meetingorganizer.copernicus.org/EPSC-DPS2025/EPSC-DPS2025-710.html'},
 P06:{title:'Ulrich et al. 2011，既有 Svalbard–Mars 比較',url:'https://doi.org/10.1016/j.geomorph.2011.07.002'},
 P07:{title:'AD1 既有 GIS 資料集',url:'https://doi.pangaea.de/10.1594/PANGAEA.921087'}
};
function text(s,content,x,y,w,h,size=26,color=C.ink,bold=false){
 const v=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 v.text=content;v.text.style={fontSize:size,typeface:font,color,bold:false,insets:0,wrap:'square',autoFit:'none'};return v;
}
function rect(s,x,y,w,h,color){return s.shapes.add({geometry:'rect',position:{left:x,top:y,width:w,height:h},fill:color,line:{fill:'none',width:0}})}
const noteBlocks=[];
function page(n,title,kicker,ids,note){
 const s=p.slides.add();s.background.fill='#FFFFFF';
 text(s,`TEAM ZASA   /   EARTH ↔ MARS   /   ${kicker}`,56,27,1168,24,14,C.teal,true);
 text(s,title,56,72,1168,70,38,C.ink,true);
 rect(s,56,650,1168,1,C.line);
 text(s,`來源 ${ids.join(' · ')}  ｜  完整連結與限制見講稿／figure_index.csv`,56,667,1100,25,13,C.muted);
 text(s,String(n).padStart(2,'0'),1180,665,44,28,17,C.teal,true);
 const sourceText=ids.map(id=>`[${id}] ${sources[id].title}\n${sources[id].url}`).join('\n\n');
 s.speakerNotes.text=`第 ${n} 頁：${title}\n\n${note}\n\n來源\n${sourceText}`;
 noteBlocks.push({n,title,ids,note,sourceText});return s;
}
function table(s,values,x,y,width,height,widths,size=23){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:x,top:y,width,height,columnWidths:widths,values});
 for(let r=0;r<values.length;r++) for(let c=0;c<values[0].length;c++){
  const q=t.getCell(r,c);q.fill=r===0?C.ink:(r%2?'#F0F5F7':'#FFFFFF');
  q.text.style={fontSize:size,typeface:font,color:r===0?'#FFFFFF':C.ink,bold:false,insets:12,verticalAlignment:'middle'};
 }
 t.borders.assign({fill:'#FFFFFF',width:1,style:'solid'});return t;
}
async function image(s,file,x,y,w,h,alt){const b=await fs.readFile(path.join(out,'assets',file));s.images.add({blob:b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength),contentType:'image/png',alt,fit:'contain',position:{left:x,top:y,width:w,height:h}})}
// 1
let s=page(1,'地球場址能幫我們回答哪些火星冰問題？','研究問題',['R01T','R02','R03'],
`開場：我們選擇三個既定火星候選，檢查地球資料實際能支援哪些研究用途。任務目的是在投入新量測前，把可用資料、已知先例與判讀限制說清楚。\n\n這輪完成的是既有資料分析、來源 QA 與配對適用性查核。乾覆土如何改變熱訊號、影像中的多邊形是否可比較，是研究問題；三個火星格的地下冰真值尚未取得。保留或降級指的是用途證據是否足夠，不是地點好壞排名。\n\n本版 8 頁依使用者要求製作。正式提交頁數、表單及格式仍需隊伍向主辦確認；不宣稱本檔已滿足提交規格。`);
text(s,'選點目的',56,177,270,34,23,C.teal,true);
text(s,'為冰探查研究，選擇\n有實測依據的地球方法參照。',56,225,1100,122,44,C.ink,true);
text(s,'核心問題：哪些訊號可解釋？哪些配對尚缺關鍵證據？',56,385,1150,50,29);
rect(s,56,475,1168,127,C.wash);
text(s,'已完成',80,493,300,30,22,C.teal,true);text(s,'既有數據分析與 QA',80,538,330,34,25);
text(s,'研究假設',462,493,300,30,22,C.orange,true);text(s,'覆土、熱響應與形貌比較',462,538,370,34,25);
text(s,'尚待驗證',878,493,290,30,22,C.muted,true);text(s,'火星地下冰與因果解釋',878,538,320,34,25);
// 2
s=page(2,'三個名義候選格，四個資料面向','研究設計',['D01','R01T','R02','R03'],
`三點座標使用火星 planetocentric 緯度、east-positive 經度。名義格都是 0.5° × 0.5°，這只是候選範圍，不是所有儀器解析度或有效影像範圍。MS-01 中心 56.75°N、72.75°E；MS-02 52.75°N、168.25°E；MS-03 57.75°N、242.25°E。\n\n地形、溫度／熱性質、水／冰、大氣／沙塵保留原產品物理意義。MOLA 區域地形約 3.7 km 基線；TES 為 20 pixels/degree 產品；MCS 為 5°、MY29–36 的 03/15 LTST 彙整背景，不能稱同日振幅或站點實測；SWIM 是資料一致性，不是冰量或機率；CDOD 是 9.3 μm 柱光學厚度，MY34/35，不是沉積率。更細的共同網格不會增加原生細節。\n\n本簡報沿用各 PR 數值與查核，未重新擷取火星網格。MS-02 原始產品存取受限，原報告依交接資料核對，不宣稱所有點均已由本輪從原始資料重算。`);
table(s,[['火星點／中心','名義格（N / E）','本輪比較重點'],['MS-01\n56.75°N, 72.75°E','56.50–57.00°\n72.50–73.00°','已知冰界面與熱訊號判讀'],['MS-02\n52.75°N, 168.25°E','52.50–53.00°\n168.00–168.50°','覆土、季節背景與證據共址'],['MS-03\n57.75°N, 242.25°E','57.50–58.00°\n242.00–242.50°','影像可辨識性與形貌配對']],56,168,1168,310,[335,340,493],23);
text(s,'地形 MOLA　｜　熱性質 TES／MCS　｜　水冰 SWIM　｜　沙塵 CDOD',56,510,1168,38,24,C.teal,true);
text(s,'候選格 ≠ 原生解析度。地溫、熱慣量、一致性與光學厚度各自解讀。',56,569,1168,44,25);
// 3
s=page(3,'MS-01｜已知冰界面，如何約束熱訊號？','完成的分析',['R01T','D02','P01','P02'],
`圖 F01 依交付 comparison.json 的四條主要剖面重繪，沒有重新擬合或重新解析原始檔。橫軸是冰界面 24 小時半振幅除以上層半振幅，無單位。點為原計算結果，橫線是逐日留一敏感度範圍，不是信賴區間。原擬合含截距、線性趨勢與 24 小時 sin/cos，溫度半振幅以 K 表示。\n\n期間固定在原印刷時間 2010-11-07 00:00 含至 2010-11-18 00:00 不含。S/M/D 各 264 個同站共同有效逐時列，W Campbell 528 個半小時列；沒有跨站或 Campbell–HOBO 配時。M 上層探針是 1 cm。來源為作者已校準／篩選匯出，不是未處理 logger bytes。\n\n界面分量都較小，可用於分層模型與資料品質檢查。D36 與 W42 比值不隨深度單調，跨站材料與邊界條件未控制；所有主剖面已知含冰，缺同材料無冰對照，所以不能證明冰獨有訊號或建立冰深校正。S/D 座標版本衝突仍未解，按匯出／序號辨識，不作坡向配準。W 短版與長版匯出的時標脈絡不同，未合併。MS-01 地下冰存在、深度與純度仍未知。`);
await image(s,'F01_UV_amplitude_ratios.png',45,158,780,407,'F01: Four delivered University Valley interface/upper 24-hour half-amplitude ratios; sensitivity ranges, not confidence intervals.');
text(s,'University Valley 保留',852,180,370,46,28,C.teal,true);
text(s,'支援已知剖面的\n分層熱傳與 QA。',852,248,350,86,29);
text(s,'材料、覆土與冰效應\n尚不能唯一分離。',852,370,360,86,29,C.orange,true);
text(s,'沒有同材料無冰對照；\n不推定 MS-01 的冰深。',852,482,360,72,23,C.muted);
text(s,'F01｜2010-11-07（含）–11-18（不含）；S/M/D 各 264 列，W 528 列。',56,578,1168,25,17,C.muted);
text(s,'比值無單位；橫線＝逐日留一範圍（非信賴區間）。原印刷時標，未做跨 logger 配時。',56,609,1168,26,17,C.muted);
// 4
s=page(4,'MS-02｜用途可保留，證據不能跨點拼接','候選處置',['R02','D03','P03','P04','P05'],
`MS-02 保留 University Valley 為乾燥覆土下冰膠結層與季節熱響應的過程參照。這是用途支持，不是定量最相似，也不是 MS-02 地下冰證明。\n\nAdventdalen 降為一般方法參照。F02 是依交付 footprint.csv 與報告 §8B 整理的證據範圍表，沒有新量測或新距離計算。CS-1：78.201°N、15.840°E，0–3.22 m 岩芯，有 OSL 年代、含冰量與冰構造；記錄涵蓋約 3000 年，取芯日期未萃取。ADE：78.1722°N、16.0613°E，2017 年 3 月鑽孔 13 m / 9 m，研究孔隙水化學及凍結結構。兩錨點間 5.97 km 沿用 MS-02 原計算。\n\nWISDOM 的 2022 年 3 月多邊形溝槽測線未取得座標，只有摘要層級；約 1.5 m 反射是作者解釋，缺該溝槽獨立冰真值。Longyearbreen 冰洞真值屬另一地形，不能挪用。未知座標不等於已確認不重疊，但不能視為同址。\n\n保留 CS-1 覆土堆積與同生冰的地球過程證據；雷達驗冰的具體配對證據不足。沙塵光學厚度不能轉成覆土厚度或堆積率。原報告早段部分假設已由 §8B 降級取代；未採用未核實的水活度與 2560 h 聯合門檻。`);
text(s,'保留 University Valley：乾覆土／冰界面的熱響應過程參照',56,164,1168,40,27,C.teal,true);
table(s,[['Adventdalen 證據','實際支撐範圍','缺件或限制'],['CS-1 岩芯','0–3.22 m；約 3000 年沉積史\n含冰量、冰構造與 OSL 年代','取芯日期未取得；\n不是雷達測線'],['ADE 鑽孔','2017 年 3 月；13 m／9 m 孔\n與 CS-1 相距 5.97 km¹','支持凍結／化學結構；\n沒有共址雷達'],['WISDOM 多邊形測線','2022 年 3 月；僅摘要\n作者解釋約 1.5 m 反射','座標未知；\n缺同處獨立冰真值']],56,228,1168,304,[300,450,418],22);
text(s,'降級：一般方法參照。只保留 CS-1 的覆土堆積／同生冰過程證據。',56,555,1168,37,25,C.orange,true);
text(s,'F02｜地球點／剖面證據表；深度 m、距離 km。¹沿用原計算；未知測線不畫成共址。',56,610,1168,26,17,C.muted);
//5
s=page(5,'MS-03｜有目錄覆蓋，形貌仍無法確認','完成的查核',['R03','D04','D05','P06','P07'],
`F03 依已交 CTX 足跡重新排版，保留原局部影像像素；未重算幾何或新增判讀。左為火星名義格 57.50–58.00°N、242.00–242.50°E 與三個 CTX 目錄足跡；中為 D01_027566_2370_XN_57N117W 的局部原生 EDR。AD1 只以已交幾何摘要作取樣尺度說明，不與火星影像混用座標。\n\n三個 CTX 產品拍攝日期為 2010-07-25、2012-06-13、2025-01-31，名義取樣 6.08–6.11 m/pixel。原圖中的局部原生影像為 2012-06-13，6.09 m/pixel，未完成精定位／正射，存在條帶與低對比。目錄足跡聯集涵蓋名義格，不代表整格有效像素或可辨識細節均已核實。\n\nAD1 GIS 共 185 個有效多邊形，EPSG:32633，等效直徑中位 18.485 m。源文影像為 2008 年 HRSC-AX，2009 年為現地工作／資料目錄脈絡，原 raster 未取得，本輪不聲稱已做地球影像 QA。18.5 m 除以 6.09 m/pixel 約 3.04 像素，只示意取樣，不是偵測閾值。\n\n受查 ODE 與任務索引沒有找到可直接支援格內判讀的有效 HiRISE 紀錄，不構成完整歷史無覆蓋。AD1 退出目前有證據支持的具體配對，保留一般已知方法參照。現有證據既不能確認相似，也不能確認不同或不存在。成因及地下冰還需同位材料／層序、精定位影像與獨立地下結構證據。`);
text(s,'目錄足跡 ≠ 有效像素覆蓋',56,156,460,35,24,C.teal,true);
await image(s,'F03_CTX_coverage.png',45,200,470,380,'F03a: Delivered CTX catalogue corner footprints in Mars planetocentric degrees, not effective image coverage.');
text(s,'CTX 局部原生 EDR',530,156,370,35,24,C.teal,true);
await image(s,'MS03_CTX_patch.png',530,200,350,350,'F03b: Unchanged author-delivered stretched CTX EDR crop, D01 2012-06-13, not orthorectified or north-up.');
text(s,'AD1 取樣尺度',914,194,310,35,25,C.ink,true);
text(s,'等效直徑中位\n18.5 m\n\n在 CTX 約 3 像素',914,248,310,172,26);
text(s,'僅為取樣示意；\n不是偵測門檻。\n兩地形貌比較未知。',914,435,310,109,23,C.orange,true);
text(s,'AD1 降為一般方法參照；現有影像不足以確認可比較的裂隙／多邊形。',56,577,1168,36,24,C.orange,true);
text(s,'F03｜足跡：2010／2012／2025；局部：2012-06-13，6.09 m/pixel，未正射、有條帶。',56,616,1168,25,17,C.muted);
//6
s=page(6,'前人已做什麼？本隊實際增加什麼？','研究差異',['R01T','R02','R03','P01','P06'],
`University Valley 已有觀測、熱傳模型與火星類比研究；Adventdalen／AD1 已有火星形貌比較及雷達方法工作。這些不是本隊首次提出。\n\nMS-01 增加固定窗口、逐站／逐通道 QA 與已交熱振幅比較；MS-02 增加出處、位置、時間、深度的共址稽核，修正把不同點拼成聯合驗冰的主張；MS-03 增加固定候選格的影像可辨識性檢查與原始 AD1 GIS 幾何核對。這些屬重現、資料整合與適用性查核，可追溯而可檢查。\n\n我們沒有新場址發現、新的火星冰觀測、受控辨識效能或全球完整新穎性排除。相同方法組成已有先例，不能把較長的方法描述稱全新流程。`);
table(s,[['案例','前人已有','本隊完成的增加'],['MS-01','UV 已知剖面觀測、\n熱傳模型與火星類比','固定窗口重現；\n通道／位置／時標 QA 與敏感度'],['MS-02','覆土沉積、鑽孔、\n雷達及火星類比研究','把證據放回各自位置與期間；\n修正無共址支撐的聯合主張'],['MS-03','AD1 幾何與既有\nSvalbard–Mars 比較','固定 MS-03 格的影像查核；\n用可觀測尺度決定配對降級']],56,177,1168,338,[190,400,578],24);
text(s,'研究定位：可重現的資料整合、QA 與用途適用性檢查。',56,559,1168,43,30,C.teal,true);
text(s,'不主張首次類比、新場址，或已驗證火星地下冰。',56,611,1168,30,22,C.muted);
//7
s=page(7,'三點比較：可支持的用途與下一筆關鍵證據','整合判斷',['R01T','R02','R03','D01'],
`三點沒有總體相似度排名。保留或降級只針對已提出用途及當下證據。MS-01 的 UV 是已知剖面方法參照，但不能唯一歸因；MS-02 UV 保留，Adventdalen 僅 CS-1 地球過程證據可用；MS-03 AD1 不保留為具體形貌配對，形貌仍未知。\n\n下一筆關鍵證據是研究缺口，不是本隊已取得成果，也不是正式期望資訊價值計算。MS-01 需要同材料無冰對照與邊界條件；MS-02 需要精確測線、同位獨立冰真值；MS-03 需要格內可精定位且能辨識邊界的影像及品質檢查。即使未來形貌相近，也不能直接推出相同成因或冰量。\n\n共同限制：地球與火星材料、輻射、大氣、重力與日照條件不同；溫度不等於熱慣量，SWIM 不是冰量，柱光學厚度不是沉積率。不同尺度支撐不直接相減、拼接或排名。Campbell 與 HOBO 校時仍未確認，跨 logger 配時／相位結論禁用。`);
table(s,[['案例','目前用途／處置','尚缺的關鍵證據'],['MS-01','UV 保留：已知剖面熱響應\n可作分層模型／QA 參照','同材料無冰對照與邊界控制；\n材料與冰效應尚未分離'],['MS-02','UV 保留；Adventdalen 降級\nCS-1 只支持地球覆土過程','共址雷達測線與獨立冰真值；\n未知座標不能視為共址'],['MS-03','AD1 降為一般方法參照\n具體形貌配對證據不足','格內可辨識、可精定位影像；\n再談共同尺度幾何比較']],56,174,1168,330,[180,485,503],23);
text(s,'共同限制',56,542,200,33,25,C.orange,true);
text(s,'尺度與物理量不同；地球證據不能直接證明火星的冰深、冰量或可採性。',56,589,1168,48,25);
//8
s=page(8,'目前的價值：讓下一步研究有可檢查的起點','目前可支持的結論',['R01T','R02','R03'],
`收束：完成的是三個固定候選的用途與資料適用性檢查。UV 可支援熱傳資料重現及模型 QA；Adventdalen 證據不能跨點拼成雷達驗冰；MS-03 形貌未知，AD1 降級。把不足說清楚，可以避免把後續工作建立在不成立的聯合證據上。\n\n後續驗證需求已列明，沒有在本輪執行新實驗。團隊現在可稱資料整合、QA、重現與研究需求設計；不能稱新場址、首次類比、偵測準確度或火星冰已證實。\n\n待確認：S/D 位置來源衝突；W 不同匯出版本與 Campbell/HOBO 歷史時標；Adventdalen 雷達測線／真值及僅摘要來源；MS-03 格內有效像素與更細影像。本 8 頁展示稿仍需確認正式提交格式。所有研究 PR 作為各自固定 SHA 輸入，不代表已合併或主線最終科學驗收。`);
text(s,'01',56,180,80,55,38,C.teal,true);text(s,'把可用的用途保留下來',155,182,1050,44,32,C.ink,true);
text(s,'University Valley 提供已知剖面的熱響應資料，支援重現與模型 QA。',155,243,1050,56,26);
text(s,'02',56,330,80,55,38,C.teal,true);text(s,'把缺少關鍵證據的配對降級',155,332,1050,45,32,C.ink,true);
text(s,'Adventdalen 不拼成共址驗冰；MS-03 不把無法辨識寫成不存在。',155,393,1050,56,26);
text(s,'03',56,480,80,55,38,C.teal,true);text(s,'明確列出下一步驗證需要什麼',155,482,1050,45,32,C.ink,true);
text(s,'材料對照、同位地下真值，以及足以辨識格內形貌的影像。',155,543,1050,56,26);
text(s,'完成：資料整合與查核　｜　待驗證：因果解釋與火星地下冰',56,610,1168,30,22,C.orange,true);
await fs.mkdir(tmp,{recursive:true});await fs.mkdir(path.join(tmp,'previews'),{recursive:true});
await fs.writeFile(path.join(tmp,'sources.json'),JSON.stringify(sources,null,2));
await fs.writeFile(path.join(tmp,'notes.json'),JSON.stringify(noteBlocks,null,2));
const notes='# Team zasa 研究展示講稿\n\n本版 8 頁；圖表與結論沿用固定研究提交，未新增場址或資料分析。\n\n'+noteBlocks.map(b=>`## ${b.n}. ${b.title}\n\n${b.note}\n\n### 本頁來源\n\n${b.ids.map(id=>`- [${id}：${sources[id].title}](${sources[id].url})`).join('\n')}\n`).join('\n');
await fs.writeFile(path.join(root,'docs/integration/presentation/speaker_notes.md'),notes);
for(let i=0;i<p.slides.items.length;i++){
 const slide=p.slides.items[i];
 await fs.writeFile(path.join(tmp,'previews',`slide-${String(i+1).padStart(2,'0')}.png`),new Uint8Array(await(await p.export({slide,format:'png',scale:1.5})).arrayBuffer()));
 console.log(`Rendered slide ${i+1}`);
}
await(await PresentationFile.exportPptx(p)).save(path.join(tmp,'candidate.pptx'));
console.log('PPTX candidate exported; finalize and convert via LibreOffice using README instructions.');
