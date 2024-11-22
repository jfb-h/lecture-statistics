library(sp)
library(sf)
library(spdep)
library(tmap)

data(meuse, package = "sp")
meuse_sf <- st_as_sf(meuse, coords = c("x", "y"))

st_crs(meuse_sf) <- 28992
meuse_sf <- st_transform(meuse_sf, crs = 4326)

coords <- st_coordinates(meuse_sf)
nb <- knn2nb(knearneigh(coords, k = 4))
lw <- nb2listw(nb, style = "W")

moran.test(meuse_sf$zinc, lw)

tmap_mode("view")
tm_shape(meuse_sf) +
    tm_tiles("CartoDB.Positron") +
    tm_dots("zinc", size = 0.08)
