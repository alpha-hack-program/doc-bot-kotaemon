

cd kotaemon

docker build --target full -t kotaemon:latest .


docker build -t kotaemon:latest .



docker run -e GRADIO_SERVER_NAME=0.0.0.0 -e GRADIO_SERVER_PORT=7860 -p 7860:7860 -it --rm -v ./certificates/cacert.pem:/usr/local/lib/python3.10/site-packages/certifi/cacert.pem:ro --network="host" kotaemon:latest



- --network=host permite usar el localhost local, con el port forwarding de OC para Milvus y para usar el nomic embedding local (ollama)
- cacert.pem para poder usar los llm de red hat con certificados, puede que se pueda hacer tambien port forwarding..
  
----

para ejecutar sin certificado cacert.pem
docker run -e GRADIO_SERVER_NAME=0.0.0.0 -e GRADIO_SERVER_PORT=7860 -p 7860:7860 -it --rm kotaemon:latest

para ejecutar con certificado

docker run -e GRADIO_SERVER_NAME=0.0.0.0 -e GRADIO_SERVER_PORT=7860 -p 7860:7860 -it --rm -v ./certificates/cacert.pem:/usr/local/lib/python3.10/site-packages/certifi/cacert.pem:ro kotaemon:latest

docker exec -it 0a52 sh


- para saber de donde coge el certificado
python -c "import certifi; print(certifi.where())"

certifi.where dice /usr/local/lib/python3.10/site-packages/certifi/cacert.pem


- Docker sin volumen
Para que funcione Mistral y Llama de OpenShift en el dockerfile de kotaemon,
si no hacemos un volumen con el certificado,
hay que hacer esto primero

1.	Conectarse por bash al dockerfile
2.	cp ./certificates/cacert.pem /usr/local/lib/python3.10/site-packages/certifi/cacert.pem
3.	export SSL_CERT_FILE=/usr/local/lib/python3.10/site-packages/certifi/cacert.pem

- parece ser que esto tambien funcionaria 
ENV SSL_CERT_FILE=$(python -c "import certifi; print(certifi.where())")

- para sacar los certificados instalados
apt-get update && apt-get install -y ca-certificates
ls /usr/lib/ssl/certs


- pruebas varias (no funcionan) -------------------------------------
si ejecuto esto en el docker
python -c "import ssl; print(ssl.get_default_verify_paths())"
sale esto
DefaultVerifyPaths(cafile='/usr/local/lib/python3.10/site-packages/certifi/cacert.pem', capath='/usr/lib/ssl/certs', openssl_cafile_env='SSL_CERT_FILE', openssl_cafile='/usr/lib/ssl/cert.pem', openssl_capath_env='SSL_CERT_DIR', openssl_capath='/usr/lib/ssl/certs')


voy a probar a añadir nuevas rutas
cp ./certificates/cacert.pem /usr/lib/ssl/certs
export SSL_CERT_DIR=/usr/lib/ssl/certs/cacert.pem

esto sigue dando fallo
export SSL_CERT_FILE=/usr/lib/ssl/certs/cacert.pem
export openssl_cafile=/usr/lib/ssl/certs/cacert.pem
export openssl_capath_env=/usr/lib/ssl/certs/cacert.pem

update-ca-certificates
apt-get update && apt-get install -y ca-certificates