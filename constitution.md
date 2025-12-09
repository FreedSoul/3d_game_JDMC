# Project Constitution: Dungeon Dice Monsters (DDM) Engine

## 1. Visión del Proyecto
Crear una implementación digital fiel, robusta y escalable del juego de mesa "Dungeon Dice Monsters". El sistema debe priorizar la integridad de las reglas del juego (Game Loop). Inicialmente, el proyecto se enfocará en una aplicación de **Escritorio** independiente, manteniendo la lógica desacoplada para permitir portabilidad futura.

## 2. Principios de Arquitectura (Non-Negotiables)
* **Separación de Intereses (SoC):** La lógica del juego (`Core Domain`) debe ser completamente independiente de la interfaz visual (`Ursina App`). El motor del juego no debe depender de clases de Ursina.
* **Source of Truth:** El `GameState` es inmutable y es la única fuente de verdad. La UI de Ursina debe reaccionar a los cambios en este estado, no almacenarlo.
* **Validación Estricta:** Ningún movimiento ilegal puede corromper el estado. Todas las acciones (Mover, Atacar, Dimensionar) deben ser validadas por el motor antes de reflejarse visualmente.
* **Modelado de Dominio:** Usaremos terminología oficial en el código (`Crest`, `DicePool`, `Dimensioning`, `DungeonMaster`).

## 3. Stack Tecnológico
* **Lenguaje (Core & UI):** Python 3.12+.
* **Motor Gráfico (UI):** **Ursina Engine**. Se utilizará para renderizar el tablero 13x19, los dados desplegados y las figuras en un entorno de escritorio.
* **Empaquetado y Distribución:** El proyecto debe estructurarse de tal manera que sea compatible con herramientas de compilación (como `PyInstaller` o `Nuitka`) para generar un ejecutable (.exe / binary) standalone. Evitar dependencias que rompan la compilación estática.
* **Type Hinting:** Uso estricto de `typing` (y Pydantic para validación de datos) para asegurar la integridad de las estructuras.
* **Testing:** `pytest` es obligatorio para la lógica del núcleo (sin depender de la ventana gráfica de Ursina).

## 4. Estilo de Código y Convenciones
* **Idioma:** El código, variables y comentarios deben estar en **Inglés**.
* **Documentación:** Docstrings obligatorios para todas las funciones públicas.
* **Manejo de Errores:** No fallar silenciosamente. Usar excepciones personalizadas (ej. `InsufficientCrestsError`, `InvalidPlacementError`, `InvalidDiceType`, `InvalidDiceValue`).

## 5. Reglas Específicas del Dominio (DDM)
* **Tablero:** Grid de 13x19 casillas.
* **Dados:** Un dado tiene 6 caras con Tipos y Niveles.
* **Despliegue (Dimension):** Un dado desplegado se convierte en geometría del nivel (Entity en Ursina). La conectividad lógica es prioritaria sobre la colisión física.