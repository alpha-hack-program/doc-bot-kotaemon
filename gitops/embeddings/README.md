# Deploying Nomic AI

## Deploy the Application object in charge of deploying the Model

Adapt the following parameters to your environment:

- modelConnection.scheme: http(s)
- name: modelConnection.awsAccessKeyId: user to access the S3 server
- name: modelConnection.awsSecretAccessKey: user key
- name: modelConnection.awsDefaultRegion: region, none in MinIO
- name: modelConnection.awsS3Bucket: bucket name
- name: modelConnection.awsS3Endpoint: host and port (minio.ic-shared-minio.svc:9000)

```yaml
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
    namespace: nomic-embeddings # DATA_SCIENCE_PROJECT_NAMESPACE used later
  source:
    path: gitops/embeddings
    repoURL: https://github.com/alpha-hack-program/doc-bot-kotaemon.git
    targetRevision: main
    helm:
      parameters:
        - name: createNamespace # This has to be false if deploying in the an existing namespace
          value: 'true'
        - name: createSecret # This has to be false if the secret already exists
          value: 'true'
        - name: dataScienceProjectNamespace
          value: "embeddings" # DATA_SCIENCE_PROJECT_NAMESPACE used later
        - name: dataScienceProjectDisplayName
          value: "embeddings"
        - name: model.root
          value: nomic-ai
        - name: model.id
          value: nomic-embed-text-v1
        - name: model.name
          value: nomic-embed-text-v1
        - name: model.displayName
          value: "Nomic Embed Text v1"
        - name: model.runtime.displayName
          value: "Nomic BERT"
        - name: model.runtime.templateName
          value: "nomic-bert-template"
        # - name: model.accelerator.productName
        #   value: "NVIDIA-A10G"
        # - name: model.accelerator.min
        #   value: '1'
        # - name: model.accelerator.max
        #   value: '1'
  syncPolicy:
    automated:
      # prune: true
      selfHeal: true
```
## Create a secret called hf-creds in the namespace ${DATA_SCIENCE_PROJECT_NAMESPACE}

```sh
HF_USERNAME=xyz
HF_TOKEN=hf_**********
DATA_SCIENCE_PROJECT_NAMESPACE=granite-8b

oc create secret generic hf-creds \
  --from-literal=HF_USERNAME=${HF_USERNAME} \
  --from-literal=HF_TOKEN=${HF_TOKEN} \
  -n ${DATA_SCIENCE_PROJECT_NAMESPACE}
```

## Test

```sh
INFERENCE_URL=$(oc get inferenceservice/granite-8b -n granite-8b -o jsonpath='{.status.url}')
RUNTIME_MODEL_ID=$(curl -ks -X 'GET' "${INFERENCE_URL}/v1/models" -H 'accept: application/json' | jq -r .data[0].id )
echo ${RUNTIME_MODEL_ID}

curl -s -X 'POST' \
  "${INFERENCE_URL}/v1/completions" \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "model": "'${RUNTIME_MODEL_ID}'",
  "prompt": "San Francisco is a",
  "max_tokens": 25,
  "temperature": 0
}'
```

