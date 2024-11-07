# Sign Language Live Translator

Un sistema de traducción en tiempo real de lenguaje de señas utilizando visión por computadora y procesamiento de video.

## 🚀 Descripción

**Sign Language Live Translator** es una aplicación web que permite la transmisión en vivo y el procesamiento de video para traducir gestos de lenguaje de señas. La herramienta utiliza visión por computadora para ofrecer una solución accesible y eficiente para la comunicación con personas sordas, permitiendo la traducción de la Lengua de Señas Ecuatoriana (LSEC) a texto en tiempo real.

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal de desarrollo.
- **Flask**: Framework web utilizado en el backend.
- **HTML/CSS**: Estructura y estilo de la interfaz.
- **Bootstrap 5**: Framework CSS para diseño responsivo.
- **MediaPipe**: Biblioteca de Machine Learning para detección de gestos.
- **OpenCV**: Procesamiento de video y visión por computadora.

## 📋 Requisitos Previos

Instalación de dependencias principales:

```bash
python -m pip install -r requirements.txt
```

Dependencias incluidas:

- `Flask>=2.0.1`
- `opencv-python>=4.5.3`
- `mediapipe>=0.8.9`
- `numpy>=1.21.0`

## 🚀 Instalación y Uso

1. **Clonar el repositorio:**

    ```bash
    git clone https://github.com/yourusername/sign-language-live-translator.git
    cd sign-language-live-translator
    ```

2. **Crear y activar entorno virtual:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows: venv\Scripts\activate
    ```

3. **Instalar dependencias:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Ejecutar la aplicación:**

    ```bash
    python app.py
    ```

5. **Abrir en el navegador:**

    Visita [http://localhost:5000](http://localhost:5000) para acceder a la aplicación.

## 🔧 Características

- ✅ Transmisión de video en tiempo real.
- ✅ Detección y reconocimiento de gestos con MediaPipe.
- ✅ Interfaz web responsiva y amigable.
- ✅ Procesamiento de video rápido y eficiente.
- ✅ Modo pantalla completa.
- ✅ Diseño moderno, inclusivo y accesible.

## 📁 Estructura del Proyecto

```plaintext
sign-language-live-translator/
├── requirements.txt        # Dependencias del proyecto
├── templates/              # Plantillas HTML
│   └── index.html          # Página principal
├── app.py                  # Aplicación principal con Flask
└── README.md               # Documentación del proyecto
```

## 👥 Desarrolladores

- Byron Ormaza Farias
- Jordan Zambrano

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE.md para obtener más detalles.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Para realizar cambios importantes:

1. Haz un fork del repositorio.
2. Crea una rama para tu función: `git checkout -b feature/NuevaCaracterística`.
3. Realiza el commit de tus cambios: `git commit -m 'Add: Nueva característica'`.
4. Haz push a la rama: `git push origin feature/NuevaCaracterística`.
5. Abre un Pull Request para revisión.

## 📞 Contacto

Proyecto: [https://github.com/yourusername/sign-language-live-translator](https://github.com/yourusername/sign-language-live-translator)  
LinkedIn: [Tu perfil de LinkedIn]  
Email: bjormaza@espe.edu.ec - ormazafariasbyron@gmail.com
