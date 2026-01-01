# ---- Build Stage ----
# Use a modern, secure Node.js Alpine image.
# Alpine is lightweight, which reduces the attack surface.
FROM node:23-alpine AS build

# Set the working directory inside the container.
WORKDIR /usr/src/app

# Install build-time dependencies for native modules, especially node-canvas.
# This includes python, make, and g++ for compilation, and dev libraries for canvas.
RUN apk add --no-cache \
    python3 \
    make \
    g++ \
    cairo-dev \
    jpeg-dev \
    pango-dev \
    giflib-dev

# Copy package definitions to leverage Docker layer caching.
COPY package.json package-lock.json* ./

# Install all npm dependencies. `npm ci` is used for reproducible builds.
RUN npm ci

# Copy the rest of the application source code.
COPY . .

# Compile TypeScript to JavaScript.
RUN npm run build

# ---- Production Stage ----
# Start from a fresh, minimal Node.js Alpine image for the final image.
FROM node:23-alpine AS production

WORKDIR /usr/src/app

# Set the environment to production for optimized performance.
ENV NODE_ENV=production

# Install only the runtime dependencies for node-canvas.
# This keeps the final image smaller than including the -dev packages.
RUN apk add --no-cache \
    cairo \
    jpeg \
    pango \
    giflib

# Create a non-root user and group for enhanced security.
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Create and set permissions for the log directory.
RUN mkdir -p /var/log/pubmed-mcp-server && chown -R appuser:appgroup /var/log/pubmed-mcp-server

# Copy build artifacts from the build stage.
# This includes the compiled code and production node_modules.
COPY --from=build /usr/src/app/dist ./dist
COPY --from=build /usr/src/app/node_modules ./node_modules
COPY --from=build /usr/src/app/package.json ./

# Switch to the non-root user.
USER appuser

# Expose the port the server will listen on.
# The PORT variable is typically provided by the deployment environment (e.g., Smithery).
ENV MCP_HTTP_PORT=${PORT:-3017}
EXPOSE ${MCP_HTTP_PORT}

# Set runtime environment variables.
ENV MCP_HTTP_HOST=0.0.0.0
ENV MCP_TRANSPORT_TYPE=http
ENV MCP_SESSION_MODE=stateless
ENV MCP_LOG_LEVEL=info
ENV LOGS_DIR=/var/log/pubmed-mcp-server
ENV MCP_AUTH_MODE=none
ENV MCP_FORCE_CONSOLE_LOGGING=true

# The command to start the server.
CMD ["node", "dist/index.js"]
