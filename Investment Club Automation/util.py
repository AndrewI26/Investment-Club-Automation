from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import datetime
from math import floor

DEFINITIONS = [
        ("Stock Symbol", "An abbreviation used to uniquely identify the shares of a company. Generally a few letters, numbers or both and can also be known as Ticker Symbol."),
        ("Stock Quotes", "A list of prices (generally bid, ask and last) for a stock at a particular point during the trading day."),
        ("Bonds", "Essentially I.O.Us used to lend money to whatever entity you are purchasing the bond from including the federal government, state and local municipalities, corporations, and foreign government bonds."),
        ("Mutual Funds", "Essentially I.O.Us used to lend money to whatever entity you are purchasing the bond from including the federal government, state and local municipalities, corporations, and foreign government bonds."),
        ("Hedge Funds", "The typical hedge fund is designed to be a partnership arrangement with the fund manager acting as the general partner responsible for making investment decisions."),
        ("Diversification", "Simply means spreading your investments over different market vehicles. It is a widely used strategy for investors who want to minimize risk to a certain degree."),
        ("Blue Chip Stocks", "Simply means spreading your investments over different market vehicles. It is a widely used strategy for investors who want to minimize risk to a certain degree."),
        ("Dividend", "Money given out as either money or extra shares by a company to it's shareholders out of it's profits or extra cash."),
        ("Initial Public Offering", "The initial sale of stock by a private company to the public which turns it into a public company."),
        ("Bull Market", "The tendency of the stock market to trend higher over time. It can be used to describe either the market as a whole or specific sectors and securities."),
        ("Bear Market", "A long period where the stock market value falls along with a sense of pessimism for the public."),
        ("Stock Volatility", "Refers to how volatile a stock is: how much a stock can quickly rise or fall."),
        ("Day Trading", "Buying and Selling (or Shorting and Covering) the same security on the same day."),
        ("Short Selling", "Practice of selling securities or other financial instruments, with the intention of subsequently repurchasing them (“covering”) at a lower price."),
        ("Bid Price", "When you are selling your shares of a security, the bid price is what the buyer is willing to pay for your shares."),
        ("Spread", "The difference between the ask price and the sell price and it is kept by the broker."),
        ("Market Order", "An order to buy or sell a stock at the best available price. Generally, this type of order will be executed immediately."),
        ("Stop Order", "An order to buy or sell a stock when the stock price reaches a specified price, which is known as a stop price. When the specified price is reached, the stop order becomes a market order."),
        ("Limit Order", "An order to buy or sell a stock at a specific price or better. A buy limit order can only be executed at the limit price or lower, and a sell limit order can only be executed at the limit price or higher."),
        ("Traling Stop", "A Stop Loss order which is placed as a percentage value as opposed to an absolute dollar value. The order will only execute if the price of the security falls by a certain percentage."),
    ]

# Web Scraper functions
def fill_field(driver: object, text: str, field_name="", xpath=""):
    field = driver.find_element(By.NAME, field_name) if field_name else driver.find_element(By.XPATH, xpath)
    field.clear()
    field.send_keys(text)

def click_element(driver: object, field_name="", xpath=""):
    field = driver.find_element(By.NAME, field_name) if field_name else driver.find_element(By.XPATH, xpath)
    driver.implicitly_wait(3)
    field.click()

def createDriver():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    driver = webdriver.Chrome(options=options)
    return driver

# Slides functions
def deleteText(row, col):
    TABLE_ID = "g237f1470abf_0_3"
    return \
    ({
        'deleteText': {
            'objectId': TABLE_ID,
        'cellLocation': {
            'rowIndex': row,
            'columnIndex': col
            },
        'textRange': {
            'type': 'ALL'
            }
        }
    })

def insertText(row, col, text):
    TABLE_ID = "g237f1470abf_0_3"
    return \
    ({
        'insertText': {
            'objectId': TABLE_ID,
            'cellLocation': {
                'rowIndex': row,
                'columnIndex': col
            },
            'text': text,
            'insertionIndex': 0
            }
    })

def findWordOfWeek():
    STARTDATE = datetime.date(2023, 7, 12)
    
    current_week = floor((datetime.date.today() - STARTDATE).days / 7)
    return DEFINITIONS[current_week]

def createRequests(leaders: list):
    TITLE_ID = "g1e55069bcd0_0_0"
    DEFINITION_ID = "g237f1470abf_0_72"
    title, definition = findWordOfWeek()
    requests = []
    # Clear table
    for row in range(3):
        requests.append(deleteText(row, 1))
        requests.append(deleteText(row, 2))
    # Clear WOW
    requests.append({
        'deleteText': {
            'objectId': TITLE_ID,
        'textRange': {
            'type': 'ALL'
            }
        }
    })
    requests.append({
        'deleteText': {
            'objectId': DEFINITION_ID,
        'textRange': {
            'type': 'ALL'
            }
        }
    })
    # Write names
    for row, (leader, gain) in enumerate(leaders):
        requests.append(insertText(row, 1, leader))
        requests.append(insertText(row, 2, gain))
    
    requests.append({
        'insertText': {
            'objectId': TITLE_ID,
            'text': title,
            'insertionIndex': 0
            }
    })
    requests.append({
        'insertText': {
            'objectId': DEFINITION_ID,
            'text': definition,
            'insertionIndex': 0
            }
    })
    return requests

# Functions for docs
def createDocsRequests(leaders):
    requests = []
    length_leaders = [len(leader) + len(gain) + 4 for leader, gain in leaders]
    sum = 1
    index_array = []
    for length in length_leaders:
        index_array.append(sum)
        sum += length

    for index, (leader, gain) in enumerate(leaders):
        number_gain = float(gain[:-1])
        requests.append({
            'insertText': {
                'text': f'{leader} ↑ {gain}',
                'location': {
                    'index': index_array[index]
                }
            }
            } if number_gain > 0 else {
            'insertText': {
                'text': f'{leader} ↓ {gain}',
                'location': {
                    'index': index_array[index]
                }
            }
                })
        requests.append({
            'insertText': {
                'text': '\n',
                'location': {
                    'index': index_array[index]
                }
            }
                })
    
    return requests

def createDefinitionsRequests():
    word, definition = findWordOfWeek()
    requests = []
    requests.append({
        'insertText': {
            'text': f'{word} - {definition}',
            'location': {
                'index': 1
            }
        }
    })
    return requests