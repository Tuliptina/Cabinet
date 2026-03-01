"""
🗄️ The Fitzroy Cabinet — 3D Renderer
Three.js r160 interactive cabinet with PBR materials,
unique bottle shapes, UV mode, and click interactions.

BUG FIXES IMPLEMENTED:
- Explicitly disabled physical light decay (`decay=0`) to prevent the cabinet from rendering entirely dim/black in r160.
"""

def get_cabinet_3d(mode: str = "gaslight", intensity: int = 3) -> str:
    colors = {
        "gaslight": {
            "bg": 0x0a0705, "ambient": 0x332211, "wood": 0x3d2817, "wood_dark": 0x1f120a,
            "brass": 0xb8860b, "glass": 0x88aacc, "cloth": 0xddddcc, "light_color": 0xffa040,
            "light_int": 1.0, "fog": 0x0a0705, "text_color": "#d4a574",
            "candle": 0xffa040, "shelf_color": 0x2c1810, "velvet": 0x2a0a0a,
        },
        "gothic": {
            "bg": 0x050505, "ambient": 0x110a0a, "wood": 0x1a0808, "wood_dark": 0x0a0303,
            "brass": 0x444444, "glass": 0x668888, "cloth": 0x770000, "light_color": 0xff3311,
            "light_int": 1.2, "fog": 0x050505, "text_color": "#cc0000",
            "candle": 0xff4422, "shelf_color": 0x1a0505, "velvet": 0x330000,
        },
        "clinical": {
            "bg": 0xcccccc, "ambient": 0x778899, "wood": 0x999988, "wood_dark": 0x777766,
            "brass": 0x99aacc, "glass": 0xaaccee, "cloth": 0xffffff, "light_color": 0xffffff,
            "light_int": 1.2, "fog": 0xcccccc, "text_color": "#2f4f4f",
            "candle": 0xffffff, "shelf_color": 0xbbbbaa, "velvet": 0x888888,
        }
    }
    c = colors.get(mode, colors["gaslight"])

    def hx(v):
        return f"0x{v:06x}"

    flicker = 0.04 + intensity * 0.03
    particle_count = 40 + intensity * 20
    creep = intensity / 5.0

    html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:100%;height:100%;overflow:hidden;background:#{c["bg"]:06x};font-family:Georgia,serif}}
#container{{width:100%;height:100%;position:relative;cursor:grab}}
#container:active{{cursor:grabbing}}
canvas{{display:block;width:100%!important;height:100%!important}}
#info{{position:absolute;bottom:15px;left:50%;transform:translateX(-50%);color:{c["text_color"]};font-size:12px;text-align:center;opacity:0.6;pointer-events:none;z-index:100}}
#mode-label{{position:absolute;top:15px;left:15px;color:{c["text_color"]};font-size:10px;text-transform:uppercase;letter-spacing:3px;opacity:0.5;pointer-events:none;z-index:100}}
#uv-btn{{position:absolute;top:15px;right:15px;background:rgba(0,0,0,0.7);color:{c["text_color"]};border:1px solid {c["text_color"]}44;padding:8px 16px;font-family:Georgia,serif;font-size:11px;cursor:pointer;z-index:200;letter-spacing:2px;text-transform:uppercase}}
#uv-btn:hover{{border-color:{c["text_color"]}}}
#uv-btn.active{{background:rgba(60,0,80,0.9);color:#bb88ff;border-color:#8844aa}}
#tooltip{{position:absolute;background:rgba(0,0,0,0.92);color:{c["text_color"]};padding:14px 18px;border-radius:4px;font-size:13px;max-width:320px;line-height:1.6;pointer-events:none;opacity:0;transition:opacity 0.3s;z-index:300;border:1px solid {c["text_color"]}33}}
#tooltip.visible{{opacity:1}}
#tooltip .tt-name{{font-weight:bold;font-size:14px;margin-bottom:4px}}
#tooltip .tt-sub{{font-style:italic;opacity:0.7;font-size:11px;margin-bottom:8px}}
#tooltip .tt-desc{{margin-bottom:8px}}
#tooltip .tt-secret{{border-top:1px solid {c["text_color"]}22;padding-top:8px;font-style:italic;opacity:0.85}}
#tooltip .tt-uv{{color:#bb88ff;border-top:1px solid #8844aa44;padding-top:8px;font-family:monospace;font-size:11px}}
.vignette{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;background:radial-gradient(ellipse at center,transparent 40%,rgba(0,0,0,{0.6+creep*0.15 if mode!='clinical' else 0.1}) 100%);z-index:50}}
</style></head><body>
<div id="container"></div>
<div class="vignette"></div>
<div id="mode-label">{mode.upper()}</div>
<button id="uv-btn" onclick="toggleUV()">🔦 UV Light</button>
<div id="info">Drag to orbit · Scroll to zoom · Click to examine</div>
<div id="tooltip"><div class="tt-name"></div><div class="tt-sub"></div><div class="tt-desc"></div><div class="tt-secret"></div><div class="tt-uv"></div></div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.min.js"></script>
<script>
(function(){{
'use strict';
const MODE='{mode}', INTENSITY={intensity}, CREEP={creep};
let uvMode=false;
const clickable=[];
const container=document.getElementById('container');
const W=container.clientWidth||window.innerWidth;
const H=container.clientHeight||window.innerHeight;

// Scene
const scene=new THREE.Scene();
scene.background=new THREE.Color({hx(c["bg"])});
scene.fog=new THREE.FogExp2({hx(c["fog"])}, 0.012);

const camera=new THREE.PerspectiveCamera(45,W/H,0.1,100);
camera.position.set(0, 2.5, 5.5);
camera.lookAt(0,2,0);

const renderer=new THREE.WebGLRenderer({{antialias:true,powerPreference:"high-performance"}});
renderer.setSize(W,H);
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.shadowMap.enabled=true;
renderer.shadowMap.type=THREE.PCFSoftShadowMap;
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.8;
container.appendChild(renderer.domElement);

const raycaster=new THREE.Raycaster();

// Materials
const woodMat=new THREE.MeshStandardMaterial({{color:{hx(c["wood"])},roughness:0.85,metalness:0.1}});
const darkWoodMat=new THREE.MeshStandardMaterial({{color:{hx(c["wood_dark"])},roughness:0.9,metalness:0.05}});
const brassMat=new THREE.MeshStandardMaterial({{color:{hx(c["brass"])},roughness:0.35,metalness:0.85}});
const glassMat=new THREE.MeshStandardMaterial({{color:{hx(c["glass"])},roughness:0.1,metalness:0.0,transparent:true,opacity:0.15}});
const velvetMat=new THREE.MeshStandardMaterial({{color:{hx(c["velvet"])},roughness:1.0}});
const shelfMat=new THREE.MeshStandardMaterial({{color:{hx(c["shelf_color"])},roughness:0.8,metalness:0.05}});
const corkMat=new THREE.MeshStandardMaterial({{color:0x8b7355,roughness:0.95}});
const labelMat=new THREE.MeshStandardMaterial({{color:0xfffff0,roughness:0.9}});
const waxRedMat=new THREE.MeshStandardMaterial({{color:0x8b0000,roughness:0.6}});
const steelMat=new THREE.MeshStandardMaterial({{color:0xaaaaaa,roughness:0.3,metalness:0.9}});
const ivoryMat=new THREE.MeshStandardMaterial({{color:0xfffff0,roughness:0.5,metalness:0.1}});

// ==================== LIGHTING (DECAY=0 FIX) ====================

scene.add(new THREE.AmbientLight({hx(c["ambient"])},{c["light_int"]*1.5}));

// Key light from above-front. Setting decay to 0 overrides the default dark falloff.
const keyLight=new THREE.SpotLight({hx(c["light_color"])},{c["light_int"]*20},15,Math.PI/5,0.7,0);
keyLight.position.set(1,6,4);
keyLight.target.position.set(0,2,0);
keyLight.castShadow=true;
scene.add(keyLight); scene.add(keyLight.target);

// Fill light from left (decay: 0)
const fillLight=new THREE.PointLight({hx(c["light_color"])},{c["light_int"]*8},12,0);
fillLight.position.set(-4,3,2);
scene.add(fillLight);

// Rim light from behind (decay: 0)
const rimLight=new THREE.PointLight({hx(c["ambient"])},{c["light_int"]*4},10,0);
rimLight.position.set(0,4,-3);
scene.add(rimLight);

// Candle on top of cabinet (decay: 0)
const candleLight=new THREE.PointLight({hx(c["candle"])},{c["light_int"]*6},8,0);
candleLight.position.set(0.4,4.8,0.2);
scene.add(candleLight);

const uvLight=new THREE.PointLight(0x6600aa,0,12,0);
uvLight.position.set(0,3,3);
scene.add(uvLight);

// ==================== CABINET BODY ====================
const CAB_W=3.2, CAB_H=4.5, CAB_D=1.2;
const cabinet=new THREE.Group();

// Back panel
const back=new THREE.Mesh(new THREE.BoxGeometry(CAB_W,CAB_H,0.08),darkWoodMat);
back.position.set(0,CAB_H/2,-CAB_D/2+0.04);
back.receiveShadow=true;
cabinet.add(back);

// Side panels
[-1,1].forEach(side=>{{
    const panel=new THREE.Mesh(new THREE.BoxGeometry(0.08,CAB_H,CAB_D),darkWoodMat);
    panel.position.set(side*(CAB_W/2-0.04),CAB_H/2,0);
    panel.castShadow=true;
    cabinet.add(panel);
}});

// Bottom
const bottom=new THREE.Mesh(new THREE.BoxGeometry(CAB_W,0.08,CAB_D),woodMat);
bottom.position.set(0,0.04,0);
bottom.receiveShadow=true;
cabinet.add(bottom);

// Top
const top=new THREE.Mesh(new THREE.BoxGeometry(CAB_W+0.1,0.1,CAB_D+0.1),woodMat);
top.position.set(0,CAB_H+0.05,0);
top.castShadow=true;
cabinet.add(top);

// Crown molding
const crown=new THREE.Mesh(new THREE.BoxGeometry(CAB_W+0.2,0.15,CAB_D+0.15),woodMat);
crown.position.set(0,CAB_H+0.18,0);
cabinet.add(crown);
const crownTop=new THREE.Mesh(new THREE.BoxGeometry(CAB_W+0.05,0.06,CAB_D+0.05),woodMat);
crownTop.position.set(0,CAB_H+0.3,0);
cabinet.add(crownTop);

// Base plinth
const plinth=new THREE.Mesh(new THREE.BoxGeometry(CAB_W+0.15,0.12,CAB_D+0.1),woodMat);
plinth.position.set(0,-0.06,0);
cabinet.add(plinth);

// Feet (4 ball feet)
[[-1,-1],[1,-1],[-1,1],[1,1]].forEach(p=>{{
    const foot=new THREE.Mesh(new THREE.SphereGeometry(0.08,8,6),brassMat);
    foot.position.set(p[0]*(CAB_W/2-0.15),-0.18,p[1]*(CAB_D/2-0.1));
    cabinet.add(foot);
}});

// ==================== SHELVES ====================
const shelfPositions=[0.6, 1.6, 2.6, 3.6];
shelfPositions.forEach((y,i)=>{{
    const shelf=new THREE.Mesh(new THREE.BoxGeometry(CAB_W-0.2,0.06,CAB_D-0.15),shelfMat);
    shelf.position.set(0,y,0);
    shelf.receiveShadow=true;
    cabinet.add(shelf);
}});

// Velvet liner on each shelf
shelfPositions.forEach(y=>{{
    const liner=new THREE.Mesh(new THREE.PlaneGeometry(CAB_W-0.25,CAB_D-0.2),velvetMat);
    liner.rotation.x=-Math.PI/2;
    liner.position.set(0,y+0.035,0);
    cabinet.add(liner);
}});

// ==================== GLASS DOORS ====================
// Left door (slightly ajar)
const leftDoor=new THREE.Group();
const leftGlass=new THREE.Mesh(new THREE.BoxGeometry(CAB_W/2-0.1,CAB_H-0.2,0.04),glassMat);
leftGlass.position.set((CAB_W/2-0.1)/2-0.02,CAB_H/2,0);
leftDoor.add(leftGlass);
// Door frame
const leftFrame=new THREE.Mesh(new THREE.BoxGeometry(0.06,CAB_H-0.2,0.06),brassMat);
leftFrame.position.set(0,CAB_H/2,0);
leftDoor.add(leftFrame);
const leftFrameR=new THREE.Mesh(new THREE.BoxGeometry(0.04,CAB_H-0.2,0.06),brassMat);
leftFrameR.position.set(CAB_W/2-0.15,CAB_H/2,0);
leftDoor.add(leftFrameR);
leftDoor.position.set(-CAB_W/2+0.1,0,CAB_D/2);
leftDoor.rotation.y=0.25;
cabinet.add(leftDoor);

// Right door (more open)
const rightDoor=new THREE.Group();
const rightGlass=new THREE.Mesh(new THREE.BoxGeometry(CAB_W/2-0.1,CAB_H-0.2,0.04),glassMat);
rightGlass.position.set(-(CAB_W/2-0.1)/2+0.02,CAB_H/2,0);
rightDoor.add(rightGlass);
const rightFrame=new THREE.Mesh(new THREE.BoxGeometry(0.06,CAB_H-0.2,0.06),brassMat);
rightFrame.position.set(0,CAB_H/2,0);
rightDoor.add(rightFrame);
const rightFrameL=new THREE.Mesh(new THREE.BoxGeometry(0.04,CAB_H-0.2,0.06),brassMat);
rightFrameL.position.set(-CAB_W/2+0.15,CAB_H/2,0);
rightDoor.add(rightFrameL);
rightDoor.position.set(CAB_W/2-0.1,0,CAB_D/2);
rightDoor.rotation.y=-0.4;
cabinet.add(rightDoor);

// Door handles
[-0.15,0.15].forEach(x=>{{
    const handle=new THREE.Mesh(new THREE.SphereGeometry(0.035,8,6),brassMat);
    handle.position.set(x,CAB_H/2,CAB_D/2+0.08);
    cabinet.add(handle);
}});

// Lock plate
const lockPlate=new THREE.Mesh(new THREE.BoxGeometry(0.06,0.1,0.02),brassMat);
lockPlate.position.set(0,CAB_H/2-0.3,CAB_D/2+0.05);
cabinet.add(lockPlate);
const keyhole=new THREE.Mesh(new THREE.CircleGeometry(0.012,8),new THREE.MeshBasicMaterial({{color:0x000000}}));
keyhole.position.set(0,CAB_H/2-0.3,CAB_D/2+0.065);
cabinet.add(keyhole);

// ==================== CANDLE ON TOP ====================
const candleGroup=new THREE.Group();
const candleHolder=new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.08,0.04,8),brassMat);
candleGroup.add(candleHolder);
const candleDish=new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.1,0.02,12),brassMat);
candleDish.position.y=-0.01;
candleGroup.add(candleDish);
const candleWax=new THREE.Mesh(new THREE.CylinderGeometry(0.025,0.03,0.2,8),new THREE.MeshStandardMaterial({{color:0xfffff0,roughness:0.6}}));
candleWax.position.y=0.12;
candleGroup.add(candleWax);
const flame=new THREE.Mesh(new THREE.SphereGeometry(0.02,6,4),new THREE.MeshBasicMaterial({{color:{hx(c["candle"])},transparent:true,opacity:0.9}}));
flame.position.y=0.24;
flame.scale.set(1,1.5,1);
candleGroup.add(flame);
// Wax drips
for(let i=0;i<3;i++){{
    const drip=new THREE.Mesh(new THREE.SphereGeometry(0.008,4,4),new THREE.MeshStandardMaterial({{color:0xfffff0,roughness:0.6}}));
    drip.position.set(Math.cos(i*2.1)*0.035,0.03+i*0.03,Math.sin(i*2.1)*0.035);
    drip.scale.y=1.5;
    candleGroup.add(drip);
}}
candleGroup.position.set(0.4,CAB_H+0.35,0.15);
cabinet.add(candleGroup);

scene.add(cabinet);

// ==================== BOTTLE DATA ====================
const bottles=[
  {{id:'laudanum',name:'Laudanum',sub:'Tinctura Opii',shelf:0,x:-1.1,color:0xb8860b,liquid:0x8b4513,shape:'tall',
    desc:'An alcoholic solution of opium. The most prescribed medicine of the age.',
    secret:'Batch 7 — modified concentration for Subject C (Sebastian Carlisle).',
    uv:'CARLISLE PROTOCOL — 3x STANDARD'}},
  {{id:'chloroform',name:'Chloroform',sub:'Chloroformum',shelf:0,x:-0.55,color:0x2d5a27,liquid:0x1a3a15,shape:'wide',
    desc:'A volatile anaesthetic. Sweet-smelling and treacherous.',
    secret:'A cloth beside the bottle smells faintly sweet. Someone used this recently.',
    uv:'SEE INCIDENT LOG — NOV 12'}},
  {{id:'mercury',name:'Mercuric Chloride',sub:'Hydrargyri Chloridum',shelf:0,x:0.0,color:0x1a3a6a,liquid:0xc0c0c0,shape:'round',
    desc:'A heavy blue bottle sealed with black wax. For the treatment of syphilis.',
    secret:'The wax seal has been broken and resealed multiple times.',
    uv:'BLACKWOOD — PERSONAL USE'}},
  {{id:'ether',name:'Diethyl Ether',sub:'Aether Sulfuricus',shelf:0,x:0.55,color:0xd4d4c8,liquid:0xeeeedd,shape:'jar',
    desc:'A wide-mouth jar with cloth draped over it. The air shimmers above.',
    secret:'The cloth is stained with something other than ether. Blood, perhaps.',
    uv:'FLAMMABLE — STORE AWAY FROM GAS'}},
  {{id:'belladonna',name:'Belladonna',sub:'Atropa Belladonna',shelf:0,x:1.1,color:0x3d1f5a,liquid:0x2a0a3a,shape:'elegant',
    desc:'An elegant purple bottle. Named for its cosmetic use dilating pupils.',
    secret:'Isabella used belladonna drops before every ritual.',
    uv:'ORDER OF THE CRIMSON VEIL'}},
  {{id:'smelling_salts',name:'Smelling Salts',sub:'Ammonium Carbonate',shelf:0,x:0.85,color:0xe8e4dc,liquid:null,shape:'crystal',
    desc:'A cut-glass bottle with a silver cap. For reviving the faint.',
    secret:'In the anatomy theatre, the question is: who needed reviving, and from what?',
    uv:null}},
  {{id:'strychnine',name:'Strychnine',sub:'Nux Vomica',shelf:1,x:-1.1,color:0x8b0000,liquid:0x4a0000,shape:'tiny',
    desc:'A tiny red bottle with a locked cap. Deceptively small.',
    secret:'The lock has scratch marks. Someone tried to open it without the key.',
    uv:'SCHEDULE I — LOCKED ACCESS ONLY'}},
  {{id:'arsenic_wafers',name:'Arsenic Wafers',sub:"Dr. Mackenzie's Tablets",shelf:1,x:-0.55,color:0xf5f0e0,liquid:null,shape:'tin',
    desc:"'For a Pale and Luminous Complexion.' Women ate these willingly.",
    secret:"Found in Beatrice Whitmore's effects after her death.",
    uv:'EVIDENCE — PWS CASE FILE #7'}},
  {{id:'dovers_powder',name:"Dover's Powder",sub:'Pulvis Ipecacuanhae',shelf:1,x:0.0,color:0x654321,liquid:0x8b7355,shape:'tall',
    desc:'Opium combined with ipecac. Standard Victorian pharmacy.',
    secret:'The label has been altered. A higher dosage in different handwriting.',
    uv:'DOSAGE MODIFIED — WHO?'}},
  {{id:'paregoric',name:'Paregoric',sub:'Camphorated Tincture of Opium',shelf:1,x:0.55,color:0xc49a6c,liquid:0xa0724a,shape:'small',
    desc:"'For the quieting of infants.' The label shows a sleeping child.",
    secret:'One of the tainted bottles. Laudanum concentration is 3x the labeled amount.',
    uv:'RED ROSE SUPPLY CHAIN — LOT 34B'}},
  {{id:'fitzroy_tonic',name:"Fitzroy's Tonic",sub:'Patent Pediatric Formula',shelf:1,x:1.1,color:0x2a4a2a,liquid:0x3a6a3a,shape:'pro',
    desc:"'Fitzroy Pediatric Compound — Safe for All Ages.'",
    secret:'Two versions exist. One saves lives. The other contains sterilizing agents.',
    uv:'BATCH 12-A — VERIFY DISTRIBUTION'}},
  {{id:'distilled_blood',name:'Distilled Blood Serum',sub:'Experimental — Restricted',shelf:3,x:0.9,color:0x4a0000,liquid:0x8b0000,shape:'vial',
    desc:'A dark vial in a leather case. The liquid inside is unmistakable.',
    secret:"Sebastian's addiction. His chain. What keeps him alive and what is killing him.",
    uv:'WARREN PROTOCOL — EYES ONLY'}},
];

// Instruments
const instruments=[
  {{id:'scarificator',name:'Scarificator',shelf:2,x:-1.2,
    desc:'A spring-loaded brass device with twelve concealed blades.',
    secret:"Engraved 'E.F.' — Edmund Fitzroy. Passed from father to son.",
    uv:'PROPERTY OF DR. EDMUND FITZROY'}},
  {{id:'leech_jar',name:'Leech Jar',shelf:2,x:-0.7,
    desc:'A tall glass vessel with a perforated lid. Something moves inside.',
    secret:'The leeches are alive. Someone has been feeding them. Fresh blood in the water.',
    uv:'ACTIVE — MAINTAIN WEEKLY'}},
  {{id:'trephine',name:'Trephination Drill',shelf:2,x:-0.2,
    desc:'A hand-cranked brass drill with a circular blade. For cutting through skull bone.',
    secret:'The blade is sharper than standard. Maintained with unusual care.',
    uv:null}},
  {{id:'amputation_saw',name:'Amputation Saw',shelf:2,x:0.3,
    desc:'A compact bone saw with an ivory handle. The handle is stained dark.',
    secret:'The ivory handle bears teeth marks. Someone gripped this in agony.',
    uv:'3 OPERATIONS — DATES RECORDED'}},
  {{id:'syringe',name:'Hypodermic Syringe',shelf:2,x:0.7,
    desc:'Early model. Glass barrel, silver fittings, a fine needle.',
    secret:'The barrel has residue — a compound not found in any pharmacopoeia.',
    uv:'CARLISLE DOSING SCHEDULE'}},
  {{id:'scalpel_set',name:'Scalpel Set',shelf:2,x:1.2,
    desc:'Seven scalpels on a leather roll. One slot is empty.',
    secret:'The third scalpel has been missing for six weeks. No one reported it.',
    uv:'BLADE #3 — MISSING SINCE OCT 4'}},
];

// Specimens
const specimens=[
  {{id:'heart_jar',name:'Heart in Formaldehyde',sub:'Subject 23',shelf:3,x:-1.1,
    jar:0xaaddaa, liquid:0x88bb88,
    desc:"A human heart suspended in pale green fluid. Label: 'Subject 23.'",
    secret:'Never a donated cadaver. The Anatomy Club paid grave robbers.',
    uv:'PROCUREMENT: IRREGULAR'}},
  {{id:'brain_section',name:'Brain Cross-Section',shelf:3,x:-0.5,
    jar:0xccbbaa, liquid:0xaa9988,
    desc:'A horizontal slice of brain tissue pressed between glass plates.',
    secret:"Fitzroy's notes call the temporal adhesion 'the seat of vision.'",
    uv:'DEMENTIA STUDY — SEE NOTES'}},
  {{id:'blood_rack',name:'Blood Sample Rack',sub:'12 Specimens',shelf:3,x:0.1,
    jar:0xaa0000, liquid:0x8b0000,
    desc:'A wooden rack holding twelve small glass vials of blood.',
    secret:"Seven vials labeled 'S.C.' — documenting Sebastian's captivity.",
    uv:'S.C. LONGITUDINAL STUDY'}},
];

// Personal items
const personal=[
  {{id:'notebook',name:"Fitzroy's Notebook",shelf:3,x:-1.2,
    desc:"Leather-bound, monogrammed 'A.F.' Dense with formulae.",
    secret:"Page 47: a formula for an unknown compound. Margin: 'It works.'",
    uv:'ENCODED PAGES — USE CIPHER KEY'}},
  {{id:'locket',name:'A Locket',shelf:3,x:1.2,
    desc:'A small gold locket on a broken chain. Torn from someone.',
    secret:'Inside: a miniature portrait. She resembles Alistair. His mother.',
    uv:'ELEANOR FITZROY — 1829-1869'}},
  {{id:'red_rose_seal',name:'Red Rose Seal',shelf:3,x:0.5,
    desc:'A heavy brass stamp depicting a crimson rose.',
    secret:'Each petal encodes a membership tier. Fitzroy keeps it here, not the vault.',
    uv:'TIER III — COUNCIL ACCESS'}},
];

// ==================== BOTTLE CREATION ====================
function makeBottle(b, shelfY, zOff){{
    const g=new THREE.Group();
    const bH=b.shape==='tiny'?0.22:b.shape==='jar'?0.28:b.shape==='tin'?0.18:b.shape==='crystal'?0.3:b.shape==='vial'?0.25:b.shape==='small'?0.28:b.shape==='pro'?0.42:b.shape==='elegant'?0.38:b.shape==='wide'?0.3:0.38;
    const bW=b.shape==='jar'?0.14:b.shape==='wide'?0.1:b.shape==='round'?0.1:b.shape==='tin'?0.14:b.shape==='tiny'?0.04:b.shape==='crystal'?0.06:b.shape==='vial'?0.04:b.shape==='small'?0.06:b.shape==='pro'?0.08:b.shape==='elegant'?0.06:0.07;
    const neckH=b.shape==='tin'?0:b.shape==='jar'?0.02:b.shape==='crystal'?0.05:0.08;
    const neckW=b.shape==='jar'?bW*0.8:bW*0.4;
    
    // Glass bottle body
    const glassBMat=new THREE.MeshStandardMaterial({{
        color:b.color, roughness:0.15, metalness:0.05, transparent:true,
        opacity:b.shape==='tin'?0.95:0.55
    }});

    let bodyGeo;
    if(b.shape==='round'){{
        bodyGeo=new THREE.SphereGeometry(bW,12,10);
    }}else if(b.shape==='tin'){{
        bodyGeo=new THREE.BoxGeometry(bW*2,bH,bW*1.5);
    }}else if(b.shape==='crystal'){{
        bodyGeo=new THREE.CylinderGeometry(bW,bW,bH,8);
    }}else if(b.shape==='elegant'){{
        bodyGeo=new THREE.CylinderGeometry(bW*0.7,bW,bH,10);
    }}else{{
        bodyGeo=new THREE.CylinderGeometry(bW,bW*1.05,bH,12);
    }}
    const body=new THREE.Mesh(bodyGeo,glassBMat);
    body.position.y=bH/2;
    body.castShadow=true;
    g.add(body);

    // Liquid inside
    if(b.liquid){{
        const liqH=bH*0.7;
        const liqMat=new THREE.MeshStandardMaterial({{
            color:b.liquid, roughness:0.2, metalness:0.1, transparent:true, opacity:0.7
        }});
        let liqGeo;
        if(b.shape==='round'){{
            liqGeo=new THREE.SphereGeometry(bW*0.85,10,8);
        }}else if(b.shape==='tin'){{
            liqGeo=null;
        }}else{{
            liqGeo=new THREE.CylinderGeometry(bW*0.85,bW*0.9,liqH,10);
        }}
        if(liqGeo){{
            const liq=new THREE.Mesh(liqGeo,liqMat);
            liq.position.y=liqH/2-0.02;
            g.add(liq);
        }}
    }}

    // Neck
    if(neckH>0 && b.shape!=='tin'){{
        const neck=new THREE.Mesh(
            new THREE.CylinderGeometry(neckW,neckW*1.2,neckH,8),
            glassBMat
        );
        neck.position.y=bH+neckH/2;
        g.add(neck);
    }}

    // Stopper/Cork/Cap
    if(b.shape==='tin'){{
        // Tin lid line
        const lid=new THREE.Mesh(new THREE.BoxGeometry(bW*2.02,0.01,bW*1.52),brassMat);
        lid.position.y=bH+0.005;
        g.add(lid);
    }}else if(b.shape==='round'){{
        // Wax seal
        const seal=new THREE.Mesh(new THREE.CylinderGeometry(neckW*1.3,neckW*1.3,0.03,8),waxRedMat);
        seal.position.y=bH+neckH+0.015;
        g.add(seal);
    }}else if(b.shape==='crystal'){{
        // Crystal stopper
        const stopper=new THREE.Mesh(new THREE.OctahedronGeometry(0.035,0),
            new THREE.MeshStandardMaterial({{color:0xdddddd,roughness:0.1,metalness:0.2,transparent:true,opacity:0.6}}));
        stopper.position.y=bH+neckH+0.04;
        g.add(stopper);
    }}else{{
        // Cork
        const cork=new THREE.Mesh(new THREE.CylinderGeometry(neckW*0.9,neckW*1.1,0.06,8),corkMat);
        cork.position.y=bH+neckH+0.03;
        g.add(cork);
    }}

    // Label (front-facing plane)
    if(b.shape!=='tin'&&b.shape!=='tiny'){{
        const labelW=bW*1.4;
        const labelH=bH*0.35;
        const label=new THREE.Mesh(new THREE.PlaneGeometry(labelW,labelH),labelMat);
        label.position.set(0,bH*0.45,bW+0.005);
        g.add(label);
    }}

    // Position on shelf
    g.position.set(b.x, shelfY+0.035, zOff);

    // Store data for interaction
    g.userData={{type:'bottle', id:b.id, title:b.name, sub:b.sub||'', desc:b.desc, secret:b.secret, uv:b.uv}};
    g.traverse(ch=>{{if(ch.isMesh) ch.userData.parentGroup=g;}});
    return g;
}}

// ==================== INSTRUMENT CREATION ====================
function makeInstrument(inst, shelfY, zOff){{
    const g=new THREE.Group();
    
    if(inst.id==='scarificator'){{
        const box=new THREE.Mesh(new THREE.BoxGeometry(0.18,0.06,0.12),brassMat);
        box.position.y=0.03;
        g.add(box);
        const knob=new THREE.Mesh(new THREE.CylinderGeometry(0.02,0.02,0.03,6),brassMat);
        knob.position.set(0,0.075,0);
        g.add(knob);
    }}else if(inst.id==='leech_jar'){{
        const jar=new THREE.Mesh(new THREE.CylinderGeometry(0.1,0.1,0.35,16),
            new THREE.MeshStandardMaterial({{color:0xaaddcc,roughness:0.1,transparent:true,opacity:0.35}}));
        jar.position.y=0.175;
        g.add(jar);
        const water=new THREE.Mesh(new THREE.CylinderGeometry(0.09,0.09,0.28,14),
            new THREE.MeshStandardMaterial({{color:0x556644,roughness:0.2,transparent:true,opacity:0.5}}));
        water.position.y=0.15;
        g.add(water);
        const lid=new THREE.Mesh(new THREE.CylinderGeometry(0.11,0.11,0.03,16),
            new THREE.MeshStandardMaterial({{color:0xccbb99,roughness:0.8}}));
        lid.position.y=0.36;
        g.add(lid);
        // Leech shapes inside
        for(let i=0;i<3;i++){{
            const leech=new THREE.Mesh(new THREE.CylinderGeometry(0.008,0.005,0.06,6),
                new THREE.MeshStandardMaterial({{color:0x1a1a0a,roughness:0.9}}));
            leech.position.set(Math.cos(i*2.1)*0.04, 0.1+i*0.06, Math.sin(i*2.1)*0.04);
            leech.rotation.z=Math.random()*0.5;
            leech.userData.isLeech=true;
            leech.userData.idx=i;
            g.add(leech);
        }}
    }}else if(inst.id==='trephine'){{
        const handle=new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.03,0.15,8),woodMat);
        handle.position.set(0,0.1,0);
        g.add(handle);
        const shaft=new THREE.Mesh(new THREE.CylinderGeometry(0.012,0.012,0.2,6),steelMat);
        shaft.position.set(0,0.02,0);
        shaft.rotation.x=Math.PI/2;
        g.add(shaft);
        const blade=new THREE.Mesh(new THREE.TorusGeometry(0.04,0.008,6,12),steelMat);
        blade.position.set(0,0.02,0.12);
        g.add(blade);
    }}else if(inst.id==='amputation_saw'){{
        const sawHandle=new THREE.Mesh(new THREE.BoxGeometry(0.04,0.08,0.1),ivoryMat);
        sawHandle.position.set(0,0.04,0);
        g.add(sawHandle);
        const sawBlade=new THREE.Mesh(new THREE.BoxGeometry(0.25,0.08,0.005),steelMat);
        sawBlade.position.set(0.14,0.04,0);
        g.add(sawBlade);
    }}else if(inst.id==='syringe'){{
        const barrel=new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.015,0.18,8),
            new THREE.MeshStandardMaterial({{color:0xeeeedd,roughness:0.1,transparent:true,opacity:0.5}}));
        barrel.position.set(0,0.03,0);
        barrel.rotation.z=Math.PI/2;
        g.add(barrel);
        const plunger=new THREE.Mesh(new THREE.CylinderGeometry(0.008,0.008,0.06,6),steelMat);
        plunger.position.set(-0.1,0.03,0);
        plunger.rotation.z=Math.PI/2;
        g.add(plunger);
        const needle=new THREE.Mesh(new THREE.CylinderGeometry(0.002,0.001,0.05,4),steelMat);
        needle.position.set(0.12,0.03,0);
        needle.rotation.z=Math.PI/2;
        g.add(needle);
        // Finger rings
        const ring=new THREE.Mesh(new THREE.TorusGeometry(0.025,0.004,4,8),steelMat);
        ring.position.set(-0.13,0.03,0);
        ring.rotation.y=Math.PI/2;
        g.add(ring);
    }}else if(inst.id==='scalpel_set'){{
        // Leather roll
        const roll=new THREE.Mesh(new THREE.BoxGeometry(0.3,0.01,0.15),
            new THREE.MeshStandardMaterial({{color:0x5a3a1a,roughness:0.9}}));
        roll.position.y=0.005;
        g.add(roll);
        for(let i=0;i<7;i++){{
            if(i===2) continue; // Missing blade #3
            const blade=new THREE.Mesh(new THREE.BoxGeometry(0.003,0.003,0.08+i*0.005),steelMat);
            blade.position.set(-0.12+i*0.04,0.015,0.02);
            g.add(blade);
            const bHandle=new THREE.Mesh(new THREE.BoxGeometry(0.008,0.005,0.04),ivoryMat);
            bHandle.position.set(-0.12+i*0.04,0.015,-0.04);
            g.add(bHandle);
        }}
    }}

    g.position.set(inst.x, shelfY+0.035, zOff);
    g.userData={{type:'instrument',id:inst.id,title:inst.name,sub:'',desc:inst.desc,secret:inst.secret,uv:inst.uv}};
    g.traverse(ch=>{{if(ch.isMesh&&!ch.userData.parentGroup) ch.userData.parentGroup=g;}});
    return g;
}}

// ==================== SPECIMEN CREATION ====================
function makeSpecimen(spec, shelfY, zOff){{
    const g=new THREE.Group();
    const jarH=0.3, jarR=0.09;
    
    // Glass jar
    const jar=new THREE.Mesh(new THREE.CylinderGeometry(jarR,jarR,jarH,14),
        new THREE.MeshStandardMaterial({{color:spec.jar||0xddddcc,roughness:0.1,transparent:true,opacity:0.3}}));
    jar.position.y=jarH/2;
    g.add(jar);

    // Liquid
    const liq=new THREE.Mesh(new THREE.CylinderGeometry(jarR*0.9,jarR*0.9,jarH*0.85,12),
        new THREE.MeshStandardMaterial({{color:spec.liquid||0xaaaa88,roughness:0.2,transparent:true,opacity:0.4}}));
    liq.position.y=jarH*0.4;
    g.add(liq);

    // Lid
    const lid=new THREE.Mesh(new THREE.CylinderGeometry(jarR*1.05,jarR*1.05,0.03,14),corkMat);
    lid.position.y=jarH+0.015;
    g.add(lid);

    // Specimen inside
    if(spec.id==='heart_jar'){{
        const heart=new THREE.Mesh(new THREE.SphereGeometry(0.05,8,6),
            new THREE.MeshStandardMaterial({{color:0x993333,roughness:0.5}}));
        heart.position.y=jarH*0.45;
        heart.scale.set(1,1.2,0.8);
        heart.userData.isFloating=true;
        g.add(heart);
    }}else if(spec.id==='brain_section'){{
        const brain=new THREE.Mesh(new THREE.CylinderGeometry(0.06,0.06,0.015,12),
            new THREE.MeshStandardMaterial({{color:0xccaa88,roughness:0.7}}));
        brain.position.y=jarH*0.4;
        g.add(brain);
    }}else if(spec.id==='blood_rack'){{
        // Rack of small vials
        const rack=new THREE.Mesh(new THREE.BoxGeometry(0.25,0.03,0.08),woodMat);
        rack.position.y=0.015;
        g.add(rack);
        for(let i=0;i<6;i++){{
            const vial=new THREE.Mesh(new THREE.CylinderGeometry(0.01,0.01,0.12,6),
                new THREE.MeshStandardMaterial({{color:0xaa0000,roughness:0.1,transparent:true,opacity:0.5}}));
            vial.position.set(-0.1+i*0.04,0.09,0);
            g.add(vial);
            const blood=new THREE.Mesh(new THREE.CylinderGeometry(0.008,0.008,0.06+Math.random()*0.04,6),
                new THREE.MeshStandardMaterial({{color:0x8b0000,roughness:0.3,transparent:true,opacity:0.7}}));
            blood.position.set(-0.1+i*0.04,0.05,0);
            g.add(blood);
        }}
        // Override jar visibility
        jar.visible=false; liq.visible=false; lid.visible=false;
    }}

    g.position.set(spec.x, shelfY+0.035, zOff);
    g.userData={{type:'specimen',id:spec.id,title:spec.name,sub:spec.sub||'',desc:spec.desc,secret:spec.secret,uv:spec.uv}};
    g.traverse(ch=>{{if(ch.isMesh&&!ch.userData.parentGroup) ch.userData.parentGroup=g;}});
    return g;
}}

// ==================== PERSONAL ITEMS ====================
function makePersonal(item, shelfY, zOff){{
    const g=new THREE.Group();

    if(item.id==='notebook'){{
        const cover=new THREE.Mesh(new THREE.BoxGeometry(0.15,0.02,0.2),
            new THREE.MeshStandardMaterial({{color:0x3a2010,roughness:0.85}}));
        cover.position.y=0.01;
        g.add(cover);
        const pages=new THREE.Mesh(new THREE.BoxGeometry(0.14,0.015,0.19),
            new THREE.MeshStandardMaterial({{color:0xfffff0,roughness:0.95}}));
        pages.position.y=0.02;
        g.add(pages);
        const strap=new THREE.Mesh(new THREE.BoxGeometry(0.005,0.005,0.22),
            new THREE.MeshStandardMaterial({{color:0x2a1508,roughness:0.9}}));
        strap.position.set(0.05,0.03,0);
        g.add(strap);
    }}else if(item.id==='locket'){{
        const locket=new THREE.Mesh(new THREE.SphereGeometry(0.025,8,6),brassMat);
        locket.position.y=0.025;
        locket.scale.y=0.6;
        g.add(locket);
        // Chain
        for(let i=0;i<8;i++){{
            const link=new THREE.Mesh(new THREE.TorusGeometry(0.008,0.002,4,6),brassMat);
            link.position.set(0.015*i-0.06,0.01,0);
            link.rotation.y=i%2===0?0:Math.PI/2;
            g.add(link);
        }}
    }}else if(item.id==='red_rose_seal'){{
        const sealBase=new THREE.Mesh(new THREE.CylinderGeometry(0.03,0.035,0.06,8),brassMat);
        sealBase.position.y=0.03;
        g.add(sealBase);
        const sealHandle=new THREE.Mesh(new THREE.CylinderGeometry(0.015,0.02,0.04,6),woodMat);
        sealHandle.position.y=0.07;
        g.add(sealHandle);
        // Rose emblem on bottom
        const emblem=new THREE.Mesh(new THREE.CircleGeometry(0.025,12),
            new THREE.MeshStandardMaterial({{color:0x8b0000,roughness:0.4}}));
        emblem.rotation.x=Math.PI/2;
        emblem.position.y=0.001;
        g.add(emblem);
    }}

    g.position.set(item.x, shelfY+0.035, zOff);
    g.userData={{type:'personal',id:item.id,title:item.name,sub:'',desc:item.desc,secret:item.secret,uv:item.uv}};
    g.traverse(ch=>{{if(ch.isMesh&&!ch.userData.parentGroup) ch.userData.parentGroup=g;}});
    return g;
}}

// ==================== PLACE ALL ITEMS ====================
const allObjects=[];
const shelfYs=[0.63, 1.63, 2.63, 3.63];

bottles.forEach(b=>{{
    const obj=makeBottle(b, shelfYs[b.shelf], -0.1);
    cabinet.add(obj);
    allObjects.push(obj);
    clickable.push(obj);
}});

instruments.forEach(inst=>{{
    const obj=makeInstrument(inst, shelfYs[inst.shelf], 0.05);
    cabinet.add(obj);
    allObjects.push(obj);
    clickable.push(obj);
}});

specimens.forEach(spec=>{{
    const obj=makeSpecimen(spec, shelfYs[spec.shelf], -0.25);
    cabinet.add(obj);
    allObjects.push(obj);
    clickable.push(obj);
}});

personal.forEach(item=>{{
    const obj=makePersonal(item, shelfYs[item.shelf||3], 0.2);
    cabinet.add(obj);
    allObjects.push(obj);
    clickable.push(obj);
}});

// ==================== FLOOR & ENVIRONMENT ====================
const floor=new THREE.Mesh(new THREE.PlaneGeometry(20,20),
    new THREE.MeshStandardMaterial({{color:{hx(c["wood_dark"])},roughness:0.9}}));
floor.rotation.x=-Math.PI/2;
floor.position.y=-0.25;
floor.receiveShadow=true;
scene.add(floor);

// Back wall
const wall=new THREE.Mesh(new THREE.PlaneGeometry(20,10),
    new THREE.MeshStandardMaterial({{color:{hx(c["wood_dark"])},roughness:0.95}}));
wall.position.set(0,4,-2);
scene.add(wall);

// Dust particles
const pCount={particle_count};
const pGeo=new THREE.BufferGeometry();
const pPos=new Float32Array(pCount*3);
const pVel=[];
for(let i=0;i<pCount;i++){{
    pPos[i*3]=(Math.random()-0.5)*6;
    pPos[i*3+1]=Math.random()*6;
    pPos[i*3+2]=(Math.random()-0.5)*4;
    pVel.push(0.001+Math.random()*0.003);
}}
pGeo.setAttribute('position',new THREE.BufferAttribute(pPos,3));
const particles=new THREE.Points(pGeo,new THREE.PointsMaterial({{
    color:{hx(c["candle"])},size:0.025,transparent:true,opacity:0.4
}}));
scene.add(particles);

// ==================== CAMERA CONTROLS ====================
let isDragging=false, prevMouse={{x:0,y:0}};
let spherical={{radius:5.5,theta:0,phi:Math.PI/3}};
const lookTarget=new THREE.Vector3(0,2.2,0);

function updateCamera(){{
    camera.position.x=lookTarget.x+spherical.radius*Math.sin(spherical.phi)*Math.cos(spherical.theta);
    camera.position.y=lookTarget.y+spherical.radius*Math.cos(spherical.phi);
    camera.position.z=lookTarget.z+spherical.radius*Math.sin(spherical.phi)*Math.sin(spherical.theta);
    camera.lookAt(lookTarget);
}}

renderer.domElement.addEventListener('mousedown',e=>{{isDragging=true;prevMouse={{x:e.clientX,y:e.clientY}}}});
renderer.domElement.addEventListener('mousemove',e=>{{
    if(isDragging){{
        spherical.theta-=(e.clientX-prevMouse.x)*0.008;
        spherical.phi=Math.max(0.4,Math.min(1.4,spherical.phi+(e.clientY-prevMouse.y)*0.008));
        prevMouse={{x:e.clientX,y:e.clientY}};
        updateCamera();
    }}
}});
window.addEventListener('mouseup',()=>{{isDragging=false}});
renderer.domElement.addEventListener('wheel',e=>{{
    e.preventDefault();
    spherical.radius=Math.max(3,Math.min(9,spherical.radius+e.deltaY*0.01));
    updateCamera();
}},{{passive:false}});
renderer.domElement.addEventListener('touchstart',e=>{{if(e.touches.length===1){{isDragging=true;prevMouse={{x:e.touches[0].clientX,y:e.touches[0].clientY}}}}}});
renderer.domElement.addEventListener('touchmove',e=>{{
    if(!isDragging||e.touches.length!==1)return;
    spherical.theta-=(e.touches[0].clientX-prevMouse.x)*0.008;
    spherical.phi=Math.max(0.4,Math.min(1.4,spherical.phi+(e.touches[0].clientY-prevMouse.y)*0.008));
    prevMouse={{x:e.touches[0].clientX,y:e.touches[0].clientY}};
    updateCamera();
}});
renderer.domElement.addEventListener('touchend',()=>{{isDragging=false}});
updateCamera();

// ==================== CLICK INTERACTION ====================
const tooltip=document.getElementById('tooltip');

function showTooltip(data,x,y){{
    tooltip.querySelector('.tt-name').textContent=data.title||'';
    tooltip.querySelector('.tt-sub').textContent=data.sub||'';
    tooltip.querySelector('.tt-desc').textContent=data.desc||'';
    const secretEl=tooltip.querySelector('.tt-secret');
    secretEl.textContent=INTENSITY>=3?(data.secret||''):'';
    secretEl.style.display=(INTENSITY>=3&&data.secret)?'block':'none';
    const uvEl=tooltip.querySelector('.tt-uv');
    uvEl.textContent=uvMode?(data.uv||''):'';
    uvEl.style.display=(uvMode&&data.uv)?'block':'none';
    tooltip.style.left=Math.min(x+15,window.innerWidth-340)+'px';
    tooltip.style.top=Math.min(y+15,window.innerHeight-200)+'px';
    tooltip.classList.add('visible');
}}

renderer.domElement.addEventListener('click',e=>{{
    const cm=new THREE.Vector2((e.clientX/window.innerWidth)*2-1,-(e.clientY/window.innerHeight)*2+1);
    raycaster.setFromCamera(cm,camera);
    const hits=raycaster.intersectObjects(scene.children,true);
    for(const hit of hits){{
        let obj=hit.object;
        if(obj.userData.parentGroup) obj=obj.userData.parentGroup;
        while(obj&&!obj.userData.type)obj=obj.parent;
        if(obj&&obj.userData.type){{
            showTooltip(obj.userData,e.clientX,e.clientY);
            return;
        }}
    }}
    tooltip.classList.remove('visible');
}});

// ==================== UV MODE ====================
window.toggleUV=function(){{
    uvMode=!uvMode;
    const btn=document.getElementById('uv-btn');
    btn.classList.toggle('active');
    if(uvMode){{
        scene.background.set(0x050008);
        keyLight.intensity=0;
        fillLight.intensity=0;
        candleLight.intensity=0;
        uvLight.intensity=15;
        scene.fog.density=0.005;
    }}else{{
        scene.background.set({hx(c["bg"])});
        keyLight.intensity={c["light_int"]*20};
        fillLight.intensity={c["light_int"]*8};
        candleLight.intensity={c["light_int"]*6};
        uvLight.intensity=0;
        scene.fog.density=0.012;
    }}
}};

// ==================== ANIMATION ====================
const clk=new THREE.Clock();

function animate(){{
    requestAnimationFrame(animate);
    const t=clk.getElapsedTime();

    // Candle flicker
    candleLight.intensity={c["light_int"]*6}*(1+Math.sin(t*15)*{flicker}+Math.sin(t*31)*{flicker*0.5});
    flame.material.opacity=0.7+Math.sin(t*12)*0.2;
    flame.scale.y=1.5+Math.sin(t*8)*0.2;

    // Key light subtle flicker
    if(!uvMode){{
        keyLight.intensity={c["light_int"]*20}*(1+Math.sin(t*7)*0.015);
    }}

    // Dust drift
    const pos=particles.geometry.attributes.position.array;
    for(let i=0;i<pCount;i++){{
        pos[i*3+1]+=pVel[i];
        pos[i*3]+=Math.sin(t*0.5+i)*0.0005;
        if(pos[i*3+1]>6)pos[i*3+1]=0;
    }}
    particles.geometry.attributes.position.needsUpdate=true;

    // Leech movement
    cabinet.traverse(ch=>{{
        if(ch.userData&&ch.userData.isLeech){{
            ch.rotation.z=Math.sin(t*0.8+ch.userData.idx*2)*0.4;
            ch.position.y+=Math.sin(t*0.5+ch.userData.idx*3)*0.0003;
        }}
    }});

    // Floating specimen
    cabinet.traverse(ch=>{{
        if(ch.userData&&ch.userData.isFloating){{
            ch.position.y+=Math.sin(t*0.4)*0.0004;
            ch.rotation.y=t*0.15;
        }}
    }});

    // Slow auto-rotate
    if(!isDragging){{
        spherical.theta+=0.0004;
        updateCamera();
    }}

    renderer.render(scene,camera);
}}

window.addEventListener('resize',()=>{{
    const w=container.clientWidth||window.innerWidth;
    const h=container.clientHeight||window.innerHeight;
    camera.aspect=w/h;
    camera.updateProjectionMatrix();
    renderer.setSize(w,h);
}});

animate();
}})();
</script></body></html>'''
    return html
