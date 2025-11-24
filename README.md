# Plataforma de despliegue escalable de la aplicación BookInfo (Docker, Docker Compose y Kubernetes)

Este repositorio recoge el desarrollo completo de una práctica de **despliegue de aplicaciones escalables en la nube**, realizada en colaboración con la **Universidad Politécnica de Madrid (UPM)**.

El trabajo integra en un único proyecto:

- Despliegue de una **aplicación monolítica** en máquina virtual.
- Contenerización del monolito con **Docker**.
- Transformación de la aplicación en una arquitectura de **microservicios poliglota**, orquestados con **Docker Compose**.
- Despliegue final de la aplicación basada en microservicios sobre **Kubernetes**, con réplicas, versiones y balanceo de carga.

La aplicación de referencia es **BookInfo**, una web que muestra información, valoraciones y reseñas de libros.

---

## Objetivos del proyecto

- Consolidar conceptos de **DevOps**, **contenedores** y **orquestación**.
- Comparar el despliegue monolítico frente a una arquitectura de **microservicios**.
- Manejar una aplicación **políglota** (Python, Ruby, Node.js, Java Liberty).
- Practicar el despliegue de aplicaciones en **Docker**, **Docker Compose** y **Kubernetes**.
- Automatizar tareas de instalación, configuración y arranque con **scripts en Python**.

---

## Arquitectura global

La aplicación BookInfo se despliega en dos enfoques:

### 1. Monolito

Una única aplicación Python (`productpage_monolith.py`) que sirve toda la lógica en un solo proceso.

### 2. Microservicios

La aplicación se descompone en cuatro servicios:

- **productpage** – Frontend en **Python**.
- **details** – Servicio de detalles en **Ruby**.
- **ratings** – Servicio de valoraciones en **Node.js**.
- **reviews** – Servicio de reseñas en **Java (WebSphere Liberty)**, con tres versiones:
  - `v1`: reseñas sin estrellas.
  - `v2`: reseñas con estrellas negras.
  - `v3`: reseñas con estrellas rojas.

Los servicios se comunican entre sí por HTTP sobre el puerto **9080**.

---

## Estructura del repositorio

```text
.
├── Parte1/
│   └── maquinavirtualpesada.py        # Script Python para despliegue monolítico automatizado
│
├── Parte2/
│   └── Dockerfile                     # Imagen Docker para la versión monolítica
│
├── Parte3/
│   ├── details/
│   │   └── Dockerfile                 # Imagen Docker del microservicio details (Ruby)
│   ├── productpage/
│   │   └── Dockerfile                 # Imagen Docker del microservicio productpage (Python)
│   ├── ratings/
│   │   └── Dockerfile                 # Imagen Docker del microservicio ratings (Node.js)
│   ├── reviews/
│   │   └── Dockerfile                 # Imagen Docker del microservicio reviews (Java Liberty)
│   └── src/
│       └── docker-compose.yaml        # Orquestación de microservicios con Docker Compose
│
└── Parte4/
    ├── kube/
    │   ├── details.yaml               # Service + Deployment para details
    │   ├── productpage.yaml           # Service (LoadBalancer) + Deployment para productpage
    │   ├── ratings.yaml               # Service + Deployment para ratings
    │   ├── reviews-svc.yaml           # Service para reviews
    │   ├── reviews-v1-deployment.yaml # Deployment reviews v1
    │   ├── reviews-v2-deployment.yaml # Deployment reviews v2
    │   └── reviews-v3-deployment.yaml # Deployment reviews v3
    │
    └── src/
        ├── details/
        │   └── Dockerfile             # Imagen details para entorno Kubernetes
        ├── productpage/
        │   └── Dockerfile             # Imagen productpage para entorno Kubernetes
        ├── ratings/
        │   └── Dockerfile             # Imagen ratings para entorno Kubernetes
        └── reviews/
            ├── reviews-wlpcfg/        # Configuración y artefactos del servicio reviews
            └── docker-compose.yaml    # Variante avanzada con varias versiones de reviews
```

---

## Requisitos previos

### Entorno general

- Linux (o WSL2) con:
  - `git`
  - `python3` y `pip3`
  - `docker` y `docker-compose`
- Acceso a un cluster de **Kubernetes** (Minikube, Kind, GKE, etc.) y `kubectl` instalado.

### Para la Parte 1

- Máquina virtual Linux con:
  - Acceso a Internet.
  - Permisos para ejecutar `apt-get` y `pip3`.

### Para la Parte 4

- Cluster Kubernetes funcional.
- Acceso a las imágenes Docker construidas localmente o publicadas en un registry.

---

## 1️. Parte 1 – Despliegue monolítico automatizado (maquinavirtualpesada.py)

Script: `Parte1/maquinavirtualpesada.py`

Esta parte automatiza el despliegue de la aplicación monolítica BookInfo en una máquina virtual:

1. **Clona** el repositorio original de la práctica:
   ```python
   url_del_repositorio = 'https://github.com/CDPS-ETSIT/practica_creativa2.git'
   ```
2. **Instala dependencias** del sistema y de Python a partir de `requirements.txt`.
3. Define la variable de entorno `GRUPO_NUMERO` (nombre o identificador del grupo).
4. **Modifica automáticamente** el código de `productpage_monolith.py` para:
   - Leer `GRUPO_NUMERO`.
   - Añadir el nombre del grupo al título de la página.
5. **Arranca la aplicación en dos puertos simultáneos** (por ejemplo 9080 y 9081) usando `multiprocessing`.

### Ejecución

Dentro de `Parte1/`:

```bash
python3 maquinavirtualpesada.py
```

El script:

- Clonará el repositorio `practica_creativa2` (si no existe).
- Instalará las dependencias.
- Modificará el código.
- Lanzará la aplicación monolítica en los puertos configurados (por defecto `[9080, 9081]`).

La URL de acceso típica será:

```text
http://<ip_maquina_virtual>:9080/productpage
```

---

## 2️. Parte 2 – Contenerización del monolito con Docker

Fichero: `Parte2/Dockerfile`

Objetivo: ejecutar la aplicación monolítica dentro de un **contenedor Docker**.

El Dockerfile:

- Usa como base `python:3.8.10`.
- Actualiza paquetes e instala `python3-pip`.
- Copia el código de `productpage_monolith.py` y sus dependencias.
- Instala los requisitos de `requirements.txt`.
- Expone el puerto `9080`.
- Arranca la aplicación con:
  ```bash
  python3 productpage_monolith.py 9080
  ```

### Construcción de la imagen

Desde la raíz del repositorio (ajustando el contexto si es necesario):

```bash
docker build -t bookinfo-monolith:latest -f Parte2/Dockerfile .
```

### Ejecución del contenedor

```bash
docker run --name bookinfo-monolith -p 9080:9080 -d bookinfo-monolith:latest
```

Acceso:

```text
http://localhost:9080/productpage
```

---

## 3️. Parte 3 – Arquitectura de microservicios con Docker Compose

En esta parte se descompone el monolito en cuatro microservicios y se orquestan con **Docker Compose**.

### Dockerfiles de cada microservicio

- `Parte3/productpage/Dockerfile`  
  - Base: `python:3.8.10`
  - Instala dependencias y ejecuta `productpage.py`.

- `Parte3/details/Dockerfile`  
  - Base: `ruby:2.7.1-slim`
  - Copia `details.rb`.
  - Define variables de entorno `SERVICE_VERSION=v1` y `ENABLE_EXTERNAL_BOOK_SERVICE=true`.
  - Expone `9080`.

- `Parte3/ratings/Dockerfile`  
  - Base: `node:12.18.1-slim`
  - Copia `package.json` y `ratings.js`.
  - Instala dependencias con `npm install`.
  - Define `SERVICE_VERSION=v1`.

- `Parte3/reviews/Dockerfile`  
  - Base: `websphere-liberty:20.0.0.6-full-java8-ibmjava`.
  - Copia la configuración de Liberty.
  - Configura variables de entorno:
    - `SERVICE_VERSION` (v1, v2 o v3).
    - `ENABLE_RATINGS` (true/false).
    - `STAR_COLOR` (black, red, etc.).

### Orquestación con docker-compose

Fichero: `Parte3/src/docker-compose.yaml`

Define los servicios:

- `productpage`
- `details`
- `ratings`
- `reviews` (versión v1 activada por defecto; v2 y v3 comentadas)

Cada servicio utiliza su imagen `34/<nombre_servicio>` (puede adaptarse al nombre de tu grupo) y expone el puerto 9080 donde corresponde. También se definen **volúmenes** para persistencia y facilidad de desarrollo.

### Ejecución con Docker Compose

Desde `Parte3/src/`:

```bash
docker-compose up --build
```

Esto:

- Construye las imágenes de cada microservicio (si no existen).
- Levanta los contenedores conectados en la misma red.
- Expone la aplicación en:

```text
http://localhost:9080/productpage
```

Para probar distintas versiones de **reviews**, se puede:

- Comentar / descomentar las secciones correspondientes en `docker-compose.yaml`.
- Volver a lanzar:

```bash
docker-compose up -d --build
```

---

## 4️. Parte 4 – Despliegue en Kubernetes

Esta parte traslada la arquitectura de microservicios al entorno Kubernetes, incorporando **replicación**, **balanceo** y **exposición externa**.

### Manifiestos en `Parte4/kube/`

- `productpage.yaml`
  - `Service` tipo **LoadBalancer** para exponer la aplicación.
  - `Deployment` con 1 réplica del pod `productpage`.

- `details.yaml`
  - `Service` para details.
  - `Deployment` con **3 réplicas** (factor de replicación 3).

- `ratings.yaml`
  - `Service` para ratings.
  - `Deployment` con **2 réplicas**.

- `reviews-svc.yaml`
  - `Service` para reviews.

- `reviews-v1-deployment.yaml`, `reviews-v2-deployment.yaml`, `reviews-v3-deployment.yaml`
  - `Deployments` para cada versión del microservicio reviews.
  - Cada uno con su imagen (`34/reviews-v1`, `34/reviews-v2`, `34/reviews-v3`) y configuración de volúmenes.

### Construcción de imágenes para Kubernetes

En `Parte4/src/` se proporcionan Dockerfiles equivalentes a los de la Parte 3 para:

- `details/`
- `productpage/`
- `ratings/`
- `reviews/` (con subcarpeta `reviews-wlpcfg`)

Desde `Parte4/src/`, se pueden construir las imágenes con:

```bash
# Ejemplos (ajustar el prefijo de imagen a tu usuario o registro)
docker build -t 34/details Parte4/src/details
docker build -t 34/productpage Parte4/src/productpage
docker build -t 34/ratings Parte4/src/ratings
# Para reviews v1/v2/v3 se usan Dockerfiles específicos dentro de reviews-wlpcfg
```

Una vez disponibles las imágenes en el registro accesible por el cluster (o en el propio nodo), se aplica la configuración de Kubernetes.

### Despliegue en Kubernetes

Desde `Parte4/kube/`:

```bash
kubectl apply -f details.yaml
kubectl apply -f ratings.yaml
kubectl apply -f reviews-svc.yaml
kubectl apply -f reviews-v1-deployment.yaml   # o v2 / v3
kubectl apply -f productpage.yaml
```

Para ver el estado de los recursos:

```bash
kubectl get pods
kubectl get svc
kubectl get deployments
```

El `Service` `productpage` expone la aplicación mediante una IP externa (LoadBalancer) o, en el caso de Minikube, se puede utilizar:

```bash
minikube service productpage
```

---

## Habilidades trabajadas

Este proyecto demuestra competencias en:

- **DevOps y Cloud-native**
  - Despliegue progresivo: VM → Docker → Docker Compose → Kubernetes.
  - Uso de Infrastructure as Code (ficheros YAML, Dockerfiles).

- **Contenerización y orquestación**
  - Construcción de imágenes Docker multilenguaje.
  - Orquestación de microservicios con Docker Compose.
  - Despliegue, escalado y actualización controlada en Kubernetes.

- **Programación y automatización**
  - Scripts en **Python** para automatizar instalación, configuración y arranque.
  - Uso de variables de entorno para parametrizar servicios.

- **Arquitecturas de microservicios**
  - Segmentación de un monolito en servicios independientes.
  - Gestión de distintas versiones de un mismo microservicio (reviews v1/v2/v3).

---
