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

### PAK & Archive Explorer — Lab 004
Investigador local de contêineres de jogos. Reconhece estruturas Quake PACK e WAD2/WAD3, identifica algumas assinaturas comuns, lista entradas quando o formato é conhecido, procura textos ASCII e exibe uma prévia HEX.

- **Pasta:** `tools/pak-archive-explorer/`
- **Entrada:** `tools/pak-archive-explorer/index.html`
- **Privacidade:** análise local no navegador; nenhum arquivo é enviado.
- **Limites:** não extrai nem reconstrói arquivos; ZIP e Unity são apenas identificados por assinatura nesta versão. Formatos proprietários podem não ser reconhecidos.

## Como testar
Abra o arquivo `index.html` da ferramenta desejada no GitHub e use a visualização Raw para abrir o HTML no navegador, ou publique o repositório com GitHub Pages. Com Pages configurado para a raiz, cada ferramenta fica no caminho `/tools/NOME-DA-FERRAMENTA/`.

## Ideias para o laboratório
Este repositório é um espaço de experimentação. Cada projeto novo deve ter sua própria pasta, instruções de uso e, quando possível, testes ou compilação automatizada.

Feito em parceria humano + IA.