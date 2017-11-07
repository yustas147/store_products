from selenium import webdriver

#driver = webdriver.Chrome()
driver = webdriver.PhantomJS(executable_path="c:\\Python27\\phantomjs.exe", port=7777)
driver.get("https://502data.com/license/415645")
#driver.get("http://www.youtube.com/results?search_query=" + "guitar+lessons")

results = driver.find_elements_by_xpath('.//div[@class="col-md-8"]/div[@class="pull-left"]/a/img')
#results = driver.find_elements_by_xpath('//div[@class="yt-lockup-content"]')

print(len(results))

for result in results:
    video = result.find_element_by_xpath('.//h3/a')
    title = video.get_attribute('title')
    url = video.get_attribute('href')
    print("{} ({})".format(title, url))
driver.quit()