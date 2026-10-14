# baseline

Корневой узел дерева экспериментов OpenResearch.

- **Гипотеза:** нет; узел фиксирует исходное состояние.
- **Что измеряется:** целостность канона — `tools/verify.py --strict`
  (ожидается 0 mismatch, 0 extra).
- **Условие поражения:** ненулевой код возврата; это FAIL проверки, а не
  контрпример — сначала диагностика (`PROJECT_INSTRUCTIONS.md#status`).

Дочерние эксперименты создаются от этого узла (`orx create-experiment --parent`),
получают каталог `experiments/<slug>/` и записывают `<slug>` в `experiments/ACTIVE`.
