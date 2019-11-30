library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(tidyverse)
library(plotly)

app <- Dash$new()

colors <- list(
  text = '#0013a3'
)

textStyle = list(
  textAlign = 'center',
  color = colors$text
)

graph <- dccGraph(
  id = 'dsci-graph',
  figure=ggplotly(p)
  )

footerText <- "We can display some text using *Markdown*. 

- Point 1
- Point 2
"

app$layout(
  htmlDiv(
    list(
      htmlH1('Hello Dash', style = textStyle),
      htmlH2('This is our R Dashboard', style = textStyle),
      dccMarkdown(children=footerText, style=list(color = colors$text)),
      htmlDiv(children = "Let's make a graph!", style = textStyle),
      graph
    )
  )
)

app$run_server()