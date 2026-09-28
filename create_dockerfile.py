import os

dockerfile_content = '''# Multi-stage Dockerfile for Flutter Web Production Build
FROM ghcr.io/cirruslabs/flutter:3.29.0 AS build

WORKDIR /app
COPY pubspec.yaml pubspec.lock* ./
RUN flutter pub get

COPY . .
RUN flutter build web --release

# Production Nginx runtime
FROM nginx:alpine
COPY --from=build /app/build/web /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
'''

with open(r"C:\Users\Admin\thalaivaa_flutter\Dockerfile", 'w', encoding='utf-8') as f:
    f.write(dockerfile_content)
print("Created Flutter Dockerfile")
