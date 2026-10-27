"""Import a user-selected sticker without editing its bytes or calling any service."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def values(text):
    return list(dict.fromkeys(x.strip() for x in re.split('[,，、]', text) if x.strip()))


def render_gallery(data):
    def cell(text):
        return str(text).replace('|', '\\|').replace('\n', ' ')
    lines = ['| 图片 | 名称 | 情绪 | 场景 |', '| --- | --- | --- | --- |']
    for item in data['stickers']:
        path = item['path']
        lines.append(f'| <img src="{path}" width="140" alt="收藏表情"> | '
                     f'{cell(item["name"])} | {cell("、".join(item["tags"]))} | '
                     f'{cell("、".join(item["use_cases"]))} |')
    readme = ROOT / 'README.md'
    text = readme.read_text(encoding='utf-8')
    start = '<!-- GALLERY:START -->'
    end = '<!-- GALLERY:END -->'
    before, rest = text.split(start, 1)
    _, after = rest.split(end, 1)
    readme.write_text(before + start + '\n' + '\n'.join(lines) + '\n' + end + after,
                      encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='添加表情包并更新文字索引与图册。')
    parser.add_argument('image', type=Path)
    parser.add_argument('--name', required=True)
    parser.add_argument('--tags', default='')
    parser.add_argument('--text', default='', help='图片上的实际文字，无法确定时留空')
    parser.add_argument('--description', default='')
    parser.add_argument('--scene', default='')
    parser.add_argument('--source', default='用户提供')
    args = parser.parse_args()
    source = args.image.resolve()
    if not source.is_file() or source.suffix.lower() not in EXTENSIONS:
        parser.error('请选择现有的 JPG、PNG、GIF 或 WebP 图片文件。')
    if not args.name.strip():
        parser.error('名称不能为空。')
    payload = source.read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    index = ROOT / 'index.json'
    data = json.loads(index.read_text(encoding='utf-8'))
    duplicate = next((s for s in data['stickers'] if s['sha256'] == digest), None)
    if duplicate:
        print(json.dumps({'added': False, 'reason': '图片已收藏', 'path': duplicate['path']}, ensure_ascii=False))
        return
    relative = 'stickers/' + digest[:16] + source.suffix.lower()
    destination = ROOT / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        parser.error('目标文件已存在且未在索引中登记，请先检查索引。')
    shutil.copyfile(source, destination)
    data['stickers'].append({
        'id': digest[:16], 'name': args.name.strip(), 'path': relative,
        'tags': values(args.tags), 'use_cases': values(args.scene),
        'visible_text': args.text, 'description': args.description,
        'source': args.source, 'author': '未知', 'license': '未确认',
        'sha256': digest, 'bytes': len(payload),
    })
    index.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    render_gallery(data)
    print(json.dumps({'added': True, 'path': relative, 'total': len(data['stickers'])}, ensure_ascii=False))


if __name__ == '__main__':
    main()
