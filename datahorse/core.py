import pandas as pd
from groq import Groq

verbose = False 
mutable = False 

model = 'llama3-8b-8192'
groq_api_key = os.getenv('DATAHORSE_API_KEY')
client = Groq(api_key=groq_api_key)

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
        import re
        from textwrap import dedent
        result = dedent(template.lstrip('\n').rstrip())
        for k, v in kw.items():
            result = result.replace(f'{{{k}}}', v)
        m = re.match(r'\{[a-zA-Z0-9_]*\}', result)
        if m:
            raise Exception(f'Expected variable: {m.group(0)}')
        return result

    def _get_prompt(self, goal, arg):
        if isinstance(arg, pd.DataFrame) or isinstance(arg, pd.Series):
            import io
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
                    "content": "Write the function in a Python code block with all necessary imports and no example usage.",
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
        import re
        pattern = r'```(\s*(py|python)\s*\n)?([\s\S]*?)```'
        m = re.search(pattern, text)
        if not m:
            return text
        return m.group(3)

    def _eval(self, source, *args):
        _args_ = args
        scope = dict(_args_=args)
        exec(self._fill_template('''
            {source}
            _result_ = process(*_args_)
        ''', source=source), scope)
        return scope['_result_']

    def _code(self, goal, arg):
        prompt = self._get_prompt(goal, arg)
        result = self._run_prompt(prompt)
        if self.verbose:
            print()
            print(result)
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
        # Check the file extension to determine the file type
        if file_path.lower().endswith('.xlsx') or file_path.lower().endswith('.xls'):
            # Attempt to read an Excel file
            return pd.read_excel(file_path)
        else:
            # Attempt to read a CSV file
            return pd.read_csv(file_path)
    except UnicodeDecodeError:
        try:
            # Retry reading the CSV file with 'utf-8' encoding
            if not (file_path.lower().endswith('.xlsx') or file_path.lower().endswith('.xls')):
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
