#
# @lc app=leetcode id=355 lang=python3
#
# [355] Design Twitter
#

# @lc code=start
class Twitter:

    def __init__(self):
        self.count = 0
        self.tweetMap = defaultdict(list)
        self.followMap = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweetMap[userId].append([self.count, tweetId])
        self.count -= 1

    def getNewsFeed(self, userId: int) -> List[int]:
        # Initialize an empty list to store the result
        res = []
        # Initialize a min heap to store the most recent tweets from followed users
        minHeap = []

        # Ensure that the user follows themselves
        self.followMap[userId].add(userId)
        
        # Iterate over users followed by the given userId
        for followeeId in self.followMap[userId]:
            # Check if the followee has any tweets
            if followeeId in self.tweetMap:
                # Get the index of the most recent tweet from the followee
                index = len(self.tweetMap[followeeId]) - 1
                # Retrieve the count and tweetId of the tweet
                count, tweetId = self.tweetMap[followeeId][index]
                # Push the tweet onto the min heap along with additional information
                heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])

        # Retrieve the 10 most recent tweets from the min heap
        while minHeap and len(res) < 10:
            count, tweetId, followeeId, index = heapq.heappop(minHeap)
            # Append the tweetId to the result list
            res.append(tweetId)
            # If the followee has more tweets, push the next tweet onto the min heap
            if index >= 0:
                count, tweetId = self.tweetMap[followeeId][index]
                heapq.heappush(minHeap, [count, tweetId, followeeId, index - 1])
        # Return the result list containing the 10 most recent tweets
        return res

        

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followMap[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followMap[followerId]:
            self.followMap[followerId].remove(followeeId)


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)
# @lc code=end

