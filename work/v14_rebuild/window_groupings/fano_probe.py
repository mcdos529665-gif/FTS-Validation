"""Crosscheck user's Fano orientation against stored O8/H4; no FTS status decision."""
from __future__ import annotations
import argparse,hashlib,itertools,json
from pathlib import Path
TRIPLES=((4,1,6),(6,3,2),(2,5,4),(6,7,5),(4,7,3),(2,7,1),(1,3,5))
LABELS={0:0,1:1,2:2,3:4,4:7,5:5,6:6,7:3}

def check(root:Path)->dict:
    src=root/'work/v14_rebuild/e5_literature_review/window_signed_products_2026-10-06/RESULTS.json'
    raw=src.read_bytes();saved=json.loads(raw)
    oct_eps=saved['models']['O8']['epsilon_table'];h_eps=saved['models']['H4']['epsilon_table']
    table={(0,i):(1,i) for i in range(8)};table.update({(i,0):(1,i) for i in range(8)})
    table.update({(i,i):(-1,0) for i in range(1,8)});pairs=[]
    for a,b,c in TRIPLES:
        for i,j,k in ((a,b,c),(b,c,a),(c,a,b)):
            assert (i,j) not in table and (j,i) not in table
            table[i,j]=(1,k);table[j,i]=(-1,k)
            assert LABELS[i]^LABELS[j]==LABELS[k]
            pairs.append(frozenset((i,j)))
    assert len(table)==64 and len(set(pairs))==21
    def mul(x,y):
        sign,k=table[x[1],y[1]];return x[0]*y[0]*sign,k
    e=lambda i:(1,i)
    signs={0:1,1:1,2:1,3:1,4:-1,5:-1,6:1,7:1}
    for i,j in itertools.product(range(8),repeat=2):
        sign,k=table[i,j]
        assert LABELS[k]==LABELS[i]^LABELS[j]
        assert sign*signs[k]==signs[i]*signs[j]*oct_eps[LABELS[i]][LABELS[j]]
    for triple in TRIPLES:
        sub=(0,*triple)
        for i,j,k in itertools.product(sub,repeat=3):
            assert mul(mul(e(i),e(j)),e(k))==mul(e(i),mul(e(j),e(k)))
    sub=(0,1,2,7)
    for i,j in itertools.product(sub,repeat=2):
        sign,k=table[i,j]
        assert sign==h_eps[LABELS[i]][LABELS[j]] and LABELS[k]==LABELS[i]^LABELS[j]
    cycles={}
    for i in range(1,8):
        path=[e(0)]
        for _ in range(4):path.append(mul(path[-1],e(i)))
        assert path==[(1,0),(1,i),(-1,0),(-1,i),(1,0)];cycles[str(i)]=path
    left=mul(mul(e(1),e(2)),e(3));right=mul(e(1),mul(e(2),e(3)))
    assert left==(1,4) and right==(-1,4)
    seq=[mul(e(i),e(i+1)) for i in range(1,7)]
    assert seq==[(1,7),(-1,6),(1,7),(-1,2),(1,7),(1,5)]
    coords={sum(int(b)<<i for i,b in enumerate(v)):int(k) for k,v in saved['coordinates24'].items()}
    assert [coords[LABELS[i]]%12 for i in sub]==[1,7,5,11]
    mapping=[dict(diagram_index=i,model_label=LABELS[i],model_sign=signs[i],residue_mod24=coords[LABELS[i]]) for i in range(8)]
    return dict(status='PASS',scope='user Fano orientation; stored O8/H4 only',source_results_sha256=hashlib.sha256(raw).hexdigest(),oriented_triples=TRIPLES,basis_products_checked=64,quaternion_lines_checked=7,line_associativity_triples_checked=448,H4_line_products_checked=16,diagram_to_model=mapping,cycles=cycles,successive_products=seq,grouping_example=dict(left=left,right=right),FTS_status_effect='none; no level or U7 minimality established',independent_external_CAS='not performed')

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[3]);p.add_argument('--output',type=Path);p.add_argument('--check',action='store_true')
    a=p.parse_args();data=check(a.root.resolve());encoded=(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode()
    out=a.output or Path(__file__).with_name('FANO_RESULTS.json')
    if a.check:assert out.read_bytes()==encoded,'stored Fano witness is stale'
    else:out.write_bytes(encoded)
    print('PASS Fano: 64 products, 7 quaternion lines, 16 H4 products; FTS mapping remains candidate')
if __name__=='__main__':main()
