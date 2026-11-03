"""Sampling error of the 2025 to 2026 change in Michigan prime-age (25-54) participation, CPS Jan-Sep.
Household-cluster bootstrap (households resampled jointly across both years), then an assumed
design effect of 1.5 to 2.0 for geographic clustering (an assumption, not a published figure).
Run: .venv/bin/python -I scripts/cps_prime_age_error.py data/cps/mi_cps_hh.csv
"""
import sys, os, requests, pandas as pd, numpy as np
sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import get_key, load_env; load_env(); k=get_key("CENSUS_API_KEY")
M=["jan","feb","mar","apr","may","jun","jul","aug","sep"]; out=sys.argv[1]
if not os.path.exists(out):
    fr=[]
    for y in [2025,2026]:
        for i,m in enumerate(M,1):
            j=requests.get(f"https://api.census.gov/data/{y}/cps/basic/{m}",params={"get":"HRHHID,HRHHID2,PRTAGE,PEMLR,PWCMPWGT","for":"state:26","key":k},timeout=180).json()
            fr.append(pd.DataFrame(j[1:],columns=j[0]).assign(year=y,month=i))
    pd.concat(fr).to_csv(out,index=False)
d=pd.read_csv(out,dtype={"HRHHID":str,"HRHHID2":str})
d=d[(d.PRTAGE>=25)&(d.PRTAGE<=54)&(d.PEMLR>0)].copy()
d["lf"]=d.PEMLR.isin([1,2,3,4]).astype(float); d["hh"]=d.HRHHID+"-"+d.HRHHID2.astype(str)
d["wl"]=d.PWCMPWGT*d.lf
g=d.groupby(["hh","year"])[["PWCMPWGT","wl"]].sum().unstack(fill_value=0)
W=g["PWCMPWGT"].values; L=g["wl"].values  # cols: 2025, 2026
def rate(idx): w=W[idx].sum(0); l=L[idx].sum(0); return l/w*100
r=rate(np.arange(len(g))); print("prime-age LFPR 2025, 2026:", r.round(2), "change", round(r[1]-r[0],2))
print("households:", len(g), "people/month 2025, 2026:", (d.groupby("year").size()/9).round(0).to_dict())
rng=np.random.default_rng(1); ch=[]
for _ in range(2000):
    i=rng.integers(0,len(g),len(g)); x=rate(i); ch.append(x[1]-x[0])
se=np.std(ch); c=r[1]-r[0]
print(f"household bootstrap SE {se:.2f}, z {c/se:.2f}")
for de in [1.5,2.0]: print(f"with design effect {de}: SE {se*np.sqrt(de):.2f}, z {c/(se*np.sqrt(de)):.2f}")
