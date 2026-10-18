"""Reviewed canon-admission decisions; --apply writes inputs, --check verifies coverage.

This script does not evaluate mathematics or award evidential St_FTS.
"""
import argparse
import csv
import io
import json
from pathlib import Path

PKG = Path(__file__).resolve().parent
ROOT = PKG.parents[2]
SOURCE = ROOT / 'source'
DATE = '2026-10-18'
RULE = 'CANON_NO_ALTERNATIVE'
SP = 'SP_CANON_NO_ALTERNATIVE_20261018'
RECORD = 'work/v14_rebuild/candidates_register_2026-10-15/CANONIZATION_2026-10-18.md'

# Explicit competing choices or an already recorded defect. Missing evidence alone
# is deliberately not a reason to withhold admission under the author's new rule.
HOLD = {
    2: ('conflict', 'Крест и исключение противоположности: oq-mu4-cross-opposite-rule.'),
    5: ('alternative', 'AC-09 и произведение ветвей; oq-u6-u7-choice-products, форма −x² не вся МУ7.'),
    8: ('alternative', 'Поворот или обращение: CP-009; нижняя цепочка поворотов отозвана в ACCEPTANCE §3.'),
    9: ('alternative', 'Обращение или поворот: CP-008, oq-mu8-inverse-vs-rotation.'),
    10: ('alternative', 'Сохранить запрет или включить противоположность: oq-mu9-opposite-inclusion.'),
    14: ('alternative', 'Узел 11 другого рода или модель только начала лестницы; выбор не сделан.'),
    15: ('alternative', 'Противовес x либо запрет y≠−x³: CP-059, DN-0040.'),
    16: ('conflict', 'Сцепка сама не задаёт узел-носитель: AC_20261003_WINDOWS_TRIPLES, ACCEPTANCE §3.'),
    25: ('alternative', 'Модели T4/C4/H4/S4/N4 и T8/B8/O8; выбор не сделан.'),
    26: ('alternative', 'Неэквивалентные знаковые модели H, M₂(R), O; правило ФТС их не выбирает.'),
    33: ('alternative', 'Масштаб или сдвиг для 9; единое определение Tot открыто, REGISTER §7.'),
    38: ('alternative', 'e^{iωt}, гиперболический поворот или пара; выбор прямо открыт.'),
    48: ('alternative', 'ℚ_p, профинитная навивка или адели как носитель агрегации; выбор не сделан.'),
    54: ('alternative', 'Квадратный или шестиугольный тор: oq-torus-on-9-shape.'),
    55: ('alternative', 'Три реализации линзирования и вопрос о двух объектах; oq-lens-two-objects.'),
    58: ('conflict', 'e^{ix} вокруг основания и действующая окружность через основание; oq-phase-modulus-12-15.'),
    59: ('alternative', 'Противовес x³: x, запрет или T₃; DN-0040, CP-015.'),
    61: ('alternative', 'CP¹ как носитель У6 или только технический аппарат; oq-sphere-u6-carrier.'),
    63: ('superseded', 'Формулировка 6→7 сфера→тор заменена CP-053, DN-0037/0038.'),
    66: ('alternative', 'Суперэллипсоид или сфера отношений как представитель У6: CP-061.'),
    67: ('alternative', 'Тор Клиффорда либо другие формы тора на 9: CP-054, oq-torus-on-9-shape.'),
    68: ('alternative', 'Поверхность Косты как стык 9→10 конкурирует с реализациями CP-055; выбор не сделан.'),
    71: ('alternative', 'Роговой тор как замыкание 12→13 или прогноз CP-058; oq-phase-modulus-12-15.'),
    84: ('alternative', 'Зависит от ресурса У7: архив или новое измерение, CP-085.'),
    85: ('alternative', 'Архив или новое измерение; четвёртый исход или контекст; oq-u6-u7-compositional-semantics.'),
    87: ('conflict', 'Требуется уже назначенная правка порогов α=2, α=1: ACCEPTANCE §3, решение 2026-10-09.'),
    92: ('alternative', 'Минимальная M_03 против действующей развёрнутой записи; выбор печатного минимума не сделан.'),
    94: ('alternative', 'Краткая R=B∨D против действующей M_07; пригодность минимума открыта.'),
    95: ('conflict', 'Строка 8 расходится с принятой двухветвевой CP-004: ACCEPTANCE §3.'),
    97: ('alternative', 'A1/A3 как возможное пояснение, A5/A5a и C_n вместо действующих оснований; поправка 2026-10-03 сохраняет выбор.'),
    103: ('alternative', 'Пакет определений-вариантов; исторический TA1 unresolved, выбор не выполнен.'),
    104: ('alternative', 'Один из возможных паспортов χ; не выбран вместо действующего CHI_CARRIER.'),
    127: ('conflict', 'H1: T₂k=−I противоречит A_07 (пара парабол): ACCEPTANCE §3.'),
}

# Narrow scopes already adopted on 15 October; do not silently restore excluded parts.
SCOPES = {
    1: 'Двухканальное чтение и его математическое ядро; произведение для У7 относится только к ветви −x², не ко всей паре A_07; роль моста остаётся проверяемой.',
    4: 'МУ8 — двухветвевое отношение y²=|x|; одиночная ветвь — его проекция. Мост к ЛУ8 не доказан.',
    6: 'Сопоставление способов решения с 7–9 как чтение; не свидетельство достижения этих уровней.',
    7: 'Протокол тестирования 7–9; не результат его прохождения.',
    53: 'Рабочее согласование 6–9; выбор тор/тело и формы тора остаётся открытым.',
    57: 'Рабочее чтение блоков; формы 12–13 и узел 15 — прогноз, не выбранная форма.',
    72: 'Механизм код→различение→новый код; не новое определение У3 или основание связности.',
    73: 'Пара У3→У2 и метод проверки; общая теорема всех спусков не принимается.',
    74: 'Необходимое информационное ядро QuestionGain; цена, RoleNec и трасса проверяются отдельно.',
    99: 'Рабочее типизированное определение отсутствия; универсальность и AbsDataGain не установлены.',
    100: 'Set-модель с отмеченной точкой r₀; общий Lift и естественность секции открыты.',
    107: 'Проверяемая гипотеза и отрицательный результат o20; положительное обобщение отозвано.',
    113: 'Исследовательский словарь и его обязательства; конфликтная конвертация CP-095 не принята.',
    114: 'Программа семантических проверок; варианты CP-033/084 не выбраны.',
    115: 'Программа пентады; прогнозы форм и общий оператор открыты.',
    118: 'Программа проверки Tot; спорные модели CP-033 не выбраны.',
    119: 'Программа проверки оверлеев; альтернативные нормировки CP-104 не выбраны.',
    123: 'Только симметричные агрегаты пары корней, D=(r₁−r₂)² и потеря бита ветви; привязка 6→7 на −x² исключена (ACCEPTANCE §2).',
}

CARD_HOLD = {
    'M_08': ('alternative', 'Link(0_K,M) / TBD: незавершённый минимум, CP-095 предлагает другое чтение.'),
    'M_09': ('alternative', 'Analogy_κ / TBD и альтернативные минимумы CP-095.'),
    'M_10': ('alternative', 'Compare_κ / TBD и альтернативные минимумы CP-095.'),
    'M_11': ('alternative', 'Fix(E,Agent,Consequences) и альтернативные минимумы CP-095.'),
    'A1': ('alternative', 'Возможное четырёхзначное пояснение; действующее логическое основание им не заменено (2026-10-03).'),
    'A3': ('alternative', 'Двухканальное приложение как возможное объяснение, а не выбранная аксиома (2026-10-03).'),
    'A5': ('alternative', 'Предложенная формализация вместо действующего критерия, прямо не принята 2026-10-03.'),
    'A5a': ('alternative', 'Предложенная формализация вместо действующего критерия, прямо не принята 2026-10-03.'),
    'CHI_LADDER_U7': ('conflict', 'Старая ветвь −χ² с !=χ² не согласована с A_07; нужен мост.'),
    'COMPLEX_LADDER_U7': ('conflict', 'Старая ветвь −Q с !=Q не согласована с A_07; нужен мост.'),
    'WINDOW_GROUPING_13': ('alternative', 'Невыбранные модели T4/C4/H4/S4/N4, CP-025/026.'),
    'WINDOW_GROUPING_25': ('alternative', 'Невыбранные модели T8/B8/O8, CP-025/026.'),
}
for _id in ('M_13', 'CH_13', 'M_14', 'CH_14', 'M_16', 'CH_16', 'M_17', 'CH_17'):
    CARD_HOLD[_id] = ('empty', 'TBD: отсутствует содержательная формулировка, которую можно принять.')
for _id in ('SP_U8', 'SP_U9', 'SP_U12'):
    CARD_HOLD[_id] = ('historical', 'Историческая запись результата прежней проверки; не предложение для повторного принятия.')


def read_tsv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_tsv(path, rows, fields=None):
    stream = io.StringIO(newline='')
    w = csv.DictWriter(stream, fieldnames=fields or list(rows[0]), delimiter='\t', lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    path.write_bytes(stream.getvalue().encode('utf-8'))


def common(card, previous, scope):
    card.update(status='canonical_adopted', canonical_membership='canonical',
                previous_status=previous, St_FTS=previous, evidence_status=previous,
                author_status='adopted_by_author_rule_20261018',
                adoption_source=RECORD, adoption_scope=scope,
                canonical_rule=RULE, canonical_date=DATE,
                revision_condition='Новая явная альтернатива открывает сравнение; контрпример или несовместимость требует сужения/отзыва. Сохраняются условия поражения первоисточника.')
    card['tags'] = list(dict.fromkeys(card.get('tags', []) + ['canonical_adopted', RULE]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.apply == args.check:
        parser.error('choose --apply or --check')
    rows = read_tsv(PKG / 'candidates.tsv')
    families = read_tsv(PKG / 'canon_families.tsv')
    family_ids = {s for r in families for s in r['cards'].split(',')}
    cards = [json.loads(s) for s in (SOURCE / 'fts_cards.jsonl').read_text(encoding='utf-8').splitlines()]
    by_id = {c['id']: c for c in cards}
    decisions = []
    accepted = []
    for r in rows:
        n = int(r['id'][3:])
        state, reason = HOLD.get(n, ('canonical', 'Явная конкурирующая альтернатива в реестре и его указанных развилках отсутствует.'))
        cid = r['id'].replace('-', '_')
        scope = SCOPES.get(n, 'Формулировка реестра в её собственном типе (' + r['kind'] + ') и области; все ограничения и открытые обязательства источника сохранены.')
        decisions.append(dict(layer='research', id=r['id'], decision=state, reason=reason, card=cid if state == 'canonical' else '', scope=scope))
        if state != 'canonical':
            continue
        accepted.append(cid)
        if args.apply and cid not in by_id:
            card = dict(id=cid, type='research_proposal', title=r['id']+' — '+r['kind'],
                        symbol=r['id'], text=r['claim']+' Область канонического принятия: '+scope,
                        original_proposal=r['claim'], depends_on=[], tags=[r['group'], r['kind']],
                        path='17_Карточки/'+cid, internal_ref=r['id']+'; '+r['source'],
                        register=r['ladder'], levels=r['levels'], formulation_origin=r['origin'],
                        proposal_kind=r['kind'], source_document='work/'+r['source'],
                        source_status=r['status'], evidence_refs=r['checks'], open_questions=r['oq'],
                        historical_author_axis=r['author_axis'])
            common(card, r['status'], scope)
            by_id[cid] = card
            cards.append(card)
    for cid in sorted(family_ids):
        state, reason = CARD_HOLD.get(cid, ('canonical', 'Нет открытого конкурирующего варианта для точной действующей записи карточки.'))
        scope = 'Точная запись карточки с её ограничениями; формализация, мосты и эмпирические проверки не объявляются завершёнными.'
        decisions.append(dict(layer='card', id=cid, decision=state, reason=reason, card=cid if state == 'canonical' else '', scope=scope))
        if state != 'canonical':
            continue
        accepted.append(cid)
        card = by_id[cid]
        if args.apply and card.get('canonical_rule') != RULE:
            # Earlier adoption provenance is retained, never overwritten silently.
            card['previous_adoption'] = {k: card[k] for k in ('author_status', 'adoption_source', 'adoption_scope', 'formulation_origin') if k in card}
            common(card, card['status'], scope)
    if args.apply:
        if RULE not in by_id:
            cards.append(dict(id=RULE, type='rule', title='Нет альтернативы — писать в канон', symbol=RULE,
                              text='Правило автора 2026-10-18: если у содержательного кандидата нет явной действующей альтернативы в той же области, записывать его в канон без повторного согласования. Сохранять происхождение, точную область, гипотетичность, проверки, ограничения и условия отзыва. Наличие альтернативы требует явного выбора; отозванные и противоречивые записи не восстанавливаются этим правилом. Каноническое принятие не удостоверяет математического доказательства или эмпирического подтверждения.',
                              status='canonical', depends_on=[], tags=['author_rule'], path='17_Карточки/'+RULE,
                              internal_ref='Поручение автора 2026-10-18; PROJECT_INSTRUCTIONS.md#canon', author_status='explicit_author_rule'))
        if SP not in by_id:
            cards.append(dict(id=SP, type='status_promotion', title='Каноническое принятие без альтернатив, 2026-10-18', symbol=SP,
                              text='Решение автора применяется к перечисленным в dispositions_2026-10-18.tsv записям. Ось принятия: кандидат → canonical_adopted; St_FTS и evidence_status сохраняют прежние ограничения. К1: существующие проверки и пробелы сохранены; К2: источники/развилки перечислены; К3: регистры и тип предложения сохранены; К4: конфликтные/заменённые записи исключены, формулы зависимостей не переписаны; К5: новая альтернатива открывает выбор, контрпример/несовместимость требует пересмотра. Это запись авторского принятия, не прохождение доказательных К1–К5.',
                              status='canonical_adoption_record', depends_on=[RULE], tags=['adoption_axis_only'],
                              path='17_Карточки/'+SP, internal_ref=RECORD, status_effect='canonical admission only; no evidential St_FTS promotion'))
        (SOURCE / 'fts_cards.jsonl').write_bytes(('\n'.join(json.dumps(c, ensure_ascii=False) for c in cards)+'\n').encode('utf-8'))
        triples = read_tsv(SOURCE / 'fts_triples.tsv')
        known = {tuple(t.values()) for t in triples}
        for pred, obj in [('depends_on', RULE)] + [('adopts', cid) for cid in accepted]:
            sig = (SP, pred, obj)
            if sig not in known:
                triples.append(dict(subject=SP, predicate=pred, object=obj))
        write_tsv(SOURCE / 'fts_triples.tsv', triples)
        write_tsv(PKG / 'dispositions_2026-10-18.tsv', decisions)
        for path in sorted((PKG / 'src').glob('G*.tsv')):
            data = read_tsv(path)
            for r in data:
                n = int(r['id'][3:])
                if n not in HOLD and not r['status'].startswith('canonical_adopted'):
                    r['status'] = 'canonical_adopted 2026-10-18 ('+r['id'].replace('-', '_')+'); прежняя доказательная ось: '+r['status']
            write_tsv(path, data)
    else:
        saved = read_tsv(PKG / 'dispositions_2026-10-18.tsv')
        assert saved == decisions, 'Disposition table does not match reviewed decisions'
        assert len(rows) == 127 and len(family_ids) == 87
        expected = {r['card'] for r in decisions if r['decision'] == 'canonical'}
        actual = {c['id'] for c in cards if c.get('canonical_rule') == RULE}
        assert actual == expected, (actual - expected, expected - actual)
        for cid in expected:
            c = by_id[cid]
            assert c['status'] == 'canonical_adopted' and c['St_FTS'] == c['previous_status'] == c['evidence_status']
            assert c['adoption_scope'] and c['revision_condition']
        graph = json.loads((ROOT / 'work/v14_rebuild/claim_graph/claim_graph.json').read_text(encoding='utf-8'))
        graph_cards = {n.get('card_id'): n for n in graph['nodes'] if n.get('card_id') in expected and n.get('type') == 'card'}
        assert set(graph_cards) == expected, 'Canon admissions absent from graph'
        assert all(graph_cards[cid]['evidence_status'] == by_id[cid]['evidence_status'] for cid in expected)
        print('Coverage PASS: 127 research proposals + 87 cards; no admission without preserved evidence axis; graph coverage complete.')
    print('Research canonical:', sum(d['layer']=='research' and d['decision']=='canonical' for d in decisions))
    print('Existing cards canonical:', sum(d['layer']=='card' and d['decision']=='canonical' for d in decisions))
    print('Retained with reasons:', sum(d['decision']!='canonical' for d in decisions))


if __name__ == '__main__':
    main()
