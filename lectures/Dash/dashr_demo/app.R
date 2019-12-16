library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)

app <- Dash$new()

library(plotly)

library(tidyverse)
district_density <- read.csv("https://raw.githubusercontent.com/plotly/datasets/master/district_density.csv",
                             stringsAsFactors = FALSE)
district_density$cluster <- factor(district_density$cluster, levels=c("Pure urban", "Urban-suburban mix", "Dense suburban", "Sparse suburban", "Rural-suburban mix", "Pure rural"))
district_density$region <- factor(district_density$region, levels=c("West", "South", "Midwest", "Northeast"))

p <- ggplot(district_density,aes(x=cluster, y=dem_margin, colour=region)) +
  geom_jitter(aes(text=paste("district: ", cd_code)), width=0.25, alpha=0.5, ) +
  geom_hline(yintercept=0) +
  theme(axis.text.x = element_text(angle = -30, hjust = 0.1)) +
  labs(title = "Democratic performance in the 2018 House elections, by region and density",
       x = "Density Index from CityLab",
       y = "Democratic Margin of Victory/Defeat")
p
#p <- ggplotly(p)

# Create a shareable link to your chart
# Set up API credentials: https://plot.ly/r/getting-started
#chart_link = api_create(p, filename="geom_jitter/basic-plot")
#chart_link


app$layout(
  htmlDiv(
    list(
      htmlH1('Hello Dash'),
      htmlDiv(children = "Dash: A web application framework for R."),
      dccGraph(
        figure=list(
          data=list(
            list(
              x=list(1, 2, 3),
              y=list(4, 1, 2),
              type='bar',
              name='SF'
            ),
            list(
              x=list(1, 2, 3),
              y=list(2, 4, 5),
              type='bar',
              name='Montr\U{00E9}al'
            )
          ),
          layout = list(title='Dash Data Visualization')
        )
      )
    )
  )
)

app$run_server()