library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)

app <- Dash$new()

app$layout(
  htmlDiv(
    list(
      htmlH1('Hello Dash'),
      htmlH2('This is our R Dashboard'),
      htmlDiv(children = "Let's make a graph!"),
      dccGraph(
        figure=list(
          data=list(
            list(
              x=list("Lab 1", "Lab 2"),
              y=list(35, 22),
              type='bar',
              name='Data'
            ),
            list(
              x=list("Lab 1", "Lab 2"),
              y=list(15, 28),
              type='bar',
              name='Science'
            )
          ),
          layout = list(title='My favourite part of data science is the...')
        )
      )
    )
  )
)

app$run_server()