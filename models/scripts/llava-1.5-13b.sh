CUDA_VISIBLE_DEVICES=6,7 python -m vllm.entrypoints.openai.api_server \
    --model /data/xwh/llava-1.5-13b-hf \
    --port=8000 \
    --tensor-parallel-size 2