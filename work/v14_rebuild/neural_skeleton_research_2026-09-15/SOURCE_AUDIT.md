# Source audit — neural skeleton first wave

Дата поиска: 2026-09-15. Результаты ниже являются внешними основаниями и не
изменяют канон или статусы ФТС.

| ID | Проверяемая запись | Точный участок | Что извлечено | Relation / предел |
|---|---|---|---|---|
| NN-E01 | Rao & Ballard (1999), DOI 10.1038/4580, Nature Neuroscience | Официальная страница Nature, abstract; article pp. 79–87 | Модель описывает feedback predictions сверху вниз и feedforward residual errors снизу вверх; hierarchical model neurons обучаются на natural images | direct для O_01/Res_n; visual model не задаёт ФТС и не доказывает unique ladder |
| NN-E02 | Andreas et al. (2016), CVPR, Neural Module Networks | CVPR Open Access, paper pp. 39–48, abstract | Reusable jointly trained modules динамически собираются в deep networks под структуру вопроса | direct/alternative для композиционного интерфейса; network layout не равен ФТС |
| NN-E03 | Graves et al. (2016), DOI 10.1038/nature20101, Nature | Официальная страница Nature, abstract и editorial summary | DNC соединяет neural controller с read/write external memory и показывает graph/reasoning tasks | alternative для memory/read-write loop; не доказательство необходимости ФТС |
| NN-E04 | Le Morvan et al. (2020), NeurIPS 33, NeuMiss | Официальная страница NeurIPS, abstract; paper | Missingness indicator участвует в differentiable architecture; заявлены risk/complexity results при MAR и self-masking | direct local bridge для typed absence; statistical missingness не равно 0_A |
| NN-E05 | Che et al. (2018), DOI 10.1038/s41598-018-24271-9 | Scientific Reports full text через PMC, раздел GRU-D: model with trainable decays | Recurrent update использует mask и time since last observation для decay | direct local bridge; health time-series mechanism и decay не равны Tot/Lift |
| NN-E06 | Ranzato & Tapparo, arXiv cs/0401016v3, DOI 10.1093/logcom/exl035 | Официальный arXiv HTML, abstract и §§1, 5–6 | Strong preservation задаётся относительно фиксированного language; minimal refinement связывается с completeness и greatest fixed point | direct formal template для O_07/O_08/O_09; область не включает neural learning, cost или FTS order |
| NN-E07 | Cohen & Welling (2016), PMLR 48, pp. 2990–2999 | Официальная PMLR page, abstract | Explicit group actions и weight sharing дают equivariance и sample-complexity benefit без увеличения параметров | alternative/limiting: symmetry/phase имеет независимый внешний formalism |
| NN-E08 | Dehaene et al. (2001), DOI 10.1111/j.1749-6632.2001.tb05714.x | Wiley abstract | Модель различает specialized processors и recurrent globally connected workspace, откуда выводятся нейровизуализационные predictions | analogy для workspace/gate; не ANN result и не подтверждение Close/κ |
| NN-E09 | Lake et al. (2017), DOI 10.1017/S0140525X16001837 | Cambridge abstract | Для human-like learning подчёркиваются causal models, compositionality и learning-to-learn | limiting requirements; не validation ФТС |
| NN-E10 | Kok & Lange (2019), PMCID PMC6400266 | PMC article, abstract/discussion | Predictive processing поддерживается для локальных hierarchical sensory circuits, но cortex в целом не сводится к одной hierarchy; обсуждаются альтернативы | limiting для T4 biological transfer; вторичный источник |

## Verification notes

- Для NN-E01, NN-E03, NN-E06 и NN-E07 использованы страницы первичных
  издателей/архива с доступными abstract/metadata.
- Для NN-E04 использована официальная страница конференции NeurIPS, а не
  сторонний пересказ.
- NN-E05 и NN-E10 открыты через PMC как копия журнального текста; PMC ID и
  DOI/название сохранены.
- NN-E08 и NN-E09 используются только для ограничения/архитектурного контекста;
  их нельзя считать прямым подтверждением ФТС.
- Ни один источник не утверждает существование «FTS skeleton»; mapping находится
  в отдельной колонке EVIDENCE_MATRIX.tsv и всегда имеет scope/limitation.

