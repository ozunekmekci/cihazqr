# CihazQR

CihazQR, hastane cihaz envanterini QR kod ile dijital ve merkezi olarak yönetmek için geliştirilmiş modern bir web uygulamasıdır. Kullanıcı dostu arayüzü, güçlü arama ve filtreleme özellikleri ile cihaz, arıza ve bakım süreçlerini kolayca yönetmenizi sağlar.

## Özellikler
- Cihaz envanteri yönetimi (QR kod ile)
- Cihazlara not ve belge ekleme
- Arıza kaydı oluşturma, güncelleme ve geçmişi görüntüleme
- Modern, responsive ve sade dashboard
- Yetkilendirme ve audit log (geliştirilebilir)
- Toplu QR kod üretimi ve çıktı alma (geliştirilebilir)

## Teknolojiler
- **Frontend:** Next.js (App Router), Tailwind CSS, Shadcn UI, Framer Motion, Lucide Icons
- **Backend:** Django + Django REST Framework
- **Veritabanı:** SQLite (demo/dev), MySQL (prod için hazır)
- **Dosya Depolama:** Lokal (media/)

## Kurulum
### 1. Backend (Django)
```bash
cd cihazqr-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Frontend (Next.js)
```bash
cd next-js-boilerplate
npm install
npm run dev
```

## Kullanım
- Sol menüden cihaz, arıza, rapor ve ayar ekranlarına erişebilirsiniz.
- Cihaz ekleyin, QR kodunu alın ve cihazın üzerine yapıştırın.
- Arıza kaydı oluşturun, geçmişi ve detayları görüntüleyin.
- Tüm işlemler sade ve modern bir arayüzde gerçekleşir.

## Ekran Görüntüleri
> Ekran görüntüleri ve demo GIF'leri buraya ekleyebilirsiniz.

## Katkı ve Geliştirme
- Kod okunabilirliği ve sürdürülebilirliği ön planda tutulmuştur.
- PR ve issue açarak katkıda bulunabilirsiniz.

## Lisans
MIT 