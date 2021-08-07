/* 
Nombre: Matías Sebastián Barrientos Zagal
ID: matibarri14
Autoría: Código extraído del siguiente link https : //gist.github.com/ooJerryLeeoo/b81c8c27f9c8221c8b23f48cea494afb 
Análisis asintótico de la solución:

    Tiempo: Sea n el número de carácteres que hay en el texto. Además, sea m la cantidad de '[' y ']' que hay en el texto. Como inserta texto cada vez que se encuentra
	con el símbolo inicio o fin, esto dirá la cantidad de veces que se realizará un Push (sea front o back). Así, como ambos push son constantes, entonces la complejidad 
	está dada por O(n*m).
    
    Espacio: Predomina el espacio utilizado por deque, ya que las demás sólo son variables de menor tamaño. Sin embargo, el largo de la dequqe dependerá
	de la cantidad de carácteres que se ingresen. Por lo tanto, depende del input n. Específicamente, es del orden lineal con respecto a n: O(n). Además,
	como la función Push recibe la deque, entonces se copia la cantidad de veces que se llama la función, es decir, O(k*n), pero con k = cte. Así, no pierde
	el orden lineal de complejidad.

 */

#include <deque>
#include <iostream>
#include <string>
using namespace std;
void Push(string &str, deque<string> &dq, bool home);

int main(){
	char ch = 0, prev_ch = 0;
	while ((ch = std::getchar()) != EOF){ //Mientras ch que es leído (input) sea distinto al final del archivo, se ejecuta el ciclo while.
		string str; //Crea la variable str como un string que es del tipo necesario para el problema.
		//Primer filtro del texto
		if (ch != '[' && ch != ']'){ //Esta condición sirve para añadir el texto que está correctamente escrito, ya que no considera los casos de las teclas malas "inicio" y "fin"
			str = str + ch; //Concatenación del texto correcto.
		}
		deque<string> ans; //Esta deque se utiliza para agregar al inicio o al final el texto correspondiente, dependiendo de la tecla mal "pulsada". La estructura de deque facilita la construcción del texto.
		bool home = false; //Crea una variable booleana "home", donde será True si es Inicio y False si es Fin.
		//Segundo filtro del texto (contiene carácteres mal escritos por el teclado.)
		while ((ch = getchar()) != '\n'){ //Este ciclo es para ejecutar el "core" del código para cada línea donde se debe identificar el "Beiju".
			if (ch == '[' || ch == ']'){ //Cuando esté recorriendo la línea de texto, entrará a este condicional si se encuentra con '[' o ']'.
				Push(str, ans, home); //Agrega a la deque el texto hasta donde no tenga alguno de los carácteres asociados a fin o inicio. La función se explicará en la misma función.
				if (ch == '['){ // Como '[' es Inicio, entonces home tomará el valor de True. Esto tiene lógica gracias a la función Push.
					home = true;
				}
				else{ //En caso contrario, como ']' es Fin, entonces home tomará el valor de False. 
					home = false;
				}
			}
			else{ //En caso de que, entre errores de tecleado, exista texto bien escrito, es decir, que no contenga ']' ni '[', entonces lo agrega/concatena a la variable str. 
				str = str + ch;
			}
			prev_ch = ch; //guarda la última parte del texto al salir del while para así ser evaluada posteriormente.
		}

		if (prev_ch != '[' && prev_ch != ']'){ //Al salir del segundo while, quedó una fracción de string pendiente por evaluar (prev_ch). Así, sabiendo que sólo es "texto" que no contiene ']' ni '[', entonces se añade a la deque (adelante o atrás dependiendo del valor de home obtenido en el while recién terminado.)
			Push(str, ans, home);
		}
		for (auto d : ans){ //En este for va imprimiendo lo que queda en la estructura deque. Utiliza auto, ya que facilita el recorrido de la deque sin necesariamente saber qué tipo de variable hay dentro de esta.
			cout << d;
		}
		puts("");
	}
	return 0;
}

void Push(string &str, deque<string> &dq, bool home){
	if (!str.empty()){ //Si la variable str es distinto de vacío, entonces entra al condicional. Esto no realiza nada si str no tiene un string asociado.
		if (home){ //En este caso, entra cuando home = True, vale decir, cuando en el texto se encuentra el carácter '['
			dq.push_front(str); //Agrega al inicio de la deque, ya que es donde correspondía originalmente la fracción del texto. Complejidad constante según cplusplus.com.
		}
		else{
			dq.push_back(str); //Agrega "al final" de la deque, precisamente, agrega después de su último elemento. Simulando ser la tecla "Fin", ya que home = False. 
		}
		str.clear(); //vacía la variable str para que no se vaya acumulando la fracción de texto que se va guardando en str = str + ch.
	}
}
