MODEL_NAME = "Qwen/Qwen2.5-3B-Instruct"

USE_VLLM = False


# ==========================
# TRY VLLM
# ==========================

try:

    from vllm import LLM
    from vllm import SamplingParams

    model = LLM(
        model=MODEL_NAME,
        trust_remote_code=True,
        gpu_memory_utilization=0.70
    )

    USE_VLLM = True

    print("vLLM Loaded")

except Exception as e:

    print("vLLM failed → using transformers")
    print(e)


# ==========================
# FALLBACK
# ==========================

if not USE_VLLM:

    from transformers import (
        AutoTokenizer,
        AutoModelForCausalLM,
        pipeline
    )

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    hf_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        device_map="auto"
    )

    hf_pipe = pipeline(
        "text-generation",
        model=hf_model,
        tokenizer=tokenizer
    )

    print("Transformers Loaded")


# ==========================
# SINGLE API
# ==========================

def llm(
    prompt,
    max_new_tokens=100
):

    if USE_VLLM:

        params = SamplingParams(
            max_tokens=max_new_tokens,
            temperature=0.2
        )

        output = model.generate(
            [prompt],
            params
        )

        return [
            {
                "generated_text":
                output[0]
                .outputs[0]
                .text
            }
        ]

    else:

        output = hf_pipe(
            prompt,
            max_new_tokens=max_new_tokens,
            do_sample=False
        )

        return [
            {
                "generated_text":
                output[0][
                    "generated_text"
                ]
            }
        ]