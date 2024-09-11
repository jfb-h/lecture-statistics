from fasthtml.common import *
import qrcode
import qrcode.image.svg


def Survey(title, items):
    return Titled(title, Hr(), items, style={"max-width": "600px"})

def Items(*args, hx_post):
    return Form(Fieldset(*args, Button("Absenden")), hx_post=hx_post)

def setup(db, rt, route, tablename, **kwargs):
    table = db.t[tablename]
    if table not in db.t:
        table.create( id=int, pk="id", **kwargs)

    Item = table.dataclass()

    @rt(f"/{route}")
    def post(item: Item):
        table.insert(item)
        return Strong("Danke für deine Antwort!")

    @rt(f"/{route}/qr")
    def get(): return QRCode(f"{route}")

# Numeric input

def NumericInput(name, title, min, max):
    tit = Legend(Strong(title))
    inp = Input(type="number", name=name, min=min, max=max)
    return Card(Group(tit, inp))


# Sliders

def SliderLabel(label):
    return Label(label, style={"margin": "0px 10px"})

def LikertSlider(name):
    return Input(type="range", name=name, min="0", max="10", step="1", value="5")

def Slider(name, title, left, right):
    return Card(
        Legend(Strong(title)),
        Group(SliderLabel(left), LikertSlider(name), SliderLabel(right)),
    )


# Multiple choice items

def Choice(label, desc):
    return Label(Input(type="Checkbox", name=label, value="1"), desc)

def MultiChoice(*options, title):
    return Card(Fieldset(Legend(Strong(title)), *options))


# QRCode generation

def QRCode(session):
    qr = qrcode.QRCode(version=2, box_size=30, border=2, image_factory=qrcode.image.svg.SvgPathImage)
    qr.add_data(f"https://surveys.eggroup-lmu.de/statlecture/{session}")
    img = qr.make_image()
    return NotStr(img.to_string().decode())
