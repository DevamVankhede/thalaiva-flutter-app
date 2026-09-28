# ==========================================
# Stage 1: Vendor Builder
# ==========================================
FROM composer:2.7 AS vendor
WORKDIR /app
COPY composer.json composer.lock ./
RUN composer install \
    --no-dev \
    --no-interaction \
    --prefer-dist \
    --optimize-autoloader \
    --ignore-platform-reqs

# ==========================================
# Stage 2: Hardened Runtime (PHP 8.3 FPM/CLI)
# ==========================================
FROM php:8.3-cli-alpine

# Install essential runtime libraries & security tools
RUN apk add --no-cache \
    postgresql-dev \
    libzip-dev \
    zip \
    unzip \
    curl \
    git \
    shadow \
    sqlite-dev \
    && docker-php-ext-install pdo pdo_pgsql pdo_sqlite zip opcache

# Configure PHP Security & Performance
RUN echo "expose_php = Off" > /usr/local/etc/php/conf.d/security.ini \
    && echo "display_errors = Off" >> /usr/local/etc/php/conf.d/security.ini \
    && echo "log_errors = On" >> /usr/local/etc/php/conf.d/security.ini \
    && echo "memory_limit = 256M" >> /usr/local/etc/php/conf.d/security.ini \
    && echo "max_execution_time = 30" >> /usr/local/etc/php/conf.d/security.ini

# Set non-root working directory
WORKDIR /var/www/html

# Copy application source
COPY . /var/www/html
COPY --from=vendor /app/vendor /var/www/html/vendor

# Create non-root application user
RUN usermod -u 1000 www-data && groupmod -g 1000 www-data \
    && chown -R www-data:www-data /var/www/html/storage /var/www/html/bootstrap/cache \
    && chmod -R 775 /var/www/html/storage /var/www/html/bootstrap/cache

# Switch to non-root user (Principle of Least Privilege)
USER www-data

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://127.0.0.1:8000/api/health || exit 1

CMD ["php", "-S", "0.0.0.0:8000", "-t", "public"]
