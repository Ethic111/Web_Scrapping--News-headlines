# Python 3 code
# Import library packages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime, time, os
import smtplib
from email.message import EmailMessage

WITH_BROWSER = False
WITH_ATTACHMENT = False
NEWS_SITE = "https://news.google.com/topstories?hl=en-IN&gl=IN&ceid=IN:en"
FILE_LOCATION = r'C:\project_py\newsfile.txt'



def print_intro_to_console():
    td = datetime.date.today()
    print ("Connecting to Authentic News source, Please wait .....\n")
    print (" ------------------------------------------------------------------------------------------- ")
    print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>  TODAY's TOP NEWS HEADLINES  <<<<<<<<<<<<<<<<<<<<<<<<<<<<< ")
    print ("Date:",td.strftime("%b-%d-%Y"))
    print (" -------------------------- ")

# create a webdriver object for chrome-option and configure
def fetch_news_content():
    wait_imp = 10
    CO = webdriver.ChromeOptions()
    CO.add_experimental_option('useAutomationExtension', False)
    CO.add_argument('--ignore-certificate-errors')
    CO.add_argument('--start-maximized')
    if not WITH_BROWSER:
        CO.add_argument("headless")
    wd = webdriver.Chrome(r'C:\Windows\chromedriver.exe',options=CO)
    # Web driver to openup website
    wd.get(NEWS_SITE)
    wd.implicitly_wait(wait_imp)
    elems = wd.find_elements(By.XPATH, "//*/div/article/div[1]/a")
    return elems

def write_to_files(elems):
    file_to_write = open(FILE_LOCATION, 'w+',encoding="utf-8")
    for idx, elem in enumerate(elems):
        file_to_write.write(str(idx + 1)+ '>> ')
        file_to_write.write(elem.get_attribute('aria-label')+'\n')
    file_to_write.close()
    print('\n')


def get_html_content(elems):
    links = []
    for elem in elems:
        news = elem.get_attribute('aria-label')
        news_link = elem.get_attribute('href')
        links.append(f'<a href="{news_link}">{news}</a>')
    html = f'''
    <html>
        <body>
            <h1>Hot and Top News Of Today</h1>
            {'<br/><br/>'.join(links)}
        </body>
    </html>'''
    return html



def send_email(news_content, email_to):
    USER_EMAIL = email_to
    MY_PASS = "zyzmqscirtmppixr"
    MY_EMAIL = "accdum666@gmail.com"
    
    # Compose message
    msg = EmailMessage()
    msg['From'] = MY_EMAIL
    msg['To']   = USER_EMAIL
    msg['Subject'] = " Hello ! Today's TOP news HEADLINES >>"

    if WITH_ATTACHMENT:
        with open(FILE_LOCATION,'rb') as f:
            N_file = f.read()
            msg.set_content("Find the attached document for detailed NEWS ...")
            msg.add_attachment(N_file, maintype = 'document',subtype = 'txt', filename = f.name )
    else:
        msg.set_content(get_html_content(news_content), subtype='html')

    server = smtplib.SMTP('smtp.gmail.com', 587) #tls , ssl
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(MY_EMAIL,MY_PASS)
    server.send_message(msg)

    # printing final info
    print (f"A copy of this NEWS HEADLINES has been sent to your E-mail ({email_to}) Successfuly !!")
    server.quit()

def print_news_to_console(news_content):
    for idx, elem in enumerate(news_content):
        print(idx+1, elem.get_attribute('aria-label'), sep=' >> ')

if __name__ == "__main__":

    receipients = ['accdum666@gmail.com']

    with_news = input('Want news in email attachment ? (Y/N)\n')
    if(with_news.lower() == 'y'):
        WITH_ATTACHMENT = True
    
    with_browser = input('Do you want to see the browser loading while fetching the news ? (Y/N)\n')
    if(with_browser.lower() == 'y'):
        WITH_BROWSER = True

    email_to_list = input('Enter additional email recepients list seperated by comma <,>\n')
    if(email_to_list):
        receipients.extend(email_to_list.split(','))

    print_intro_to_console()

    news_content = fetch_news_content()

    print_news_to_console(news_content)

    if WITH_ATTACHMENT:
        write_to_files(news_content)

    for receipient in receipients:
        send_email(news_content, email_to=receipient)
    