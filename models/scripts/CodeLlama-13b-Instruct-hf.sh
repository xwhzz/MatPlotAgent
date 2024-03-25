CUDA_VISIBLE_DEVICES=4,5 python -m vllm.entrypoints.openai.api_server \
    --model /data/xwh/CodeLlama-13b-Instruct-hf \
    --port=8006 \
    --tensor-parallel-size 2