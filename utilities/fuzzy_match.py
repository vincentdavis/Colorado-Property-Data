

import string
#
# http://blog.yhathq.com/posts/fuzzy-matching-with-yhat.html


def normalize_address(field):
    # Normalize an address field
    field = field.lower()
    field = ''.join(x for x in field if x not in set(string.punctuation))
    return field


def normalize_name(name):
    # nomalize a name
    # Todo remove LLC
    name = name.lower()
    name = ''.join(x for x in name if x not in set(string.punctuation))
    # name = re.sub("\w+[ ]+(llc[., ]+)\w+","",data)
    return name
