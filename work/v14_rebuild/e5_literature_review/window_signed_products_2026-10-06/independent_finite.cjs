// Independent integer implementation: quaternion vectors, real matrices, H-pairs.
// This is a local finite proof, not a successful external CAS evaluation.
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const eq = (a, b) => a.length === b.length && a.every((x, i) => x === b[i]);
const add = (a, b) => a.map((x, i) => x + b[i]);
const sub = (a, b) => a.map((x, i) => x - b[i]);
const scale = (s, a) => a.map(x => s * x);
const unit = (n, k) => Array.from({length: n}, (_, i) => +(i === k));
const conj = a => [a[0], -a[1], -a[2], -a[3]];
function quaternion(a, b) {
  return [
    a[0]*b[0]-a[1]*b[1]-a[2]*b[2]-a[3]*b[3],
    a[0]*b[1]+a[1]*b[0]+a[2]*b[3]-a[3]*b[2],
    a[0]*b[2]+a[2]*b[0]+a[3]*b[1]-a[1]*b[3],
    a[0]*b[3]+a[3]*b[0]+a[1]*b[2]-a[2]*b[1]
  ];
}
function matrix(a, b) {
  return [a[0]*b[0]+a[1]*b[2], a[0]*b[1]+a[1]*b[3],
          a[2]*b[0]+a[3]*b[2], a[2]*b[1]+a[3]*b[3]];
}
function octonion(a, b) {
  const x=a.slice(0,4), y=a.slice(4), u=b.slice(0,4), v=b.slice(4);
  return sub(quaternion(x,u), quaternion(v,conj(y)))
    .concat(add(quaternion(conj(x),v), quaternion(u,y)));
}
const basisH = Array.from({length:4}, (_, i) => unit(4, i));
const basisS = [[1,0,0,1], [0,-1,1,0], [1,0,0,-1], [0,1,1,0]];
const basisO = Array.from({length:8}, (_, i) => unit(8, i));
function decode(basis, value) {
  for (let g=0; g<basis.length; g++) for (const s of [-1,1]) {
    if (eq(value, scale(s,basis[g]))) return [s,g];
  }
  throw new Error('Product outside the signed basis');
}
function audit(basis, product) {
  const n=basis.length, table=[], signed=[];
  for (let g=0; g<n; g++) {
    table[g]=[];
    for (let h=0; h<n; h++) {
      table[g][h]=decode(basis,product(basis[g],basis[h]));
      assert.equal(table[g][h][1],g^h);
    }
    for (const s of [-1,1]) signed.push([s,g]);
  }
  const mult=(a,b)=>[a[0]*b[0]*table[a[1]][b[1]][0],a[1]^b[1]];
  let commFail=0, assocFail=0, first=null;
  for (let g=0; g<n; g++) for (let h=0; h<n; h++) {
    if (!eq(product(basis[g],basis[h]),product(basis[h],basis[g]))) commFail++;
    for (let k=0; k<n; k++) {
      const left=product(product(basis[g],basis[h]),basis[k]);
      const right=product(basis[g],product(basis[h],basis[k]));
      if (!eq(left,right)) {assocFail++; first ??= [g,h,k];}
    }
  }
  for (const a of signed) for (const b of signed) for (const c of signed) {
    const left=mult(mult(a,b),c), right=mult(a,mult(b,c));
    assert.equal(left[1],right[1]);
    assert.equal(left[1],a[1]^b[1]^c[1]);
  }
  const result={negativeSquares:table.slice(1).filter((r,i)=>r[i+1][0]===-1).length,
    noncommutingPairs:commFail, nonassociativeTriples:assocFail,
    firstAssociatorCounterexample:first, table};
  if(n===8) result.independentTriple=[
    decode(basis,product(product(basis[1],basis[2]),basis[4])),
    decode(basis,product(basis[1],product(basis[2],basis[4])))];
  if(n===4) {
    const invJ=scale(table[3][3][0],basis[3]);
    // The conjugation map is R-linear, so 1 and I suffice for all x+yI.
    assert(eq(product(product(basis[3],basis[0]),invJ),basis[0]));
    assert(eq(product(product(basis[3],basis[1]),invJ),scale(-1,basis[1])));
    result.innerConjugationOnComplexBasis=[1,-1];
  }
  return result;
}
const results={H4:audit(basisH,quaternion), S4:audit(basisS,matrix),
               O8:audit(basisO,octonion)};
assert.deepEqual([results.H4.negativeSquares,results.S4.negativeSquares,
                  results.O8.negativeSquares],[3,1,7]);
assert.equal(results.H4.nonassociativeTriples,0);
assert.equal(results.S4.nonassociativeTriples,0);
assert.equal(results.O8.nonassociativeTriples,168);
assert.deepEqual(results.O8.independentTriple,[[-1,7],[1,7]]);
const original=JSON.parse(fs.readFileSync(path.join(__dirname,'RESULTS.json'),'utf8'));
for (const name of Object.keys(results)) {
  assert.deepEqual(results[name].table.map(row=>row.map(entry=>entry[0])),
                   original.models[name].epsilon_table);
}
const output={status:'PASS', method:'independent local integer implementation',
  external_CAS_status:'inconclusive', models:results};
fs.writeFileSync(path.join(__dirname,'INDEPENDENT_FINITE.json'),JSON.stringify(output,null,2)+'\n');
process.stdout.write('PASS: independent vector/matrix/H-pair products match all H4/S4/O8 tables.\n');
