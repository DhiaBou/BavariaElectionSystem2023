FROM node:20-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json files
COPY ./client/package.json ./client/package-lock.json /app/

# Install dependencies with --legacy-peer-deps flag
RUN npm install --legacy-peer-deps

# Copy the rest of the client application
COPY ./client /app

# Expose port 3000 for the Node.js application
EXPOSE 3000

# Command to start the application
CMD ["npm", "start"]
