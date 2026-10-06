# WF-108 — геометрия круга, 2026-10-06

Claim: `WINDOW_CIRCLE_CANDIDATE`; адрес `oq-window-family-roles`.
Навык `fts-wolfram-audit`, механический шаг делегирован.
Оценка основного агента: **confirmed_math** только для предикатов ниже.
Связь с ФТС остаётся assistant_candidate; новый C-NN не вводится.

## Точный пакет

Local check: `circle_probe.py`; та же арифметика и фазовые тождества.
Дополнительная локальная проверка матриц S4 не входит в этот CAS-предикат.

Переменные: `x1,y1,x2,y2,t,p∈R`; `r,s,k∈U12/U24` в конечных проверках;
`m∈{0,1,2,3}`, `j∈{0,1}`. `U_n={1≤k<n:gcd(k,n)=1}`.
Точка индекса k означает `exp(2πik/n)`.

Для всех вещественных x1,y1,x2,y2 проверяется
`(x1*x2+y1*y2)^2+(x1*y2-y1*x2)^2=(x1^2+y1^2)*(x2^2+y2^2)`;
для всех вещественных t,p — формулы cos(p−t), sin(p−t).
Для всех пар r,s∈U24 — гомоморфность редукции U24→U12; слои и ядро
перечисляются полностью. Для всех k∈U24 проверяются сохранение множества,
`R²=D`, `K²=id`, `KR=DRK`, где `R(k)=k+6`, `K(k)=−k`, `D(k)=k+12`
по mod24, и проекции R,K на действия 7,11 по mod12. Перечисляются
восемь перестановок `k↦(−1)^j k+6m`. Арифметическое действие r есть
`k↦rk mod24`, отличный тип операции. Следы с k=1:
R: `1→7→13`; арифметическое действие 7: `1→7→1`.

Опровержение: ненулевой остаток тождества, ложная конечная проверка,
другой слой, число перестановок или след. Семантика ФТС не включена.

## Выполненный код и сырой результат

Один context: 12.7 с, нерелевантная документация, не доказательство.
Один evaluator: 4.3 с, `timeConstraint=20`; всего 17.0 с, повторов нет.
Provider error/timeout/unevaluated отсутствуют.

```wl
ClearAll[x1,y1,x2,y2,t,p,k,rotation,mirror,deck];
poly=Expand[(x1*x2+y1*y2)^2+(x1*y2-y1*x2)^2-(x1^2+y1^2)*(x2^2+y2^2)];
nonempty=Resolve[Exists[{x1,y1,x2,y2},x1==1&&y1==0&&x2==1&&y2==0],Reals];
universal=Resolve[ForAll[{x1,y1,x2,y2},poly==0],Reals];
violation=Reduce[poly!=0,{x1,y1,x2,y2},Reals];
phase=FullSimplify[{Cos[t]*Cos[p]+Sin[t]*Sin[p]-Cos[p-t],Cos[t]*Sin[p]-Sin[t]*Cos[p]-Sin[p-t]},Element[{t,p},Reals]];
u12=Select[Range[11],CoprimeQ[#,12]&];
u24=Select[Range[23],CoprimeQ[#,24]&];
fibers=Table[Select[u24,Mod[#,12]==k&],{k,u12}];
kernel=Select[u24,Mod[#,12]==1&];
hom=And@@Flatten[Table[Mod[Mod[r*s,24],12]==Mod[Mod[r,12]*Mod[s,12],12],{r,u24},{s,u24}]];
squares=Mod[#^2,24]& /@ u24;
rotation[k_]:=Mod[k+6,24];mirror[k_]:=Mod[-k,24];deck[k_]:=Mod[k+12,24];
relations=And@@Table[MemberQ[u24,rotation[k]]&&MemberQ[u24,mirror[k]]&&rotation[rotation[k]]==deck[k]&&mirror[mirror[k]]==k&&mirror[rotation[k]]==deck[rotation[mirror[k]]],{k,u24}];
lifts=And@@Table[Mod[rotation[k],12]==Mod[7*k,12]&&Mod[mirror[k],12]==Mod[11*k,12],{k,u24}];
perms=Flatten[Table[Table[Mod[(-1)^j*k+6*m,24],{k,u24}],{m,0,3},{j,0,1}],1];
traces={{1,rotation[1],rotation[rotation[1]]},{1,Mod[7,24],Mod[7*7,24]}};
InputForm[{nonempty,universal,violation,phase,u12,u24,fibers,kernel,hom,squares,relations,lifts,Length[DeleteDuplicates[perms]],traces}]
```

```wl
Out[1]=
{True, True, False, {0, 0}, {1, 5, 7, 11},
 {1, 5, 7, 11, 13, 17, 19, 23},
 {{1, 13}, {5, 17}, {7, 19}, {11, 23}},
 {1, 13}, True, {1, 1, 1, 1, 1, 1, 1, 1},
 True, True, 8, {{1, 7, 13}, {1, 7, 1}}}
```

## Оценка и границы

Непустота подтверждена явным единичным входом; универсальное тождество —
Resolve и нулевым полиномиальным остатком. Reduce нарушения даёт False.
FindInstance отдельно не выполнялся; обратная подстановка неприменима,
поскольку свидетеля нет. Конечные области перебраны полностью, фазовые
тождества упрощены для всех вещественных углов. Нулевые векторы допускаются
в полиноме, но не в интерпретации фазы; ветвей обратных функций и полюсов
здесь нет, углы берутся по модулю 2π. Локальная проверка согласована.

Проверка не доказывает смысл окна, доступность общего фазового носителя,
соответствие отражения анти-моде, выбор H/O или неассоциативность операций
ФТС. Канонические St_math/St_FTS не меняются. WF-106 остаётся inconclusive.
