library(dplyr)
library(tidyr)
library(readr)
library(ggplot2)
library(ggthemes)
library(viridis)
library(patchwork)
library(posterior)

theme_set(theme_tufte(base_family = "Arial"))

theme_update(
  axis.title.x = element_text(hjust = 0.99),
  axis.title.y = element_text(hjust = 0.99),
  plot.title = element_text(face = "bold"),
  plot.caption = element_text(face = "italic"),
  strip.text.x = element_text(hjust = 0.01, face = "bold"),
  strip.text.y = element_text(vjust = 0.01, face = "bold"),
  legend.position = "top",
  legend.justification.top = "left"
)

data <- read_csv("data/ESS10/ESS10.csv")

lvls <- c(
  "No trust\nat all",
  1, 2, 3, 4, 5, 6, 7, 8, 9,
  "Complete\ntrust"
)

svy <- data |>
  as_survey_design(
    ids = psu,
    strata = stratum,
    weights = anweight,
    nest = TRUE
  ) |>
  select(
    Wissenschaft = trstsci,
    Politik = trstplt
  )

svy_counts <- function(df, name) {
  colname <- as_string(ensym(name))
  df |>
    group_by({{ name }}) |>
    srvyr::survey_tally() |>
    filter(!{{ name }} %in% c(77, 88, 99)) |>
    mutate(
      field = colname,
      value = factor(
        {{ name }},
        levels = 0:10,
        labels = lvls,
        ordered = TRUE
      ),
      n = round(n)
    ) |>
    select(field, value, n)
}

num_summary <- function(df, name) {
  counts <- rep(df$value, df$n)
  paste0(
    name, " - ",
    "Median: ", median(as.numeric(counts) - 1),
    " | Entropie: ", round(entropy(counts), digits = 2),
    " | Dissens: ", round(dissent(counts), digits = 2)
  )
}

svy_pol <- svy_counts(svy, Politik)
svy_sci <- svy_counts(svy, Wissenschaft)

labels <- c(
  Politik = num_summary(svy_pol, "Politik"),
  Wissenschaft = num_summary(svy_sci, "Wissenschaft")
)

rbind(
  svy_pol,
  svy_sci
) |>
  ggplot(aes(value, n, group = field)) +
  geom_bar(stat = "identity", fill = "tomato") +
  facet_wrap(~field, ncol = 1, labeller = as_labeller(labels)) +
  geom_vline(aes(xintercept = median(as.numeric(value) - 1))) +
  labs(
    x = NULL,
    y = "Häufigkeit",
    title = "Vertrauen in Politik und Wissenschaft",
    subtitle = "European Social Survey, Items trstsci, trstplt",
    caption = "Quelle: ESS10"
  ) +
  theme(legend.position = "none")
