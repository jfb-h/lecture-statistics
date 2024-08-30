from fasthtml.common import *
import qrcode
import qrcode.image.svg

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

def QRCode(session):
    qr = qrcode.QRCode(version=2, box_size=30, border=2,
                       image_factory=qrcode.image.svg.SvgPathImage)
    qr.add_data(f'https://surveys.eggroup-lmu.de/statlecture/{session}')
    img = qr.make_image()
    return NotStr(img.to_string().decode())
