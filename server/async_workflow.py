import logging
import os
import shutil
import glob
import asyncio
import aiofiles

from agents.query_expansion_agent import QueryExpansionAgent
from agents.plot_agent import PlotAgent
from agents.visual_refine_agent import VisualRefineAgent
from agents.utils import is_run_code_success, run_code, get_code


model_type = 'codellama'
vl_model = 'llava'
visual_refine = True

async def async_mkdir(path):
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, os.makedirs, path, exist_ok=True)

async def copy_files_async(source_dir, destination_dir):
    csv_files = glob.glob(f"{source_dir}/*.csv")
    for file in csv_files:
        await asyncio.get_event_loop().run_in_executor(None, shutil.copy, file, destination_dir)

async def mainworkflow(test_sample_id, workspace='./workspace', max_try=3):
    # Query expanding
    directory = f'{workspace}/example_{test_sample_id}'
    if not os.path.exists(directory):
        await async_mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")
    logging.info('=========Query Expansion AGENT=========')
    config = {'workspace': directory}

    async with aiofiles.open('./benchmark_data/benchmark_instructions.json', mode='r') as file:
        data = await file.json()
    simple_instruction = data[test_sample_id - 1]["simple_instruction"]
    expert_instruction = data[test_sample_id - 1]["expert_instruction"]

    # Copy CSV files
    if test_sample_id in range(76, 101):
        source_dir = f"./benchmark_data/data/{test_sample_id}"
        destination_dir = directory
        await copy_files_async(source_dir, destination_dir)
    
    # Assuming QueryExpansionAgent and PlotAgent are updated to be async or their operations do not require async handling
    query_expansion_agent = QueryExpansionAgent(expert_instruction, simple_instruction, model_type=args.model_type)
    expanded_simple_instruction = await query_expansion_agent.run_async('simple')  # This should ideally be async
    logging.info('=========Expanded Simple Instruction=========')
    logging.info(expanded_simple_instruction)
    logging.info('=========Plotting=========')

    action_agent = PlotAgent(config, expanded_simple_instruction)  # This should ideally be async
    logging.info('=========Novice 4 Plotting=========')
    novice_log, novice_code = await action_agent.run_initial_async(model_type, 'novice.png')  # This should ideally be async
    logging.info(novice_log)
    logging.info('=========Original Code=========')
    logging.info(novice_code)
    
    if visual_refine and os.path.exists(f'{directory}/novice.png'):
        print('Use original code for visual feedback')
        # Assuming VisualRefineAgent is also updated for async
        visual_refine_agent = VisualRefineAgent('novice.png', config, '', simple_instruction)
        visual_feedback = await visual_refine_agent.run_async(vl_model, 'novice', 'novice_final.png') 
        logging.info('=========Visual Feedback=========')
        logging.info(visual_feedback)
        final_instruction = '' + '\n\n' + visual_feedback
        action_agent = PlotAgent(config, final_instruction) 
        novice_log, novice_code = await action_agent.run_vis_async(model_type, 'novice_final.png') 
        logging.info(novice_log)


# if __name__ == "__main__":
#     ## /home/xwh/MatPlotAgent/workspace /workflow.log
#     workspace_base = args.workspace
#     logging.basicConfig(level=logging.INFO, filename=f'{workspace_base}/workflow.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
#     for i in range(3,101):
#         mainworkflow(i, workspace_base)
