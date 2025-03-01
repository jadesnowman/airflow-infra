docker compose down --volumes --remove-orphans



  # phpredisadmin:
  #   image: erikdubbelboer/phpredisadmin
  #   environment:
  #     REDIS_1_HOST: redis
  #     REDIS_1_PORT: 6379
  #   ports:
  #     - "4001:80"
  #   stdin_open: true
  #   tty: true
  #   restart: unless-stopped

  # adminer:
  #   image: adminer
  #   restart: unless-stopped
  #   ports:
  #     - 4002:8080
