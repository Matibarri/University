/* 
Nombre: Matías Sebastián Barrientos Zagal
ID: matibarri14
Autoría: Código extraído del siguiente link https : //github.com/allen1759/UVa-online-judge/blob/master/978%20-%20Lemmings%20Battle!.cpp 
Análisis asintótico de la solución:
    Tiempo: El peor de los casos sería cuando al realizar las batallas o enfrentamientos, un equipo ganara las batallas pero sobreviven todos los lemming con
    menos poder que antes. Por tanto, considerando "n" como el tamaño de la cola de prioridad más grande, se tendría que recorrer el vector
    para que en la cola de prioridad ir añadiendo los valores. Esto lleva a una complejidad O(nlogn). Sin embargo, al utilizar el método .clear() de <vector>,
    entonces se obtiene una complejidad lineal O(n), ya que se debe recorrer elemento por elemento para poder eliminarlos del vector. 
    
    Espacio: El espacio utilizado proviene de las dos colas de prioridad y de los dos vectores, donde cada una de las estructuras sólo considera elementos enteros.
    Por lo cual el número de bits estará dado según la cantidad de lemming que hayan como entrada y de los triunfos que éstos obtengan. En el peor de los casos,
    tanto la cola de prioridad como el vector de cada equipo tendrá un largo n, así, el espacio final uilizado estará dado por O(n). Específicamente, 4*n*4 bytes.
 */

//A Continuación se presentan las librerías importadas en este programa.

#include <iostream>
#include <cstdio>
#include <vector>
#include <queue>
using namespace std;

int main(){
    //N = testcases, representa el número de casos de prueba que siguen.
    int testcases;
    cin >> testcases;

    for (int test = 0; test < testcases; ++test){
        int wars, green, blue, tmp; //Para los N casos se define el número de batallas o guerras, los lemmings azules y verdes junto con el poder de cada lemming
        /* Se eligen colas de prioridad debido a que el orden del input no es de manera creciente o decreciente, donde el elemento que se necesita "sacar" es el de mayor valor(poder)
        Así, se utilizan dos colas para poder extraer los valores más grandes (lemmings más poderosos), siendo este el criterio, para luego realizar el combate entre ellos */
        priority_queue<int, deque<int>, less<int>> gpq; //Cola de prioridad para los lemmings verdes
        priority_queue<int, deque<int>, less<int>> bpq; //Cola de prioridad para los lemmings azulez
        cin >> wars >> green >> blue; // Se leen desde el input las variables definidas anteriormente
        for (int i = 0; i < green; ++i){ //En este for se le agregan los poderes de los lemmings verdes y el tamaño de la priority queue será el tamaño de la variable "green"
            cin >> tmp;
            gpq.push(tmp); //Complejidad logarítmica (con push_heap)
        }
        for (int i = 0; i < blue; ++i)
        { //En este for se le agregan los poderes de los lemmings azules y el tamaño de la priority queue será el tamaño de la variable "blue"
            cin >> tmp;
            bpq.push(tmp); //Complejidad logarítmica (con push_heap)
        }
        while (gpq.size() > 0 && bpq.size() > 0){ //La condición del while hace referencia a que existe guerra siempre que hayan lemmings para combatir.
            vector<int> garr, barr; //En estos vectores irán los lemming que vayan sobreviviendo de los combates (garr para verde y barr para los azules)
            for (int w = 0; w < wars; ++w){ 
                if (gpq.empty() || bpq.empty()) // si alguno de las dos colas ya no contiene lemmings, entonces se termina la guerra.
                    break;
                int gso = gpq.top(); //Se guarda el lemming verde que combatirá (top muestra el elemento de mayor prioridad), donde .top() es de complejidad cte.
                gpq.pop(); //Se extrae el lemming verde que combatirá, el de mayor poder primero.
                int bso = bpq.top(); //Se guarda el lemming azul que combatirá (top muestra el elemento de mayor prioridad). 
                bpq.pop();           //Se extrae el lemming azul que combatirá, el de mayor poder primero. Complejidad logarítmica (pop_heap)
                /*Luego de esto, se debe realizar la batalla entre gso y bso. Aquí se tienen dos casos, donde gana uno o gana el otro.
                En cualquiera de los dos if, se agrega el poder que le queda al triunfador al final del vector barr o garr, después de su último elemento actual.
                La diferencia de los poderes dependerá de cuál sea el mayor.*/
                if (gso > bso){
                    garr.push_back(gso - bso); //Complejidad constante (amortizado) o lineal (reasignación).
                }
                else if (gso < bso){
                    barr.push_back(bso - gso); //Complejidad constante (amortizado) o lineal (reasignación).
                }
            }
            for (int e : garr){ //Para todos los lemmings verdes que ganaron y les queda poder, se insertan en la green priority queue
                gpq.push(e);    //Complejidad logarítmica (con push_heap)
            }
            for (int e : barr){ //Para todos los lemmings azulez que ganaron y les queda poder, se insertan en la blue priority queue
                bpq.push(e);    //Complejidad logarítmica (con push_heap)
            }
            garr.clear(); //Remueve todos los elementos del vector garr. Complejidad lineal.
            barr.clear(); //Remueve todos los elementos del vector barr. Complejidad lineal.
        }

        if (test != 0){
            cout << endl; //Va generando un salto de línea que se solicita en el output del problema.
        }
        if (gpq.size() == bpq.size()){ //Imprime "verde y azul murieron" cuando ambas priorities queues no tienen elementos, es decir, no hay lemming al cual le haya quedado poder.
            cout << "green and blue died" << endl;
        }
        else if (gpq.size() > 0){ //Este caso es para cuando lemmings verdes ganan.
            cout << "green wins" << endl;
            while (!gpq.empty()){ //cuando hay un ganador, se debe imprimir el poder de cada lemming que le quedaba.
                //for(int e : gpq) {
                int e = gpq.top(); //Guarda el elemento de mayor prioridad (el lemming con más poder) en una variable "e"
                gpq.pop(); //Elimina dicho elemento
                cout << e << endl; //y finalmente lo imprime para cumplir con el output del problema.
            }
        }
        else{
            cout << "blue wins" << endl; //Este caso es para cuando lemmings azules ganan y la lógica es igual al else-if anterior.
            while (!bpq.empty())
            { //cuando hay un ganador, se debe imprimir el poder de cada lemming que le quedaba.
                //for(int e : bpq) {
                int e = bpq.top(); //Guarda el elemento de mayor prioridad (el lemming con más poder) en una variable "e"
                bpq.pop();         //Elimina dicho elemento
                cout << e << endl; //y finalmente lo imprime para cumplir con el output del problema.
            }
        }
    }

    return 0;
}