import pgzrun
import sys
import random
import time

from pgzero.clock import schedule

import random

pergunta = ""
resposta_correta = 0
resposta_jogador = ""

def gerar_pergunta():
    global pergunta, resposta_correta, resposta_jogador
    a = random.randint(2, 12)
    b = random.randint(2, 12)
    pergunta = f"{a} x {b} = ?"
    resposta_correta = a * b
    resposta_jogador = ""

tempo_restante = 10


scroll_x = 0
scroll_y = 0

chunk_tamanho = 700
pontos_por_chunk = 10
pontos_chunk = {}

def gerar_pontos_chunk(cx, cy):
    pontos = []
    for i in range(pontos_por_chunk):
        x = cx * chunk_tamanho + random.randint(0, chunk_tamanho)
        y = cy * chunk_tamanho + random.randint(0, chunk_tamanho)
        pontos.append((x,y))
    return pontos

musica_combate = False

RAIO_COLISAO = 20

print("Comecando jogo")

WIDTH = 800
HEIGHT = 600
tile = images.tile

camera_offset = [0,0]

estado_jogo = "menu"
tempo_entrada = 0
musica_ativa = True
music.play('musica_tema')

estado_player = ""
estado_inimigo = ''

# Botões retangulo 
botao_jogar = Rect((300, 220), (200, 60))
botao_musica = Rect((300, 300), (200, 60))
botao_sair = Rect((300, 380), (200, 60))

COR_BOTAO = (50, 50, 200)
COR_BOTAO_HOVER = (80, 80, 250)
COR_TEXTO = (255, 255, 255)

#posicao inicial do mouse
mouse_pos = (0, 0)

#classe jogador
class Player:
    def __init__(self, idle_images, running_images, attack_images, combate_attack_imgs, combate_idle_imgs, combate_running_imgs, pos):
        #imgs
        self.idle_images = idle_images
        self.running_images = running_images
        self.attack_images = attack_images
        self.combat_attack_imgs = combate_attack_imgs
        self.combat_idle_imgs = combate_idle_imgs
        self.combat_running_imgs = combate_running_imgs

        #posicao e img sprite inicial
        self.images = idle_images
        self.pos = list(pos)
        self.estado = "esperando"

        #configuracao dos frames
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 0.15
        self.speed = 100

        #attack
        self.attacking = False
        self.attack_timer = 0
        self.attack_duration = 0.8

        #atributos
        self.dano = 2
        self.xp = 0
        self.lvl = 1
        self.hp = 10
        self.hp_max = 10

    def atualiza_atributos(self):
        if self.xp >= 100:
            self.lvl +=1
            self.dano += 2

    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.images = self.attack_images
            self.current_frame = 0
            self.frame_time = 0
            self.attack_timer = 0

    def update(self, dt, scroll_x, scroll_y):
        
        

         # Prioridade: ataque
        if self.attacking:
            self.attack_timer += dt
            self.frame_time += dt

            if self.frame_time >= self.frame_duration:
                self.frame_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.attack_images)

            if self.attack_timer >= self.attack_duration:
                self.attacking = False
                self.images = self.idle_images
                self.current_frame = 0
                self.frame_time = 0
                self.attack_timer = 0
            return  # Impede movimento enquanto ataca

        #atualiza frames
        self.frame_time += dt

        #keyboard
        keys = keyboard
        moved = False

        if keys.a:
            self.pos[0] -= self.speed * dt
            scroll_x -= self.speed
            moved = True
        if keys.d:
            self.pos[0] += self.speed * dt
            scroll_x += self.speed
            moved = True
        if keys.w:
            self.pos[1] -= self.speed * dt
            scroll_y -= self.speed
            moved = True
        if keys.s:
            self.pos[1] += self.speed * dt
            scroll_y += self.speed
            moved = True

        if moved:

            if self.images != self.running_images:
                self.images = self.running_images
                self.current_frame = 0
                self.frame_time = 0
            
        else:
            if self.images != self.idle_images:
                self.images = self.idle_images
                self.current_frame = 0
                self.frame_time = 0 
        
        if self.frame_time >= self.frame_duration:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)

        #verificando em que chunk o jogador esta
        cx = int(self.pos[0] // chunk_tamanho)
        cy = int(self.pos[1] // chunk_tamanho)

        if(cx, cy) not in pontos_chunk:
            pontos_chunk[(cx, cy)] = gerar_pontos_chunk(cx, cy)

        


    def draw(self):
        
        img = self.images[self.current_frame]
        img_width = img.get_width()
        img_height = img.get_height()
        draw_pos = (self.pos[0] - camera_offset[0] - img_width // 2,
                    self.pos[1] - camera_offset[1] - img_height // 2)

        screen.blit(img, draw_pos)

    def draw_combat(self):
        
        img = self.images[self.current_frame]
        img_width = img.get_width()
        img_height = img.get_height()
        draw_pos = (self.pos[0] - img_width, self.pos[1] - img_height)

        screen.blit(img, draw_pos)

    def update_combat(self,dt):
        global estado_player

        self.estado = estado_player
        #atualizar imgs
        self.images = self.combat_idle_imgs
        self.frame_time += dt
        
        if self.estado == "correndo":
            self.images = self.combat_running_imgs
        
        if self.estado == "atacando":
            self.pos[1] = 300
            self.images = self.combat_attack_imgs
            if self.current_frame >= 5:
                self.estado = "esperando"
                estado_player = "esperando"
                
                print("teste")
        
        if self.estado == "esperando":
            self.images = combate_idle_imgs
            
            self.pos = [200, 300]

        if self.frame_time >= self.frame_duration:
            self.frame_time = 0
            self.current_frame = (self.current_frame + 1) % len(self.images)

#classe do inimigo reutilizavel
class Inimigo:
    def __init__(self, idle_imgs, running_imgs, attack_imgs, pos):
        #imgs
        self.idle_imgs = idle_imgs
        self.running_imgs = running_imgs
        self.attack_imgs = attack_imgs
        self.estado = "esperando"

        #atributos
        self.hp = 10
        self.dano = 2
        self.velocidade_ataque = 50
        self.hp_max = 10

        #posicao inicial
        self.images = self.idle_imgs
        self.pos = list(pos)

        #configuracao dos frames
        self.current_frame = 0
        self.frame_time = 0
        self.frame_duration = 0.15

    def update(self, dt):
        global estado_inimigo

        #atualiza frames
        self.frame_time += dt
        self.estado = estado_inimigo

        if self.estado == "correndo":

            self.images = self.running_imgs

        if self.estado == "atacando":
            self.images = self.attack_imgs
                
            if self.current_frame >= 8:
                self.estado = "esperando"
                estado_inimigo = "esperando"
            
        if self.estado == "esperando":
            estado_inimigo = "esperando"
            self.pos[0] = 700
            self.images = self.idle_imgs

        if self.frame_time >= self.frame_duration:
                self.frame_time = 0
                self.current_frame = (self.current_frame + 1) % len(self.images)

        
    def draw(self):
        img = self.images[self.current_frame]
        img_width = img.get_width()
        img_height = img.get_height()
        draw_pos = (self.pos[0] - img_width, self.pos[1] - img_height)

        screen.blit(img, draw_pos)


        

# Sprites
player_images = [
    images.player1, images.player2, images.player3, images.player4,
    images.player5, images.player6, images.player7
]

player_running_images = [
    images.running1, images.running2, images.running3, images.running4,
    images.running5, images.running6, images.running7, images.running8,
    images.running9, images.running10, images.running11, images.running12,
    images.running13, images.running14, images.running15, images.running16
]

player_attack_images = [
    images.attack0, images.attack1, images.attack2,
    images.attack3, images.attack4, images.attack5, images.attack6
]

combate_attack_imgs = [images.attack1_2x, images.attack2_2x,
    images.attack3_2x, images.attack4_2x, images.attack5_2x, images.attack6_2x]

combate_idle_imgs = [
    images.player1_2x, images.player2_2x, images.player3_2x, images.player4_2x,
    images.player5_2x, images.player6_2x, images.player7_2x
]

combate_running_images = [
    images.running1_2x, images.running2_2x, images.running3_2x, images.running4_2x,
    images.running5_2x, images.running6_2x, images.running7_2x, images.running8_2x,
    images.running9_2x, images.running10_2x
    ]

enemy_images = [
    images.enemy01, images.enemy02, images.enemy03, images.enemy04,
    images.enemy05, images.enemy06, images.enemy07, images.enemy08, images.enemy09
]

enemy_running_imgs = [
    images.enemy_running1, images.enemy_running2, images.enemy_running3, images.enemy_running4,
    images.enemy_running5, images.enemy_running6, images.enemy_running7, images.enemy_running8
]

enemy_attack_images = [
    images.enemy_attack1, images.enemy_attack2, images.enemy_attack3, images.enemy_attack4,
    images.enemy_attack5, images.enemy_attack6, images.enemy_attack7, images.enemy_attack8, images.enemy_attack9
]

#criacao do jogador e do inimigo
player = Player(player_images, player_running_images, player_attack_images, combate_attack_imgs, combate_idle_imgs, combate_running_images, (400, 400))
enemy = Inimigo(enemy_images, enemy_running_imgs, enemy_attack_images, (600, 400))

#desenha
def draw():
    screen.clear()
    screen.fill((200,200,200))

    if estado_jogo == "combate_mensagem":
        screen.draw.text("COMBATE", center=(WIDTH//2, HEIGHT//2), fontsize=64, color="black")
        

    if estado_jogo == "combate":
        screen.fill((180,180,180))
        #pergunta
        screen.draw.text(pergunta, center=(WIDTH//2, 300), fontsize=50, color="black")
        screen.draw.text(f"Resposta: {resposta_jogador}", center=(WIDTH//2, 400), fontsize=40, color="black")

        player.draw_combat()
        desenhar_barra_hp(50, 30, 200, 20, player.hp, player.hp_max)
        enemy.draw()

        screen.draw.text(
            f"Tempo: {int(tempo_restante)}s",
            center=(WIDTH // 2, 50),
            fontsize=40,
            color="black"
        )

        desenhar_barra_hp(500, 30, 200, 20, enemy.hp, enemy.hp_max)


    #desenha menu se menu
    if estado_jogo == "menu":
        draw_menu()
    #player draw se jogo
    elif estado_jogo == "jogo":
        draw_background()
        desenhar_barra_hp(50, 30, 200, 20, player.hp, player.hp_max)
        player.draw()
        for pontos in pontos_chunk.values():
            for ponto in pontos:
                tela_x = ponto[0] - camera_offset[0]
                tela_y = ponto[1] - camera_offset[1]
                screen.draw.filled_circle((tela_x, tela_y), 5 , (80, 80, 80))
    
    if estado_jogo == "ganhou":
        screen.clear()
        screen.fill((200,200,200))
        player.draw_combat()
        screen.draw.text(f"VOCE GANHOU", center=(WIDTH//2, 400), fontsize=60, color="black")
    
    if estado_jogo == "perdeu":
        screen.clear()
        screen.fill((0,0,0))
        screen.draw.text("VOCE PERDEU",center=(WIDTH//2, HEIGHT//2), fontsize=60, color="white")

gerar_pergunta()

def update(dt):
    global estado_jogo, tempo_entrada, musica_combate, scroll_x, scroll_y, player, enemy, estado_player, estado_inimigo

    if estado_jogo == "combate":
        
           
        if not musica_combate and musica_ativa:
            music.stop()
            music.play("musica_tema_combate")
            musica_combate = True

        player.update_combat(dt)

        #enemy
        enemy.update(dt)    
        
        global tempo_restante
        tempo_restante -= dt

        if tempo_restante <= 0:
            enemy.current_frame = 0
            estado_inimigo = "correndo"
            gerar_pergunta()
            player.hp -= enemy.dano
            tempo_restante = 11
           
        #ataque do player
        if player.estado == "correndo":
            player.pos[1] = 375
            if player.pos[0] > enemy.pos[0] + 100:
                player.pos[0] -= player.speed
            if player.pos[0] < enemy.pos[0] - 100:
                player.pos[0] += player.speed
            player.current_frame = 0
        
        if player.pos[0] == 600:
            
            estado_player = "atacando"
            player.estado = "atacando"
            
        if enemy.hp == 0:
            mudar_para_ganhou()
            estado_player = "esperando"
            
           
        
        #ataque inimigo
        if enemy.estado == "correndo":
            if enemy.pos[0] > player.pos[0] + 100:
               
                enemy.pos[0] -= enemy.velocidade_ataque 
            if enemy.pos[0] < player.pos[0] - 100:
                
                enemy.pos[0] += enemy.velocidade_ataque 

            if enemy.pos[0] == player.pos[0] + 100:
                estado_inimigo = "atacando"
                enemy.estado = "atacando"
                
                
                
            
       
            

    

    if estado_jogo == "jogo":
        #checa a musica
        if not music.is_playing("musica_tema") and musica_ativa:
            music.play("musica_tema")

        #atualiza o estado da classe player se estiver no jogo
        player.update(dt, scroll_x, scroll_y)

        #CAMERA!!
        camera_offset[0] = player.pos[0] - WIDTH // 2
        camera_offset[1] = player.pos[1] - HEIGHT //2

        #teste de colisao
        pontos_a_remover = []
        for chunk, pontos in pontos_chunk.items():
            for ponto in pontos:
                dist = ((ponto[0] - player.pos[0])**2 + (ponto[1] - player.pos[1])**2) ** 0.5
                if dist < RAIO_COLISAO:
                    if random.random() < 0.5:
                        print("COMBATE!!")
                        estado_jogo = "combate_mensagem"
                        tempo_entrada = time.time()
                        player.current_frame = 0
                        
                    else:
                        print("Você se livrou dessa vez")
                    pontos_a_remover.append((chunk, ponto))
                    break

        for chunk, ponto in pontos_a_remover:
            pontos_chunk[chunk].remove(ponto)


    if estado_jogo == "combate_mensagem":
        if time.time() - tempo_entrada > 3:
            player.pos = [200, 300]
            enemy.pos = [700, 285]
        
            estado_jogo = "combate"

#desenha menu
def draw_menu():
    screen.draw.text("Gakusei", center=(WIDTH // 2, 140), fontsize=64, color="black")
    
    desenhar_botao(botao_jogar, "INICIAR JOGO")
    desenhar_botao(botao_musica, "MUSICA: " + ("ON"  if musica_ativa else "OFF"))
    desenhar_botao(botao_sair, "SAIR")

#desenha os botoes
def desenhar_botao(botao, texto):
    #detecta colisao com o mouse nos botoes
    mouse_em_cima = botao.collidepoint(mouse_pos)
    #botao HOVER!!!
    cor = COR_BOTAO_HOVER if mouse_em_cima else COR_BOTAO

    #desenha na tela um retangulo preenchido
    screen.draw.filled_rect(botao, cor)
    #desenha um texto
    screen.draw.textbox(texto, botao, color=COR_TEXTO)

#armazena a posicao do mouse
def on_mouse_move(pos):
    global mouse_pos
    mouse_pos = pos

#funcao que pega o click do mouse
def on_mouse_down(pos):
    global estado_jogo, musica_ativa
    if estado_jogo == "menu":
        #se clicar em menu altera o estado global do jogo pra jogo
        if botao_jogar.collidepoint(pos):
            estado_jogo = "jogo"
        #musica
        elif botao_musica.collidepoint(pos):
            musica_ativa = not musica_ativa
            if musica_ativa:
                print("Musica ativada")
                music.play("musica_tema")
            else:
                print("Musica desativada")
                music.stop()
        elif botao_sair.collidepoint(pos):
            print("Saindo do jogo...")
            sys.exit()

def on_key_down(key):
    global resposta_jogador

    if estado_jogo == "combate":
        if key == keys.K_0:
            resposta_jogador += "0"
        elif key == keys.K_1:
            resposta_jogador += "1"
        elif key == keys.K_2:
            resposta_jogador += "2"
        elif key == keys.K_3:
            resposta_jogador += "3"
        elif key == keys.K_4:
            resposta_jogador += "4"
        elif key == keys.K_5:
            resposta_jogador += "5"
        elif key == keys.K_6:
            resposta_jogador += "6"
        elif key == keys.K_7:
            resposta_jogador += "7"
        elif key == keys.K_8:
            resposta_jogador += "8"
        elif key == keys.K_9:
            resposta_jogador += "9"
        elif key == keys.BACKSPACE:
            resposta_jogador = resposta_jogador[:-1]
        elif key == keys.RETURN:
            verificar_resposta()

    elif estado_jogo == "jogo":
        if key == keys.SPACE:
            player.attack()

    
def desenhar_barra_hp(x, y, largura, altura, vida_atual, vida_maxima):
    # Cor de fundo (vermelha)
    screen.draw.filled_rect(Rect((x, y), (largura, altura)), "red")
    
    # Cor da vida restante (verde)
    vida_percentual = max(vida_atual / vida_maxima, 0)
    largura_vida = int(largura * vida_percentual)
    screen.draw.filled_rect(Rect((x, y), (largura_vida, altura)), "green")

    # Borda
    screen.draw.rect(Rect((x, y), (largura, altura)), "black")

def draw_background():
    global scroll_x, scroll_y
    # Quantos tiles cabem na tela
    tiles_x = WIDTH // 16 + 2
    tiles_y = HEIGHT // 16 + 2

    # Deslocamento para centralizar o scroll
    offset_x = scroll_x % 16
    offset_y = scroll_y % 16

    # Desenha os tiles de forma que pareçam infinitos
    for y in range(tiles_y):
        for x in range(tiles_x):
            screen.blit("tile", (x * 16 - offset_x, y * 16 - offset_y))



def verificar_resposta():
    global resposta_jogador, tempo_restante, estado_player, estado_inimigo, estado_jogo, player, enemy

    if resposta_jogador.isdigit():
        if int(resposta_jogador) == resposta_correta:
            player.current_frame = 0
            print("Correto!")
            estado_player = "correndo"
            gerar_pergunta()
            enemy.hp -= player.dano
            tempo_restante = 11
            
        else:
            print("Errado!")
            enemy.current_frame = 0
            estado_inimigo = "correndo"
            player.hp -= enemy.dano
            if player.hp == 0:
                estado_jogo = "perdeu"
            tempo_restante = 11
            gerar_pergunta()

def reiniciar():
    global estado_jogo, musica_combate
    music.stop()
    musica_combate = False
    music.play("musica_tema")

    enemy.hp = 10
    estado_jogo = "jogo"

def mudar_para_ganhou():
    global estado_jogo

    estado_jogo = "ganhou"
    schedule(reiniciar, 5.0)

pgzrun.go()
