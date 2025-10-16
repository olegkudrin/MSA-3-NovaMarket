# Примечания по заданию 3

## Динамическая маршрутизация на основании показателей утилизации памяти

Запуск minikube.
```shell
minikube start
```

Активация и проверка metrics-server.
```shell
minikube addons enable metrics-server
kubectl get deployment metrics-server -n kube-system
```

Переключение среды на докер minikube.
```shell
eval $(minikube docker-env)
```

Собрать образ приложения.
```shell
docker build -t scaletestapp:v1 .
```

Применить deployment, service, hpa_memory.
```shell
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa_memory.yaml
```

Определить IP-адрес minikube:
```shell
minikube ip
```

Проверить приложение:
```shell
curl http://192.168.49.2:30080
```

Смотрим сколько подов:
```shell
kubectl get pods -l pod=scaletestapp-pod
```

Сгенерировать нагрузку на приложение
```shell
locust
```

## Динамическая маршрутизация на основании показателей количества запросов в секунду

Настроить динамическое масштабирование на основании количества запросов в секунду (RPS) на один под приложения.

### Установить Prometheus в вашем кластере

```shell
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus-operator prometheus-community/kube-prometheus-stack
```

Проверка Prometheus:
```shell
kubectl get pods -l "release=prometheus-operator"
```

Доступ к Prometheus UI:
```shell
export POD_NAME=$(kubectl get pods -l "app.kubernetes.io/name=prometheus" -oname)
kubectl port-forward $POD_NAME 9090
```

Пароль к Grafana (выдает prom-operator):
```shell
kubectl get secrets prometheus-operator-grafana -o jsonpath="{.data.admin-password}" | base64 -d ; echo
```

Доступ к Grafana:
```shell
export POD_NAME=$(kubectl get pod -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=prometheus-operator" -oname)
kubectl port-forward $POD_NAME 3000
```

### Настроить экспорт метрик из приложения в Prometheus

Применить конфигурацию Service Monitor:
```shell
kubectl apply -f sm.yaml
```

### Проверить поступление метрик приложения в Prometheus

Смотрим метрику http_requests_total.

С помощью Prometheus Web UI, откройте раздел Graph или
Targets и убедитесь, что метрики отображаются.
Сделайте скриншоты интерфейса с метриками.

### Настроить автоматическое масштабирование по RPS через HPA

Установить Prometheus Adapter.
```shell
helm install prometheus-adapter prometheus-community/prometheus-adapter -f prom-adapter-values.yaml
```

Список метрик:
```shell
kubectl get --raw /apis/custom.metrics.k8s.io/v1beta1 | jq
```
Вывод:
```json
{
  "kind": "APIResourceList",
  "apiVersion": "v1",
  "groupVersion": "custom.metrics.k8s.io/v1beta1",
  "resources": [
    {
      "name": "namespaces/http_requests_per_second",
      "singularName": "",
      "namespaced": false,
      "kind": "MetricValueList",
      "verbs": [
        "get"
      ]
    },
    {
      "name": "pods/http_requests_per_second",
      "singularName": "",
      "namespaced": true,
      "kind": "MetricValueList",
      "verbs": [
        "get"
      ]
    }
  ]
}
```

Проверка значений метрики:
```shell
kubectl get --raw "/apis/custom.metrics.k8s.io/v1beta1/namespaces/default/pods/*/http_requests_per_second" | jq .
```

### Убедиться, что всё работает как задумано.

Применить hpa_rps.
```shell
kubectl apply -f hpa_rps.yaml
```

Смотрим сколько подов:
```shell
kubectl get pods -l pod=scaletestapp-pod
```

Сгенерировать нагрузку на приложение
```shell
locust
```
