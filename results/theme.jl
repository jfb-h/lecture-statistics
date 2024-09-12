WGLMakie.activate!(; resize_to=:parent)

const SCATTER_ARGS = (color=(:black, 0.0), strokewidth=4, strokecolor=(:crimson, .8))  

function ThemeClean()
    Theme(
        fontsize=24,
        figure_padding=(60, 100, 30, 30),
        justification=:left,
        Axis=(titlecolor=:grey20, titlealign=:left, titlesize=30, titlefont=:bold,
            # xtrimspine=true, ytrimspine=true,
            topspinevisible=false, rightspinevisible=false,
            ygridstyle=:dash, xgridstyle=:dash, xminorgridvisible=true,
            yminorgridvisble=true, xminorgridstyle=:dash, yminorgridstyle=:dash),
        Legend=(marker=:rect, markersize=28,),
        Scatter=(markersize=20,),
    )
end
