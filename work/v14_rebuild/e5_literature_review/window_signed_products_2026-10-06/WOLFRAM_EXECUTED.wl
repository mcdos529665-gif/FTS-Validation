ClearAll["Global`*"];
bit[g_, i_] := Mod[Quotient[g, 2^(i - 1)], 2];
eT[g_, h_] := 1;
eC[g_, h_] := (-1)^(bit[g, 1] bit[h, 1] + bit[g, 2] bit[h, 2]);
eH[g_, h_] := (-1)^(bit[g, 1] bit[h, 1] + bit[g, 2] bit[h, 2] + bit[g, 2] bit[h, 1]);
eS[g_, h_] := (-1)^(bit[g, 1] bit[h, 1] + bit[g, 2] bit[h, 1]);
eN[g_, h_] := If[g == h && g != 0, -1, 1];
eB[g_, h_] := eH[Mod[g, 4], Mod[h, 4]];
sb[d_] := Flatten[Table[{q, g}, {q, {-1, 1}}, {g, 0, 2^d - 1}], 1];
smul[ep_][{q_, g_}, {r_, h_}] := {q r ep[g, h], BitXor[g, h]};
proj[{q_, g_}] := g;

fin[ep_, d_] := Module[{v = sb[d], m = smul[ep], com, ass, cw, aw},
  com = And @@ Flatten[Table[m[a, b] == m[b, a], {a, v}, {b, v}]];
  ass = And @@ Flatten[Table[
    m[m[a, b], c] == m[a, m[b, c]], {a, v}, {b, v}, {c, v}
  ]];
  cw = Select[
    Tuples[v, 2],
    m[#[[1]], #[[2]]] != m[#[[2]], #[[1]]] &,
    1
  ];
  aw = Select[
    Tuples[v, 3],
    m[m[#[[1]], #[[2]]], #[[3]]] !=
      m[#[[1]], m[#[[2]], #[[3]]]] &,
    1
  ];
  <|
    "negativeSquares" -> Count[Table[ep[g, g], {g, 1, 2^d - 1}], -1],
    "commutative" -> com,
    "associative" -> ass,
    "nonassociativeTriples" -> Count[
      Flatten[Table[
        m[m[a, b], c] != m[a, m[b, c]],
        {a, v}, {b, v}, {c, v}
      ]],
      True
    ],
    "commutatorWitness" -> cw,
    "associatorWitness" -> aw
  |>
];

models = {
  {"T4", eT, 2}, {"C4", eC, 2}, {"H4", eH, 2}, {"S4", eS, 2},
  {"N4", eN, 2}, {"T8", eT, 3}, {"B8", eB, 3}
};
finiteTables = Association @@ (#[[1]] -> fin[#[[2]], #[[3]]] & /@ models);

projectionChecks = Association @@ (
  #[[1]] -> And @@ Join[
    Flatten[Table[
      proj[smul[#[[2]]][a, b]] == BitXor[a[[2]], b[[2]]],
      {a, sb[#[[3]]]}, {b, sb[#[[3]]]}
    ]],
    Flatten[Table[
      proj[smul[#[[2]]][smul[#[[2]]][a, b], c]] ==
        BitXor[a[[2]], b[[2]], c[[2]]] &&
      proj[smul[#[[2]]][a, smul[#[[2]]][b, c]]] ==
        BitXor[a[[2]], b[[2]], c[[2]]],
      {a, sb[#[[3]]]}, {b, sb[#[[3]]]}, {c, sb[#[[3]]]}
    ]]
  ] & /@ models
);

hvec[p_] := UnitVector[4, p + 1];
hadd[a_, b_] := a + b;
hneg[a_] := -a;
hconj[a_] := {a[[1]], -a[[2]], -a[[3]], -a[[4]]};
hmul[a_, b_] := Sum[
  a[[p + 1]] b[[q + 1]] eH[p, q] hvec[BitXor[p, q]],
  {p, 0, 3}, {q, 0, 3}
];
obasis[g_] := If[
  g < 4,
  {hvec[g], ConstantArray[0, 4]},
  {ConstantArray[0, 4], hvec[g - 4]}
];
omul[{a_, b_}, {c_, d_}] := {
  hmul[a, c] - hmul[d, hconj[b]],
  hmul[hconj[a], d] + hmul[c, b]
};
osignlabel[z_] := Module[{flat = Join[z[[1]], z[[2]]], pos},
  pos = First@FirstPosition[Abs[flat], 1];
  {flat[[pos]], pos - 1}
];
omulsl[{q_, g_}, {r_, h_}] := Module[
  {z = omul[
    {q hvec[g], ConstantArray[0, 4]},
    {r hvec[h], ConstantArray[0, 4]}
  ]},
  osignlabel[z]
];
omulbase[g_, h_] := osignlabel[omul[obasis[g], obasis[h]]];
ov = sb[3];

oCom = And @@ Flatten[
  Table[omulsl[a, b] == omulsl[b, a], {a, ov}, {b, ov}]
];
oAss = And @@ Flatten[
  Table[
    omulsl[omulsl[a, b], c] == omulsl[a, omulsl[b, c]],
    {a, ov}, {b, ov}, {c, ov}
  ]
];
oCW = Select[
  Tuples[ov, 2],
  omulsl[#[[1]], #[[2]]] != omulsl[#[[2]], #[[1]]] &,
  1
];
oAW = Select[
  Tuples[ov, 3],
  omulsl[omulsl[#[[1]], #[[2]]], #[[3]]] !=
    omulsl[#[[1]], omulsl[#[[2]], #[[3]]] &,
  1
];

oTable = <|
  "negativeSquares" -> Count[Table[First[omulbase[g, g]], {g, 1, 7}], -1],
  "commutative" -> oCom,
  "associative" -> oAss,
  "nonassociativeTriples" -> Count[
    Flatten[Table[
      omulsl[omulsl[a, b], c] != omulsl[a, omulsl[b, c]],
      {a, ov}, {b, ov}, {c, ov}
    ]],
    True
  ],
  "commutatorWitness" -> oCW,
  "associatorWitness" -> oAW,
  "projection" -> And @@ Flatten[
    Table[
      proj[omulsl[a, b]] == BitXor[a[[2]], b[[2]]],
      {a, ov}, {b, ov}
    ]
  ]
|>;

hC = <|
  "ab" -> smul[eH][{1, 1}, {1, 2}],
  "ba" -> smul[eH][{1, 2}, {1, 1}],
  "left" -> smul[eH][smul[eH][{1, 1}, {1, 2}], {1, 3}],
  "right" -> smul[eH][{1, 1}, smul[eH][{1, 2}, {1, 3}]]
|>;
sC = <|
  "ab" -> smul[eS][{1, 1}, {1, 2}],
  "ba" -> smul[eS][{1, 2}, {1, 1}],
  "left" -> smul[eS][smul[eS][{1, 1}, {1, 2}], {1, 3}],
  "right" -> smul[eS][{1, 1}, smul[eS][{1, 2}, {1, 3}]]
|>;
nC = <|
  "left" -> smul[eN][smul[eN][{1, 1}, {1, 1}], {1, 2}],
  "right" -> smul[eN][{1, 1}, smul[eN][{1, 1}, {1, 2}]]
|>;
oC = <|
  "left" -> omulsl[omulsl[{1, 1}, {1, 2}], {1, 4}],
  "right" -> omulsl[{1, 1}, omulsl[{1, 2}, {1, 4}]]
|>;
bC = <|
  "left" -> smul[eB][smul[eB][{1, 1}, {1, 2}], {1, 4}],
  "right" -> smul[eB][{1, 1}, smul[eB][{1, 2}, {1, 4}]]
|>;

dCheck[ep_] := Module[
  {ii = hvec[1], jj = hvec[3], ji, z, image, univ, red, inst},
  ji = ep[3, 3] hvec[3];
  z = x hvec[0] + y ii;
  image = FullSimplify[hmul[hmul[jj, z], ji]];
  univ = Resolve[
    ForAll[
      {x, y},
      Element[{x, y}, Reals],
      image == x hvec[0] - y ii
    ],
    Reals
  ];
  red = Reduce[
    Element[{x, y}, Reals] &&
      image != x hvec[0] - y ii,
    {x, y},
    Reals
  ];
  inst = FindInstance[
    Element[{x, y}, Reals] &&
      image != x hvec[0] - y ii,
    {x, y},
    Reals
  ];
  <|
    "nonemptyAssumptions" ->
      Resolve[Exists[{x, y}, Element[{x, y}, Reals]], Reals],
    "Jinverse" -> ji,
    "J2" -> hmul[jj, jj],
    "imageFormula" -> image,
    "universalResolve" -> univ,
    "violationReduce" -> red,
    "violationFindInstance" -> inst
  |>
];

dH = dCheck[eH];
dS = dCheck[eS];

id = IdentityMatrix[2];
mi = {{0, -1}, {1, 0}};
mk = {{1, 0}, {0, -1}};
mb = {id, mi, mk, mi.mk};

matrixS = <|
  "basis" -> mb,
  "multiplicationMatchesS" -> And @@ Flatten[
    Table[
      mb[[g + 1]].mb[[h + 1]] ==
        eS[g, h] mb[[BitXor[g, h] + 1]],
      {g, 0, 3}, {h, 0, 3}
    ]
  ],
  "conjugationFormula" ->
    FullSimplify[mi.mk.(x id + y mi).(eS[3, 3] mi.mk)]
|>;

u24 = Select[Range[1, 23], CoprimeQ[#, 24] &];
dd = {-1, -3, -2};
coord24[r_] := Sum[
  ((1 - JacobiSymbol[dd[[i]], r])/2) 2^(i - 1),
  {i, 1, 3}
];

eCheck = <|
  "U24" -> u24,
  "coords" -> (coord24 /@ u24),
  "bijection" -> Sort[coord24 /@ u24] == Range[0, 7],
  "homomorphism" -> And @@ Flatten[
    Table[
      coord24[Mod[r s, 24]] == BitXor[coord24[r], coord24[s]],
      {r, u24}, {s, u24}
    ]
  ],
  "specific" -> (coord24 /@ {5, 7, 11}),
  "product" -> Mod[5 7, 24],
  "oAssociatorSign" ->
    First[omulsl[omulsl[{1, 6}, {1, 5}], {1, 3}]] *
    First[omulsl[{1, 6}, omulsl[{1, 5}, {1, 3}]]]
|>;

result = <|
  "finiteTables" -> finiteTables,
  "projectionChecks" -> projectionChecks,
  "O8" -> oTable,
  "namedWitnesses" -> <|
    "H4" -> hC, "S4" -> sC, "N4" -> nC, "O8" -> oC, "B8" -> bC
  |>,
  "D" -> <|"H4" -> dH, "S4" -> dS, "S4matrices" -> matrixS|>,
  "E" -> eCheck
|>;

InputForm[result]
