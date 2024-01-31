import webbrowser
import wikipedia
import subprocess
import requests
import openai
import speedtest
import random
import bs4
from bs4 import BeautifulSoup
import re

class NarvisHelper:
    def __init__(self):
        self.wikipedia_data = {
            'Python': 'Python is a high-level, interpreted programming language...',
            'Artificial Intelligence': 'Artificial Intelligence (AI) is the simulation of human intelligence...',
            'Space Exploration': 'Space exploration is the use of astronomy and space technologies to explore outer space...',
            # Tambahkan entri-entri Wikipedia lainnya sesuai kebutuhan
        }

        # Masukkan kunci API OpenAI, J&T, dan MediaStack langsung di sini
        self.openai_api_key = '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'
        self.weather_api_key = '443f8ce319ad4c4ba27164818240501'
        self.jnt_api_key = '6a35d330a55de6883ceeaca03cc4871c'
        self.mediastack_api_key = '9fe5a2c756d9553c954993b6f9b26477'

        self.responses = {
            'apa kabar': 'Saya baik, terima kasih! Bagaimana dengan Anda?',
            'siapa namamu': 'Saya adalah Narvis Helper, senang bertemu dengan Anda!',
            'buka aplikasi': self.open_application,
            'buka youtube': lambda: self.open_link('https://www.youtube.com'),
            'cari di youtube': self.search_youtube,
            'buka tiktok': lambda: self.open_link('https://www.tiktok.com'),
            'cari di google': self.search_google,
            'cari di tiktok': self.search_tiktok,
            'mencari kata kunci di wikipedia': self.search_wikipedia,
            'tanya ai': self.ask_gpt2,
            'translate': self.translate_text,
            'pengingat': self.remind_me,
            'cek ip saya': self.check_ip,
            'cek cuaca': self.check_weather,
            'lacak paket': self.track_package,  # Tambahkan fitur pelacakan resi J&T
            'search': self.secret_search,
            'berita indonesia': self.get_news,  # Tambahkan fitur berita Indonesia
            'tes kecepatan': self.test_speed,  # Tambahkan fitur tes kecepatan internet
            'simulate hacking multiple': self.simulate_hacking_multiple,  # Tambahkan fitur simulasi hacking multiple
            'hitung': self.calculate_math,
            'pujian': self.compliment,
            'lelucon': self.indonesian_joke,
            'ramalan': self.fortune_cookie,          
            'leave': self.exit_narvis,
            '/help': self.show_help,
            # Tambahkan pertanyaan dan jawaban sesuai kebutuhan
        }

       

        self.access_code = 'n4s11d'  # Ganti dengan kode akses yang Anda inginkan
        self.logged_in = False
                    
           
    def calculate_math(self):
        math_expression = input('\033[95mMasukkan ekspresi matematika: \033[0m')  # Warna ungu untuk input ekspresi matematika
        sanitized_expression = re.sub(r'[^0-9+\-*/().]', '', math_expression)  # Membersihkan ekspresi dari karakter tidak valid

        try:
            result = eval(sanitized_expression)
            self.print_narvis_message(f'Hasil perhitungan: {result}')
        except Exception as e:
            self.print_narvis_message(f'Gagal menghitung ekspresi: {e}')

    def authenticate(self):
        user_code = input('\033[95mMasukkan kode akses: \033[0m')
        if user_code == self.access_code:
            self.logged_in = True
            self.print_narvis_message('Autentikasi berhasil. Selamat datang, NarvisHelp Siap Membantu!')
        else:
            self.print_narvis_message('\033[91mKode akses salah. Autentikasi gagal.\033[91m')

    def exit_narvis(self):
        self.print_narvis_message('\033[91mTerima kasih! Sampai jumpa.\033[0m')
        self.logged_in = False
        
    def print_narvis_message(self, message):
        print(f'\033[92mNarvis: {message}\033[0m')  # Warna hijau untuk pesan Narvis

    def print_user_message(self, message):
        print(f'\033[94mAnda: {message}\033[0m')  # Warna biru untuk pesan pengguna

    def open_application(self):
        app_name = input('\033[95mNama aplikasi yang ingin dibuka: \033[0m')  # Warna ungu untuk input aplikasi
        package_name = self.get_package_name(app_name)
        if package_name:
            try:
                subprocess.run(['adb', 'shell', 'monkey', '-p', package_name, '-c', 'android.intent.category.LAUNCHER', '1'])
                self.print_narvis_message(f'Membuka aplikasi: {app_name}')
            except subprocess.CalledProcessError as e:
                self.print_narvis_message(f'Gagal membuka aplikasi: {e}')
            except Exception as e:
                self.print_narvis_message(f'Error: {e}')
        else:
            self.print_narvis_message(f'Tidak dapat menemukan paket aplikasi untuk: {app_name}')


    def open_link(self, link):
        webbrowser.open(link)

    def search_youtube(self):
        query = input('\033[95mMasukkan kata kunci pencarian di YouTube: \033[0m')  # Warna ungu untuk input pencarian YouTube
        search_url = f'https://www.youtube.com/results?search_query={query}'
        self.open_link(search_url)           

    
    
    def search_duckduckgo(self):
        query = input('\033[95mMasukkan kata kunci pencarian: \033[0m')
        self.print_narvis_message('Hasil pencarian:')
        results = self.secret_search(query)

        if results:
            display_limit = 5
            total_results = len(results)

            for i, result in enumerate(results[:display_limit], start=1):
                self.print_narvis_message(f"{i}. {result['title']} ({result['link']})")

            if total_results > display_limit:
                show_more = input('\033[95mIngin melihat lebih banyak hasil? (ya/tidak): \033[0m')
                if show_more.lower() == 'ya':
                    for i, result in enumerate(results[display_limit:], start=display_limit + 1):
                        self.print_narvis_message(f"{i}. {result['title']} ({result['link']})")

                    selected_index = input('\033[95mPilih nomor hasil yang ingin dibuka (ketik "selesai" untuk kembali): \033[0m')

                    if selected_index.lower() == 'selesai':
                        self.print_narvis_message('Kembali ke menu utama.')
                    elif selected_index.isdigit() and 1 <= int(selected_index) <= len(results):
                        selected_result = results[int(selected_index) - 1]
                        self.open_link(selected_result['link'])
                    else:
                        self.print_narvis_message('Pilihan tidak valid. Kembali ke menu utama.')
                else:
                    self.print_narvis_message('Tidak ada hasil tambahan.')
        else:
            self.print_narvis_message('Tidak ada hasil pencarian.')

    def secret_search(self, query):
        search_url = f'https://duckduckgo.com/html/?q={query.replace(" ", "+")}'
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            search_results = soup.select('.result__a')

            if not search_results:
                self.print_narvis_message('Tidak ada hasil ditemukan.')
                return []

            results = []
            for result in search_results[:5]:
                title = result.text
                link = result['href']
                results.append({'title': title, 'link': link})

            return results
        except requests.RequestException as e:
            self.print_narvis_message(f'Gagal melakukan pencarian: {e}')
            return []
    def search_google(self):
        query = input('\033[95mMasukkan kata kunci pencarian di Google: \033[0m')  # Warna ungu untuk input pencarian Google
        search_url = f'https://www.google.com/search?q={query}'
        self.open_link(search_url)

    def search_tiktok(self):
        query = input('\033[95mMasukkan kata kunci pencarian di TikTok: \033[0m')  # Warna ungu untuk input pencarian TikTok
        search_url = f'https://www.tiktok.com/search?q={query}'
        self.open_link(search_url)

    def search_wikipedia(self):
        query = input('\033[95mMasukkan kata kunci pencarian di Wikipedia: \033[0m')  # Warna ungu untuk input pencarian Wikipedia
        matching_key = next((key for key in self.wikipedia_data.keys() if key.lower() == query.lower()), None)
        if matching_key:
            self.print_narvis_message(f"Informasi dari Wikipedia: {self.wikipedia_data[matching_key]}")
        else:
            self.print_narvis_message(f"Tidak ada hasil ditemukan untuk '{query}' di Wikipedia lokal.")
    
    
    def ask_gpt2(self):
        while True:
            user_question = input('\033[95mApa pertanyaan Anda? \033[0m')  # Warna ungu untuk input pertanyaan AI
            if user_question.lower() == 'tidak':
                self.print_narvis_message('\033[91mTerima kasih! Sampai jumpa.\033[0m')  # Warna merah untuk pesan perpisahan
                break

            gpt2_endpoint = 'https://api.openai.com/v1/engines/text-davinci-003/completions'  # Ganti dengan endpoint model GPT-2 Anda
            openai.api_key = self.openai_api_key

            try:
                response = openai.Completion.create(
                    engine="text-davinci-003",  # Ganti dengan model GPT-2 yang sesuai
                    prompt=user_question,
                    max_tokens=150
                )
                answer = response.choices[0].text.strip()
                self.print_narvis_message(answer)

                # Tambahkan logika untuk menentukan apakah pertanyaan tambahan diperlukan
                if "apakah ada pertanyaan lain?" in answer.lower():
                    continue
                else:
                    self.print_user_message(user_question)
                    self.handle_user_input(user_question)

            except Exception as e:
                self.print_narvis_message(f'Gagal mendapatkan jawaban dari GPT-2: {e}')

    def handle_user_input(self, user_input):
        response = self.responses.get(user_input.lower())
        if response:
            if callable(response):
                self.print_user_message(user_input)  # Tambahkan pesan pengguna ke chat
                response()
            else:
                self.print_narvis_message(response)  # Tambahkan pesan Narvis ke chat
        else:
            self.print_narvis_message("\033[93mAda Pertanyaan Lain? Ketik \033[91mTIDAK\033[91m Untuk Selesai.\033[0m")

    def run_narvis(self):
        while True:
            user_input = input('\033[95mPerintah Anda: \033[0m')  # Warna ungu untuk input pengguna

            if user_input.lower() == 'selesai':
                self.print_narvis_message('\033[91mTerima kasih! Sampai jumpa.\033[0m')  # Warna merah untuk pesan perpisahan
                break
        self.handle_user_input(user_input.lower())
    
    def show_help(self):
        self.print_narvis_message("Daftar Perintah Pengguna:")
        for command in self.responses.keys():
            self.print_narvis_message(f"- {command}")

    def get_package_name(self, app_name):
        try:
            result = subprocess.check_output(['adb', 'shell', 'pm', 'list', 'packages', '-f']).decode('utf-8')
            for line in result.split('\n'):
                if app_name.lower() in line.lower():
                    return line.split(':')[1].strip()
        except Exception as e:
            self.print_narvis_message(f'Gagal mendapatkan paket aplikasi: {e}')
            return None

    def check_ip(self):
        try:
            # Gunakan cara yang lebih andal untuk mendapatkan alamat IP pengguna
            response = requests.get('https://api64.ipify.org?format=json')
            user_ip = response.json().get('ip')
            self.print_narvis_message(f'Alamat IP Anda adalah: {user_ip}')
        except requests.RequestException as e:
            self.print_narvis_message(f'Gagal mendapatkan alamat IP: {e}')

    def check_weather(self):
        city = input('\033[95mMasukkan nama kota untuk cek cuaca: \033[0m')  # Warna ungu untuk input nama kota
        try:
            weather_url = f'http://api.weatherapi.com/v1/current.json?key={self.weather_api_key}&q={city}'
            response = requests.get(weather_url)
            data = response.json()
            
            if 'error' in data:
                self.print_narvis_message(f"Gagal mendapatkan informasi cuaca untuk {city}: {data['error']['message']}")
            else:
                temperature = data['current']['temp_c']
                condition = data['current']['condition']['text']
                self.print_narvis_message(f"Cuaca saat ini di {city}: {temperature}°C, {condition}")
        except requests.RequestException as e:
            self.print_narvis_message(f'Gagal mendapatkan informasi cuaca: {e}')

    def track_package(self):
        tracking_number = input('\033[95mMasukkan nomor pelacakan paket J&T: \033[0m')  # Warna ungu untuk input nomor pelacakan
        try:
            jnt_url = f'https://api.jnt.id/tracking/v1/track?number={tracking_number}'
            headers = {'Authorization': f'Bearer {self.jnt_api_key}'}
            response = requests.get(jnt_url, headers=headers)
            data = response.json()
            
            if 'error' in data:
                self.print_narvis_message(f"Gagal melacak paket: {data['error']['message']}")
            else:
                status = data['result']['status']
                self.print_narvis_message(f"Status pelacakan untuk paket {tracking_number}: {status}")
        except requests.RequestException as e:
            self.print_narvis_message(f'Gagal melacak paket: {e}')

    def get_news(self):
        try:
            country_code = 'id'  # Kode negara untuk Indonesia
            news_url = f'http://api.mediastack.com/v1/news?access_key={self.mediastack_api_key}&countries={country_code}'
            response = requests.get(news_url)
            data = response.json()
            
            if 'error' in data:
                self.print_narvis_message(f"Gagal mendapatkan berita: {data['error']['info']}")
            else:
                articles = data['data']
                for index, article in enumerate(articles, start=1):
                    title = article.get('title', 'Tidak ada judul')
                    source = article.get('source', 'Sumber tidak diketahui')
                    self.print_narvis_message(f"{index}. {title} (Sumber: {source})")

                selected_index = input('\033[95mPilih nomor berita yang ingin dibaca (ketik "selesai" untuk kembali): \033[0m')

                if selected_index.lower() == 'selesai':
                    self.print_narvis_message('Kembali ke menu utama.')
                elif selected_index.isdigit() and 1 <= int(selected_index) <= len(articles):
                    selected_article = articles[int(selected_index) - 1]
                    article_title = selected_article.get('title', 'Tidak ada judul')
                    article_content = selected_article.get('content', 'Tidak ada konten')
                    self.print_narvis_message(f"Berita terpilih: {article_title}\n{article_content}")
                else:
                    self.print_narvis_message('Pilihan tidak valid. Kembali ke menu utama.')
        except requests.RequestException as e:
            self.print_narvis_message(f'Gagal mendapatkan berita: {e}')

    def test_speed(self):
        try:
            st = speedtest.Speedtest()
            download_speed = st.download()
            upload_speed = st.upload()

            self.print_narvis_message(f'Kecepatan unduh: {download_speed / 1024 / 1024:.2f} Mbps')
            self.print_narvis_message(f'Kecepatan unggah: {upload_speed / 1024 / 1024:.2f} Mbps')
        except Exception as e:
            self.print_narvis_message(f'Gagal melakukan tes kecepatan: {e}')

    def simulate_hacking(self):
        code_length = random.randint(50, 200)  # Panjang kode acak antara 50 dan 200 karakter
        code = ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*()_-+=') for _ in range(code_length))

        repeat_count = random.randint(3, 10)  # Jumlah pengulangan kode
        hacked_code = code * repeat_count

        self.print_narvis_message('Hacking in progress...')
        self.print_narvis_message(hacked_code)

    def simulate_hacking_multiple(self):
        count = int(input('\033[95mMasukkan jumlah simulasi hacking yang diinginkan: \033[0m'))
        for _ in range(count):
            self.simulate_hacking()
            
     

    def compliment(self):
        compliments = [
            "Anda benar-benar cerdas!",
            "Tingkat produktivitas Anda luar biasa.",
            "Anda memiliki kehadiran yang menginspirasi.",
            "Anda membuat dunia ini menjadi tempat yang lebih baik.",
            "Pandangan Anda sangat berharga."
        ]
        random_compliment = random.choice(compliments)
        self.print_narvis_message(random_compliment)

    def indonesian_joke(self):
        joke_url = "https://icanhazdadjoke.com/search?term=indonesia"
        headers = {'Accept': 'application/json'}
        try:
            response = requests.get(joke_url, headers=headers)
            data = response.json()

            if data.get('results'):
                random_joke = random.choice(data['results'])
                joke_text = random_joke.get('joke', "Maaf, tidak dapat menemukan lelucon saat ini.")
                self.print_narvis_message(joke_text)
            else:
                self.print_narvis_message("Maaf, tidak dapat menemukan lelucon saat ini.")
        except requests.RequestException as e:
            self.print_narvis_message(f'Gagal mendapatkan lelucon: {e}')

    # (Metode lainnya)

    def fortune_cookie(self):
        fortune_url = "https://www.yerkee.com/api/fortune"
        try:
            response = requests.get(fortune_url)
            data = response.json()
            fortune_text = data.get("fortune", "Maaf, tidak dapat menemukan ramalan saat ini.")
            self.print_narvis_message(f"Ramalan Hari Ini: {fortune_text}")
        except requests.RequestException as e:
            self.print_narvis_message(f'Gagal mendapatkan ramalan: {e}')
            
            # (Metode sebelumnya)

    def translate_text(self):
        text_to_translate = input('\033[95mMasukkan teks yang ingin diterjemahkan: \033[0m')
        target_language = input('\033[95mMasukkan kode bahasa tujuan (contoh: id untuk Bahasa Indonesia): \033[0m')

        translation_url = f'https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={text_to_translate}'

        try:
            response = requests.get(translation_url)
            data = response.json()
            translated_text = data[0][0][0]

            self.print_narvis_message(f'Teks terjemahan: {translated_text}')
        except requests.RequestException as e:
            self.print_narvis_message(f'Gagal menerjemahkan teks: {e}')

    def remind_me(self):
        reminder_text = input('\033[95mApa yang ingin Anda diingatkan? \033[0m')
        reminder_time = input('\033[95mKapan Anda ingin diingatkan? (contoh: 15:30) \033[0m')

        # Simulasi sederhana untuk pengingat
        current_time = datetime.datetime.now().strftime('%H:%M')
        if current_time >= reminder_time:
            self.print_narvis_message(f"Waktu pengingat ({reminder_time}) telah berlalu. Anda diingatkan: {reminder_text}")
        else:
            self.print_narvis_message(f"Anda akan diingatkan pada pukul {reminder_time}.")


    def run_narvis(self):
        while not self.logged_in:
            print('\033[91mDev: @Nar\033[91m')
            self.print_narvis_message('Silakan autentikasi terlebih dahulu.')
            self.authenticate()

        while self.logged_in:
            user_input = input('\033[95mPerintah Anda: \033[0m')

            response = self.responses.get(user_input.lower())
            if response:
                if callable(response):
                    response()
                else:
                    self.print_narvis_message(response)
            else:
                self.print_narvis_message("\033[93mPerintah tidak dikenali. Ketik '/help' untuk melihat daftar perintah.\033[0m")
                
    def print_narvis_message(self, message):
        print(f'\033[92mNarvis: {message}\033[0m')  # Warna hijau untuk pesan Narvis

# Contoh penggunaan:
narvis = NarvisHelper()
narvis.run_narvis()