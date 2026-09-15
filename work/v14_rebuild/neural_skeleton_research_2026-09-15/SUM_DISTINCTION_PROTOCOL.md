# Protocol: alternating summation/distinction for electronic FTS

- Date: 2026-09-15
- Status: active research-layer protocol
- Object: DN-0003 operationalization
- Canon: unchanged

## Research question

Какие минимальные операторы, состояния, learning rules и hardware constraints нужно
добавить к принципу чередования суммирования и различения, чтобы он стал
исполняемым каркасом будущей электронной нейросети?

## Search directions

- aggregation/message passing/set functions;
- attention, normalization and lateral inhibition;
- predictive coding and residual/error units;
- recurrent memory, revision and provenance;
- neuromorphic hardware, event routing and on-chip learning.

## Inclusion rule

Источник включается, если задаёт архитектуру, формальный предикат, circuit model
или hardware constraint, который можно сопоставить с конкретной ролью Agg, Dist,
Residual, Memory, Update или Communication.

Сходство слов «sum», «difference», «layer» без объектов, операций и условий
помечается analogy и не считается direct.

## Required output

Для каждого bridge фиксируются:

- external operation;
- FTS candidate role;
- input/output type;
- invariants;
- failure mode;
- hardware cost;
- possible M′ alternative;
- relation and scope.

## Acceptance

A design increment is accepted as a useful research-layer specification only if:

- at least one independent source supports Aggregate;
- at least one independent source supports Dist/competition;
- at least one source supports Residual/feedback;
- at least one source constrains hardware communication/memory/learning;
- the proposed cycle has explicit failure tests and no canonical status promotion.

