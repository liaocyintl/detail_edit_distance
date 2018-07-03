# Example 1
from distance import ded
source = "kitten"
target = "sitting"
rs = ded(source=source, target=target)
print(rs)

# Example 2
from distance import ded
source = 'I have a dream'
target = 'I had a dream about you'
rs = ded(source=source.split(" "), target=target.split(" "))
print(rs)

# Example 3
from distance import ded
source = "kitten"
target = "sitting"
rs = ded(source=source, target=target, is_combine_LCS=False)
print(rs)


# Example 3
from distance import ded
source = "I had a dream that my"
target = "I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin, but by the content of their character."
rs = ded(source=source.split(" "), target=target.split(" "), as_least_cost=True)
print(rs)
