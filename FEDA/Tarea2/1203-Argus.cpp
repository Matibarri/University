/* 
Nombre: Matías Sebastián Barrientos Zagal
ID: matibarri14
Autoría: Código extraído del siguiente link https : //github.com/KHvic/uva-online-judge/blob/master/1203-Argus.cpp 
Análisis asintótico de la solución:
    Tiempo: El primer while, estará dado por .push y la cantidad de veces que se realiza el ciclo. Así, dado que se utiliza push_heap, la complejidad de ese while
    es O(log(n)) con n el número de registros que habrá en ese caso del input. Por otra parte, el segundo while también está dado por push, ya que pop es constante.
    En este while, la cantidad de veces que se ejecute la línea con .push() será k. Por lo tanto, la complejidad será O(log(k)). Finalmente, la complejidad del problema
    será el O(log(m)) donde m  = max{k,n}.
    
    Espacio: el espacio estará dado por el número de registros que tenga el caso, definido como "n". Además, las estructuras de datos que se utilizan son dos: priority queue y unordered map.
    Donde en el algoritmo se añaden todos esos registros. Así, el tamaño del vector de la priority queue y del diccionario será n. Así, el total será 2*n.
    Con respecto a la cantidad de bytes, al ser pares de enteros, entonces será 2*n*2*4 bytes.
*/

//A Continuación se presentan las librerías importadas en este programa.

#include <bits/stdc++.h>
using namespace std;

#define pa pair<int, int>

int main(){
    string in; //En este caso, el string será "Register" o "#".
    int q, p; //p: periodo y q: q num como números enteros.
    priority_queue<pa, vector<pa>, greater<pa>> pq; //creación cola de prioridad con elementos pares dentro de vectores y usando la comparación mayor que.
    //en un pair, greater compara con .first de dicho pair.
    unordered_map<int, int> qToP; //Creación de un diccionario que guardará un par de dos elementos enteros para guardar el period de cada registro para su uso posterior.
    while (cin >> in, in != "#"){ //Este ciclo lee el primer string de cada línea y entrará siempre y cuando no sea "#".
        cin >> q >> p;
        qToP[q] = p; // Le añade el valor de la variable p a la clave q del diccionario
        pq.push({p, q}); //Añade a la cola de prioridad el par {p,q} 
    }
    int k;
    cin >> k; //Se define y se lee k que vendría después de "#", ya que el while anterior se saldrá cuando encuentre este string en cierta línea del input.
    while (k--){ //Este ciclo se realiza las "k" cantidad de veces solicitadas por el caso dado.
        pa top = pq.top(); //Al pair de mayor prioridad lo define como top. Complejidad constante.
        pq.pop(); //Luego elimina el elemento siguiente, que sería el mismo que se definió anteriormente como top (pero no elimina a top!!)
        cout << top.second << endl; //Como el par es {p,q}, imprime q que sería top.second en el par. En el ejemplo del enunciado, sería el 2004 o 2005. Lo cual es lo solicitado por el problema.
        top.first += qToP[top.second]; //al p del pair top se le suma el valor de su period que será cuando nuevamente se devolverá el resultado.
        pq.push(top); //Finalmente, lo añade a la cola de prioridad con el nuevo valor de top.first obtenido en la línea anterior.
    }
}