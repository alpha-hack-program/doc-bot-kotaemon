

persistence in docker compose and OIDC

version: '3'
services:
  cinnamon:
    environment:
      - GRADIO_SERVER_NAME=0.0.0.0
      - GRADIO_SERVER_PORT=7860
      - COHERE_API_KEY=
      - SECRET_KEY=thisIsASampleR@nd0mString
      - OPENID_CLIENT_ID=kotaemon
      - OPENID_CLIENT_SECRET=yNlv7TXC0yNAufDrKQtckZNpiHrPiX2C
      - OPENID_CONFIG_URL=http://host.docker.internal:8082/realms/MDACA/.well-known/openid-configuration
    ports:
      - '8000:8000'
    image: 'ghcr.io/cinnamon/kotaemon:latest-full'
    volumes:
      - ./app_data:/app/ktem_app_data
      - ./pipelines.py:/app/libs/ktem/ktem/index/file/graph/pipelines.py
      - ./login.py:/app/libs/ktem/ktem/pages/login.py
      - ./user.py:/app/libs/ktem/ktem/pages/resources/user.py
      - ./pdf_viewer.js:/app/libs/ktem/ktem/assets/js/pdf_viewer.js
      - ./render.py:/app/libs/ktem/ktem/utils/render.py
      - ./app.py:/app/app.py

---------------------------------------------------------------------------


