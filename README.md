Introduction
======
This is a variation of edit distance (Levenshtein distance, LD [1]), 
which can extract detail modifications between source array and target array, 
including insertions, deletions, substitutions.

The traditional LD can only output a cost, 
which describes the shortest steps when a source string is updated into a target string -- called the least cost or the shortest edit distance.
Based on LD, our improvement makes extracting the detail modifications possible.

For example, the Levenshtein distance between "kitten" and "sitting" is 3.
Our algorithm can show detail modifications as following:
- kitten → sitten (substitution of "s" for "k")
- sitten → sittin (substitution of "i" for "e")
- sittin → sitting (insertion of "g" at the end).

About edit distance:
(Levenshtein distance)[https://en.wikipedia.org/wiki/Levenshtein_distance]

Ref:
[1] LEVENSHTEIN, Vladimir I. Binary codes capable of correcting deletions, insertions, and reversals. Soviet physics doklady. Vol.10, No.8, pp.707-710, 1966.

Quick Start
======
**Example 1.** get detail modifications between "kitten" and "sitting":

Python code:
```python
from distance import ded
source = "kitten"
target = "sitting"
rs = ded(source=source, target=target)
print(rs)
```

Ouput (rs):
```json
{
  "detail": [
      {"type": "sub", "src_i": [0], "tgt": "s", "src": "k", "tgt_i": [0], "cost": 1}, 
      {"type": "none", "src_i": [1, 2, 3], "tgt": "itt", "src": "itt", "tgt_i": [1, 2, 3], "cost": 0}, 
      {"type": "update", "src_i": [4], "tgt": "i", "src": "e", "tgt_i": [4], "cost": 1}, 
      {"type": "none", "src_i": [5], "tgt": "n", "src": "n", "tgt_i": [5], "cost": 0},
      {"type": "ins", "src_i": [], "tgt": "g", "src": "", "tgt_i": [6], "cost": 1}
  ], 
  "cost": 3
}
```

- "detail": The 'delail' element shows detail modification from source "kitten" to target "sitting".
    - "type" is enumerated in ["none", "ins", "del", "sub"]
        - 'none":  none difference between source and target
        - "ins": insertion of substring in target for substring in source
        - 'del': deletion of substring in target for substring in source
        - "sub": substitution of substring in target for substring in source
    - "src" and "tgt": substring in source and target
    - "src_i" and "tgt_i": indexes of substring in source and target
    - "cost": How many cost is added to in this modification.
- "cost": the "cost" element is the total cost of edit distance between source and target

**Example 2.** get detail modifications with morphological analysis:

If you want to compare two sentences in word, you can split them into words as the input:
```python
from distance import ded
source = 'I have a dream'
target = 'I had a dream about you'
rs = ded(source=source.split(" "), target=target.split(" "))
print(rs)
```

Output:
```json
{
  "cost": 3, 
  "detail": [
      {"src_i": [0], "src": "i", "tgt_i": [0], "tgt": "i", "type": "none", "cost": 0}, 
      {"src_i": [1], "src": "have", "tgt_i": [1], "tgt": "had", "type": "sub", "cost": 1}, 
      {"src_i": [2, 3], "src": "adream", "tgt_i": [2, 3], "tgt": "adream", "type": "none", "cost": 0}, 
      {"src_i": [], "src": "", "tgt_i": [4, 5], "tgt": "aboutyou", "type": "ins", "cost": 2}
  ]
}
```

**Example 3.** output the details in character one by one:

Setting 'is_combine_LCS' to 'False' that allows outputting details in character one by one

```python
from distance import ded
source = "kitten"
target = "sitting"
rs = ded(source=source, target=target, is_combine_LCS=False)
print(rs)
```

output:

```json
{
  "cost": 3, 
  "detail": [
      {"src": "k", "cost": 1, "type": "sub", "tgt_i": [0], "src_i": [0], "tgt": "s"}, 
      {"src": "i", "cost": 0, "type": "none", "tgt_i": [1], "src_i": [1], "tgt": "i"}, 
      {"src": "t", "cost": 0, "type": "none", "tgt_i": [2], "src_i": [2], "tgt": "t"}, 
      {"src": "t", "cost": 0, "type": "none", "tgt_i": [3], "src_i": [3], "tgt": "t"}, 
      {"src": "e", "cost": 1, "type": "sub", "tgt_i": [4], "src_i": [4], "tgt": "i"}, 
      {"src": "n", "cost": 0, "type": "none", "tgt_i": [5], "src_i": [5], "tgt": "n"}, 
      {"src": "", "cost": 1, "type": "ins", "tgt_i": [6], "src_i": [], "tgt": "g"}
  ]}

```
You can see the sub-string "itt" is split into characters.


**Example 4.** output as the least cost on source:

Such as in a typing exercise application, we need to score user typing.
The text maybe a long content, but the user can types only a part of the text.
In this case, we need find the effective typing numbers.

Setting the user typing content as source
Setting the text content as the target.
Setting 'as_least_cost' to 'True' that finds the least cost on source;


As following:

```python
from distance import ded
source = "I had a dream that my"
target = "I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin, but by the content of their character."
rs = ded(source=source.split(" "), target=target.split(" "), as_least_cost=True)
print(rs)
```

```json
{
  "detail": [
    {"tgt_i": [0], "src": "i", "type": "none", "src_i": [0], "tgt": "i", "cost": 0}, 
    {"tgt_i": [1], "src": "had", "type": "sub", "src_i": [1], "tgt": "have", "cost": 1}, 
    {"tgt_i": [2, 3, 4, 5], "src": "adreamthatmy", "type": "none", "src_i": [2, 3, 4, 5], "tgt": "adreamthatmy", "cost": 0}
  ], 
  "cost": 1
}

```
You can see only "had" in source was wrong.
Therefore the effective typing numbers should be len(source) - rs["cost"] = 6 - 1 = 5

Citation
======
Please cite our paper for any purpose of usage.
```text
@article{liao2013,
    title={Development of the Japanese Input Training System: Four Types of Training and the Fast Algorithm for Automatic Scoring},
    author={Liao, Chenyi and Minoura, Emiko and Takeoka, Saori and Ozaki Masahiro},
    journal={Proceedings of the 75th National Convention of IPSJ},
    pages={655--656},
    year={2013}
}
```

Others
======
[中文版说明](https://liaocy.net/2018/20180703-detaileditdistance/)