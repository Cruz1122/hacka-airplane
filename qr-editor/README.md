# Editor QR · Los Nevados

Esta aplicación web prepara fichas de conocimiento para la Guía Los Nevados. Genera un PNG y el texto del QR en el navegador.

## Ejecutar

Desde `qr-editor/`:

```powershell
npm ci
npm run dev
```

Abre la URL que muestra Vite. `npm run build` genera `dist/`, que se puede servir desde un servidor HTTP local sin internet. La instalación inicial de dependencias requiere acceso al registro de npm.

## Agregar, reemplazar y retirar

1. Para una ficha nueva, escribe un título y la respuesta principal. **Sugerir preguntas y variantes** prepara el ID, preguntas de búsqueda y una variante editable basada en tu propio texto. Para reemplazar una ficha existente, búscala en el catálogo o conserva su ID.
2. Completa las variantes y las ampliaciones para «sigue» y «por qué». Puedes incluir pasos, fuentes HTTPS y los IDs de otras fichas relacionadas.
3. Pulsa **Generar QR**. Cada QR contiene un cambio y admite hasta 1500 bytes de texto UTF-8. La pantalla muestra el tamaño del código.
4. En la guía, toca **Actualízame · Escanea el QR**. Escanea la pantalla, elige el PNG o pega el código. Revisa la ficha y confirma.
5. Para quitar una ficha, selecciona **Quitar ficha** y genera un QR con su mismo ID. Una revisión aplicada no puede ser reemplazada por una revisión anterior. Escanea únicamente códigos entregados por una fuente de confianza.

El dispositivo genera los embeddings de las preguntas con su modelo e5 local. Guarda la ficha y sus vectores con SQLite en Android e iOS o con el almacenamiento local del navegador. Las fichas de emergencia y la sección de seguridad las mantiene la versión instalada de la guía.

