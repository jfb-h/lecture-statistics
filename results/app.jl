using Bonito, WGLMakie
import Bonito.DOM as D
using Tyler, Tyler.MapTiles
using Statistics, LinearAlgebra
using DataFrames, SQLite, DBInterface

include("theme.jl")
include("components.jl")
include("livingcost.jl")
include("earnings.jl")
include("tyler.jl")

WGLMakie.activate!(; resize_to=:parent)
set_theme!(ThemeClean())

db = "../lecture-surveys/surveys.db"
proxy_url = "https://surveys.eggroup-lmu.de/statlecture-results/"

con = SQLite.DB(db)

server = Server("0.0.0.0", 8080; proxy_url)
route!(server, "/wohnen" => livingcost(con))
route!(server, "/einkommen" => earnings(con))
route!(server, "/wohnort-aktuell" => place_current(con))
route!(server, "/wohnort-vorher" => place_before(con))
server

