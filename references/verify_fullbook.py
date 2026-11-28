#!/usr/bin/env python3
"""verify_fullbook.py — 翻译成品全书终验三防线一键扫描（泛化自蓝皮书 scan_v20_* 系列）

用法:
  python3 verify_fullbook.py <原书.pdf> <成品.pdf> [--out 候选输出.json]

包含三道防线:
  1) redact 截断扫描（坑27）: 成品 span 为同位置原书 span 真前缀/真后缀残段（严格判据），
     另附 english_short 宽线索供人工分诊（假阳性极高，不可直接当缺陷）。
  2) 黑底/SMask 扫描（坑28/29）: 逐页低倍渲染统计近黑像素占比（>30% 计嫌疑页），
     并列出带 SMask 图像（图像替换工艺需确认 SMask 未丢失）。
  3) 页数一致性: 两版页数核对。

输出: 终端摘要 + JSON 候选清单。严格判据命中才视为疑似缺陷，需人工复核后定点修。
"""
import argparse, json, re, sys
from collections import Counter
import fitz

LATIN = re.compile(r'[A-Za-z]')

def spans(page):
    out = []
    for b in page.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for l in b['lines']:
            for s in l['spans']:
                t = s['text']
                if t.strip():
                    out.append({'text': t, 'bbox': s['bbox'], 'size': round(s['size'], 1)})
    return out

def overlap(a, b):
    x0 = max(a[0], b[0]); y0 = max(a[1], b[1])
    x1 = min(a[2], b[2]); y1 = min(a[3], b[3])
    if x1 <= x0 or y1 <= y0:
        return 0.0
    inter = (x1 - x0) * (y1 - y0)
    area = (a[2] - a[0]) * (a[3] - a[1])
    return inter / area if area else 0.0

def scan_truncation(doc_o, doc_v):
    cands = []
    for pno in range(min(len(doc_o), len(doc_v))):
        po = spans(doc_o[pno]); pv = spans(doc_v[pno])
        for so in po:
            to = so['text'].strip()
            if not LATIN.search(to) or len(to) < 4:
                continue
            for sv in pv:
                tv = sv['text'].strip()
                if not tv or tv == to:
                    continue
                ov = overlap(so['bbox'], sv['bbox'])
                if ov < 0.55:
                    continue
                if (to.startswith(tv) or to.endswith(tv)) and 3 <= len(tv) < len(to):
                    cands.append({'pno': pno, 'type': 'prefix_suffix', 'orig': to, 'new': tv,
                                  'bbox': [round(x, 1) for x in sv['bbox']], 'size': sv['size']})
                elif LATIN.search(tv) and len(tv) < len(to) and ov > 0.8 and len(tv) >= 3:
                    cands.append({'pno': pno, 'type': 'english_short', 'orig': to, 'new': tv,
                                  'bbox': [round(x, 1) for x in sv['bbox']], 'size': sv['size']})
    return cands

def scan_blackbg(doc_v, dark_thresh=24, frac_thresh=0.30):
    flags, smask_pages = [], []
    for i, page in enumerate(doc_v):
        for img in page.get_images(full=True):
            xref = img[0]
            if doc_v.xref_get_key(xref, 'SMask')[0] != 'null':
                smask_pages.append(i + 1)
        pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5), colorspace=fitz.csGRAY)
        s = pix.samples
        frac = sum(1 for v in s if v < dark_thresh) / (pix.width * pix.height)
        if frac > frac_thresh:
            flags.append({'pno': i + 1, 'dark_frac': round(frac, 3)})
    return flags, sorted(set(smask_pages))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('original'); ap.add_argument('translated')
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    doc_o = fitz.open(a.original); doc_v = fitz.open(a.translated)
    print(f'pages: original={len(doc_o)} translated={len(doc_v)}'
          + ('' if len(doc_o) == len(doc_v) else '  << 页数不一致，需人工核查'))

    trunc = scan_truncation(doc_o, doc_v)
    strict = [c for c in trunc if c['type'] == 'prefix_suffix']
    loose = [c for c in trunc if c['type'] == 'english_short']
    dark, smask = scan_blackbg(doc_v)

    print(f'[防线1 redact截断] 严格判据命中: {len(strict)}  （english_short 宽线索 {len(loose)} 项仅供分诊，假阳性极高）')
    for c in strict[:20]:
        print(f"  p{c['pno']+1} {c['type']}: orig={c['orig'][:50]!r} -> new={c['new'][:50]!r}")
    print(f"[防线2 黑底/SMask] 黑底嫌疑页: {len(dark)} {dark[:10]}")
    print(f'  带 SMask 图像页数: {len(smask)} （若成品做过图像替换，需确认 SMask 未丢失）')

    if a.out:
        json.dump({'strict': strict, 'loose': loose, 'dark_pages': dark, 'smask_pages': smask},
                  open(a.out, 'w'), ensure_ascii=False, indent=1)
        print('saved', a.out)
    sys.exit(1 if strict or dark else 0)

if __name__ == '__main__':
    main()
