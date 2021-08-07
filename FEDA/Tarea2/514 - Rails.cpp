/* 
Nombre: Matías Sebastián Barrientos Zagal
ID: matibarri14
Autoría: Código extraído del siguiente link https://github.com/ackoroa/UVa-Solutions/blob/master/UVa%20514%20-%20Rails/src/UVa%20514%20-%20Rails.cpp 
Análisis asintótico de la solución:
    Tiempo: Tanto .pop() como .push(elemento) son operaciones de stack con complejidad constante (ref:cplusplus.com). Así,la complejidad estará relacionada
    a los ciclos while existentes. Específicamente, el while que contiene el .push(elemento) y el while que contiene el .pop() harán tantas iteraciones como
    el entero "n" extraído del input. Por lo tanto, como hay dos ciclos while, pero uno es constante (n máx 1000), la complejidad será lineal.
    
    Espacio: En el peor de los casos, el input será con n=1000 enteros en un vector. Por lo tanto, el espacio máximo a utilizar por el vector
    es 4 bytes * 1000 enteros. Luego, en el peor de los casos, se incorporan los n elementos a la pila. Lo cual también ocuparía un espacio máximo
    de 16*1000 bytes. Luego, el espacio total sería la suma de ambas estructuras de enteros.
 */

// Librerías a utilizar en el programa.
#include <iostream>
#include <stack>
using namespace std;

int main(){
    // el tren llega desde la dirección A y tiene "n" vagones.
    int n, target[1000]; //Declara la variable "n" como un entero y el vector target de tamaño 1000 debido a que es el límite de "n", lo cual sería el espacio máx a utiliza.
    int i; //Declara la variable "i" como un entero.

    while (true){
        cin >> n; // Se lee la primera línea que contiene a "n" para luego ir leyendo las demás líneas de este caso.
        if (n == 0) //El último bloque consta de sólo una línea que contiene un "0" y ahí se debe detener el programa.
            break; //Con esto se detiene el while true.

        while (true){ //Al ser un while true, siempre se entra a este ciclo.
            cin >> target[0]; //Lee el primer número de la línea siguiente al "n". En el Sample Input del enunciado, sería el "1" que viene después del "n = 5".
            //Si no lo leyera, podría ser un error, ya que el vector contiene basura y podría darse la casualidad de que justo sea un 0.
            if (target[0] == 0){ //Con este if se verifica el término de un i-ésimo bloque o caso.
                cout << endl; //El salto de línea corresponde a la forma del output que pide el problema.
                break; //con esto se detiene el while true
            }
            for (i = 1; i < n; i++){ //En este for lee los demás enteros que vienen luego del primero y los pone en el vector (que originalmente tiene "basura")
                cin >> target[i];    //En el caso del Sample Input del enunciado, luego del "1" estaría leyendo "2", "3", "4" y el "5" como enteros.
            }

            int currCoach = 1; //Carro actual al cual se está evaluando.
            int targetIndex = 0; //índice del vector al carro objetivo.
            /*Como la estación tiene sólo una entrada que también es la salida (callejón sin salida)
            y el primer vagón será el último en salir, entonces se puede considerar una pila.*/
            stack<int> station;
            while (currCoach <= n){
                station.push(currCoach); //inserción del elemento currCoach encima de la stack
                /*Para entrar a este while, la pila no debe estar vacía (primera condición) y (AND, vale decir, se deben cumplir ambas)
                el elemento que está en el tope de la pila debe ser igual al elemento de la posición targetIndex*/
                while (!station.empty() && station.top() == target[targetIndex]){
                    station.pop(); //Aquí se remueve el elemento del tope de la pila station.
                    targetIndex++; //Luego, se aumenta en uno el índice del targetIndex, ya que se debe cumplir que los vagones ingresan de manera creciente.
                    if (targetIndex >= n) //El límite del targetIndex es "n", ya que es el número de vagones que tiene el tren.
                        break; //Termina el while si targetIndex es igual o mayor al "n".
                }
                /*Finalmente, se aumenta en uno el carro actual por la lógica de que ingresan de manera creciente. Por lo tanto, el sig vagón del i-ésimo 
                vagón es el i+1. Con ello se asegura que se estén insertando los vagones correspondientes al "n" dado por el tren.*/
                currCoach++;

            }
            //En este condicional if-else se verifica si es viable la permutación dada y se obtiene el output que pide el problema.
            if (station.empty())
                cout << "Yes" << endl; 
            else
                cout << "No" << endl; 
        }

    }
    return 0;
}