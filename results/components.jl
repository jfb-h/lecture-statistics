function card(body...; header=nothing, footer=nothing)
    hdr = isnothing(header) ? header : D.header(header)
    ftr = isnothing(footer) ? footer : D.footer(footer)
    D.article(hdr, body..., ftr)
end

function grid(items...; columns="none", rows="none", height="90vh")
    style = "grid-template-columns: $columns; grid-template-rows: $rows; height: $height"
    D.div(items...; class="grid", style)
end

function titled(title, components...)
    l = D.link(rel="stylesheet", href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css")
    m = D.script(id="MathJax-script", src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js", async=true)
    t = D.title(title)
    head = D.head(l, t, m, D.meta(charset="UTF-8"))
    body = D.body(D.main(components...; class="container"))
    D.html(head, body)
end

function bignum(val; header=nothing, footer=nothing)
    card(D.strong(val); header, footer)
end

# helpers
L(s) = raw"\( " * s * raw" \)"
r(digits) = x -> round(x; digits)
