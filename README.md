# 🎙️ EBS AI Vocal Separator

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-1F6AA5)](https://github.com/TomSchimansky/CustomTkinter)
[![PyTorch](https://img.shields.io/badge/AI-PyTorch-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Demucs](https://img.shields.io/badge/Audio-Demucs-6A5ACD)](https://github.com/facebookresearch/demucs)
[![License](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](LICENSE)

**EBS AI Vocal Separator**, Python tabanlı yapay zekâ destekli ses kaynağı ayırma projesidir. Projenin bağımlılık listesinde yer alan **Demucs** ve **PyTorch**, ses içeriğini vokal ve enstrümantal bileşenlere ayırmak için kullanılan AI altyapısını sağlar. **CustomTkinter** masaüstü arayüzü, **NumPy** ve **SoundFile** ise sayısal ve ses verisi işlemleri için kullanılan bileşenlerdir.

> Bu depo için README ve bağımlılık dosyası incelenmiştir. Kaynak kod dosyalarının içeriği bu incelemede doğrulanamadığından, aşağıdaki açıklamalar yalnızca doğrulanabilen teknoloji ve proje kapsamıyla sınırlıdır; doğrulanmamış düğme adları, çıktı klasörleri veya komut satırı seçenekleri özellikle belirtilmemiştir.

## ✨ Proje kapsamı

- Demucs tabanlı yapay zekâ ile vokal/ses kaynağı ayırma altyapısı.
- PyTorch ile model çalıştırma.
- CustomTkinter ile masaüstü arayüzü oluşturmak için gerekli bağımlılık.
- NumPy ile sayısal veri işlemleri.
- SoundFile ile ses dosyası okuma/yazma desteği.
- Python ortamında yerel çalıştırmaya yönelik bağımlılık tanımları.

## 🧰 Teknoloji kartları

| Teknoloji | Kullanım amacı |
|---|---|
| Python | Uygulama geliştirme dili |
| CustomTkinter | Masaüstü GUI bileşenleri |
| PyTorch | Derin öğrenme çalışma altyapısı |
| Demucs | Müzik/ses kaynaklarını ayıran AI modeli |
| NumPy | Sayısal dizi ve veri işlemleri |
| SoundFile | Ses dosyası I/O işlemleri |

## 📁 Depo yapısı

Depoda bu dokümantasyon ve bağımlılık dosyası doğrulanmıştır:

```text
EBS-AI-Vocal-Separator/
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

Uygulama kaynak dosyaları bu README incelemesinde listelenemediği için kaynak dosya isimleri tahmin edilerek proje ağacına eklenmemiştir.

## 🚀 Kurulum

### 1. Depoyu klonlayın

```bash
git clone https://github.com/ebubekirbastama/EBS-AI-Vocal-Separator.git
cd EBS-AI-Vocal-Separator
```

### 2. Sanal ortam oluşturun

Windows:

```powershell
py -m venv .venv
.venv\Scripts\activate
```

Linux / macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Bağımlılıkları yükleyin

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> **PyTorch notu:** Kurulum, sisteminizin işletim sistemi ve CPU/GPU yapılandırmasına uygun PyTorch paketini gerektirebilir. CUDA kullanacaksanız PyTorch'un resmi kurulum seçicisinden uyumlu komutu belirleyin: https://pytorch.org/get-started/locally/

## ▶️ Kullanım

1. Sanal ortamı etkinleştirin.
2. Bağımlılıkların sorunsuz kurulduğunu doğrulayın.
3. Depodaki Python uygulama giriş dosyasını çalıştırın.
4. Uygulama arayüzünde işlemek istediğiniz ses kaynağını seçin ve ayırma işlemini başlatın.
5. İşlem tamamlandığında uygulamanın belirttiği çıktı konumunu kontrol edin.

**Çalıştırma komutu:** Depodaki gerçek giriş dosyası adı kaynak dosyalar bu incelemede doğrulanamadığı için burada sabit bir komut verilmemiştir. Kök dizindeki uygulama dosyasının adıyla `python dosya_adi.py` biçiminde çalıştırılmalıdır.

## 🔍 Çalışma akışı

Genel Demucs tabanlı kaynak ayırma süreci:

1. Ses kaynağı uygulamaya alınır.
2. Ses verisi modelin beklediği biçime hazırlanır.
3. Demucs modeli PyTorch altyapısıyla çıkarım (inference) işlemini gerçekleştirir.
4. Model, vokal ve eşlik/enstrümantal gibi ses bileşenlerini ayırır.
5. Ayrıştırılmış ses bileşenleri ses dosyası olarak dışa aktarılır.

Bu akış, kullanılan Demucs modelinin genel çalışma prensibini açıklar; uygulamanın kaynak kodundaki özel işlem adımları ayrıca doğrulanmalıdır.

## ⚠️ Teknik sınırlamalar ve dikkat edilmesi gerekenler

- **İşlem süresi:** Ses uzunluğu, model seçimi, CPU/GPU ve RAM kapasitesine göre değişir.
- **GPU uyumluluğu:** CUDA hızlandırması için PyTorch, NVIDIA sürücüsü ve CUDA sürümlerinin birbiriyle uyumlu olması gerekir.
- **Bellek ihtiyacı:** Uzun veya yüksek örnekleme oranlı ses dosyaları daha fazla RAM/VRAM tüketebilir.
- **Model kalitesi:** Kaynak ayırma sonuçları her kayıtta kusursuz olmayabilir; yoğun efekt, yankı ve üst üste binmiş frekanslar artefakt oluşturabilir.
- **Bağımlılık uyumluluğu:** PyTorch ve Demucs sürümlerinin Python sürümü ve işletim sistemiyle uyumlu olması gerekir.
- **Giriş/çıkış formatları:** Kesin desteklenen formatlar ve çıktı biçimleri uygulamanın gerçek ses okuma/yazma koduna bağlıdır; yalnızca bağımlılık listesinden kesin format garantisi verilemez.

## 🔐 Güvenli ve sorumlu kullanım

- Yalnızca kullanım veya işleme hakkına sahip olduğunuz ses dosyalarını kullanın.
- Telif hakkıyla korunan içerikleri izinsiz çoğaltmayın veya dağıtmayın.
- Bilinmeyen kaynaklardan gelen ses dosyalarını işlerken güncel güvenlik yazılımı kullanın.
- Model ve Python paketlerini mümkün olduğunca resmi kaynaklardan yükleyin.
- Özel veya hassas kayıtları paylaşmadan önce yerel dosya ve yedekleme güvenliğini kontrol edin.

## 🛠️ Geliştirme ve modernizasyon önerileri

- Python giriş noktası ve uygulama modülleri README'de açıkça listelenmeli.
- `requirements.txt` için test edilmiş sürüm aralıkları veya kilit dosyası eklenmeli.
- Dosya türü, süre ve boyut kontrolleri ile anlaşılır hata mesajları sağlanmalı.
- Uzun süren model işlemleri arayüzü kilitlemeyecek şekilde arka plan iş parçacığına/iş kuyruğuna taşınmalı.
- İşlem ilerlemesi, iptal ve çıktı klasörünü açma özellikleri eklenebilir.
- CPU/CUDA otomatik cihaz seçimi ve seçili cihaz bilgisinin arayüzde gösterilmesi faydalı olur.
- Birim testleri ve küçük örnek ses dosyalarıyla tekrarlanabilir test akışı eklenebilir.
- Uygulama sürümü, model adı ve işlem parametreleri dışa aktarılan sonuçlarla birlikte kaydedilebilir.

## 📄 Lisans

Bu proje **Apache License 2.0** lisansı altında sunulmaktadır. Ayrıntılar için [LICENSE](LICENSE) dosyasına bakın.

## 👨‍💻 Geliştirici

**Ebubekir Bastama**

- GitHub: [@ebubekirbastama](https://github.com/ebubekirbastama)
- Proje: [EBS-AI-Vocal-Separator](https://github.com/ebubekirbastama/EBS-AI-Vocal-Separator)

---

<p align="center">EBS AI Vocal Separator · Python & AI Audio Processing</p>
