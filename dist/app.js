(function(){var f=document.getElementById('qf');if(f){f.addEventListener('submit',function(e){e.preventDefault();var d=new FormData(f),m=document.getElementById('qfmsg');
if(!d.get('ten').trim()||!d.get('sdt').trim()){m.textContent='Vui lòng nhập họ tên và số điện thoại.';return}
var t='YÊU CẦU BÁO GIÁ SỈ
Họ tên: '+d.get('ten')+'
SĐT: '+d.get('sdt')+'
Là: '+d.get('loai')+'
Tỉnh/thành: '+d.get('tinh')+'
Quan tâm: '+d.get('nd');
if(navigator.clipboard)navigator.clipboard.writeText(t).catch(function(){});m.textContent='Đã chép nội dung. Dán vào Zalo rồi gửi giúp chúng tôi nhé.';window.open('https://zalo.me/0362771650','_blank','noopener')})}
})();(function(){var g=document.getElementById('grid');if(!g)return;var q=document.getElementById('q'),cs=g.parentNode.querySelectorAll('.chip'),f='',
cards=g.querySelectorAll('.card'),em=document.getElementById('empty');function run(){var t=q.value.trim().toLowerCase(),n=0;
cards.forEach(function(c){var ok=(!f||c.dataset.cat===f)&&(!t||c.dataset.name.indexOf(t)>-1);c.hidden=!ok;if(ok)n++});em.hidden=n>0}
q.addEventListener('input',run);cs.forEach(function(b){b.addEventListener('click',function(){cs.forEach(function(x){x.classList.remove('on')});b.classList.add('on');f=b.dataset.f;run()})})})();