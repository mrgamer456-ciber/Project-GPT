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
- **Referência PSM:** os identificadores de formato GS seguem o [PS2SDK](https://ps2dev.github.io/ps2sdk/gs__psm_8h.html), incluindo PSMT4HL = `0x24` e PSMT4HH = `0x2C`.
- **Alinhamento:** reconhece o ID `0x00` (16 bytes) e `0x01` (128 bytes). A variante `0x81` aparece em uma referência técnica, mas há divergência entre implementações; permanece sem interpretação até ser validada com uma amostra real.
- **Teste sintético:** o botão “Testar exemplo sintético” cria localmente um cabeçalho TIM2 mínimo de 1 × 1 PSMCT32. É um teste rápido da leitura de metadados, não uma amostra real nem uma validação de decodificação.
- **Desempenho:** lê apenas 16 bytes do cabeçalho principal e 48 bytes por imagem para inspecionar metadados; não carrega os dados completos das texturas.
- **Limites:** não decodifica pixels, não converte para PNG e não valida completamente swizzling, alinhamento GS ou paletas. A validação estrutural é preliminar.

### Utilitário — ZIP Extractor
Ferramenta auxiliar para listar o conteúdo de arquivos ZIP locais ou de um link direto e baixar itens individualmente.

- **Pasta:** `tools/zip-extractor/`
- **Entrada:** `tools/zip-extractor/index.html`
- **Privacidade:** o ZIP é lido no navegador; o conteúdo não é enviado para um servidor.
- **Dependência:** carrega JSZip 3.10.2 pelo jsDelivr; precisa de internet para abrir a biblioteca.
- **Pré-validação estrutural:** antes de chamar JSZip, verifica o EOCD e o diretório central, valida offsets e assinaturas dos cabeçalhos locais e compara nomes, flags, método de compactação, CRC e tamanhos entre cabeçalhos locais e centrais. Também confere descritores de dados. Aceita prefixos autoextraíveis (SFX); ZIP64, arquivos multidisco, criptografia e métodos diferentes de STORE/DEFLATE são rejeitados explicitamente.
- **Teste de regressão:** com Node.js 18 ou superior, execute `node tests/zip-preflight.test.mjs` para executar 16 casos: ZIP comum, prefixo SFX, descritores de dados com e sem assinatura, ZIP vazio e inconsistências entre cabeçalhos locais e centrais. O teste cobre a pré-validação, não a descompactação pelo JSZip nem a execução em navegador.
- **Limites de segurança/desempenho:** rejeita ZIPs acima de 128 MiB, mais de 5.000 entradas (incluindo pastas), um item com tamanho declarado acima de 128 MiB ou soma declarada acima de 256 MiB. A extração de cada item é contada em blocos e interrompida se os dados realmente descompactados ultrapassarem 128 MiB.
- **Memória:** o arquivo ZIP e o item escolhido continuam sendo mantidos em memória do navegador; o item é acumulado em um Blob de até 128 MiB antes do download. Não é uma extração direta para disco. Em celulares, prefira ZIPs menores e itens individuais pequenos.
- **Cuidado:** os limites de tamanho não substituem a validação do conteúdo. Use arquivos de origem confiável.

## Experimento de análise — Cross Strike (PS2)

A pasta `samples/cross-strike/` reúne uma amostra ZIP, arquivos PS2 extraídos e resultados de engenharia reversa. O relatório atual identifica `MAIN.ELF` como ELF32 MIPS little-endian e registra sete arquivos PAK com assinatura `HJK1`, versão 2 e tabelas de seções verificadas.

- **Originais:** `samples/cross-strike/PS2/` contém `MAIN.ELF` e os sete PAKs.
- **Análise:** `analysis/report.md` documenta cabeçalhos, hashes, seções e strings; `analysis/extracted/` guarda cópias brutas das seções extraídas.
- **Texturas:** `converted/` contém inspeções e PNGs experimentais de registros TEXR. `converted/alpha-clut-test-v4/` compara interpretações de alpha e ordem de CLUT; são candidatos de comparação, não uma confirmação de renderização idêntica à do jogo.
- **Edição:** `textures-to-edit/` reúne cópias planas das texturas originais exportadas, sem alterar os BINs de origem.
- **Geometria experimental:** `models/raw/` guarda seções MODL brutas; `models/geometry/raw/` guarda seções VERT, INDX, MATL e CHNK com inventário e SHA-256. `models/geometry/experimental/FLAT_normalized_experimental.obj` é apenas uma hipótese de visualização: contém 4.588 vértices e 2.288 faces, mas não tem UVs, normais ou materiais; somente 144 índices distintos são usados, deixando 4.444 vértices sem referência. Isso é compatível com a hipótese de índices locais por bloco CHNK, ainda sem offsets de vértice por bloco. Não trate esse OBJ como malha recuperada ou pronta para port.


### Inspeção de registros VERT (CLI)

O script `tools/ps2-geometry/inspect_vertex_records.py` analisa arquivos `*_VERT_*.bin` ou uma pasta inteira, com stride configurável (padrão de 16 bytes). Ele mostra HEX, interpretações little-endian u16/i16 e floats f32 somente em offsets alinhados a 4 bytes; não presume que essas lanes sejam posições, UVs ou normais. Exemplo:

```bash
python3 tools/ps2-geometry/inspect_vertex_records.py samples/cross-strike/models/geometry/raw --output vertex-layout-report.md
python3 -m unittest discover -s tests -p 'test_ps2_vertex_inspector.py'
```

O CLI impede que `--output` aponte para o mesmo arquivo analisado, inclusive por caminho simbólico (symlink), para evitar sobrescrever acidentalmente os BINs originais.

A execução de 10/11/2026 do workflow `decode-crossstrike-vertices.yml` falhou com `struct.error`: tentou ler um float32 no offset 14 de um registro de 16 bytes. O script CLI evita essa leitura fora dos limites; o workflow não foi alterado nesta revisão porque possui permissão de escrita e etapa de commit/push.

### Workflows do Cross Strike

Há 19 workflows em `.github/workflows/`. Dezessete declaram `permissions: contents: write` e incluem etapas de commit/push para `main`; todos os 19 aceitam `workflow_dispatch`. Seis também têm gatilho `push`: `analyze-crossstrike-modl.yml`, `convert-crossstrike-texr-png-v3.yml`, `decode-crossstrike-vertices.yml`, `extract-crossstrike-geometry.yml`, `extract-crossstrike-model-sections.yml` e `inspect-crossstrike-elf-deep.yml`. Cinco desses seis reagem a alterações no próprio YAML; `inspect-crossstrike-elf-deep.yml` também reage a mudanças em `samples/cross-strike/PS2/MAIN.ELF`. Entre os seis, quatro têm permissão de escrita e fazem commit/push; `analyze-crossstrike-modl.yml` e `inspect-crossstrike-elf-deep.yml` apenas geram artifacts. Antes de executar ou editar qualquer workflow, confira suas etapas e os arquivos que ele modifica. Esta documentação não executa workflows automaticamente. O probe `analyze-crossstrike-modl.yml` também é exploratório: o loop percorre offsets em passos fixos de 4 bytes e não usa o stride candidato como passo; portanto, seus resultados não são comparações independentes de registros de 12/16/20/24/32 bytes.

### PAK combinado experimental

`merged/CROSSSTRIKE_ALL.PAK` reúne as 105 seções dos sete PAKs originais. `merged/EXTRACTION-VERIFICATION.md` registra a comparação byte a byte dos 105 blocos extraídos. Isso valida a integridade estrutural e dos dados, mas **não confirma compatibilidade com o carregador do jogo**; mantenha os sete PAKs originais.

### Aviso sobre distribuição

O repositório é público. Publique amostras, executáveis, PAKs e texturas extraídas somente se você tiver autorização para redistribuí-los. A presença de um aviso nesta documentação não concede direitos sobre conteúdo de terceiros. Se a autorização não estiver clara, mantenha os arquivos em um repositório privado ou não os publique.

## Abrir as ferramentas
A página inicial está em [index.html](index.html) e reúne os cinco laboratórios e o utilitário ZIP Extractor. Cada ferramenta também pode ser baixada como um arquivo `index.html` e aberta localmente em um navegador moderno.

O repositório está preparado com caminhos relativos para hospedagem estática, mas **GitHub Pages não foi ativado** nesta revisão. Se quiser publicar o site, habilite Pages manualmente nas configurações do repositório, usando a branch `main` e a raiz (`/`).

## Ideias para o laboratório
Este repositório é um espaço de experimentação. Cada projeto novo deve ter sua própria pasta, instruções de uso e, quando possível, testes ou compilação automatizada.

Feito em parceria humano + IA.
