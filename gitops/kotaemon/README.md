# Deployment of Kotaemon

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: doc-bot-kotaemon
  namespace: openshift-gitops
spec:
  destination:
    namespace: doc-bot
    server: 'https://kubernetes.default.svc'
  ignoreDifferences:
    - group: apps
      jqPathExpressions:
        - '.spec.template.spec.containers[].image'
      kind: Deployment
      name: kotaemon
  project: default
  source:
    helm:
      parameters:
        - name: createNamespace
          value: 'false'
        - name: dataScienceProjectDisplayName
          value: doc-bot
        - name: dataScienceProjectNamespace
          value: doc-bot
        - name: localOpenaiApiBase
          value: https://mistral-7b-predictor-doc-bot.apps.cluster-8q7tj.8q7tj.sandbox277.opentlc.com/v1
        - name: localOpenaiChatModel
          value: /mnt/models/
        - name: localOpenaiEmbeddingsApiBase
          value: https://nomic-embed-text-v1-gpu-embeddings.apps.cluster-8q7tj.8q7tj.sandbox277.opentlc.com/v1
        - name: localOpenaiEmbeddingsModel
          value: nomic-embed-text-v1-gpu
    path: gitops/kotaemon
    repoURL: 'https://github.com/alpha-hack-program/doc-bot-kotaemon.git'
    targetRevision: main
  syncPolicy:
    automated:
      selfHeal: true
```