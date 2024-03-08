import os
import base64
from pyexpat import model
import re
import traceback
import pdb
from typing import List

from models.llava import completion_for_llava
# from base_agent import BaseAgent
from .prompt import SYSTEM_PROMPT, USER_PROMPT, ERROR_PROMPT
from agents.openai_chatComplete import completion_with_backoff, completion_with_log, completion_for_4v
from agents.utils import fill_in_placeholders, get_error_message, is_run_code_success, run_code
from agents.utils import print_filesys_struture
from agents.utils import change_directory


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_code(response):
    # 匹配所有在```python和```之间的代码块
    all_python_code_blocks_pattern = re.compile(r'```python\s*([\s\S]+?)\s*```', re.MULTILINE)

    # 提取所有代码块并连接在一起
    all_code_blocks = all_python_code_blocks_pattern.findall(response)
    all_code_blocks_combined = '\n'.join(all_code_blocks)
    return all_code_blocks_combined


class VisualRefineAgent:
    def __init__(self, plot_file, config, code, query):
        self.chat_history = []
        self.plot_file = plot_file
        self.code = code
        self.query = query
        self.workspace = config['workspace']

    def run(self, model_type, query_type, file_name):
        plot = os.path.join(self.workspace, self.plot_file)
        if model_type=='gpt-4':
            base64_image1 = encode_image(f"{plot}")

            information = {
                'query': self.query,
                'file_name': file_name,
                'code': self.code
            }

            messages = []
            messages.append({"role": "system", "content": fill_in_placeholders(SYSTEM_PROMPT, information)})
            messages.append({"role": "user",
                            "content": [fill_in_placeholders(USER_PROMPT, information),
                                        {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image1}"
                                        }
                                        },
                                        ]
                            })
            # pdb.set_trace()
            visual_feedback = completion_for_4v(messages, 'gpt-4-vision-preview')

            return visual_feedback
        elif model_type=='llava':
            information = {
                'query': self.query,
                'file_name': file_name,
                'code': self.code
            }

            messages = []
            messages.append({"role": "system", "content": fill_in_placeholders(SYSTEM_PROMPT, information)})
            messages.append({"role": "user","content": fill_in_placeholders(USER_PROMPT, information)})
            visual_feedback = completion_for_llava(messages,plot )

            return visual_feedback

        '''self.chat_history.append({"role": "assistant", "content": visual_refined_code})
        try_count = 0
        while try_count < 2:
            if model_type == 'gpt-3.5-turbo':
                # pdb.set_trace()
                code = get_code(visual_refined_code)
                if code == '':
                    code = visual_refined_code
            else:
                code = get_code(visual_refined_code)
            # write code to workspace and run
            # print(code)

            file_name = f'code_action_{model_type}_{query_type}_vis_refined.py'
            with open(os.path.join(self.workspace, file_name), 'w') as f:
                f.write(code)
            error = None
            log = run_code(self.workspace, file_name)

            if is_run_code_success(log):
                if print_filesys_struture(self.workspace).find('.png') == -1:
                    log = log + '\n' + 'No plot generated.'
                    self.chat_history.append({"role": "user", "content": 'No plot generated.'})
                    try_count += 1
                    result = ""

                else:
                    return log

            else:
                error = get_error_message(log) if error is None else error
                # TODO error prompt
                self.chat_history.append({"role": "user", "content": fill_in_placeholders(ERROR_PROMPT,
                                         {'error_message': error})})
                try_count += 1
                result = completion_with_backoff(self.chat_history, model_type=model_type)
                print(result)

        return log'''