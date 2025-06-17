import hashlib
from flask import Flask, request, jsonify

class BloomFilter:
    def __init__(self, size=100, hash_functions=None):
        self.size = size
        self.bit_array = [0] * size
        if hash_functions is None:
            self.hash_functions = [self._hash_md5, self._hash_sha1]
        else:
            self.hash_functions = hash_functions
    def _hash_md5(self, key):
        hash_value = hashlib.md5(str(key).encode()).hexdigest()
        return int(hash_value, 16) % self.size
    def _hash_sha1(self, key):
        hash_value = hashlib.sha1(str(key).encode()).hexdigest()
        return int(hash_value, 16) % self.size
    def insert(self, key):
        for func in self.hash_functions:
            index = func(key)
            self.bit_array[index] = 1
    #поиск ключа
    def search(self, key):
        return all(self.bit_array[func(key)] == 1 for func in self.hash_functions)
#создаем объект фильтра
bloom_filter = BloomFilter(size=1000)

#создаем сервер
webserver = Flask(__name__)

#запрос уровня hello world
@webserver.route('/', methods=['GET'])
def hello():
    return "Hello, World!", 200

#вставка ключа
@webserver.route('/insert', methods=['POST'])
def api_insert():
    data = request.json
    key = data.get('key')
    if key is None:
        return jsonify({'error': 'No key provided'}), 400
    bloom_filter.insert(key)
    return jsonify({'message': f'Key "{key}" inserted'}), 200

#поиск ключа
@webserver.route('/search', methods=['POST'])
def api_search():
    data = request.json
    key = data.get('key')
    if key is None:
        return jsonify({'error': 'No key provided'}), 400
    found = bloom_filter.search(key)
    return jsonify({'result': found}), 200
#запуск
if __name__ == '__main__':
    webserver.run(host='0.0.0.0', port=5000)
