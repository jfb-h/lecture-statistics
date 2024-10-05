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

# Styled Cards and Grids

def StyledCard(*items, header=None, footer=None):
    return Card(*items, header=header, footer=footer,
        style="display: flex; flex-direction: column; height: 95%; width: 100%;",
    )

def StyledGrid(*items, columns="1fr"):
    return Grid(*items,
        style = f"grid-template-columns: {columns}; grid-template-rows: none; height: 95vh"
    )


# Numeric input

def NumericInput(name, title, min, max):
    tit = Legend(Strong(title))
    inp = Input(type="number", name=name, min=min, max=max)
    return Card(Group(tit, inp))

# Time input

def TimeInput(name, title, placeholder):
    tit = Legend(Strong(title))
    inp = Input(type="time", name=name, placeholder=placeholder)
    return Card(Group(tit, inp))

# Text input

def TextInput(name, title, placeholder):
    tit = Legend(Strong(title))
    inp = Input(type="text", name=name, placeholder=placeholder)
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

# SelectInput

def SelectInput(name, title, *options):
    return Card(
        Legend(Strong(title)),
        Select(*options, name=name)
    )


# Choice items

def Check(name, desc):
    return Label(Input(type="checkbox", name=name, value="1"), desc)

def Radio(name, value, desc):
    return Label(Input(type="radio", name=name, value=value), desc)

def Choice(*options, title):
    return Card(Fieldset(Legend(Strong(title)), *options))


# Plot container

def PlotContainer(id):
    return Div(id=id, style="padding: 20px; flex-grow: 1; height: 0;")

# QRCode generation

def QRCode(session):
    qr = qrcode.QRCode(version=2, box_size=35, border=2, image_factory=qrcode.image.svg.SvgPathImage)
    qr.add_data(f"https://surveys.eggroup-lmu.de/statlecture/{session}")
    img = qr.make_image()
    return NotStr(img.to_string().decode())

