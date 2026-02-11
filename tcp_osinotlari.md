# Ağ İletişim Modelleri : OSI ve TCP/IP

Bu doküman, ağ iletişiminin temel taşları olan OSI Referans modeli ve TCP/IP Protokol kümesi hakkında aldığım notları ve teknik detayları içermektedir.

## 1. OSI (Open Systems Interconnection) Modeli 

OSI modeli, farklı donanım ve yazılımların birbiriyle nasıl iletişim kuracağını belirleyen 7 katmanlı bir standarttır.

### Katmanlar ve Görevleri 

| # | Katman Adı | Veri Birimi(PDU) | Görev ve Açıklama | Örnek Protokol/Cihaz |
| :--- | :--- | :--- | :--- | :---|
| **7** | **Application** (Uygulama) | Data | Kullanıcı arayüzü ve ağ servisleri. | HTTP,FTP,SMTP,DNS |
| **6** | **Presentation** (Sunum) | Data | Veri formatlama, şifreleme ve sıkıştırma. | SSl/TLS, JPEG ,ASCII |
| **5** | **Session** (Oturum) | Data | Bağlantıları başlatma, yönetme ve sonlandırma. | NetBıos,RPC |
| **4** | **Transport** (Taşıma) | Segment | Veri iletimi , hata kontrolü ve akış denetimi. | **TCP** , **UDP**|
| **3** | **Network** (Ağ) | Packet | Mantıksal adresleme (IP) ve yönlendirme(Routing). | **IP**, ICMP , Router |
| **2** | **Data Link** (Veri Bağlantısı) | Frame | Fiziksel adresleme (MAC) ve hata tespiti | Ethernet , Switch , Mac |
| **1** | **Physical** | Bit | Bitlerin fiziksel ortamda taşınması. | Kablolar ,Hub ,Fiber |
 

> **Unutma:** Veri Göderilirken 7'den 1'e (Encapsulation),alınırken 1'den 7'ye(Decapsulation) ilerler.

---


## 2. TCP/IP Modeli

İntenetin temelini oluşturan, OSI ' nin daha pratik ve uygulanabilir halidir. 4 katmandan oluşur.

### OSI ile karşılaştırılması 

| TCP/IP Katmanı | Karşılık gelen OSI katmanları | Açıklama |
| :--- | :--- | :--- |
| **Application** | Application , Presentation ,Session | Tüm üst düzey protokoller burada çalışır (HTTP,SSH vb.) |
| **Transport** | Transport | Uçtan uca iletşim ve güvenilirlik sağlar.(TCP/UDP) |
| **Internet** | Network | Paketlerin hedefe yönlendirilmesini sağlar (IP,ARP) |
| **Network Access** | Data Link, Physical | Fiziksel donanım ve Mac adresleme katmanıdır. |


---

## 3. Önemli Protokoller ve Kavramlar 

### TCP vs UDP Farkı 

* **TCP (Transmission Control Protocol):**
	* **Bağlantı Temelli (Connection-oriented):** "3-Way Handshake" (SYN,SYN-ACK,ACK)ile bağlantı kurar.
	* **Güvenilir:** Verinin ulaştığını teyit eder(ACK).
	* **Kullanım:** Web siteleri ,Eposta, Dosya İndirme.

* **UDP(User Datagram Protocol):**
	* **Bağlantısız(Connectionless):** Selamlaşma yapmaz,veriyi doğrudan gönderir.
	* **Hızlı ama Güvensiz:** Paket kaybı olabilir,kontrol etmez.
	* **Kullanım:** Online oyunlar, Canlı yayınlar ,DNS sorguları.


### Adresleme Türleri


1.  **MAC Adresi (Fiziksel):** Cihazın üretiminde karta kazınan benzersiz kimliktir. (Örn: `(Örn: `00:1A:2B:3C:4D:5E`) - *Data Link Katmanı*
2.  **IP Adresi (Mantıksal):** Ağdaki konumunu belirten, değişebilen adrestir. (Örn: `192.168.1.1`) - *Network Katmanı*
3.  **Port Numarası:** Hangi uygulamanın veriyi alacağını belirler.  (Örn: `80` web için, `22` SSH için) - *Transport Katmanı*


## 3. Teknik Detaylar 

Standart teorinin ötesinde, TCP/IP protokolünün çalışma mekaniği , durum makinesi (state machine) ve paket analizi detayları.

### A. TCP Header(Başlık) ve Bayraklar (Flags)

TCP bir durum makinesi gibi çalışır. İletişiminin hangi aşamada olduğunu belirlemek için bayrak bitlerini kullanır.

| Bayrak | Tam Adı | Anlamı ve Görevi |
| :--- | :--- | :---|
| **SYN** | Synchronize | Bağlantıyı başlatmak için ilk gönderilen pakettir |
| **ACK** | Acknowledgement | verinin ulaştığını teyit eder.|
| **FIN** | Finish | "bağlantıyı sonlandırır"|
| **RST** | Reset | "hata durumunda port kapalıysa döner" |
| **PSH** | Push | "Veriyi tampona almadan doğrudan uygulamaya ilet.|
| **URG** | Urgent | " Öncelikli veri taşındığını belirtir." |

### B. TCP 3-Way Handshake (Üçlü El Sıkışma)

Güvenilir bir bağlantının (Session) kurulma sürecidir.

1.  **SYN:** İstemci (Client) sunucuya bir `SYN` paketi atar ve rastgele bir Sequence Number (SEQ=X) belirler. *(Durum: SYN-SENT)*
2.  **SYN-ACK:** Sunucu bunu alır, X+1'i onaylar (`ACK`) ve kendi `SYN` paketini (SEQ=Y) ekleyerek geri döner. *(Durum: SYN-RECEIVED)*
3.  **ACK:** İstemci, sunucunun Y+1 numarasını onaylar (`ACK`) ve bağlantı kurulur. *(Durum: ESTABLISHED)*

> **Güvenlik Notu:** Sunucu SYN alıp SYN-ACK dönmesine rağmen istemci son ACK'yı göndermezse, sunucu kaynakları tükenir. Buna **SYN Flood (DDoS)** saldırısı denir.

### C. Akış Kontrolü (Flow Control & Windowing)

TCP, alıcı tarafın kapasitesine göre hızı ayarlar.
* **Window Size:** Alıcının göndericiye "Şu an X byte kadar boş yerim (buffer) var, daha fazlasını gönderme" dediği limittir.
* Eğer alıcı yavaşlarsa Window Size'ı düşürür, gönderici de yavaşlar. UDP'de bu mekanizma yoktur, bu yüzden paket kaybı yaşanır.

---

## 4. Veri Kapsülleme (Encapsulation) Süreci

Verinin bir uygulamadan çıkıp kabloya gidene kadar geçirdiği "Matruşka Bebek" dönüşümü.

1.  **L7 (Application):** HTTP isteği oluşturulur (`GET /index.html`).
2.  **L4 (Transport):** Veriye **TCP Başlığı** eklenir. (Kaynak Port, Hedef Port: 80).
3.  **L3 (Network):** Pakete **IP Başlığı** eklenir. (Kaynak IP, Hedef IP, TTL).
4.  **L2 (Data Link):** Pakete **Ethernet Başlığı** ve **MAC Adresleri** eklenir.
5.  **L1 (Physical):** Tüm yapı 0 ve 1 (bit) sinyallerine dönüştürülür.

> **Kritik Ayrım:**
> * **Switch (L2):** Sadece MAC adresine bakar, IP başlığını okumaz.
> * **Router (L3):** IP adresine bakar, paketi yönlendirir.

---

## 5. Linux Ağ Analizi (Practical Debugging)

Mühendislik çalışmalarında kullanılacak temel terminal komutları:

**TCP Bağlantılarını Listeleme (`ss` veya `netstat`):**

```bash
# Tüm TCP portlarını (dinleyenler dahil) sayısal olarak göster
ss -tuna
# -t: TCP, -u: UDP, -n: Numeric (DNS çözme), -a: All
```  


---

## 6. HTTP Protokolü (Web'in Dili)

OSI 7. Katmanda çalışan, istemci (client) ve sunucu (server) arasındaki veri alışverişini sağlayan protokoldür.

### Temel Özellikler
* **Stateless (Durumsuz):** Sunucu önceki istekleri hatırlamaz. Oturum yönetimi için Cookie veya Token kullanılır.
* **Portlar:** Standart HTTP **80**, güvenli olan HTTPS **443** portunu kullanır.

### En Sık Kullanılan Metotlar (Verbs)

| Metot | Görev | Örnek Senaryo |
| :--- | :--- | :--- |
| **GET** | Veri İster | Sayfa görüntüleme, arama yapma. |
| **POST** | Veri Gönderir | Üye olma, form gönderme. |
| **PUT** | Günceller | Profil bilgilerini değiştirme (Tümünü). |
| **PATCH** | Kısmi Günceller | Sadece şifreyi değiştirme. |
| **DELETE** | Siler | Hesabı silme. |

### HTTP Durum Kodları (Status Codes)

Bir API isteği attığınızda dönen cevabın anlamı:

* **200 OK:** Başarılı.
* **400 Bad Request:** İstek hatalı (Eksik parametre vs.).
* **401 Unauthorized:** Kimlik doğrulama başarısız (Giriş yapılmamış).
* **403 Forbidden:** Yetki yok (Giriş var ama admin değilsin).
* **404 Not Found:** Sayfa veya kaynak bulunamadı.
* **500 Internal Server Error:** Sunucu hatası (Backend kodunda sorun var).

### HTTP vs HTTPS
HTTPS, HTTP'nin **SSL/TLS** sertifikası ile şifrelenmiş halidir. HTTP'de veriler açık giderken, HTTPS'de veriler şifreli tünelden geçer.
