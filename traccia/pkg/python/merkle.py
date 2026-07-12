import hashlib
import json
from typing import List, Optional, Tuple, Any

class MerkleTree:
    def __init__(self, leaves: List[str]):
        self.leaves = leaves
        self.tree = self._build_tree(leaves)
        self.root = self.tree[-1][0] if self.tree else None

    def _build_tree(self, leaves: List[str]) -> List[List[str]]:
        if not leaves:
            return []
        current_level = [self._hash(leaf) for leaf in leaves]
        tree = [current_level]
        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                if i + 1 < len(current_level):
                    combined = current_level[i] + current_level[i+1]
                else:
                    combined = current_level[i] + current_level[i]
                next_level.append(self._hash(combined))
            tree.append(next_level)
            current_level = next_level
        return tree

    def _hash(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()

    def get_root(self) -> Optional[str]:
        return self.root

    def get_proof(self, leaf_index: int) -> List[Tuple[str, str]]:
        """返回证明路径，每个元组为 (hash, side) 其中 side='L' 或 'R'"""
        if leaf_index < 0 or leaf_index >= len(self.leaves):
            raise ValueError("Leaf index out of range")
        proof = []
        idx = leaf_index
        for level in range(len(self.tree) - 1):
            siblings = self.tree[level]
            if idx % 2 == 0:
                # 当前是左节点，兄弟在右边
                if idx + 1 < len(siblings):
                    proof.append((siblings[idx + 1], 'R'))
                else:
                    proof.append((siblings[idx], 'S'))  # 自己，无兄弟
            else:
                # 当前是右节点，兄弟在左边
                proof.append((siblings[idx - 1], 'L'))
            idx //= 2
        return proof

    def verify_proof(self, leaf: str, proof: List[Tuple[str, str]], root: str) -> bool:
        """验证证明，使用位置信息"""
        current = self._hash(leaf)
        for sibling, side in proof:
            if side == 'L':
                combined = sibling + current
            elif side == 'R':
                combined = current + sibling
            else:
                combined = current + sibling  # 只有一个节点，自己组合
            current = self._hash(combined)
        return current == root

    def to_dict(self) -> dict:
        return {
            "root": self.root,
            "leaves": self.leaves,
            "tree": self.tree
        }