import redis
from flask import current_app

class RedisClient:
    def __init__(self):
        self.redis = redis.Redis(
            host=current_app.config['REDIS_HOST'],
            port=current_app.config['REDIS_PORT'],
            db=current_app.config['REDIS_DB'],
            password=current_app.config['REDIS_PASSWORD']
        )

    def set(self, key, value, ex=None):
        """
        设置键值对
        :param key: 键
        :param value: 值
        :param ex: 过期时间（秒）
        :return:
        """
        return self.redis.set(key, value, ex=ex)

    def get(self, key):
        """
        获取键的值
        :param key: 键
        :return: 值
        """
        return self.redis.get(key)

    def delete(self, key):
        """
        删除键
        :param key: 键
        :return:
        """
        return self.redis.delete(key)

    def exists(self, key):
        """
        检查键是否存在
        :param key: 键
        :return: 是否存在
        """
        return self.redis.exists(key)

    def expire(self, key, time):
        """
        设置键的过期时间
        :param key: 键
        :param time: 过期时间（秒）
        :return:
        """
        return self.redis.expire(key, time)

    def ttl(self, key):
        """
        获取键的剩余生存时间
        :param key: 键
        :return: 剩余生存时间（秒）
        """
        return self.redis.ttl(key)
