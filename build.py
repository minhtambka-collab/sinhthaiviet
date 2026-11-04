#!/usr/bin/env python3
"""Dựng site tĩnh Sinh Thái Việt -> thư mục dist/. Chạy: python3 build.py"""
import json, os, re, html, shutil, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist")
DOMAIN = "https://sinhthaiviet.vn"
PHONE = "0362771650"
PHONE_FMT = "0362 771 650"
ADDR = "Số nhà 5, Tổ 1, Phường Đồng Quang, TP. Thái Nguyên"
NAME = "Hợp tác xã Đầu tư Sinh Thái Việt"
TODAY = datetime.date.today().isoformat()
e = html.escape

DATA = json.load(open(os.path.join(ROOT, "data/products.json"), encoding="utf-8"))


def money(s):
    d = re.sub(r"\D", "", s or "")
    return f"{int(d):,}".replace(",", ".") + "đ" if d else "Liên hệ"


def slug(s):
    s = s.lower().replace("đ", "d")
    import unicodedata
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def cat_bt(n):
    l = n.lower()
    if l.startswith(("set", "combo")) or "khay khô" in l: return "Set & combo ăn vặt"
    if "cơm cháy" in l: return "Cơm cháy"
    if re.match(r"^(mực|khô bò|khô gà|khô heo)", l): return "Khô & mực ăn liền"
    if re.search(r"(sốt .*lọ|bơ vàng lọ|muối tép|tóp (nhỏ|to)|chà bông|rong biển)", l): return "Sốt, topping & gia vị lọ"
    if l.startswith("bánh tráng vip"): return "Bánh tráng hũ mix topping"
    return "Bánh tráng trộn, phơi sương & dẻo tôm"


def cat_nvl(n):
    l = n.lower()
    if "combo" in l: return "Combo nguyên liệu"
    if re.search(r"(sốt|sate|dầu tỏi)", l): return "Sốt & dầu"
    if re.search(r"(vỏ|bánh tráng|bt )", l): return "Bánh tráng & vỏ cuộn"
    if re.search(r"(khô|mực|bò|chà bông)", l): return "Khô, mực & chà bông"
    return "Topping, bơ & gia vị"


# ---------- dữ liệu sản phẩm ----------
NEWIMG = {20:103,64:102,65:107,67:104,12:109,13:111,69:105,70:108,71:108,72:110,48:112,53:113,46:114,47:116,14:115,
          44:131,45:132,15:118,56:118,19:130,37:124,41:119,2:120,10:120,8:121,11:121,4:122,7:125,66:125,36:123,43:123,
          55:126,38:127,3:127,40:128,54:128,42:129,34:129}
BT = []
for r in DATA["bt"]:
    _n = NEWIMG.get(int(r["stt"])) if r["name"] != "Khô mực cốt dừa 100g" else None
    BT.append(dict(name=r["name"], unit=r["unit"], price=money(r["retail"]), raw=re.sub(r"\D", "", r["retail"]),
                   img=(f"img/anh/b{_n}.jpg" if _n else (("img/sp/" + r["img"]) if r["img"] else None)), cat=cat_bt(r["name"])))
NVL = []
for r in DATA["nvl"]:
    NVL.append(dict(name=r["name"], unit=r["unit"], price=money(r["retail"]), raw=re.sub(r"\D", "", r["retail"]),
                    img=("img/sp/" + r["img"]) if r["img"] else None, cat=cat_nvl(r["name"])))

# ---------- layout ----------
NAV = [("", "Trang chủ"), ("cau-chuyen/", "Câu chuyện"), ("san-pham/", "Sản phẩm"),
       ("nguyen-lieu/", "Nguyên liệu sỉ"), ("dai-ly/", "Đại lý & sỉ"), ("kien-thuc/", "Kiến thức"), ("chung-nhan/", "Chứng nhận"), ("lien-he/", "Liên hệ")]


def page(path, title, desc, body, depth=0, og_img="img/anh/b102.jpg", jsonld=None, crumbs=None):
    rel = "../" * depth
    url = f"{DOMAIN}/{path}"
    nav = "".join(
        f'<a href="{rel}{h}" {"aria-current=page" if h == path else ""}>{t}</a>' for h, t in NAV)
    ld = [dict(
        {"@context": "https://schema.org", "@type": "Organization", "@id": f"{DOMAIN}/#org", "name": NAME,
         "alternateName": ["Sinh Thái Việt", "Viet Ecological Investment Cooperative"],
         "url": DOMAIN + "/", "logo": f"{DOMAIN}/img/logo-2.png", "telephone": "+84" + PHONE[1:],
         "address": {"@type": "PostalAddress", "streetAddress": "Số nhà 5, Tổ 1, Phường Đồng Quang",
                     "addressLocality": "Thái Nguyên", "addressCountry": "VN"},
         "foundingDate": "2024-04-17", "areaServed": "VN", "contactPoint": {"@type": "ContactPoint", "telephone": "+84362771650", "contactType": "sales", "availableLanguage": "vi"}})]
    ld.append({"@context": "https://schema.org", "@type": "WebSite", "name": "Sinh Thái Việt", "url": DOMAIN + "/",
               "inLanguage": "vi"})
    if crumbs:
        ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": f"{DOMAIN}/{p}"} for i, (n, p) in enumerate(crumbs)]})
    if jsonld: ld += jsonld
    ldjson = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f"""<!doctype html>
<html lang="vi"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="vi-VN" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="theme-color" content="#C9922E">
<link rel="icon" href="{rel}img/favicon.png" type="image/png">
<meta property="og:type" content="website"><meta property="og:locale" content="vi_VN">
<meta property="og:site_name" content="Sinh Thái Việt"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&family=Lora:wght@600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{rel}style.css">
{ldjson}
</head><body>
<a class="skip" href="#main">Bỏ qua điều hướng</a>
<header class="hd"><div class="wrap hd-in">
<a class="brand" href="{rel}" aria-label="Sinh Thái Việt - trang chủ"><img src="{rel}img/logo-2.png" width="46" height="46" alt="Logo Sinh Thái Việt"><span>SINH THÁI VIỆT<small>Hợp tác xã Đầu tư</small></span></a>
<button class="burger" aria-label="Mở menu" aria-expanded="false" onclick="var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)">☰</button>
<nav id="nav" aria-label="Menu chính">{nav}</nav>
</div></header>
<main id="main">{body}</main>
<footer class="ft"><div class="wrap ft-grid">
<div><img src="{rel}img/logo-2.png" width="64" height="64" alt="" loading="lazy"><h2>{NAME}</h2>
<p>Sản xuất, đóng gói, kinh doanh các sản phẩm từ bánh tráng. Hệ thống quản lý an toàn thực phẩm ISO 22000:2018.</p></div>
<div><h3>Liên hệ</h3><p>Trụ sở: {ADDR}</p><p>Cơ sở sản xuất: Tòa B, chung cư Sao Vàng, phường Hòa Bình, tỉnh Hòa Bình</p>
<p>Điện thoại / Zalo: <a href="tel:{PHONE}">{PHONE_FMT}</a></p></div>
<div><h3>Khám phá</h3>{"".join(f'<p><a href="{rel}{h}">{t}</a></p>' for h, t in NAV[1:])}</div>
</div><div class="wrap copy">© {datetime.date.today().year} {NAME}. Mã số hợp tác xã 4601617683.</div></footer>
<a class="zalo" href="https://zalo.me/{PHONE}" rel="noopener" target="_blank" aria-label="Chat Zalo">Zalo</a>
<script src="{rel}app.js" defer></script>
</body></html>"""


SITE = []


def write(path, content):
    SITE.append(path)
    p = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


def img(src, alt, rel, w=600, h=600, cls="", lazy=True):
    return f'<img src="{rel}{wp(src)}" alt="{e(alt)}" width="{w}" height="{h}" {"loading=lazy decoding=async" if lazy else "fetchpriority=high"} class="{cls}">'


def card(p, rel, kind):
    src = p["img"] or "img/logo-2.png"
    ph = "" if p["img"] else " ph"
    alt = f'{p["name"]} - {"nguyên liệu bánh tráng" if kind=="nvl" else "bánh tráng"} Sinh Thái Việt'
    return (f'<article class="card{ph}" data-cat="{e(p["cat"])}" data-name="{e(p["name"].lower())}">'
            f'<a href="{rel}{p["url"]}" tabindex="-1" aria-hidden="true">{img(src, alt, rel, 300, 300)}</a><div class="cb"><h3><a href="{rel}{p["url"]}">{e(p["name"])}</a></h3>'
            f'<p class="un">Đơn vị: {e(p["unit"])}</p><p class="pr">{p["price"]}<small> giá bán lẻ tham khảo</small></p>'
            f'<a class="btn sm" href="https://zalo.me/{PHONE}" target="_blank" rel="noopener">Hỏi mua qua Zalo</a></div></article>')


def catalog(items, rel, kind):
    cats = []
    for p in items:
        if p["cat"] not in cats: cats.append(p["cat"])
    chips = '<button class="chip on" data-f="">Tất cả</button>' + "".join(
        f'<button class="chip" data-f="{e(c)}">{e(c)} <span>{sum(1 for p in items if p["cat"]==c)}</span></button>' for c in cats)
    grid = "".join(card(p, rel, kind) for p in items)
    return (f'<h2 class="sr">Danh sách sản phẩm</h2><div class="tools"><input id="q" type="search" placeholder="Tìm sản phẩm..." aria-label="Tìm sản phẩm"><div class="chips">{chips}</div></div>'
            f'<div class="grid" id="grid">{grid}</div><p id="empty" class="muted" hidden>Không tìm thấy sản phẩm phù hợp.</p>')


def itemlist(items, name, path):
    return {"@context": "https://schema.org", "@type": "ItemList", "name": name, "numberOfItems": len(items),
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {
                "@type": "Product", "name": p["name"], "brand": {"@type": "Brand", "name": "Sinh Thái Việt"},
                "image": f"{DOMAIN}/{p['img']}" if p["img"] else f"{DOMAIN}/img/logo-2.png",
                "offers": {"@type": "Offer", "priceCurrency": "VND", "price": p["raw"] or "0",
                           "availability": "https://schema.org/InStock", "url": f"{DOMAIN}/{path}"}}}
                for i, p in enumerate(items[:50])]}


# ---------- TRANG CHỦ ----------
def home():
    feats = [("img/anh/b102.jpg", "Sate bò ngũ vị"), ("img/anh/b107.jpg", "Gà sốt me cay"),
             ("img/anh/b105.jpg", "Phô mai chà bông"), ("img/anh/b108.jpg", "Lá bò lục vị")]
    fcards = "".join(f'<figure>{img(s, "Bánh tráng trộn " + t + " Sinh Thái Việt", "", 500, 500)}<figcaption>{t}</figcaption></figure>' for s, t in feats)
    body = f"""
<section class="hero"><div class="wrap hero-in"><div>
<p class="eyebrow">Hợp tác xã Đầu tư Sinh Thái Việt · Thái Nguyên</p>
<h1>Bánh tráng trộn &amp; đặc sản ăn vặt đạt chuẩn ISO 22000</h1>
<p class="lead">Từ tấm bánh tráng đến hũ, túi, set ăn vặt hoàn chỉnh. Sản xuất và đóng gói theo hệ thống an toàn thực phẩm ISO 22000:2018, phục vụ khách lẻ, đại lý và quán ăn vặt trên toàn quốc.</p>
<p class="cta"><a class="btn" href="san-pham/">Xem sản phẩm</a><a class="btn ghost" href="dai-ly/">Làm đại lý / mua sỉ</a></p>
<ul class="badges"><li>ISO 22000:2018</li><li>{len(BT)}+ sản phẩm</li><li>{len(NVL)}+ nguyên liệu sỉ</li></ul>
</div>{img("img/anh/b102.jpg", "Bánh tráng trộn sate bò ngũ vị Sinh Thái Việt", "", 700, 700, "hero-img", lazy=False)}</div></section>

<section class="sec"><div class="wrap"><h2>Vì sao chọn Sinh Thái Việt?</h2>
<div class="cols3">
<div class="box"><h3>Quản lý an toàn thực phẩm</h3><p>Chứng nhận ISO 22000:2018 số W2386F do WCERT cấp, hiệu lực 11/7/2025 – 10/7/2028, phạm vi sản xuất, đóng gói, kinh doanh sản phẩm từ bánh tráng.</p></div>
<div class="box"><h3>Danh mục đầy đủ</h3><p>Bánh tráng trộn, phơi sương, dẻo tôm, cơm cháy, khô bò – gà – mực, sốt và topping. Bán lẻ, bán sỉ và cung cấp nguyên liệu.</p></div>
<div class="box"><h3>Chính sách đại lý rõ ràng</h3><p>Ba mức giá: đại lý chiến lược, đại lý và giá sỉ từ 30 gói, kèm giá bán lẻ khuyến nghị để dễ lên kế hoạch kinh doanh.</p></div>
</div></div></section>

<section class="sec alt"><div class="wrap"><h2>Sản phẩm được yêu thích</h2><p class="muted">Một số vị bánh tráng trộn đóng túi zip, hút chân không, đủ topping.</p>
<div class="feat">{fcards}</div><p class="center"><a class="btn" href="san-pham/">Xem toàn bộ {len(BT)} sản phẩm</a></p></div></section>

<section class="sec"><div class="wrap split">
{img("img/anh/b120.jpg", "Set bánh tráng trộn topping nhiều màu Sinh Thái Việt", "", 700, 700)}
<div><h2>Câu chuyện thương hiệu</h2>
<p>Biểu tượng Sinh Thái Việt là bàn tay nâng đỡ cánh đồng và mầm cây, gắn với đồng tiền và nhịp sống hiện đại. Đó cũng là cách chúng tôi làm nghề: tôn trọng nguyên liệu, nâng niu người làm ra, đầu tư dài hạn vào chất lượng.</p>
<p><a class="btn ghost" href="cau-chuyen/">Đọc câu chuyện</a></p></div></div></section>

<section class="sec alt"><div class="wrap"><h2>Cung cấp nguyên liệu cho quán ăn vặt</h2>
<p>Vỏ bánh tráng, sốt me – tắc – bò – ớt, khô bò, khô gà, mực cán, hành phi, tóp mỡ, bơ... đóng can, thùng hoặc theo kg. Có sẵn combo trộn, cuộn, nướng để mở quán nhanh.</p>
<p><a class="btn" href="nguyen-lieu/">Xem bảng nguyên liệu</a></p></div></section>
{home_extra()}
"""
    write("", page("", "Bánh tráng trộn Thái Nguyên: bán sỉ & lẻ, ISO 22000 | Sinh Thái Việt",
                   "Sinh Thái Việt: sản xuất, đóng gói, bán sỉ và lẻ bánh tráng trộn, khô bò, khô gà, mực, sốt và nguyên liệu cho quán ăn vặt. Đạt ISO 22000:2018. Hotline 0362 771 650.",
                   body, 0))


# ---------- CÂU CHUYỆN ----------
def story():
    def step(n, t, p, im, alt, href):
        return (f'<article class="step"><span class="num">{n}</span><img src="../img/anh/{im}.webp" alt="{e(alt)}" width="520" height="520" loading="lazy" decoding="async">'
                f'<div><h3>{t}</h3><p>{p}</p><a class="btn sm" href="{href}">Xem nhóm sản phẩm</a></div></article>')
    steps = "".join([
        step(1, "Mở túi là ăn: bánh tráng trộn sẵn", "Dành cho người bận rộn. Sợi bánh tráng đã tẩm vị, trộn sẵn khô bò, khô gà, tóp mỡ, hành phi, đậu phộng. Chọn vị sate bò ngũ vị, gà sốt me cay, phô mai gà cay, lá bò lục vị, hải sản...", "b102", "Bánh tráng trộn sate bò ngũ vị Sinh Thái Việt", "../san-pham/banh-trang-tron/"),
        step(2, "Tự tay trộn: set vỏ, sốt và topping", "Dành cho người thích chủ động. Mỗi set có vỏ bánh tráng, túi sốt bơ trứng gà, sốt me hoặc sốt tắc và các hũ topping riêng. Bạn trộn đến đúng vị mình thích.", "b70", "Combo bánh tráng me bơ siêu toppings", "../san-pham/set-an-vat/"),
        step(3, "Nướng và cuộn: món ăn vặt đường phố tại nhà", "Bánh tráng nướng vỏ vàng giòn kèm khay topping, hoặc bánh tráng cuộn bơ đầy đủ nhân. Đóng hút chân không, sẵn sàng cho buổi tụ họp.", "b92", "Bánh tráng nướng set topping khay", "../san-pham/set-an-vat/"),
        step(4, "Sốt &amp; topping: linh hồn của món ăn", "Sốt me, sốt tắc, ớt rim, bơ trứng gà, tóp mỡ rim mắm hành, muối tép hành phi. Dùng kèm bánh tráng hoặc cho quán ăn vặt.", "b81", "Sốt me Sinh Thái Việt", "../san-pham/sot-topping-gia-vi/")])
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../">Trang chủ</a> / Câu chuyện</nav>
<h1>Câu chuyện Sinh Thái Việt</h1><p class="lead">Từ một hợp tác xã ở Thái Nguyên đến những túi bánh tráng đạt chuẩn ISO 22000:2018, đi cùng bạn từ bữa ăn vặt nhanh đến quán ăn vặt của riêng mình.</p></div></section>

<section class="sec"><div class="wrap split">
<div><h2>Khởi nguồn: một tấm bánh tráng, rất nhiều cách thưởng thức</h2>
<p>Hợp tác xã Đầu tư Sinh Thái Việt được đăng ký thành lập ngày 17/4/2024 tại thành phố Thái Nguyên. Chúng tôi chọn bánh tráng, món ăn vặt quen thuộc của mọi lứa tuổi, làm điểm khởi đầu, với mong muốn đưa món ăn đường phố vào một chiếc túi sạch, đẹp, an toàn và dễ mang đi.</p>
<p>Từ đó, mỗi sản phẩm của Sinh Thái Việt đều đi theo một câu hỏi: hôm nay bạn muốn ăn thế nào?</p></div>
<img src="../img/anh/b18.webp" alt="Bánh tráng phơi sương và sốt đóng gói Sinh Thái Việt" width="700" height="700" loading="lazy"></div></section>

<section class="sec alt"><div class="wrap"><h2>Hôm nay bạn muốn ăn thế nào?</h2><p class="muted">Chọn một hành trình, chúng tôi dẫn bạn đến đúng sản phẩm.</p><div class="steps">{steps}</div></div></section>

<section class="sec"><div class="wrap split">
<img src="../img/anh/b19.webp" alt="Gian hàng giới thiệu sản phẩm Hợp tác xã Đầu tư Sinh Thái Việt" width="700" height="500" loading="lazy">
<div><h2>Gặp gỡ khách hàng, lắng nghe để làm tốt hơn</h2>
<p>Chúng tôi mang sản phẩm đến các sự kiện và hội chợ để khách trải nghiệm trực tiếp, nhận góp ý về hương vị, quy cách đóng gói và giá bán. Đại lý và quán ăn vặt cũng là những người đồng hành lâu dài.</p>
<p><a class="btn ghost" href="../dai-ly/">Trở thành đại lý</a></p></div></div></section>

<section class="sec alt"><div class="wrap narrow">
<h2>Cam kết an toàn: chuẩn ISO 22000:2018</h2>
<p>Tháng 7/2025, Sinh Thái Việt được Công ty Cổ phần Chứng nhận WCERT cấp Giấy chứng nhận Hệ thống Quản lý An toàn Thực phẩm theo tiêu chuẩn ISO 22000:2018 (số W2386F), cho hoạt động sản xuất, đóng gói, kinh doanh các sản phẩm từ bánh tráng. Giấy chứng nhận có hiệu lực đến ngày 10/7/2028 và được đánh giá giám sát định kỳ hằng năm.</p>
<p><a class="btn ghost" href="../chung-nhan/">Xem giấy chứng nhận</a></p>
<h2>Ý nghĩa biểu tượng</h2>
<div class="logo-story">{img("img/logo-2.png", "Logo Hợp tác xã Đầu tư Sinh Thái Việt", "../", 220, 220)}
<p>Vòng tròn âm dương thể hiện sự cân bằng giữa con người, đồng tiền đầu tư và thiên nhiên. Bàn tay nâng đỡ cánh đồng và mầm cây là lời cam kết đồng hành cùng nhà vườn, người làm nghề và đại lý. Sắc vàng đất là màu của lúa chín, của bánh tráng giòn và của sự thịnh vượng.</p></div></div></section>

<section class="sec"><div class="wrap center"><h2>Sẵn sàng thử hoặc cùng kinh doanh?</h2>
<p class="cta" style="justify-content:center"><a class="btn" href="../san-pham/">Xem sản phẩm</a><a class="btn ghost" href="../nguyen-lieu/">Nguyên liệu mở quán</a><a class="btn ghost" href="https://zalo.me/{PHONE}" target="_blank" rel="noopener">Zalo {PHONE_FMT}</a></p></div></section>
"""
    write("cau-chuyen", page("cau-chuyen/", "Câu chuyện thương hiệu Sinh Thái Việt | Hợp tác xã Đầu tư Thái Nguyên",
                             "Câu chuyện Sinh Thái Việt: từ hợp tác xã Thái Nguyên đến bánh tráng trộn ISO 22000:2018. Chọn cách ăn: trộn sẵn, tự trộn, nướng cuộn, sốt và topping.",
                             body, 1, "img/anh/b102.jpg", crumbs=[("Trang chủ", ""), ("Câu chuyện", "cau-chuyen/")]))


def products():
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../">Trang chủ</a> / Sản phẩm</nav>
<h1>Sản phẩm bánh tráng &amp; đặc sản ăn vặt</h1>
<p class="lead">{len(BT)} sản phẩm: bánh tráng trộn, phơi sương, dẻo tôm, cơm cháy, khô, sốt và set ăn vặt. Giá hiển thị là giá bán lẻ khuyến nghị.</p></div></section>
<section class="sec"><div class="wrap">{catalog(BT, "../", "bt")}</div></section>
<section class="sec"><div class="wrap"><h2>Chọn theo cách bạn muốn ăn</h2><div class="cols3 linkbox">
<a class="box" href="banh-trang-tron/"><img src="../img/anh/b102.webp" alt="Bánh tráng trộn sate bò ngũ vị" width="300" height="300" loading="lazy"><h3>Ăn liền, mở túi là có</h3><p>Bánh tráng trộn sẵn topping đóng túi đứng</p></a>
<a class="box" href="set-an-vat/"><img src="../img/anh/b70.webp" alt="Combo bánh tráng me bơ siêu toppings" width="300" height="300" loading="lazy"><h3>Tự trộn tại nhà</h3><p>Set vỏ, sốt và topping rời để tự tay trộn</p></a>
<a class="box" href="sot-topping-gia-vi/"><img src="../img/anh/b81.webp" alt="Sốt me Sinh Thái Việt" width="300" height="300" loading="lazy"><h3>Sốt &amp; topping</h3><p>Sốt me, sốt tắc, ớt rim, bơ trứng gà, tóp mỡ</p></a></div></div></section>
<section class="sec alt"><div class="wrap"><h2>Thư viện ảnh sản phẩm</h2><div class="gallery">
{"".join(img(f"img/anh/b{i}.jpg", "Bánh tráng trộn Sinh Thái Việt - ảnh sản phẩm " + str(i), "../", 500, 500) for i in range(102,133))}
</div></div></section>"""
    write("san-pham", page("san-pham/", f"{len(BT)} sản phẩm bánh tráng trộn, khô bò, mực, sốt | Sinh Thái Việt",
                           "Danh mục bánh tráng trộn, phơi sương, dẻo tôm, cơm cháy, khô bò, khô gà, mực rim, sốt me tắc, set ăn vặt. Giá bán lẻ khuyến nghị. Đặt hàng qua Zalo 0362 771 650.",
                           body, 1, "img/anh/a41.jpg", jsonld=[itemlist(BT, "Sản phẩm Sinh Thái Việt", "san-pham/")],
                           crumbs=[("Trang chủ", ""), ("Sản phẩm", "san-pham/")]))


def materials():
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../">Trang chủ</a> / Nguyên liệu sỉ</nav>
<h1>Nguyên liệu bánh tráng trộn bán sỉ</h1>
<p class="lead">{len(NVL)} mặt hàng cho quán ăn vặt, cửa hàng và đại lý: vỏ bánh tráng, khô bò, khô gà, mực, sốt, bơ, topping, combo mở quán. Giá hiển thị là giá bán lẻ khuyến nghị; giá sỉ vui lòng liên hệ.</p></div></section>
<section class="sec"><div class="wrap">{catalog(NVL, "../", "nvl")}</div></section>"""
    write("nguyen-lieu", page("nguyen-lieu/", "Nguyên liệu bánh tráng trộn giá sỉ: vỏ, sốt, khô bò, mực | Sinh Thái Việt",
                              "Cung cấp nguyên liệu bánh tráng trộn giá sỉ cho quán ăn vặt: vỏ bánh tráng, sốt me tắc bò ớt, khô bò, khô gà, mực cán, hành phi, tóp mỡ, combo mở quán.",
                              body, 1, "img/anh/a40.jpg", jsonld=[itemlist(NVL, "Nguyên liệu Sinh Thái Việt", "nguyen-lieu/")],
                              crumbs=[("Trang chủ", ""), ("Nguyên liệu sỉ", "nguyen-lieu/")]))


# ---------- ĐẠI LÝ ----------
FAQ = [("Mua sỉ tối thiểu bao nhiêu?", "Giá sỉ áp dụng khi lấy từ 30 gói. Giá đại lý áp dụng cho doanh số khoảng 3 triệu đồng mỗi tháng, đại lý chiến lược từ 10 triệu đồng mỗi tháng."),
       ("Giá đại lý có công khai không?", "Bảng giá đại lý và sỉ được gửi trực tiếp sau khi bạn liên hệ qua Zalo hoặc điện thoại, để cập nhật đúng thời điểm."),
       ("Sản phẩm có đạt chuẩn an toàn thực phẩm không?", "Có. Hợp tác xã được cấp Giấy chứng nhận ISO 22000:2018 số W2386F, hiệu lực đến 10/7/2028."),
       ("Có bán nguyên liệu để mở quán bánh tráng trộn không?", "Có. Chúng tôi cung cấp vỏ, sốt, khô, topping và các combo trộn, cuộn, nướng, combo 3 trong 1.")]


def dealer():
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQ)
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../">Trang chủ</a> / Đại lý &amp; sỉ</nav>
<h1>Làm đại lý &amp; mua sỉ bánh tráng Sinh Thái Việt</h1>
<p class="lead">Ba mức chính sách giá rõ ràng, sản phẩm có chứng nhận ISO 22000:2018, hỗ trợ tư vấn lên kế hoạch kinh doanh.</p></div></section>
<section class="sec"><div class="wrap"><div class="cols3">
<div class="box hl"><h3>Đại lý chiến lược</h3><p class="big">Doanh số từ 10 triệu/tháng</p><p>Mức giá tốt nhất, ưu tiên hàng mới và hỗ trợ hình ảnh bán hàng.</p></div>
<div class="box"><h3>Đại lý</h3><p class="big">Doanh số từ 3 triệu/tháng</p><p>Giá đại lý ổn định, phù hợp cửa hàng tạp hóa, quán ăn vặt, bán online.</p></div>
<div class="box"><h3>Giá sỉ</h3><p class="big">Lấy từ 30 gói</p><p>Dành cho khách mua số lượng, chưa cam kết doanh số tháng.</p></div></div>
<p class="center"><a class="btn" href="https://zalo.me/{PHONE}" target="_blank" rel="noopener">Nhận bảng giá qua Zalo {PHONE_FMT}</a></p></div></section>
<section class="sec alt"><div class="wrap narrow"><h2>Câu hỏi thường gặp</h2>{faq}</div></section>"""
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    write("dai-ly", page("dai-ly/", "Làm đại lý bánh tráng, mua sỉ từ 30 gói | Sinh Thái Việt",
                         "Chính sách đại lý và giá sỉ bánh tráng trộn Sinh Thái Việt: đại lý chiến lược, đại lý, sỉ từ 30 gói. Sản phẩm ISO 22000:2018. Liên hệ Zalo 0362 771 650.",
                         body, 1, "img/anh/b120.jpg", jsonld=[faqld], crumbs=[("Trang chủ", ""), ("Đại lý & sỉ", "dai-ly/")]))


# ---------- CHỨNG NHẬN ----------
def certs():
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../">Trang chủ</a> / Chứng nhận</nav>
<h1>Chứng nhận &amp; pháp lý</h1><p class="lead">Minh bạch thông tin doanh nghiệp và hệ thống an toàn thực phẩm.</p></div></section>
<section class="sec"><div class="wrap split top">
<a href="../img/cert/iso22000-giay-chung-nhan.jpg" target="_blank" rel="noopener">{img("img/cert/iso22000-giay-chung-nhan.jpg", "Giấy chứng nhận ISO 22000:2018 số W2386F của Hợp tác xã Đầu tư Sinh Thái Việt", "../", 640, 905)}</a>
<div><h2>ISO 22000:2018</h2><table class="tb">
<tr><th>Số chứng nhận</th><td>W2386F</td></tr><tr><th>Tổ chức cấp</th><td>Công ty Cổ phần Chứng nhận WCERT</td></tr>
<tr><th>Hiệu lực</th><td>11/7/2025 – 10/7/2028</td></tr>
<tr><th>Phạm vi</th><td>Sản xuất, đóng gói, kinh doanh các sản phẩm từ bánh tráng</td></tr>
<tr><th>Địa chỉ sản xuất</th><td>Tòa B, chung cư Sao Vàng, phường Hòa Bình, tỉnh Hòa Bình</td></tr></table>
<h2>Đăng ký hợp tác xã</h2><table class="tb">
<tr><th>Tên</th><td>Hợp tác xã Đầu tư Sinh Thái Việt</td></tr><tr><th>Mã số HTX</th><td>4601617683</td></tr>
<tr><th>Đăng ký lần đầu</th><td>17/4/2024 (thay đổi lần 1: 15/4/2025)</td></tr>
<tr><th>Trụ sở</th><td>{ADDR}</td></tr><tr><th>Vốn điều lệ</th><td>1.000.000.000 đồng</td></tr>
<tr><th>Giám đốc</th><td>Nguyễn Thị Minh Phượng</td></tr><tr><th>Chủ tịch HĐQT</th><td>Ngô Việt Cường</td></tr></table>
<p><a class="btn ghost" href="../img/cert/dang-ky-hop-tac-xa.jpg" target="_blank" rel="noopener">Xem giấy đăng ký HTX</a></p></div></div></section>"""
    write("chung-nhan", page("chung-nhan/", "Chứng nhận ISO 22000:2018 & giấy đăng ký HTX | Sinh Thái Việt",
                             "Giấy chứng nhận ISO 22000:2018 số W2386F (WCERT) và đăng ký hợp tác xã mã số 4601617683 của Hợp tác xã Đầu tư Sinh Thái Việt, Thái Nguyên.",
                             body, 1, "img/cert/iso22000-giay-chung-nhan.jpg", crumbs=[("Trang chủ", ""), ("Chứng nhận", "chung-nhan/")]))


# ---------- LIÊN HỆ ----------
def contact():
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../">Trang chủ</a> / Liên hệ</nav>
<h1>Liên hệ Sinh Thái Việt</h1><p class="lead">Đặt hàng, nhận bảng giá đại lý, tư vấn mở quán.</p></div></section>
<section class="sec"><div class="wrap cols3">
<div class="box"><h3>Điện thoại / Zalo</h3><p class="big"><a href="tel:{PHONE}">{PHONE_FMT}</a></p><p><a class="btn" href="https://zalo.me/{PHONE}" target="_blank" rel="noopener">Chat Zalo</a></p></div>
<div class="box"><h3>Trụ sở</h3><p>{ADDR}</p></div>
<div class="box"><h3>Cơ sở sản xuất</h3><p>Tòa B, chung cư Sao Vàng, phường Hòa Bình, tỉnh Hòa Bình</p></div></div></section>"""
    write("lien-he", page("lien-he/", "Liên hệ đặt hàng, đại lý | Sinh Thái Việt Thái Nguyên",
                          "Liên hệ Hợp tác xã Đầu tư Sinh Thái Việt: hotline/Zalo 0362 771 650, trụ sở Thái Nguyên, cơ sở sản xuất Hòa Bình.",
                          body, 1, crumbs=[("Trang chủ", ""), ("Liên hệ", "lien-he/")]))


CSS = """:root{--gold:#C9922E;--gold-d:#9A6B14;--cream:#FFF6DC;--cream2:#FFE7A8;--ink:#3A2A0E;--muted:#7a6a4c;--bg:#FFFCF3}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font:16px/1.65 'Be Vietnam Pro',system-ui,sans-serif;color:var(--ink);background:var(--bg)}
img{max-width:100%;height:auto;display:block}a{color:var(--gold-d)}h1,h2,h3{font-family:Lora,Georgia,serif;line-height:1.25;margin:0 0 .5em}
h1{font-size:clamp(1.9rem,4.5vw,3rem)}h2{font-size:clamp(1.4rem,3vw,2rem)}h3{font-size:1.1rem}
.wrap{max-width:1160px;margin:0 auto;padding:0 20px}.narrow{max-width:800px}.center{text-align:center}.muted{color:var(--muted)}
.skip{position:absolute;left:-999px}.skip:focus{left:8px;top:8px;background:#fff;padding:8px;z-index:99}
.hd{position:sticky;top:0;z-index:50;background:rgba(255,252,243,.95);backdrop-filter:blur(8px);border-bottom:1px solid var(--cream2)}
.hd-in{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:66px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font-weight:700;letter-spacing:.04em}.brand small{display:block;font-weight:500;font-size:.7rem;letter-spacing:.02em;color:var(--muted)}
nav a{margin-left:18px;text-decoration:none;color:var(--ink);font-weight:500;font-size:.95rem}nav a:hover,nav a[aria-current]{color:var(--gold-d);border-bottom:2px solid var(--gold)}
.burger{display:none;background:none;border:0;font-size:1.6rem;cursor:pointer;color:var(--ink)}
.btn{display:inline-block;background:var(--gold);color:#fff;padding:12px 24px;border-radius:999px;text-decoration:none;font-weight:600;border:2px solid var(--gold);transition:.2s}
.btn:hover{background:var(--gold-d);border-color:var(--gold-d)}.btn.ghost{background:transparent;color:var(--gold-d)}.btn.ghost:hover{background:var(--cream2)}.btn.sm{padding:7px 14px;font-size:.85rem}
.hero{background:linear-gradient(135deg,var(--cream),var(--cream2));padding:56px 0}.hero-in{display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.hero-img{border-radius:24px;box-shadow:0 20px 50px rgba(154,107,20,.25);aspect-ratio:1;object-fit:cover}
.eyebrow{color:var(--gold-d);font-weight:600;text-transform:uppercase;letter-spacing:.08em;font-size:.8rem}.lead{font-size:1.1rem;color:#5a4824}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin:24px 0}.badges{display:flex;gap:10px;flex-wrap:wrap;list-style:none;padding:0}.badges li{background:#fff;border:1px solid var(--gold);color:var(--gold-d);padding:4px 14px;border-radius:999px;font-size:.85rem;font-weight:600}
.sec{padding:56px 0}.alt{background:var(--cream)}.pagehead{background:linear-gradient(135deg,var(--cream),var(--cream2));padding:36px 0}.bc{font-size:.85rem;color:var(--muted);margin-bottom:10px}
.cols3{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}.box{background:#fff;border:1px solid var(--cream2);border-radius:16px;padding:24px}.box.hl{border:2px solid var(--gold);background:var(--cream)}.big{font-weight:700;font-size:1.2rem;color:var(--gold-d)}
.feat{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:24px 0}.feat figure{margin:0}.feat img{border-radius:16px;aspect-ratio:1;object-fit:cover}.feat figcaption{text-align:center;font-weight:600;margin-top:8px}
.split{display:grid;grid-template-columns:1fr 1fr;gap:40px;align-items:center}.split.top{align-items:start}.split>img{aspect-ratio:1;object-fit:cover;max-height:520px;width:100%}.split>img,.split>a>img{border-radius:20px;box-shadow:0 12px 30px rgba(0,0,0,.12)}
.ticks{padding-left:0;list-style:none}.ticks li{padding-left:28px;position:relative;margin:8px 0}.ticks li:before{content:"✓";position:absolute;left:0;color:var(--gold);font-weight:700}
.logo-story{display:flex;gap:20px;align-items:center}.logo-story img{flex:none;width:140px}
.tools{margin-bottom:24px}#q{width:100%;padding:12px 18px;border:2px solid var(--cream2);border-radius:999px;font:inherit;margin-bottom:12px;background:#fff}#q:focus{outline:none;border-color:var(--gold)}
.chips{display:flex;gap:8px;flex-wrap:wrap}.chip{border:1px solid var(--gold);background:#fff;color:var(--gold-d);border-radius:999px;padding:6px 14px;cursor:pointer;font:inherit;font-size:.88rem}.chip span{opacity:.6}.chip.on{background:var(--gold);color:#fff}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:18px}.card{background:#fff;border:1px solid var(--cream2);border-radius:16px;overflow:hidden;display:flex;flex-direction:column}
.card img{aspect-ratio:1;object-fit:cover;width:100%;background:var(--cream)}.card.ph img{object-fit:contain;padding:28px;opacity:.5}.cb{padding:14px;display:flex;flex-direction:column;flex:1}.cb h3{font-size:.95rem;font-family:'Be Vietnam Pro',sans-serif;font-weight:600}
.un{margin:0;font-size:.8rem;color:var(--muted)}.pr{margin:6px 0 12px;font-weight:700;color:var(--gold-d);font-size:1.15rem}.pr small{display:block;font-size:.7rem;font-weight:400;color:var(--muted)}.cb .btn{margin-top:auto;text-align:center}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:14px}.gallery img{border-radius:14px;aspect-ratio:1;object-fit:cover;width:100%}
.tb{width:100%;border-collapse:collapse;margin-bottom:24px}.tb th,.tb td{padding:9px 10px;border-bottom:1px solid var(--cream2);text-align:left;vertical-align:top;font-size:.95rem}.tb th{width:36%;color:var(--gold-d)}
details{background:#fff;border:1px solid var(--cream2);border-radius:12px;padding:14px 18px;margin:10px 0}summary{cursor:pointer;font-weight:600}
.ft{background:var(--ink);color:#f0e4c4;padding:48px 0 0}.ft a{color:var(--cream2)}.ft h2,.ft h3{color:#fff;font-size:1.05rem}.ft-grid{display:grid;grid-template-columns:1.3fr 1fr 1fr;gap:32px}.ft p{margin:.3em 0;font-size:.92rem}
.copy{border-top:1px solid #5a4824;margin-top:32px;padding:16px 20px;font-size:.82rem;color:#bfae85}
.zalo{position:fixed;right:16px;bottom:16px;background:#0068ff;color:#fff;width:56px;height:56px;border-radius:50%;display:grid;place-items:center;font-weight:700;text-decoration:none;box-shadow:0 6px 18px rgba(0,0,0,.3);z-index:60}
@media(max-width:860px){.hero-in,.split,.cols3,.ft-grid{grid-template-columns:1fr}.feat{grid-template-columns:repeat(2,1fr)}.burger{display:block}
nav{display:none;position:absolute;left:0;right:0;top:66px;background:var(--bg);padding:12px 20px;border-bottom:1px solid var(--cream2);flex-direction:column}nav.open{display:flex}nav a{margin:0;padding:10px 0}.logo-story{flex-direction:column;align-items:flex-start}}
"""

JS = """(function(){var g=document.getElementById('grid');if(!g)return;var q=document.getElementById('q'),cs=g.parentNode.querySelectorAll('.chip'),f='',
cards=g.querySelectorAll('.card'),em=document.getElementById('empty');function run(){var t=q.value.trim().toLowerCase(),n=0;
cards.forEach(function(c){var ok=(!f||c.dataset.cat===f)&&(!t||c.dataset.name.indexOf(t)>-1);c.hidden=!ok;if(ok)n++});em.hidden=n>0}
q.addEventListener('input',run);cs.forEach(function(b){b.addEventListener('click',function(){cs.forEach(function(x){x.classList.remove('on')});b.classList.add('on');f=b.dataset.f;run()})})})();"""


# =================== SEO MỞ RỘNG ===================
SLUG_BT = {"Bánh tráng trộn, phơi sương & dẻo tôm": "banh-trang-tron", "Set & combo ăn vặt": "set-an-vat",
           "Cơm cháy": "com-chay", "Khô & mực ăn liền": "kho-muc-an-lien",
           "Sốt, topping & gia vị lọ": "sot-topping-gia-vi", "Bánh tráng hũ mix topping": "banh-trang-hu-mix"}
SLUG_NVL = {"Combo nguyên liệu": "combo-mo-quan", "Sốt & dầu": "sot-dau", "Bánh tráng & vỏ cuộn": "vo-banh-trang",
            "Khô, mực & chà bông": "kho-muc-cha-bong", "Topping, bơ & gia vị": "topping-bo-gia-vi"}

CAT_INFO = {
    "Bánh tráng trộn, phơi sương & dẻo tôm": dict(
        h1="Bánh tráng trộn, phơi sương, dẻo tôm", title="Bánh tráng trộn, phơi sương, dẻo tôm giá sỉ & lẻ | Sinh Thái Việt",
        desc="Bánh tráng trộn, bánh tráng phơi sương, dẻo tôm đóng túi zip, hút chân không, đủ topping và sốt. Đạt ISO 22000:2018. Bán lẻ, bán sỉ, làm đại lý.",
        intro=["Bánh tráng trộn là món ăn vặt quen thuộc: sợi bánh tráng được tẩm vị, trộn cùng khô bò, khô gà, tóp mỡ, hành phi, đậu phộng và các loại sốt. Sinh Thái Việt đóng gói sẵn từng suất để khách mang đi, mở túi là ăn.",
               "Nhóm này gồm bánh tráng tẩm vị, bánh tráng phơi sương, bánh tráng dẻo tôm và các bộ trộn kèm sốt. Mỗi sản phẩm được sản xuất và đóng gói theo hệ thống an toàn thực phẩm ISO 22000:2018."],
        faq=[("Bánh tráng phơi sương khác bánh tráng dẻo tôm thế nào?", "Bánh tráng phơi sương có độ mềm dẻo đặc trưng, thường ăn kèm sốt và topping; bánh tráng dẻo tôm có vị tôm đặc trưng. Bạn có thể xem từng sản phẩm bên dưới để chọn."),
             ("Mua sỉ bánh tráng trộn tối thiểu bao nhiêu?", "Giá sỉ áp dụng khi lấy từ 30 gói. Liên hệ Zalo 0362 771 650 để nhận bảng giá.")]),
    "Set & combo ăn vặt": dict(
        h1="Set & combo ăn vặt bánh tráng", title="Set ăn vặt bánh tráng: set cuộn, set nướng, set me bơ | Sinh Thái Việt",
        desc="Set ăn vặt bánh tráng đóng sẵn: set cuộn, set nướng khay, set me bơ, set tắc bơ, khay khô tứ vị. Tiện làm quà, bán lẻ, bán đại lý.",
        intro=["Set ăn vặt là các bộ sản phẩm được phối sẵn bánh tráng, sốt và topping, phù hợp làm quà, ăn nhóm hoặc bày bán tại cửa hàng.",
               "Sinh Thái Việt có set cuộn, set nướng khay, set me bơ, set tắc bơ, set dẻo tôm và khay khô tứ vị. Tất cả đóng gói theo chuẩn ISO 22000:2018."],
        faq=[("Set ăn vặt có làm quà được không?", "Có. Các set được phối sẵn, đóng gói gọn nên phù hợp biếu tặng hoặc bán kèm tại cửa hàng.")]),
    "Cơm cháy": dict(
        h1="Cơm cháy lắc topping các vị", title="Cơm cháy lắc topping túi zip, cơm cháy 5 vị 6 vị | Sinh Thái Việt",
        desc="Cơm cháy lắc topping túi zip, cơm cháy 5 vị, 6 vị, cơm cháy mắm hành. Đóng gói chuẩn ISO 22000:2018, bán lẻ và bán sỉ cho đại lý.",
        intro=["Cơm cháy giòn rụm, lắc cùng topping và sốt là món ăn vặt được nhiều khách trẻ yêu thích.",
               "Sinh Thái Việt cung cấp cơm cháy lắc túi zip, cơm cháy 5 vị, 6 vị và cơm cháy mắm hành, đóng gói tiện lợi để bán lẻ hoặc nhập sỉ."],
        faq=[("Cơm cháy có bán sỉ không?", "Có. Liên hệ Zalo 0362 771 650 để nhận giá đại lý và giá sỉ.")]),
    "Khô & mực ăn liền": dict(
        h1="Khô bò, khô gà, khô heo, mực ăn liền", title="Khô bò, khô gà lá chanh, khô heo cháy tỏi, mực cán 100g | Sinh Thái Việt",
        desc="Khô bò sợi, khô bò miếng, khô gà lá chanh, khô heo cháy tỏi, mực cán, mực tẩm vị đóng gói 100g. Chuẩn ISO 22000:2018, giá bán lẻ và sỉ.",
        intro=["Khô bò, khô gà, khô heo và mực là các món đồ nhắm, ăn vặt được đóng gói sẵn theo khối lượng 100g, tiện bán lẻ.",
               "Sinh Thái Việt đóng gói khô bò sợi, khô bò miếng, khô gà lá chanh, khô heo cháy tỏi, mực cán và khô mực cốt dừa."],
        faq=[("Có bán khô bò, khô gà theo cân không?", "Có. Xem thêm mục Nguyên liệu sỉ để xem khô bò, khô gà, mực theo kg và theo thùng.")]),
    "Sốt, topping & gia vị lọ": dict(
        h1="Sốt, topping & gia vị đóng lọ", title="Sốt me, sốt tắc, muối tép hành phi, tóp mỡ, chà bông lọ | Sinh Thái Việt",
        desc="Sốt me, sốt tắc, sốt bò, sốt ớt, bơ vàng, muối tép hành phi, tóp mỡ, chà bông, rong biển đóng lọ. Bán lẻ, bán sỉ.",
        intro=["Sốt và topping quyết định hương vị của bánh tráng trộn. Sinh Thái Việt đóng lọ sốt me, sốt tắc, sốt bò, sốt ớt, bơ vàng và nhiều loại topping.",
               "Ngoài ra còn có muối tép hành phi, tóp mỡ, chà bông và rong biển tỏi đóng lọ, dùng ăn kèm hoặc làm quà."],
        faq=[("Có bán sốt số lượng lớn không?", "Có. Sốt có dạng lọ, chai 1 lít và can 5 lít trong mục Nguyên liệu sỉ.")]),
    "Bánh tráng hũ mix topping": dict(
        h1="Bánh tráng hũ mix topping", title="Bánh tráng hũ mix mực, khô bò, khô gà, tóp mỡ | Sinh Thái Việt",
        desc="Bánh tráng hũ mix mực cán, mực rim, khô bò, khô gà, tóp mỡ, hành phi. Hũ 100g và 200g. Chuẩn ISO 22000:2018, bán lẻ, bán sỉ.",
        intro=["Bánh tráng đóng hũ mix topping là dòng sản phẩm cao cấp hơn, đóng hũ chắc chắn, thuận tiện làm quà và bày bán.",
               "Có hai quy cách hũ 100g và 200g với các vị mực cán, mực rim, khô mực cốt dừa, khô bò, khô gà, tóp mỡ, hành và khô heo cháy tỏi."],
        faq=[("Bánh tráng hũ có làm quà tặng được không?", "Có. Hũ đóng chắc chắn, phù hợp làm quà biếu và bán tại cửa hàng.")]),
    "Combo nguyên liệu": dict(
        h1="Combo nguyên liệu mở quán bánh tráng trộn", title="Combo nguyên liệu mở quán bánh tráng trộn, cuộn, nướng | Sinh Thái Việt",
        desc="Combo nguyên liệu mở quán bánh tráng: combo trộn, combo cuộn, combo nướng, combo 3 trong 1. Giá sỉ, hỗ trợ tư vấn đại lý.",
        intro=["Combo nguyên liệu giúp bạn mở quán nhanh: đã gồm vỏ, sốt, khô và topping cần thiết cho từng kiểu bán.",
               "Có combo trộn, combo cuộn, combo nướng và combo 3 trong 1 để bán đủ ba món."],
        faq=[("Mở quán bánh tráng trộn cần nhập gì?", "Cần vỏ bánh tráng, sốt, khô và topping. Combo đã gom các nguyên liệu này; liên hệ Zalo để được tư vấn theo vốn.")]),
    "Sốt & dầu": dict(
        h1="Sốt, sate, dầu tỏi bán sỉ", title="Sốt me, sốt tắc, sốt bò, sốt ớt, sate, dầu tỏi giá sỉ | Sinh Thái Việt",
        desc="Sốt me, sốt tắc, sốt bò, sốt ớt dạng can 5 lít, chai 1 lít, túi nhỏ; sate, dầu tỏi. Nguyên liệu cho quán bánh tráng trộn.",
        intro=["Sốt là nguyên liệu quan trọng của quán bánh tráng trộn. Có dạng can 5 lít, chai 1 lít và túi nhỏ dùng một lần.",
               "Ngoài sốt còn có sate và dầu tỏi chai 1 lít."],
        faq=[("Sốt có đóng gói túi nhỏ không?", "Có. Có túi 30g, 30ml, 35ml cho từng suất bán mang đi.")]),
    "Bánh tráng & vỏ cuộn": dict(
        h1="Vỏ bánh tráng, bánh tráng sợi, bánh tráng tẩm vị", title="Vỏ bánh tráng cuộn, vỏ nướng, bánh tráng sợi giá sỉ | Sinh Thái Việt",
        desc="Vỏ bánh tráng cuộn, vỏ nướng, bánh tráng sợi trộn, bánh tráng phơi sương, dẻo tôm, bánh tráng tẩm vị bán theo kg.",
        intro=["Vỏ bánh tráng và bánh tráng sợi là nguyên liệu nền cho các món trộn, cuộn, nướng.",
               "Bán theo kg, phù hợp quán ăn vặt và đại lý."],
        faq=[("Bánh tráng sợi có loại nào?", "Có bánh tráng sợi trộn 5 ly và 7 ly, bán theo kg.")]),
    "Khô, mực & chà bông": dict(
        h1="Khô bò, khô gà, mực, chà bông bán theo cân", title="Khô bò, khô gà, mực cán, chà bông giá sỉ theo kg, thùng | Sinh Thái Việt",
        desc="Khô bò, khô gà, khô heo cháy tỏi, mực tẩm vị, mực cán, chà bông bán theo kg và thùng 5kg cho quán ăn vặt và đại lý.",
        intro=["Nguyên liệu khô bán theo kg và thùng 5kg, dành cho quán bánh tráng trộn, cơ sở đóng gói và đại lý.",
               "Gồm khô bò, khô bò miếng, khô gà, khô heo cháy tỏi, mực tẩm vị, mực cán, khô mực cốt dừa và chà bông."],
        faq=[("Có bán thùng 5kg không?", "Có. Khô bò, khô gà, khô heo cháy tỏi, mực cán có quy cách thùng 5kg.")]),
    "Topping, bơ & gia vị": dict(
        h1="Topping, bơ, hành phi, tép sấy, gia vị", title="Hành sấy, tép sấy, bơ, tóp mỡ, rong biển, lạc rang giá sỉ | Sinh Thái Việt",
        desc="Topping cho bánh tráng trộn: hành sấy, tép sấy, lạc rang, tóp mỡ, rong biển cháy tỏi, bơ thẻ, me thẻ, tắc thẻ, ớt thẻ, muối.",
        intro=["Topping và gia vị tạo nên hương vị cho bánh tráng trộn: hành sấy, tép sấy, lạc rang, tóp mỡ, rong biển cháy tỏi.",
               "Bơ, me, tắc, ớt dạng thẻ và các loại muối cũng có sẵn, bán theo kg."],
        faq=[("Topping có bán lẻ theo kg không?", "Có. Phần lớn topping bán theo kg, một số theo thùng.")]),
}

def _expand(n):
    n = re.sub(r"\bBT\b", "Bánh tráng", n)
    return re.sub(r"\bDT\b", "Dẻo tôm", n)


for _p in BT + NVL:
    _p["name"] = _expand(_p["name"])
_seen = set()
for _items, _base, _sl in ((BT, "san-pham", SLUG_BT), (NVL, "nguyen-lieu", SLUG_NVL)):
    for p in _items:
        s = slug(p["name"]) or "san-pham"
        while (_base, s) in _seen: s += "-2"
        _seen.add((_base, s))
        p["slug"] = s; p["cslug"] = _sl[p["cat"]]; p["url"] = f"{_base}/{p['cslug']}/{s}/"; p["base"] = _base


def wp(src):
    return re.sub(r"\.(jpe?g|png)$", ".webp", src) if src.startswith(("img/anh/", "img/sp/")) else src



# =========== ẢNH SẢN PHẨM THEO NHÓM ===========
G_TRON = [(102,"Bánh tráng trộn saté bò ngũ vị cao cấp"),(107,"Bánh tráng trộn gà sốt me cay"),(109,"Bánh tráng trộn phô mai gà cay"),
 (108,"Bánh tráng trộn lá bò lục vị"),(110,"Bánh tráng trộn tỏi thơm bò cay"),(104,"Bánh tráng trộn hải sản cao cấp"),
 (105,"Bánh tráng trộn phô mai chà bông"),(106,"Bánh tráng trộn mật chà chà bông"),(111,"Bánh tráng trộn saté me khô mực"),
 (132,"Bánh tráng trộn thập cẩm cao cấp"),(131,"Bánh tráng trộn túi zip 200g"),(112,"Bánh tráng xì ke vị đặc biệt"),
 (113,"Bánh tráng Luxury hút chân không"),(114,"Bánh tráng trộn hút chân không"),(116,"Bánh tráng trộn Vip"),
 (115,"Bánh tráng phô mai cuộn mực cay"),(117,"Bánh tráng matcha lá dứa phô mai"),(103,"Bánh tráng phơi sương mini"),
 (130,"Bánh tráng phơi sương muối tép hành phi"),
 (88,"Bánh tráng bò bò lục vị"),(87,"Bánh tráng trộn phô mai gà quay"),(27,"Bánh tráng vương tôm đặc biệt"),(28,"Bánh tráng lá tỏi bò"),
 (29,"Bánh tráng rong biển cháy tỏi"),(34,"Bánh tráng phô mai lá dứa"),(35,"Bánh tráng cuộn phô mai sốt bơ"),
 (37,"Bánh tráng lắc vị tomyum"),(38,"Bánh tráng lắc vị trứng muối"),(40,"Bánh tráng lắc vị kimchi"),(44,"Bánh tráng cuộn dứa thập cẩm"),
 (48,"Bánh tráng sợi nguyên sate bò"),(49,"Bánh tráng phô mai tôm"),(101,"Bánh tráng sọt phô mai sốt mai")]
G_SET = [(118,"Bánh tráng phơi sương best seller mix sốt"),(119,"Bánh tráng tóp mỡ hành phi"),(120,"Set siêu vip topping lọ"),
 (121,"Bánh tráng khô mực cốt dừa"),(122,"Set dẻo tôm bơ chà bông"),(123,"Bánh tráng bơ lục vị"),(124,"Bánh tráng phơi sương tóp mỡ"),
 (125,"Bánh tráng sốt chấm chua ngọt"),(126,"Bánh tráng me lục vị"),(127,"Bánh tráng bơ béo trứng muối"),
 (128,"Bánh tráng bơ ngũ vị"),(129,"Bánh tráng bơ me"),
 (70,"Combo bánh tráng me bơ siêu toppings"),(74,"Combo bánh tráng tắc bơ siêu toppings"),(57,"Bánh tráng bò ngũ vị set sốt và topping"),
 (80,"Bánh tráng mix sốt bơ tam vị"),(100,"Set bánh tráng sốt chua ngọt đủ topping"),(91,"Bánh tráng khô mực ớt dừa túi bạc"),
 (92,"Bánh tráng nướng set topping khay"),(98,"Bánh tráng nướng vỏ vàng và khay topping"),(75,"Bánh tráng cuộn bơ set đầy đủ"),
 (94,"Set 6 lọ topping và bánh tráng"),(97,"Set bánh tráng 4 lọ topping và bơ trứng gà"),(69,"Nguyên liệu trộn bánh tráng: vỏ, topping, sốt tắc")]
G_SAUCE = [(81,"Sốt me Sinh Thái Việt"),(78,"Sốt tắc Sinh Thái Việt"),(77,"Ớt rim Sinh Thái Việt"),
 (73,"Bơ trứng gà Sinh Thái Việt"),(72,"Bơ trứng gà chai bóp"),(79,"Tóp mỡ rim mắm hành hũ")]
G_MAP = {"Bánh tráng trộn, phơi sương & dẻo tôm": G_TRON, "Set & combo ăn vặt": G_SET,
         "Sốt, topping & gia vị lọ": G_SAUCE, "Sốt & dầu": G_SAUCE[:4], "Combo nguyên liệu": G_SET[12:14]+G_SET[-1:],
         "Topping, bơ & gia vị": G_SAUCE[3:]}


def gallery_html(items, rel, h2="Hình ảnh sản phẩm"):
    figs = "".join(f'<figure><img src="{rel}img/anh/b{n:02d}.webp" alt="{e(c)} - Sinh Thái Việt" width="600" height="600" loading="lazy" decoding="async"><figcaption>{e(c)}</figcaption></figure>' for n, c in items)
    return f'<h2>{h2}</h2><div class="gal2">{figs}</div>'

def cat_page(items, base, cat, sl):
    info = CAT_INFO[cat]
    its = [p for p in items if p["cat"] == cat]
    grid = "".join(card(p, "../../", base) for p in its)
    others = "".join(f'<a class="pill" href="../{sl[c]}/">{e(c)}</a>' for c in sl if c != cat)
    faq = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in info["faq"])
    parent = ("Sản phẩm", "san-pham/") if base == "san-pham" else ("Nguyên liệu sỉ", "nguyen-lieu/")
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../../">Trang chủ</a> / <a href="../">{parent[0]}</a> / {e(cat)}</nav>
<h1>{e(info["h1"])}</h1><p class="lead">{e(info["intro"][0])}</p></div></section>
<section class="sec"><div class="wrap"><p class="narrow">{e(info["intro"][1])}</p>
<h2>{len(its)} sản phẩm trong nhóm</h2><div class="grid">{grid}</div></div></section>
{('<section class="sec alt"><div class="wrap">' + gallery_html(G_MAP[cat], "../../") + '</div></section>') if cat in G_MAP else ""}
<section class="sec alt"><div class="wrap narrow"><h2>Câu hỏi thường gặp</h2>{faq}
<h2>Nhóm khác</h2><p class="pills">{others}</p>
<p><a class="btn" href="https://zalo.me/{PHONE}" target="_blank" rel="noopener">Nhận báo giá qua Zalo {PHONE_FMT}</a></p></div></section>"""
    faqld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in info["faq"]]}
    path = f"{base}/{sl[cat]}"
    ogi = its[0]["img"] if its and its[0]["img"] else "img/anh/b102.jpg"
    write(path, page(path + "/", info["title"], info["desc"], body, 2, ogi,
                     jsonld=[itemlist(its, info["h1"], path + "/"), faqld],
                     crumbs=[("Trang chủ", ""), parent, (cat, path + "/")]))


def prod_page(p, items, sl):
    cat = p["cat"]; base = p["base"]
    related = [q for q in items if q["cat"] == cat and q is not p][:4]
    rel_html = "".join(card(q, "../../../", base) for q in related)
    kind = "nguyên liệu bánh tráng" if base == "nguyen-lieu" else "bánh tráng, đồ ăn vặt"
    desc_txt = (f"{p['name']} thuộc nhóm {cat.lower()} của Sinh Thái Việt, đóng gói theo {p['unit'].lower()}, "
                f"sản xuất và đóng gói theo hệ thống an toàn thực phẩm ISO 22000:2018. Giá bán lẻ khuyến nghị {p['price']}.")
    src = p["img"] or "img/logo-2.png"
    parent = ("Sản phẩm", "san-pham/") if base == "san-pham" else ("Nguyên liệu sỉ", "nguyen-lieu/")
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../../../">Trang chủ</a> / <a href="../../">{parent[0]}</a> / <a href="../">{e(cat)}</a> / {e(p["name"])}</nav></div></section>
<section class="sec"><div class="wrap split top">
{img(src, p["name"] + " - " + kind + " Sinh Thái Việt", "../../../", 600, 600, "" if p["img"] else "ph", lazy=False)}
<div><h1>{e(p["name"])}</h1><p class="pr big">{p["price"]}<small> giá bán lẻ khuyến nghị / {e(p["unit"].lower())}</small></p>
<p>{e(desc_txt)}</p><table class="tb"><tr><th>Nhóm</th><td><a href="../">{e(cat)}</a></td></tr><tr><th>Đơn vị</th><td>{e(p["unit"])}</td></tr>
<tr><th>Thương hiệu</th><td>Sinh Thái Việt</td></tr><tr><th>Tiêu chuẩn</th><td>ISO 22000:2018 (số W2386F)</td></tr></table>
<p><a class="btn" href="https://zalo.me/{PHONE}" target="_blank" rel="noopener">Đặt mua qua Zalo</a> <a class="btn ghost" href="../../../dai-ly/">Giá đại lý & sỉ</a></p></div></div></section>
<section class="sec alt"><div class="wrap"><h2>Sản phẩm cùng nhóm</h2><div class="grid">{rel_html}</div></div></section>"""
    price = p["raw"] or "0"
    pld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": desc_txt,
           "image": f"{DOMAIN}/{p['img']}" if p["img"] else f"{DOMAIN}/img/logo-2.png", "category": cat,
           "brand": {"@type": "Brand", "name": "Sinh Thái Việt"},
           "manufacturer": {"@id": f"{DOMAIN}/#org"},
           "offers": {"@type": "Offer", "priceCurrency": "VND", "price": price, "availability": "https://schema.org/InStock",
                      "url": f"{DOMAIN}/{p['url']}", "seller": {"@id": f"{DOMAIN}/#org"}}}
    title = f"{p['name']}{' (nguyên liệu sỉ)' if base == 'nguyen-lieu' else ''} - giá {p['price']} | Sinh Thái Việt"
    d = f"{p['name']} giá {p['price']}/{p['unit'].lower()}, {cat.lower()} Sinh Thái Việt đạt ISO 22000:2018. Mua lẻ, mua sỉ, làm đại lý. Zalo {PHONE_FMT}."
    write(p["url"].rstrip("/"), page(p["url"], title, d[:300], body, 3, p["img"] or "img/anh/b102.jpg", jsonld=[pld],
                                      crumbs=[("Trang chủ", ""), parent, (cat, f"{base}/{p['cslug']}/"), (p["name"], p["url"])]))


ARTICLES = [
    dict(slug="banh-trang-tron-gom-nhung-gi", title="Bánh tráng trộn gồm những gì? Cách trộn và các loại topping",
         desc="Bánh tráng trộn gồm bánh tráng sợi, khô bò, khô gà, tóp mỡ, hành phi, đậu phộng và sốt. Tìm hiểu thành phần, cách trộn và các vị phổ biến.",
         body="""<p>Bánh tráng trộn là món ăn vặt phổ biến, được làm từ bánh tráng cắt sợi tẩm vị, trộn cùng nhiều loại topping và sốt. Mỗi vùng, mỗi quán có công thức riêng, nhưng các thành phần chính khá giống nhau.</p>
<h2>Thành phần chính của bánh tráng trộn</h2><ul><li><strong>Bánh tráng:</strong> sợi trộn, bánh tráng tẩm vị, phơi sương hoặc dẻo tôm.</li><li><strong>Đồ khô:</strong> khô bò, khô gà lá chanh, khô heo cháy tỏi, mực.</li><li><strong>Topping:</strong> tóp mỡ, hành phi, tép sấy, đậu phộng, rong biển, chà bông.</li><li><strong>Sốt và gia vị:</strong> sốt me, sốt tắc, sốt bò, sốt ớt, bơ, muối tép.</li></ul>
<h2>Cách trộn cơ bản</h2><p>Cho bánh tráng vào bát hoặc túi, thêm sốt theo khẩu vị rồi trộn đều cho bánh thấm. Sau đó thêm đồ khô và topping, trộn nhẹ tay để không làm vụn. Thưởng thức ngay để giữ độ giòn và dai.</p>
<h2>Các vị được ưa chuộng</h2><p>Các vị hay gặp gồm sate bò, me bơ, tắc bơ, bơ ngũ vị, phô mai, gà sốt me cay và lá bò lục vị. Bạn có thể xem toàn bộ danh mục tại <a href="../../san-pham/banh-trang-tron/">bánh tráng trộn, phơi sương, dẻo tôm</a> của Sinh Thái Việt.</p>"""),
    dict(slug="mo-quan-banh-trang-tron-can-nhung-gi", title="Mở quán bánh tráng trộn cần chuẩn bị nguyên liệu gì?",
         desc="Danh sách nguyên liệu cần có khi mở quán bánh tráng trộn: vỏ bánh tráng, sốt, khô bò, mực, topping và combo nhập sỉ tiết kiệm.",
         body="""<p>Quán bánh tráng trộn có vốn ban đầu nhỏ và dễ bắt đầu, nhưng nguyên liệu cần ổn định về chất lượng và nguồn nhập. Dưới đây là danh sách cơ bản.</p>
<h2>Nhóm nguyên liệu bắt buộc</h2><ul><li>Bánh tráng sợi, vỏ cuộn, vỏ nướng.</li><li>Sốt me, tắc, bò, ớt, bơ.</li><li>Khô bò, khô gà, khô heo cháy tỏi, mực.</li><li>Topping: hành phi, tép sấy, lạc rang, tóp mỡ, rong biển.</li><li>Bao bì: túi, hộp, thìa.</li></ul>
<h2>Nhập theo combo để tiết kiệm</h2><p>Nếu mới bắt đầu, bạn có thể chọn combo trộn, combo cuộn, combo nướng hoặc combo 3 trong 1 để có đủ nguyên liệu cho từng kiểu bán. Xem tại <a href="../../nguyen-lieu/combo-mo-quan/">combo nguyên liệu mở quán</a>.</p>
<h2>Chọn nhà cung cấp</h2><p>Nên chọn đơn vị có chứng nhận an toàn thực phẩm và bảng giá rõ ràng cho từng mức số lượng. Sinh Thái Việt có <a href="../../dai-ly/">chính sách đại lý và giá sỉ</a> theo ba mức, kèm giá bán lẻ khuyến nghị để bạn tính lợi nhuận.</p>"""),
    dict(slug="iso-22000-2018-la-gi", title="ISO 22000:2018 là gì? Vì sao quan trọng với đồ ăn vặt đóng gói",
         desc="ISO 22000:2018 là tiêu chuẩn hệ thống quản lý an toàn thực phẩm. Tìm hiểu ý nghĩa và vì sao nên chọn nhà cung cấp bánh tráng có chứng nhận.",
         body="""<p>ISO 22000:2018 là tiêu chuẩn quốc tế về hệ thống quản lý an toàn thực phẩm, áp dụng cho các tổ chức trong chuỗi cung ứng thực phẩm.</p>
<h2>Tiêu chuẩn này yêu cầu gì?</h2><p>Tổ chức phải nhận diện mối nguy an toàn thực phẩm, kiểm soát quy trình sản xuất và đóng gói, ghi chép hồ sơ và cải tiến liên tục. Chứng nhận được đánh giá giám sát định kỳ.</p>
<h2>Lợi ích với người mua và đại lý</h2><ul><li>Quy trình sản xuất được kiểm soát và có hồ sơ.</li><li>Dễ tạo niềm tin với khách hàng cuối.</li><li>Thuận lợi khi làm việc với siêu thị, cửa hàng, đại lý.</li></ul>
<h2>Sinh Thái Việt đạt chứng nhận</h2><p>Hợp tác xã Đầu tư Sinh Thái Việt được Công ty Cổ phần Chứng nhận WCERT cấp chứng nhận ISO 22000:2018 số W2386F, hiệu lực 11/7/2025 đến 10/7/2028, cho hoạt động sản xuất, đóng gói, kinh doanh sản phẩm từ bánh tráng. Xem <a href="../../chung-nhan/">giấy chứng nhận</a>.</p>"""),
    dict(slug="cach-bao-quan-banh-trang-tron-kho-bo", title="Cách bảo quản bánh tráng trộn, khô bò, khô gà đúng cách",
         desc="Hướng dẫn bảo quản bánh tráng trộn, khô bò, khô gà, mực: nơi khô ráo, tránh nắng, đóng kín sau khi mở và lưu ý khi bán hàng.",
         body="""<p>Bảo quản đúng cách giúp bánh tráng, khô và sốt giữ hương vị lâu hơn. Hãy ưu tiên làm theo hướng dẫn in trên bao bì của từng sản phẩm.</p>
<h2>Nguyên tắc chung</h2><ul><li>Để nơi khô ráo, thoáng mát, tránh ánh nắng trực tiếp.</li><li>Đóng kín túi zip hoặc hũ sau khi mở.</li><li>Không để sản phẩm tiếp xúc nước hoặc hơi ẩm.</li><li>Dùng thìa, dụng cụ sạch khi lấy sản phẩm.</li></ul>
<h2>Với sốt và topping</h2><p>Sốt nên đậy kín, để nơi mát. Topping như hành phi, tóp mỡ nên đóng kín để giữ độ giòn.</p>
<h2>Với đại lý và quán</h2><p>Nhập số lượng vừa đủ, xoay vòng hàng theo nguyên tắc nhập trước bán trước. Xem thêm <a href="../../nguyen-lieu/">nguyên liệu sỉ</a> của Sinh Thái Việt.</p>"""),
]


def articles():
    cards = "".join(f'<article class="box"><h2><a href="{a["slug"]}/">{e(a["title"])}</a></h2><p>{e(a["desc"])}</p><a href="{a["slug"]}/">Đọc tiếp</a></article>' for a in ARTICLES)
    body = f"""<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../">Trang chủ</a> / Kiến thức</nav>
<h1>Kiến thức bánh tráng trộn &amp; kinh doanh đồ ăn vặt</h1><p class="lead">Hướng dẫn mở quán, chọn nguyên liệu, bảo quản và tiêu chuẩn an toàn thực phẩm.</p></div></section>
<section class="sec"><div class="wrap cols3">{cards}</div></section>"""
    write("kien-thuc", page("kien-thuc/", "Kiến thức bánh tráng trộn, mở quán ăn vặt | Sinh Thái Việt",
                            "Bài viết về bánh tráng trộn, nguyên liệu mở quán, tiêu chuẩn ISO 22000:2018 và cách bảo quản đồ ăn vặt từ Sinh Thái Việt.",
                            body, 1, crumbs=[("Trang chủ", ""), ("Kiến thức", "kien-thuc/")]))
    for a in ARTICLES:
        path = f"kien-thuc/{a['slug']}"
        b = f"""<section class="sec pagehead"><div class="wrap narrow"><nav class="bc" aria-label="Breadcrumb"><a href="../../">Trang chủ</a> / <a href="../">Kiến thức</a> / {e(a["title"])}</nav>
<h1>{e(a["title"])}</h1><p class="muted">Sinh Thái Việt · Cập nhật {TODAY}</p></div></section>
<section class="sec"><div class="wrap narrow article">{a["body"]}<p><a class="btn" href="https://zalo.me/{PHONE}" target="_blank" rel="noopener">Tư vấn qua Zalo {PHONE_FMT}</a></p></div></section>"""
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["desc"],
              "datePublished": TODAY, "dateModified": TODAY, "inLanguage": "vi",
              "author": {"@id": f"{DOMAIN}/#org"}, "publisher": {"@id": f"{DOMAIN}/#org"},
              "mainEntityOfPage": f"{DOMAIN}/{path}/", "image": f"{DOMAIN}/img/anh/b102.jpg"}
        write(path, page(path + "/", a["title"] + " | Sinh Thái Việt", a["desc"], b, 2, jsonld=[ld],
                         crumbs=[("Trang chủ", ""), ("Kiến thức", "kien-thuc/"), (a["title"], path + "/")]))


def home_extra():
    cats = "".join(f'<a class="box" href="san-pham/{SLUG_BT[c]}/"><h3>{e(CAT_INFO[c]["h1"])}</h3><p>{sum(1 for p in BT if p["cat"]==c)} sản phẩm</p></a>' for c in SLUG_BT)
    faqs = [("Sinh Thái Việt bán những sản phẩm gì?", "Bánh tráng trộn, phơi sương, dẻo tôm, cơm cháy, khô bò, khô gà, mực, sốt, topping, set ăn vặt và nguyên liệu bán sỉ cho quán."),
            ("Sản phẩm có đạt chuẩn an toàn thực phẩm không?", "Có. Hợp tác xã được cấp chứng nhận ISO 22000:2018 số W2386F, hiệu lực đến 10/7/2028."),
            ("Làm sao để làm đại lý hoặc mua sỉ?", "Liên hệ Zalo 0362 771 650 để nhận bảng giá. Giá sỉ áp dụng từ 30 gói."),
            ("Sinh Thái Việt ở đâu?", "Trụ sở tại Phường Đồng Quang, thành phố Thái Nguyên; cơ sở sản xuất tại phường Hòa Bình, tỉnh Hòa Bình.")]
    fh = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in faqs)
    return (f'<section class="sec"><div class="wrap"><h2>Danh mục sản phẩm</h2><div class="cols3 linkbox">{cats}</div></div></section>'
            f'<section class="sec alt"><div class="wrap narrow"><h2>Câu hỏi thường gặp</h2>{fh}'
            f'<p><a href="kien-thuc/">Xem thêm bài viết kiến thức</a></p></div></section>'
            f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}, ensure_ascii=False)}</script>')


EXTRA_CSS = """
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0)}
.cb h3 a{color:inherit;text-decoration:none}.cb h3 a:hover{color:var(--gold-d)}
.pills{display:flex;flex-wrap:wrap;gap:8px}.pill{border:1px solid var(--gold);border-radius:999px;padding:6px 14px;text-decoration:none;font-size:.9rem;background:#fff}
.linkbox a{text-decoration:none;color:var(--ink)}.linkbox a:hover{border-color:var(--gold)}.linkbox p{margin:0;color:var(--muted)}
.article h2{margin-top:1.6em}.article li{margin:.4em 0}.cols3 .box h2{font-size:1.15rem}.cols3 .box h2 a{text-decoration:none;color:var(--ink)}
.bc a{color:var(--muted)}.split.top>img{max-height:none}
"""
EXTRA_CSS += """
.gal2{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:16px}.gal2 figure{margin:0;background:#fff;border:1px solid var(--cream2);border-radius:14px;overflow:hidden}
.gal2 img{aspect-ratio:1;object-fit:cover;width:100%}.gal2 figcaption{padding:10px 12px;font-size:.88rem;font-weight:600}
.steps{display:grid;gap:22px;margin-top:24px}.step{display:grid;grid-template-columns:48px 260px 1fr;gap:20px;align-items:center;background:#fff;border:1px solid var(--cream2);border-radius:18px;padding:16px}
.step img{border-radius:14px;aspect-ratio:1;object-fit:cover;width:100%}.num{width:44px;height:44px;border-radius:50%;background:var(--gold);color:#fff;display:grid;place-items:center;font-weight:700;font-size:1.2rem}
.linkbox .box img{border-radius:12px;margin-bottom:12px;aspect-ratio:1;object-fit:cover;width:100%}
@media(max-width:860px){.step{grid-template-columns:1fr}.num{margin:0}}
"""
CSS += EXTRA_CSS


def to_webp():
    from PIL import Image
    for d in ("img/anh", "img/sp"):
        full = os.path.join(OUT, d)
        for f in os.listdir(full):
            if f.lower().endswith((".jpg", ".jpeg", ".png")):
                im = Image.open(os.path.join(full, f)).convert("RGB")
                im.thumbnail((1000, 1000))
                im.save(os.path.join(full, os.path.splitext(f)[0] + ".webp"), "WEBP", quality=78, method=6)


if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    for d in ("img",):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d))
    open(os.path.join(OUT, "style.css"), "w").write(CSS)
    open(os.path.join(OUT, "app.js"), "w").write(JS)
    to_webp()
    home(); story(); products(); materials(); dealer(); certs(); contact(); articles()
    for c in SLUG_BT: cat_page(BT, "san-pham", c, SLUG_BT)
    for c in SLUG_NVL: cat_page(NVL, "nguyen-lieu", c, SLUG_NVL)
    for p in BT: prod_page(p, BT, SLUG_BT)
    for p in NVL: prod_page(p, NVL, SLUG_NVL)
    pages = sorted(set(("" if x == "" else x.rstrip("/") + "/") for x in SITE))
    open(os.path.join(OUT, "llms.txt"), "w", encoding="utf-8").write(
        "# Sinh Thái Việt\n> Hợp tác xã Đầu tư Sinh Thái Việt (Thái Nguyên): sản xuất, đóng gói, kinh doanh bánh tráng trộn, khô, sốt, nguyên liệu sỉ. ISO 22000:2018 số W2386F.\n\n"
        + "\n".join(f"- {DOMAIN}/{x}" for x in pages if x.count("/") <= 2) + "\n")
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
        "".join(f"<url><loc>{DOMAIN}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if not p else ('0.8' if p.count('/') <= 1 else '0.6')}</priority></url>" for p in pages) + "</urlset>")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
        page("404.html", "Không tìm thấy trang | Sinh Thái Việt", "Trang không tồn tại.",
             '<section class="sec"><div class="wrap center"><h1>Không tìm thấy trang</h1><p><a class="btn" href="/">Về trang chủ</a></p></div></section>', 0)
        .replace('index,follow', 'noindex').replace('href="style.css"','href="/style.css"').replace('src="app.js"','src="/app.js"').replace('src="img/','src="/img/').replace('href="img/','href="/img/').replace('href="#main"','href="#main"'))
    print("OK", len(BT), len(NVL))
