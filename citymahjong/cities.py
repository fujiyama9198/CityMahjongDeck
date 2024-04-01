import csv
import pathlib

_characters_src = [
    ("川", 4),
    ("大", 3),
    ("島", 3),
    ("野", 3),
    ("山", 3),
    ("田", 3),
    ("南", 2),
    ("津", 2),
    ("東", 2),
    ("上", 2),
    ("松", 2),
    ("小", 2),
    ("富", 2),
    ("原", 2),
    ("高", 2),
    ("北", 1),
    ("中", 1),
    ("美", 1),
    ("三", 1),
    ("城", 1),
    ("西", 1),
    ("崎", 1),
    ("長", 1),
    ("豊", 1),
    ("佐", 1),
    ("戸", 1),
    ("平", 1),
    ("日", 1),
    ("井", 1),
    ("浜", 1),
    ("岡", 1),
    ("本", 1),
    ("吉", 1),
    ("木", 1),
    ("内", 1),
    ("和", 1),
    ("白", 1),
    ("見", 1),
    ("郷", 1),
    ("江", 1),
    ("新", 1),
    ("宮", 1),
    ("賀", 1),
    ("河", 1),
    ("泉", 1),
    ("士", 1),
    ("古", 1),
    ("越", 1),
    ("国", 1),
    ("坂", 1),
    ("下", 1),
    ("海", 1),
    ("里", 1),
    ("久", 1),
    ("浦", 1),
    ("福", 1),
    ("石", 1),
    ("宇", 1),
    ("知", 1),
    ("玉", 1),
    ("多", 1),
    ("加", 1),
    ("神", 1),
    ("広", 1),
    ("村", 1),
    ("岩", 1),
    ("清", 1),
    ("伊", 1),
    ("庄", 1),
    ("良", 1),
    ("谷", 1),
    ("鹿", 1),
    ("水", 1),
    ("幌", 1),
    ("土", 1),
    ("阿", 1),
    ("根", 1),
    ("前", 1),
    ("部", 1),
    ("生", 1),
    ("波", 1),
    ("府", 1),
    ("沢", 1),
    ("須", 1),
    ("安", 1),
    ("市", 1),
    ("沼", 1),
    ("米", 1),
    ("別", 1),
    ("瀬", 1),
    ("飯", 1),
    ("金", 1),
    ("熊", 1),
    ("横", 1),
    ("立", 1),
    ("都", 1),
    ("屋", 1),
    ("手", 1),
    ("関", 1),
    ("取", 1),
    ("丹", 1),
    ("五", 1),
    ("名", 1),
    ("羽", 1),
    ("子", 1),
    ("会", 1),
    ("阪", 1),
    ("京", 1),
    ("尾", 1),
    ("十", 1),
    ("奈", 1),
    ("八", 1),
    ("倉", 1),
    ("口", 1),
]


# All character cards with duplicates
characters = []
for c, n in _characters_src:
    characters.extend([c] * n)
assert len(characters) == 136
character_set = set(characters)


with open(pathlib.Path(__file__).parent / "list.csv", "r") as f:
    all_city_names = [n[2] for n in csv.reader(f) if n[2][-1] in {"市", "町", "村"}]

# All city/town/village names (including "impossible" names with the character set)
all_city_names = [n[:-1] for n in all_city_names]

# All possible city/town/village names (including duplicates like "横浜(市)" and "横浜(町)")
possible_names = []

# Dictionary of lists of possible names for each character
character_candidates = {}
for name in all_city_names:
    if all((c in character_set) for c in name):
        possible_names.append(name)
        for c in name:
            character_candidates.setdefault(c, []).append(name)

# All character cards with its possible city/town/village names
character_numbers = [(c, len(character_candidates[c])) for c in characters]
