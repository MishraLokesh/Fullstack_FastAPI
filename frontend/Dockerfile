# Use the official Node.js image from Docker Hub
FROM node:18

# Set the working directory
WORKDIR /app

# Install dependencies
COPY package.json /app/package.json
COPY package-lock.json /app/package-lock.json
RUN npm install

# Copy the rest of the project files
COPY . /app

# Build the Next.js application
RUN npm run build

# Expose the port Next.js will run on
EXPOSE 3000

# Command to run the Next.js application in production mode
CMD ["npm", "run", "start", "--", "--hostname", "0.0.0.0"]