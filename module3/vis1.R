library(tidyverse)
library(usmap)

raw.data <- read_csv('C:\\Users\\Brian\\Desktop\\GradClasses\\Fall18\\608\\module3\\data\\cleaned-cdc-mortality-1999-2010-2.csv')

data.2010 <- raw.data %>%
  filter(Year == 2010) %>%
  select(-Year, -Deaths, -Population) %>%
  rename('cause'='ICD.Chapter', 'state'='State', 'rate'='Crude.Rate')

regions <- read_csv('C:\\Users\\Brian\\Desktop\\GradClasses\\Fall18\\608\\module3\\data\\regions.csv')

data.2010 <- data.2010 %>%
  inner_join(regions, by='state')

cause.par <- 'Certain infectious and parasitic diseases'
region.par <- 'West'
division.par <- 'Pacific'

data.2010 %>%
  filter(cause == cause.par,
         region == region.par,
         division == division.par) %>%
  plot_usmap(data=., values='rate') +
  scale_fill_continuous(low='white', high='red', name='Deaths (per 100k)') +
  theme(legend.position=c(.5, -.1), legend.direction='horizontal') +
  labs(title=paste0('2010 Deaths (per 100k) from "', disease, '"'))
  

# 2nd ---------------------------------------------------------------------

library(ggrepel)

all.data <- raw.data %>%
  rename('cause'='ICD.Chapter', 'state'='State', 'year'='Year', 'deaths'='Deaths', 'population'='Population', 'rate'='Crude.Rate') %>%
  inner_join(regions, by='state')

national.rates <- all.data %>% 
  group_by(year, cause) %>%
  summarise(rate = sum(deaths) / sum(population) * 100000) %>%
  mutate(state='NA', #National
         region='NA',
         division='NA')

all.data <- all.data %>%
  select(-deaths, -population) %>%
  bind_rows(national.rates)
  
state.par <- c('CA', 'WV')
cause.par <- 'Certain infectious and parasitic diseases'

to.plot <- all.data %>%
  filter(state %in% c(state.par, 'NA') ,
         cause == cause.par)

to.label <- to.plot %>%
  filter(year == 2010) %>%
  mutate(year = year + 1)
  
  
ggplot(to.plot, aes(year, rate, group=state, color=state), show.legend=FALSE) +
  geom_point() +
  geom_line() +
  geom_label_repel(data=to.label, aes(year, rate, color=state, label=state), show.legend=FALSE) +
  theme_bw() +
  labs(title=paste0('Deaths From "', cause, '"'),
       x='Year',
       y='Death Rate (per 100k)',
       color='State'
  ) 
  
  
  
  
  
