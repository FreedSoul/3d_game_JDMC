¡Excelente\! Con el `spec.md` aprobado, ahora actuamos como el "Arquitecto de Software".

El paso 3 es el **`plan.md`**. Aquí traducimos los requisitos humanos a un **plano técnico detallado**.

Este plan define la estructura de carpetas, las clases principales y el flujo de datos. He diseñado esto asegurándome de que el `core` (lógica) no sepa nada sobre `ursina` (visuales), cumpliendo nuestra Constitución.

-----

### Archivo: `plan.md`

````markdown
# Implementation Plan: DDM Desktop MVP

## 1. Arquitectura del Proyecto
Seguiremos una arquitectura **Hexagonal (Ports & Adapters)** simplificada.
* **Core:** Contiene toda la lógica del juego. Python puro. Sin dependencias externas.
* **Adapters:** Ursina Engine actúa como el adaptador de interfaz para mostrar el estado y capturar inputs.

### Estructura de Carpetas
```text
ddm-game/
├── data/                   # Archivos JSON (Monstruos, Dados)
├── tests/                  # Unit tests (pytest)
├── src/
│   ├── core/               # Lógica Pura (The Brain)
│   │   ├── __init__.py
│   │   ├── constants.py    # Dimensiones (13x19), Fases
│   │   ├── dataclasses.py  # Monster, DieFace, PlayerState
│   │   ├── grid.py         # Lógica del Tablero (Graph/Matrix)
│   │   ├── patterns.py     # Lógica de rotación de "Tetris shapes"
│   │   └── engine.py       # Clase principal GameController
│   ├── ui/                 # Ursina Implementation (The Skin)
│   │   ├── __init__.py
│   │   ├── main.py         # Entry point (App)
│   │   ├── board_view.py   # Renderizado del grid 3D
│   │   ├── pieces.py       # Prefabs de Monstruos/Dados
│   │   └── hud.py          # Interfaz 2D (Botones, Stats)
│   └── main.py             # Launcher
└── requirements.txt
````

## 2\. Modelado de Datos (Core)

### `src/core/dataclasses.py`

Usaremos `pydantic` o `dataclasses` estándar.

  * **DieFace:** `type: Enum (SUMMON, MOVE, ATK...)`, `value: int`.
  * **Pattern:** Lista de coordenadas relativas `[(0,0), (1,0), (0,1)]` para representar la forma del dado desplegado.
  * **Monster:** `name`, `level`, `hp`, `atk`, `def`, `pattern`.
  * **Cell:** `owner_id` (quién puso el dado), `creature_ref` (si hay alguien encima).

### `src/core/grid.py`

  * Clase `Grid`: Mantiene una matriz de `13x19`.
  * Método `validate_dimension(pattern, origin_x, origin_y, player_id)`:
    1.  Verifica colisiones (¿está ocupado?).
    2.  Verifica adyacencia (¿toca una pieza mía?).
    3.  Retorna `True/False`.

### `src/core/engine.py`

  * Clase `GameEngine`: Máquina de estados.
  * Atributos: `turn_count`, `current_player`, `players_crests`.
  * Métodos: `roll_dice()`, `execute_dimension()`, `execute_move()`, `execute_attack()`.

## 3\. Integración con Ursina (UI)

### `src/ui/board_view.py`

  * Generará 13x19 entidades `Entity(model='quad')`.
  * Mapeará coordenadas `(x, y)` lógicas a posiciones `(x, z)` en el mundo 3D.
  * **Event System:** Cuando el usuario hace clic en una celda, llama a `engine.handle_click(x, y)`.

### `src/ui/camera_controls.py`

  * Botones en pantalla para mover la cámara (Pan/Zoom/Rotar).
  * Lógica de restricciones (Clamping) para no perder el tablero de vista.

### `src/ui/hud.py`

  * Botones para acciones: "End Turn", "Roll Dice".
  * Textos dinámicos para HP y Crestas.

## 4\. Fases de Implementación (Roadmap)

### Fase 1: Core Foundation & Tests (Sin Gráficos)

1.  Definir estructuras de datos (`Monster`, `Die`).
2.  Implementar lógica del `Grid` y validación de `Patterns` (rotación/colocación).
3.  Implementar contabilidad de `Crests`.
4.  Escribir tests unitarios para verificar que no se pueden poner dados ilegales.

### Fase 2: Visualización Básica

1.  Configurar ventana de Ursina.
2.  Renderizar el tablero vacío.
3.  Renderizar a los dos Dungeon Masters (DM) en sus posiciones iniciales.

### Fase 3: Mecánica de Dimensionar (El Reto Técnico)

1.  UI para seleccionar dado y mostrar "fantasma" del patrón sobre el tablero.
2.  Controles para rotar el patrón con teclado/UI.
3.  Conectar el clic de confirmación con `engine.execute_dimension()`.
4.  Actualizar el color del tablero visualmente.

### Fase 4: Movimiento y Combate

1.  Pathfinding básico (o validación de distancia) para movimiento.
2.  Implementar `execute_attack()` en el engine.
3.  Actualizar HUD con los nuevos valores de HP/Crestas.

## 5\. Datos Iniciales (JSON)

Crearemos un `monsters.json` con 3 monstruos básicos para pruebas:

  * *Knight of Twin Swords* (Nivel 1, Patrón simple).
  * *Blast Lizard* (Nivel 2, Patrón medio).
  * *Dark Magician* (Nivel 4, Patrón complejo).

<!-- end list -->

```

***

### Detalle importante sobre la "Validación de Adyacencia"
En el plan he especificado que el `Grid` debe verificar la adyacencia. Esto es crucial. En DDM, solo puedes expandir tu territorio si el nuevo dado toca uno de tus dados anteriores. El algoritmo será:
1.  Tomar todas las coordenadas del nuevo patrón propuesto.
2.  Revisar sus vecinos (arriba, abajo, izq, der).
3.  Al menos uno de esos vecinos debe pertenecer al `player_id`.

```