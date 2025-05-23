import random
import pandas as pd
from seleniumbase import SB
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import time
import os
from dotenv import load_dotenv
load_dotenv()


# ================== Konfigurasi ==================
twitter_email = os.getenv("TWITTER_EMAIL")
twitter_username = os.getenv("TWITTER_USERNAME")
twitter_password = os.getenv("TWITTER_PASSWORD")

keyword = os.getenv("KEYWORD")
jumlah_tweet = os.getenv("JUMLAH_TWEET")
tanggal_mulai = os.getenv("TANGGAL_MULAI")
tanggal_akhir = os.getenv("TANGGAL_AKHIR")
# =================================================

with SB(test=True, uc=True) as sb:
    sb.open("https://twitter.com/i/flow/login")
    sb.sleep(3)
    
    sb.type('input[name="text"]', twitter_email)
    sb.send_keys('input[name="text"]', Keys.ENTER)
    sb.sleep(3)
    
    sb.type('input[name="text"]', twitter_username)
    sb.send_keys('input[name="text"]', Keys.ENTER)
    sb.sleep(3)
    
    sb.type('input[name="password"]', twitter_password)
    sb.send_keys('input[name="password"]', Keys.ENTER)  # ENTER
    sb.sleep(5)

    query = f"{keyword} since:{tanggal_mulai} until:{tanggal_akhir} lang:id"
    search_url = f"https://twitter.com/search?q={query}&src=typed_query"
    sb.open(search_url)
    sb.sleep(5)

    tweets_data = set()
    tweets = []
    
    while len(tweets) < jumlah_tweet:
        elements = sb.find_elements('//article[@data-testid="tweet"]')
        
        for el in elements:
            try:
                konten = el.text
                if konten not in tweets_data:
                    tweets_data.add(konten)
                    
                    spans = el.find_elements("xpath", ".//span")
                    texts = [span.text for span in spans if span.text.strip() != ""]
                    full_text = " ".join(texts)
                    
                    username = el.find_element("xpath", './/div[@dir="ltr"]//span').text
                    waktu_utc = el.find_element("xpath", './/time').get_attribute('datetime')
                    
                    waktu_obj = datetime.fromisoformat(waktu_utc.replace("Z", "+00:00"))
                    waktu_wib = waktu_obj + timedelta(hours=7)
                    waktu_str = waktu_wib.strftime("%d-%m-%Y %H:%M")

                    tweets.append({
                        "username": username,
                        "waktu": waktu_str,
                        "konten": full_text
                    })
                    
                    print(f"Mendapatkan tweet ke -{len(tweets)}")
                    
                if len(tweets) >= jumlah_tweet:
                    break
                
                
            except Exception as e:
                print(f"Gagal mengambil tweets Error: {e}")
                continue
            
        sb.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))
        
    # sb.quit()
    
    df = pd.DataFrame(tweets)
    df.to_csv("tweets.csv", index=False)

    try:
        df.to_excel("tweets.xlsx", index=False)
        print("Berhasil menyimpan ke Excel.")
    except Exception as e:
        print(f"Gagal menyimpan ke Excel. Error: {e}")

    
    print(f"Berhasil menyimpan {len(df)} tweets ke dalam file CSV dan Excel")
