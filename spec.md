# Specification: DDM Desktop MVP

## 1. Resumen Ejecutivo
Construir una versión jugable de escritorio de "Dungeon Dice Monsters" donde dos jugadores humanos puedan competir en la misma computadora (Hotseat Multiplayer). El foco estará en la correcta implementación de la mecánica de "Dimensionar", movimiento y un sistema de combate básico basado en gestión de recursos (Crestas).

## 2. Historias de Usuario (User Stories)

### Configuración de Partida
* Como jugador, quiero iniciar una partida nueva con una reserva (Dice Pool) predefinida de monstruos.
* Como jugador, quiero ver el tablero de 13x19 vacío, salvo por los dos "Dungeon Masters" (DM) en extremos opuestos.

### Fase de Dados (Roll Phase)
* Como jugador, quiero seleccionar 3 dados de mi reserva y "lanzarlos".
* Quiero ver el resultado de las caras (Invocación, Movimiento, Ataque, Defensa, Magia, Trampa).
* Si obtengo invocaciones ("Summon Crests"), quiero poder decidir si "Dimensionar" un monstruo.

### Fase de Dimensionar (The Core Mechanic)
* Como jugador, al invocar, quiero ver el patrón de despliegue sobre el tablero.
* El sistema debe permitirme rotar e invertir el patrón.
* **Validación Crítica:** El sistema debe impedir colocar el patrón si se superpone o no conecta con mi territorio existente.
* **Selección de Patrón:** El sistema debe permitir al jugador elegir entre diferentes formas de despliegue válidas (6 casillas) antes de colocarlo.
* Al confirmar, el patrón se convierte en terreno y el monstruo aparece.

### Fase de Acción y Movimiento
* El sistema debe acumular las "Crestas" obtenidas.
* Como jugador, quiero gastar **Crestas de Movimiento** para desplazar un monstruo por casillas válidas.

### Fase de Combate Básico
* Como jugador, quiero declarar un ataque a un monstruo enemigo adyacente gastando una **Cresta de Ataque**.
* El sistema debe preguntar al defensor si desea gastar una **Cresta de Defensa**.
* **Cálculo de Daño:**
    * Si el defensor paga defensa: `Daño = Atacante.ATK - Defensor.DEF`.
    * Si el defensor NO paga (o no tiene): `Daño = Atacante.ATK`.
* **Resolución:** El sistema resta el daño a los HP del defensor. Si HP <= 0, la figura del monstruo se elimina del tablero, pero su camino (dado desplegado) permanece.

## 3. Requerimientos Funcionales (Backend Logic)
* **Grid System:** Matriz de datos que gestiona propiedad de casillas.
* **Dice Parser:** Definición de dados y patrones (JSON/Dicts). **Nota:** Todo dado desplegado ("Unfold") debe ocupar exactamente 6 casillas conectadas.
* **Resource Manager:** Sistema contable para sumar y restar Crestas por jugador.
* **Combat Engine:** Función pura que recibe (Atacante, Defensor, Bool:DefensaPagada) y retorna el nuevo estado de HP.
* **Turn Manager:** Control de estados y turnos.

## 4. UI/UX
- **HUD**:
    - "Roll Dice" and "Summon" buttons stacked vertically bottom-left.
    - "End Turn" button bottom-right.
    - **Monster Cards**: Row of 5 clickable cards at bottom-center.
        - Display: Name, Level, Type, HP, Attack, Defense, Description.
        - Interaction: Click to select monster for summoning.
- **Crest Counter**: Displays current crest resources.
- **Action Log**: Scrolling text log of game events.

## 5. Requerimientos de UI (Ursina)
* **Cámara:** Vista isométrica/cenital.
* **Interacción:** Clic para seleccionar, mover y atacar.
* **HUD:** Panel con Stats y contadores de Crestas.
* **Feedback de Combate:** Mostrar visualmente el cambio de HP (ej. barra de vida o texto flotante "-500").
* **Control de Cámara:** Interfaz UI para mover, rotar y hacer zoom sobre el tablero, con restricciones de límites.

## 5. Fuera del Alcance (Out of Scope) para v1.0
* Multijugador en red (Online).
* IA contra la computadora.
* Editor de mazos (Deck Builder).
* Habilidades especiales de monstruos (Efectos de Magia/Trampa complejos).
* Animaciones cinemáticas de batalla.