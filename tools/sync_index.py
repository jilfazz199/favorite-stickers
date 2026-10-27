"""Discover uploads, inspect actual formats, and prepare previews without guessing meanings."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
FORMAT_INFO = {'JPEG': ('image/jpeg', '.jpg'), 'PNG': ('image/png', '.png'),
               'GIF': ('image/gif', '.gif'), 'WEBP': ('image/webp', '.webp')}


def sync(root=ROOT, check=False):
    root = Path(root)
    index = root / 'index.json'
    data = json.loads(index.read_text(encoding='utf-8'))
    entries = {item['path']: item for item in data['stickers']}
    problems = []; added = 0; updated = []
    for source in sorted((root / 'stickers').rglob('*')):
        if not source.is_file() or source.suffix.lower() not in EXTENSIONS:
            continue
        relative = source.relative_to(root).as_posix()
        payload = source.read_bytes(); digest = hashlib.sha256(payload).hexdigest()
        item = entries.get(relative)
        if item is None:
            problems.append({'path': relative, 'problem': 'unindexed'})
            if check: continue
            item = {'id': digest[:16], 'name': '待标注_' + source.stem, 'path': relative,
                'tags': [], 'use_cases': [], 'visible_text': '', 'description': '', 'meaning': '',
                'source': '用户上传到仓库', 'author': '未知', 'license': '未确认',
                'review_status': 'pending', 'avoid_when': [], 'interpretation_note': '尚未实际看图，不猜含义。'}
            added += 1
        elif item.get('sha256') != digest:
            problems.append({'path': relative, 'problem': 'changed_since_review'})
            if check: continue
            item['review_status'] = 'needs_review'
            item.pop('visual_review', None)
        with Image.open(source) as image:
            fmt = image.format
            if fmt not in FORMAT_INFO:
                raise ValueError('不支持的实际图片格式：' + relative)
            mime, extension = FORMAT_INFO[fmt]
            frame_count = getattr(image, 'n_frames', 1)
            indices = sorted({0, frame_count // 2, frame_count - 1}) if frame_count > 1 else [0]
            previews = [f'previews/{digest[:16]}/frame-{n:03d}.png' for n in indices]
            delivery = f'delivery/{digest[:16]}{extension}'
            metadata = {'sha256': digest, 'bytes': len(payload), 'actual_format': fmt,
                'media_type': mime, 'animated': frame_count > 1, 'frame_count': frame_count,
                'width': image.width, 'height': image.height, 'preview_paths': previews,
                'delivery_path': delivery,
                'extension_matches_format': source.suffix.lower() in (('.jpg', '.jpeg') if fmt == 'JPEG' else (extension,))}
            if check:
                if any(item.get(k) != v for k, v in metadata.items()):
                    problems.append({'path': relative, 'problem': 'media_metadata_outdated'})
                for preview, n in zip(previews, indices):
                    preview_path = root / preview
                    if not preview_path.is_file():
                        problems.append({'path': preview, 'problem': 'missing_preview'})
                    else:
                        image.seek(n)
                        with Image.open(preview_path) as actual:
                            expected = image.convert('RGBA')
                            if actual.size != expected.size or actual.convert('RGBA').tobytes() != expected.tobytes():
                                problems.append({'path': preview, 'problem': 'preview_mismatch'})
                if not (root / delivery).is_file() or (root / delivery).read_bytes() != payload:
                    problems.append({'path': delivery, 'problem': 'delivery_mismatch'})
            else:
                for preview, n in zip(previews, indices):
                    image.seek(n)
                    target = root / preview; target.parent.mkdir(parents=True, exist_ok=True)
                    image.convert('RGBA').save(target, format='PNG')
                target = root / delivery; target.parent.mkdir(parents=True, exist_ok=True)
                if not target.is_file() or target.read_bytes() != payload:
                    shutil.copyfile(source, target)
                item.update(metadata)
                item.setdefault('review_status', 'pending')
                updated.append(item)
    for item in data['stickers']:
        resolved = (root / item['path']).resolve()
        if not resolved.is_relative_to((root / 'stickers').resolve()):
            raise ValueError('索引路径超出 stickers 目录。')
        if not resolved.is_file():
            problems.append({'path': item['path'], 'problem': 'missing_original'})
            if not check: updated.append({**item, 'review_status': 'missing'})
    if not check:
        data['schema_version'] = 2
        data['stickers'] = sorted(updated, key=lambda item: item['path'])
        index.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        from add_sticker import render_gallery
        # render_gallery is also used by the import command.
        render_gallery(data, root=root)
    return {'ok': not problems if check else True, 'added': added, 'total': len(data['stickers']),
            'pending': sum(s.get('review_status') != 'reviewed' for s in data['stickers']), 'issues': problems}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='发现新图、生成看图预览与正确后缀的原始文件副本，不自动编造标签。')
    parser.add_argument('--check', action='store_true', help='只检查，不修改文件')
    args = parser.parse_args()
    result = sync(check=args.check)
    print(json.dumps(result, ensure_ascii=False))
    if args.check and not result['ok']: raise SystemExit(1)
