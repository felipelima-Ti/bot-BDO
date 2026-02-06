import pyautogui as pg, json, os, sys
input("1) Coloque BDO em tela cheia/borderless.\n2) Vá com o personagem parado.\n3) Posicione o MOUSE no CANTO SUPERIOR ESQUERDO da área VISÍVEL do jogo e dê ENTER…")
x1, y1 = pg.position()
input("Agora posicione no CANTO INFERIOR DIREITO e dê ENTER…")
x2, y2 = pg.position()
roi = (x1, y1, x2-x1, y2-y1)
print("ROI detectada:", roi)
# atualiza CFG do bot com a ROI detectada
with open("bdo_bot.py", "r", encoding="utf-8") as f:
    txt = f.read()
txt = txt.replace('"roi": (300, 150, 1320, 600)', f'"roi": {roi}')
with open("bdo_bot.py", "w", encoding="utf-8") as f:
    f.write(txt)
print("CFG atualizado – pode fechar esta janela.")