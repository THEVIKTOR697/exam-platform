FROM node:20

WORKDIR /app

# Copiar package.json
COPY package*.json ./

# Cambiar permisos antes de instalar
RUN chown -R node:node /app

# Cambiar a usuario node
USER node

# Instalar deps como node (🔥 clave)
RUN npm install

# Volver a root solo para copiar (opcional pero seguro)
USER root
COPY . .

# Asegurar permisos finales
RUN chown -R node:node /app

# Volver a node
USER node

EXPOSE 3000

CMD ["npm", "run", "dev"]