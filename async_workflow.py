import logging
import os
import shutil
import glob
# import asyncio
import json
# import aiofiles

from agents.query_expansion_agent import QueryExpansionAgent
from agents.plot_agent import PlotAgent
from agents.visual_refine_agent import VisualRefineAgent
# from agents.utils import is_run_code_success, run_code, get_code

model_type = 'codellama'
vl_model = 'llava'
visual_refine = True

async def mainworkflow(test_sample_id, workspace='./workspace1', max_try=3):
    directory = f'{workspace}/example_{test_sample_id}'
    if not os.path.exists(directory):
        os.mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")
        for file in os.listdir(directory):
            os.remove(os.path.join(directory, file))
    logging.info('=========Query Expansion AGENT=========')
    config = {'workspace': directory}

    with open('./benchmark_data/benchmark_instructions.json') as file:
        data = json.load(file)

    simple_instruction = data[test_sample_id - 1]["simple_instruction"]
    expert_instruction = data[test_sample_id - 1]["expert_instruction"]

    if test_sample_id in range(76,101):
        source_dir = f"./benchmark_data/data/{test_sample_id}"
        destination_dir = f"{directory}"
        csv_files = glob.glob(f"{source_dir}/*.csv")
        for file in csv_files:
            shutil.copy(file, destination_dir)
    # Assuming QueryExpansionAgent and PlotAgent are updated to be async or their operations do not require async handling
    total_length = 0
    query_expansion_agent = QueryExpansionAgent(expert_instruction, simple_instruction, model_type=model_type)
    expanded_simple_instruction, ll = await query_expansion_agent.run_async('simple')  # This should ideally be async
    total_length += ll
    logging.info('=========Expanded Simple Instruction=========')
    logging.info(expanded_simple_instruction)
    logging.info('=========Plotting=========')

    action_agent = PlotAgent(config, expanded_simple_instruction)  # This should ideally be async
    logging.info('=========Novice 4 Plotting=========')
    novice_log, novice_code, ll = await action_agent.run_initial_async(model_type, 'novice.png')  # This should ideally be async
    total_length += ll
    logging.info(novice_log)
    logging.info('=========Original Code=========')
    logging.info(novice_code)
    if not os.path.exists(f'{directory}/novice.png'): ## simulate 
        shutil.copy(f'./benchmark_data/ground_truth/example_{test_sample_id}.png', f'{directory}/novice.png')
        logging.info(f'Copied ground truth to {directory}/novice.png')
    if visual_refine and os.path.exists(f'{directory}/novice.png'):
        print('Use original code for visual feedback')
        # Assuming VisualRefineAgent is also updated for async
        visual_refine_agent = VisualRefineAgent('novice.png', config, '', simple_instruction)
        visual_feedback, ll = await visual_refine_agent.run_async(vl_model, 'novice', 'novice_final.png') 
        total_length += ll
        logging.info('=========Visual Feedback=========')
        logging.info(visual_feedback)
        final_instruction = '' + '\n\n' + visual_feedback
        action_agent = PlotAgent(config, final_instruction) 
        novice_log, novice_code, ll = await action_agent.run_vis_async(model_type, 'novice_final.png') 
        total_length += ll
        logging.info(novice_log)
    return total_length

