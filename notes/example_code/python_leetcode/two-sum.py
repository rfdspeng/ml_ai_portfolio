"""
Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.


Example 1:

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].

Example 2:

Input: nums = [3,2,4], target = 6
Output: [1,2]

Example 3:

Input: nums = [3,3], target = 6
Output: [0,1]

"""

class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        
        ### Most efficient

        # Store the numbers you've already seen
        # key = number, value = index
        num_map = {}
        for num_idx, num in enumerate(nums):
            difference = target - num
            if difference in num_map:
                return [num_idx, num_map[difference]]
            num_map[num] = num_idx


        ### Brute force

        for num_idx in range(len(nums)):
            for num_idx2 in range(num_idx+1, len(nums)):
                if nums[num_idx] + nums[num_idx2] == target:
                    return [num_idx, num_idx2]

solver = Solution()

inputs = [
    {"nums": [2,7,11,15],
     "target": 9},
    {"nums": [3,2,4],
     "target": 6},
    {"nums": [3,3],
     "target": 6},
]

for input in inputs:
    print(solver.twoSum(input["nums"], input["target"]))