#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
library(ggplot2)
library(ggthemes)
library(knitr)
library(gapminder)
library(dplyr)
library(forcats)
library(patchwork)
library(scales)
library(treemapify)
library(beeswarm)
library(stringr)

theme_set(theme_tufte(base_family = "GillSans"))

theme_update(
  axis.title.x = element_text(hjust = 0.99),
  axis.title.y = element_text(hjust = 0.99),
  plot.title = element_text(face = "bold"),
  plot.caption = element_text(face="italic"),
  strip.text.x = element_text(hjust = 0.01, face = "bold"),
  strip.text.y = element_text(vjust = 0.01, face = "bold"),
  legend.position = "top",
  legend.justification.top = "left"
)

#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
data <- tibble(x=LETTERS[1:5], y=sample(1:10, 5, replace=T))

data <- data |> 
  arrange(y) |>
  mutate(x=factor(x, levels=rev(x)))

p1 <- data |> 
  ggplot(aes(x=x, y=y)) + 
  geom_bar(fill="tomato", stat="identity") +
  labs(x=NULL, y=NULL)

p2 <- data |> 
  ggplot(aes(y=rep(1, 5), x=y/sum(y), fill=x)) + 
  geom_bar(
    color="white",
    stat="identity", 
    position=position_stack(reverse=T), 
    orientation="y", show.legend=F) +
  scale_x_continuous(labels = scales::percent) +
    scale_fill_tableau() +
  theme(
    axis.text.y=element_blank(),
    panel.grid.minor=element_blank(),
    panel.grid.major=element_blank(),
    legend.position="bottom") +
  labs(x=NULL, y=NULL, fill=NULL)

hsize <- 2.5

p3 <- data |>
  ggplot(aes(x=hsize, y=y/sum(y), fill=x)) +
  geom_col(color="white") +
  coord_polar(theta="y") +
  geom_text(
    aes(label = percent(y/sum(y))),
    position = position_stack(vjust = 0.5), 
    size=2.5, color="white") +
  xlim(c(0.2, hsize + 0.5)) +
    scale_fill_tableau() +
  theme_void() +
  labs(fill=NULL)

combined <- p1 + (p2 + p3 + plot_layout(nrow=2, heights=c(0.1, 0.9)))

combined + plot_annotation( tag_levels="A",
    title="Absolute und relative Häufigkeiten",
    subtitle=str_wrap("Säulendiagramm mit absoluten Häufigkeiten (A), gestapeltes Säulendiagramm
        mit relativen Häufigkeiten (B), Donut-Diagramm mit relativen Häufigkeiten (C).", 100)
)
#
#
#
#
data <- tibble(
    x = rnorm(1000),
    xexp = rexp(1000),
    xmix = c(rnorm(500, 0), rnorm(500, 4))
)

p4 <- data |>
    ggplot(aes(x = x)) +
    geom_histogram(bins = 30, color = "white", fill = "tomato") +
    labs(x = NULL, y = "Häufigkeit")

p5 <- data |>
    ggplot(aes(x = x)) +
    geom_density(lwd = 0.8, color = "white", fill = "tomato") +
    labs(x = NULL, y = "Dichte")

p6 <- data |>
    ggplot(aes(x = xexp)) +
    geom_histogram(bins = 30, color = "white", fill = "tomato") +
    labs(x = NULL, y = "Häufigkeit")

p7 <- data |>
    ggplot(aes(x = xexp)) +
    geom_density(lwd = 0.8, color = "white", fill = "tomato") +
    labs(x = NULL, y = "Dichte")

p8 <- data |>
    ggplot(aes(x = xmix)) +
    geom_histogram(bins = 30, color = "white", fill = "tomato") +
    labs(x = NULL, y = "Häufigkeit")

p9 <- data |>
    ggplot(aes(x = xmix)) +
    geom_density(lwd = 0.8, color = "white", fill = "tomato") +
    labs(x = NULL, y = "Dichte")

combined <- p4 + p5 + p6 + p7 + p8 + p9 + plot_layout(byrow = F)

combined + plot_annotation(
    tag_levels = "A",
    title = "Diskretisierte und stetige Häufigkeitsverteilungen",
    subtitle = str_wrap("Histogramme und Kerndichtediagramme für Daten mit unterschiedlichen
        Verteilungseigenschaften: Normalverteilt (A,B), rechtsschief (C,D), und bimodal (E,F).", 120)
)

#
#
#
#
data <- tibble(x=sample(LETTERS[1:5], 100, replace=T), y=sample(LETTERS[24:26], 100, replace=T))

p1 <- ggplot(data, aes(x=x, fill=y)) +
  geom_bar() +
  labs(x=NULL, y="Häufigkeit", fill=NULL) +
    scale_fill_tableau() +
  theme(legend.position="bottom") 

p2 <- ggplot(data, aes(x=x, fill=y)) +
  geom_bar(position="dodge") +
  labs(x=NULL, y="Häufigkeit", fill=NULL) +
    scale_fill_tableau() +
  theme(legend.position="bottom")

p3 <- ggplot(data, aes(x=x, fill=y)) +
  geom_bar(position="fill") +
  labs(x=NULL, y="Anteil", fill=NULL) +
    scale_fill_tableau() +
  theme(legend.position="bottom")

combined <- p1 + p2 + p3
combined + plot_annotation(
  tag_levels="A",
  title="Bivariate absolute und relative Häufigkeiten",
  subtitle=str_wrap("Gestapeltes Säulendiagramm mit Häufigkeiten (A), gruppiertes
        Säulendiagramm mit Häufigkeiten (B), normalisiertes Säulendiagramm mit relativen Häufigkeiten (C).", 150))
#
#
#
#
set.seed(123)
n = 200
data <- tibble(x=rnorm(n), y=sample(LETTERS[1:4], n, replace=T))
data <- data |> group_by(y) |> mutate(x = x + cur_group_id())

p1 <- data |>
  ggplot(aes(x=y, y=x)) +
  geom_boxplot(orientation = "x", fill="tomato") +
  labs(x=NULL, y=NULL)

p2 <- data |>
  ggplot(aes(x=x, fill=y)) + 
  geom_histogram(alpha=0.6, color="white") + 
    scale_fill_tableau() +
  labs(fill=NULL, x=NULL, y=NULL)

p3 <- data |>
  ggplot(aes(x=x, fill=y)) + 
  geom_density(alpha=0.6, color="white") + 
    scale_fill_tableau() +
  labs(fill=NULL, x=NULL, y=NULL)

p4 <- data |>
  ggplot(aes(x=y, y=x)) + 
  geom_dotplot(binaxis="y", stackdir="center", color="white", fill="tomato") + 
    scale_fill_tableau() +
  labs(fill=NULL, x=NULL, y=NULL) + 
  theme(legend.position="bottom")


combined <- p1 + p4 + (p2 / p3)

combined + 
  plot_layout(widths=c(0.2, 0.5, 0.3)) +
  plot_annotation(
      tag_levels="A",
      title="Vergleiche kontinuierlicher Variablen über Gruppen",
      subtitle=str_wrap("Boxplot (A)  und Punktdiagramm (b), Histogramm (C) und Kerndichtediagramm (D).", 150)
  )

#
#
#
#
#
#
#
#
library(ggridges)

# library(GSODR)
# data = get_GSOD(years=2013:2023, station="108660-99999") |> select(YEAR, MONTH, DAY, TEMP)
# data$MONTH = lubridate::month(data$MONTH, label=T, abbr=T)
# arrow::write_parquet(data, "data/temp_munich.parquet")

data = arrow::read_parquet("data/temp_munich.parquet")

ggplot(data, aes(x = TEMP, y = fct_rev(MONTH), fill=stat(x))) +
  geom_density_ridges_gradient(scale=4, rel_min_height=0.01, gradient_lwd = 1.0) +
  scale_y_discrete(expand=c(0,0)) +
  scale_x_continuous(expand=c(0,0)) +
  scale_fill_viridis_c(name="Temp. (C)", option="C") +
  coord_cartesian(clip="off") +
  labs(title="Monatsweise Temperaturen in München",
       subtitle="Aggregierte Tagesdurchschnittstemperaturen, 2013 - 2023",
       y="", x="Temperatur (C)") +
  theme_ridges()
#
#
#
#
data <- tibble(x=rnorm(2000), 
               y_lin=2*x + rnorm(2000, sd=3),
               y_sqr=2*x + x^2 + rnorm(2000, sd=3))

p1 <- data |>
  ggplot(aes(x, y_lin)) +
  geom_point(alpha=0.5, color="tomato") +
  geom_smooth(method="lm", color="black") +
  labs(x="", y="")

p2 <- data |>
  ggplot(aes(x, y_lin)) + 
  geom_bin2d() +
  labs(x="", y="") +
  theme(legend.position="right")

p3 <- data |>
  ggplot(aes(x, y_sqr)) +
  geom_point(alpha=0.5, color="tomato") +
  geom_smooth(method="gam", color="black") +
  labs(x="", y="")

p4 <- data |>
  ggplot(aes(x, y_sqr)) + 
  geom_bin2d() +
  labs(x="", y="") +
  theme(legend.position="right")

combined <- p1 + p2 + p3 + p4

combined + plot_annotation(
  tag_levels="A",
  title="",
  subtitle=str_wrap("Streudiagramme (A, C) und 2D-Histogramme (B,D) für lineare und nichtlineare Zusammenhänge.", 150)
)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
kable(head(gapminder, 10))
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| fig-width: 7
#| fig-height: 5

df = distinct(gapminder, country, continent)
ggplot(df, aes(fct_infreq(continent))) +
    geom_bar(fill="tomato") +
    labs(x="Kontinent",
        y="# Länder",
        title="Welcher Kontinent hat die meisten Länder?",
        caption="Quelle: gapminder.org")
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| fig-width: 8
#| fig-height: 6

df = distinct(gapminder, country, continent)
df = df |> group_by(continent) |> summarize(count=n(), share=n() / nrow(df))

hsize = 2.5

p1 = ggplot(df, aes(x=hsize, y=count, fill=continent)) +
    geom_col(color="white") +
    coord_polar(theta="y") +
    theme_void() +
    scale_fill_tableau() +
    labs(fill=NULL) +
    theme(legend.position="top")

p2 = ggplot(df, aes(x=hsize, y=count, fill=continent)) +
    geom_col(color="white", show.legend=FALSE) +
    coord_polar(theta="y") +
    xlim(c(0.2, hsize + 0.5)) +
    theme_void() +
    scale_fill_tableau()

p1 + p2 + plot_annotation(title="Welcher Kontinent hat die meisten Länder?")
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| fig-width: 7
#| fig-height: 5

library(likert)
data(pisaitems)

items28 = pisaitems[, substr(names(pisaitems), 1, 5) == "ST24Q"]
p = likert(items28)
plot(p) +
    labs(title="Pisa-Umfrage zum Leseverhalten", 
        subtitle="z.B. ST24Q01 = 'Ich lese nur wenn ich muss'"
    )
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| fig-width: 7
#| fig-height: 5

df = filter(gapminder, year == 2007)
ggplot(df, aes(x=gdpPercap)) +
    geom_histogram(color="white", fill="tomato", binwidth=2000) +
    scale_x_continuous(labels=label_currency(big.mark=" ")) +
    labs(title="Pro-Kopf-BIP (Landesdurchschnitt)", x="Pro-Kopf-BIP (USD)", y="# Länder")
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| fig-width: 7
#| fig-height: 5

df = filter(gapminder, year == 2007)
ggplot(df, aes(x=gdpPercap)) +
    geom_dotplot(color="white", fill="tomato", dotsize=0.5, binwidth=2000, method="histodot") +
    scale_x_continuous(labels=label_currency(big.mark=" ")) +
    theme(axis.ticks.y=element_blank(), axis.text.y=element_blank()) +
    labs(title="Pro-Kopf-BIP (Landesdurchschnitt)", x="Pro-Kopf-BIP (USD)", y="")
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| fig-width: 7
#| fig-height: 5

df = filter(gapminder, year == 2007)

p1 = ggplot(df, aes(x=gdpPercap)) +
    geom_histogram(color="white", fill="tomato", binwidth=2000) +
    scale_x_continuous(labels=label_currency(big.mark=" ")) +
    scale_y_continuous(labels=label_number(scale_cut=cut_short_scale())) +
    labs(title="Pro-Kopf-BIP (Landesdurchschnitt)", x="Pro-Kopf-BIP (USD)", y="# Länder")

p2 = ggplot(df, aes(x=gdpPercap, weight=pop)) +
    geom_histogram(color="white", fill="tomato", binwidth=2000) +
    geom_density(color="white", fill="tomato") +
    scale_x_continuous(labels=label_currency(big.mark=" ")) +
    scale_y_continuous(labels=label_number(scale_cut=cut_short_scale())) +
    labs(title="Pro-Kopf-BIP (Einwohnergewichtet)", x="Pro-Kopf-BIP (USD)", y="# Personen")

p1 / p2
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| fig-width: 7
#| fig-height: 5

p1 = ggplot(df, aes(x=gdpPercap)) +
    geom_density(color="white", fill="tomato") +
    scale_x_continuous(labels=label_currency(big.mark=" ")) +
    scale_y_continuous(labels=label_scientific()) +
    labs(title="Pro-Kopf-BIP (Landesdurchschnitt)", x="Pro-Kopf-BIP (USD)", y="Dichte")

p2 = ggplot(df, aes(x=gdpPercap, weight=pop)) +
    geom_density(color="white", fill="tomato") +
    scale_x_continuous(labels=label_currency(big.mark=" ")) +
    scale_y_continuous(labels=label_scientific()) +
    labs(title="Pro-Kopf-BIP (Einwohnergewichtet)", x="Pro-Kopf-BIP (USD)", y="Dichte")

p1 / p2
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| fig-width: 7
#| fig-height: 5

library(ggbeeswarm)

ggplot(df, aes(x=gdpPercap, y="")) +
    scale_x_continuous(labels=label_currency(big.mark=" ")) +
    geom_beeswarm(method="center", color = "tomato", cex=2) + 
    labs(title="Pro-Kopf-BIP (Einwohnergewichtet)", x="Pro-Kopf-BIP (USD)", y="")
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#| fig-width: 7
#| fig-height: 5

df = filter(gapminder, year == 2007)
ggplot(df, aes(area=pop, fill=continent, label=country, subgroup=continent)) +
    geom_treemap(color="white") +
    geom_treemap_text(place="topleft", colour="white", reflow=TRUE) +
    geom_treemap_subgroup_border(color="white") +
    geom_treemap_subgroup_text(place="center", grow=TRUE, fontface="italic", colour="black", alpha=0.1, min.size = 0) +
    scale_fill_tableau() +
    theme(legend.position="")
```
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
