# 🚀 Pecibalto: Universal Media Extractor

## 📝 Descripción
Este proyecto es una potente herramienta de escritorio creada al 100% en Python con **Tkinter**, diseñada para ser un extractor universal de medios. El flujo es fluido: pegas un enlace de redes sociales (YouTube, X, Instagram), presionas "Encontrar" para previsualizar la miniatura y el nombre, y el botón se transforma automáticamente en "Descargar".

Al descargar, el programa utiliza `yt-dlp` para obtener el archivo multimedia, mostrando una barra de progreso en tiempo real. La aplicación sigue una arquitectura basada en el principio **SRP** (Responsabilidad Única), separando la interfaz de los servicios de extracción y la gestión de hilos.

## 📂 Estructura del Proyecto
*   **/ui**: `main_window.py` (Layout) y `components.py` (Widgets).
*   **/services**: `extractor_service.py` (yt-dlp) e `image_service.py` (Pillow).
*   **/utils**: `thread_manager.py` (Manejo de hilos).

## 🛠 Checklist de Features

| Feature | Descripción Técnica | Estado |
| :--- | :--- | :--- |
| **1. Botón Mutante** | Toggle visual de texto y comando en el botón principal. | [ ] No hecha |
| **2. Pre-fetch** | Obtención de metadatos vía `extract_info` (download=False). | [ ] No hecha |
| **3. Renderizado** | Procesamiento de miniatura con Pillow para mostrar en UI. | [ ] No hecha |
| **4. Hilos** | Ejecución asíncrona para evitar congelamiento de la ventana. | [ ] No hecha |
| **5. Formatos** | Selector (Combobox) para alternar entre perfiles MP3 y MP4. | [ ] No hecha |
| **6. Hook Progreso** | Interceptor de señales de `yt-dlp` para la Progressbar. | [ ] No hecha |
| **7. Validador** | Validación previa de URLs mediante expresiones regulares. | [ ] No hecha |
| **8. Ruta Destino** | Selección dinámica de carpeta con `filedialog.askdirectory`. | [ ] No hecha |
| **9. Logs Errores** | Sistema de alertas visuales (`messagebox`) para fallos. | [ ] No hecha |
| **10. Reset UI** | Función `reset_app` que limpia la interfaz tras éxito. | [ ] No hecha |

## Los commits hechos del laboratorio informatica 1 son hechos por Juan33-Felipe
 Los commits hechos antes se hicieron con el usuario de Juan felipe pero quien los hizo fue Edgar Arteaga