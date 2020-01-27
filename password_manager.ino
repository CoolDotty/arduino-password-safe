
#include <SPI.h>
#include <SD.h>
#include <Keyboard.h>

const char* FLAG_FILE = "F.LG";

void setup() {
  Keyboard.begin();
  Serial.begin(9600);
  if (!SD.begin()) {
    render("SD err");
    return;
  }

  if (SD.exists(FLAG_FILE)) {
    // Enter cred
    File flag = SD.open(FLAG_FILE, FILE_READ);
    File cred = SD.open(getContent(flag), FILE_READ);
    render(getContent(cred));
    cred.close();
    flag.close();
    SD.remove(FLAG_FILE);
  } else {
    // Cycle through creds

    File root = SD.open("/");
    File next = root.openNextFile();
    while(next) {
      if (strcmp(next.name(), FLAG_FILE) == 0) {
        continue;
      }
      File flag = SD.open(FLAG_FILE, FILE_WRITE);
      flag.write(next.name());
      Serial.print(next.name());
      flag.close();
      render(next.name());
      delay(1500);
      next = root.openNextFile();
      SD.remove(FLAG_FILE);
    }
    render("End program");
  }
}

void loop() {
  
}

int bufferSize = 0;

void render(String s) {
  for (int i = 0; i < bufferSize; i++) {
    Keyboard.write(178); // backspace
  }
  Keyboard.print(s);
  bufferSize = s.length();
}

String getContent(File f) {
  String s = "";
  while(f.available()) {
    s = s + (char)f.read();
  }
  return s;
}
