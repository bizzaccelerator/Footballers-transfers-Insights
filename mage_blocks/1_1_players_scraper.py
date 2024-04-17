if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import time 
import pandas as pd
from datetime import datetime, timedelta
import os, os.path
from pathlib import Path

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """

    ChromeOptions = Options()
    # ChromeOptions.headless = False # Because we want to display our window
    ChromeOptions.add_argument('--no-sandbox')
    ChromeOptions.add_argument('--headless=new')
    ChromeOptions.add_argument('--disable-dev-shm-usage')

    s = Service(ChromeDriverManager().install()) 

    #create a UserAgent instance
    user_agent = UserAgent()
    #add a random user agent to our options
    ChromeOptions.add_argument(f'user-agent={user_agent.random}')

    # Create a our web driver
    driver = webdriver.Chrome(service=s, options=ChromeOptions)
    # user_agent = driver.execute_script("return navigator.userAgent")
    driver.maximize_window() # Maximize the screen
    driver.implicitly_wait(30)

    # Obtain the information of the site
    website = 'https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/'
    driver.get(website)
    time.sleep(2)
    WebDriverWait(driver,20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe#sp_message_iframe_953358")))

    # Closing the cookies' windows
    # driver.switch_to.frame('sp_message_iframe_953358')
    consent_button = driver.find_element(By.XPATH,value="//*[@aria-label='Accept & continue']")
    time.sleep(5)
    consent_button.click()

    # Moving to detailed tab
    info_tabs = driver.find_elements(By.CSS_SELECTOR, value='div.tm-tabs a.tm-tab')
    detailed_tab = (info_tabs[1]).get_property('href')
    time.sleep(2)
    driver.get(detailed_tab)

    # To get the information
    pagelinks = []
    pages = driver.find_elements(By.CSS_SELECTOR,value="ul.tm-pagination li a")
    pages = pages[0:10]
    for page in pages:
        pagelinks.append(page.get_attribute('href'))
        # print(page.get_attribute('href'))

    # Preparing the list to construct the dataframe
    time.sleep(3)
    tm_id = []
    player_name = []
    player_position = []
    player_details = []
    player_age = []
    player_nationality = []
    team_left = []
    league_left = []
    country_previous = []
    team_joined = []
    league_joined = []
    country_current = []
    transf_date = []
    market_value = []

    # To get the elements for current day only
    today = datetime.now().date()
    yesterday = today - timedelta(days = 1)

    # For iterate in the ten screens
    for link in pagelinks:
        driver.get(link)
        time.sleep(2)
        # To get the elements from each row 
        info_players = driver.find_elements(By.XPATH,value="//table[@class='items']/tbody/tr")
        time.sleep(3)
        print(pagelinks.index(link))

        for info_player in info_players:
            # Compared to transference reported date
            date_row = info_player.find_element(By.XPATH,value='./td[6]').text
            reported_date = date_row.replace(',','')
            date_comparable = datetime.strptime(reported_date, '%b %d %Y').date()
            
            if date_comparable > yesterday:
                print('You have nothing to do here')  
            elif date_comparable == yesterday:
                player_name.append(info_player.find_element(By.XPATH,value='./td[1]/table/tbody/tr[1]/td[2]/a').text)
                player_position.append(info_player.find_element(By.XPATH,value='./td[1]/table/tbody/tr[2]/td').text)
                player_details.append(info_player.find_element(By.XPATH,value='./td[1]/table/tbody/tr[1]/td[2]/a').get_property('href'))
                tm_id.append(info_player.find_element(By.XPATH,value='./td[1]/table/tbody/tr[1]/td[2]/a').get_property('href').split('/')[-1])
                player_age.append(info_player.find_element(By.XPATH,value='./td[2]').text)
                player_nationality.append(info_player.find_element(By.XPATH,value='./td[3]/img').get_property('title'))
                
                # Evaluating the previous team existence
                exit_pass = info_player.find_element(By.XPATH,value='./td[4]/table/tbody/tr[2]/td').text
                active = info_player.find_elements(By.XPATH,value='./td[4]/table/tbody/tr[1]/td[1]/a')
                if exit_pass == '':
                    league_left.append('No league')
                    country_previous.append('No country')
                    if active:
                        old_team = info_player.find_element(By.XPATH,value='./td[4]/table/tbody/tr[1]/td[1]/a').get_property('title')
                        team_left.append(old_team)
                    else:
                        old_team = info_player.find_element(By.XPATH,value='./td[4]/table/tbody/tr[1]/td[1]/img').get_property('title')
                        team_left.append(old_team)
                else:
                    if info_player.find_elements(By.XPATH,value='./td[4]/table/tbody/tr[2]/td/a'):
                        league_left.append(info_player.find_element(By.XPATH,value='./td[4]/table/tbody/tr[2]/td/a').text)
                        country_previous.append(info_player.find_element(By.XPATH,value='./td[4]/table/tbody/tr[2]/td/img').get_attribute('title'))
                        old_team = info_player.find_element(By.XPATH,value='./td[4]/table/tbody/tr[1]/td[1]/a').get_property('title')
                        team_left.append(old_team)
                    else:         
                        league_left.append('No league')
                        country_previous.append(info_player.find_element(By.XPATH,value='./td[4]/table/tbody/tr[2]/td/img').get_attribute('title'))
                        old_team = info_player.find_element(By.XPATH,value='./td[4]/table/tbody/tr[1]/td[1]/a').get_property('title')
                        team_left.append(old_team)

                # Evaluating the new team existence
                arrival_pass = info_player.find_element(By.XPATH,value='./td[5]/table/tbody/tr[2]/td').text
                non_inactive = info_player.find_elements(By.XPATH,value='./td[5]/table/tbody/tr[1]/td[1]/a')
                if arrival_pass == '':
                    league_joined.append('No league')
                    country_current.append('No country')
                    if non_inactive:
                        new_team = info_player.find_element(By.XPATH,value='./td[5]/table/tbody/tr[1]/td[1]/a').get_property('title')
                        team_joined.append(new_team)
                    else:
                        new_team = info_player.find_element(By.XPATH,value='./td[5]/table/tbody/tr[1]/td[1]/img').get_property('title')
                        team_joined.append(new_team)
                else:
                    if info_player.find_elements(By.XPATH,value='./td[5]/table/tbody/tr[2]/td/a'):
                        league_joined.append(info_player.find_element(By.XPATH,value='./td[5]/table/tbody/tr[2]/td/a').text)
                        country_current.append(info_player.find_element(By.XPATH,value='./td[5]/table/tbody/tr[2]/td/img').get_attribute('title'))
                        new_team = info_player.find_element(By.XPATH,value='./td[5]/table/tbody/tr[1]/td/a').get_property('title')
                        team_joined.append(new_team)
                    else: 
                        league_joined.append('No league')
                        country_current.append(info_player.find_element(By.XPATH,value='./td[5]/table/tbody/tr[2]/td/img').get_attribute('title'))
                        new_team = info_player.find_element(By.XPATH,value='./td[5]/table/tbody/tr[1]/td/a').get_property('title')
                        team_joined.append(new_team)

                transf_date.append(info_player.find_element(By.XPATH,value='./td[6]').text)
                market_value.append(info_player.find_element(By.XPATH,value='./td[7]').text)
                print(info_player.find_element(By.XPATH,value='./td[1]/table/tbody/tr[1]/td[2]/a').text)
            else:
                print('You have successfully extracted all the transferences reported for today')
                break
            
    print('The number of players today were: ',len(tm_id))

    # Timer to set the time for the bot wait with the screen open
    time.sleep(2)

    # Turning off the bot
    driver.quit()

    # Preparing the data to be exported    
    players_data = dict({'tm_id': tm_id,
                        'player_name': player_name,
                        'player_position': player_position,
                        'player_details': player_details,
                        'player_age': player_age,
                        'player_nationality': player_nationality,
                        'team_left': team_left,
                        'league_left': league_left,
                        'country_previous': country_previous,
                        'team_joined': team_joined,
                        'league_joined': league_joined,
                        'country_current': country_current,
                        'transf_date': transf_date,
                        'market_value': market_value,
                        })

    # To get the data in a new file, we prepare the file name
    day_name = today.strftime("%A")
    number_day = today.strftime("%d")
    month_name = today.strftime("%b")
    month_number = today.strftime("%m")
    year = today.strftime("%Y")
    dataset_file = f'{year}_{month_name}_{number_day}_{day_name}'

    # Save the new dataset in the directory selected
    players = pd.DataFrame(players_data)

    return players