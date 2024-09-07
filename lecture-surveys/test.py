from fasthtml.common import *

app, rt = fast_app(live=True)

@rt('/sess/test')
def get(): return Div(P('Hello World!'), hx_post='/statlecture/sess/test')

@rt('/sess/test')
def get(): return P('Nice to be here!')

serve(port=8081)

