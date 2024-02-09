import os

def install_modules():
    # Cài đặt các module Node.js
    
    os.system('npm install user-agents cheerio keepalive.js header-generator request fake-useragent randomstring colors axios cheerio gradient-string cloudscraper set-cookie-parser random-useragent crypto-random-string playwright-extra fingerprint-generator fingerprint-injector ua-parser-js http2 minimist socks puppeteer hcaptcha-solver puppeteer-extra puppeteer-extra-plugin-recaptcha puppeteer-extra-plugin-stealth http zombie random-referer jar')
    os.system('pip install telebot')
    os.system('pip install psutil')
    print("Cài đặt thành công các module.")

if __name__ == "__main__":
    install_modules()
