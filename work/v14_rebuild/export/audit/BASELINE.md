# Baseline полного аудита ФТС v13/v14

Дата фиксации: 2026-07-13 (Europe/Moscow).

## Репозиторий

- Commit: `201c9e67af5739c048102600d495f05fee509c8a`.
- Ветка: `claude/agitated-khorana-ac2ec6`.
- Рабочее дерево перед аудитом: чистое.
- `core.autocrlf=false`.
- `source/` перед аудитом: `13 ok / 0 missing / 0 mismatch / 0 extra`.
- SHA256 `source/MANIFEST.json`:
  `a91c453226cac21072478fa1fbf2db766e36f1bfe477e52414ee19f5c8f6f16a`.
- SHA256 исходного workbook, записанный в MANIFEST:
  `32a6ed34febaf62a57f6aac986e8caf9716b09b7b8f14bc131e76f81d15acbd6`.

## Проверки до исправлений

- `verification.py`: 62 PASS / 0 FAIL.
- `probes.py`: 47 PASS / 0 FAIL; это кандидатные пробы, не основной сьют.
- Review-копии статьи, status patch и verification report совпадали с рабочими файлами.
- Все шесть записей исходного `CHECKSUMS.sha256` сходились.

Важно: это только снимок исходного состояния. PASS не считается доказательством
корректности самой формулировки проверки; именно это проверяет аудит.

## Среда воспроизведения

- Python 3.13.14
- SymPy 1.14.0
- NumPy 2.4.6
- pandas 3.0.3
- SciPy 1.17.1
- scikit-learn 1.9.0

## Данные

- Локальный RadioML 2016.10a:
  `work/v14_rebuild/d10_phase/radioml/RML2016.10a_dict.pkl`.
- Размер: 640919653 байта.
- SHA256:
  `b29ccc25b00d0718cd3b70ffa9158662ec83f6d9b63ffd845c7bcbe3b3096e8c`.
- Файл игнорируется git правилом `radioml/.gitignore: *.pkl`.

## Границы baseline

- Исходного xlsx v14 в репозитории нет; workbook round-trip не может быть
  сертифицирован этим аудитом.
- Сетевые OpenML-данные не входят в git. Их точные идентификаторы, версии и
  полученные хеши фиксируются в журнале воспроизведения при реанализе.
- Исторические предрегистрации и исходные результаты после этой точки не
  переписываются.
