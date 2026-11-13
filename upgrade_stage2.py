from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

if 'id="hydraulic"' in s and 'id="spindleTorque"' in s:
    print("این دو ابزار قبلاً اضافه شده‌اند؛ تغییری اعمال نشد.")
    raise SystemExit(0)

nav_marker = '<button data-id="machining"><b>◷ زمان ماشین‌کاری</b><small>زمان نظری برش</small></button>'

nav_add = nav_marker + '''
<button data-id="spindleTorque"><b>◉ گشتاور اسپیندل</b><small>توان و دور موتور</small></button>
<button data-id="hydraulic"><b>↗ نیروی هیدرولیک</b><small>فشار و قطر سیلندر</small></button>'''

if 'id="spindleTorque"' not in s:
    if nav_marker not in s:
        raise SystemExit("دکمه زمان ماشین‌کاری پیدا نشد؛ فایل تغییر نکرد.")
    s = s.replace(nav_marker, nav_add, 1)

footer = '<footer>ابزارک صنعت · نتایج نیازمند بررسی شرایط واقعی کار هستند.</footer>'

sections = r'''
<section class="panel hide" id="spindleTorque">
<h2>گشتاور اسپیندل CNC</h2>
<label>توان در دسترس اسپیندل (kW)</label>
<input id="sp" type="number" value="7.5" min="0" step="any">
<label>دور اسپیندل (rpm)</label>
<input id="sn" type="number" value="3000" min="0" step="any">
<button class="go" onclick="spindleTorque()">محاسبه گشتاور</button>
<div class="result">گشتاور نظری
<strong id="sr">23.875 N·m</strong>
<div class="note">T (N·m) ≈ 9550 × P (kW) ÷ n (rpm)</div>
</div>
<p class="note">توان باید توان مکانیکی در دسترس اسپیندل باشد. تلفات انتقال و تغییرات گشتاور موتور در دورهای مختلف ممکن است نتیجه واقعی را تغییر دهند.</p>
</section>

<section class="panel hide" id="hydraulic">
<h2>نیروی جک هیدرولیک</h2>
<label>فشار کاری (bar)</label>
<input id="hp" type="number" value="100" min="0" step="any">
<label>قطر داخلی سیلندر (mm)</label>
<input id="hd" type="number" value="50" min="0" step="any">
<button class="go" onclick="hydraulicForce()">محاسبه نیرو</button>
<div class="result">نیروی تئوری سمت پیستون
<strong id="hr">19.635 kN</strong>
<div class="note">F (kN) = P (bar) × π × D² ÷ 40000</div>
</div>
<p class="note">این نتیجه برای حرکت خروجی سیلندر از سمت سطح کامل پیستون است و اصطکاک، افت فشار و نیروی برگشتی را لحاظ نمی‌کند.</p>
</section>
'''

if 'id="spindleTorque"' not in s:
    if footer not in s:
        raise SystemExit("پاورقی پیدا نشد؛ فایل تغییر نکرد.")
    s = s.replace(footer, sections + "\n" + footer, 1)

marker = "$('kind').onchange=units;"

functions = r"""
function spindleTorque(){
 const p=readNumber('sp'),n=readNumber('sn');
 if(p===null||n===null||p<0||n<=0){
  invalid('sr','توان باید غیرمنفی و دور باید بزرگ‌تر از صفر باشد');
  return;
 }
 invalid('sr',f(9550*p/n)+' N·m');
}
function hydraulicForce(){
 const p=readNumber('hp'),d=readNumber('hd');
 if(p===null||d===null||p<0||d<=0){
  invalid('hr','فشار باید غیرمنفی و قطر باید بزرگ‌تر از صفر باشد');
  return;
 }
 const force=p*Math.PI*d*d/40000;
 invalid('hr',f(force)+' kN');
}
"""

if "function spindleTorque(){" not in s:
    if marker not in s:
        raise SystemExit("محل افزودن توابع پیدا نشد؛ فایل تغییر نکرد.")
    s = s.replace(marker, functions + "\n" + marker, 1)

init = "feedrate();machiningTime();"
if init not in s:
    raise SystemExit("خط راه‌اندازی قبلی پیدا نشد؛ فایل تغییر نکرد.")

if "spindleTorque();hydraulicForce();" not in s:
    s = s.replace(init, init + "spindleTorque();hydraulicForce();", 1)

p.write_text(s, encoding="utf-8")
print("دو ابزار جدید اضافه شدند.")
