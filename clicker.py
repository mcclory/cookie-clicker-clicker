# Generated by Selenium IDE
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from multiprocessing import Process, Pool
import threading 
from collections import Counter
from pynput.keyboard import Key, Listener
from concurrent.futures import ThreadPoolExecutor
import time
import keyboard

RUN_LOOP = True 

RUN_UPGRADES = True 

RUN_PRODUCTS = True 

def on_press(key):
    if str(key).lower() == 'r': 
      RUN_LOOP = not RUN_LOOP
      print(f"RUN_LOOP set to {RUN_LOOP}")
    if str(key).lower() == 'u':
      RUN_UPGRADES = not RUN_UPGRADES
      print(f"RUN_UPGRADES set to {RUN_UPGRADES}")
    if str(key).lower() == 'p':
      RUN_PRODUCTS = not RUN_PRODUCTS
      print(f"RUN_PRODUCTS set to {RUN_PRODUCTS}")

def get_names(): 
  names = []
  if RUN_UPGRADES: 
    names.append('upgrade')
  if RUN_PRODUCTS:
    names.append('product')
  return names

class CookieClickerClicker():

  def __init__(self, *args, **kwargs):
    self.driver = kwargs.get('driver', webdriver.Firefox())
    self.vars = {}
    self.run_clicker = bool(kwargs.get('run_clicker', True))
    self.clicker_loop_count = int(kwargs.get('clicker_loop_count', 10))
    self.buy_products = bool(kwargs.get('buy_products', True))
    self.buy_upgrades = bool(kwargs.get('buy_upgrades', True))
    self.click_shimmer = bool(kwargs.get('click_shimmer', True))
    self.driver.get("https://orteil.dashnet.org/cookieclicker/")
    lang_select = WebDriverWait(self.driver, 30).until(expected_conditions.element_to_be_clickable((By.ID, "langSelect-EN")))
    lang_select.click()
    self.big_cookie = WebDriverWait(self.driver, 20).until(expected_conditions.element_to_be_clickable((By.ID, "bigCookie")))

  def toggle_run_clicker(self):
    self.run_clicker = not self.run_clicker 

  def toggle_buy_products(self): 
    self.buy_products = not self.buy_products

  def toggle_buy_upgrades(self):
    self.buy_upgrades = not self.buy_upgrades

  def click_buyables(self, base_name): 
    for x in sorted(range(20), reverse=True):
      self.click_buy_item(f"{base_name}{x}")

  def click_buy_item(self, id, max_clicks=3):
    try: 
      c = 0
      item = self.driver.find_element(By.ID, id)
      while 'enabled' in item.get_attribute('class') and c < max_clicks:
        item.click()
        c += 1
    except: 
      pass

  def click_cookie(self):
    self.big_cookie.click()

  def evaluate_shimmers(self): 
    for shimmer in self.driver.find_elements(By.CLASS_NAME, "shimmer"):
      shimmer.click()
      print(f"Clicked shimmer {shimmer.get_attribute('id')}")

  def run_loop(self, join_at_end=True, log_details=False): 
    tic = time.perf_counter()
    ret_val = {}
    if self.click_shimmer:
      t = threading.Thread(target=self.evaluate_shimmers)
      ret_val['shimmer'] = [t]
      t.start()
    if self.buy_products:
      t = threading.Thread(target=self.click_buyables, args=('product',))
      ret_val['product'] = [t]
      t.start()
    if self.buy_upgrades:
      t = threading.Thread(target=self.click_buyables, args=('upgrade',))
      ret_val['upgrade'] = [t]
      t.start()
    if self.run_clicker:
      ret_val['clicker'] = []
      for _ in range(self.clicker_loop_count):
        t = threading.Thread(target=self.click_cookie)
        ret_val['clicker'].append(t)
        t.start()
    if join_at_end:
      for tl in ret_val.values(): 
        for t in tl:
          t.join()
    toc = time.perf_counter()
    print(f"Ran loop in {toc - tic:0.4f} seconds - { {k: len(v) for k, v in ret_val.items()} }")
    if log_details:
      print(f"Loop counts: ")
      for k, v in ret_val.items():
        print(f"    {k}: {len(v)}")
      print("")

if __name__ == '__main__': 
  ccc = CookieClickerClicker()
  # keyboard.on_press_key("u", ccc.toggle_buy_upgrades)
  # keyboard.on_press_key("p", ccc.toggle_buy_products)
  # keyboard.on_press_key("c", ccc.toggle_run_clicker)
  
  while True: 
    ccc.run_loop()