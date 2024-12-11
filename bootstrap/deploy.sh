#!/bin/bash

# Load environment variables
if [ -f ".env" ]; then
  source .env
else
  echo "Error: .env file not found."
  exit 1
fi

# Check if essential environment variables are set
if [[ -z "${DATA_SCIENCE_PROJECT_NAMESPACE}" || -z "${EMBEDDINGS_NAMESPACE}" || -z "${EMBEDDINGS_MODEL_ROOT}" || -z "${EMBEDDINGS_MODEL_ID}" || -z "${EMBEDDINGS_MODEL_NAME}" || -z "${EMBEDDINGS_MODEL_DISPLAY_NAME}" || -z "${REPO_URL}" ]]; then
  echo "Error: One or more required environment variables are missing."
  exit 1
fi

# Print environment variables
echo "DATA_SCIENCE_PROJECT_NAMESPACE: ${DATA_SCIENCE_PROJECT_NAMESPACE}"
echo "EMBEDDINGS_NAMESPACE: ${EMBEDDINGS_NAMESPACE}"
echo "EMBEDDINGS_MODEL_ROOT: ${EMBEDDINGS_MODEL_ROOT}"
echo "EMBEDDINGS_MODEL_ID: ${EMBEDDINGS_MODEL_ID}"
echo "EMBEDDINGS_MODEL_NAME: ${EMBEDDINGS_MODEL_NAME}"
echo "EMBEDDINGS_MODEL_DISPLAY_NAME: ${EMBEDDINGS_MODEL_DISPLAY_NAME}"
echo "REPO_URL: ${REPO_URL}"
echo ""

# Deploy nomic ai embeddings
cat <<EOF | oc apply -f -
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: nomic-embeddings
  namespace: openshift-gitops
  annotations:
    argocd.argoproj.io/compare-options: IgnoreExtraneous
    argocd.argoproj.io/sync-options: SkipDryRunOnMissingResource=true
spec:
  project: default
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: "${EMBEDDINGS_NAMESPACE}"
  source:
    path: gitops/embeddings
    repoURL: https://github.com/alpha-hack-program/doc-bot-kotaemon.git
    targetRevision: main
    helm:
      parameters:
        - name: createNamespace # This has to be false if deploying in the an existing namespace
          value: 'true'
        - name: modelConnection.createSecret # This has to be false if the secret `embeddings` already exists
          value: 'true'
        - name: dataScienceProjectNamespace
          value: "${EMBEDDINGS_NAMESPACE}"
        - name: dataScienceProjectDisplayName
          value: "${EMBEDDINGS_NAMESPACE}"
        - name: model.root
          value: "${EMBEDDINGS_MODEL_ROOT}"
        - name: model.id
          value: "${EMBEDDINGS_MODEL_ID}"
        - name: model.name
          value: "${EMBEDDINGS_MODEL_NAME}"
        - name: model.displayName
          value: "${EMBEDDINGS_MODEL_DISPLAY_NAME}"
        - name: model.runtime.displayName
          value: "Nomic BERT"
        - name: model.runtime.templateName
          value: "nomic-bert-template"
  syncPolicy:
    automated:
      # prune: true
      selfHeal: true
EOF

# Wait for the nomic inferenceservice to be ready
while [[ $(oc get inferenceservice ${EMBEDDINGS_MODEL_NAME} -n ${EMBEDDINGS_NAMESPACE} -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do
  echo "Waiting for nomic-embed-text-v1 to be ready..."
  sleep 5
done

# Get the nomic-embeddings service URL
LOCAL_OPENAI_EMBEDDINGS_API_BASE=$(oc get inferenceservice ${EMBEDDINGS_MODEL_NAME} -n ${EMBEDDINGS_NAMESPACE} -o jsonpath='{.status.url}')
echo "LOCAL_OPENAI_EMBEDDINGS_API_BASE: ${LOCAL_OPENAI_EMBEDDINGS_API_BASE}"

# Wait for the openai-chat inferenceservice to be ready
while [[ $(oc get inferenceservice ${LOCAL_OPENAI_API_PREDICTOR_NAME} -n ${LOCAL_OPENAI_API_PREDICTOR_NAMESPACE} -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}') != "True" ]]; do
  echo "Waiting for openai-chat to be ready..."
  sleep 5
done

# Get the openai-chat service URL
LOCAL_OPENAI_API_BASE=$(oc get inferenceservice ${LOCAL_OPENAI_API_PREDICTOR_NAME} -n ${LOCAL_OPENAI_API_PREDICTOR_NAMESPACE} -o jsonpath='{.status.url}')
echo "LOCAL_OPENAI_API_BASE: ${LOCAL_OPENAI_API_BASE}"

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
          value: "${DATA_SCIENCE_PROJECT_NAMESPACE}"
        - name: dataScienceProjectNamespace
          value: "${DATA_SCIENCE_PROJECT_NAMESPACE}"
        # - name: localOpenaiApiBase
        #   value: ${LOCAL_OPENAI_API_BASE}/v1
        - name: localOpenaiApiChatPredictorName
          value: mistral-7b
        - name: localOpenaiChatModel
          value: /mnt/models/
        # - name: localOpenaiEmbeddingsApiBase
        #   value: "${LOCAL_OPENAI_EMBEDDINGS_API_BASE}/v1"
        - name: localOpenaiApiEmbeddingsPredictorName
          value: nomic-embed-text-v1
        - name: localOpenaiEmbeddingsModel
          value: "${EMBEDDINGS_MODEL_NAME}"
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

