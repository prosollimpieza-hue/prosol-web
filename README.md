# Sitio web de Prosol

Sitio de [limpieza-prosol.com.ar](https://limpieza-prosol.com.ar), la empresa de limpieza de Prosol (Pronto SRL) en San Miguel de Tucumán.

HTML estático, sin compilación. Netlify publica la carpeta `sitio/` cada vez que hay cambios en la rama `main` de GitHub.

## Estructura

```
sitio/
  index.html                                  inicio
  limpieza-de-oficinas-tucuman/index.html     servicio
  limpieza-de-locales-y-galerias-tucuman/     servicio
  limpieza-final-de-obra-tucuman/             servicio
  trabaja-con-nosotros/index.html             empleo (formulario de Netlify Forms con CV)
  404.html                                    página de error
  images/                                     fotos y logos (images/trabajos/ = fotos reales de trabajos)
  sitemap.xml, robots.txt, og-image.jpg, favicon.png
netlify.toml                                  configuración de Netlify (carpeta publicada, cabeceras)
```

## Cómo hacer cambios

1. Editar los archivos de `sitio/`.
2. Abrir `sitio/index.html` en el navegador para revisar (las rutas que empiezan con `/` se ven bien solo
   con un servidor: `npx serve sitio`).
3. Hacer commit y subir a `main`: Netlify publica solo en un par de minutos.

Cada subida a `main` es una publicación en Netlify y gasta créditos: juntar los cambios y subirlos de una vez.
Para probar sin publicar, trabajar en otra rama y unirla a `main` cuando esté lista.

## Reglas

- Paleta y tipografías: naranja `#D4571C` solo decorativo o grande; texto chico naranja `#a03d17` sobre fondo claro
  y `#E8854A` sobre fondo oscuro; botones `#b8461a`. Playfair Display (títulos) e Inter (texto).
- Nada de guiones largos (—) en los textos.
- Imágenes siempre como archivo en `images/`, nunca en base64, con `width`, `height` y `alt` descriptivo.
- Las imágenes quedan guardadas 30 días en el navegador de cada visitante: si se reemplaza una foto, usar un nombre nuevo.
- Al cambiar una página, actualizar su `<lastmod>` en `sitemap.xml`.
- Fotos de trabajos: solo las aprobadas por Lourdes, sin logos ni nombres de clientes.
