# Независимая попытка Wolfram — 2026-10-05

Навык: fts-wolfram-audit. Делегирован только механический CAS-шаг; интерпретация ниже принадлежит основному агенту. Один вызов context (19.5 с), один evaluator (6.5 с, timeConstraint=30); всего 26 с внешнего ожидания. Повторов не было.

Пакет: конечные единицы mod 48 и генераторы 5,47,17; точные матрицы Blackwell 2×2; вещественная граница q+(y−2)²=4 при q≥0; кубическая/четвёртая поляризация; потеря знака квадратом; круговая/гиперболическая матрицы; конечный тензорный свидетель. Смысл уровней ФТС не передавался как CAS-предикат.

## Принятые и непринятые части свидетельства

| Пункт | Сырой результат | Диагноз |
|---|---|---|
| 1, units48 | U и generated совпали: {1,5,7,11,13,17,19,23,25,29,31,35,37,41,43,47}; orders={4,2,2} | Конечное перечисление пригодно. Quantified-wrapper непригоден: assumptionsReduce=False, assumptionsExists=False. CoprimeQ на символе не выражает нужный предикат. Его vacuous True не используется. Доказательство даёт явная биекция OC01. |
| 2, Blackwell | Q={{5/8,3/8},{3/8,5/8}}, riskP=1/4, riskQ=3/8; R не вычислен | Построение системы в worker некорректно: First::nofirst, ReplaceAll::reps; универсальный результат unevaluated. Независимая проверка обратного канала inconclusive. Локальная обратная матрица проверяется отдельно и не выдаётся за Wolfram PASS. |
| 3, boundary | existsResolve=q<=4; universal=True; counterexampleReduce=False | Условие существования пригодно. Solve вернул ConditionalExpression с q<4 и Undefined при q=4; эта параметрическая подстановка не проверяет границу. Точка q=4,y=2 подставлена непосредственно в локальный полином. q=5ComplexRoots={{y->2-I},{y->2+I}}. |
| 4, polynomials | universal=True; counterexampleReduce=False; findInstance={} | Пригодно для точных полиномиальных тождеств на R². |
| 5, sign | assumptions=x<0 or x>0; universal=True; witness x=1; squares=1,1; signs=1,-1 | Пригодно; запрет факторизации следует из одной пары с одинаковой проекцией. |
| 6, dynamics | universal остался ForAll; counterexampleReduce=False; t0=True,tPi=True | Нельзя назвать всю универсальную формулировку вычисленной. Общий вывод в REVIEW обоснован прямыми тождествами; локальная SymPy-проверка отдельна. |
| 7, tensor | DetK=4, left=30, right=30, predicate=True | Пригодно для одного конечного свидетеля; общий закон выводится алгебраически. |

## Существенные фрагменты фактически выполненного кода

    u = Select[Range[47], CoprimeQ[#, 48] &];
    gen1 = Sort@DeleteDuplicates@Flatten@Table[
      Mod[5^i 47^j 17^k, 48], {i, 0, 3}, {j, 0, 1}, {k, 0, 1}];
    ord1 = {MultiplicativeOrder[5, 48], MultiplicativeOrder[47, 48],
      MultiplicativeOrder[17, 48]};
    ass1 = Element[a, Integers] && 1 <= a <= 47 && CoprimeQ[a, 48];
    p = {{3/4, 1/4}, {1/4, 3/4}}; k = p; qmat = p.k;
    risk[m_] := 1/2 Total[Map[Min @@ # &, Transpose[m]]];
    rvars = {{r11, r12}, {r21, r22}};
    rsol = Solve[Join[Flatten[qmat.rvars == p], Total /@ rvars == {1,1}],
      {r11,r12,r21,r22}, Reals];
    rmat = rvars /. First[rsol];
    exists3 = Resolve[Exists[y, q + (y - 2)^2 == 4], Reals];
    roots3 = Solve[q + (y - 2)^2 == 4, y, Reals];
    poly4 = (a+b)^4-(a-b)^4 == 8 a b (a^2+b^2);
    poly3 = (a+b)^3-(a-b)^3 == 2 b (3 a^2+b^2);
    pred5 = x^2 == (-x)^2 && Sign[x] != Sign[-x];
    r[t_] := {{Cos[t],-Sin[t]},{Sin[t],Cos[t]}};
    h[t_] := {{Cosh[t],Sinh[t]},{Sinh[t],Cosh[t]}};
    aa={{1,1},{0,1}}; bb={{2,0},{0,1}}; v={1,2,3,4};
    km=KroneckerProduct[aa,bb]; g=IdentityMatrix[4];
    gp=Transpose[Inverse[km]].g.Inverse[km];
    pred7=(km.v).gp.(km.v)==v.g.v;

Ошибка управляющего кода не является контрпримером к математическим утверждениям. Полный batch не получает статуса PASS; пригодные вычисленные значения и непроверенные части перечислены раздельно. Канон, St_math и St_FTS этой попыткой не повышены.
