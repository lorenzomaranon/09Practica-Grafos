"""Práctica 09 · Grafos: una red social.

La red es un grafo NO dirigido y SIN pesos: cada persona es un vértice y cada
amistad una arista. Se guarda como LISTA DE ADYACENCIA (la representación por
defecto del tema 6), con los nombres traducidos a números UNA sola vez:

    self._nombres[i]   nombre de la persona i                   (número -> nombre)
    self._indice[n]    número de la persona con nombre n        (nombre -> número)
    self._ady[i]       números de los amigos de i, en el orden en que se añadieron
    self._m            número de amistades (aristas)

Invariante (grafo simple y no dirigido):
    1. v aparece en self._ady[u]  <=>  u aparece en self._ady[v]
    2. nadie aparece en su propia lista (sin lazos)
    3. nadie aparece dos veces en la misma lista (sin multiaristas)
    4. self._m == (suma de las longitudes de las listas) / 2

Fuera de la clase todo son nombres; dentro, todo son enteros 0..n-1.
"""

from collections import deque


class RedSocial:
    # ------------------------------------------------------------------ dado
    def __init__(self, personas=(), amistades=()):
        self._nombres = []
        self._indice = {}
        self._ady = []
        self._m = 0
        for p in personas:
            self.anadir_persona(p)
        for a, b in amistades:
            self.anadir_amistad(a, b)

    def anadir_persona(self, nombre):
        """Añade una persona sin amigos. O(1) esperado."""
        if nombre in self._indice:
            raise ValueError(f"persona repetida: {nombre}")
        self._indice[nombre] = len(self._nombres)
        self._nombres.append(nombre)
        self._ady.append([])

    def _id(self, nombre):
        """Nombre -> número. ValueError si la persona no existe. O(1) esperado."""
        try:
            return self._indice[nombre]
        except KeyError:
            raise ValueError(f"persona desconocida: {nombre}") from None

    def num_personas(self):
        return len(self._nombres)

    def num_amistades(self):
        return self._m

    def personas(self):
        return list(self._nombres)

    def amigos(self, nombre):
        """Amigos de `nombre`, en el orden en que se añadieron. O(grado)."""
        return [self._nombres[v] for v in self._ady[self._id(nombre)]]

    def grado(self, nombre):
        return len(self._ady[self._id(nombre)])

    def son_amigos(self, a, b):
        """¿Hay amistad entre a y b? Recorre la lista de a: O(grado(a))."""
        return self._id(b) in self._ady[self._id(a)]

    # ------------------------------------------------------------ Ejercicio 1
    def anadir_amistad(self, a, b):
        """Añade la amistad {a, b}.

        Contrato:
          - a o b desconocidos      -> ValueError (lo hace self._id)
          - a == b                  -> ValueError (no hay lazos)
          - la amistad ya existía   -> no cambia nada y devuelve False
          - si no                   -> la añade EN LAS DOS LISTAS, m += 1, devuelve True
        Coste: O(grado(a)) por la comprobación de duplicado.
        """
        # TODO: implementar
        raise NotImplementedError("Ejercicio 1: anadir_amistad")

    def amigos_en_comun(self, a, b):
        """Amigos de a que también lo son de b, en el orden de la lista de a.

        Pista: pasa los amigos de b a un set y recorre los de a.
        Coste: O(grado(a) + grado(b)) esperado. Nada de dos bucles anidados.
        """
        # TODO: implementar
        raise NotImplementedError("Ejercicio 1: amigos_en_comun")

    # ------------------------------------------------------------ Ejercicio 2
    def etiquetas_de_grupo(self):
        """Lista `grupo` de longitud n: grupo[i] = número del grupo de la persona i.

        Un grupo es una componente conexa. Los grupos se numeran 0, 1, 2...
        en el orden en que aparece su primera persona (la de menor número):
        recorre las personas 0..n-1 y lanza un recorrido desde cada una que
        siga sin grupo.

        OBLIGATORIO: con una PILA explícita (una lista con append/pop), sin
        recursión. Hay un test con una cadena de 100 000 personas.
        Coste: O(n + m).
        """
        n = self.num_personas
        grupo = [-1] * n
        actual = 0
        for s in range(n):
            if grupo[s] != -1:
                continue


            grupo[s] = actual
            pila = [s]

            while pila:
                u = pila.pop()
                for v in self._ady[u]:
                    if grupo[v] == -1:
                        grupo[v] = actual
                        pila.append(v)
            actual += 1

        return grupo

    def grupos(self):
        """Lista de grupos; cada grupo, la lista de sus nombres por número. O(n + m)."""
        grupo = self.etiquetas_de_grupo()
        salida = [[] for _ in range(max(grupo) + 1)] if grupo else []
        for i, g in enumerate(grupo):
            salida[g].append(self._nombres[i])
        return salida

    def mismo_grupo(self, a, b):
        """¿Hay alguna cadena de amistades entre a y b? O(n + m)."""
        u, v = self._id(a), self._id(b)
        grupo = self.etiquetas_de_grupo()
        return grupo[u] == grupo[v]

    # ------------------------------------------------------------ Ejercicio 3
    def _bfs(self, origen):
        """BFS desde el número `origen`. Devuelve (dist, padre), dos listas de longitud n.

        dist[v]  = mínimo número de amistades para llegar de origen a v (-1 si no se llega)
        padre[v] = persona desde la que se descubrió v (-1 para el origen y los no alcanzados)

        Reglas: los vecinos se exploran en el orden de self._ady[u]; la cola es
        un collections.deque (popleft es O(1); list.pop(0) es O(n)); y se marca
        al METER en la cola. Coste: O(n + m).
        """
        # TODO: implementar
        raise NotImplementedError("Ejercicio 3: _bfs")

    def separacion(self, a, b):
        """Grados de separación entre a y b: amistades del camino más corto, -1 si no hay."""
        u, v = self._id(a), self._id(b)
        dist, _ = self._bfs(u)
        return dist[v]

    def niveles(self, nombre):
        """Personas agrupadas por distancia a `nombre`: [[nombre], [amigos], [amigos de amigos], ...]."""
        dist, _ = self._bfs(self._id(nombre))
        alcanzadas = [d for d in dist if d != -1]
        salida = [[] for _ in range(max(alcanzadas) + 1)]
        for i, d in enumerate(dist):
            if d != -1:
                salida[d].append(self._nombres[i])
        return salida

    def cadena(self, a, b):
        """Cadena de presentaciones más corta de a a b: [a, ..., b].

        [a] si a == b; [] si no están conectados. Usa _bfs y sigue `padre`
        hacia atrás desde b; luego dale la vuelta. Coste: O(n + m).
        """
        # TODO: implementar
        raise NotImplementedError("Ejercicio 3: cadena")

    # -------------------------------------------------------- Ejercicio extra
    def sugerencias(self, nombre):
        """'Personas que quizá conozcas'.

        Candidatos: amigos de amigos de `nombre` que no son ella misma ni ya
        amigos suyos. Para cada uno, cuántos amigos tiene en común con `nombre`.
        Devuelve una lista de pares (candidato, comunes) ordenada por comunes
        de mayor a menor y, a igualdad, por número de persona (de menor a mayor).

        Pistas: un set con los amigos de `nombre` y un diccionario contador
        candidato -> comunes (como las frecuencias de la práctica 08). No hace
        falta un BFS completo: basta con dos niveles de bucles sobre listas.
        Coste: O(suma de los grados de sus amigos + S log S), S = candidatos.
        """
        # TODO: implementar
        raise NotImplementedError("Ejercicio extra: sugerencias")


# ---------------------------------------------------------------- la red de ejemplo
PERSONAS_EJEMPLO = ["Ana", "Bruno", "Carla", "David", "Elena", "Fede",
                    "Gloria", "Hugo", "Irene", "Jorge", "Lucas"]

AMISTADES_EJEMPLO = [
    ("Ana", "Bruno"), ("Ana", "Carla"), ("Bruno", "Carla"), ("Bruno", "David"),
    ("Carla", "David"), ("Carla", "Elena"), ("David", "Fede"), ("Elena", "Fede"),
    ("Fede", "Gloria"), ("Hugo", "Irene"), ("Irene", "Jorge"),
]


def red_de_ejemplo():
    return RedSocial(PERSONAS_EJEMPLO, AMISTADES_EJEMPLO)
