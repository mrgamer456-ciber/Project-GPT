# FPS Battle (nome provisório)

Projeto homebrew original para PlayStation 2, desenvolvido em C com PS2SDK e gsKit.

## Objetivo

Criar um jogo de tiro 3D em primeira pessoa, começando por uma versão pequena e testável no PS2 Slim SCPH-90010.

## Alpha 0.1 — primeiro protótipo

- Inicialização de vídeo e controle DualShock 2.
- Câmera em primeira pessoa com movimento e rotação.
- Cenário 3D low-poly pequeno.
- Arma simples em primeira pessoa.
- Tiro com raycast e alvo de teste.
- HUD com vida e munição.

## Plano de desenvolvimento

1. **Base técnica:** projeto PS2SDK, loop principal, vídeo e controle.
2. **Protótipo FPS:** câmera, movimento, colisão e cenário de teste.
3. **Combate:** arma, disparo, recarga, dano e HUD.
4. **Bots:** navegação simples, perseguição e ataque.
5. **Conteúdo:** mapas, armas, personagens, menus e emotes.
6. **Modos offline:** treinamento, partida contra bots e Battle Royale com bots.
7. **Online experimental:** avaliar rede TCP/IP do PS2SDK e infraestrutura externa. O online real depende de servidor e testes de rede; não será simulado como multiplayer.

## Limites e prioridades

- Prioridade inicial: jogabilidade estável, controles confortáveis e desempenho.
- Arte low-poly e texturas pequenas para caber nos limites de memória e processamento do PS2.
- Não prometer 3D avançado, muitos bots ou multiplayer antes de medir o protótipo no hardware.
- O primeiro alvo é um ELF executável; depois podemos preparar uma ISO para OPL.

## Controles planejados

- Analógico esquerdo: andar.
- Analógico direito: olhar.
- X: atirar.
- Quadrado: recarregar.
- L1: correr.
- R1: mirar.
- START: pausar.

Os controles ainda podem mudar após o primeiro teste no console.

## Ferramentas

- PS2SDK / PS2DEV: https://ps2dev.github.io/
- gsKit: https://github.com/ps2dev/gsKit
- Guia inicial: https://ps2dev.github.io/

## Estado atual

Planejamento inicial. Ainda não há build ELF nem protótipo testado no console.
