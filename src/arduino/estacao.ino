/*
  Estação Meteorológica - Sketch Arduino

  Lê dados do sensor DHT11 (temperatura e umidade) e envia
  pela porta serial em formato JSON a cada 5 segundos.

  Circuito:
    - DHT11 VCC  → 5V do Arduino
    - DHT11 GND  → GND do Arduino
    - DHT11 DATA → Pino Digital 2 (com resistor pull-up de 10kΩ para 5V)

  Nota: Este sketch é referência para uso com hardware real.
  Para simulação, use o script Python simulador.py.
*/

#include "DHT.h"

#define DHTPIN 2
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  float temp = dht.readTemperature();
  float umid = dht.readHumidity();

  if (!isnan(temp) && !isnan(umid)) {
    Serial.print("{");
    Serial.print("\"temperatura\":"); Serial.print(temp);
    Serial.print(",\"umidade\":");    Serial.print(umid);
    Serial.println("}");
  }

  delay(5000);
}
