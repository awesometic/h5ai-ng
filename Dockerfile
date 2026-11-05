# The build output is platform independent, so build it once on the host platform.
FROM --platform=$BUILDPLATFORM node:24-alpine AS build
WORKDIR /src
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY . .
RUN npm run build && node test/bundle.js

FROM nginx:1.30.6-alpine3.24
LABEL maintainer="Deokgyu Yang <secugyu@gmail.com>" \
      description="h5ai with Nginx & PHP 8.5.12+ based on Alpine Linux 3.24."

RUN apk add --no-cache \
    bash bash-completion supervisor tzdata shadow logrotate \
    'php85>=8.5.12' php85-fpm php85-session php85-json php85-xml php85-mbstring php85-exif \
    php85-intl php85-gd php85-pecl-imagick php85-zip \
    ffmpeg imagemagick imagemagick-pdf zip apache2-utils patch

# Environments
ENV PUID=911
ENV PGID=911
ENV TZ='Asia/Seoul'
ENV HTPASSWD='false'
ENV HTPASSWD_USER='guest'
ENV HTPASSWD_PW=''

# Copy configuration files
# init.sh copies the defaults to /config and links conf.d/h5ai.conf to the copy
COPY docker/h5ai.conf /etc/nginx/h5ai.conf.default
COPY docker/php_set_timezone.ini /etc/php85/conf.d/00_timezone.ini
COPY docker/php_set_jit.ini /etc/php85/conf.d/00_jit.ini
COPY docker/php_set_memory_limit.ini /etc/php85/conf.d/00_memlimit.ini
COPY docker/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY --chmod=0755 docker/logs.sh /usr/local/bin/h5ai-logs

# Copy h5ai; it lives outside the served /h5ai root, so tell PHP where the root is
# init.sh handles it like the Nginx default; nginx serves /usr/share/h5ai, so the default stays outside that
COPY --from=build /src/build/_h5ai /usr/share/h5ai-default/_h5ai
RUN echo 'env[H5AI_ROOT_PATH] = /h5ai' >> /etc/php85/php-fpm.d/www.conf

# Configure Nginx server
RUN sed --in-place=.bak 's/worker_processes  1/worker_processes  auto/g' /etc/nginx/nginx.conf
RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.bak

# Add shell script, patch files
ADD docker/init.sh /
ADD docker/h5ai.conf.htpasswd.patch /
# Set entry point file permission
RUN chmod a+x /init.sh

EXPOSE 80
VOLUME [ "/config", "/h5ai" ]
ENTRYPOINT [ "/init.sh" ]
