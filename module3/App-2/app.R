library(tidyverse)
library(shiny)
library(ggrepel)
library(magrittr)

load('data.rdata')

ui <- fluidPage(
  tags$head(tags$title('US Death Rate By State Explorer by Brian Weinfeld'),
            tags$style("label.checkbox-inline { margin-left: 10px}"),
            tags$style("span { font-family: 'Courier New'}")
            ),
  div(class='jumbotron', style='padding-top: 10px; padding-bottom: 10px',
      h1(align='center', 'US Death Rate By State Explorer'),
      h3(align='right', 'By Brian Weinfeld')
  ),
  div(
    div(class='well col-xs-2',
        selectInput('Cause', label='Cause', choices = causes),
        checkboxGroupInput('State', label='States', inline=TRUE, choices = states$state),
        actionButton('action', 'Filter', class='btn btn-primary btn-block')
    ),
    div(class='col-xs-10', plotOutput('plot'))
  ),
  div(class='col-xs-12', style='margin-top: 10px', dataTableOutput('table'))
)

server <- function(input, output){
  
  data <- eventReactive(input$action,{
    to.plot <- all.data %>%
      filter(state %in% c(input$State, 'NA') ,
             cause == input$Cause)
    
    
    to.plot
  })
  
  output$plot <- renderPlot({
    to.plot <- data()
    
    to.plot %>%
      ggplot(aes(year, rate, group=state, color=state), show.legend=FALSE) +
      geom_point(show.legend=FALSE) +
      geom_line(show.legend=FALSE) +
      geom_label_repel(data=to.plot %>% filter(year==2010), aes(year, rate, color=state, label=state), show.legend=FALSE) +
      geom_label_repel(data=to.plot %>% filter(year==1999), aes(year, rate, color=state, label=state), show.legend=FALSE) +
      theme_bw() +
      labs(title=paste0('Deaths From "', to.plot$cause[1], '"'),
           x='Year',
           y='Death Rate (per 100k)',
           color='State'
      ) 
  })
  
  output$table <- renderDataTable({
    data() %>%
      select(state, year, rate) %>%
      spread(key=state, value=rate)
  })
}

shinyApp(ui, server)


