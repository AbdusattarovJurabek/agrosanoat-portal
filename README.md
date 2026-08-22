# Agrosanoatni rivojlantirish agentligi portali

Rasmiy portal, xavfsiz admin panel va murojaatlar API-si. Tizim tashqi backend
kutubxonalarisiz Python standart kutubxonasida ishlaydi.

## Ishga tushirish

Python 3.9 yoki yangiroq versiya kerak.

~~~bash
ADMIN_PASSWORD='uzun-va-tasodifiy-parol' python3 server.py
~~~

Sayt: http://127.0.0.1:8000  
Admin panel: http://127.0.0.1:8000/admin.html  
Standart admin login: admin

Login nomini ham environment orqali almashtirish mumkin:

~~~bash
ADMIN_USERNAME='portal-admin' ADMIN_PASSWORD='uzun-va-tasodifiy-parol' python3 server.py
~~~

ADMIN_PASSWORD berilmasa ommaviy sayt ishlaydi, ammo admin login xavfsizlik
sababli o‘chiriladi.

## Docker orqali ishga tushirish

Loyihada Docker Compose konfiguratsiyasi tayyor. Lokal admin ma’lumotlari
.env faylida saqlanadi va Git tomonidan kuzatilmaydi.

~~~bash
docker compose up -d --build
~~~

Holatni tekshirish:

~~~bash
docker compose ps
docker compose logs --tail=100 portal
~~~

To‘xtatish:

~~~bash
docker compose down
~~~

Kontent va murojaatlar agrosanoat-portal-data nomli Docker volume ichida
saqlanadi. Oddiy docker compose down volume ma’lumotlarini o‘chirmaydi.
Volumeni o‘chirish uchun -v parametrini faqat zaxira nusxa olingandan keyin
ishlating.

## Ma’lumotlar

- data/content.json — rahbariyat, hududlar va yangiliklar.
- data/contacts.json — elektron murojaatlar.
- Yozish jarayoni vaqtinchalik fayl va atomik almashtirish orqali bajariladi.
- Admin kiritmalari serverda uzunlik va format bo‘yicha tekshiriladi.
- Yangilik matni HTML sifatida bajarilmaydi; frontend uni oddiy matn sifatida chiqaradi.

Muhim: data/contacts.json shaxsiy ma’lumot saqlashi mumkin. Production
serverda faylga kirish huquqlarini cheklang va zaxira nusxalash siyosatini
belgilang. HTTP server data/ katalogini internet orqali bermaydi.

## Production sozlamalari

Reverse proxy orqali HTTPS ishlatilganda:

~~~bash
HOST='127.0.0.1' PORT='8000' COOKIE_SECURE='1' \
ADMIN_USERNAME='portal-admin' ADMIN_PASSWORD='...' python3 server.py
~~~

Nginx yoki boshqa reverse proxy quyidagilarni ta’minlashi kerak:

- HTTPS sertifikati;
- so‘rov hajmi va timeout limitlari;
- process supervision (systemd, Docker yoki platforma servisi);
- data/ katalogining muntazam zaxira nusxasi.

Admin sessiyalari server xotirasida 8 soat saqlanadi va server qayta ishga
tushganda avtomatik bekor bo‘ladi.

## Testlar

~~~bash
PYTHONPYCACHEPREFIX=/tmp/agro-pycache python3 -m unittest discover -s tests -v
~~~

Health-check:

~~~bash
curl http://127.0.0.1:8000/health
~~~
