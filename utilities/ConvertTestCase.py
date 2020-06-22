code='../orangehrm.py.xpath'
code_css='../orangehrm.py'
tc = 'C:\\Users\\h.imhah\\Desktop\\testcase.txt'
base_url = 'http://localhost/orangehrm'

def convert_katalon():
    with open(tc, encoding='utf-8') as f:
        for line in f:
            line = line.replace('\n', '')
            if ('def ' in line) and ('(self)' in line):
                print(line)
                continue
            if ('.click()' in line):
                line = line.replace('.click()', '')
                line = line.replace ('driver.find_element_by_xpath(', 'self.click(')
                line = line.replace ('driver.find_element_by_id("', 'self.click("#')
                print (line)
                continue
            if ('.clear()' in line):
                continue
            if ('.send_keys(' in line):
                line = line.replace ('driver.find_element_by_xpath(', 'self.type(')
                line = line.replace ('driver.find_element_by_id("', 'self.type("#')
                line = line.replace (').send_keys(', ', ')
                print (line)
                continue
            if (').text' in line):
                line = line.replace('driver.find_element_by_xpath(', 'self.get_text(')
                line = line.replace('.text', '')
                print (line)
                continue
            if ('Select(driver.' in line):
                line = line.replace('Select(driver.find_element_by_id("', 'self.select("#')
                line = line.replace(')).select_by_visible_text("', ', "label=')
            if ('driver.get' in line):
                line = line.replace('driver.get', 'self.get')
                line = line.replace(base_url, '')
                print (line)
                continue
            else:
                print(line)

def extract_id (line):
    start = line.find('[@id=\'') + 6
    end = line.find("'", start)
    return (line[start:end])

def extract_xpath (line):
    start = line.find('("') + 2
    end = line.find('"', start)
    return(line[start:end])

convert_katalon()