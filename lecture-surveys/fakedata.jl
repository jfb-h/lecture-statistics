using SQLite
using DBInterface
using Printf: @sprintf

function simulate_latlon()
    # Germany
    ger_lat_min = 47.2701
    ger_lat_max = 55.0581
    ger_lon_min = 5.8663
    ger_lon_max = 15.0419

    # Munich
    muc_lat_min = 48.008
    muc_lat_max = 48.247
    muc_lon_min = 11.400
    muc_lon_max = 11.726

    lat_current = rand() * (muc_lat_max - muc_lat_min) + muc_lat_min
    lon_current = rand() * (muc_lon_max - muc_lon_min) + muc_lon_min

    lat_before = rand() * (ger_lat_max - ger_lat_min) + ger_lat_min
    lon_before = rand() * (ger_lon_max - ger_lon_min) + ger_lon_min

    (; lat_current, lon_current,
        lat_before, lon_before,
        place_current="",
        place_before=""
    )
end

function simulate_time()
    time = @sprintf("%02d:%02d", rand(5:7), rand(0:59))
    (; time)
end

const SUBJECTS = [
    "Biologie",
    "Gephysik",
    "Experimentalphysik",
    "Meteorologie",
    "Statistik",
    "Informatik",
    "KI",
    "Soziologie",
    "Politik",
    "VWL",
    "BWL",
    "Andere",
]

const GRADEMEANS = float.(rand(6:12, length(SUBJECTS)))

function simulate_minor()
    (; minor=rand(SUBJECTS))
end

function simulate_grade(subject)
    s = findfirst(==(subject), SUBJECTS)
    subjm = GRADEMEANS[s]
    grade = min(Int(floor(subjm + randn() * 2)), 15)
    (; grade)
end

function simulate_data(n::Int)
    return map(1:n) do i
        minor = simulate_minor()
        merge(
            (; id=i),
            simulate_latlon(),
            simulate_time(),
            minor,
            simulate_grade(minor.minor),
        )
    end
end

function (@main)(args)
    n = parse(Int, only(args))
    table = simulate_data(n)
    con = SQLite.DB("surveys.db")
    DBInterface.execute(con, """DELETE FROM wohnort;""")
    table |> SQLite.load!(con, "wohnort"; replace=true)
    return 1
end
