from selenium import webdriver

search_string = 'fbref Joao Felix'
search_string = search_string.replace(' ', '+')  

browser = webdriver.Chrome('/Users/eduardooportoalonso/Documents/Cursos/Ironhack/datamad1020/ironhack-projects/pipelines-project/chromedriver') 
  
for i in range(1): 
    matched_elements = browser.get("https://www.google.com/search?q=" +
                                     search_string + "&start=" + str(i)) 

print(matched_elements)
