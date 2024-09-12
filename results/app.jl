using Bonito
import Bonito.DOM as D
using WGLMakie
using Statistics
using TidierDB, SQLite
import TidierData as TD

#TODO: page_html could be good for sharing slides afterwards

include("components.jl")
include("theme.jl")
include("livingcost.jl")
set_theme!(ThemeClean())

db = "../surveys/surveys.db"
proxy_url = "https://surveys.eggroup-lmu.de/statlecture-results/"
con = connect(sqlite(), db)
server = Server("0.0.0.0", 8080; proxy_url)
route!(server, "/session-01" => livingcost(con))
server

