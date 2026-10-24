import numpy as np, pandas as pd
from pathlib import Path

rng = np.random.default_rng(42)
OUT = Path("data/raw"); OUT.mkdir(parents=True, exist_ok=True)
START, END = pd.Timestamp("2023-01-01"), pd.Timestamp("2026-09-30")
days = pd.date_range(START, END)

# ---------- branches and routes ----------
branches = pd.DataFrame({
    "branch_id": range(1, 11),
    "branch": ["Nairobi","Mombasa","Kisumu","Nakuru","Eldoret","Garissa","Kisii","Nyeri","Kitale","Malindi"],
    "county": ["Nairobi","Mombasa","Kisumu","Nakuru","Uasin Gishu","Garissa","Kisii","Nyeri","Trans Nzoia","Kilifi"],
    "region": ["Nairobi","Coast","Nyanza","Rift Valley","Rift Valley","North Eastern","Nyanza","Central","Rift Valley","Coast"]})
bid = dict(zip(branches.branch, branches.branch_id))

routes = pd.DataFrame([
    # origin, destination, km, base_fare(KES), seats_per_bus, trips_per_day, class
    ("Nairobi","Mombasa",480,1500,49,3,"Executive"),
    ("Mombasa","Nairobi",480,1500,49,3,"Executive"),
    ("Nairobi","Kisumu",350,1400,49,3,"Executive"),
    ("Nairobi","Eldoret",310,1200,49,2,"Standard"),
    ("Nairobi","Garissa",370,1600,33,1,"Standard"),
    ("Mombasa","Malindi",120,800,33,2,"Standard"),
    ("Nakuru","Kisii",230,900,33,1,"Standard"),
    ("Nairobi","Nyeri",150,600,49,3,"Standard"),
    ("Kisumu","Kitale",160,700,33,1,"Standard"),
    ("Nairobi","Nakuru",160,700,49,3,"Standard"),
    ("Nairobi","Kisii",300,1300,49,2,"Standard"),
    ("Nairobi","Malindi",600,1800,49,1,"Executive"),
], columns=["origin","destination","distance_km","base_fare","seats_per_bus","trips_per_day","service_class"])
routes.insert(0, "route_id", range(1, len(routes) + 1))
routes["origin_branch_id"] = routes.origin.map(bid)
routes["daily_seat_capacity"] = routes.seats_per_bus * routes.trips_per_day
routes["base_daily_bookings"] = 0.5 * routes.daily_seat_capacity / 1.6   # about 50% load at baseline

# ---------- holidays (fixed dates only; add Easter/Eid etc. yourself from the Gazette) ----------
fixed = [("01-01","New Year"),("05-01","Labour Day"),("06-01","Madaraka Day"),
         ("10-20","Mashujaa Day"),("12-12","Jamhuri Day"),("12-25","Christmas"),("12-26","Boxing Day")]
holidays = pd.DataFrame([(pd.Timestamp(f"{y}-{md}"), n) for y in range(2023, 2027) for md, n in fixed],
                        columns=["date","holiday"])
hol_set = set(holidays.date)

# ---------- customers ----------
n_cust = 6000
seg = rng.choice(["commuter","business","occasional"], n_cust, p=[.25, .15, .60])
span = (END - START).days - 30
signup_days = rng.integers(0, span, n_cust)
signup_days[rng.random(n_cust) < 0.25] = 0                  # existing base at start
signup = START + pd.to_timedelta(signup_days, unit="D")
churn = pd.Series(signup + pd.to_timedelta(rng.exponential(400, n_cust), unit="D"))
churn = churn.where(rng.random(n_cust) < 0.35)               # 35% eventually churn
customers = pd.DataFrame({"customer_id": range(1, n_cust + 1), "segment": seg,
    "home_branch_id": rng.choice(branches.branch_id, n_cust, p=[.30,.15,.10,.10,.08,.05,.07,.06,.05,.04]),
    "signup_date": signup, "churn_date": churn})
cust_w = customers.segment.map({"commuter": 6, "business": 4, "occasional": 1}).to_numpy()
churn_f = customers.churn_date.fillna(pd.Timestamp("2100-01-01"))

# ---------- daily demand per route (seasonality, trend, weekday, holiday, promo) ----------
season = {1:1.0, 2:0.9, 3:0.95, 4:1.35, 5:1.0, 6:1.05, 7:1.05, 8:1.4, 9:1.0, 10:1.0, 11:1.0, 12:1.6}
promo_set = set()                       # random 7-day promo windows
for r in routes.route_id:
    for m in pd.period_range(START, END, freq="M"):
        if rng.random() < 0.35:
            s = m.start_time + pd.Timedelta(days=int(rng.integers(0, 21)))
            promo_set |= {(s + pd.Timedelta(days=k), r) for k in range(7)}

recs = []
for d in days:
    t = (d - START).days / 365
    for r in routes.itertuples():
        promo = (d, r.route_id) in promo_set
        lam = (r.base_daily_bookings * (1 + 0.10 * t) * season[d.month]
               * (1.3 if d.dayofweek in (4, 6) else 1.0)
               * (1.25 if d in hol_set else 1.0) * (1.12 if promo else 1.0))
        n = min(rng.poisson(lam), int(r.daily_seat_capacity / 1.6))
        recs.append((d, r.route_id, n, promo))
agg = pd.DataFrame(recs, columns=["date","route_id","n","promo"])
bk = agg.loc[agg.index.repeat(agg.n)].drop(columns="n").reset_index(drop=True)

# ---------- booking details ----------
t = (bk.date - START).dt.days.to_numpy() / 365
base = bk.route_id.map(routes.set_index("route_id").base_fare).to_numpy()
bk["fare"] = np.round(base * (1 + 0.06 * t) * np.where(bk.promo, 0.9, 1.0)
                      * rng.normal(1, 0.04, len(bk)), -1)
pm = np.clip(0.60 + 0.08 * t, 0, 0.85); u = rng.random(len(bk))
bk["payment"] = np.where(u < pm, "mpesa", np.where(u < pm + (1 - pm) * 0.65, "cash", "card"))
bk["seats"] = 1 + rng.binomial(3, np.where(bk.payment == "mpesa", 0.22, 0.17))
bk["branch_id"] = bk.route_id.map(routes.set_index("route_id").origin_branch_id)

# customer assignment: only customers active in that month

# ---------- customer assignment: use actual booking dates ----------
# Assign each booking to a customer who had signed up by that date and whose churn date is after that date.

bk["date"] = pd.to_datetime(bk["date"])
cid = np.empty(len(bk), dtype=int)

# Process bookings in monthly groups to keep assignment efficient
bk["month"] = bk["date"].dt.to_period("M")

for m, idx in bk.groupby("month").indices.items():
    booking_dates = bk.iloc[idx]["date"]

    # Match each booking date to customers eligible on that date
    for booking_date in booking_dates.unique():
        date_mask = booking_dates.eq(booking_date).to_numpy()
        booking_positions = np.asarray(idx)[date_mask]

        active = (
            (customers["signup_date"] <= booking_date)
            & (churn_f > booking_date)
        ).to_numpy()

        eligible_ids = customers.loc[active, "customer_id"].to_numpy()
        weights = cust_w[active]

        if len(eligible_ids) == 0:
            raise ValueError(
                f"No eligible customers found for booking date {booking_date}"
            )

        cid[booking_positions] = rng.choice(
            eligible_ids,
            size=len(booking_positions),
            p=weights / weights.sum()
        )

bk["customer_id"] = cid
bk.insert(0, "booking_id", np.arange(1, len(bk) + 1))
bk = bk.drop(columns="month")

# ---------- inject realistic mess ----------
bk["date"] = bk.date.dt.strftime("%Y-%m-%d")
bad = rng.random(len(bk)) < 0.01; bk.loc[bad, "date"] = pd.to_datetime(bk.loc[bad, "date"]).dt.strftime("%d/%m/%Y")
var = rng.random(len(bk)) < 0.08
bk.loc[var, "payment"] = bk.loc[var, "payment"].map({"mpesa":"M-Pesa","cash":"CASH","card":"Card "})
bk.loc[rng.random(len(bk)) < 0.03, "payment"] = np.nan
bk.loc[rng.random(len(bk)) < 0.01, "customer_id"] = np.nan
bk.loc[rng.random(len(bk)) < 0.002, "fare"] = -1 * bk.fare.abs()
k = rng.random(len(bk)) < 0.001; bk.loc[k, "fare"] = bk.loc[k, "fare"] * 10
bk = pd.concat([bk, bk.sample(frac=0.015, random_state=1)], ignore_index=True)   # duplicates

# ---------- save ----------
bk.to_csv(OUT / "bookings.csv.gz", index=False, compression="gzip")
customers.to_csv(OUT / "customers.csv", index=False)
branches.to_csv(OUT / "branches.csv", index=False)
routes.to_csv(OUT / "routes.csv", index=False)
holidays.to_csv(OUT / "holidays.csv", index=False)
print(len(bk), "bookings written")