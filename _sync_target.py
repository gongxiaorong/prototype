import json, os, re

WS = r'e:/test/prototype/merchant/locales'
TGT = r'E:\Open Design\9bb5c4ac-2a38-4455-8e5c-bca098259906\locales'

def flat(d, pre=''):
    r = {}
    if isinstance(d, dict):
        for k, v in d.items():
            r.update(flat(v, pre + '.' + k if pre else k))
    else:
        r[pre] = d
    return r

def setval(d, path, val):
    parts = path.split('.')
    cur = d
    for p in parts[:-1]:
        if p not in cur or not isinstance(cur[p], dict):
            cur[p] = {}
        cur = cur[p]
    cur[parts[-1]] = val

for lang in ['en', 'id', 'zh-HK', 'zh-CN']:
    wf = os.path.join(WS, lang + '.json')
    tf = os.path.join(TGT, lang + '.json')
    with open(wf, encoding='utf-8') as f:
        raw_w = f.read()
    with open(tf, encoding='utf-8') as f:
        raw_t = f.read()
    w, t = json.loads(raw_w), json.loads(raw_t)
    fw, ft = flat(w), flat(t)
    diffs = [k for k in fw if k not in ft or fw[k] != ft[k]]
    if not diffs:
        print(lang + ': 已一致，无写入')
        continue
    for k in diffs:
        setval(t, k, fw[k])
    m = re.search(r'\n([ \t]+)"', raw_t)
    indent = len(m.group(1)) if (m and set(m.group(1)) <= {' ', '\t'}) else 2
    trailing = raw_t.endswith('\n')
    with open(tf, 'w', encoding='utf-8') as f:
        f.write(json.dumps(t, ensure_ascii=False, indent=indent))
        if trailing:
            f.write('\n')
    print(lang + ': target written, ' + str(len(diffs)) + ' keys')

# verify
print('--- verify ---')
for lang in ['en', 'id', 'zh-HK', 'zh-CN']:
    w = json.load(open(os.path.join(WS, lang + '.json'), encoding='utf-8'))
    t = json.load(open(os.path.join(TGT, lang + '.json'), encoding='utf-8'))
    print(lang + ': merchant==target -> ' + str(w == t))
