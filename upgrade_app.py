from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

# بررسی اینکه ارتقا دوباره اجرا نشده باشد
if 'id="feed"' in s:
    print("ابزارهای جدید از قبل وجود دارند؛ تغییری اعمال نشد.")
    raise SystemExit(0)

# افزودن گزینه‌های تبدیل واحد
old_options = '''<option value="pressure">بار به مگاپاسکال / برعکس</option>'''
new_options = '''<option value="pressure">بار به مگاپاسکال / برعکس</option>
<option value="torque">نیوتن‌متر به پوند-فوت / برعکس</option>
<option value="power">کیلووات به اسب‌بخار / برعکس</option>'''

if old_options not in s:
    raise SystemExit("گزینه تبدیل فشار پیدا نشد؛ فایل بدون تغییر باقی ماند.")

s = s.replace(old_options, new_options, 1)

# افزودن دکمه‌های ناوبری
old_nav = '''<button data-id="torque"><b>↻ گشتاور</b><small>گشتاور خروجی</small></button>'''
new_nav = old_nav + '''
<button data-id="feed"><b>⚙ پیشروی CNC</b><small>سرعت پیشروی ابزار</small></button>
<button data-id="machining"><b>◷ زمان ماشین‌کاری</b><small>زمان نظری برش</small></button>'''

if old_nav not in s:
    raise SystemExit("دکمه گشتاور پیدا نشد؛ فایل بدون تغییر باقی ماند.")

s = s.replace(old_nav, new_nav, 1)

# افزودن صفحه‌های محاسباتی
old_footer = '<footer>ابزارک صنعت · نتایج نیازمند بررسی شرایط واقعی کار هستند.</footer>'

new_sections = r'''
<section class="panel hide" id="feed">
<h2>سرعت پیشروی CNC</h2>
<label>دور اسپیندل (rpm)</label>
<input id="fn" type="number" value="3000" min="0" step="any">
<label>تعداد دندانه ابزار</label>
<input id="fz" type="number" value="4" min="1" step="1">
<label>پیشروی هر دندانه (mm/tooth)</label>
<input id="fzv" type="number" value="0.05" min="0" step="any">
<button class="go" onclick="feedrate()">محاسبه پیشروی</button>
<div class="result">سرعت پیشروی نظری
<strong id="fr">600 mm/min</strong>
<div class="note">Vf = n × z × fz</div>
</div>
</section>

<section class="panel hide" id="machining">
<h2>زمان تقریبی ماشین‌کاری</h2>
<label>طول مسیر برش (mm)</label>
<input id="ml" type="number" value="100" min="0" step="any">
<label>سرعت پیشروی (mm/min)</label>
<input id="mf" type="number" value="600" min="0" step="any">
<button class="go" onclick="machiningTime()">محاسبه زمان</button>
<div class="result">زمان نظری برش
<strong id="mt">10 ثانیه</strong>
<div class="note">زمان (دقیقه) = طول مسیر ÷ سرعت پیشروی</div>
</div>
</section>
''' + old_footer

if old_footer not in s:
    raise SystemExit("پاورقی پیدا نشد؛ فایل بدون تغییر باقی ماند.")

s = s.replace(old_footer, new_sections, 1)

# جایگزینی تابع تبدیل واحد با پشتیبانی از چهار نوع واحد
start = s.index("function units(){")
end = s.index("function rpm(){", start)

new_units = r"""function units(){
 const v=readNumber('uv');
 const k=$('kind').value;
 const d=Number($('direction').value);
 if(v===null || v<0){
  invalid('ur','لطفاً عدد معتبر و غیرمنفی وارد کنید');
  $('un').textContent='ورودی خالی یا نامعتبر است';
  return;
 }
 const cfg={
  length:{factor:25.4,from:'mm',to:'in'},
  pressure:{factor:10,from:'bar',to:'MPa'},
  torque:{factor:1.355817948,from:'N·m',to:'lbf·ft'},
  power:{factor:0.745699872,from:'kW',to:'hp'}
 };
 const c=cfg[k];
 let from=c.from,to=c.to;
 const out=d===1?v/c.factor:v*c.factor;
 if(d===2)[from,to]=[to,from];
 $('ur').textContent=f(out)+' '+to;
 $('un').textContent=f(v)+' '+from+' = '+f(out)+' '+to;
}
"""

s = s[:start] + new_units + s[end:]

# افزودن توابع پیشروی و زمان پیش از راه‌اندازی اولیه
marker = "$('kind').onchange=units;"
new_functions = r"""
function feedrate(){
 const n=readNumber('fn'),z=readNumber('fz'),fz=readNumber('fzv');
 if(n===null||z===null||fz===null||n<=0||z<1||!Number.isInteger(z)||fz<=0){
  invalid('fr','دور، تعداد دندانه و پیشروی باید مقادیر معتبر و مثبت باشند');
  return;
 }
 invalid('fr',f(n*z*fz)+' mm/min');
}
function machiningTime(){
 const l=readNumber('ml'),v=readNumber('mf');
 if(l===null||v===null||l<0||v<=0){
  invalid('mt','طول مسیر باید غیرمنفی و سرعت پیشروی مثبت باشد');
  return;
 }
 const minutes=l/v;
 if(minutes<1){
  invalid('mt',f(minutes*60)+' ثانیه');
 }else{
  invalid('mt',f(minutes)+' دقیقه');
 }
}
"""

if marker not in s:
    raise SystemExit("محل راه‌اندازی توابع پیدا نشد؛ فایل بدون تغییر باقی ماند.")

s = s.replace(marker, new_functions + "\n" + marker, 1)

# اجرای محاسبات هنگام بارگذاری
old_init = "units();rpm();gear();torque();"
new_init = "units();rpm();gear();torque();feedrate();machiningTime();"

if old_init not in s:
    raise SystemExit("خط راه‌اندازی اولیه پیدا نشد؛ فایل بدون تغییر باقی ماند.")

s = s.replace(old_init, new_init, 1)

p.write_text(s, encoding="utf-8")
print("ارتقا با موفقیت انجام شد.")
