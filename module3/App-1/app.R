library(tidyverse)
library(shiny)
library(usmap)
library(magrittr)

load('data.rdata')

ui <- fluidPage(
  tags$head(tags$title('US Death Rate Explorer by Brian Weinfeld')),
  div(class='jumbotron', style='padding-top: 10px; padding-bottom: 10px',
      h1(align='center', 'US Death Rate Explorer'),
      h3(align='right', 'By Brian Weinfeld')
      ),
  div(
    div(class='well col-xs-2',
        selectInput('Cause', label='Cause', choices = causes),
        selectInput('Region', label='Region', choice = regions),
        conditionalPanel(condition = 'input.Region == "South"',
                          selectInput('South', label='Division', choice = division.south)
                         ),
        conditionalPanel(condition = 'input.Region == "West"',
                         selectInput('West', label='Division', choice = division.west)
                         ),
        conditionalPanel(condition = 'input.Region == "Northeast"',
                         selectInput('Northeast', label='Division', choice = division.northeast)
                         ),
        conditionalPanel(condition = 'input.Region == "Midwest"',
                         selectInput('Midwest', label='Division', choice = division.midwest)
                         ),
        actionButton('action', 'Filter', class='btn btn-primary btn-block')
    ),
    div(class='col-xs-10', plotOutput('plot'))
  ),
  div(class='col-xs-12', style='margin-top: 10px', dataTableOutput('table'))
)

server <- function(input, output){
  
  data <- eventReactive(input$action,{
    to.ret <- data.2010 %>%
      filter(cause == input$Cause)
    if(input$Region != 'All'){
      if(input$Region == 'South'){
        if(input$South == 'All'){
          to.ret %<>% filter(region == input$Region)
        }else{
          to.ret %<>% filter(division == input$South)
        }
      }else if(input$Region == 'Northeast'){
        if(input$Northeast == 'All'){
          to.ret %<>% filter(region == input$Region)
        }else{
          to.ret %<>% filter(division == input$Northeast)
        }
      }else if(input$Region == 'Midwest'){
        if(input$Midwest == 'All'){
          to.ret %<>% filter(region == input$Region)
        }else{
          to.ret %<>% filter(division == input$Midwest)
        }
      }else if(input$Region == 'West'){
        if(input$West == 'All'){
          to.ret %<>% filter(region == input$Region)
        }else{
          to.ret %<>% filter(division == input$West) 
        }
      }
    }
    to.ret
  })
  
  output$plot <- renderPlot({
    to.plot <- data()
    
    to.plot %>%
      plot_usmap(data=., values='rate') +
      scale_fill_continuous(low='white', high='red', name='Deaths (per 100k)') +
      theme(legend.position=c(.5, .05), legend.direction='horizontal') +
      labs(title=paste0('2010 Deaths (per 100k) from "', to.plot$cause[1], '"'))
  }, height=500)
  
  output$table <- renderDataTable({
    data() %>%
      select(-cause)
  })
}

shinyApp(ui, server)


