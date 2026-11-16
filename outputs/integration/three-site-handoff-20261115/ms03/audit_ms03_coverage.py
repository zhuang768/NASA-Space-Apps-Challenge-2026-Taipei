import csv, hashlib, json, math, pathlib, re, urllib.parse, urllib.request

P=pathlib.Path(__file__).parent
roi=(242.0, 57.5, 242.5, 58.0)  # W,S,E,N; planetocentric, east-positive
ext=(241.5,57.,243.,58.5)
rad=math.radians
radius=3396.19
checks=[]
FETCHED = P / "downloaded"
ODE = "https://oderest.rsl.wustl.edu/live2/"
RED = "https://hirise.lpl.arizona.edu/PDS/RDR/PSP/ORB_006800_006899/PSP_006864_2380/PSP_006864_2380_RED.LBL"

def acquire(name, url):
    # Reuse any retained source. Otherwise download to a separate raw cache.
    for path in (P / name, FETCHED / name):
        if path.is_file():
            return path
    FETCHED.mkdir(exist_ok=True)
    path = FETCHED / name
    with urllib.request.urlopen(url, timeout=25) as response:
        content = response.read(2_000_000)
    if len(content) == 2_000_000:
        raise ValueError("Unexpectedly large source: " + name)
    path.write_bytes(content)
    return path
def check(ok, label):
    if not ok: raise ValueError(label)
    checks.append(label)
def area(bounds):
    w,s,e,n=bounds
    return radius**2 * rad(e-w) * (math.sin(rad(n))-math.sin(rad(s)))
def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def csv_out(file, rows):
    with (P/file).open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
def secant_area(latitude):
    # Inverse area scale for the documented pole-tangent spherical stereographic.
    return ((1+math.sin(rad(latitude)))/2)**2

src=json.loads((P/'coverage_input.json').read_text())
a=area(roi)
ctx=[]
for sample in src["samples"]:
    b=sample["overlay"]["bounds"]
    w,s,e,n=b["west"]+360,b["south"],b["east"]+360,b["north"]
    check(roi[0]<=w<e<=roi[2] and roi[1]<=s<n<=roi[3] and sample["acquired"],"CTX "+sample["sample_id"]+" inside, acquired")
    v=area((w,s,e,n))
    ctx.append(dict(id=sample["sample_id"],west_east_deg=w,east_east_deg=e,south_north_deg=s,north_north_deg=n,area_km2=v,pct_of_cell=v/a*100,source_url=sample["overlay"]["url"]))
for i,b in enumerate(ctx):
    for c in ctx[i+1:]:
        check(b["east_east_deg"]<=c["west_east_deg"] or c["east_east_deg"]<=b["west_east_deg"] or b["north_north_deg"]<=c["south_north_deg"] or c["north_north_deg"]<=b["south_north_deg"],f"nonoverlap {b['id']} / {c['id']}")
csv_out("ctx_review_area.csv",ctx)
m=src["moc"]
pix=(m["map_grid_m"]/1000)**2
check(all(t["valid_roi_pixels"]==512**2 for t in m["tiles"]),"MOC review windows 512×512 all valid")
check(len(m["tiles"])==3 and all(x["source_rows_0based_inclusive"][1]<y["source_rows_0based_inclusive"][0] for x,y in zip(m["tiles"],m["tiles"][1:])),"MOC review windows disjoint")
f=[secant_area(roi[1]), secant_area(roi[3])]
whole=[m["roi_valid_nonzero_pixel_centres"]*pix*k for k in f]
seen=[sum(t["valid_roi_pixels"] for t in m["tiles"])*pix*k for k in f]

rows=[]
ps=[]
for typ in ("RDRV11","RDR4","DTM"):
    for label, bounds in [("core",roi),("extended",ext)]:
        name=f"{typ}-{label}.json"
        params=dict(query="product", target="mars", ihid="mro", iid="hirise",
            output="json", results="copmf", pt=typ, minlat=bounds[1],
            maxlat=bounds[3], westernlon=bounds[0], easternlon=bounds[2])
        p=acquire(name, ODE+"?"+urllib.parse.urlencode(params))
        r=json.loads(p.read_bytes())["ODEResults"]
        q=r["QuerySummary"]
        check(q["pt"].upper()==typ and q["iid"].upper()=="HIRISE" and tuple(float(q[k]) for k in ["westernlon","minlat","easternlon","maxlat"])==bounds, p.name+" exact echoed request")
        n=int(r["Count"]); v=r["Products"]
        products=v.get("Product",[]) if isinstance(v,dict) else []
        if isinstance(products,dict):products=[products]
        check(len(products)==n,p.name+" all product records present")
        ids=set(d["Observation_id"] for d in products)
        rows.append(dict(query_label=label,product_type=typ,west=bounds[0],south=bounds[1],east=bounds[2],north=bounds[3],catalogue_count=n,observations=len(ids),query_date_as_returned=q["Date"],raw_file=p.name,sha256=sha(p)))
        for d in products:
            geom=d["Footprint_geometry"]
            parts=re.findall(r"([0-9.]+) ([0-9.]+)",geom)
            check(geom.startswith("POLYGON") and len(parts)>=4 and parts[0]==parts[-1],"closed ODE WKT "+d["pdsid"])
            maxlon=max(float(x) for x,_ in parts)
            check(maxlon<roi[0],"ODE polygon entirely west: "+d["pdsid"])
            ps.append(dict(product=d["pdsid"],observation=d["Observation_id"],footprint_wkt=geom,easternmost_deg_from_wkt=maxlon,utc_start_as_supplied=d["UTC_start_time"],native_map_scale_m_per_pixel=d["Map_scale"],intersects_roi="false (longitude separation)",file_label_url=d["LabelURL"]))
check([r["catalogue_count"] for r in rows]==[0,2,0,0,0,0],"observed hit counts")
label=acquire("PSP_006864_2380_RED.LBL", RED)
east=float(re.search(r"^\s*EASTERNMOST_LONGITUDE\s*=\s*([0-9.]+)",label.read_text(),re.M).group(1))
check(east<242 and abs(east-241.83751839088)<1e-9,"original RED label independently excludes lon overlap")
csv_out("hirise_query_results.csv",rows)
csv_out("hirise_nearby_footprints.csv",ps)

result=dict(cell_area_km2=a,ctx_five_review_area_km2=sum(p["area_km2"] for p in ctx),ctx_five_review_pct=sum(p["pct_of_cell"] for p in ctx),
  moc_all_retained_valid_area_approx_bounds_km2=whole,moc_all_retained_valid_area_approx_bounds_pct=[x/a*100 for x in whole],
  moc_three_review_windows_area_approx_bounds_km2=seen,moc_three_review_windows_area_approx_bounds_pct=[x/a*100 for x in seen],
  moc_coverage_note="Approximate valid pixel area from min/max local stereographic Jacobian over pixel centres; ignores boundary subpixel correction. The separate image-support and visual-review bounds are not polygon-detection efficacy. Do not add CTX and MOC percentages (potential overlap).",
  hirise_original_label_eastmost_deg=east,hirise_red_label_sha256=sha(label),
  checks_passed=len(checks),checks=checks)
(P/"coverage_summary.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k!="checks"},indent=2))
