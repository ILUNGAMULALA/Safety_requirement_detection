#include <WiFi.h>

const char* ssid = "Daniel Kadurha";
const char* password = "danielkadurha";

WiFiServer server(80);

int ledPin = 4; 
unsigned long lastMessageTime = 0; 
unsigned long timeoutDuration = 30000;  

void setup() {
  Serial.begin(115200);
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");


  Serial.println("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Start the server
  server.begin();

  // Set the LED pin as an output
  pinMode(ledPin, OUTPUT);
}

void loop() {
  WiFiClient client = server.available();  // Listen for incoming clients

  if (client) {
    Serial.println("New Client Connected");

    String command = client.readStringUntil('\n');
    command.trim();  // Remove any whitespace

    Serial.println("Command received: " + command);

    // Update the last message time
    lastMessageTime = millis();

    // Control the built-in LED based on the received command
    if (command == "yes") {
      digitalWrite(ledPin, HIGH);  // Turn on LED
      Serial.println("LED ON");
    } 
    else if (command == "no") {
      digitalWrite(ledPin, LOW);   // Turn off LED
      Serial.println("LED OFF");
    }

    // Close the connection
    client.stop();
    Serial.println("Client Disconnected");
  }

  // Check for timeout: if no message received in timeoutDuration, turn off LED
  if (millis() - lastMessageTime > timeoutDuration) {
    digitalWrite(ledPin, LOW);  // Turn off LED
    //Serial.println("No message received for 1 minute, LED OFF due to timeout.");
  }
  millis()==0;
}

