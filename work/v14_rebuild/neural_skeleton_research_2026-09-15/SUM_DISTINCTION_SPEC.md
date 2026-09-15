# Чередование суммирования и различения: спецификация для электронной нейросети

- Дата: 2026-09-15
- Статус: research-layer design hypothesis
- Связь с ФТС: рабочая операционализация DN-0003; не новая аксиома и не изменение source/
- Scope: будущая искусственная/neuromorphic neural architecture

## Короткий ответ

Чтобы принцип ФТС стал архитектурным, а не только описательным, ей нужно задать
полный цикл:

    Aggregate → Normalize/Compete → Distinguish → Residual/Memory → Update

Суммирование должно собирать контекст, различение — менять наблюдаемую
эквивалентность или выбирать ветвь, residual — показывать, что осталось
невыраженным, memory/gate — удерживать результат и provenance, а update — передавать
его в следующий цикл.

Простое чередование «суммировать на чётном уровне, различать на нечётном» само по
себе недостаточно: не заданы оператор, критерий, память, стоимость, устойчивость
и правило поражения [DN-0003].

## 1. Минимальный цикл

Пусть на шаге t система имеет typed state:

    z_t = (h_t, mask_t, provenance_t, revision_t, W_t)

где h — активное представление, mask — наблюдаемость/структурированное отсутствие,
provenance — источник, revision — версия, W — локальная память. Эти поля являются
исследовательской типизацией; они не объявляются тождественными 0_A, κ или W/0_W.

### 1.1 Aggregate

    a_t = Agg_t({message_j(h_j,t)}, context_t, mask_t)

Требования:

- явно задать носитель сообщений и арность;
- определить, что сохраняется: сумму, среднее, максимум, распределение,
  invariant/equivariant statistic или relation;
- задать инвариант перестановки/симметрии, если порядок входов не должен иметь
  значения;
- не терять mask/provenance при агрегации;
- учитывать overflow, saturation, quantization и communication cost.

Внешний аналог: MPNN формулирует нейросеть как message-passing algorithm plus
aggregation procedure [внешнее: Gilmer et al. 2017].

### 1.2 Normalize/Compete

Агрегат нельзя просто передать дальше: без контроля масштаба система может
схлопнуться в один большой activation или потерять слабые различия.

Рабочие варианты:

- divisive normalization по pool;
- subtractive/lateral inhibition;
- softmax или attention competition;
- k-winner-take-all;
- clipping, homeostatic scaling или event threshold.

Нормализация — не отдельный «уровень ФТС», а обязательный регулятор между
суммированием и различением. В нейронных моделях normalization делит drive одного
нейрона на суммарную активность pool и может одновременно давать усреднение или
winner-take-all в зависимости от режима [внешнее: Carandini–Heeger].

### 1.3 Distinguish

    d_t = Dist(a_t, q_t, context_t)

Различение должно делать что-то проверяемое:

- уточнять partition наблюдений;
- выбирать одну или несколько ветвей;
- выделять контраст/границу;
- создавать sparse event;
- формировать attention weights;
- отклонять обновление;
- порождать новый вопрос или residual.

Минимальный формальный тест:

    x ≡_t y  iff  Read_t(x) = Read_t(y)

Шаг Dist считается содержательным, если существует пара x,y, для которой
эквивалентность на t ещё держалась, а после Dist различие становится доступным
или меняется допустимое действие. Если Dist не отделяет ни одного случая — это
переименование. Если он сливает различие, нужное следующему вопросу, — это
collapse/false Tot.

Конкуренция должна быть не только логической: lateral inhibition и WTA дают
механизм разнесения близких активностей, но могут порождать multiple stable
equilibria и hysteresis [внешнее: Coultrip et al.; Mao–Massaquoi].

### 1.4 Residual

    e_t = Target_t - Predict_t
    r_t = (e_t, q_t, provenance_t, revision_t)

Residual — не просто ошибка обучения. В ФТС-контуре он должен отвечать на вопрос:

- что не выразимо текущим чтением;
- какой новый вопрос возник;
- какой старый ответ больше нельзя безопасно перенести;
- нужно ли увеличить carrier/state или отказаться от обновления.

Predictive-coding models реализуют отдельные expectation и error units на
соседних иерархических уровнях, с обратными predictions и прямыми prediction
errors [внешнее: Rao–Ballard; Neural Elements for Predictive Coding].

### 1.5 Memory/Update

    W_(t+1) = GateUpdate(W_t, d_t, r_t, provenance_t, revision_t)

Обязательные поля:

- accepted state;
- rejected/deferred state;
- provenance trace;
- revision trigger;
- expiry/forgetting condition;
- cost of keeping memory;
- local versus global access.

Без этого суммирование повторяет текущий вход, а различение не становится
устойчивым состоянием. Для У7+ это место, где candidate-gate κ/Prov/Rev может
быть проверен; он не должен автоматически объявляться сущностью уровня.

## 2. Что именно должна добавить ФТС

### A. Алгебра агрегаторов

Нужен небольшой typed vocabulary:

- Sum/Mean — контекст и статистический pool;
- Max/K-WTA — конкурентное различение;
- Attention-weighted sum — выбор с сохранением soft alternatives;
- Ratio/Normalization — относительная различимость;
- Message passing — локальная агрегация отношений;
- Memory read/write — межтактовое суммирование истории.

Для каждого агрегатора нужны identity, saturation/zero behavior, arity, symmetry,
quantization tolerance и failure mode.

### B. Алгебра различителей

Нужны операторы, которые различают не только значения, но и режимы:

- comparator;
- threshold/event encoder;
- inhibitory competition;
- attention/router;
- typed absence discriminator;
- provenance/revision gate;
- residual-triggered refinement;
- refuse/sever/defer.

В искусственных сетях attention и GAT показывают, как weighted aggregation может
одновременно собирать сообщения и выделять их относительную важность. В ФТС надо
развести эти две функции: weights — не сами доказательства Dist.

### C. Закон чередования

Чередование должно быть динамическим, а не только привязанным к номеру уровня:

    S_t = Aggregate(...)
    D_t = Distinguish(S_t, residual_t)
    S_(t+1) = Aggregate(selected_messages(D_t), memory_t)

Нужны:

- условие перехода S→D;
- условие повторения D→S;
- stop/seal criterion;
- режим отказа/застревания;
- возможность деградации и ошибочной траектории;
- запрет на автоматическое «восхождение» после каждого цикла.

Нечётные/чётные позиции ФТС могут остаться картой чтения, но реализация должна
допускать несколько S/D циклов внутри одного уровня и пропуски между уровнями.

### D. Partition/refinement law

Для каждого D-шагa надо хранить:

    P_t = partition of states distinguishable by current readout
    P_(t+1) = refine(P_t, witness_t)

Требования:

- refinement должен иметь witness;
- старый интерфейс должен сохраняться через projection;
- новый вопрос должен быть явно назван;
- стоимость refinement должна быть оплачена;
- независимая M′ должна получать тот же контракт.

Это связывает DN-0003 с O_07/O_08/O_09/O_14, но не доказывает канонический
порядок ФТС автоматически.

### E. Hardware contract

Для будущей электронной нейросети ФТС должна быть разложима на реальные
primitive operations:

| Функция | Аппаратный примитив |
|---|---|
| Aggregate | MAC/crossbar, accumulator, local message buffer |
| Normalize | divider/approximate reciprocal, shunting inhibition, scale controller |
| Distinguish | comparator, threshold, WTA/k-WTA, router, attention score |
| Residual | subtractor, error register, prediction comparator |
| Memory | local SRAM/SRAM-like state, register file, nonvolatile synapse |
| Update | local plasticity rule, event queue, eligibility trace |
| Provenance | tag/timestamp/source bits |
| Revision | version counter, invalidate/commit flag |
| Communication | packet/event routing, NoC, local broadcast |

TrueNorth demonstrates why local memory, event packets, on-core routing and
event-driven control must be part of the design rather than afterthoughts:
the chip stores synapse/neuron state locally and routes spikes as packets across
a mesh [внешнее: Merolla et al.]. Loihi demonstrates a programmable on-chip
learning engine, so learning rule and state update must be specified as hardware
operations, not assumed to happen off-chip [внешнее: Davies et al.].

### F. Learning contract

ФТС должна выбрать, где происходит обучение:

1. offline gradient training + hardware inference;
2. local predictive-error update;
3. STDP/three-factor update;
4. hybrid: global slow update + local fast plasticity.

Для каждого варианта нужны:

- что считается pre/post activity;
- где хранится eligibility;
- как используется reward/error;
- как делается credit assignment через S/D cycles;
- устойчивость к quantization, noise и device mismatch;
- возможность online revision без полного retraining.

## 3. Почему одного «суммирования» мало

Deep Sets показывают, что сумма после element-wise transform — строгий способ
строить permutation-invariant set function: f(X)=rho(sum phi(x)). Это полезный
шаблон для Aggregate, но он сам по себе не задаёт Dist, memory, error или
hardware routing [внешнее: Zaheer et al.].

MPNN расширяет идею до графа: сообщения агрегируются по структуре отношений.
Однако даже MPNN не гарантирует:

- typed absence;
- provenance;
- revision;
- refusal;
- distinction witness;
- stable recurrent memory.

Именно эти интерфейсы должны быть добавлены в ФТС, если она претендует на
scaffold, а не на переименование MPNN/attention/normalization.

## 4. Минимальный комплект тестов

1. AGG-INVARIANCE — перестановка входов сохраняет требуемый результат.
2. AGG-CONSERVATION — агрегат сохраняет заявленный invariant и не теряет
   provenance/mask.
3. DIST-REFINE — Dist реально расщепляет заранее заданный equivalence class.
4. DIST-WTA — competition даёт controlled sparsity, но не runaway/hysteresis.
5. RESIDUAL-LIFT — residual создаёт новый выразимый вопрос, а не просто новый
   слой.
6. MEMORY-REV — revision/provenance меняют accept/refuse/readout по протоколу.
7. S-D-TRANSFER — одна и та же Agg/Dist схема переносится между readouts и
   domains.
8. HARDWARE-COST — измеряются MACs, events, memory movement, latency, energy и
   quantization loss.
9. ABLATION — удаление Agg, Dist, Normalize, Residual, Memory и Gate даёт
   заранее классифицируемый failure.
10. M-PRIME — независимая модель с теми же primitives и стоимостью не должна
    быть проигнорирована.

## Рабочий вывод

Чтобы больше соответствовать будущей электронной нейросети, ФТС прежде всего
нужно дополнить:

1. typed algebra of aggregation;
2. typed algebra of distinction/competition;
3. formal residual/refinement witness;
4. recurrent memory with provenance/revision;
5. normalization and stability law;
6. local/event-driven hardware mapping;
7. local or hybrid learning rule;
8. cost model and ablation suite.

Это исследовательская дорожная карта. Она не переписывает DN-0003 и не повышает
статусы канона.

