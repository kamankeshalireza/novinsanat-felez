# راهنمای دیپلوی پروژه روی لیارا (Liara)

این پروژه (Django 5.2) برای دیپلوی روی پلتفرم **Django لیارا** آماده‌سازی شده است. تغییرات زیر روی پروژه اعمال شده‌اند:

## فایل‌ها و تغییرات اعمال‌شده

| فایل | تغییر |
|---|---|
| `core/core/settings.py` | بازنویسی کامل: تمام مقادیر حساس (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, دیتابیس) از متغیرهای محیطی خوانده می‌شوند؛ هدرهای امنیتی HTTP، HSTS، کوکی‌های امن، WhiteNoise برای static، پشتیبانی از PostgreSQL و لاگ‌گیری روی stdout اضافه شد. |
| `core/core/urls.py` | سرو کردن مدیا (فایل‌های آپلودی) در محیط پروداکشن هم فعال شد (WhiteNoise فقط static را پوشش می‌دهد). |
| `requirements.txt` | `whitenoise`, `gunicorn`, `psycopg2-binary` اضافه شد؛ کتابخانه‌های تستی (`factory_boy`, `Faker`) به `requirements-dev.txt` منتقل شدند تا محیط پروداکشن سبک‌تر و امن‌تر بماند. |
| `liara.json` | فایل پیکربندی لیارا؛ پلتفرم `django`، پایتون `3.12`، و `modifySettings: false` (چون خودمان تنظیمات امنیتی را کامل پیاده کرده‌ایم و نمی‌خواهیم لیارا چیزی به `settings.py` اضافه کند). |
| `.env.sample` | لیست کامل متغیرهای محیطی مورد نیاز، برای راهنمایی هنگام تنظیم در پنل لیارا. |
| `.gitignore` / `.liaraignore` | جلوگیری از آپلود فایل‌های غیرضروری (venv، `__pycache__`، `db.sqlite3`، `.env`, و غیره). |

> **نکته:** فولدر `core/media` در پروژه فعلی وجود دارد ولی طبق گفتهٔ شما تصاویر از آن حذف شده‌اند. کافی است بعد از اعمال این تغییرات، تصاویر را داخل `core/media` و `core/static` قرار دهید و مجدداً پروژه را فشرده (zip) و آپلود/push کنید.

---

## مرحله ۱: ساخت برنامه در لیارا

۱. وارد [پنل لیارا](https://console.liara.ir) شوید.
۲. از منوی **پلتفرم**، گزینه **ایجاد برنامه** را بزنید.
۳. پلتفرم را روی **Django** تنظیم کنید.
۴. یک **شناسه یکتا** برای برنامه انتخاب کنید (مثلاً `novinsanat-felez`) — همین مقدار را در فیلد `app` داخل `liara.json` هم قرار دهید.
۵. منابع سخت‌افزاری (RAM/CPU) مناسب را انتخاب و برنامه را بسازید.

## مرحله ۲: ساخت دیتابیس PostgreSQL

برای امنیت و پایداری بیشتر (به‌خصوص چون فضای دیسک لیارا در هر ری‌دیپلوی پاک می‌شود)، **از SQLite در پروداکشن استفاده نکنید**.

۱. از منوی **دیتابیس‌ها**، یک دیتابیس **PostgreSQL** بسازید.
۲. آن را به برنامه‌ی خود متصل کنید — لیارا به‌صورت خودکار متغیرهای زیر را به برنامه اضافه می‌کند:
   - `POSTGRESQL_DB_HOST`
   - `POSTGRESQL_DB_PORT`
   - `POSTGRESQL_DB_USER`
   - `POSTGRESQL_DB_PASS`
   - `POSTGRESQL_DB_NAME`

فایل `settings.py` به‌صورت خودکار این متغیرها را تشخیص داده و از PostgreSQL استفاده می‌کند (در نبود آن‌ها، به SQLite برای تست محلی برمی‌گردد).

## مرحله ۳: تنظیم متغیرهای محیطی

در پنل برنامه، وارد بخش **Environment Variables** شوید و مقادیر زیر را اضافه کنید (فایل `.env.sample` را هم ببینید):

```
SECRET_KEY=<یک مقدار طولانی و تصادفی>
DEBUG=false
ALLOWED_HOSTS=<app-id>.liara.run
CSRF_TRUSTED_ORIGINS=https://<app-id>.liara.run
DJANGO_TIME_ZONE=Asia/Tehran
```

برای ساخت `SECRET_KEY` امن، این دستور را روی سیستم خودتان اجرا کنید:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

⚠️ **هرگز `SECRET_KEY` قدیمی پروژه (`django-insecure-...`) را استفاده نکنید** — این مقدار قبلاً در کد عمومی بوده و از نظر امنیتی سوخته محسوب می‌شود.

اگر دامنه‌ی اختصاصی هم متصل کردید، آن را هم به `ALLOWED_HOSTS` و `CSRF_TRUSTED_ORIGINS` (با `https://`) اضافه کنید.

## مرحله ۴: آپلود پروژه

**روش CLI (پیشنهادی):**

```bash
npm install -g @liara/cli
liara login
cd novinsanat-felez-main
liara deploy
```

**روش Drag & Drop:** پوشه پروژه (شامل `liara.json`, `requirements.txt`, `core/`) را zip کرده و از پنل، در بخش «استقرار جدید» آپلود کنید.

**روش GitHub:** ریپازیتوری را به گیت‌هاب پوش کنید، سپس در پنل لیارا، برنامه را به همان ریپازیتوری و برنچ متصل کنید تا با هر push، دیپلوی خودکار انجام شود.

در هر سه حالت، لیارا به‌صورت خودکار:
- `pip install -r requirements.txt` را اجرا می‌کند،
- `python manage.py collectstatic` را اجرا می‌کند (چون `collectStatic: true`),
- برنامه را با **Gunicorn** پشت **nginx** اجرا می‌کند.

## مرحله ۵: اجرای Migration

بعد از اولین دیپلوی موفق، وارد بخش **Console / Shell** برنامه در پنل لیارا شوید و دستور زیر را اجرا کنید:

```bash
python manage.py migrate
```

سپس برای ساخت کاربر ادمین:

```bash
python manage.py createsuperuser
```

## مرحله ۶: افزودن مجدد تصاویر

بعد از این‌که مطمئن شدید دیپلوی و اتصال دیتابیس درست کار می‌کند:

1. تصاویر را داخل `core/static/` (برای asset های ثابت سایت) و/یا `core/media/` (برای تصاویر آپلودی مثل `featured_image` پست‌های بلاگ) قرار دهید.
2. پروژه را دوباره zip/push و دیپلوی کنید — `collectstatic` به‌صورت خودکار اجرا می‌شود.
3. اگر حجم تصاویر مدیا (media) زیاد است و می‌خواهید بین دیپلوی‌ها از بین نروند، از قابلیت **Disk** لیارا برای mount کردن یک دیسک پایدار روی مسیر `core/media` استفاده کنید (از پنل برنامه > Disks)، یا از **Liara Object Storage** (سازگار با S3) استفاده کنید.

---

## چک‌لیست امنیتی که در این پروژه اعمال شده

- ✅ `SECRET_KEY` و تمام مقادیر حساس از متغیر محیطی خوانده می‌شوند (هیچ‌چیز در کد hardcode نیست)
- ✅ `DEBUG` پیش‌فرض `False` است (فقط با تنظیم صریح env var فعال می‌شود)
- ✅ `ALLOWED_HOSTS` و `CSRF_TRUSTED_ORIGINS` از env خوانده می‌شوند (نه `*`)
- ✅ HTTPS اجباری (`SECURE_SSL_REDIRECT`) در پروداکشن
- ✅ HSTS با `includeSubDomains` و `preload` فعال است
- ✅ کوکی‌های Session و CSRF با `Secure`, `HttpOnly`, `SameSite=Lax`
- ✅ `X-Frame-Options: DENY`، `X-Content-Type-Options: nosniff`، `Referrer-Policy: same-origin`
- ✅ محدودیت حجم آپلود فایل (۵ مگابایت) برای جلوگیری از حملات DoS
- ✅ اعتبارسنجی رمز عبور با حداقل طول ۱۰ کاراکتر
- ✅ فایل‌های استاتیک با WhiteNoise، فشرده و hash‑شده سرو می‌شوند
- ✅ لاگ‌ها روی stdout (قابل مشاهده در پنل لیارا) هستند
- ✅ کتابخانه‌های تستی از dependency های پروداکشن حذف شدند

پس از دیپلوی، پیشنهاد می‌شود دستور زیر را هم روی سرور اجرا کنید تا از نبود مشکل امنیتی دیگری مطمئن شوید:

```bash
python manage.py check --deploy
```

## منابع رسمی لیارا

- [استقرار برنامه Django](https://docs.liara.ir/paas/django/quick-start/)
- [اتصال به PostgreSQL](https://docs.liara.ir/paas/django/how-tos/connect-to-db/postgresql/)
- [تنظیم متغیرهای محیطی](https://docs.liara.ir/paas/django/how-tos/set-envs/)
- [استفاده از دیسک](https://docs.liara.ir/paas/django/how-tos/use-disk/)
