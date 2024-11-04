#!/bin/bash

# Load environment variables
. .env

# Create an ArgoCD application to deploy the helm chart at this repository and path ./gitops/kotaemon
cat <<EOF | oc apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: ${DATA_SCIENCE_PROJECT_NAMESPACE}-kotaemon
  namespace: openshift-gitops
spec:
  project: default
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: ${DATA_SCIENCE_PROJECT_NAMESPACE}
  source:
    path: gitops/kotaemon
    repoURL: ${REPO_URL}
    targetRevision: main
    helm:
      parameters:
        - name: createNamespace
          value: "false"
        - name: dataScienceProjectDisplayName
          value: "kotaemon"
        - name: dataScienceProjectNamespace
          value: "kotaemon"
  syncPolicy:
    automated:
      # prune: true
      selfHeal: true
  ignoreDifferences:
    - group: apps
      kind: Deployment
      name: kotaemon
      jqPathExpressions:
        - '.spec.template.spec.containers[].image'
      
EOF

