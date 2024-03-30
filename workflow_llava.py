"""
VL Model: Llava
Language Model: Codellama
"""
import argparse
import json
from agents.query_expansion_agent import QueryExpansionAgent
from agents.plot_agent import PlotAgent
from agents.visual_refine_agent import VisualRefineAgent
import logging
import os
import shutil
import glob
import time
parser = argparse.ArgumentParser()
parser.add_argument('--workspace', type=str, default='./workspace')
parser.add_argument('--model_type', type=str, default= 'codellama')# 'gpt-3.5-turbo')
parser.add_argument('--visual_refine', type=bool, default=True)
parser.add_argument('--vl_model',type=str,default='llava')#'gpt-4v-preview')
args = parser.parse_args()

def mainworkflow(test_sample_id, workspace, max_try=3):
    # Query expanding
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
    
    query_expansion_agent = QueryExpansionAgent(expert_instruction, simple_instruction,model_type=args.model_type)
    expanded_simple_instruction = query_expansion_agent.run('simple')
    logging.info('=========Expanded Simple Instruction=========')
    logging.info(expanded_simple_instruction)
    logging.info('=========Plotting=========')

    # GPT-4 Plot Agent
    # Initial plotting
    action_agent = PlotAgent(config, expanded_simple_instruction)
    logging.info('=========Novice 4 Plotting=========')
    novice_log, novice_code = action_agent.run_initial(args.model_type, 'novice.png')
    logging.info(novice_log)
    logging.info('=========Original Code=========')
    logging.info(novice_code)
    if not os.path.exists(f'{directory}/novice.png'): ## simulate 
        shutil.copy(f'./benchmark_data/ground_truth/example_{test_sample_id}.png', f'{directory}/novice.png')
        logging.info(f'Copied ground truth to {directory}/novice.png')
    if args.visual_refine:
        print('Use original code for visual feedback')
        visual_refine_agent = VisualRefineAgent('novice.png', config, '', simple_instruction)
        visual_feedback = visual_refine_agent.run(args.vl_model, 'novice', 'novice_final.png')
        logging.info('=========Visual Feedback=========')
        logging.info(visual_feedback)
        final_instruction = '' + '\n\n' + visual_feedback
        action_agent = PlotAgent(config, final_instruction)
        novice_log, novice_code = action_agent.run_vis(args.model_type, 'novice_final.png')
        logging.info(novice_log)

if __name__ == "__main__":
    workspace_base = args.workspace
    if not os.path.exists(workspace_base):
        os.mkdir(workspace_base)
    logging.basicConfig(level=logging.INFO, filename=f'{workspace_base}/workflow.log', filemode='w+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    for i in range(1,101):
        cur_time = []
        for _ in range(3):
            st = time.time()
            mainworkflow(i, workspace_base)
            cur_time.append(time.time()-st)
        logging.info(f"Time taken for sample {i}: {cur_time}, average: {sum(cur_time)/3}")
