import os
import re

import spaces
import gradio as gr
import torch
from diffusers import StableDiffusionPipeline
from transformers import pipeline
from huggingface_hub import login

# login opcional: se o secret HF_TOKEN estiver configurado no Space (Settings -> Variables
# and secrets), autentica para evitar o aviso de rate limit. Se nao estiver configurado,
# o app continua funcionando normalmente (todos os modelos usados sao publicos).
_hf_token = os.environ.get("HF_TOKEN")
if _hf_token:
    login(token=_hf_token)

# ---- Config: qual LoRA usar (troca facil aqui depois da avaliacao humana) ----
LORA_REPO = "lramosc1512/lora-estilo-brasilia-config2"  # trocar para -config1 se decidir usar a outra
TOKEN_ESTILO = "estilo_brasilia,"

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

print(f"Carregando modelo no device: {device}")

pipe = StableDiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=dtype,
)
pipe.load_lora_weights(LORA_REPO)
pipe = pipe.to(device)

expansor = pipeline(
    "text-generation",
    model="Qwen/Qwen2.5-0.5B-Instruct",
    device=0 if device == "cuda" else -1,
)
tts = pipeline(
    "text-to-speech",
    model="suno/bark-small",
    device=0 if device == "cuda" else -1,
)


ANCORA_ESTILO = "com curvas e fachadas de concreto branco, no estilo modernista de Brasilia"

# reconhece o token gerado pelo LLM em qualquer variacao: com/sem acento, maiusculas, espaco ou underline
PADRAO_TOKEN = re.compile(r'^(?:\s*estilo[_\s]*bras[ií]lia\s*,?\s*)+', re.IGNORECASE)


def expandir_tema(tema):
    exemplos = (
        "Tema: futebol de rua\n"
        "Resposta: estilo_brasilia, criancas jogando futebol em uma praca com pilotis de concreto branco ao fundo, tarde ensolarada\n\n"
        "Tema: chuva no cerrado\n"
        "Resposta: estilo_brasilia, fachada curva de concreto molhada pela chuva, ceu cinza sobre o cerrado\n\n"
        "Tema: noite de lua cheia\n"
        "Resposta: estilo_brasilia, cupula branca iluminada refletida no espelho d'agua sob a lua cheia\n\n"
    )
    instrucao = (
        f"{exemplos}"
        f"Tema: {tema}\n"
        f"Resposta:"
    )

    saida = expansor(
        instrucao,
        max_new_tokens=40,
        do_sample=True,
        temperature=0.7,
        return_full_text=False,
    )
    texto = saida[0]["generated_text"]

    # fica só com a primeira linha/frase gerada (o modelo pequeno as vezes continua divagando)
    texto = texto.strip().split("\n")[0].strip()
    if "." in texto:
        texto = texto.split(".")[0].strip()

    # remove qualquer variacao do token que o LLM tenha gerado sozinho (evita duplicar)
    texto = PADRAO_TOKEN.sub("", texto).strip()

    # o tema do usuario sempre entra literalmente no prompt - nao depende do LLM ter usado
    # ancora logo apos o token (inicio do prompt tende a ter mais peso de atencao no modelo)
    if texto:
        texto = f"{TOKEN_ESTILO} {ANCORA_ESTILO}, {tema}, {texto}"
    else:
        texto = f"{TOKEN_ESTILO} {ANCORA_ESTILO}, {tema}"

    return texto


@spaces.GPU
def gerar(tema):
    if not tema or not tema.strip():
        return "Digite um tema para começar.", None, None

    prompt = expandir_tema(tema)

    imagem = pipe(
        prompt,
        negative_prompt="desfocado, deformado, baixa qualidade",
        guidance_scale=7.5,
        num_inference_steps=30,
    ).images[0]

    audio = tts(prompt)

    return prompt, imagem, (audio["sampling_rate"], audio["audio"])


demo = gr.Interface(
    fn=gerar,
    inputs=gr.Textbox(
        label="Tema",
        placeholder="ex.: feira de domingo, futebol de rua, pôr do sol no lago...",
    ),
    outputs=[
        gr.Textbox(label="Prompt expandido"),
        gr.Image(label="Imagem gerada"),
        gr.Audio(label="Narração"),
    ],
    title="Ateliê Generativo — Arquitetura Modernista de Brasília",
    description=(
        "Digite um tema curto e veja-o reinterpretado no estilo da arquitetura "
        "modernista de Brasília, com narração em áudio. Projeto acadêmico — "
        "UniCEUB, disciplina de Modelos Multimodais."
    ),
)

if __name__ == "__main__":
    demo.launch()
