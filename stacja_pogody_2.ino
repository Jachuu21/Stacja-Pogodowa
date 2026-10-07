#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <Adafruit_GFX.h>

#include <DHT.h>
#define DHTPIN 2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP280 bmp;

void setup() {
  Serial.begin(9600);
  dht.begin();
  
  if(!bmp.begin(0x76)){
    Serial.println("Nie znaleziono czujnika");
    while(1);
  }
  
  
  delay(3000);
  
}

void loop() {
  
  float temp=bmp.readTemperature();
  float press=bmp.readPressure() / 100.0;
  float wys=bmp.readAltitude(1013.25);
  float wilgotnosc = dht.readHumidity();
  Serial.print(temp);
  Serial.print(",");
  Serial.print(press);
  Serial.print(",");
  Serial.print(wys);
  Serial.print(",");
  Serial.println(wilgotnosc);
  
  delay(2000);

}
