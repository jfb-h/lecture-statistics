from fasthtml.common import *

def Items(*args, port):
    return Form(Fieldset(*args, Button("Absenden")), hx_post=port)
    
def SliderLabel(label):
    return Label(label, style={"margin": "0px 10px"})

def LikertSlider(name):
    return Input(type="range", name=name, min="0", max="10", step="1", value="5")

def Slider(name, title, left, right):
    return Card(
        Legend(Strong(title)),
        Group(SliderLabel(left), LikertSlider(name), SliderLabel(right))
    )
