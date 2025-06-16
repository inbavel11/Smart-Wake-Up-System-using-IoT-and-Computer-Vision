#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

// Replace with your WiFi credentials
const char* ssid = "inba";
const char* password = "inba@610";

// Create a web server object
ESP8266WebServer server(80);

// GPIO pins
#define LIGHT_PIN D1
#define MOTOR_PIN D2
#define BUZZER_PIN D3

void setup() {
  Serial.begin(115200);

  // Set pins as output
  pinMode(LIGHT_PIN, OUTPUT);
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);

  // Initially OFF
  digitalWrite(LIGHT_PIN, LOW);
  digitalWrite(MOTOR_PIN, LOW);
  digitalWrite(BUZZER_PIN, LOW);

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Connected to WiFi");
  Serial.print("📶 IP address: ");
  Serial.println(WiFi.localIP());

  // Define routes for controlling devices
  server.on("/", HTTP_GET, []() {
    String html = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width, initial-scale=1'>";
    html += "<style>";
    html += "body { font-family: Arial, sans-serif; text-align: center; padding: 20px; background-color: #f4f4f4; }";
    html += "h2 { color: #333; }";
    html += "button { padding: 10px 20px; font-size: 18px; margin: 10px; cursor: pointer; border-radius: 5px; border: none; }";
    html += "button:hover { background-color: #4CAF50; color: white; }";
    html += "</style></head><body>";
    html += "<h2>Device Control Dashboard</h2>";
    html += "<button onclick=\"window.location.href='/light/on'\">Turn Light ON</button><br>";
    html += "<button onclick=\"window.location.href='/light/off'\">Turn Light OFF</button><br>";
    html += "<button onclick=\"window.location.href='/motor/on'\">Turn Motor ON</button><br>";
    html += "<button onclick=\"window.location.href='/motor/off'\">Turn Motor OFF</button><br>";
    html += "<button onclick=\"window.location.href='/buzzer/on'\">Turn Buzzer ON</button><br>";
    html += "<button onclick=\"window.location.href='/buzzer/off'\">Turn Buzzer OFF</button><br>";
    html += "</body></html>";
    server.send(200, "text/html", html);
  });

  // Define actions for each route
  server.on("/light/on", []() {
    digitalWrite(LIGHT_PIN, HIGH);
    server.send(200, "text/plain", "Light ON");
  });

  server.on("/light/off", []() {
    digitalWrite(LIGHT_PIN, LOW);
    server.send(200, "text/plain", "Light OFF");
  });

  server.on("/motor/on", []() {
    digitalWrite(MOTOR_PIN, HIGH);
    server.send(200, "text/plain", "Motor ON");
  });

  server.on("/motor/off", []() {
    digitalWrite(MOTOR_PIN, LOW);
    server.send(200, "text/plain", "Motor OFF");
  });

  server.on("/buzzer/on", []() {
    digitalWrite(BUZZER_PIN, HIGH);
    server.send(200, "text/plain", "Buzzer ON");
  });

  server.on("/buzzer/off", []() {
    digitalWrite(BUZZER_PIN, LOW);
    server.send(200, "text/plain", "Buzzer OFF");
  });

  server.onNotFound([]() {
    server.send(404, "text/plain", "404 Not Found");
  });

  server.begin();
  Serial.println("🚀 HTTP Server started");
}

void loop() {
  server.handleClient();
}
