# Loads the rvest, stringr, dplyr and purrr libraries
suppressWarnings({
  suppressPackageStartupMessages({
    library(rvest)
    library(stringr)
    library(dplyr)
    library(purrr)
  })
})

# Language: us-english
Sys.setlocale("LC_ALL", "en_US.UTF-8")

setwd('C:/Users/joaov/Documents/Whisky Recomendation System/Whisky Notes Extraction/Step 1')

# Loads the Step 1 RDS file
links_df <- read.csv2("Whisky Notes - Step 1.csv")

# Creates an empty data frame to store the reviews data
reviews_df <- data.frame()

# Goes through all reviews pages
for (i in 1:nrow(links_df)){
  
  # Selects the review date
  review_date <- links_df[i, 'review_date']
  
  # Selects the review URL link
  review_link <- links_df[i, 'review_link']
  
  # Tries to load the review page 3 times
  review_page <- NULL
  attempts <- 0
  while (is.null(review_page) && attempts < 3) {
    attempts <- attempts + 1
    
    review_page <- tryCatch(
      read_html(review_link),
      error = function(e) NULL
    )
    
    if (is.null(review_page)) {
      Sys.sleep(5)
    }
  }
  
  # Extracts the review page titles and texts
  contents <- review_page %>%
    html_nodes('div.entry-content') %>%
    html_nodes('p, h2')
  
  # Titles not associated with reviews don't have "%" (ABV) on it, so we need to remove it from the contents list
  contents <- contents[
    !(html_name(contents) == "h2" & !str_detect(html_text(contents), "%"))
  ]
  
  # Extracts the review page entry image
  entry_image <- review_page %>%
    html_nodes('div.entry-image') %>%
    html_nodes('img') %>%
    html_attr('src') %>%
    .[grep('https', .)] %>%
    .[grep('upload', .)] %>%
    trimws()
  entry_image <- ifelse(length(entry_image) == 0, NA, entry_image)
  
  # Extracts the review page entry score
  review_score <- review_page %>%
    html_nodes('div.entry-score') %>%
    html_text() %>%
    trimws()
  
  # Gets the titles (h2) positions in the contents list
  title_indexes <- which(html_name(contents) == 'h2')
  
  # If there is no title in the review page (page with no review) it goes to the next one
  if (length(title_indexes) == 0){
    next
  }
  
  # Calculates the first text positions in the contents list
  first_text_indexes <- title_indexes + 1
  
  # If there is more than one title, there is multiple reviews in the same review page and a different last text position logic is necessary
  if (length(title_indexes) > 1){
    last_text_indexes <- append(title_indexes[2:length(title_indexes)] - 1, length(contents)) 
  } else {
    last_text_indexes <- length(contents)
  }
  
  # Goes through all titles positions
  for (j in 1:length(title_indexes)){
    
    # Extracts the review title
    review_title <- contents[title_indexes[j]] %>%
      html_text() %>%
      trimws()
    review_title <- ifelse(length(review_title) == 0, NA, review_title)
    
    # Extracts the image associated to the review title and text
    image <- contents[title_indexes[j]:last_text_indexes[j]] %>%
      html_nodes('img') %>%
      html_attr('src') %>%
      .[grep('https', .)] %>%
      .[grep('upload', .)] %>%
      trimws()
    image <- ifelse(length(image) == 0, NA, image)
    
    # If there is no entry image and there is image on text, review image = text image
    if ((is.na(entry_image)) & (!is.na(image))){
      review_image <- image
      
    } else if ((!is.na(entry_image)) & (is.na(image))){ # If there is entry image and there is no image on text, review image = entry image
      review_image <- entry_image
      entry_image <- NA
      
    } else if ((is.na(entry_image)) & (is.na(image))){ # If there is no entry image and there is no image on text, it looks if there is image outside it's review text but inside the contents list
      images <- contents %>%
        html_nodes('img') %>%
        html_attr('src') %>%
        .[grep('https', .)] %>%
        .[grep('upload', .)] %>%
        trimws()
      review_image <- images[j]
    }
    
    # If there is no entry image and there is no image on text, it looks if there is image before the review title (outside contents list)
    if (is.na(review_image)){
      pre_review_image <- review_page %>%
        html_nodes('div.entry-content') %>%
        html_nodes('h2') %>%
        html_nodes('img') %>%
        html_attr('src') %>%
        .[grep('https', .)] %>%
        .[grep('upload', .)] %>%
        trimws()
      review_image <- pre_review_image
    }
    
    review_image <- ifelse(length(review_image) == 0, NA, review_image)
    
    # Starts with the review full text as an empty string
    review_full_text <- ''
    
    # Goes through all paragraphs of the review text
    for (text_position in first_text_indexes[j]:last_text_indexes[j]){
      
      # Extracts each paragraph text
      text <- contents %>%
        .[text_position] %>%
        html_text() %>%
        trimws()
      
      # Adds each paragraph text to the review full text
      review_full_text <- paste0(review_full_text, ' ', text)
      
      # If there is "/10" or "Score:" in the text = score text
      if ((grepl("/10", text)) | (grepl("Score:", text))) {
        score_text = text
        # Stops in the score text, ignoring the text after the reviews that appears in some cases
        break
        
      } else {
        
        # If there is no score text, score = NA
        score_text = NA
      }
      
    }
    
    # Tests if there is score text in the review
    if (!is.na(score_text)){
      
      # Tests if there is "/" in the score text
      if (str_detect(score_text, '/')){
        
        # Extracts the review score based on "/"
        review_score <- score_text %>%
          sub(".*?(\\d+)/.*", "\\1", .) %>%
          trimws()
        
      } else if (str_detect(score_text, 'Score:')){ # Tests if there is "Score:" in the score text
        
        # Extracts the review score based on "Score:"
        review_score <- review_full_text %>%
          str_split('Score: ') %>%
          unlist() %>%
          .[2] %>%
          str_split(., '/') %>%
          unlist() %>%
          .[1]
        
      }
      
    }
    
    review_score <- ifelse(length(review_score) == 0, NA, review_score)
    
    # Removes the score information from the review full text
    review_full_text <- review_full_text %>%
      str_split('Score') %>%
      unlist() %>%
      .[1] %>%
      str_replace(., '\n', ' ') %>%
      trimws()
    
    # Creates the review data frame
    review_df <- data.frame(review_date = review_date,
                            review_title = review_title,
                            review_link = review_link,
                            review_full_text = review_full_text,
                            review_image = review_image,
                            review_score = review_score)
    
    # Stores each review information in the reviews data frame
    reviews_df <- bind_rows(reviews_df, review_df)
    
    # Resets the review score value
    review_score <- NA
    
  }
  
  # Waits 0.2 seconds to go to the next review page
  Sys.sleep(0.2)
  
}

setwd('C:/Users/joaov/Documents/Whisky Recomendation System/Whisky Notes Extraction/Step 2')

# Exports the Step 2 RDS file
write.csv2(reviews_df, file = 'Whisky Notes - Step 2.csv', row.names = FALSE)