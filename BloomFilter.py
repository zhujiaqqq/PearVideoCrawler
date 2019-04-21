import mmh3
from bitarray import bitarray

# Implement a simple bloom filter with murmurhash algorithm.
# Bloom filter is used to check wether an element exists in a collection, and it has a good performance in big data situation.
# It may has positive rate depend on hash functions and elements count.
from repository.MysqlRepo import MysqlHelper


class BloomFilter(object):
    def __init__(self, BIT_SIZE):
        # 初始化布隆过滤器,生成一下全0的 bitarray
        bit_array = bitarray(BIT_SIZE)
        self.BIT_SIZE = BIT_SIZE
        bit_array.setall(0)
        self.bit_array = bit_array

    def add(self, url):
        # 添加一个url,同时获取这个url的对应的bitarray的位置
        point_list = self.get_postions(url)
        for b in point_list:
            self.bit_array[b] = 1

    def contains(self, url):
        # 验证这个url是否存在在集合中
        point_list = self.get_postions(url)
        result = True
        for b in point_list:
            result = result and self.bit_array[b]
        return result

    def get_postions(self, url):
        # 一个url获取七个位置,之后会把这七个位置变为1
        point1 = mmh3.hash(url, 41) % self.BIT_SIZE
        point2 = mmh3.hash(url, 42) % self.BIT_SIZE
        point3 = mmh3.hash(url, 43) % self.BIT_SIZE
        point4 = mmh3.hash(url, 44) % self.BIT_SIZE
        point5 = mmh3.hash(url, 45) % self.BIT_SIZE
        point6 = mmh3.hash(url, 46) % self.BIT_SIZE
        point7 = mmh3.hash(url, 47) % self.BIT_SIZE
        return [point1, point2, point3, point4, point5, point6, point7]


if __name__ == '__main__':
    BIT_SIZE = 5000000
    # 类的实例化
    bloom_filter = BloomFilter(BIT_SIZE)

    helper = MysqlHelper()
    results = helper.fetchall("select * from pear_video limit 1000")
    for result in results:
        bloom_filter.add(result[3])

    test_list = helper.fetchall("select * from pear_video where id between 700 and 1300")
    for test in test_list:
        res = bloom_filter.contains(test[3])
        print('被检测的网址 : ', test[3], '/ 是否被包含在原集合中 : ', res)
