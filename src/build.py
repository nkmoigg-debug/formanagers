import re,base64,sys
D='/home/claude/deck/'
FD=D+'fnt/node_modules/@fontsource/'
def u64(p): return base64.b64encode(open(p,'rb').read()).decode()
def img(n): return 'data:image/jpeg;base64,'+u64(D+f'assets/{n}.jpg')
UNIT=lambda s:re.sub(r'(?<![\w#.\-])(-?\d*\.?\d+)u(?![\w\-])',lambda m:f'calc(var(--u)*{m.group(1)})',s)

css=UNIT(open(D+'css_ref.txt').read()+open(D+'css_add.txt').read()+'''
#sEnd .in{max-width:88u}
#sEnd .h{font-size:4.6u}.m #sEnd .h{font-size:8.2u}
#sF .h{font-size:3.3u}.m #sF .h{font-size:6.4u}
.m #sA .in,.m #sB .in,.m #sC .in,.m #sD .in{max-width:88u}
''')
js=open(D+'js.txt').read()

# шрифты внутри файла (офлайн)
rng={'cyrillic':'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116','latin':'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD,U+20BD'}
faces=''
for fam,pkg,w in (('Unbounded','unbounded','900'),('Onest','onest','400'),('Onest','onest','500'),('Onest','onest','700')):
    for sub in ('cyrillic','latin'):
        faces+=f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;src:url(data:font/woff2;base64,{u64(f'{FD}{pkg}/files/{pkg}-{sub}-{w}-normal.woff2')}) format('woff2');unicode-range:{rng[sub]}}}"

ICONS={'shield':'<path d="M12 3l7 3v5c0 5-3 8-7 10-4-2-7-5-7-10V6l7-3z"/><path d="M9 12l2 2 4-4"/>','lock':'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 018 0v3"/>','doc':'<path d="M7 3h7l4 4v14H7z"/><path d="M14 3v4h4M10 12h5M10 16h5"/>','cam':'<rect x="3" y="7" width="18" height="13" rx="2"/><circle cx="12" cy="13" r="3.5"/><path d="M8 7l1.5-3h5L16 7"/>','phone':'<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>','tag':'<path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.2"/>'}
def ic(n): return f'<div class="ico"><svg viewBox="0 0 24 24">{ICONS[n]}</svg></div>'
def H(lines,base=.1,step=.09,tag='h2',cls=''):
    out=[];i=0
    for line in lines:
        ws=[]
        for w in line:
            t,c=(w if isinstance(w,tuple) else (w,''))
            ws.append(f'<span class="w"><span style="--d:{base+i*step:.2f}s"{(" class=%s"%c) if c else ""}>{t}</span></span>');i+=1
        out.append(' '.join(ws))
    return f'<{tag} class="h {cls}">'+'<br>'.join(out)+f'</{tag}>'
def bc(icon,t,s,d): return f'<div class="bc"><div style="--d:{d:.2f}s">{ic(icon)}<div><h4>{t}</h4><p>{s}</p></div></div></div>'
def pin(n,x,y,d): return f'<i class="pin" data-i="{n-1}" style="left:{x:.2f}%;top:{y:.2f}%;--d:{d:.2f}s">{n}</i>'
def shot(name,alt,pins='',extra='',d=.3):
    return f'<div class="shotw"><div class="shot" style="--d:{d}s"><img src="{img(name)}" alt="{alt}">{pins}{extra}</div></div>'


def leg(items,d0=.5):
    out='<ol class="leg">'
    for i,it in enumerate(items):
        t,sd,r=it[:3];tab=it[3] if len(it)>3 else None
        out+=f'<li class="rv" style="--d:{d0+i*.08:.2f}s" data-i="{i}"'+(f' data-tab="{tab}"' if tab is not None else '')+f'><b class="n">{i+1}</b><div><h4>{t}{" <span class=tag>обязательно</span>" if r else ""}</h4><p>{sd}</p></div></li>'
    return out+'</ol><div class="cap"></div>'
CR={'s1':(115,915,960,895),'s2':(115,887,960,950),'s3':(115,718,960,1287)}
def box(c,x1,y1,x2,y2):
    X,Y,W,Hh=CR[c];return f'left:{(x1-X)/W*100:.2f}%;top:{(y1-Y)/Hh*100:.2f}%;width:{(x2-x1)/W*100:.2f}%;height:{(y2-y1)/Hh*100:.2f}%'
def ty(c,rect,text,beat,sp=55,kind=''):
    return f'<div class="ty {kind}" data-b="{beat}" data-t="{text}" data-s="{sp}" style="{box(c,*rect)}"></div>'
def shot(name,alt,pins='',extra='',d=.3):
    return f'<div class="shotw"><div class="shot" style="--d:{d}s"><img src="{img(name)}" alt="{alt}">{extra}{pins}</div></div>'
def step(sid,eb,h,items,pic):
    return f'<section class="sl" id="{sid}"><div class="in two big"><div class="lt"><div class="eyebrow rv">{eb}</div>{h}{leg(items)}</div>{pic}</div></section>'

ICO={'ПРИЛОЖЕНИЕ':open('ico_l.txt').read(),'MAX':open('ico_mm.txt').read(),'TELEGRAM':open('ico_r.txt').read()}
LINKS={'ПРИЛОЖЕНИЕ':'https://app.dropdealer.ru','MAX':'https://max.ru/join/2rA2kvRL6sa1yu-Qorso-G_hOcH6ofVObEl90T9q0vI','TELEGRAM':'https://t.me/dropdealerofficial'}
BTN={'ПРИЛОЖЕНИЕ':'ПЕРЕЙТИ В ПРИЛОЖЕНИЕ','MAX':'ПЕРЕЙТИ В MAX','TELEGRAM':'ПЕРЕЙТИ В TG'}
def phone(name,c,pd):
    return f'<a class="phone {c}" href="{LINKS[name]}" target="_blank" rel="noopener" aria-label="Открыть: {name}" style="--pd:{pd}s"><div class="ph-in"><div class="ph-top"><span class="pn">{name}</span><i class="live"><s></s>LIVE</i></div><div class="ph-img"><img src="{ICO[name]}" alt=""></div><div class="ph-ln"></div><div class="ph-ln s"></div><div class="ph-btn">{BTN[name]}</div></div></a>'

def sit(i,tag,title,steps,note,d,kind=''):
    li=''.join(f'<li><i>{k+1}</i><span>{s}</span></li>' for k,s in enumerate(steps))
    nt=f'<div class="nt">{note}</div>' if note else ''
    return f'<div class="sit {kind} rv" style="--d:{d:.2f}s"><div class="tg">{tag}</div><h3>{title}</h3><ol>{li}</ol>{nt}</div>'

S=[]
# 1. авто
DESC='Один владелец, обслуживалась у дилера. Кузов без ДТП, есть мелкие царапины на заднем бампере. По диагностике двигатель и АКПП без замечаний.'
t1=(ty('s1',(152,1088,582,1130),'Hyundai',0,70)+ty('s1',(607,1088,1037,1130),'Solaris',0,70)
   +ty('s1',(152,1186,538,1228),'2019',0,90)+ty('s1',(607,1186,1037,1228),'80 000',0,80)
   +ty('s1',(152,1284,1037,1326),'Z94CB41BBLR000000',1,60)
   +ty('s1',(152,1392,1037,1434),'Hyundai Solaris 1.6 АТ',2,60)
   +ty('s1',(152,1501,1037,1571),DESC,3,26,'area')
   +ty('s1',(985,1466,1041,1494),'',9,0,'ctr').replace('data-t=""','data-t="" id="ctr1"').replace('></div>','>0/452</div>')
   +ty('s1',(152,1638,1037,1680),'https://autoteka.ru/report/6c1f2e8a',4,38))
t1=re.sub(r'(<div class="ty area" data-b="3" data-t="[^"]*" data-s="26")',r'\1 data-ctr="ctr1"',t1)
S.append(f'''<section class="sl" id="s1"><div class="in">
<div class="eyebrow rv"><i class="live"><s></s>ANDROID И iOS</i> · приложение дилера</div>
<h1 class="h h1"><span class="w bk"><span style="--d:.15s">Лот</span></span> <span class="w"><span style="--d:.24s">с</span></span> <span class="w"><span style="--d:.3s">телефона.</span></span></h1>
<p class="sub rv" style="--d:.7s">Заносите лот с телефона, а следите за торгами где угодно. Приложение работает на Android и iOS, и на телефоне так же быстро и удобно. Не нужно бежать к компьютеру: сфотографировали в ремзоне, на улице или в шоуруме и сразу занесли лот. Ставки видны в приложении, MAX и Telegram.</p>
<div class="phones"><div class="tapnote rv" style="--d:1.1s"><svg viewBox="0 0 24 24"><path d="M12 4v14M6 12l6 6 6-6"/></svg>Кликабельно — нажми на кнопку</div>{phone("ПРИЛОЖЕНИЕ","l",.7)}{phone("MAX","mm",.9)}{phone("TELEGRAM","r",1.1)}</div>
</div></section>''')
S.append(step('sA','Шаг 1 из 3 · Авто',H([["Данные","об"],["автомобиле."]],.1),
 [("Марка, модель, год","Заполняйте с клавиатуры: например, Hyundai и Solaris. Год выберите из списка",True),
  ("VIN","Номер из документов на автомобиль",True),
  ("Название лота","Например: Hyundai Solaris 1.6 АТ",True),
  ("Описание","Своими словами напишите состояние автомобиля или кратко изложите диагностику. Это увеличивает шансы на продажу: чем понятнее описание перекупу, тем дороже торгуют автомобиль",False),
  ("Автотека","Вставьте ссылку на отчёт из Автотеки",False)],
 shot('step1','Шаг 1: данные об автомобиле',pins=pin(1,96.35,21.7,.9)+pin(2,96.35,43.6,1.0)+pin(3,96.35,55.6,1.1)+pin(4,87.5,63,1.2)+pin(5,96.35,83.1,1.3),extra=t1)))
# 2. аукцион
t2=ty('s2',(152,1060,582,1102),'650 000',0,90)
S.append(step('sB','Шаг 2 из 3 · Аукцион',H([["Условия"],["аукциона."]],.1),
 [("Начальная цена","Цена должна быть привлекательной для партнёров. Старт в рынок или выше почти не даёт шансов: на аукционе торгуются профессиональные продавцы, то есть перекупы. Если занижаете цену, чтобы привлечь внимание к лоту, добавьте в описание «Предварительный аукцион»: так перекупы поймут, что после торгов нужно согласовать лот, а не сразу ехать на выдачу",True),
  ("Шаг ставки","Для автомобилей до 1 000 000 ₽ рекомендуем шаг 5–10 тысяч",True),
  ("Своя ставка: от и до","Позволяет поставить в приложении любую сумму в этих пределах: 15 тысяч, 27 или 38. Верхняя граница — максимум, который можно поставить",True),
  ("Быстрые ставки","Кнопки, которые покупатель видит в MAX и Telegram. Свою кнопку добавляет «+ Кнопка»",True),
  ("Старт и длительность","Сначала назначьте старт: без него конец торгов не определён. Длительность выбирайте под задачу. Предварительный аукцион, пока клиент на диагностике и нужно назвать или подтвердить стоимость: 30–90 минут. Обычный лот: 3–5 часов, от 3 часов охват среди перекупов хороший. Максимальный охват и более высокая ставка: аукцион на сутки. Нет времени: ставьте 3–5 часов",False)],
 shot('step2','Шаг 2: условия аукциона',pins=pin(1,49,20.4,.9)+pin(2,96.35,36.6,1.0)+pin(3,96.35,46.9,1.1)+pin(4,92.2,63.4,1.2)+pin(5,27.5,76.5,1.3),extra=t2)))
# 3. контакты
t3=ty('s3',(152,1180,1037,1222),'Игорь Петров, +7 921 555-12-34',1,55)
S.append(step('sC','Шаг 3 из 3 · Контакты',H([["Контакты,","фото"],["и запуск."]],.1),
 [("Компания, город, адрес","По умолчанию стоит ваш дилер, который выкладывает лот",True),
  ("Контакт дилера","Уходит покупателю после завершения торгов",True),
  ("Фото и видео","Первое фото станет титульным. Его можно поменять и после создания лота, но лучше позаботиться об этом заранее",False),
  ("Документы","Сюда прикрепляйте PDF с диагностикой и окрасами, а в мультилотах можно добавить дополнительные Автотеки. Не прикладывайте сканы ПТС и СТС с данными владельца: файлы увидят все, кто откроет лот",False),
  ("Создать лот","Последний клик, и лот в системе",False)],
 shot('step3','Шаг 3: контакты, фото и документы',pins=pin(1,96.35,15.1,.9)+pin(2,96.35,37.5,1.0)+pin(3,96.35,63.2,1.1)+pin(4,96.35,83.5,1.2)+pin(5,71.4,95.1,1.3),extra=t3)))
# 4. карточка лота
S.append(f'''<section class="sl" id="sD"><div class="in two big"><div class="lt"><div class="eyebrow rv">После создания</div>
{H([["Что","видно"],["в","карточке","лота."]],.1,.08)}
{leg([("Информация","Текущая цена, время до конца торгов, данные об автомобиле и документы",False,0),("Ставки","В момент торгов в карточке видно, кто торгуется, какая ставка и номер телефона партнёра. Рекомендуем звонить партнёрам и подтверждать ставки: это повышает лояльность к дилеру и к аукциону, ведь могут возникнуть дополнительные вопросы",False,1),("Изменить лот","Чтобы внести изменения, приостановите лот, поменяйте время, информацию и фотографии и запустите его заново",False,0)])}
</div>
<div class="shotw"><div class="tabsx rv" style="--d:.4s"><button class="on">Информация</button><button>Ставки</button></div>
<div class="shot sstack" style="--d:.45s"><img class="on" src="{img('infotop')}" alt="Карточка лота: информация"><img src="{img('bids')}" alt="Карточка лота: ставки"></div></div>
</div></section>''')
# 5. памятка
S.append(f'''<section class="sl" id="sF"><div class="in">
<div class="eyebrow rv">Памятка</div>
{H([["Что","делает"],[("лот","g"),("сильным.","g")]],.1)}
<div class="dgrid bgrid">
{bc('doc','Понятное описание','Состояние и диагностика своими словами: чем понятнее перекупу, тем дороже торги',.4)}
{bc('tag','Цена для перекупов','Старт в рынок и выше почти не даёт шансов. Заниженный старт: «Предварительный аукцион»',.52)}
{bc('cam','Первое фото','Оно станет титульным. Выберите лучшее заранее',.64)}
{bc('phone','Звоните партнёрам','Подтверждайте ставки во время торгов: это повышает лояльность',.76)}
{bc('lock','Без сканов ПТС и СТС','Файлы видят все, кто откроет лот',.88)}
<div class="bc"><div class="last" style="--d:1s"><div><h4>DROPDEALER</h4><p class="t2">Три шага, и торги идут.</p></div></div></div>
</div></div></section>''')
S.append(f'''<section class="sl" id="sN"><div class="in">
<div class="eyebrow rv">Если что-то пошло не так</div>
{H([["Нестандартные"],[("ситуации.","g")]],.1)}
<div class="sgrid">
{sit(1,"Ситуация 1","Лот не сыграл",["Снизьте цену на 10 000 ₽","Перезапустите не на 60 минут, а на 5–6 или 12 часов, а лучше на сутки"],"Автомобиль уже выкуплен, а мы зарабатываем, а не соревнуемся в скорости. Сутки дают максимум охвата, так делает большинство компаний",.4)}
{sit(2,"Ситуация 2","Перекуп отказался без причины",["Напишите в техподдержку","Отправьте недобросовестного участника в бан, чтобы он не мешал на будущих торгах"],"",.55,"y")}
{sit(3,"Ситуация 3","Отказ по объективной причине",["Не перезапускайте лот сразу. Например, нашли дополнительный окрас или оказалось, что авто дымит, а об этом не было написано","Позвоните участнику со второй или третьей ставкой, опишите ситуацию и предложите авто по его цене","Если и они отказались: добавьте в лот новую информацию и перезапустите"],"",.7)}
</div></div></section>''')
# 6. поддержка
S.append(f'''<section class="sl dark" id="sEnd"><div class="in cta">
<div class="top"><div class="eyebrow rv" id="ebE">Поддержка дилеров</div>
{H([["По","всем"],["техническим"],[("вопросам.","g")]],.1)}</div>
<div class="ctl2">
<div class="ct rv" style="--d:.4s"><div class="av">ИЧ</div><div><b>Иван Червоняк</b><div class="btns"><a class="btn" href="tel:+79111184107">+7 911 118-41-07</a><button class="btn gh" data-copy="+7 911 118-41-07">Скопировать</button></div></div></div>
<div class="ct rv" style="--d:.55s"><div class="av">НМ</div><div><b>Никита Мошкин</b><div class="btns"><a class="btn" href="tel:+79213434337">+7 921 343-43-37</a><button class="btn gh" data-copy="+7 921 343-43-37">Скопировать</button></div></div></div>
</div>
<div class="links rv" style="--d:.6s"><a href="https://panel.dropdealer.ru" target="_blank" rel="noopener"><small>ПАНЕЛЬ ДИЛЕРА</small>panel.dropdealer.ru</a><a href="https://app.dropdealer.ru" target="_blank" rel="noopener"><small>ПРИЛОЖЕНИЕ</small>app.dropdealer.ru</a><a href="https://dropdealer.ru" target="_blank" rel="noopener"><small>САЙТ</small>dropdealer.ru</a><span><small>ПОЧТА</small>dropdealerspb@gmail.com</span></div>
</div></section>''')

# версия без JS
_on=[l for l in css.split('\n') if '.on ' in l]
_nj='\n'.join(l.replace('.on ','.sl ') for l in _on)
NOJS='''html,body{height:auto!important;overflow:auto!important}body{display:block!important}
#app,#app.m,#app.land{--u:1cqw!important;position:static!important;width:100%!important;max-width:560px;margin:0 auto;height:auto!important;container-type:inline-size;overflow:visible!important}
#stage{position:static!important;perspective:none!important}
.sl{position:relative!important;inset:auto!important;visibility:visible!important;padding-top:calc(var(--u)*13)!important;padding-bottom:calc(var(--u)*12)!important}
.nav,.pgb,.hint,#fx,.topb{display:none!important}
.sstack img+img{display:none!important}
.njn{background:#111214;color:#fff;font:500 14px/1.4 Onest,system-ui,sans-serif;padding:12px 16px;text-align:center}
'''+_nj
html=f'''<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>DROPDEALER — как занести лот</title>
<style>{faces}</style>
<style>{css}</style><noscript><style>{NOJS}</style></noscript></head><body>
<noscript><div class="njn"><b>Версия без анимации.</b> Откройте обучение в браузере, чтобы листать слайды.</div></noscript>
<div id="app" class="m">
<div id="stage">{''.join(S)}</div>
<div id="fx"></div>
<header class="topb"><div class="logo"><s></s>DROPDEALER</div><div class="rt"><div class="sw"><button data-m="land">ПК</button><button data-m="m">ТЕЛЕФОН</button></div><div class="cnt"><b id="cn">01</b> / 0{len(S)}</div></div></header>
<nav class="nav">{''.join('<a></a>' for _ in S)}</nav>
<div class="pgb"><i id="pg"></i></div>
<div class="hint">ЛИСТАЙ</div>
</div>
<script>{js}</script></body></html>'''
# счётчики: итоговые значения в разметке
def _c(m):
    n=int(m.group(2));suf=m.group(3) or ''
    return m.group(1)+f'{n:,}'.replace(',',' ')+suf+'<'
html=re.sub(r'(data-to="(\d+)"(?: data-suf="([^"]*)")?[^>]*>)[^<]*<',_c,html)
open(D+'index.html','w').write(html);print('slides',len(S),'bytes',len(html))
