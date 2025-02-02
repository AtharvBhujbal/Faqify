import pytest
import json
from unittest.mock import patch, MagicMock
from app.redis import Redis

@pytest.fixture
def mock_redis():
    with patch('app.redis.redis.StrictRedis') as mock_redis:
        yield mock_redis.return_value

@pytest.fixture
def redis_instance(mock_redis):
    return Redis()

def test_set_with_expiry(redis_instance, mock_redis):
    redis_instance.set('key1', {'value': 123}, expiry=60)
    mock_redis.set.assert_called_with('key1', json.dumps({'value': 123}))
    mock_redis.expire.assert_called_with('key1', time=60)

def test_set_without_expiry(redis_instance, mock_redis, monkeypatch):
    monkeypatch.setenv('REDIS_EXPIRY_TIME', '120')
    redis_instance.set('key2', {'value': 456})
    mock_redis.set.assert_called_with('key2', json.dumps({'value': 456}))
    mock_redis.expire.assert_called_with('key2', time=120)

def test_get(redis_instance, mock_redis):
    mock_redis.get.return_value = json.dumps({'value': 789}).encode()
    result = redis_instance.get('key1')
    assert result == {'value': 789}
    mock_redis.get.assert_called_with('key1')

def test_keys(redis_instance, mock_redis):
    mock_redis.keys.return_value = [b'key1', b'key2']
    result = redis_instance.keys()
    assert result == [b'key1', b'key2']
    mock_redis.keys.assert_called_once()

def test_flush(redis_instance, mock_redis):
    redis_instance.flush()
    mock_redis.flushall.assert_called_once()

def test_exists(redis_instance, mock_redis):
    mock_redis.exists.return_value = 1
    result = redis_instance.exists('key1')
    assert result == 1
    mock_redis.exists.assert_called_with('key1')

def test_expire(redis_instance, mock_redis):
    redis_instance.expire('key1', 180)
    mock_redis.expire.assert_called_with('key1', 180)

def test_time_to_live(redis_instance, mock_redis):
    mock_redis.ttl.return_value = 150
    result = redis_instance.time_to_live('key1')
    assert result == 150
    mock_redis.ttl.assert_called_with('key1')
