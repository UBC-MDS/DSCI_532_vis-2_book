# Adding full interactivity

library(dash)
library(dashCoreComponents)
library(dashHtmlComponents)
library(dashTable)
library(tidyverse)
library(plotly)
library(gapminder)

app <- Dash$new(external_stylesheets = "https://codepen.io/chriddyp/pen/bWLwgP.css")

# Selection components
yearMarks <- lapply(unique(gapminder$year), as.character)
names(yearMarks) <- unique(gapminder$year)
yearSlider <- dccRangeSlider(
  id="year",
  marks = yearMarks,
  min = 1952,
  max = 2007,
  step=5,
  value = list(1952, 2007)
)

continentDropdown <- dccDropdown(
  id = "continent",
  options = lapply(
    levels(gapminder$continent), function(x){
      list(label=x, value=x)
    }),
  value = levels(gapminder$continent),
  multi = TRUE
)

yaxisDropdown <- dccDropdown(
  id = "y-axis",
  options = list(
    list(label = "GDP Per Capita", value = "gdpPercap"),
    list(label = "Life Expectancy", value = "lifeExp"),
    list(label = "Population", value = "pop")
  ),
  value = "gdpPercap"
)

# Graph
all_continents <- unique(gapminder$continent)
make_graph <- function(years=c(1952, 2007), 
                       continents=all_continents,
                       yaxis="gdpPercap"){
  
  data <- gapminder %>%
    filter(year >= years[1] & year <= years[2]) %>%
    filter(continent %in% continents)
 
  p <- ggplot(data, aes(x=year, y=gdpPercap, colour=continent)) +
    geom_point(alpha=0.6) +
    scale_color_manual(name="Continent", values=continent_colors) +
    scale_x_continuous(breaks = unique(data$year))+
    xlab("Year") +
    ylab("GDP Per Capita") +
    ggtitle(paste0("Change in ", yaxis, " Over Time")) +
    theme_bw()
  
  ggplotly(p)
}

make_table <- function(years=c(1952, 2007), 
                       continents=all_continents){
  
  gapminder %>%
    filter(year >= years[1] & year <= years[2]) %>%
    filter(continent %in% continents) %>%
    df_to_list()
  
}

# Table that can be sorted by column
table <- dashDataTable(
  id = "gap-table",
  # these make the table scrollable
  fixed_rows= list(headers = TRUE, data = 0),
  style_table= list(
    maxHeight = '200',
    overflowY = 'scroll'
  ),
  columns = lapply(colnames(gapminder), 
                   function(colName){
                     list(
                       id = colName,
                       name = colName
                     )
                   }),
  data = make_table(),
  sort_action="native"
)

app$layout(
  htmlDiv(
    list(
      htmlH1('Gapminder Dash Demo'),
      htmlH2('Looking at country data interactively'),
      #selection components
      htmlLabel('Select a year range:'),
      yearSlider,
      htmlIframe(height=15, width=10, style=list(borderWidth = 0)), #space
      htmlLabel('Select continents:'),
      continentDropdown,
      htmlLabel('Select y-axis metric:'),
      yaxisDropdown,
      #graph and table
      dccGraph(
        id = 'gap-graph',
        figure=make_graph()
      ),
      htmlIframe(height=20, width=10, style=list(borderWidth = 0)), #space
      htmlLabel('Try sorting by table columns!'),
      table,
      htmlIframe(height=20, width=10, style=list(borderWidth = 0)), #space
      dccMarkdown("[Data Source](https://cran.r-project.org/web/packages/gapminder/README.html)")
    )
  )
)

#Adding callbacks for interactivity
app$callback(
  output=list(id='gap-graph', property='figure'),
  params=list(input(id='year', property='value'),
              input(id='continent', property='value'),
              input(id='y-axis', property='value')),
  function(year_value, continent_value, yaxis_value) {
    make_graph(year_value, continent_value, yaxis_value)
  })

app$callback(
  output=list(id='gap-table', property='data'),
  params=list(input(id='year', property='value'),
              input(id='continent', property='value')),
  function(year_value, continent_value) {
    make_table(year_value, continent_value)
  })

app$run_server()