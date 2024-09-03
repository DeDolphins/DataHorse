import pandas as pd
from groq import Groq
import re
import io
import streamlit as st
from textwrap import dedent
import matplotlib.pyplot as plt
from helper import save_uploaded_file
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px 
from IPython.display import display 
import os
# Initial Streamlit page configuration
st.set_page_config(
    page_title="DataHorse",
    page_icon="png.png",
    layout="wide",
)

# Initialize session state variables if they don't exist
if 'my_result' not in st.session_state:
    st.session_state.my_result = []

if 'history' not in st.session_state:
    st.session_state.history = []

# Settings and keys
verbose = False
mutable = False

model = 'llama3-8b-8192'
groq_api_key = os.getenv('APIKEY')
client = Groq(api_key=groq_api_key)

# Prompt template
template = '''
Write a Python function `process({arg_name})` which takes the following input value:

{arg_name} = {arg}

This is the function's purpose: {goal}
'''

_ask_cache = {}

class Ask:
    def __init__(self, *, verbose=None, mutable=None):
        self.verbose = verbose if verbose is not None else globals()['verbose']
        self.mutable = mutable if mutable is not None else globals()['mutable']

    @staticmethod
    def _fill_template(template, **kw):
        print("tempolateeeeeeeeeeeeeeeeee")
        print(template)
        print("templateeeeeeeeeeeeeeeeee")
        result = dedent(template.lstrip('\n').rstrip())
        for k, v in kw.items():
            result = result.replace(f'{{{k}}}', v)
        m = re.match(r'\{[a-zA-Z0-9_]*\}', result)
        if m:
            raise Exception(f'Expected variable: {m.group(0)}')
        return result

    def _get_prompt(self, goal, arg):
        if isinstance(arg, pd.DataFrame) or isinstance(arg, pd.Series):
            buf = io.StringIO()
            arg.info(buf=buf)
            arg_summary = buf.getvalue()
        else:
            arg_summary = repr(arg)
        arg_name = 'df' if isinstance(arg, pd.DataFrame) else 'index' if isinstance(arg, pd.Index) else 'data'

        return self._fill_template(template, arg_name=arg_name, arg=arg_summary.strip(), goal=goal.strip())

    def _run_prompt(self, prompt):
        cache = _ask_cache
        completion = cache.get(prompt) or client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Write the function in a Python code block with all necessary imports and no example usage.\n Note: I want to show the result in streamlit. Use df variable the data is already loaded in that.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            model=model,
        )
        cache[prompt] = completion
        return completion.choices[0].message.content

    def _extract_code_block(self, text):
        """
        Extracts code blocks from a string enclosed in triple backticks (```).

        Args:
            text (str): The input string containing code blocks.

        Returns:
            list of dict: A list of dictionaries, each containing the language and the code block.
        """
        # Regular expression to match code blocks with optional language identifiers
        code_block_pattern = re.compile(r'```(\w*)\n(.*?)```', re.DOTALL)
        
        # Find all code blocks
        matches = code_block_pattern.findall(text)
        
        # Format matches into a list of dictionaries
        code_blocks = [{'language': match[0], 'code': match[1]} for match in matches]
        
        return code_blocks[0]["code"]

    def _eval(self, source, *args):
        scope = dict(_args_=args)
        exec(self._fill_template('''
            {source}
            _result_ = process(*_args_)
        ''', source=source), scope)
        return scope['_result_']

    def _code(self, goal, arg):
        prompt = self._get_prompt(goal, arg)
        result = self._run_prompt(prompt)
        st.session_state.my_result.append(result)
        return self._extract_code_block(result)

    def code(self, *args):
        print(self._code(*args))

    def prompt(self, *args):
        print(self._get_prompt(*args))

    def __call__(self, goal, *args):
        source = self._code(goal, *args)
        return self._eval(source, *args)


@pd.api.extensions.register_dataframe_accessor('chat')
@pd.api.extensions.register_series_accessor('chat')
@pd.api.extensions.register_index_accessor('chat')
class AskAccessor:
    def __init__(self, pandas_obj):
        self._validate(pandas_obj)
        self._obj = pandas_obj

    @staticmethod
    def _validate(obj):
        pass

    def _ask(self, **kw):
        return Ask(**kw)

    def _data(self, **kw):
        if not mutable and not kw.get('mutable') and hasattr(self._obj, 'copy'):
            return self._obj.copy()
        return self._obj

    def __call__(self, goal, *args, **kw):
        ask = self._ask(**kw)
        data = self._data(**kw)
        return ask(goal, data, *args)

    def code(self, goal, *args, **kw):
        ask = self._ask(**kw)
        data = self._data(**kw)
        return ask.code(goal, data, *args)

    def prompt(self, goal, *args, **kw):
        ask = self._ask(**kw)
        data = self._data(**kw)
        return ask.prompt(goal, data, *args)


def read(file_path):
    try:
        return pd.read_csv(file_path)
    except UnicodeDecodeError:
        try:
            return pd.read_csv(file_path, encoding='utf-8')
        except Exception as e:
            print(f"Failed to read file with 'utf-8' encoding: {e}")
            return None
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
        return None
    except pd.errors.ParserError:
        print("Error: There was a problem parsing the file.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    

def extract_code_from_result(result):
    pattern = r'```(?:\s*(?:py|python)\s*)?\n([\s\S]*?)```'
    match = re.search(pattern, result)
    if match:
        return match.group(1)
    return result  


logo_path = 'png.png'
with st.sidebar:
    st.sidebar.image(logo_path, width=150)
    st.header("Upload Documents")
    uploaded_file = st.file_uploader("")
    if uploaded_file:
        df = save_uploaded_file(uploaded_file)
        st.success('file Upload Successfully')
    else:
        st.write('No files were uploaded')



def display():
    for i, code in enumerate(st.session_state.my_result):
        head = st.session_state.history[i]
        # st.text_area(f"Cell{i}", value=head, height=30)
        st.subheader(f'Output No {i+1}')
        
        st.code(head)
        
        code = extract_code_from_result(code)
        with st.expander("Review the Code", expanded=False):
            st.code(code)
        local_scope = {}
        exec(code, globals(), local_scope)

        if 'process' in local_scope:
            result = local_scope['process'](df)
            st.write(result)
        else:
            st.write("The 'process' function was not found in the generated code.")



def clear_text():
    st.session_state.my_text = st.session_state.widget
    st.session_state.widget = ""


st.text_input('Ask Question', key='widget', on_change=clear_text)
new_code = st.session_state.get('my_text', '')

if new_code:
    st.session_state.history.append(new_code)
    ask = df.chat.code(new_code)

display()


styl = """
<style>
    .stTextInput {
        bottom: 0px;
        background-color: var(--cell-background-light);
        position:fixed;
        color: var(--text-color-light);
        border-radius: 5px;
        z-index: 1000;
    }
    p{  
    }
</style>
"""
st.markdown(styl, unsafe_allow_html=True)


st.markdown("""
       <style>
.stTextArea textarea, .stCodeCell textarea {
        padding-left: 10px !important;
        font-size: 18px;  /* Increase font size */
        align-items: center;  /* Vertically center text */
        min-height: 55px !important;  /* Set a minimum height */
    }
   .row-widget {
    height: 120px;
    padding:20px;
            border-radius:-1px;;
    margin-top: 10px;
    background-color: rgb(14,17,23);
}
     </style>
# """, unsafe_allow_html=True)
