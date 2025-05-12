Jogo 2D de Combate com Perguntas de Matemática Gakusei.
Este é um jogo 2D em Python, desenvolvido usando a biblioteca Pygame Zero, que combina mecânicas de combate com perguntas de matemática. O objetivo do jogo é derrotar inimigos ao responder perguntas de matemática dentro de um tempo limite.

Funcionalidades
Combate: O jogador enfrenta inimigos em batalhas de ritmo rápido. Durante o combate, o jogador precisa responder a uma pergunta de multiplicação antes que o tempo acabe. Se a resposta for correta, o jogador pode atacar; caso contrário, o inimigo ataca.

Níveis e XP: O jogador ganha pontos de experiência (XP) e pode subir de nível ao derrotar inimigos.

Música: O jogo possui música de fundo que muda durante o combate.

Contagem Regressiva: Durante o combate, o jogador tem 10 segundos para responder à pergunta.

Requisitos
Python 3.x

Pygame Zero instalado

Você pode instalar o Pygame Zero usando o seguinte comando:

bash
pip install pgzero


Como Jogar
Iniciar o jogo: Ao iniciar o jogo, você será levado para o menu principal, onde pode escolher começar uma nova partida.

Mecânica de combate: O combate é baseado em perguntas de matemática. Durante o combate, uma pergunta será exibida na tela. Você deve digitar a resposta corretamente dentro do tempo limite para atacar o inimigo. Se o inimigo atacar primeiro, o jogador perde vida.

Vencer o combate: Se o jogador derrotar o inimigo, ele ganha experiência e passa para o próximo nível.

Perder o combate: Se o tempo expirar ou o jogador errar a resposta, o inimigo terá a chance de atacar.

Estrutura do Projeto
1. pgzrun.py
Este é o arquivo principal que executa o jogo. Ele contém as principais mecânicas de atualização de estado do jogo, incluindo o combate, movimentação do jogador, e o controle do tempo.

2. player.py (Classe Player)
Define a classe Player, que controla as ações do personagem jogável, incluindo a movimentação, ataque, e status como saúde (HP) e pontos de experiência (XP).

3. inimigo.py (Classe Inimigo)
Define a classe Inimigo, que controla os inimigos enfrentados pelo jogador. Assim como o jogador, os inimigos têm atributos de saúde e dano, e podem atacar o jogador.

4. game.py (Funções auxiliares)
Contém funções auxiliares para gerar perguntas de matemática, verificar colisões e desenhar elementos do jogo na tela, como a barra de saúde, fundo e personagens.

![image](https://github.com/user-attachments/assets/c40e89a1-3796-42ae-ade8-357139f515e0)

![image](https://github.com/user-attachments/assets/98b69a9a-addf-4527-95df-3c6165831bc2)

![image](https://github.com/user-attachments/assets/48017489-8368-448b-ab18-fce13adc6c43)



