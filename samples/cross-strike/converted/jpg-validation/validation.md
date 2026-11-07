# CrossStrike JPEG candidate validation

Este teste NÃO considera uma assinatura FF D8 FF suficiente para provar que os bytes são uma imagem.
Cada candidato é aberto pelo Pillow, passa por verify(), é reaberto e decodificado por load().

- **COMMON/TEXR_01.bin**, candidato 1, offset 0x1ad2bb: **REJEITADO** — OSError: Truncated File Read
- **COMMON/TEXR_01.bin**, candidato 2, offset 0x1ae032: **REJEITADO** — OSError: Truncated File Read
- **COMMON/TEXR_01.bin**, candidato 3, offset 0x1ae937: **REJEITADO** — OSError: Truncated File Read
- **COMMON/TEXR_01.bin**, candidato 4, offset 0x1aeaca: **REJEITADO** — OSError: Truncated File Read
- **COMMON/TEXR_01.bin**, candidato 5, offset 0x1aeecd: **REJEITADO** — OSError: Truncated File Read
- **OFFSHORE/TEXR_01.bin**, candidato 1, offset 0x20695b: **REJEITADO** — OSError: Truncated File Read
- **OFFSHORE/TEXR_01.bin**, candidato 2, offset 0x2076d2: **REJEITADO** — OSError: Truncated File Read
- **OFFSHORE/TEXR_01.bin**, candidato 3, offset 0x207fd7: **REJEITADO** — OSError: Truncated File Read
- **OFFSHORE/TEXR_01.bin**, candidato 4, offset 0x20816a: **REJEITADO** — OSError: Truncated File Read
- **OFFSHORE/TEXR_01.bin**, candidato 5, offset 0x20856d: **REJEITADO** — OSError: Truncated File Read

## Resultado
- Candidatos encontrados: 10
- JPEGs realmente validados e decodificados: 0

Nenhum candidato passou pela validação completa. Isso indica que as assinaturas encontradas provavelmente são bytes internos dos dados TEXR, não fotos JPEG completas.
