/* 
Nombre: Matías Sebastián Barrientos Zagal
ID: matibarri14
Autoría: Código extraído del siguiente link  https : //github.com/Rodagui/UVa-Solutions/blob/master/11286%20-%20Conformity.cpp 
Análisis asintótico de la solución:
    Tiempo: A pesar de que el ordenamiento es O(mlogm), donde m=5 (cantidad de cursos tomados), este será constante. No varía el tamaño.
    Por otra parte, el método count() es O(logn)  donde n es el número de frosh que hay en total (este varía, pero está en un intervalo dado). Sin embargo,
    insertar en la posición j cada curso en el vector es O(m), pero como m es fijo también será constante. Así el ciclo for que hará estas operaciones
    es el que se lleva la complejidad lineal O(n) (O(n) > O(logn)), dependiendo del número de frosh.
    
    Espacio: Dado que un entero tiene tamaño de 32 bits y como son 5 enteros por vector, entonces los bits utilizados por cada frosh en esta estructura
    es de 160 bits. Además, se debe multiplicar por el n dado, es decir, 160*n bits. El map también guarda un entero asociado a cada vector (combinación de cursos),
    por lo que por cada vector se utilizan 32 bits para representarlo. Así, (160*n  + 32*n) será el tamaño utilizado.

 */

#include <iostream>
#include <map>
#include <vector>
#include <algorithm>
using namespace std;

int main(){
    int n;  //Declara el tipo de variable entera para n.

    while (cin >> n and n){ //Lee el valor de n, correspondiente al número de frosh, y será la cantidad de veces que se ejecutará el ciclo.

        int maximo = 0;

        map< vector<int>, int> frosh; //Creación del diccionario ordenado frosh para que cada "frosh" tenga asociado un vector con su respectiva combinación de cursos.
        vector<int> arr(5); // Arreglo que constará de los 5 cursos que toma cada uno de los frosh (combinación de cursos de cada frosh).
        //O(5*n) in O(n)
        for (int i = 0; i < n; i++){ //O(n)
            for (int j = 0; j < 5; j++){// O(k) En este for se agregan los números de curso, que son exactamente 5, al vector arr definido anteriormente.
                cin >> arr[j];
                //cout << "arr[j]: " << arr[j] << endl;
            }
            //cout << "i: " << i << endl;

            //Se ordenan los vectores para identificar los que son iguales (misma combinación), pero que no están en el mismo orden. Por ejemplo: 103 102 101 488 100 y 100 101 102 103 488.
            sort(arr.begin(), arr.end()); //Aquí se ordenan los cursos que han ingresado anteriormente al vector, en este caso,
                                        // al usar sort() se ordenan los elementos del rango [first,last) en orden ascendente. O(mlogm)

            if (frosh.count(arr) == 1){ // Acá cuenta con .count(), que es O(logm), la cantidad de veces que está arr en el map. Si es una vez, entra al if.
                frosh[arr]++; //Acá suma los valores del vector arr.
               
            }
            else{
                frosh[arr] = 1;
            }
        }

        map<vector<int>, int>::iterator i; //Creación del iterador que se utilizará para ver cuántas veces se repite la o las combinaciones más populares de cursos.

        for (i = frosh.begin(); i != frosh.end(); ++i){ //En esta parte se utiliza un iterador para recorrer el map y ver cuál es el máximo, es decir, cuál combinación de cursos es más popular y establecer esa cantidad como máximo.
            if ((i->second) > maximo)
                maximo = i->second;
                
        }

        int cont = 0;

        for (i = frosh.begin(); i != frosh.end(); ++i){ // En esta sección se recorre el map para ver cuántas combinaciones de cursos son las más populares.
            if ((i->second) == maximo)
                cont++;
        }

        maximo = maximo * cont; //Calcula el número total de estudiantes que toma alguna combinación de cursos que sea de las más populares o la más popular.

        cout << maximo << '\n'; //Imprime el valor máximo contado "cont" veces (combi de cursos más populares.)

        frosh.clear(); //Vacía el map para poder realizar la siguiente iteración del ciclo con la estructura de datos disponible.
    }

    return 0;
}