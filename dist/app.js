(function(){var g=document.getElementById('grid');if(!g)return;var q=document.getElementById('q'),cs=g.parentNode.querySelectorAll('.chip'),f='',
cards=g.querySelectorAll('.card'),em=document.getElementById('empty');function run(){var t=q.value.trim().toLowerCase(),n=0;
cards.forEach(function(c){var ok=(!f||c.dataset.cat===f)&&(!t||c.dataset.name.indexOf(t)>-1);c.hidden=!ok;if(ok)n++});em.hidden=n>0}
q.addEventListener('input',run);cs.forEach(function(b){b.addEventListener('click',function(){cs.forEach(function(x){x.classList.remove('on')});b.classList.add('on');f=b.dataset.f;run()})})})();