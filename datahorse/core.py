import pandas as pd
from groq import Groq
from .logger import Logger
import hashlib
import os

verbose = False
mutable = False
model = 'llama3-8b-8192'
groq_api_key = os.getenv("DATAHORSE_API_KEY")
client = Groq(api_key=groq_api_key)

template = '''
Write a Python function process({arg_name}) which takes the following input value:

{arg_name} = {arg}

This is the function's purpose: {goal}
'''

_ask_cache = {}

class Ask:
    def __init__(self, *, verbose=None, mutable=None, seed=None, cache_req=True):
        self.verbose = verbose if verbose is not None else globals()['verbose']
        self.mutable = mutable if mutable is not None else globals()['mutable']
        self.seed = seed if seed else None
        self.cache_req = cache_req

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
        try:
            if isinstance(arg, pd.DataFrame) or isinstance(arg, pd.Series):
                import io
                buf = io.StringIO()
                arg.info(buf=buf)
                arg_summary = buf.getvalue()
            else:
                arg_summary = repr(arg)
            arg_name = 'df' if isinstance(arg, pd.DataFrame) else 'index' if isinstance(arg, pd.Index) else 'data'

            return self._fill_template(template, arg_name=arg_name, arg=arg_summary.strip(), goal=goal.strip())
        except Exception as e:
            Logger().log({"title": "Get Prompt Failed", "details": str(e)})
            return ""

    def _clean_prompt(self, prompt):
        cleaned_content = prompt.split("This is the function's purpose:")[0]
        return cleaned_content.strip()

    def _hash_content(self, content):
        return hashlib.md5(content.encode()).hexdigest()

    def _run_prompt(self, prompt):
        try:
            cache = _ask_cache
            cleaned_content = self._clean_prompt(prompt)
            cache_key = self._hash_content(cleaned_content)

            if not self.cache_req:
                _ask_cache.clear()

            if cache_key in cache:
                return cache[cache_key]

            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "Write the function in a Python code block with all necessary imports and no example usage."},
                    {"role": "user", "content": prompt},
                ],
                model=model,
                seed=self.seed if self.seed is not None else None
            )

            response_content = completion.choices[0].message.content
            cleaned_code = self._extract_code_block(response_content)

            if self.cache_req and self.seed is not None:
                cache[cache_key] = cleaned_code

            return cleaned_code
        except Exception as e:
            Logger().log({"title": "Run Prompt Failed", "details": str(e)})
            return ""

    def _extract_code_block(self, text):
        try:
            import re
            pattern = r'```(?:py|python)?\n([\s\S]*?)```'
            m = re.search(pattern, text)
            if not m:
                return text
            code = m.group(1)
            code_lines = code.splitlines()
            if code_lines:
                min_indent = min((len(line) - len(line.lstrip())) for line in code_lines if line.strip())
                code = "\n".join(line[min_indent:] for line in code_lines)
            return code
        except Exception as e:
            Logger().log({"title": "Extract Code Failed", "details": str(e)})
            return ""

    def _eval(self, source, *args):
        try:
            _args_ = args
            scope = dict(_args_=args)
            exec(self._fill_template('''\
                {source}
                _result_ = process(*_args_)
            ''', source=source), scope)
            return scope['_result_']
        except Exception as e:
            Logger().log({"title": "Eval Failed", "details": str(e)})
            return None

    def _code(self, goal, arg):
        try:
            prompt = self._get_prompt(goal, arg)
            result = self._run_prompt(prompt)
            review = self._extract_code_block(result)
            Logger().log({"title": "Review Code", "details": review})
            return review
        except Exception as e:
            Logger().log({"title": "_Code Failed", "details": str(e)})
            return ""

    def code(self, *args):
        try:
            print(self._code(*args))
        except Exception as e:
            Logger().log({"title": "Code Failed", "details": str(e)})

    def prompt(self, *args):
        try:
            print(self._get_prompt(*args))
        except Exception as e:
            Logger().log({"title": "Prompt Failed", "details": str(e)})

    def __call__(self, goal, *args):
        try:
            source = self._code(goal, *args)
            return self._eval(source, *args)
        except Exception as e:
            Logger().log({"title": "Execution Failed", "details": str(e)})
            return None


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
        return Ask(
            verbose=kw.get('verbose'), 
            mutable=kw.get('mutable'), 
            seed=kw.get('seed'), 
            cache_req=kw.get('cache_req', True)
        )

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
        if file_path.lower().endswith(('.xlsx', '.xls')):
            return pd.read_excel(file_path)
        else:
            return pd.read_csv(file_path)
    except UnicodeDecodeError:
        try:
            if not file_path.lower().endswith(('.xlsx', '.xls')):
                return pd.read_csv(file_path, encoding='utf-8')
        except Exception as e:
            Logger().log({"title": "Read File Failed", "details": str(e)})
            return None
    except FileNotFoundError:
        Logger().log({"title": "File Not Found", "details": f"The file '{file_path}' was not found."})
        return None
    except pd.errors.EmptyDataError:
        Logger().log({"title": "Empty File", "details": "The file is empty or not a valid file."})
        return None
    except Exception as e:
        Logger().log({"title": "File Read Error", "details": str(e)})
        return None
