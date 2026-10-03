# Внутренние эмпирические результаты, относящиеся к neural-skeleton claim

- Дата сводки: 2026-09-15
- Статус: internal limiting/supporting evidence
- Это не внешняя литература и не изменение канона.

## I1 — train_reflection

Источник: work/v14_rebuild/train_reflection/RESULTS.md,
work/v14_rebuild/train_reflection/results.json.

- 64 seeds × 600 episodes, общая история и замкнутый контур.
- R с обратной связью улучшил среднюю цену против R_no_feedback на 1.5861
  на 64/64 seed.
- Против сильной B_adaptive получено +0.0056, исходы 30/30/4.
- R и B_event поведенчески эквивалентны.
- Узкий claim специфической «рефлексивной» архитектуры не выделен.

Relation: supports_local_feedback_effect против no-feedback; limiting для
claim, что конкретный FTS/reflection mechanism лучше сильной альтернативы.
Это синтетический внутренний эксперимент, не свидетельство У11 и не
нейробиологическое подтверждение.

## I2 — O_20 typed-absence test

Источник: work/v14_rebuild/o20/AUDIT_REANALYSIS.md,
work/v14_rebuild/o20/RESULTS.md и связанный REPRODUCIBILITY.md.

- Гипотеза, что typed absence encoding T3 превосходит нетипизированный flag,
  не подтвердилась.
- 1/4 dataset wins.
- Средний ΔAUC = -0.0079.
- One-sided exact sign p = 0.9375.
- T3 не был capacity-matched; OpenML cylinder-bands id=33/version=1 отмечен
  inactive.

Relation: nonconfirmation/limiting; нельзя использовать как окончательное
опровержение typed absence вообще, но нельзя и выдавать T3 как подтверждённый
механизм.

## Следствие для neural-skeleton оценки

Внутренние результаты поддерживают более слабую формулировку:

- рекуррентная обратная связь может быть полезной в конкретной среде;
- специфичность FTS-операций не следует из одного выигрыша против слабой
  baseline;
- typed absence требует новой постановки с заранее заданным механизмом
  missingness, capacity matching и корректной единицей вывода.

Они не подтверждают:

- полную архитектуру FTS;
- необходимость 0_A, κ, Close или Lift;
- преимущество над независимой M′;
- перенос на мозг или consciousness.

