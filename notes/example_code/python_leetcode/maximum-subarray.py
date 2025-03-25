"""
Given an integer array nums, find the

with the largest sum, and return its sum.

 

Example 1:

Input: nums = [-2,1,-3,4,-1,2,1,-5,4]
Output: 6
Explanation: The subarray [4,-1,2,1] has the largest sum 6.

Example 2:

Input: nums = [1]
Output: 1
Explanation: The subarray [1] has the largest sum 1.

Example 3:

Input: nums = [5,4,-1,7,8]
Output: 23
Explanation: The subarray [5,4,-1,7,8] has the largest sum 23.

 

Constraints:

    1 <= nums.length <= 105
    -104 <= nums[i] <= 104

 

Follow up: If you have figured out the O(n) solution, try coding another solution using the divide and conquer approach, which is more subtle.
"""

# Verbose with subarray    
class Solution:
    def maxSubArray(self, nums: list[int], verbose: bool=False) -> int:
        running_idx = [0, 0]
        running_sum = nums[0]
        best_idx = [0, 0]
        best_sum = running_sum

        if verbose:
            print(f"Input = {nums}")
        for ndx, num in enumerate(nums[1:]):
            if verbose:
                print(f"Current index, number = {ndx}: {num}")
                print(f"Running sum = {running_sum}")
                print(f"Running idx = {running_idx}")
                print(f"Best sum = {best_sum}")
                print(f"Best idx = {best_idx}")
            if running_sum < 0 and num >= running_sum:
                running_sum = num
                running_idx = [ndx+1, ndx+1]
                if num >= best_sum:
                    best_idx = [ndx+1, ndx+1]
                    best_sum = running_sum
                    if verbose:
                        print(f"Reset best sum to {best_sum}.")
                else:
                    if verbose:
                        print(f"Reset running sum to {running_sum}.")
            else:
                running_sum += num
                running_idx[1] = ndx+1
                if verbose:
                    print(f"Update running sum to {running_sum}.")
                if running_sum >= best_sum:
                    best_sum = running_sum
                    best_idx[0] = running_idx[0]
                    best_idx[1] = running_idx[1]
                    if verbose:
                        print(f"Update best sum to {best_sum}.")
            if verbose:
                print("-"*50)
        
        subarray = nums[best_idx[0]:best_idx[1]+1]
        if verbose:
            print(f"Best sum = {best_sum}")
            print(f"Subarray = {subarray}")
            print("-"*50)

        return best_sum, subarray

# # Clean
# class Solution:
#     def maxSubArray(self, nums: list[int]) -> int:
#         running_sum = nums[0]
#         best_sum = running_sum

#         for num in nums[1:]:
#             if running_sum < 0 and num >= running_sum:
#                 running_sum = num
#                 if num >= best_sum:
#                     best_sum = running_sum
#             else:
#                 running_sum += num
#                 if running_sum >= best_sum:
#                     best_sum = running_sum

#         return best_sum

# class Solution:
#     def maxSubArray(self, nums: list[int]) -> int:
#         current_sum = best_sum = nums[0]

#         for num in nums[1:]:
#             # current_sum = max(current_sum + num, num)
#             # best_sum = max(current_sum, best_sum)
#             if current_sum + num < num:
#                 current_sum = num
#             else:
#                 current_sum += num
            
#             if current_sum > best_sum:
#                 best_sum = current_sum
        
#         return best_sum
    
solver = Solution()

inputs = [[-2,1,-3,4,-1,2,1,-5,4],      # 6
          [1],                          # 1
          [5,4,-1,7,8],                 # 23
          [-2, -1],                     # -1
          [-1,-1,-2,-2],                # -1
          [8,-19,5,-4,20]]              # 21

# inputs = [[-1,-1,-2,-2]]
# inputs = [[8,-19,5,-4,20]]

for input in inputs:
    best_sum, subarray = solver.maxSubArray(input, verbose=False)
    print(f"Input = {input}")
    print(f"Subarray = {subarray}")
    print(f"Sum = {best_sum}")
    print("-"*100)

# for input in inputs:
#     best_sum = solver.maxSubArray(input)
#     print(f"Input = {input}")
#     print(f"Sum = {best_sum}")
#     print("-"*100)