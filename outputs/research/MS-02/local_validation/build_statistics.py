#!/usr/bin/env python3
"""Compile MS-02 statistics tables (counts only, no prose conclusions). Run from anywhere."""
import csv, json, pathlib, subprocess, sys, collections as C
R=pathlib.Path(__file__).resolve().parents[4]; M=R/"outputs/research/MS-02"; L=M/"local_validation"
rd=lambda p:list(csv.DictReader(open(p,encoding="utf-8-sig")))
def tab(h,rows): return "\n".join(["| "+" | ".join(h)+" |","|"+"---|"*len(h)]+["| "+" | ".join(str(x) for x in r)+" |" for r in rows])
def cnt(rows,key,f=lambda v:v): return sorted(C.Counter(f(r[key]) for r in rows).items(),key=lambda x:-x[1])
out=["# MS-02 統計彙整（僅計數與核對結果；非報告正文）\n",f"目標：MS-02，52.75°N、168.25°E；branch research/ms-02-earth-analogs；HEAD `{subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD']).decode().strip()}`\n"]
files=[("candidates.csv",M),("claims.csv",M),("evidence.csv",M),("footprint.csv",M),("prior_work.csv",M),("search_log.csv",M),
 ("local_prior_work.csv",L),("mars_ice_evidence.csv",L),("analog_validation.csv",L),("search_log.csv",L),("scale_gap_resolution.csv",L)]
out+=["## 1. 檔案與列數\n",tab(["檔案","資料列"],[(("local_validation/" if d==L else "")+f,len(rd(d/f))) for f,d in files]),""]
ev=rd(M/"evidence.csv")
out+=["\n## 2. 證據表 evidence.csv（61 列）\n","依候選：",tab(["candidate","列數"],cnt(ev,"candidate_id")),"\n依面向：",tab(["facet","列數"],cnt(ev,"facet")),
 "\n依證據類型（取第一個詞）：",tab(["類型","列數"],cnt(ev,"evidence_type",lambda v:v.split("(")[0].split("+")[0])),""]
cl=rd(M/"claims.csv");out+=["\n## 3. 主張 claims.csv\n",tab(["claim_id","狀態"],[(r["claim_id"],r["status"]) for r in cl]),""]
fp=rd(M/"footprint.csv");out+=["\n## 4. 足跡 footprint.csv 幾何狀態\n",tab(["狀態","數"],cnt(fp,"geometry_status",lambda v:v.split(" (")[0])),""]
pw=rd(M/"prior_work.csv");out+=["\n## 5. 先例 prior_work.csv 分類\n",tab(["分類","數"],cnt(pw,"classification_vs_MS02_use",lambda v:v.split(" (")[0])),""]
ca=rd(M/"candidates.csv");out+=["\n## 6. 地球候選處置\n",tab(["id","處置"],[(r["candidate_id"],r["disposition"].split(" (")[0]) for r in ca]),""]
lp=rd(L/"local_prior_work.csv");out+=["\n## 7. local_validation 先例（14 列）\n",tab(["分類","數"],cnt(lp,list(lp[0])[-1] if False else [k for k in lp[0] if "class" in k.lower()][0],lambda v:v.split(" (")[0])),""]
sg=rd(L/"scale_gap_resolution.csv");out+=["\n## 8. 尺度缺口判定\n",tab(["id","主題","狀態"],[(r["id"],r["theme"],r["status"]) for r in sg]),""]
D=json.load(open(L/"derived_metrics.json"))
out+=["\n## 9. MS-02 格尺度數值（來源 hand-off main 共享資料）\n",tab(["項目","值"],[("格大小 km (EW×NS)","29.636 × 17.938（約 531.6 km²）"),("MOLA 平均 m",D["MOLA"]["mean_m"]),("MOLA 坡度 平均/最大 °",f'{D["MOLA"]["slope_mean_deg"]}/{D["MOLA"]["slope_max_deg"]}'),("MOLA 起伏 m",D["MOLA"]["relief_m"]),
 ("TES TI 平均/中位/範圍/標準差",f'{D["TES_TI"]["mean"]:.3f}/{D["TES_TI"]["median"]}/{D["TES_TI"]["min"]}–{D["TES_TI"]["max"]}/{D["TES_TI"]["std"]}'),("TES 有效格","93/100"),("SWIM 0–1 m 平均",round(D["SWIM_0_1m"]["mean"],4)),("SWIM 1–5 m 平均",round(D["SWIM_1_5m"]["mean"],4)),
 ("CDOD MY34 平均/p95",f'{D["CDOD"]["MY34_mean"]:.4f}/{D["CDOD"]["MY34_p95"]:.4f}'),("CDOD MY35 平均/p95",f'{D["CDOD"]["MY35_mean"]:.4f}/{D["CDOD"]["MY35_p95"]:.4f}'),
 ("最近 Morgan 2025 冰點 km","389.0 (Site 46)"),("距 Bramson/Viola/Ramsdale/Séjourné km","463.6/421.1/628.7/2534.5")]),""]
res=[]
for s in ["local_validation/verify_local_validation.py","local_validation/verify_scale_gap.py"]:
    p=subprocess.run([sys.executable,"-I",str(M/s)],capture_output=True,text=True,cwd=R);res.append((s,"PASS" if p.returncode==0 else "FAIL",(p.stdout.strip().splitlines() or [""])[-1][:100]))
v=json.load(open(M/"verification.json"));res.append(("verification.json（原 PR 腳本）","PASS" if v.get("all_consistency_checks_pass") else "FAIL",f'{len(v["checks"])} checks'))
out+=["\n## 10. 核對結果（本次重跑）\n",tab(["腳本","結果","摘要"],res),""]
(L/"statistics_summary.md").write_text("\n".join(out)+"\n",encoding="utf-8");print("\n".join(out))
