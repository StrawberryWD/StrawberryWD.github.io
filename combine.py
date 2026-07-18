#!/usr/bin/env python3
"""
combine.py

递归扫描指定路径（默认当前目录），将可读的文本文件按文件头顺序写入一个输出 txt。

用法:
  python combine.py            # 在当前目录递归查找文本文件，输出到 combined.txt
  python combine.py -o out.txt folder1 file2.html

输出格式：每个文件前会有分隔线和 `FILE: 相对路径` 的清晰头部。
"""

from __future__ import annotations
import os
import sys
import argparse

def is_text_file(path: str) -> bool:
    try:
        with open(path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return False
            try:
                chunk.decode('utf-8')
                return True
            except UnicodeDecodeError:
                try:
                    chunk.decode('latin-1')
                    return True
                except Exception:
                    return False
    except Exception:
        return False

def gather_files(paths: list[str]) -> list[str]:
    files: list[str] = []
    for p in paths:
        if os.path.isdir(p):
            for root, _, filenames in os.walk(p):
                for fn in filenames:
                    files.append(os.path.join(root, fn))
        elif os.path.isfile(p):
            files.append(p)
    files.sort()
    return files

def main() -> None:
    parser = argparse.ArgumentParser(description='Combine text files into one readable txt.')
    parser.add_argument('paths', nargs='*', default=['.'], help='Files or directories to include (default: .)')
    parser.add_argument('-o', '--output', default='combined.txt', help='Output file name (default: combined.txt)')
    args = parser.parse_args()

    files = gather_files(args.paths)
    written = 0
    sep = '=' * 80
    with open(args.output, 'w', encoding='utf-8') as out:
        for f in files:
            if not is_text_file(f):
                continue
            try:
                rel = os.path.relpath(f)
                out.write(sep + '\n')
                out.write(f'FILE: {rel}\n')
                out.write('-' * 80 + '\n')
                with open(f, 'r', encoding='utf-8', errors='replace') as inp:
                    out.write(inp.read())
                out.write('\n\n')
                written += 1
            except Exception as e:
                out.write(f'[!ERROR reading {f}: {e}]\n\n')

    print(f'Wrote {written} files into {args.output}')

if __name__ == '__main__':
    main()
