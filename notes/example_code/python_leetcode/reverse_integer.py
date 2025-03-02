"""
Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-231, 231 - 1], then return 0.

Assume the environment does not allow you to store 64-bit integers (signed or unsigned).


Example 1:

Input: x = 123
Output: 321

Example 2:

Input: x = -123
Output: -321

Example 3:

Input: x = 120
Output: 21

"""

class Solution:
    """
    def reverse(self, x: int) -> int:
        is_negative = 1
        digits = []
        if x < 0:
            x = -x
            is_negative = -1
        
        while True:
            digit = x % 10
            digits.append(digit)

            if x - digit == 0:
                break
            else:
                x = int(x/10)
        
        x_reverse = 0
        for dig_idx, digit in enumerate(digits):
            x_reverse += digit * 10**(len(digits)-1-dig_idx)
        
        x_reverse *= is_negative

        if x_reverse > 2**31-1 or x_reverse < -2**31:
            x_reverse = 0

        return x_reverse
    """

    """
    def reverse(self, x: int) -> int:
        sign = -1 if x < 0 else 1
        x_reverse = int(str(abs(x))[::-1])*sign
        if x_reverse > 2**31-1 or x_reverse < -2**31:
            x_reverse = 0

        return x_reverse
    """

    def reverse (self, x: int) -> int:
        # if x < -2**31 or x >= 2**31:
        #     raise Exception(f"Input {x} is out of bounds")

        INT_MAX = 2**31

        is_neg = x < 0
        x = abs(x)
        xr = 0
        while x > 0:
            digit = x % 10

            if digit > INT_MAX - 10*xr - 1*(not is_neg):
                return 0
            
            xr = 10 * xr + digit

            # print("--------------------")
            # print(f"x: {x}")
            # print(f"digit: {digit}")
            # print(f"xr: {xr}")

            x //= 10

        return -xr if is_neg else xr

solver = Solution()

inputs = [123, -123, 120, -1111111119, 1111111119]
# inputs = [123]

for input in inputs:
    print(f"Input: {input}")
    print(solver.reverse(input))