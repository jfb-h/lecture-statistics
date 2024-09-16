using Bonito
import Bonito.DOM as D
using WGLMakie
using Statistics
using TidierDB, SQLite
import TidierData as TD

include("theme.jl")
include("components.jl")
include("livingcost.jl")
include("earnings.jl")
set_theme!(ThemeClean())

db = "../lecture-surveys/surveys.db"
proxy_url = "https://surveys.eggroup-lmu.de/statlecture-results/"

con = connect(sqlite(); db)

server = Server("0.0.0.0", 8080; proxy_url)
route!(server, "/wohnen" => livingcost(con))
route!(server, "/einkommen" => earnings(con))
server

