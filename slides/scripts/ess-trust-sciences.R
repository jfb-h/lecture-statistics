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

data <- read_csv("data/CRON2W5e01/CRON2W5e01.csv")

lvls <- c(
  "No trust\nat all",
  1, 2, 3, 4, 5, 6, 7, 8, 9,
  "Complete\ntrust"
)

svy <- data |>
  as_survey_design(
    ids = idno,
    weights = c2weight
  ) |>
  select(
    cntry, c2weight,
    Medizin = w5q7,
    Umweltwissenschaften = w5q9,
    Physik = w5q6,
  )

svy_counts <- function(df, name) {
  colname <- as_string(ensym(name))
  df |>
    group_by({{ name }}) |>
    srvyr::survey_tally() |>
    filter({{ name }} != 99) |>
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

labels <- c(
  Physik = num_summary(svy_counts(svy, Physik), "Physik"),
  Medizin = num_summary(svy_counts(svy, Medizin), "Medizin"),
  Umweltwissenschaften = num_summary(
    svy_counts(svy, Umweltwissenschaften), "Umweltwissenschaften"
  )
)

rbind(
  svy_counts(svy, Medizin),
  svy_counts(svy, Physik),
  svy_counts(svy, Umweltwissenschaften)
) |>
  ggplot(aes(value, n, group = field)) +
  geom_bar(stat = "identity", fill = "tomato") +
  facet_wrap(~field, ncol = 1, labeller = as_labeller(labels)) +
  labs(
    x = NULL,
    y = "Häufigkeit",
    title = "Vertrauen in die Wissenschaften",
    subtitle = "European Social Survey, Items w5q7, w5q8, w5q9",
    caption = "ESS CRONOS 2 Wave 5"
  ) +
  theme(legend.position = "none")
