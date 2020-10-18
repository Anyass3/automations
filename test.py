#A selenium.webdriver test on loalhost

from mywebdriver import Chrome, webdriver
from check import confirm, ShortenName
from t import paragraph, sentence
webdriver()
driver = Chrome()
amail = 'nyassabu@gmail.com'
apass = 'nyassabu'
email = 'testing14145@gmail.com'
pwd = 'password'
role = 'Association'


def add_admin():
    driver.get("http://127.0.0.1:5000/myadmin/add")
    driver.implicitly_wait(3)
    driver.find_element_by_name('f_name').send_keys('Abdullah')
    driver.find_element_by_name('l_name').send_keys('Nyass')
    driver.find_element_by_name('address').send_keys('shorten')
    driver.find_element_by_name('phone').send_keys('12346789') #todo
    driver.find_element_by_name('code').send_keys('123456')
    driver.find_element_by_name('email').send_keys(amail)
    driver.find_element_by_name('password').send_keys(apass)
    driver.find_element_by_name('confirm_password').send_keys(apass)
    driver.find_element_by_name('submit').click()

def send_code(amail, apass, role, email):
        
    driver.get("http://127.0.0.1:5000/myadmin/login")

    driver.find_element_by_name('email').send_keys(amail)
    driver.find_element_by_name('password').send_keys(apass)
    driver.find_element_by_name('submit').click()

    driver.find_element_by_link_text('Account').click()
    driver.find_element_by_link_text(f'Send code to {role}').click()

    driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_name('submit').click()

    driver.find_element_by_link_text('Logout').click()

def get_code():
    pass

def check_mail(email, pwd):
        
    driver.implicitly_wait(6)

    driver.get("https://mail.google.com")
    driver.find_element_by_name('identifier').send_keys(email)
    driver.find_element_by_id('identifierNext').click()
    #driver.find_elements_by_tag_name('div').
    driver.implicitly_wait(4)
    driver.find_element_by_name('password').send_keys(pwd)
    #driver.find_element_by_class_name('Xb9hP').send_keys('@Testing14145')
    driver.find_element_by_id('passwordNext').click()

    driver.implicitly_wait(14)

    #driver.find_element_by_id('text').click()
    #driver.find_element_by_name('website.an').click()
    #driver.find_elements_by_xpath('//*[@id=":2z"]')
    unread = driver.find_elements_by_class_name('zE')

    for i in range(len(unread)):
        if 'Your code' in unread[i].text:
            code_text = unread[i].text
            #print(code_text)


    s1=code_text.split(':')
    s2=s1[1]
    s3=s2.split(' ')
    num=str(1234567890)

    for i in s3:
        s=i
        if len(s) == 6:
            for a in s:
                if a in num:
                    code=s
    return code



def register(name, email, pwd='nyassabou'):
        
    driver.get("http://127.0.0.1:5000/")
    text = 'Register'
    codes = []
    confirm(codes)
    c=0
    #pw='0b3016'#code
    for pw in codes:
        
        code = pw
        #print(f'woow {code} appears')
        driver.implicitly_wait(4)

        c+=1
        shorten = ShortenName(name)

        driver.find_element_by_link_text(text).click()
        driver.find_element_by_name('or_name').send_keys(name)
        driver.find_element_by_name('shorten').send_keys(shorten) #todo
        driver.find_element_by_name('email').send_keys(email)
        driver.find_element_by_name('code').send_keys(code)
        driver.find_element_by_name('password').send_keys(pwd)
        driver.find_element_by_name('confirm_password').send_keys(pwd)
        driver.find_element_by_name('submit').click()
        if c%100==0:
            print(c)
        remainder = len(codes) - c
        if c % 1000 == 0:
            print(f'{c} is checked')
            print(f'Remaining {remainder}')
            print('#' * 10)
        driver.implicitly_wait(4)
    #else:
    #    print('code is secure')

def login(email, role, pwd='nyassabou'):
    role = role.lower()
    driver.get(f"http://127.0.0.1:5000/login/{role}")
    driver.implicitly_wait(2)

    driver.find_element_by_name('email').send_keys(email)
    driver.find_element_by_name('password').send_keys(pwd)
    driver.find_element_by_name('submit').click()


def post():
    driver.get("http://127.0.0.1:5000/post/new")
    driver.implicitly_wait(3)

    title = sentence(10)
    content = paragraph()

    driver.find_element_by_name('title').send_keys(title)
    driver.find_element_by_name('content').send_keys(content)
    driver.find_element_by_name('submit').click()

#driver.back()
#driver.forward()
#
#name='International Association for Bridge and Structural Engineering '
#register(name, email)
def makePost(amount=20):
    s=0
    a=0
    try:
        for i in range(amount):
            if i%2==0:
                a+=1
                login('nyassabou@gmail.com', 'Association')
                print(f'An Association logged in')
            else:
                s+=1
                login('general14145@gmail.com', 'Scholar')
                print(f'A Scholar logged in')#todo 
            post()
            print(f'total posts = {i+1}')
            driver.find_element_by_link_text('Logout').click()
            driver.find_element_by_xpath('//*[@id="logoutModal"]/div/div/div[2]/form/input').click()
            driver.implicitly_wait(3)
    except:
        print('There was an error')

#todo: not ready
def download():
    driver.get("https://www.google.com/search?q=corona")
download()
#makePost(40)
