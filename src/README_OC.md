# Changing only the deployment file and restarting the app

oc apply -f deployment-kotaemon.yaml -n geneva 

oc rollout restart deployment/kotaemon -n geneva 

Ir a la url de la app 

 

# Changing the code and redeploying the app 

- Upload the code to gitlab ... 

oc start-build kotaemon --follow -n geneva 

oc rollout restart deployment/kotaemon -n geneva 


# Step-by-Step Deployment Process Including Verification
1. Verify and Create BuildConfig if Needed
First, check if the BuildConfig named kotaemon exists in the geneva namespace:

sh
Copiar código
oc get buildconfig kotaemon -n geneva
If the output says No resources found or similar, create the BuildConfig using a YAML file (buildconfig-kotaemon.yaml). Here’s a basic example of the YAML:

yaml
Copiar código
apiVersion: build.openshift.io/v1
kind: BuildConfig
metadata:
  name: kotaemon
  namespace: geneva
spec:
  source:
    type: Git
    git:
      uri: 'https://gitlab.cm.jccm.es/inteligencia-artificial/geneva/geneva.git'
      ref: kotaemon
    contextDir: kotaemon/kotaemon
  strategy:
    type: Docker
    dockerStrategy: {}
  output:
    to:
      kind: ImageStreamTag
      name: 'kotaemon:latest'
  triggers:
    - type: GitLab
      gitlab:
        secretReference:
          name: kotaemon-gitlab-webhook-secret
    - type: ImageChange
      imageChange: {}
    - type: ConfigChange
Apply the BuildConfig if it doesn’t exist:

sh
Copiar código
oc apply -f buildconfig-kotaemon.yaml -n geneva
2. Verify and Create ImageStream if Needed
Check if the ImageStream named kotaemon exists in the geneva namespace:

sh
Copiar código
oc get imagestream kotaemon -n geneva
If the ImageStream doesn’t exist, create it:

sh
Copiar código
oc create imagestream kotaemon -n geneva
3. Start a New Build
Once the BuildConfig and ImageStream are verified or created, trigger a new build:

sh
Copiar código
oc start-build kotaemon --follow -n geneva
4. Verify and Create Deployment if Needed
Check if the Deployment named kotaemon exists in the geneva namespace:

sh
Copiar código
oc get deployment kotaemon -n geneva
If the Deployment doesn’t exist, create it using a deployment YAML file (deployment-kotaemon.yaml). Here’s a basic example:

yaml
Copiar código
apiVersion: apps/v1
kind: Deployment
metadata:
  name: kotaemon
  namespace: geneva
spec:
  replicas: 1
  selector:
    matchLabels:
      app: kotaemon
  template:
    metadata:
      labels:
        app: kotaemon
    spec:
      containers:
        - name: kotaemon
          image: 'image-registry.openshift-image-registry.svc:5000/geneva/kotaemon:latest'
          ports:
            - name: http
              containerPort: 7860
              protocol: TCP
Apply the Deployment if it doesn’t exist:

sh
Copiar código
oc apply -f deployment-kotaemon.yaml -n geneva
5. Rollout Deployment
Restart the deployment to apply any changes:

sh
Copiar código
oc rollout restart deployment/kotaemon -n geneva
6. Verify and Create Service if Needed
Check if the Service named kotaemon-service exists:

sh
Copiar código
oc get service kotaemon-service -n geneva
If the Service doesn’t exist, create it using a Service YAML (service-kotaemon.yaml):

yaml
Copiar código
apiVersion: v1
kind: Service
metadata:
  name: kotaemon-service
  namespace: geneva
spec:
  ports:
    - name: http
      port: 7860
      targetPort: http
      protocol: TCP
  selector:
    app: kotaemon
  type: ClusterIP
Apply the Service if it doesn’t exist:

sh
Copiar código
oc apply -f service-kotaemon.yaml -n geneva
7. Verify and Create Route if Needed
Check if the Route named kotaemon-service exists:

sh
Copiar código
oc get route kotaemon-service -n geneva
If the Route doesn’t exist, create it using a Route YAML (route-kotaemon.yaml):

yaml
Copiar código
apiVersion: route.openshift.io/v1
kind: Route
metadata:
  name: kotaemon-service
  namespace: geneva
spec:
  host: kotaemon-service-geneva.apps.ocp-ia.jccm.es
  to:
    kind: Service
    name: kotaemon-service
  port:
    targetPort: http
  tls:
    termination: edge
    insecureEdgeTerminationPolicy: Redirect
Apply the Route if it doesn’t exist:

sh
Copiar código
oc apply -f route-kotaemon.yaml -n geneva
8. Verify Pods Status
Ensure the kotaemon pods are running correctly:

sh
Copiar código
oc get pods -n geneva
Summary of All Commands with Verification
Verify and Create BuildConfig:

sh
Copiar código
oc get buildconfig kotaemon -n geneva || oc apply -f buildconfig-kotaemon.yaml -n geneva
Verify and Create ImageStream:

sh
Copiar código
oc get imagestream kotaemon -n geneva || oc create imagestream kotaemon -n geneva
Start New Build:

sh
Copiar código
oc start-build kotaemon --follow -n geneva
Verify and Create Deployment:

sh
Copiar código
oc get deployment kotaemon -n geneva || oc apply -f deployment-kotaemon.yaml -n geneva
Rollout Deployment:

sh
Copiar código
oc rollout restart deployment/kotaemon -n geneva
Verify and Create Service:

sh
Copiar código
oc get service kotaemon-service -n geneva || oc apply -f service-kotaemon.yaml -n geneva
Verify and Create Route:

sh
Copiar código
oc get route kotaemon-service -n geneva || oc apply -f route-kotaemon.yaml -n geneva
Verify Pods Status:

sh
Copiar código
oc get pods -n geneva
This series of commands ensures that the BuildConfig, ImageStream, Deployment, Service, and Route are all in place. If any of these resources are missing, they will be created. You then trigger a new build, apply changes, and verify that everything is running smoothly.