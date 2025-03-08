import os
import time
import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller

#  Fix: Matikan XNNPACK delegate agar tidak error
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
os.environ["TF_LITE_DISABLE_XNNPACK"] = "1"

#  Auto-install ChromeDriver jika belum ada
chromedriver_autoinstaller.install()

#  Path ke Tesseract OCR (ganti sesuai lokasi instalasi)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Konfigurasi Chrome agar lebih stabil
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

#  Jalankan WebDriver tanpa manual install
driver = webdriver.Chrome(options=chrome_options)

# Buka halaman login Kolotibablo
driver.get("https://kolotibablo.com/")

# Tunggu user login secara manual
print("Silakan login terlebih dahulu di Chrome yang terbuka.")
input("Tekan ENTER setelah login untuk melanjutkan...")

# Setelah login, buka halaman kerja captcha
driver.get("https://kolotibablo.com/id/workers/earn")
time.sleep(5)  # Tunggu halaman termuat

print("Bot siap untuk mengerjakan captcha!")

#  Loop utama
while True:
    try:
        #  Cek apakah ada captcha
        captcha_img = driver.find_element(By.XPATH, "//img[@class='captcha-image']")
        
        #  Ambil lokasi dan ukuran elemen captcha
        location = captcha_img.location
        size = captcha_img.size

        #  Screenshot full layar lalu crop captcha
        driver.save_screenshot("full_screenshot.png")
        img = Image.open("full_screenshot.png")

        #  Crop area captcha
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        captcha_image = img.crop((left, top, right, bottom))
        
        #  Simpan gambar captcha
        captcha_image.save("captcha.png")
        print("Captcha disimpan!")

        #  Gunakan Tesseract OCR untuk membaca teks captcha
        ocr_config = "--psm 7 --oem 3"
        captcha_text = pytesseract.image_to_string(captcha_image, config=ocr_config).strip()
        print(f"Captcha terbaca: {captcha_text}")

        #  Temukan input field captcha dan masukkan teks
        captcha_input = driver.find_element(By.XPATH, "//input[@type='text']")
        captcha_input.clear()
        captcha_input.send_keys(captcha_text)
        captcha_input.send_keys(Keys.RETURN)

        print("Captcha dikirim!")

        # Tunggu beberapa detik sebelum mencari captcha baru
        time.sleep(3)

    except Exception as e:
        print(f"Tidak ada captcha atau terjadi error: {e}")
        time.sleep(5)  # Coba lagi setelah 5 detik


