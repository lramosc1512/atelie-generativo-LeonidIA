# Ateliê Generativo — Arquitetura Modernista de Brasília

Projeto final da disciplina Modelos Multimodais (UniCEUB), desenvolvido individualmente por Leonardo Coutinho.

## Links do projeto

- **Aplicação publicada:** [huggingface.co/spaces/lramosc1512/atelie-generativo-brasilia](https://huggingface.co/spaces/lramosc1512/atelie-generativo-brasilia)
- **LoRA Config 1** (rank 4): [huggingface.co/lramosc1512/lora-estilo-brasilia-config1](https://huggingface.co/lramosc1512/lora-estilo-brasilia-config1)
- **LoRA Config 2** (rank 8, usada no app): [huggingface.co/lramosc1512/lora-estilo-brasilia-config2](https://huggingface.co/lramosc1512/lora-estilo-brasilia-config2)
- **Relatório final:** [relatorio/relatorio_final.pdf](relatorio/relatorio_final.pdf)

## Visão geral

Fine-tuning de um modelo Stable Diffusion com LoRA no estilo da arquitetura modernista de Brasília: concreto aparente, curvas orgânicas, pilotis e o contraste com o céu do Cerrado. O modelo treinado foi integrado a um pipeline multimodal (LLM → Difusor → TTS) publicado como aplicação Gradio no Hugging Face Spaces.

## Fluxo da aplicação

1. Usuário digita um tema curto (ex.: "feira de domingo")
2. Um LLM expande o tema em uma descrição visual rica
3. O Stable Diffusion, com o LoRA carregado, gera a imagem no estilo treinado
4. Um modelo de TTS narra a descrição em áudio
5. A interface Gradio exibe imagem, texto e áudio juntos

## Como executar os notebooks

1. Abra os notebooks em `notebooks/` no Google Colab (GPU T4 ativada).
2. Execute na ordem: `01_dataset.ipynb` → `02_treino_lora.ipynb` → `03_avaliacao.ipynb`.

## Estrutura do repositório

```
atelie-generativo-LeonidIA/
├── README.md
├── dados/
│   ├── imagens/          # as 50 imagens do dataset
│   ├── fontes.csv        # proveniência e licença de cada imagem
│   └── legendas.txt      # legendas revisadas manualmente
├── notebooks/
│   ├── 01_dataset.ipynb
│   ├── 02_treino_lora.ipynb
│   └── 03_avaliacao.ipynb
├── app/
│   ├── app.py            # aplicação Gradio publicada no Spaces
│   └── requirements.txt
└── relatorio/
    └── relatorio_final.pdf
```

## Estilo visual

**Tema:** arquitetura modernista de Brasília
**Token de estilo:** `estilo_brasilia,`

## Dataset e licenças

50 imagens de arquitetura modernista de Brasília, obtidas do Wikimedia Commons sob licenças CC-BY e CC-BY-SA. Proveniência completa (URL de origem, autor, licença e data de coleta) documentada em `dados/fontes.csv`.

## Resultados resumidos

- **CLIPScore médio:** base 30.43, Config 1 31.45, Config 2 31.38
- **Avaliação humana** (8 respondentes, escala 1-5): Config 2 superou a Config 1 em fidelidade ao estilo e qualidade geral
- Detalhes completos, incluindo achados sobre memorização e vieses, estão no relatório final

## Uso de IA no desenvolvimento

Este projeto contou com apoio da IA Claude (Anthropic) em etapas específicas: estruturação inicial do repositório, expansão do exemplo de BLIP do PDF da disciplina em um pipeline completo, construção da conversão de dataset para o formato exigido pelo script de treino LoRA, e suporte de troubleshooting ao longo do projeto. A declaração completa está na Seção 7 do relatório final.
