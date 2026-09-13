# -*- coding: utf-8 -*-
import json, io

with io.open('suno.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with io.open('logo.txt', 'r', encoding='utf-8') as f:
    LOGO = f.read().strip()

data_json = json.dumps(data, ensure_ascii=False)
# Prevent any </script> inside the data from closing the script tag early
data_json = data_json.replace('</', '<\\/')

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SUNO · Prompt Explorer</title>
<style>
:root{
  --bg:#08080c;--bg2:#0e0d16;
  --card:rgba(255,255,255,.03);--card-hover:rgba(255,255,255,.055);
  --border:rgba(255,255,255,.09);--border-hover:rgba(139,92,246,.5);
  --text:#eceaf2;--text-dim:#8b8a99;--text-faint:#5c5b68;
  --a1:#8b5cf6;--a2:#ec4899;--a3:#38bdf8;
  --grad:linear-gradient(120deg,#8b5cf6 0%,#ec4899 55%,#f59e0b 120%);
  --radius:14px;
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:'Inter','Segoe UI',system-ui,-apple-system,sans-serif;min-height:100vh;-webkit-font-smoothing:antialiased;overflow-x:hidden}
.bg{position:fixed;inset:0;z-index:-2;background:radial-gradient(900px 500px at 15% -5%,rgba(139,92,246,.22),transparent 60%),radial-gradient(800px 500px at 90% 0%,rgba(236,72,153,.16),transparent 55%),radial-gradient(700px 600px at 50% 120%,rgba(56,189,248,.10),transparent 60%),linear-gradient(180deg,var(--bg) 0%,var(--bg2) 100%)}
.bg::after{content:"";position:absolute;inset:0;background-image:radial-gradient(rgba(255,255,255,.04) 1px,transparent 1px);background-size:26px 26px;mask-image:linear-gradient(180deg,rgba(0,0,0,.5),transparent 70%);-webkit-mask-image:linear-gradient(180deg,rgba(0,0,0,.5),transparent 70%)}
.topbar{position:sticky;top:0;z-index:50;backdrop-filter:blur(18px) saturate(140%);-webkit-backdrop-filter:blur(18px) saturate(140%);background:rgba(8,8,12,.72);border-bottom:1px solid var(--border);padding:12px 20px;display:flex;align-items:center;gap:16px}
.brand{display:flex;flex-direction:column;gap:3px;flex-shrink:0}
.logo{font-family:ui-monospace,'Cascadia Code','Consolas','Courier New',monospace;font-size:9px;line-height:1.05;font-weight:700;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;white-space:pre;filter:drop-shadow(0 0 14px rgba(139,92,246,.35))}
.brand-sub{font-size:9.5px;letter-spacing:.25em;text-transform:uppercase;color:var(--text-faint);font-weight:600}
.right-col{display:flex;flex-direction:column;align-items:flex-end;gap:6px;margin-left:auto}
.controls{display:flex;align-items:center;gap:8px}
.seg{display:inline-flex;background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:11px;padding:3px}
.seg button{border:0;background:transparent;color:var(--text-dim);font:inherit;font-size:13px;font-weight:600;padding:7px 15px;border-radius:8px;cursor:pointer;transition:.2s}
.seg button:hover{color:var(--text)}
.seg button.active{background:var(--grad);color:#fff;box-shadow:0 4px 14px rgba(139,92,246,.4)}
.sort-wrap{position:relative;display:inline-flex;align-items:center}
.sort-wrap select{font:inherit;font-size:13px;font-weight:600;color:var(--text-dim);background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:11px;padding:8px 32px 8px 14px;cursor:pointer;appearance:none;-webkit-appearance:none;transition:.2s}
.sort-wrap select:hover{color:var(--text);border-color:var(--border-hover)}
.sort-wrap select:focus{outline:none;border-color:var(--a1)}
.sort-wrap::after{content:"";position:absolute;right:12px;top:50%;transform:translateY(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-top:5px solid var(--text-faint);pointer-events:none}
.stats{display:flex;gap:14px;align-items:center;font-size:11px;color:var(--text-faint);white-space:nowrap}
.stats b{color:var(--text-dim);font-weight:600}
.stats .dot{color:var(--a1)}
.search{font:inherit;font-size:13px;color:var(--text);background:rgba(255,255,255,.04);border:1px solid var(--border);border-radius:11px;padding:9px 14px;width:200px;transition:.2s}
.search::placeholder{color:var(--text-faint)}
.search:focus{outline:none;border-color:var(--a1);box-shadow:0 0 0 3px rgba(139,92,246,.15);width:240px}
main{padding:10px 26px 60px 58px;max-width:1200px;margin:0 auto}
.letter-divider{display:flex;align-items:center;gap:14px;margin:26px 0 14px;scroll-margin-top:90px}
.letter-divider .letter{font-size:24px;font-weight:800;background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;width:44px;height:44px;display:flex;align-items:center;justify-content:center;border-radius:12px;border:1px solid var(--border);background-color:rgba(255,255,255,.03)}
.letter-divider .line{flex:1;height:1px;background:linear-gradient(90deg,var(--border),transparent)}
.letter-divider .count{font-size:12px;color:var(--text-faint)}
.card{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;margin-bottom:14px;transition:.22s;position:relative;overflow:hidden}
.card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--grad);opacity:0;transition:.22s}
.card:hover{background:var(--card-hover);border-color:var(--border-hover);transform:translateY(-2px)}
.card:hover::before{opacity:1}
.card-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:10px}
.count-badge{font-size:11.5px;font-weight:600;color:var(--text-dim);background:rgba(255,255,255,.05);border:1px solid var(--border);padding:4px 10px;border-radius:20px;white-space:nowrap}
.copy-btn{font:inherit;font-size:12px;font-weight:600;color:#fff;background:var(--grad);border:0;border-radius:9px;padding:7px 13px;cursor:pointer;transition:.2s;white-space:nowrap;display:inline-flex;align-items:center;gap:6px}
.copy-btn:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(139,92,246,.45)}
.copy-btn.copied{background:linear-gradient(120deg,#22c55e,#16a34a)}
.copy-btn.small{padding:5px 9px;font-size:11px}
.prompt-text{font-size:13px;line-height:1.6;color:var(--text-dim);display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden;cursor:pointer;transition:color .2s}
.prompt-text:hover{color:var(--text)}
.prompt-text.expanded{display:block;-webkit-line-clamp:unset}
.prompt-text .hint{color:var(--a1);font-size:11px;font-weight:600;margin-left:6px}
.songs-row{display:flex;gap:9px;overflow-x:auto;padding:6px 2px 4px;margin-top:12px;scrollbar-width:thin}
.song-pill{flex:0 0 auto;width:158px;display:flex;flex-direction:column;gap:5px;padding:11px 13px;background:rgba(255,255,255,.035);border:1px solid var(--border);border-radius:11px;text-decoration:none;color:var(--text);transition:.2s}
.song-pill:hover{background:rgba(139,92,246,.14);border-color:var(--a1);transform:translateY(-2px)}
.song-title{font-size:13px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.song-link{font-size:11px;color:var(--text-faint);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.song-name{font-size:16px;font-weight:700;letter-spacing:-.01em}
.prompts-list{display:flex;flex-direction:column;gap:8px;margin-top:4px}
.prompt-line{display:flex;align-items:flex-start;gap:10px;background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:10px;padding:10px 12px}
.prompt-line .prompt-text{flex:1;-webkit-line-clamp:2}
.links-row{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.links-row a{font-size:12px;font-weight:600;color:var(--a1);text-decoration:none;border:1px solid var(--border);border-radius:8px;padding:5px 10px;transition:.2s}
.links-row a:hover{background:rgba(139,92,246,.14);border-color:var(--a1)}
.empty{text-align:center;padding:80px 20px;color:var(--text-faint)}
.empty .big{font-size:44px;margin-bottom:14px}
footer{text-align:center;padding:30px;color:var(--text-faint);font-size:12px;border-top:1px solid var(--border);margin-left:32px}
.alpha-nav{position:fixed;left:6px;top:126px;z-index:40;display:flex;flex-direction:column;gap:1px;background:rgba(8,8,12,.7);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border:1px solid var(--border);border-radius:10px;padding:6px 4px;opacity:0;pointer-events:none;transition:opacity .3s}
.alpha-nav.visible{opacity:1;pointer-events:auto}
.alpha-nav a{display:flex;align-items:center;justify-content:center;width:20px;height:18px;font-size:9.5px;font-weight:700;color:var(--text-faint);text-decoration:none;border-radius:4px;transition:.15s}
.alpha-nav a:hover{color:var(--text);background:rgba(255,255,255,.06)}
.alpha-nav a.active{color:#fff;background:var(--grad);box-shadow:0 2px 8px rgba(139,92,246,.4)}
.alpha-nav a.disabled{opacity:.3;pointer-events:none}
::-webkit-scrollbar{width:10px;height:10px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(255,255,255,.12);border-radius:10px}
::-webkit-scrollbar-thumb:hover{background:rgba(139,92,246,.4)}
.stats .clickable{cursor:pointer;text-decoration:underline;text-decoration-color:rgba(139,92,246,.4);text-underline-offset:3px;transition:.2s}
.stats .clickable:hover{text-decoration-color:var(--a1)}
.song-overlay{position:fixed;inset:0;z-index:100;background:rgba(4,4,8,.88);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .25s}
.song-overlay.open{opacity:1;pointer-events:auto}
.song-panel{width:92%;max-width:680px;height:88vh;background:rgba(12,12,18,.95);border:1px solid var(--border);border-radius:20px;display:flex;flex-direction:column;overflow:hidden;transform:scale(.96);transition:transform .25s}
.song-overlay.open .song-panel{transform:scale(1)}
.song-panel-head{display:flex;align-items:center;justify-content:space-between;padding:18px 24px;border-bottom:1px solid var(--border);flex-shrink:0}
.song-panel-head h2{font-size:15px;font-weight:700;color:var(--text)}
.song-close{width:32px;height:32px;display:flex;align-items:center;justify-content:center;border:1px solid var(--border);border-radius:8px;background:transparent;color:var(--text-dim);font-size:18px;cursor:pointer;transition:.2s}
.song-close:hover{color:var(--text);border-color:var(--a1);background:rgba(139,92,246,.1)}
.song-list{flex:1;overflow-y:auto;padding:12px 16px}
.song-item{padding:7px 14px;border-radius:8px;transition:.15s}
.song-item:hover{background:rgba(255,255,255,.03)}
.song-item .s-title{font-size:13px;font-weight:500;color:var(--text-dim);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.5;text-decoration:none;transition:.15s;display:block}
.song-item .s-title:hover{color:var(--a1)}
@media(max-width:768px){.topbar{flex-wrap:wrap;padding:12px 16px}.right-col{width:100%;align-items:flex-start}.controls{flex-wrap:wrap}.stats{flex-wrap:wrap;gap:10px}.alpha-nav{display:none}main{padding:8px 16px 50px}.search{width:100%}.song-panel{width:96%;height:92vh;border-radius:16px}}
</style>
</head>
<body>
<div class="bg"></div>
<header class="topbar">
  <div class="brand">
    <pre class="logo" aria-label="SUNO">__LOGO__</pre>
    <div class="brand-sub">Prompt Explorer</div>
  </div>
  <div class="right-col">
    <div class="controls">
      <div class="seg" id="viewToggle">
        <button data-view="prompt" class="active">By Prompt</button>
        <button data-view="song">By Song</button>
      </div>
      <div class="sort-wrap">
        <select id="sortMode" title="Sort order">
          <option value="alpha">A–Z · Alphabetical</option>
          <option value="original">Original Order</option>
          <option value="reverse">Reverse Order</option>
        </select>
      </div>
      <input type="search" id="search" class="search" placeholder="Search prompts or songs…">
    </div>
    <div class="stats" id="stats"></div>
  </div>
</header>
<nav class="alpha-nav" id="alphaNav"></nav>
<main id="content"></main>
<footer>SUNO Prompt Explorer · <span id="footCount"></span></footer>
<div class="song-overlay" id="songOverlay">
  <div class="song-panel">
    <div class="song-panel-head">
      <h2>All Songs</h2>
      <button class="song-close" id="songClose">&times;</button>
    </div>
    <div class="song-list" id="songList"></div>
  </div>
</div>
<script>
const DATA = __DATA__;
const content=document.getElementById('content');
const statsEl=document.getElementById('stats');
const footCount=document.getElementById('footCount');
const sortMode=document.getElementById('sortMode');
const searchEl=document.getElementById('search');

const promptEntries=[];const promptMap=new Map();
const songEntries=[];const songMap=new Map();
DATA.forEach((item,i)=>{
  const p=item.prompt;let pe=promptMap.get(p);
  if(!pe){pe={key:p,songs:[],firstIndex:i,id:promptEntries.length};promptMap.set(p,pe);promptEntries.push(pe);}
  pe.songs.push({title:item.title,link:item.link});
  const t=item.title;let se=songMap.get(t);
  if(!se){se={key:t,prompts:[],links:[],firstIndex:i,id:songEntries.length,_ps:new Set()};songMap.set(t,se);songEntries.push(se);}
  se.links.push(item.link);
  if(!se._ps.has(p)){se._ps.add(p);se.prompts.push(p);}
});

let state={view:'prompt',sort:'alpha',query:''};
function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function firstLetter(s){for(const ch of s){if(/[a-z]/i.test(ch))return ch.toUpperCase();}return '#';}
function sortEntries(entries,sort){const arr=entries.slice();if(sort==='alpha'){arr.sort((a,b)=>{const la=firstLetter(a.key),lb=firstLetter(b.key);if(la!==lb)return la<lb?-1:1;return a.key.localeCompare(b.key);});}else if(sort==='original'){arr.sort((a,b)=>a.firstIndex-b.firstIndex);}else{arr.sort((a,b)=>b.firstIndex-a.firstIndex);}return arr;}

function promptCard(e){
  const songs=e.songs.map(s=>'<a class="song-pill" href="'+esc(s.link)+'" target="_blank" rel="noopener"><span class="song-title">'+esc(s.title)+'</span><span class="song-link">suno.com ↗</span></a>').join('');
  const long=e.key.length>160;
  return '<article class="card"><div class="card-head"><span class="count-badge">'+e.songs.length+' song'+(e.songs.length>1?'s':'')+'</span><button class="copy-btn" data-pid="'+e.id+'">⧉ Copy prompt</button></div><p class="prompt-text" data-expand>'+esc(e.key)+(long?'<span class="hint">click to expand</span>':'')+'</p><div class="songs-row">'+songs+'</div></article>';
}
function songCard(e){
  const prompts=e.prompts.map(p=>{const pid=promptMap.get(p).id;return '<div class="prompt-line"><span class="prompt-text" data-expand>'+esc(p)+'</span><button class="copy-btn small" data-pid="'+pid+'">⧉ Copy</button></div>';}).join('');
  const links=e.links.map(l=>'<a href="'+esc(l)+'" target="_blank" rel="noopener">↗ version</a>').join('');
  return '<article class="card"><div class="card-head"><h3 class="song-name">'+esc(e.key)+'</h3><span class="count-badge">'+e.prompts.length+' prompt'+(e.prompts.length>1?'s':'')+' · '+e.links.length+' version'+(e.links.length>1?'s':'')+'</span></div><div class="prompts-list">'+prompts+'</div><div class="links-row">'+links+'</div></article>';
}
function emptyState(msg){return '<div class="empty"><div class="big">🎵</div><div>'+(msg||'No matches found')+'</div></div>';}

function renderByPrompt(){
  let entries=promptEntries;
  if(state.query){const q=state.query.toLowerCase();entries=entries.filter(e=>e.key.toLowerCase().includes(q)||e.songs.some(s=>s.title.toLowerCase().includes(q)));}
  entries=sortEntries(entries,state.sort);
  let html='';let cur=null;let counts={};
  if(state.sort==='alpha'){entries.forEach(e=>{const l=firstLetter(e.key);counts[l]=(counts[l]||0)+1;});}
  for(const e of entries){
    if(state.sort==='alpha'){const l=firstLetter(e.key);if(l!==cur){cur=l;html+='<div class="letter-divider" id="letter-'+l+'" data-letter="'+l+'"><span class="letter">'+esc(l)+'</span><span class="line"></span><span class="count">'+counts[l]+' prompt'+(counts[l]>1?'s':'')+'</span></div>';}}
    html+=promptCard(e);
  }
  content.innerHTML=html||emptyState();bindInteractions();
}
function renderBySong(){
  let entries=songEntries;
  if(state.query){const q=state.query.toLowerCase();entries=entries.filter(e=>e.key.toLowerCase().includes(q)||e.prompts.some(p=>p.toLowerCase().includes(q)));}
  entries=sortEntries(entries,state.sort);
  let html='';let cur=null;
  for(const e of entries){
    if(state.sort==='alpha'){const l=firstLetter(e.key);if(l!==cur){cur=l;html+='<div class="letter-divider"><span class="letter">'+esc(l)+'</span><span class="line"></span></div>';}}
    html+=songCard(e);
  }
  content.innerHTML=html||emptyState();bindInteractions();
}
function bindInteractions(){
  content.querySelectorAll('.copy-btn').forEach(btn=>{
    btn.onclick=()=>{
      const text=promptEntries[btn.dataset.pid].key;
      const done=()=>{if(btn.dataset.orig===undefined)btn.dataset.orig=btn.innerHTML;btn.innerHTML='✓ Copied';btn.classList.add('copied');setTimeout(()=>{btn.innerHTML=btn.dataset.orig;btn.classList.remove('copied');},1300);};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(text).then(done).catch(done);}
      else{const ta=document.createElement('textarea');ta.value=text;document.body.appendChild(ta);ta.select();try{document.execCommand('copy');}catch(e){}document.body.removeChild(ta);done();}
    };
  });
  content.querySelectorAll('[data-expand]').forEach(el=>{el.onclick=()=>el.classList.toggle('expanded');});
}
function renderStats(){
  statsEl.innerHTML='<span class="clickable" id="songCountBtn"><b>'+DATA.length.toLocaleString()+'</b> songs</span><span class="dot">•</span><span><b>'+promptEntries.length.toLocaleString()+'</b> unique prompts</span><span class="dot">•</span><span><b>'+songEntries.length.toLocaleString()+'</b> unique song titles</span>';
  footCount.textContent=DATA.length.toLocaleString()+' songs · '+promptEntries.length.toLocaleString()+' unique prompts';
}
function render(){if(state.view==='prompt')renderByPrompt();else renderBySong();}
document.querySelectorAll('#viewToggle button').forEach(b=>{b.onclick=()=>{document.querySelectorAll('#viewToggle button').forEach(x=>x.classList.remove('active'));b.classList.add('active');state.view=b.dataset.view;render();};});
sortMode.onchange=()=>{state.sort=sortMode.value;render();};
searchEl.oninput=()=>{state.query=searchEl.value.trim();render();};
renderStats();render();

// Song overlay
const songOverlay=document.getElementById('songOverlay');
const songList=document.getElementById('songList');
const songClose=document.getElementById('songClose');
let songListBuilt=false;
function buildSongList(){
  if(songListBuilt)return;
  songListBuilt=true;
  let html='';
  const entries=[...songEntries].reverse();
  entries.forEach(e=>{
    const t=(e.key||'Untitled').replace(/</g,'&lt;');
    const l=(e.links&&e.links[0]||'');
    if(l){html+='<div class="song-item"><a class="s-title" href="'+l.replace(/"/g,'&quot;')+'" target="_blank" rel="noopener">'+t+'</a></div>';}else{html+='<div class="song-item"><span class="s-title">'+t+'</span></div>';}
  });
  songList.innerHTML=html;
}
document.getElementById('songCountBtn').onclick=()=>{
  buildSongList();
  songOverlay.classList.add('open');
  document.body.style.overflow='hidden';
};
songClose.onclick=()=>{
  songOverlay.classList.remove('open');
  document.body.style.overflow='';
};
songOverlay.onclick=(e)=>{
  if(e.target===songOverlay){
    songOverlay.classList.remove('open');
    document.body.style.overflow='';
  }
};
document.addEventListener('keydown',(e)=>{
  if(e.key==='Escape'&&songOverlay.classList.contains('open')){
    songOverlay.classList.remove('open');
    document.body.style.overflow='';
  }
});

// Alphabet navigation
const alphaNav=document.getElementById('alphaNav');
const letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'.split('');
let alphaSet=new Set();
function buildAlphaNav(){
  alphaSet=new Set();
  if(state.view==='prompt'&&state.sort==='alpha'){
    promptEntries.forEach(e=>{const c=e.key.trim().charAt(0).toUpperCase();if(c>='A'&&c<='Z')alphaSet.add(c);});
  }
  let html='';
  letters.forEach(l=>{
    const dis=alphaSet.size>0&&!alphaSet.has(l);
    html+='<a href="#letter-'+l+'" data-letter="'+l+'" class="'+(dis?'disabled':'')+'">'+l+'</a>';
  });
  alphaNav.innerHTML=html;
  alphaNav.classList.toggle('visible',alphaSet.size>0);
  alphaNav.querySelectorAll('a:not(.disabled)').forEach(a=>{
    a.onclick=(e)=>{e.preventDefault();const t=document.getElementById('letter-'+a.dataset.letter);if(t)t.scrollIntoView({behavior:'smooth',block:'start'});};
  });
}
function updateAlphaActive(){
  if(!alphaNav.classList.contains('visible'))return;
  const dividers=document.querySelectorAll('.letter-divider');
  let active=null;
  dividers.forEach(d=>{
    if(d.getBoundingClientRect().top<=80)active=d.dataset.letter;
  });
  alphaNav.querySelectorAll('a').forEach(a=>{
    a.classList.toggle('active',a.dataset.letter===active);
  });
}
window.addEventListener('scroll',updateAlphaActive,{passive:true});
const origRender=render;
render=function(){origRender();buildAlphaNav();updateAlphaActive();};
render();
</script>
</body>
</html>
"""

html = TEMPLATE.replace('__LOGO__', LOGO).replace('__DATA__', data_json)

with io.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Generated index.html')
print('  total items        :', len(data))
print('  unique prompts     :', len(set(d['prompt'] for d in data)))
print('  unique song titles :', len(set(d['title'] for d in data)))
print('  output size (MB)   :', round(len(html.encode('utf-8'))/1024/1024, 2))
