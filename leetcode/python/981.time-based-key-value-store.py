#
# @lc app=leetcode id=981 lang=python3
#
# [981] Time Based Key-Value Store
#

# @lc code=start
class TimeMap:

    def __init__(self):
        self.cache = {}
        

    def set(self, key: str, value: str, timestamp: int) -> None:
        values = self.cache.get(key, [])
        l = 0
        r = len(values) - 1
        while l <= r:
            mid = (l + r) // 2
            if values[mid][0] <= timestamp:
                l = mid + 1
            else:
                r = mid - 1
        values.insert(l, (timestamp, value))
        self.cache[key] = values
        

    def get(self, key: str, timestamp: int) -> str:
        values = self.cache.get(key, [])
        if len(values) == 0:
            return ""
        l = 0
        r = len(values) - 1
        while l <= r:
            mid = (l + r) // 2
            if values[mid][0] <= timestamp: 
                l = mid + 1
            else: r = mid - 1
        if l - 1 < 0:
            return ""
        return values[l-1][1]
        


# Your TimeMap object will be instantiated and called as such:
# obj = TimeMap()
# obj.set(key,value,timestamp)
# param_2 = obj.get(key,timestamp)
# @lc code=end


obj = TimeMap()
obj.set("foo","bar1",1)
obj.set("foo","bar2",2)
obj.set("foo","bar0",0)
obj.get("foo", 1)
obj.get("foo", 3)
