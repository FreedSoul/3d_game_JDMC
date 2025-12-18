# Tasks: DDM Desktop MVP

## Phase 1: Core Logic Foundation (Python Pure)
- [ ] **Task 1.1:** Inicializar estructura del proyecto (`src/core`, `src/ui`, `tests`) y crear `requirements.txt`.
- [ ] **Task 1.2:** Implementar `dataclasses.py`: Definir `DieFace`, `Monster`, `PlayerState` y `Pattern` (usando listas de tuplas para la forma).
- [ ] **Task 1.3:** Implementar `grid.py`: Crear la clase `Grid` (13x19) y métodos básicos `get_cell`, `set_cell`.
- [ ] **Task 1.4:** Implementar lógica de validación de despliegue en `grid.py`:
    - [ ] Algoritmo de rotación de patrones (90 grados).
    - [ ] Verificación de colisión (¿celda ocupada?).
    - [ ] Verificación de adyacencia (¿conecta con mi territorio?).
- [ ] **Task 1.5:** Implementar `engine.py`: Gestión básica de turnos y contadores de crestas.
- [ ] **Task 1.6:** Crear `tests/test_core.py` para validar la lógica de adyacencia y rotación sin abrir ninguna ventana gráfica.

## Phase 2: Basic Visuals (Ursina Setup)
- [ ] **Task 2.1:** Configurar `src/main.py` y levantar una ventana de Ursina vacía.
- [ ] **Task 2.2:** Crear `board_view.py`: Generar la grilla visual 13x19. Cada celda debe tener referencia a su coordenada `(x,y)`.
- [ ] **Task 2.3:** Implementar cámara isométrica o cenital fija pero centrada en el tablero.
- [ ] **Task 2.4:** Renderizar a los "Dungeon Masters" iniciales en las posiciones correctas (extremos del tablero).

## Phase 3: The "Dimension" Mechanic
- [ ] **Task 3.1:** Crear UI temporal para "Lanzar Dados" (botón simple que genere resultados aleatorios en consola/debug).
- [ ] **Task 3.2:** Implementar el "Modo Construcción": Al seleccionar una invocación, mostrar un "Fantasma" del patrón del dado sobre el tablero (hover).
- [ ] **Task 3.3:** Añadir input (teclas R/T o UI) para rotar el patrón fantasma visualmente.
- [ ] **Task 3.4:** Conectar clic del ratón -> Validación del Core -> Actualización visual (pintar las celdas del color del jugador).

## Phase 4: Movement & Combat
- [ ] **Task 4.1:** Sistema de Selección: Clic en un monstruo -> Resaltar celdas válidas de movimiento (Pathfinding simple: distancia Manhattan basada en casillas desplegadas).
- [ ] **Task 4.2:** Ejecutar Movimiento: Actualizar posición en `Core` y mover entidad en `Ursina`. Restar cresta de movimiento.
- [ ] **Task 4.3:** Combate Básico: Clic en enemigo adyacente -> Calcular daño -> Restar HP.
- [ ] **Task 4.4:** Eliminar pieza visual si HP <= 0.

## Phase 5: Polish & Packaging
- [ ] **Task 5.1:** Implementar HUD simple (Texto, Botón End Turn).
- [ ] **Task 5.2:** Implementar UI de Control de Cámara (Pan, Zoom, Rotate con límites).
- [ ] **Task 5.3:** Cargar datos de 3 monstruos reales desde `data/monsters.json`.

## Phase 6: Monster Cards & Advanced UI
- [x] **Task 6.1:** Refactor HUD: Replace Summon Button with Card Hover Options.
    - [x] **Polish:** Replaced "Roll Dice" text with custom PNG icon.
- [x] **Task 6.2:** Create `MonsterCard` Component: Visuals & Interactions (Hover/Click).
- [x] **Task 6.3:** Implement Hand View: Display 5 Monster Cards.
- [x] **Task 6.4:** Implement Effects System (`src/core/effects.py`).
- [x] **Task 6.5:** Load Crystal Golem data and texture using relative paths.
- [x] **Task 6.6:** Integrate Card Selection with Summoning Logic (Hover -> Summon -> Patterns).
