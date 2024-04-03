import citymahjong
from typing import List, Tuple, Optional, Union


class CityNameTrieNode:
    def __init__(self, idx=None) -> None:
        super().__init__()
        self.dst: List[Tuple[str, CityNameTrieNode]] = []
        self.failure:Optional[CityNameTrieNode] = None
        self.match: List[Tuple[str, str]] = []
        self.idx: Optional[int] = idx
        self.has_match = False
    
    def visualize(self, count=0):
        for ch, node in self.dst:
            if node.match:
                tail_space = "-" * (16 - count*2)
                match = ", ".join([f"{cn}({pn})" for cn, pn in node.match])
            else:
                tail_space = ""
                match = ""
            failure_idx_str = f"(->{node.failure.idx:3d})" if node.failure else "       "
            print("{idx:3d}: {lead_space:{lead_len}s}{ch} {failure_idx_str} {tail_space} {match}".format(
                lead_space="", lead_len=count*2,
                idx=node.idx,
                ch = ch,
                tail_space=tail_space,
                failure_idx_str=failure_idx_str,
                match=match
            ))
            node.visualize(count + 1)
    
    def reset(self):
        self.has_match = False
        for _, node in self.dst:
            node.reset()


def add_city_to_tree(cityname: str, prefecture:str, fullname:str, root: Optional[CityNameTrieNode] = None):
    if cityname is None or len(cityname) == 0:
        raise ValueError("string must not be empty")
    
    if root is None:
        root = CityNameTrieNode()
    
    def _add(node:CityNameTrieNode, substring: str, prefecture:str, fullname:str):
        if len(substring) == 0:
            node.match.append((fullname, prefecture))
            return node
        ch = substring[0]
        next_node = None
        for c, n in node.dst:
            if c == ch:
                next_node = n
                break
        if next_node is None:
            next_node = CityNameTrieNode()
            node.dst.append((ch, next_node))
        return _add(next_node, substring[1:], prefecture, fullname)
    
    def _get_failure(node:CityNameTrieNode, root:CityNameTrieNode, ch:str):
        if node.failure is None:
            assert node == root
            return node
        for next_ch, next_node in node.failure.dst:
            if next_ch == ch:
                return next_node
        return _get_failure(node.failure, root, ch)
    
    def _build_failure(node:CityNameTrieNode, root:CityNameTrieNode):
        for next_ch, next_node in node.dst:
            if next_node.failure is None:
                next_node.failure = _get_failure(node, root, next_ch)
        for next_ch, next_node in node.dst:
            _build_failure(next_node, root)
    
    def _enumerate_idx(node:CityNameTrieNode, idx:int):
        node.idx = idx
        latest_idx = idx
        for _, new_node in node.dst:
            latest_idx = _enumerate_idx(new_node, latest_idx + 1)
        return latest_idx
    
    _add(root, cityname, prefecture, fullname)
    _build_failure(root, root)
    _enumerate_idx(root, 0)
    return root





root = None

use_sorted = True
# use_sorted = False
if use_sorted:
    citynames = sorted(
        citymahjong.cities.possible_names_with_prefecture,
        key=lambda x: tuple(citymahjong.cities.character_codes[ch] for ch in x[0])
    )
else:
    citynames = citymahjong.cities.possible_names_with_prefecture

for name, prefecture, fullname in citynames:
   name = "".join(sorted(name, key=lambda x: citymahjong.cities.character_codes[x]))
#    print(name)
   root = add_city_to_tree(name, prefecture, fullname, root)

root.visualize()

