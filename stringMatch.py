#import nothing!

def leading_char_match(a,b):
    string_min_length = min(len(a), len(b))
    l = [list(a.lower())[x] == list(b.lower())[x] for x in list(range(0,string_min_length))]
    i=0
    while l[i]:
        i+=1
        if i==string_min_length:
            break
    return float(i/string_min_length)

def jaccard_dist(a,b):
    a_split = set(list(a.lower()))
    b_split = set(list(b.lower()))
    i = len(a_split.intersection(b_split))
    u = len(a_split.union(b_split))
    return i/u

def string_match(a,b):
    jaccard = jaccard_dist(a=a,b=b)
    leading_char = leading_char_match(a=a,b=b)
    return jaccard + leading_char
