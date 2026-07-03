# Ateliê Generativo — Arquitetura Modernista de Brasília

Projeto final da disciplina Inteligência Artificial Generativa e Modelos Multimodais (UniCEUB), desenvolvido individualmente por Leo.

## Visão geral

Fine-tuning de um modelo Stable Diffusion com LoRA no estilo da arquitetura modernista de Brasília — concreto aparente, curvas orgânicas, pilotis e o contraste com o céu do Cerrado — integrado a um pipeline multimodal (LLM → Difusor → TTS) publicado como aplicação Gradio no Hugging Face Spaces.

## Fluxo da aplicação

1. Usuário digita um tema curto (ex.: "feira de domingo")
2. Um LLM expande o tema em uma descrição visual rica
3. O Stable Diffusion + LoRA gera a imagem no estilo treinado
4. Um modelo TTS narra a descrição em áudio
5. A interface Gradio exibe imagem, texto e áudio

## Como executar

1. Abra os notebooks em `notebooks/` no Google Colab (GPU T4 ativada).
2. Execute na ordem: `01_dataset.ipynb` → `02_treino_lora.ipynb` → `03_avaliacao.ipynb`.
3. A aplicação publicada está disponível em: `[link do Space aqui]`

## Estrutura do repositório

```
atelie-generativo-leo/
├── README.md
├── dados/
│   ├── fontes.csv        # proveniência e licença de cada imagem
│   └── legendas.txt      # captions revisadas manualmente
├── notebooks/
│   ├── 01_dataset.ipynb
│   ├── 02_treino_lora.ipynb
│   └── 03_avaliacao.ipynb
├── app/
│   └── app.py            # aplicação Gradio publicada no Spaces
└── relatorio/
    └── relatorio_final.pdf
```

## Estilo visual

**Tema:** Arquitetura modernista de Brasília
**Token de estilo:** `estilo_brasilia`

## Licenças do dataset

Proveniência completa de cada imagem em `dados/fontes.csv`. Dataset composto majoritariamente por fotografias autorais, complementadas por imagens de domínio público ou licença Creative Commons.

## Uso de IA no desenvolvimento

[Atualizar ao longo do projeto: quais ferramentas de IA foram usadas e para quê — declaração exigida pela Seção 6 da Sistematização.]

## Link do Hugging Face Space

`[adicionar após publicação — Etapa 4]`
