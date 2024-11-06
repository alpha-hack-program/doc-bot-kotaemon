
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
    path: gitops/kotaemon
    repoURL: 'https://github.com/alpha-hack-program/doc-bot-kotaemon.git'
    targetRevision: main
  syncPolicy:
    automated:
      selfHeal: true
```