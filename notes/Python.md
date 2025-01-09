# Data structures

## Hash tables - add two-sum problem

A hash table is an implementation of an associative array, also known as a dictionary or a map. An associative array maps keys to values. Given a key, a hash table uses a hash function to compute an index, aka a hash code, into an array of buckets or slots from which the corresponding value can be found.

## Stacks - add valid parentheses example

# Big O notation for time and space complexity

## Two sum example
```python
def twoSum(self, nums: list[int], target: int) -> list[int]:
        num_map = {}
        for num_idx, num in enumerate(nums):
            difference = target - num # O(1)
            if difference in num_map: # O(1)
                return [num_idx, num_map[difference]]
            num_map[num] = num_idx # O(1)
```
**Time complexity:**
* Arithmetic operations, dictionary membership check (hash table), and assignments are $O(1)$.
* The loop runs once for each element in `nums`. If the size of `nums` is $n$, the total number of iterations is $n$.
* Since each iteration does $O(1)$ work, the total time complexity is $O(1) \times n = O(n)$.

**Space complexity:** `num_map` stores up to $n$ elements, so the space complexity is $O(n)$.

## Two sum, brute-force example
```python
def twoSum(self, nums: list[int], target: int) -> list[int]:
    for num_idx in range(len(nums)):
        for num_idx2 in range(num_idx+1, len(nums)):
            if nums[num_idx] + nums[num_idx2] == target:
                return [num_idx, num_idx2]
```
**Time complexity:**
* The outer loop runs $n$ times.
* In the worst case, the inner loop runs $n-1$ times, then $n-2$, and so on until $1$.
* In the worst case, the total number of iterations across the two loops is $(n-1) + (n-2) + (n-3) + ... + 2 + 1$, which is equal to $n(n-1) \over 2$.
* Checking the condition in the `if` statement is $O(1)$.
* The total time complexity is then $O\left(\frac{n(n-1)}{2}\right)$, which simplifies to $O(n^2)$.

**Space complexity:** since this doesn't need any additional data structures, the space complexity is $O(1)$.








# Random stuff

`zip`

`sorted`

`*args, **kwargs`