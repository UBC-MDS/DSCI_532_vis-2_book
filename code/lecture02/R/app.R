library(shiny)
library(bslib)
library(dplyr)
library(plotly)
library(ggridges)
library(ggplot2)

# Load data
tips <- read.csv(
  "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv"
)

# UI
ui <- page_fillable(
  title = "Restaurant tipping",
  layout_sidebar(
    sidebar = sidebar(
      sliderInput(
        inputId = "slider",
        label = "Bill amount",
        min = min(tips$total_bill),
        max = max(tips$total_bill),
        value = c(min(tips$total_bill), max(tips$total_bill))
      ),
      checkboxGroupInput(
        inputId = "checkbox_group",
        label = "Food service",
        choices = c("Lunch", "Dinner"),
        selected = c("Lunch", "Dinner")
      ),
      actionButton("action_button", "Reset filter"),
      open = "desktop"
    ),
    layout_columns(
      value_box(
        title = "Total tippers",
        value = textOutput("total_tippers")
      ),
      value_box(
        title = "Average tip",
        value = textOutput("average_tip")
      ),
      value_box(
        title = "Average bill",
        value = textOutput("average_bill")
      ),
      fill = FALSE
    ),
    layout_columns(
      card(
        card_header("Tips data"),
        dataTableOutput("tips_data"),
        full_screen = TRUE
      ),
      card(
        card_header("Total bill vs tip"),
        plotlyOutput("scatterplot"),
        full_screen = TRUE
      ),
      col_widths = c(6, 6)
    ),
    layout_columns(
      card(
        card_header("Tip percentages"),
        plotlyOutput("ridge"),
        full_screen = TRUE
      )
    )
  )
)

# Server
server <- function(input, output, session) {
  filtered_data <- reactive({
    tips %>%
      filter(
        total_bill >= input$slider[1],
        total_bill <= input$slider[2],
        time %in% input$checkbox_group
      )
  })

  output$total_tippers <- renderText({
    as.character(nrow(filtered_data()))
  })

  output$average_tip <- renderText({
    perc <- filtered_data()$tip / filtered_data()$total_bill
    paste0(sprintf("%.1f", mean(perc) * 100), "%")
  })

  output$average_bill <- renderText({
    bill <- mean(filtered_data()$total_bill)
    paste0("$", sprintf("%.2f", bill))
  })

  output$tips_data <- renderDataTable({
    filtered_data()
  })

  output$scatterplot <- renderPlotly({
    plot_ly(
      data = filtered_data(),
      x = ~total_bill,
      y = ~tip,
      type = "scatter",
      mode = "markers"
    ) %>%
      add_lines(
        y = ~ fitted(loess(tip ~ total_bill, data = filtered_data())),
        line = list(color = "red"),
        name = "LOWESS"
      )
  })

  output$ridge <- renderPlotly({
    df <- filtered_data() %>%
      mutate(percent = tip / total_bill)

    p <- ggplot(df, aes(x = percent, y = day, fill = day)) +
      geom_density_ridges(bandwidth = 0.01) +
      scale_fill_viridis_d() +
      theme_minimal() +
      theme(legend.position = "top")

    ggplotly(p)
  })
}

# Create app
shinyApp(ui = ui, server = server)
