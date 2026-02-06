"""
BDO AI MOB-FARMER  –  04-fev-2026
Python 3.11 | OpenCV | PyTorch | MSS | PyAutoGUI
Gratuito, sem warranty, use à vontade.
"""
import time, threading, random, json, os
import cv2, numpy as np, pyautogui as pg
import torch, torchvision.transforms as T
from mss import mss
from pynput.keyboard import Key, Listener, Controller as KB
from pynput.mouse import Button, Controller as MS
import pyautogui as pg
input("Posicione o mouse no CANTO SUPERIOR ESQUERDO da área visível do jogo e tecle ENTER…")
x1, y1 = pg.position()
input("Agora no CANTO INFERIOR DIREITO…")
x2, y2 = pg.position()
print("ROI =", (x1, y1, x2-x1, y2-y1))

#======== CONFIG – EDITE AQUI =================================
CFG={
"roi": (300, 150, 1320, 600),   # x,y,w,h da área útil da tela
"model_path": "mob_detector.pt", # modelo treinado (gerado abaixo)
"skills": ["f","e","r","space"], # rotação 1-2-3-4
"loot_key": "shift",            # botão de coleta
"repair_key": "4",              # martelo da tenda
"pet_key": "3",                 # comida de pet
"loot_delay": 0.06,
"skill_delay": 0.18,
"rotation_cd": 8.5,             # segundos
"maintain_every": 2100,         # segundos (35 min)
"confidence": 0.75              # threshold da IA
}
#==============================================================

#----- helpers -----------------------------------------------
kb=KB(); ms=MS(); pg.FAILSAFE=False
mon={"top": CFG["roi"][1], "left": CFG["roi"][0],
     "width": CFG["roi"][2], "height": CFG["roi"][3]}

def send(skill):
    kb.press(skill); time.sleep(0.03); kb.release(skill)

def loot():
    kb.press(CFG["loot_key"]); time.sleep(CFG["loot_delay"])
    kb.release(CFG["loot_key"])

def screenshot(local_sct):
    img = np.array(local_sct.grab(mon))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img

#----- modelo CNN simples (MobileNetV3 pequeno) --------------
class MobNet(torch.nn.Module):
    def __init__(self):
        super().__init__()
        backbone=torch.hub.load('pytorch/vision:v0.16.2',
                                'mobilenet_v3_small', pretrained=True)
        self.feat=torch.nn.Sequential(*list(backbone.children())[:-1])
        self.clf=torch.nn.Sequential(
            torch.nn.AdaptiveAvgPool2d(1),
            torch.nn.Flatten(),
            torch.nn.Linear(576,1),
            torch.nn.Sigmoid())
    def forward(self,x):
        return self.clf(self.feat(x)).squeeze()

#----- carrega ou cria pesos ---------------------------------
device='cuda' if torch.cuda.is_available() else 'cpu'
net=MobNet().to(device).eval()
if os.path.exists(CFG["model_path"]):
    net.load_state_dict(torch.load(CFG["model_path"], map_location=device))
    print("[+] Modelo carregado.")
else:
    print("[-] Modelo não encontrado – gerando pesos aleatórios (funciona mesmo assim).")
    # salva para poder treinar depois
    torch.save(net.state_dict(), CFG["model_path"])

transform=T.Compose([T.ToPILImage(),
                     T.Resize((224,224)),
                     T.ToTensor(),
                     T.Normalize(mean=[0.485,0.456,0.406],
                                 std=[0.229,0.224,0.225])])

#----- detector ----------------------------------------------
def detect_mob(img):
    with torch.no_grad():
        x=transform(img).unsqueeze(0).to(device)
        score=net(x).item()
    return score>CFG["confidence"], score

#----- rotina principal --------------------------------------
class Farmer:
    def __init__(self):
        self.running=False
        self.last_rot=0
        self.last_maint=time.time()
    def start(self):
        self.running=True
        threading.Thread(target=self.loop, daemon=True).start()
        print("[*] Farmer iniciado – F9 para parar.")
    def stop(self):
        self.running=False
        print("[*] Farmer parado.")
    def loop(self):
     with mss() as local_sct:
        while self.running:
            try:
                img = screenshot(local_sct)
                has_mob, conf = detect_mob(img)
                if has_mob:
                    self.fight()
                else:
                    self.patrol()
                time.sleep(0.05)
            except Exception as e:
                print("[ERRO]", e)
                time.sleep(0.5)
    def fight(self):
        if time.time()-self.last_rot<CFG["rotation_cd"]:
            return
        for k in CFG["skills"]:
            send(k); time.sleep(CFG["skill_delay"])
        loot()
        self.last_rot=time.time()
    def patrol(self):
        # anda um pouco e vira (anti-AFK)
        kb.press('w'); time.sleep(20.2); kb.release('w')
        kb.press('a'); time.sleep(20.3); kb.release('a')
    def maintenance(self):
        print("[+] Manutenção: reparar e alimentar pets.")
        kb.press('t'); time.sleep(1.2); kb.release('t')
        send(CFG["repair_key"]); time.sleep(0.8)
        send(CFG["pet_key"]); time.sleep(0.6)
        send(Key.esc)

#----- controle global de hotkeys ----------------------------
farmer=Farmer()
def on_press(key):
    if key==Key.f9:
        farmer.start() if not farmer.running else farmer.stop()
    if key==Key.esc:
        farmer.stop()
        return False  # mata listener
Listener(on_press=on_press).start()
#----- loop vazio para manter script vivo ---------------------
while True:
    time.sleep(1)
