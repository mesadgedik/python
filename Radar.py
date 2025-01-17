import serial
import matplotlib.pyplot as plt
import numpy as np

# Seri port ayarları
SERIAL_PORT = "COM5"  # Arduino'nun bağlı olduğu portu buraya yazın
BAUD_RATE = 9600
MAX_DISTANCE = 75  # Maksimum ölçüm mesafesi (cm)

def update_radar(ax, angles, distances):
    """
    Radar grafiğini günceller.
    ax: Radar ekseni.
    angles: Açılar (radyan cinsinden).
    distances: Mesafeler.
    """
    ax.clear()  # Grafiği temizle
    ax.set_theta_zero_location("N")  # Kuzey 0 derece
    ax.set_theta_direction(-1)       # Saat yönünün tersine hareket
    ax.set_ylim(0, MAX_DISTANCE)

    # Verileri çiz
    ax.plot(angles, distances, marker='o', label="Ölçüm")
    ax.fill_between(angles, distances, MAX_DISTANCE, color='gray', alpha=0.2, label="Maksimum Mesafe")
    ax.legend(loc="upper right")
    ax.set_title("Radar Taraması", va='bottom')

def read_serial_data():
    """
    Arduino'dan gelen veriyi okuyarak anlık radar grafiği çizer.
    """
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
        angles = []
        distances = []
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})  # Radar grafiği için polar eksen

        while True:
            try:
                line = ser.readline().decode('utf-8').strip()  # Satırı oku ve temizle
                if line:
                    print(f"Gelen veri: {line}")
                    angle, distance = map(int, line.split(','))  # Açıyı ve mesafeyi ayır
                    if distance > MAX_DISTANCE:  # Maksimum mesafeden büyük değerleri 0 kabul et
                        distance = 0

                    # Verileri güncelle
                    if angle == 0:  # Yeni tur başladığında grafiği sıfırla
                        angles.clear()
                        distances.clear()

                    angles.append(np.deg2rad(angle))  # Açıyı radyan cinsine çevir
                    distances.append(distance)

                    # Grafiği güncelle
                    update_radar(ax, angles, distances)
                    plt.pause(0.01)  # Küçük bir gecikme ile güncelleme yap

            except KeyboardInterrupt:
                print("Program sonlandırıldı.")
                break
            except Exception as e:
                print(f"Hata: {e}")

# Programı çalıştır
read_serial_data()
