from fasthtml.common import *

app, rt = fast_app(live=True)

def route1():
    @rt('/sess/test')
    def get(): return Div(P('Hello World!'), hx_post='/statlecture/sess/test')

    @rt('/sess/test')
    def post(): return P('Nice to be here!')

def route2():
    @rt('/sess/test2')
    def get(): return Div(P('Hello Moon!'), hx_post='/statlecture/sess/test2')

    @rt('/sess/test2')
    def post(): return P('Nice to be on the moon!')

route1()
route2()
serve(port=8081)

