# Project-GPT

Laboratório independente de experimentos com jogos, ferramentas, ports e homebrew.

## Projeto atual

### ByteScope — Lab 001
Um visualizador binário que roda direto no navegador. Abre arquivos locais, mostra offsets, bytes HEX e ASCII, permite buscar sequências e exportar um relatório TXT.

- **Pasta:** `tools/bytescope/`
- **Entrada:** `tools/bytescope/index.html`
- **Privacidade:** o arquivo é processado localmente no navegador; não é enviado para servidor.
- **Limite visual:** mostra até os primeiros 64 KiB para manter o desempenho em celulares.



### PS2 ELF Inspector — Lab 002
Uma ferramenta experimental para identificar cabeçalhos ELF e verificar se o arquivo parece ser ELF32 MIPS little-endian, formato comum em homebrews de PS2.

- **Pasta:** `tools/ps2-elf-inspector/`
- **Entrada:** `tools/ps2-elf-inspector/index.html`
- **Privacidade:** análise local no navegador; nenhum arquivo é enviado.
- **Aviso:** identificação preliminar, não garante compatibilidade ou execução no console.



### Game File Detective — Lab 003
Ferramenta local para investigar arquivos de jogos: detecta assinaturas comuns (ELF, WAD, ZIP, PNG, Ogg, UnityFS e outras), mostra os primeiros bytes em HEX e procura sequências ASCII.

- **Pasta:** `tools/game-file-detective/`
- **Entrada:** `tools/game-file-detective/index.html`
- **Privacidade:** análise local no navegador.
- **Aviso:** assinaturas são pistas, não garantia de formato ou extração.

## Como testar
Abra `tools/bytescope/index.html` no navegador ou publique o repositório com GitHub Pages apontando para a raiz do site (a ferramenta está dentro de `tools/bytescope/`).

## Ideias para o laboratório
Este repositório é um espaço de experimentação. Cada projeto novo deve ter sua própria pasta, instruções de uso e, quando possível, testes ou compilação automatizada.

Feito em parceria humano + IA.