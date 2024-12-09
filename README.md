OT Projekt  

 

Opis: 
Projekt IoT ma na celu monitorowanie temperatury za pomocą modułu ESP8266 wyposażonego w czujnik DS18B20. Odczyty temperatury są wyświetlane w terminalu Arduino oraz na wyświetlaczu LCD. Dane temperatury są wysyłane do zdalnego brokera MQTT z zastosowaniem autoryzacji oraz szyfrowania. Aplikacja Python subscriber subskrybuje te dane, zapisuje je do bazy danych InfluxDB, a wizualizację danych zapewnia Grafana. Dodatkowo, projekt zawiera funkcje zamiany mowy na tekst (speech-to-text) oraz detekcji obiektów na obrazie (video-to-text) przy użyciu modeli Whisper i YOLO, które również wysyłają dane przez MQTT do brokera. Cały system jest uruchamiany za pomocą Docker, co umożliwia łatwe zarządzanie kontenerami. 
 
Autorzy: 

Wojciech Biziuk, Mateusz Karolewski 

 

Wymagania sprzętowe: 

Sprzęt: komputer x2, moduł ESP8266, Czujnik temperatury DS18B20, Wyświetlacz LCD 

Oprogramowanie: Arduino IDE, Docker, Python 3.x, InfluxDB, Grafana 

 

Opis Komponentów: 

ESP8266 + Subscriber 
 
MQTT configuration 

MQTT_BROKER = 'broker.emqx.io' # Replace with your broker's address MQTT_PORT = 1883 MQTT_TOPIC = 'emqx/esp8266_laby'  

InfluxDB configuration 

token = "JvNlsVx9-TNoat_Op6d0GeiQZezk7DnAWhYQj7AdB9sSv65ypZtQYd3qDxbT3aytzTEfxWFLPxjVz71bn4uSNw==" org = "IOT" url = "http://localhost:8086/" bucket = "new" # Replace with the name of your InfluxDB bucket write_client = InfluxDBClient(url=url, token=token, org=org) write_api = write_client.write_api(write_options=SYNCHRONOUS)  

Define the MQTT client callbacks 

def on_connect(client, userdata, flags, rc): print("Connected with result code " + str(rc)) client.subscribe(MQTT_TOPIC) def on_message(client, userdata, msg): try: temperature = float(msg.payload.decode()) print(f"Received temperature: {temperature}") # Create a data point and write it to InfluxDB point = ( Point("measurement1") .tag("tagname1", "tagvalue1") .field("field1", temperature) ) write_api.write(bucket=bucket, org=org, record=point) print("Data written to InfluxDB.") except ValueError as e: print("Failed to decode or write data:", e)  

Initialize and run the MQTT client 

client_mqtt = mqtt.Client() client_mqtt.on_connect = on_connect client_mqtt.on_message = on_message client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60) client_mqtt.loop_forever() 

 
 
 
Speech to text: 

logging.basicConfig(level=logging.DEBUG) print("Starting application...") print("MQTT polaczenie")  

MQTT configuration 

MQTTBROKER = 'broker.emqx.io' MQTTPORT = 1883 MQTTTOPIC = 'emqx/esp8266laby' def on_connect(client, userdata, flags, rc): print("Connected with result code " + str(rc)) client.subscribe(MQTT_TOPIC)  

Inicjalizacja modelu Whisper 

print("Loading Whisper model...") whisper_asr = pipeline("automatic-speech-recognition", model="openai/whisper-small") def record_audio(duration=5, samplerate=16000): """ Rejestracja dźwięku z mikrofonu. """ print(f"Recording audio for {duration} seconds...") audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.float32) sd.wait() # Oczekiwanie na zakończenie nagrywania print("Recording complete.") return audio.flatten() def transcribe_audio(audio): """ Zamiana dźwięku na tekst przy użyciu modelu Whisper. """ print("Transcribing audio...") result = whisper_asr(audio) # Usunięto sampling_rate return result["text"] if __name == "__main": try: duration = 5 # Czas nagrywania w sekundach samplerate = 16000 # Częstotliwość próbkowania audio_data = record_audio(duration=duration, samplerate=samplerate) transcription = transcribe_audio(audio_data) client = mqtt.Client() client.connect(MQTT_BROKER,1883,60) client.publish(MQTT_TOPIC, transcription); client.disconnect(); print(f"Transcribed text: {transcription}") except Exception as e: print(f"An error occurred: {e}") finally: print("Press Ctrl+C to exit...") while True: time.sleep(1) client_mqtt = mqtt.Client() client_mqtt.on_connect = on_connect 
 


 def on_connect(client, userdata, flags, rc): print("Connected with result code " + str(rc)) 
client.subscribe(MQTT_TOPIC) def on_message(client, userdata, msg): try: temperature = 
float(msg.payload.decode()) print(f"Received temperature: {temperature}") # Create a data 
point and write it to InfluxDB point = ( Point("measurement1") .tag("tagname1", "tagvalue1") 
.field("field1", temperature) ) write_api.write(bucket=bucket, org=org, record=point) print("Data 
written to InfluxDB.") except ValueError as e: print("Failed to decode or write data:", e) 
Initialize and run the MQTT client
client_mqtt = mqtt.Client() client_mqtt.on_connect = on_connect client_mqtt.on_message = 
on_message client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60) client_mqtt.loop_forever()
Speech to text:
logging.basicConfig(level=logging.DEBUG) print("Starting application...") print("MQTT 
polaczenie") 
MQTT configuration
MQTTBROKER = 'broker.emqx.io' MQTTPORT = 1883 MQTTTOPIC = 'emqx/esp8266laby' def 
on_connect(client, userdata, flags, rc): print("Connected with result code " + str(rc)) 
client.subscribe(MQTT_TOPIC) 
Inicjalizacja modelu Whisper
print("Loading Whisper model...") whisper_asr = pipeline("automatic-speech-recognition", 
model="openai/whisper-small") def record_audio(duration=5, samplerate=16000): """ 
Rejestracja dźwięku z mikrofonu. """ print(f"Recording audio for {duration} seconds...") audio = 
sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype=np.float32) 
sd.wait() # Oczekiwanie na zakończenie nagrywania print("Recording complete.") return 
audio.flatten() def transcribe_audio(audio): """ Zamiana dźwięku na tekst przy użyciu modelu 
Whisper. """ print("Transcribing audio...") result = whisper_asr(audio) # Usunięto sampling_rate 
return result["text"] if __name == "__main": try: duration = 5 # Czas nagrywania w sekundach 
samplerate = 16000 # Częstotliwość próbkowania audio_data = 
record_audio(duration=duration, samplerate=samplerate) transcription = 
transcribe_audio(audio_data) client = mqtt.Client() client.connect(MQTT_BROKER,1883,60) 
client.publish(MQTT_TOPIC, transcription); client.disconnect(); print(f"Transcribed text: 
{transcription}") except Exception as e: print(f"An error occurred: {e}") finally: print("Press Ctrl+C 
to exit...") while True: time.sleep(1) client_mqtt = mqtt.Client() client_mqtt.on_connect = 
on_connect
 
Video to text: 




client = mqtt.Client() client.connect(MQTTBROKER,1883,60) def 
processvideo(videosource=0): """ Funkcja do przetwarzania wideo z kamery lub pliku 
i wypisywania obiektów do terminalu. """ # Otwórz źródło wideo (kamera/plik) cap = 
cv2.VideoCapture(videosource) if not cap.isOpened(): print("Nie można otworzyć 
źródła wideo") return print("Rozpoczęto przetwarzanie wideo. Wciśnij 'q', aby 
zakończyć.") while True: ret, frame = cap.read() if not ret: print("Koniec wideo lub 
błąd odczytu") break # Wykrywanie obiektów w ramce results = model(frame) # 
Pobieranie wyników wykrywania detections = results[0].boxes.data # Dane detekcji 
for detection in detections: x1, y1, x2, y2, confidence, class_id = detection.tolist() 
class_name = model.names[int(class_id)] # Nazwa klasy obiektu 
client.publish(MQTT_TOPIC, class_name); print(f"Obiekt: {class_name}, Pewność: 
{confidence:.2f}") # Rysowanie prostokąta na obiekcie cv2.rectangle(frame, (int(x1), 
int(y1)), (int(x2), int(y2)), (0, 255, 0), 2) cv2.putText(frame, class_name, (int(x1), int(y1) 
10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) # Wyświetlanie przetwarzanego
wideo cv2.imshow('Wideo - YOLO Detection', frame) # Przerwij, jeśli naciśnięto 'q' if 
cv2.waitKey(1) & 0xFF == ord('q'): break cap.release() cv2.destroyAllWindows() if 
name == "main": # Użyj domyślnej kamery (lub zamień na ścieżkę do pliku 
wideo, np. "video.mp4") process_video(video_source=0) client_mqtt = 
mqtt.Client() client_mqtt.on_connect = on_connect client.disconnect()
