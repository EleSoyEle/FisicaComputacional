//Librerias para poder usar codigo de C
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

//Librerias para controlar la pantalla
#include <Adafruit_ST7735.h>
#include <Adafruit_GFX.h>
#include <SPI.h>
#include <Wire.h>

#define TFT_CS         14
#define TFT_RST        32
#define TFT_DC         15

//Definimos las macros de los colores
#define BLACK   0xFFFF
#define WHITE   0x0000
#define BLUE    0x07FF
#define RED     0xFFE0 
#define GREEN   0xF81F
#define CYAN    0xFFE0
#define MAGENTA 0x07E0
#define YELLOW  0xF800 
#define ORANGE  0xFE00  
#define POISON  0x68FF

//Creamos el objeto display que contiene las funciones para la pantalla
Adafruit_ST7735 display(TFT_CS,TFT_DC,TFT_RST);

//Variables para la lectura del voltaje
int val = 0; //Valor que sera medido en el loop
int analog_pin = 26; //Pin del esp32

//Puntero donde vamos a guardar las lecturas
int* points = (int*)calloc(80,sizeof(int));
int num = 1; //Cuenta que tan lleno esta el puntero

float w = 7.335e-4; //Factor de peso para calcular el voltaje

void setup() {
  Serial.begin(9600); //Comunicacion con el pc

  //Inicializamos la pantalla
  display.initR(INITR_MINI160x80);
  display.fillScreen(BLACK);
  display.setRotation(3);
  display.fillScreen(BLACK);
  display.setTextColor(WHITE);

}

void loop() {
  val = analogRead(analog_pin); //Tomamos la lectura del pin analogico
  int conv = (int)(60*(val-2350)/1745); //Ajuste del punto para graficar
  float voltaje = w*((float)val-2350.0)+1.34; //Calculamos el voltaje

  //Preparamos el texto que sera mostrado en la pantalla
  char text[20];
  sprintf(text,"V: %f",voltaje); 
  
  //Aqui añadimos y modificamos el puntero
  if(num<80){
    //Si el buffer no esta lleno entonces le podemos añadir el siguiente elemento de las lecturas
    num+=1;
    points[num] = conv;
  }
  else{
    //En caso de que el buffer este lleno vamos a desplazar los numeros para poder añadir la siguiente lectura
    //Ejemplo: Buffer: [1,2,3,4], Val: 5 ---> [2,3,4,5] Buffer desplazado
    for(int i=1;i<80;i++){
      points[i-1] = points[i];
    }
    points[num-1]=conv;
  }
  Serial.println(val);
  delay(100); //Dejamos 100 milisegundos entre lecturas

  if(num>0){
    //Mostramos la informacion del buffer en la pantalla
    display.fillScreen(BLACK);
    display.setCursor(10,10);
    display.print(text);
    for(int i=1;i<79;i++){
      display.drawLine(2*(i-1),78-points[i],2*i,78-points[i+1],WHITE);
    }
  }

}
