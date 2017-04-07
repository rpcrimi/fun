import time
import requests
from selenium import webdriver

for i in range(100):
	print "Iteration %d" % i
	driver = webdriver.Firefox()
	driver.set_window_position(10000, 0)
	driver.get("https://www.instagram.com/p/BPGiNMuAzKU/")
	element = driver.find_element_by_class_name('_c2kdw').click()
	time.sleep(55)
	driver.quit()