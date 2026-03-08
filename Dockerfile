# Use the lightweight Nginx image to serve static content
FROM nginx:alpine

# Remove the default Nginx index.html completely
RUN rm -rf /usr/share/nginx/html/*

# Copy the specific frontend dashboard files over
COPY index.html /usr/share/nginx/html/
COPY index.css /usr/share/nginx/html/
COPY dashboard.css /usr/share/nginx/html/
COPY app.js /usr/share/nginx/html/
COPY dashboard.js /usr/share/nginx/html/

# Expose port 80 (Render cloud automatically routes HTTP traffic here)
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
