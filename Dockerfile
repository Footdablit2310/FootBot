# Use Node.js 20 on Alpine Linux (small image)
FROM node:20-alpine

# Set working directory inside container
WORKDIR /app

# Copy package files first (better caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your source code
COPY . .

# Build TypeScript -> dist/
RUN npm run build

# Start the bot
CMD ["npm", "start"]
