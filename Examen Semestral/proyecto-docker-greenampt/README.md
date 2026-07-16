# Despliegue Green-Ampt + Menú — examen507.site

## 1. En tu VPS
```bash
docker network create proxy
unzip proyecto.zip -d proyecto
cd proyecto
docker compose up -d --build
```

## 2. DNS (en Namecheap, donde está examen507.site)
Crea registros tipo A apuntando a la IP pública del VPS:
| Tipo | Host        | Valor (IP VPS) |
|------|-------------|-----------------|
| A    | @           | tu.ip.publica   |
| A    | www         | tu.ip.publica   |
| A    | greenampt   | tu.ip.publica   |

## 3. Nginx Proxy Manager
- Abre `http://TU_IP:81` (usuario/clave por defecto: admin@example.com / changeme — cámbiala).
- Crea los 2 Proxy Hosts indicados en `CONFIG_NGINX_PROXY_MANAGER.txt`.
- En cada uno, pestaña SSL → "Request a new SSL Certificate" → Force SSL + HTTP/2.

## 4. Resultado
- https://examen507.site        → Carátula / menú con los 4 proyectos (solo Green-Ampt activo)
- https://greenampt.examen507.site → Proyecto Green-Ampt funcionando, con candado 🔒

## Notas
- El código de Green-Ampt no se tocó, solo se agregó `Dockerfile`, `start.sh`
  y se ajustó `rxconfig.py` para tomar el dominio desde la variable `API_URL`.
- Cuando tengas listos los otros 3 proyectos, repite el mismo patrón:
  carpeta propia + Dockerfile + un Proxy Host nuevo en NPM, y solo
  actualizas el link en `menu/index.html`.
