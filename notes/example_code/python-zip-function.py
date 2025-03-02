a = (1, 2, 3)
b = [4, 5, 6]
c = [2.1, 8.4, 4.7]

# a and b must have the same number of elements
# x is a zip object, which is an iterator of tuples
# Each element in x is a 2-ple consisting of one value from a and one value from b
x = zip(a,b,c)

print(tuple(x))

for ele in x:
    print(ele)

# Since x is an iterator, after you step through it, it will be empty
print(tuple(x))

x = zip(a,b,c)
print(sorted(x, key=lambda ele: ele[2], reverse=True))
print(tuple(zip(*sorted(x, key=lambda ele: ele[1], reverse=True))))

# These are 1 x 10
x = list(range(10))
y = list(range(10,20))
z = list(range(20,30))

# This zips the values from x, y, and z together
t = zip(x,y,z)
t = tuple(t)
print(t)

# This decouples the value from x, y, and z, recovering the original arrays
print(tuple(zip(*t)))