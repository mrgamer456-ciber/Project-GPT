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
Ferramenta local para investigar arquivos de jogos: detecta assinaturas comuns (ELF, WAD, ZIP, PNG, Ogg, UnityFS e outras), mostra os primeiros bytes em HEX e procura até 70 sequências ASCII nos primeiros 1 MiB.

- **Pasta:** `tools/game-file-detective/`
- **Entrada:** `tools/game-file-detective/index.html`
- **Privacidade:** análise local no navegador.
- **Desempenho:** lê somente os primeiros 1 MiB, mesmo quando o arquivo é maior.
- **Aviso:** assinaturas são pistas, não garantia de formato ou extração.

### PAK & Archive Explorer — Lab 004
Investigador local de contêineres de jogos. Reconhece estruturas Quake PACK e WAD2/WAD3, identifica algumas assinaturas comuns, lista entradas quando o formato é conhecido, procura até 250 sequências ASCII nos primeiros 1 MiB e exibe uma prévia HEX.

- **Pasta:** `tools/pak-archive-explorer/`
- **Entrada:** `tools/pak-archive-explorer/index.html`
- **Privacidade:** análise local no navegador; nenhum arquivo é enviado.
- **Limites:** não extrai nem reconstrói arquivos; ZIP e Unity são apenas identificados por assinatura nesta versão. Formatos proprietários podem não ser reconhecidos.

### PS2 TIM2 Texture Inspector — Lab 005
Ferramenta local para inspecionar arquivos de textura TIM2 do PlayStation 2. Lê o cabeçalho principal e os cabeçalhos das imagens, mostrando dimensões, formato PSM, mipmaps, tamanhos, offsets e validações básicas de limites.

- **Pasta:** `tools/ps2-tim2-inspector/`
- **Entrada:** `tools/ps2-tim2-inspector/index.html`
- **Privacidade:** análise local no navegador; nenhum arquivo é enviado.
- **Limites:** não decodifica pixels, não converte para PNG e não valida completamente swizzling, alinhamento GS ou paletas. A validação estrutural é preliminar.

### Utilitário — ZIP Extractor
Ferramenta auxiliar para listar o conteúdo de arquivos ZIP locais ou de um link direto e baixar itens individualmente.

- **Pasta:** `tools/zip-extractor/`
- **Entrada:** `tools/zip-extractor/index.html`
- **Privacidade:** o ZIP é lido no navegador; o conteúdo não é enviado para um servidor.
- **Dependência:** carrega JSZip 3.10.2 pelo jsDelivr; precisa de internet para abrir a biblioteca.
- **Limite:** não cria uma pasta extraída completa. Arquivos ZIP muito grandes ou com milhares de entradas podem consumir bastante memória; prefira amostras confiáveis e pequenas.

## Experimento de análise — Cross Strike (PS2)

A pasta `samples/cross-strike/` reúne uma amostra ZIP, arquivos PS2 extraídos e resultados de engenharia reversa. O relatório atual identifica `MAIN.ELF` como ELF32 MIPS little-endian e registra sete arquivos PAK com assinatura `HJK1`, versão 2 e tabelas de seções verificadas.

- **Originais:** `samples/cross-strike/PS2/` contém `MAIN.ELF` e os sete PAKs.
- **Análise:** `analysis/report.md` documenta cabeçalhos, hashes, seções e strings; `analysis/extracted/` guarda cópias brutas das seções extraídas.
- **Texturas:** `converted/` contém inspeções e PNGs experimentais de registros TEXR. `alpha-clut-test-v4/` compara interpretações de alpha e ordem de CLUT; são candidatos de comparação, não uma confirmação de renderização idêntica à do jogo.
- **Edição:** `textures-to-edit/` reúne cópias planas das texturas originais exportadas, sem alterar os BINs de origem.

### Workflows do Cross Strike

Os nove workflows em `.github/workflows/` são iniciados manualmente (`workflow_dispatch`). Eles têm permissão `contents: write` porque alguns publicam os resultados gerados com commit e push para `main`. Execute-os somente quando quiser atualizar esses resultados; esta documentação não os executa automaticamente.

### Aviso sobre distribuição

O repositório é público. Publique amostras, executáveis, PAKs e texturas extraídas somente se você tiver autorização para redistribuí-los. A presença de um aviso nesta documentação não concede direitos sobre conteúdo de terceiros. Se a autorização não estiver clara, mantenha os arquivos em um repositório privado ou não os publique.

## Abrir as ferramentas
A página inicial está em [index.html](index.html) e reúne os cinco laboratórios e o utilitário ZIP Extractor. Cada ferramenta também pode ser baixada como um arquivo `index.html` e aberta localmente em um navegador moderno.

O repositório está preparado com caminhos relativos para hospedagem estática, mas **GitHub Pages não foi ativado** nesta revisão. Se quiser publicar o site, habilite Pages manualmente nas configurações do repositório, usando a branch `main` e a raiz (`/`).

## Ideias para o laboratório
Este repositório é um espaço de experimentação. Cada projeto novo deve ter sua própria pasta, instruções de uso e, quando possível, testes ou compilação automatizada.

Feito em parceria humano + IA.