options(shiny.port = 8050, shiny.autoreload = TRUE)

library(shiny)


# No explicit initiatlization in Shiny

# Layout
ui <- fluidPage('I am alive')

# Server side callbacks/reactivity
server <- function(input, output, session) {}

# Run the app/dashboard
shinyApp(ui, server)