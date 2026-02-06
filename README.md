Esse script é um bot de automação em python para o jogo Black Desert Online (BDO), que tenta detectar mobs na tela com uma IA simples e executar habilidades, loot e <br/>movimentação automaticamente.
<br/><br/>
Recomendaçoes de uso: ultilize o Python 13.11.8, dependendo se tiver dando erro de versão mude as variaveis ambiente do python, desative todos os sistema de segurança 
<br/><br/>
O que esse bot faz (em resumo)
<br/><br/>
Captura uma área da tela do jogo (ROI).
<br/><br/>
Usa uma rede neural (MobileNetV3) para tentar identificar se existe um mob na imagem.
<br/><br/>
Se detectar mob:
<br/><br/>
Executa uma rotação de skills.
<br/><br/>
Dá loot automaticamente.
<br/><br/>
Se não detectar:
<br/><br/>
Anda em padrões para não ficar AFK.
<br/><br/>
A cada tempo:
<br/><br/>
Faz manutenção (reparar tenda e alimentar pets).
<br/><br/>
Tudo é controlado por teclas globais:
<br/><br/>
F9 → liga/desliga o bot
<br/><br/>
ESC → encerra
<br/><br/><br/><br/>
. Seleção da área do jogo (ROI)
![alt text](image-1.png)
<br/><br/>
Isso serve para definir qual parte da tela será analisada pela IA (a área onde aparecem os mobs).
<br/><br/>
Depois essa área é usada no MSS:
<br/>
mon={"top": CFG["roi"][1], "left": CFG["roi"][0],
     "width": CFG["roi"][2], "height": CFG["roi"][3]}
<br/><br/>
Configurações principais
![alt text](image.png)
<br/><br/>
Isso define:
<br/>
Config	Função
<br/>
skills	Teclas das habilidades
<br/>
loot_key	Tecla de loot
<br/>
rotation_cd	Tempo mínimo entre rotações
<br/>
confidence	Quanto a IA precisa estar confiante para agir
<br/><br/>
Captura da tela
<br/><br/>
def screenshot(local_sct):
    img = np.array(local_sct.grab(mon))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img
<br/>
Ele captura apenas a área do jogo, não a tela inteira.
<br/><br/>
5. IA: detector de mob
<br/>
Ele cria uma rede neural baseada em MobileNetV3:
<br/>
class MobNet(torch.nn.Module):
    ...
<br/>
Ela retorna 1 valor entre 0 e 1:
<br/>
score=net(x).item()
<br/>
return score>CFG["confidence"], score
<br/>

Ou seja:
<br/>
“Essa imagem tem um mob? Sim/Não
<br/>
⚠️ Importante:
Se o arquivo mob_detector.pt não existir, ele usa pesos aleatórios, ou seja:
<br/>
A IA não funciona de verdade até ser treinada.
<br/><br/>
6. Lógica principal
<br/>
if has_mob:
<br/>
    self.fight()
    <br/>
else:<br/>
    self.patrol()
    <br/>

fight()<br/>
for k in CFG["skills"]:<br/>
    send(k)<br/>
loot()<br/>

<br/>
Ele aperta as skills em sequência e depois dá loot.
<br/>
patrol()<br/>
kb.press('w'); time.sleep(20.2)<br/>
kb.press('a'); time.sleep(20.3)<br/>

<br/>
Ele anda para frente e para o lado → anti-AFK.
<br/><br/>
7. Controle por teclas<br/>
if key==Key.f9:<br/>
    farmer.start() if not farmer.running else farmer.stop()<br/>

<br/><br/>
F9 → inicia / pausa o bot
<br/>
ESC → encerra tudo
<br/><br/>