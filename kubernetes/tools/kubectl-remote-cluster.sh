
# on local server


kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: default-token
  annotations:
    kubernetes.io/service-account.name: default
type: kubernetes.io/service-account-token
EOF

while ! kubectl describe secret default-token | grep -E '^token' >/dev/null; do
  echo "waiting for token..." >&2
  sleep 1
done

APISERVER=$(kubectl config view --minify -o jsonpath='{.clusters[0].cluster.server}')
TOKEN=$(kubectl get secret default-token -o jsonpath='{.data.token}' | base64 --decode)

curl $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure



# on remote console

export APISERVER=https://10.39.122.85:6443
export TOKEN=

kubectl config set-cluster demo1 --server=$APISERVER --insecure-skip-tls-verify
kubectl config set-credentials default --token=$TOKEN
kubectl config set-context demo1 --cluster=demo1 --namespace=default --user=default

kubectl config view
kubectl config use-context demo1
kubectl config view --minify

kubectl get ns


