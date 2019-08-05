#import libraries
library(ggplot2)
library(directlabels)
library(grid)
library(dplyr)
library(ggthemes)

#read in data that was scraped cleaned and manipulated in python
pdat <- read.csv('c:/Users/Noah/Documents/facebook_analysis/goonsquadfinal.csv',
                 stringsAsFactors = FALSE)

#format date strings as date objects
pdat$date <- as.Date(pdat$date)

pdat <- pdat[2:4] # remove index column

names(pdat) <- c("date","username","cumposts") # change column names

#create boolean to filter out users with low post totals
pdat <- pdat %>% group_by(username) %>% mutate(filterout = ifelse(max(cumposts) >= 100, 
                                                                  TRUE,FALSE))

#plot
p <- ggplot(subset(pdat, filterout == TRUE),
            aes(x=date,y=cumposts , group = username, col= username)) + 
  geom_line(lwd=1) +
  geom_dl(aes(label = username), method = list(dl.trans(x = x + 0.2), 
                                               "last.points", 
                                               cex = 0.8, 
                                               'last.bumpup', hjust = -.05)) +
  guides(group = FALSE, col=FALSE) +
  labs(x = "Date", y = "Cumulative Posts", 
       title = "Cumulative Posts in Meme Lovers -- Data from 3/05/18 - 12/25/18 -- Min 100 Posts") +
  theme(plot.margin = unit(c(1,6,1,1), "lines"), 
        panel.background = element_blank(), 
        panel.grid.major = element_line(size = 0.5, linetype = 'dashed', colour = "gray90"))
  
  

gt <- ggplotGrob(p)
gt$layout$clip[gt$layout$name == "panel"] <- "off"
grid.draw(gt)

