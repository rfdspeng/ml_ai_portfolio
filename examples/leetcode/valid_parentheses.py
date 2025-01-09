"""
Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

    Open brackets must be closed by the same type of brackets.
    Open brackets must be closed in the correct order.
    Every close bracket has a corresponding open bracket of the same type.

Example 1:

Input: s = "()"

Output: true

Example 2:

Input: s = "()[]{}"

Output: true

Example 3:

Input: s = "(]"

Output: false

Example 4:

Input: s = "([])"

Output: true
"""

class Solution:
    def isValid(self, s: str) -> bool:
        closing_map = {
            "}": "{",
            ")": "(",
            "]": "[",
        }
        stack = []
        for c in s:
            if c in closing_map:
                top_of_stack = stack.pop() if stack else "#"
                if top_of_stack != closing_map[c]:
                    return False
            else:
                stack.append(c)
        
        return stack == []

solver = Solution()

inputs = ["()", "()[]{}", "(]", "([])", "(){}}{"]
for input in inputs:
    print(f"{input}: {solver.isValid(input)}")