int score[10][7] = {                      //Array to display number on 7 seg display
        { 0,0,0,0,0,0,1 },  // = 0
        { 1,0,0,1,1,1,1 },  // = 1
        { 0,0,1,0,0,1,0 },  // = 2
        { 0,0,0,0,1,1,0 },  // = 3
        { 1,0,0,1,1,0,0 },  // = 4
        { 0,1,0,0,1,0,0 },  // = 5
        { 0,1,0,0,0,0,0 },  // = 6
        { 0,0,0,1,1,1,1 },  // = 7
        { 0,0,0,0,0,0,0 },  // = 8
        { 0,0,0,0,1,0,0 }   // = 9
};

int p1score = 0;    //Player scores
int p2score = 0;
int p3score = 0;

int p1 =11;         //Pin numbers for players
int p2 = 12;
int p3 = 13;


void setup() {                    //Setup
 Serial.begin(9600);
 //delay(2000);
 pinMode(A1,INPUT);
 pinMode(A0,INPUT); 
 for(int i = 4; i < 14; i++) {
  pinMode(i, OUTPUT);
 }
}

void num_write(int p, int num) {      //Takes player number and score as input and displays the score on 7 seg display
  digitalWrite(p, HIGH);
  for(int i = 4; i < 11; i++) {
    digitalWrite(i, score[num][i-4]);
  }
  delay(5);
  digitalWrite(p, LOW);
}
void m(){                             //Take control signals from the first arduino and updates the score accordingly
  Serial.println(digitalRead(A0));
  Serial.println(digitalRead(A1));
  if(digitalRead(A0) != 0 || analogRead(A1) != 0){
    if(digitalRead(A0) == 0 && digitalRead(A1) == 1){           
      p1score = p1score + 1;
      delay(2000);
    }
    else if(digitalRead(A0)== 1 && digitalRead(A1) == 0){
      p2score = p2score  +  1;
      delay(2000);
    }
    else if(digitalRead(A0) == 1 && digitalRead(A1)== 1){
      p3score = p3score + 1;
      delay(2000);
    }
  }
}

void Seg() {                //Displays overall score
  m();
  num_write(p1, p1score);
  num_write(p2, p2score);
  num_write(p3, p3score);
}

void loop() {
 Seg();
}
