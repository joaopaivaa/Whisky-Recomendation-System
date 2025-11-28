# Loads the rvest, stringr and dplyr libraries
suppressWarnings({
  suppressPackageStartupMessages({
    library(rvest)
    library(stringr)
    library(dplyr)
  })
})

# Language: us-english
Sys.setlocale("LC_ALL", "en_US.UTF-8")

setwd('C:/Users/joaov/Documents/Whisky Recomendation System/Whisky Notes Extraction/Step 1')

# Loads the Step 1 page
step1_page <- read_html("https://www.whiskynotes.be/")

# Extracts the number of pages
number_of_pages <- step1_page %>%
  html_nodes('a.page-numbers') %>% 
  html_text() %>%
  as.integer() %>% sort(., TRUE) %>% .[1]

# Creates an empty data frame to store the reviews URL links and dates
links_df <- data.frame()

# Goes through all pages
for (page in 1:number_of_pages){
  
  # Loads each Whisky Notes page
  load_page <- NULL
  attempts <- 0
  while (is.null(load_page) && attempts < 3) {
    attempts <- attempts + 1
    
    load_page <- tryCatch(
      read_html(paste0("https://www.whiskynotes.be/page/", page, "/")),
      error = function(e) NULL
    )
    
    if (is.null(load_page)) {
      Sys.sleep(5)
    }
  }
  
  # Get the reviews sections
  sections <- load_page %>%
    html_nodes('article')
  
  # Goes through each review section
  for (section in sections){
    
    # Extracts the review category
    category <- section %>%
      html_nodes('span.cat-links') %>%
      html_text() %>%
      str_replace('\\*', '') %>%
      trimws()
    
    # Don't store the review information if its category is "Whisky News" (because it isn't a review)
    if (length(category) > 0){
      if (category == 'Whisky News'){
        next
      }
    }
    
    # Extracts the review date
    review_date <- section %>%
      html_nodes('div.entry-meta') %>%
      html_nodes('time.entry-date.published') %>%
      html_text() %>%
      trimws() %>%
      as.Date(., format = "%d %B %Y")
    
    # The whisky of the day needs a different logic to extract its review date
    if (length(review_date) == 0){
      review_date <- section %>%
        html_nodes('div.whiskyoftheday') %>%
        html_text() %>%
        trimws() %>%
        as.Date(., format = "%d %B %Y")
    }
    
    # Extracts the review URL link
    review_link <- section %>%
      html_nodes('header.entry-header') %>%
      html_nodes('a') %>%
      html_attr('href') %>%
      trimws()
    
    # Creates the review data frame
    review_df <- data.frame(review_date = review_date,
                            review_link = review_link)
    
    # Stores each review information in the links data frame
    links_df <- bind_rows(links_df, review_df)
    
  }
  
  # Waits 0.8 seconds to go to the next page (less than 0.8 seconds was breaking my code here)
  Sys.sleep(0.2)
  
}

# Ignores the first review as it comes duplicated in the sections list
links_df <- links_df[2:nrow(links_df), ]

# Resets the data frame index
rownames(links_df) <- NULL

# Exports the Step 1 RDS file
write.csv2(links_df, file = 'Whisky Notes - Step 1.csv', row.names = FALSE)