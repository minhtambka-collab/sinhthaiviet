#!/usr/bin/env python3
"""Dựng site tĩnh Sinh Thái Việt -> thư mục dist/. Chạy: python3 build.py"""
import json, os, re, html, shutil, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "dist")
DOMAIN = "https://sinhthaiviet.vercel.app"
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
BT = []
for r in DATA["bt"]:
    BT.append(dict(name=r["name"], unit=r["unit"], price=money(r["retail"]), raw=re.sub(r"\D", "", r["retail"]),
                   img=("img/sp/" + r["img"]) if r["img"] else None, cat=cat_bt(r["name"])))
NVL = []
for r in DATA["nvl"]:
    NVL.append(dict(name=r["name"], unit=r["unit"], price=money(r["retail"]), raw=re.sub(r"\D", "", r["retail"]),
                    img=("img/sp/" + r["img"]) if r["img"] else None, cat=cat_nvl(r["name"])))

# ---------- layout ----------
NAV = [("", "Trang chủ"), ("cau-chuyen/", "Câu chuyện"), ("san-pham/", "Sản phẩm"),
       ("nguyen-lieu/", "Nguyên liệu sỉ"), ("dai-ly/", "Đại lý & sỉ"), ("chung-nhan/", "Chứng nhận"), ("lien-he/", "Liên hệ")]


def page(path, title, desc, body, depth=0, og_img="img/anh/a45.jpg", jsonld=None, crumbs=None):
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
         "foundingDate": "2024-04-17"})]
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


def write(path, content):
    p = os.path.join(OUT, path, "index.html") if path else os.path.join(OUT, "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w", encoding="utf-8").write(content)


def img(src, alt, rel, w=600, h=600, cls="", lazy=True):
    return f'<img src="{rel}{src}" alt="{e(alt)}" width="{w}" height="{h}" {"loading=lazy decoding=async" if lazy else "fetchpriority=high"} class="{cls}">'


def card(p, rel, kind):
    src = p["img"] or "img/logo-2.png"
    ph = "" if p["img"] else " ph"
    alt = f'{p["name"]} - {"nguyên liệu bánh tráng" if kind=="nvl" else "bánh tráng"} Sinh Thái Việt'
    return (f'<article class="card{ph}" data-cat="{e(p["cat"])}" data-name="{e(p["name"].lower())}">'
            f'{img(src, alt, rel, 300, 300)}<div class="cb"><h3>{e(p["name"])}</h3>'
            f'<p class="un">Đơn vị: {e(p["unit"])}</p><p class="pr">{p["price"]}<small> giá bán lẻ tham khảo</small></p>'
            f'<a class="btn sm" href="https://zalo.me/{PHONE}" target="_blank" rel="noopener">Hỏi mua qua Zalo</a></div></article>')


def catalog(items, rel, kind):
    cats = []
    for p in items:
        if p["cat"] not in cats: cats.append(p["cat"])
    chips = '<button class="chip on" data-f="">Tất cả</button>' + "".join(
        f'<button class="chip" data-f="{e(c)}">{e(c)} <span>{sum(1 for p in items if p["cat"]==c)}</span></button>' for c in cats)
    grid = "".join(card(p, rel, kind) for p in items)
    return (f'<div class="tools"><input id="q" type="search" placeholder="Tìm sản phẩm..." aria-label="Tìm sản phẩm"><div class="chips">{chips}</div></div>'
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
    feats = [("img/anh/a45.jpg", "Sate bò ngũ vị"), ("img/anh/a41.jpg", "Gà sốt me cay"),
             ("img/anh/a49.jpg", "Phô mai chà bông"), ("img/anh/a40.jpg", "Lá bò lục vị")]
    fcards = "".join(f'<figure>{img(s, "Bánh tráng trộn " + t + " Sinh Thái Việt", "", 500, 500)}<figcaption>{t}</figcaption></figure>' for s, t in feats)
    body = f"""
<section class="hero"><div class="wrap hero-in"><div>
<p class="eyebrow">Hợp tác xã Đầu tư Sinh Thái Việt · Thái Nguyên</p>
<h1>Bánh tráng trộn &amp; đặc sản ăn vặt đạt chuẩn ISO 22000</h1>
<p class="lead">Từ tấm bánh tráng đến hũ, túi, set ăn vặt hoàn chỉnh. Sản xuất và đóng gói theo hệ thống an toàn thực phẩm ISO 22000:2018, phục vụ khách lẻ, đại lý và quán ăn vặt trên toàn quốc.</p>
<p class="cta"><a class="btn" href="san-pham/">Xem sản phẩm</a><a class="btn ghost" href="dai-ly/">Làm đại lý / mua sỉ</a></p>
<ul class="badges"><li>ISO 22000:2018</li><li>{len(BT)}+ sản phẩm</li><li>{len(NVL)}+ nguyên liệu sỉ</li></ul>
</div>{img("img/anh/a45.jpg", "Bánh tráng trộn sate bò ngũ vị Sinh Thái Việt", "", 700, 700, "hero-img", lazy=False)}</div></section>

<section class="sec"><div class="wrap"><h2>Vì sao chọn Sinh Thái Việt?</h2>
<div class="cols3">
<div class="box"><h3>Quản lý an toàn thực phẩm</h3><p>Chứng nhận ISO 22000:2018 số W2386F do WCERT cấp, hiệu lực 11/7/2025 – 10/7/2028, phạm vi sản xuất, đóng gói, kinh doanh sản phẩm từ bánh tráng.</p></div>
<div class="box"><h3>Danh mục đầy đủ</h3><p>Bánh tráng trộn, phơi sương, dẻo tôm, cơm cháy, khô bò – gà – mực, sốt và topping. Bán lẻ, bán sỉ và cung cấp nguyên liệu.</p></div>
<div class="box"><h3>Chính sách đại lý rõ ràng</h3><p>Ba mức giá: đại lý chiến lược, đại lý và giá sỉ từ 30 gói, kèm giá bán lẻ khuyến nghị để dễ lên kế hoạch kinh doanh.</p></div>
</div></div></section>

<section class="sec alt"><div class="wrap"><h2>Sản phẩm được yêu thích</h2><p class="muted">Một số vị bánh tráng trộn đóng túi zip, hút chân không, đủ topping.</p>
<div class="feat">{fcards}</div><p class="center"><a class="btn" href="san-pham/">Xem toàn bộ {len(BT)} sản phẩm</a></p></div></section>

<section class="sec"><div class="wrap split">
{img("img/anh/a20.jpg", "Set bánh tráng trộn topping nhiều màu Sinh Thái Việt", "", 700, 700)}
<div><h2>Câu chuyện thương hiệu</h2>
<p>Biểu tượng Sinh Thái Việt là bàn tay nâng đỡ cánh đồng và mầm cây, gắn với đồng tiền và nhịp sống hiện đại. Đó cũng là cách chúng tôi làm nghề: tôn trọng nguyên liệu, nâng niu người làm ra, đầu tư dài hạn vào chất lượng.</p>
<p><a class="btn ghost" href="cau-chuyen/">Đọc câu chuyện</a></p></div></div></section>

<section class="sec alt"><div class="wrap"><h2>Cung cấp nguyên liệu cho quán ăn vặt</h2>
<p>Vỏ bánh tráng, sốt me – tắc – bò – ớt, khô bò, khô gà, mực cán, hành phi, tóp mỡ, bơ... đóng can, thùng hoặc theo kg. Có sẵn combo trộn, cuộn, nướng để mở quán nhanh.</p>
<p><a class="btn" href="nguyen-lieu/">Xem bảng nguyên liệu</a></p></div></section>
"""
    write("", page("", "Bánh tráng trộn, đặc sản ăn vặt ISO 22000 | Sinh Thái Việt Thái Nguyên",
                   "Sinh Thái Việt: sản xuất, đóng gói, bán sỉ và lẻ bánh tráng trộn, khô bò, khô gà, mực, sốt và nguyên liệu cho quán ăn vặt. Đạt ISO 22000:2018. Hotline 0362 771 650.",
                   body, 0))


# ---------- CÂU CHUYỆN ----------
def story():
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../">Trang chủ</a> / Câu chuyện</nav>
<h1>Câu chuyện Sinh Thái Việt</h1><p class="lead">Từ một hợp tác xã ở Thái Nguyên đến dòng sản phẩm bánh tráng đạt chuẩn quốc tế về an toàn thực phẩm.</p></div></section>

<section class="sec"><div class="wrap narrow">
<h2>Khởi nguồn: hợp tác xã đầu tư vào đồ ăn vặt Việt</h2>
<p>Hợp tác xã Đầu tư Sinh Thái Việt được đăng ký thành lập ngày 17/4/2024 tại thành phố Thái Nguyên, với vốn điều lệ một tỷ đồng. Chúng tôi chọn bánh tráng, món ăn vặt quen thuộc của mọi lứa tuổi, làm nền tảng để xây dựng một chuỗi sản phẩm bài bản, thay vì chỉ bán lẻ từng gói.</p>
<h2>Một tấm bánh tráng, nhiều cách thưởng thức</h2>
<p>Từ tấm bánh tráng, chúng tôi phát triển ra bánh tráng trộn, phơi sương, dẻo tôm, cơm cháy, bánh tráng nướng, cùng các loại khô bò, khô gà, khô heo cháy tỏi, mực cán, mực rim và những lọ sốt, topping đi kèm. Mỗi sản phẩm được đóng gói tiện mang đi, đủ topping, sẵn sàng ăn liền.</p>
</div></section>

<section class="sec alt"><div class="wrap split">
{img("img/anh/a23.jpg", "Bánh tráng trộn đóng túi hút chân không nhiều topping", "", 700, 700)}
<div><h2>Sản phẩm của chúng tôi gồm những gì?</h2><ul class="ticks">
<li>Bánh tráng trộn, phơi sương, dẻo tôm đóng túi zip và hút chân không</li>
<li>Set ăn vặt: set cuộn, set nướng, set me bơ, set tắc bơ, khay khô tứ vị</li>
<li>Khô bò, khô gà lá chanh, khô heo cháy tỏi, mực cán, khô mực cốt dừa</li>
<li>Sốt me, sốt tắc, sốt bò, sốt ớt, bơ vàng, muối tép hành phi, tóp mỡ</li>
<li>Nguyên liệu sỉ theo kg, can, thùng cho quán và đại lý</li></ul></div></div></section>

<section class="sec"><div class="wrap narrow">
<h2>Cam kết an toàn: chuẩn ISO 22000:2018</h2>
<p>Tháng 7/2025, Sinh Thái Việt được Công ty Cổ phần Chứng nhận WCERT cấp Giấy chứng nhận Hệ thống Quản lý An toàn Thực phẩm theo tiêu chuẩn ISO 22000:2018 (số W2386F), cho hoạt động sản xuất, đóng gói, kinh doanh các sản phẩm từ bánh tráng. Giấy chứng nhận có hiệu lực đến ngày 10/7/2028 và được đánh giá giám sát định kỳ hằng năm.</p>
<p><a class="btn ghost" href="../chung-nhan/">Xem giấy chứng nhận</a></p>
<h2>Ý nghĩa biểu tượng</h2>
<div class="logo-story">{img("img/logo-2.png", "Logo Hợp tác xã Đầu tư Sinh Thái Việt", "../", 220, 220)}
<p>Vòng tròn âm dương thể hiện sự cân bằng giữa con người, đồng tiền đầu tư và thiên nhiên. Bàn tay nâng đỡ cánh đồng và mầm cây là lời cam kết đồng hành cùng nhà vườn, người làm nghề và đại lý. Sắc vàng đất là màu của lúa chín, của bánh tráng giòn và của sự thịnh vượng.</p></div>
<h2>Hướng đi tiếp theo</h2>
<p>Chúng tôi tiếp tục mở rộng mạng lưới đại lý, chuẩn hóa nguyên liệu cho quán ăn vặt và phát triển thêm hương vị mới. Nếu bạn muốn trở thành đối tác, hãy liên hệ để được tư vấn chính sách giá và hỗ trợ khởi động.</p>
<p><a class="btn" href="../dai-ly/">Trở thành đại lý</a></p>
</div></section>
"""
    write("cau-chuyen", page("cau-chuyen/", "Câu chuyện thương hiệu Sinh Thái Việt | Hợp tác xã Đầu tư Thái Nguyên",
                             "Câu chuyện Hợp tác xã Đầu tư Sinh Thái Việt: thành lập 2024 tại Thái Nguyên, sản xuất bánh tráng đạt chuẩn ISO 22000:2018, ý nghĩa logo và định hướng phát triển.",
                             body, 1, "img/anh/a23.jpg", crumbs=[("Trang chủ", ""), ("Câu chuyện", "cau-chuyen/")]))


# ---------- SẢN PHẨM ----------
def products():
    body = f"""
<section class="sec pagehead"><div class="wrap"><nav class="bc" aria-label="Breadcrumb"><a href="../">Trang chủ</a> / Sản phẩm</nav>
<h1>Sản phẩm bánh tráng &amp; đặc sản ăn vặt</h1>
<p class="lead">{len(BT)} sản phẩm: bánh tráng trộn, phơi sương, dẻo tôm, cơm cháy, khô, sốt và set ăn vặt. Giá hiển thị là giá bán lẻ khuyến nghị.</p></div></section>
<section class="sec"><div class="wrap">{catalog(BT, "../", "bt")}</div></section>
<section class="sec alt"><div class="wrap"><h2>Thư viện ảnh sản phẩm</h2><div class="gallery">
{"".join(img(f"img/anh/a{i:02d}.jpg", "Bánh tráng trộn Sinh Thái Việt - ảnh sản phẩm " + str(i), "../", 500, 500) for i in [36,37,38,39,40,41,42,43,44,46,47,48,49,50])}
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
                         body, 1, "img/anh/a20.jpg", jsonld=[faqld], crumbs=[("Trang chủ", ""), ("Đại lý & sỉ", "dai-ly/")]))


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

if __name__ == "__main__":
    if os.path.exists(OUT): shutil.rmtree(OUT)
    os.makedirs(OUT)
    for d in ("img",):
        shutil.copytree(os.path.join(ROOT, d), os.path.join(OUT, d))
    open(os.path.join(OUT, "style.css"), "w").write(CSS)
    open(os.path.join(OUT, "app.js"), "w").write(JS)
    home(); story(); products(); materials(); dealer(); certs(); contact()
    pages = ["", "cau-chuyen/", "san-pham/", "nguyen-lieu/", "dai-ly/", "chung-nhan/", "lien-he/"]
    open(os.path.join(OUT, "sitemap.xml"), "w").write(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' +
        "".join(f"<url><loc>{DOMAIN}/{p}</loc><lastmod>{TODAY}</lastmod><priority>{'1.0' if not p else '0.8'}</priority></url>" for p in pages) + "</urlset>")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    open(os.path.join(OUT, "404.html"), "w", encoding="utf-8").write(
        page("404.html", "Không tìm thấy trang | Sinh Thái Việt", "Trang không tồn tại.",
             '<section class="sec"><div class="wrap center"><h1>Không tìm thấy trang</h1><p><a class="btn" href="/">Về trang chủ</a></p></div></section>', 0)
        .replace('index,follow', 'noindex').replace('href="style.css"','href="/style.css"').replace('src="app.js"','src="/app.js"').replace('src="img/','src="/img/').replace('href="img/','href="/img/').replace('href="#main"','href="#main"'))
    print("OK", len(BT), len(NVL))
