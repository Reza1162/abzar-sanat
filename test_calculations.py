import math
from pathlib import Path

html = Path("index.html").read_text(encoding="utf-8")

tests = [
    ("تبدیل طول با ضریب 25.4", "length:{factor:25.4" in html),
    ("تبدیل فشار با ضریب 10", "pressure:{factor:10" in html),
    ("تبدیل گشتاور", "torque:{factor:1.355817948" in html),
    ("تبدیل توان", "power:{factor:0.745699872" in html),
    ("فرمول دور اسپیندل", "1000*v/(Math.PI*d)" in html),
    ("اعتبارسنجی دور اسپیندل", "v<=0||d<=0" in html),
    ("فرمول دور گیربکس", "n/r" in html),
    ("اعتبارسنجی نسبت گیربکس", "r<=0" in html),
    ("فرمول گشتاور خروجی", "t*r*e/100" in html),
    ("اعتبارسنجی راندمان", "e<=0||e>100" in html),
    ("فرمول پیشروی CNC", "n*z*fz" in html),
    ("تابع زمان ماشین‌کاری", "function machiningTime()" in html),
    ("تابع گشتاور اسپیندل", "function spindleTorque()" in html),
    ("تابع نیروی هیدرولیک", "function hydraulicForce()" in html),
]

failed = False

print("===== بررسی ساختار برنامه =====")
for name, ok in tests:
    print(("PASS" if ok else "FAIL") + " | " + name)
    if not ok:
        failed = True

cases = [
    ("25.4 mm به inch", 25.4 / 25.4, 1.0),
    ("1 inch به mm", 1 * 25.4, 25.4),
    ("10 bar به MPa", 10 / 10, 1.0),
    ("1 MPa به bar", 1 * 10, 10.0),
    ("1 N.m به lbf.ft", 1 / 1.355817948, 0.737562),
    ("1 kW به hp", 1 / 0.745699872, 1.341022),
    ("دور اسپیندل CNC", 1000 * 120 / (math.pi * 10), 3819.718634),
    ("دور خروجی گیربکس", 1500 / 20, 75.0),
    ("گشتاور خروجی گیربکس", 688 * 20 * 90 / 100, 12384.0),
    ("پیشروی CNC", 3000 * 4 * 0.05, 600.0),
    ("زمان ماشین‌کاری 100 میلی‌متر", 100 / 600 * 60, 10.0),
    ("گشتاور اسپیندل 7.5 کیلووات در 3000 دور",
     9550 * 7.5 / 3000, 23.875),
    ("نیروی نظری سیلندر 100 بار و قطر 50 میلی‌متر",
     100 * math.pi * 50 * 50 / 40000, 19.634954),
]

print("\n===== آزمایش محاسبات نمونه =====")
for name, actual, expected in cases:
    ok = math.isclose(actual, expected, rel_tol=1e-5, abs_tol=1e-4)
    print(("PASS" if ok else "FAIL") + f" | {name}: {actual:.4f}")
    if not ok:
        failed = True

print("\nنتیجه:", "نیازمند بررسی" if failed else "همه آزمون‌ها موفق بودند")
print("توجه: این آزمون محاسبات نمونه و ساختار کد را بررسی می‌کند؛")
print("اجرای واقعی دکمه‌ها در مرورگر را به‌تنهایی تأیید نمی‌کند.")

if failed:
    raise SystemExit(1)
