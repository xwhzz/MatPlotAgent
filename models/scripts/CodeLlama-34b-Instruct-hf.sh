CUDA_VISIBLE_DEVICES=4,5,6,7 python -m vllm.entrypoints.openai.api_server \
    --model /data/xwh/CodeLlama-34b-Instruct-hf \
    --port=8006 \
    --tensor-parallel-size 4