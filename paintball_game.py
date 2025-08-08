import random

class Player:
    """
    Representa a un jugador en el juego de paintball.
    """
    def __init__(self, nombre, vida=100, municion=10):
        self.nombre = nombre
        self.vida = vida
        self.municion = municion
        self.posicion = (0, 0) # (x, y)

    def __str__(self):
        return f"{self.nombre} (Vida: {self.vida}, Munición: {self.municion}, Pos: {self.posicion})"

    def disparar(self, objetivo):
        """Intenta disparar a otro jugador."""
        if self.municion > 0:
            self.municion -= 1
            print(f"{self.nombre} dispara a {objetivo.nombre}.")
            # 75% de probabilidad de acertar
            if random.random() < 0.75:
                print("¡Impacto!")
                objetivo.recibir_dano(25)
            else:
                print("¡Falló!")
        else:
            print(f"{self.nombre} no tiene munición.")

    def recibir_dano(self, cantidad):
        """Reduce la vida del jugador."""
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0
        print(f"A {self.nombre} le quedan {self.vida} puntos de vida.")

    def recargar(self):
        """Recarga la munición del jugador."""
        self.municion = 10
        print(f"{self.nombre} ha recargado. Munición: {self.municion}.")

    def moverse(self, direccion, ancho_tablero, alto_tablero):
        """Mueve al jugador en el tablero."""
        x, y = self.posicion
        if direccion == 'w': # Arriba
            y -= 1
        elif direccion == 's': # Abajo
            y += 1
        elif direccion == 'a': # Izquierda
            x -= 1
        elif direccion == 'd': # Derecha
            x += 1

        # Comprobar si el movimiento es válido (dentro del tablero)
        if 0 <= x < ancho_tablero and 0 <= y < alto_tablero:
            self.posicion = (x, y)
            print(f"{self.nombre} se mueve a {self.posicion}.")
        else:
            print("Movimiento inválido. Fuera de los límites del tablero.")

class Game:
    """
    Gestiona el estado y la lógica del juego de paintball.
    """
    def __init__(self, ancho_tablero=10, alto_tablero=10):
        self.ancho_tablero = ancho_tablero
        self.alto_tablero = alto_tablero
        self.tablero = [['.' for _ in range(ancho_tablero)] for _ in range(alto_tablero)]
        self.jugadores = []
        self.game_over = False

    def __str__(self):
        # Dibuja el tablero con los jugadores en él.
        # Creamos una copia para no modificar el original al dibujar.
        tablero_a_mostrar = [row[:] for row in self.tablero]
        for i, jugador in enumerate(self.jugadores):
            x, y = jugador.posicion
            if 0 <= x < self.ancho_tablero and 0 <= y < self.alto_tablero:
                tablero_a_mostrar[y][x] = f"P{i+1}"

        # Unimos las filas para crear el string del tablero
        return "\n".join([" ".join(row) for row in tablero_a_mostrar])

    def iniciar_juego(self):
        """Prepara el juego, creando y colocando a los jugadores."""
        jugador1 = Player("Jugador 1")
        jugador2 = Player("Jugador 2")

        # Colocamos a los jugadores en posiciones aleatorias
        jugador1.posicion = (random.randint(0, self.ancho_tablero-1), random.randint(0, self.alto_tablero-1))

        while True:
            pos2 = (random.randint(0, self.ancho_tablero-1), random.randint(0, self.alto_tablero-1))
            if pos2 != jugador1.posicion:
                jugador2.posicion = pos2
                break

        self.jugadores = [jugador1, jugador2]
        print("Estado inicial de los jugadores:")
        print(self.jugadores[0])
        print(self.jugadores[1])

    def hay_ganador(self):
        """Comprueba si algún jugador ha ganado."""
        for i, jugador in enumerate(self.jugadores):
            if jugador.vida <= 0:
                # El otro jugador es el ganador
                ganador = self.jugadores[1-i]
                print("-" * 40)
                print(f"¡El juego ha terminado! {jugador.nombre} ha sido eliminado.")
                print(f"¡El ganador es {ganador.nombre}!")
                print("-" * 40)
                self.game_over = True
                return True
        return False

    def jugar(self):
        """Inicia y gestiona el bucle principal del juego."""
        turno = 0
        while not self.game_over:
            jugador_actual = self.jugadores[turno % 2]
            oponente = self.jugadores[(turno + 1) % 2]

            print("\n" + "="*40)
            print(f"Turno de: {jugador_actual.nombre}")
            print(self) # Muestra el tablero
            print(f"Estado: {jugador_actual}")
            print(f"Oponente: {oponente}")
            print("Acciones: [d]isparar, [m]over (w/a/s/d), [r]ecargar")

            accion = input("Elige tu acción: ").lower()

            if accion == 'd':
                jugador_actual.disparar(oponente)
            elif accion == 'r':
                jugador_actual.recargar()
            elif accion == 'm':
                direccion = input("Elige la dirección (w/a/s/d): ").lower()
                if direccion in ['w', 'a', 's', 'd']:
                    jugador_actual.moverse(direccion, self.ancho_tablero, self.alto_tablero)
                else:
                    print("Dirección inválida.")
            else:
                print("Acción no válida. Pierdes el turno.")

            if self.hay_ganador():
                break

            turno += 1

# --- Bloque principal para iniciar el juego ---
if __name__ == "__main__":
    print("¡Bienvenido al Juego de Paintball en Python!")
    print("-" * 40)

    juego = Game()
    juego.iniciar_juego()
    juego.jugar()
