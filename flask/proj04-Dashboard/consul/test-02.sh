

curl -X PUT -d @service.dns.json   localhost:8500/v1/agent/service/register
curl -X PUT -d @service.redis.json localhost:8500/v1/agent/service/register
