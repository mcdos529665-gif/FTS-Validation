# WF-109 — классы шага22 и первый чётный шаг, 2026-10-07

Claim: `WINDOW_BOUNDARY_22`; локальная проверка `boundary_recheck.py`.
Навык `fts-wolfram-audit`; механический шаг делегирован.

Область: `m∈{2,4,…,24}`, `a,b∈U_m={1≤a<m:gcd(a,m)=1}`.
При m=22 перебраны все подмножества U22, содержащие1 и замкнутые по
умножению: в конечной группе это все подгруппы. Область непуста.
Наблюдение — вектор принадлежности всем подгруппам, не семантика ФТС.

Для всех a,b∈U22 совпадение наблюдений эквивалентно совпадению порождённых
подгрупп. Ожидаемые классы: `{{1},{3,5,9,15},{7,13,17,19},{21}}`.
Предъявляемый свидетель нарушения «только равные или обратные»: a=3,b=9.
Для всех чётных m от2 до24 максимальные размеры классов должны быть
`{1,1,1,1,2,1,2,2,2,2,4,1}`; первый m с размером больше2 — 22.
Условие поражения: иной класс, несовпадение хотя бы одной пары или размера,
либо неработающий свидетель.

## Провайдер и выполненный код

Один `wolframcontext`: 31.0 с, ошибка навигации:

```text
tool call failed for codex_apps/wolfram.WolframContext
Mcp error: -32603: Internal error
```

Один `wolframlanguageevaluator`: 8.2 с, timeConstraint=20, isError=false.
Всего39.2 с; повторов нет. Provider timeout/unevaluated отсутствуют.

```wl
ClearAll[units,cyc,classes,signature,a,b,m,h];
units[m_]:=Select[Range[m-1],CoprimeQ[#,m]&];
cyc[a_,m_]:=Sort[DeleteDuplicates[Table[PowerMod[a,j,m],{j,0,Length[units[m]]-1}]]];
classes[m_]:=SortBy[GatherBy[units[m],cyc[#,m]&],First];
u22=units[22];
subs=SortBy[Select[Subsets[u22],Function[h,MemberQ[h,1]&&And@@Flatten[Table[MemberQ[h,Mod[a*b,22]],{a,h},{b,h}]]]],Length];
signature[a_]:=Boole[MemberQ[#,a]]& /@ subs;
c22=SortBy[GatherBy[u22,signature],First];
nonempty=Length[u22]>0&&MemberQ[u22,1]&&Length[subs]>0;
violations=Select[Tuples[u22,2],Function[pair,(signature[pair[[1]]]===signature[pair[[2]]])=!=(cyc[pair[[1]],22]===cyc[pair[[2]],22])]];
bounds=Table[{m,Max[Length /@ classes[m]]},{m,2,24,2}];
first=First[Select[bounds,Last[#]>2&]][[1]];
badPairs=Select[Tuples[u22,2],Function[pair,signature[pair[[1]]]===signature[pair[[2]]]&&pair[[1]]!=pair[[2]]&&Mod[Times@@pair,22]!=1]];
witness={3,9,signature[3]===signature[9],Mod[3*9,22],cyc[3,22]===cyc[9,22]};
InputForm[{nonempty,Length[subs],c22,c22===classes[22],violations,bounds,first,Length[badPairs],witness}]
```

## Сырой результат evaluator

```text
{True, 4, {{1}, {3, 5, 9, 15}, {7, 13, 17, 19}, {21}},
 True, {},
 {{2, 1}, {4, 1}, {6, 1}, {8, 1}, {10, 2}, {12, 1},
  {14, 2}, {16, 2}, {18, 2}, {20, 2}, {22, 4}, {24, 1}},
 22, 16, {3, 9, True, 5, True}}
```

Нарушений эквивалентности профилей/подгрупп нет; найдено16 упорядоченных
пар с равными профилями, которые не равны и не обратны. Свидетель3,9
проверен в коде подстановкой в сигнатуры, произведение и порождённые
подгруппы; отдельно воспроизведён локально.

## Оценка основного агента

Навигационный вызов: `provider_error`, доказательной силы не имеет.
Основной конечный математический предикат: **confirmed_math** по точному
результату evaluator и совпадению независимых локальных алгоритмов.
Полный конечный перебор заменяет поиск по неограниченной области;
FindInstance/Reduce здесь не применялись. Все операции выполняются в
конечных группах единиц, единица включена, ноль исключён условием gcd.

Это уточняет арифметическую строку окна23 и область проверки парности.
Не доказывает смысловую роль окна23, не назначает ему уровень ФТС,
не изменяет C-94 на его прежней области и не повышает St_FTS.
