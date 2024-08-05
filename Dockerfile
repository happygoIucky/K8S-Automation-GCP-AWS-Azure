# Use an official Node.js runtime as a pzarent image with a specific version for security
FROM node:18.17.1

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm ci --only=production

# Copy the rest of the application code to the working directory
COPY pii-json-input-xml-body.js .

# Expose the port that your application will run on
EXPOSE 3333

# Use a non-root user for security
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

# Define the command to run your application
CMD ["node", "pii-json-input-xml-body.js"]