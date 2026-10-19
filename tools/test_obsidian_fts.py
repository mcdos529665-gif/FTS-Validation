"""Integration gates for the derived Obsidian vault (no canon changes)."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import obsidian_fts as export
import obsidian_fts_corpus as corpus


class VaultTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.enc=export.Encyclopedia(export.ROOT)
        cls.enc.build()
        cls.enc.files[export.FOLDERS[9]+'/Состояние обновления.md']='# Состояние обновления\n'
        cls.validation=cls.enc.verify()
        cls.enc.files.pop(export.FOLDERS[9]+'/Состояние обновления.md')
        cls.temp_root=Path('E:/Codex/cache/fts-obsidian-tests')
        cls.temp_root.mkdir(parents=True,exist_ok=True)

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(dir=self.temp_root)
        self.addCleanup(self.temp.cleanup)
        self.vault=Path(self.temp.name)/'vault'

    def write(self, enc=None):
        return export.publish(self.vault,enc or self.enc,write=True,date='2026-10-19')

    def test_coverage_links_exact_records_and_sample(self):
        self.assertEqual(self.validation,[])
        self.assertEqual(len(self.enc.paths),len(self.enc.nodes))
        self.assertTrue(any(n['type']=='open_question' for n in self.enc.nodes.values()))
        self.assertTrue(any(n['type']=='verification' for n in self.enc.nodes.values()))
        self.assertIn('Проверка математического предиката не повышает',self.enc.page(self.enc.nodes['card_a_07']))

    def test_byte_idempotence_and_personal_notes(self):
        self.write()
        note=self.vault/export.FOLDERS[8]/'Моя мысль.md'
        note.write_text('Личный комментарий: сохранять точно.\n',encoding='utf-8')
        before={p.relative_to(self.vault).as_posix():p.read_bytes() for p in self.vault.rglob('*') if p.is_file()}
        result=self.write()
        after={p.relative_to(self.vault).as_posix():p.read_bytes() for p in self.vault.rglob('*') if p.is_file()}
        self.assertEqual(before,after)
        self.assertEqual(result['create_or_update'],0)

    def test_manual_edit_stops_entire_write_and_keeps_both_versions(self):
        self.write()
        page=self.vault/export.HOME
        edited=page.read_bytes()+b'\nMy manual edit\n'
        page.write_bytes(edited)
        with self.assertRaises(RuntimeError): self.write()
        self.assertEqual(page.read_bytes(),edited)
        conflicts=list((self.vault/export.FOLDERS[9]/'Конфликты').rglob('сохранённая-правка-*.md'))
        self.assertTrue(conflicts)
        self.assertEqual(conflicts[0].read_bytes(),edited)

    def test_removed_page_retained_as_archive_and_stable(self):
        enc=copy.copy(self.enc); enc.files=self.enc.files.copy()
        rel=export.FOLDERS[6]+'/obsolete — Прежняя сущность.md'
        enc.files[rel]='# Прежняя сущность\n'
        self.write(enc)
        self.write()
        content=(self.vault/rel).read_bytes()
        self.assertIn('Архивная страница'.encode(),content)
        self.write()
        self.assertEqual((self.vault/rel).read_bytes(),content)

    def test_changed_editorial_source_is_flagged(self):
        enc=copy.copy(self.enc); enc.editorial=copy.deepcopy(self.enc.editorial); enc.stale_editorial=[]
        enc.editorial['OP_Lift']['source_sha256']='different'
        node=next(n for n in enc.nodes.values() if n.get('card_id')=='OP_Lift' and enc.card_for(n))
        text=enc.page(node)
        self.assertIn('Пояснение требует пересмотра',text)
        self.assertIn('OP_Lift',enc.stale_editorial)

    def test_published_paths_stay_stable_when_title_changes(self):
        mapping=self.enc.paths.copy()
        mapping['card_op_lift']=export.FOLDERS[4]+'/OP_Lift — Прежнее название.md'
        enc=export.Encyclopedia(export.ROOT,mapping)
        self.assertEqual(enc.paths['card_op_lift'],mapping['card_op_lift'])

    def test_path_traversal_rejected(self):
        with self.assertRaises(ValueError): export.checked_path(self.vault,'../outside.md')

    def test_obsidian_link_syntax_and_windows_filenames(self):
        self.assertNotIn('[[',export.cell([[-1,0,1],[1,2,3]]))
        for path in self.enc.paths.values():
            if '#' not in path:
                self.assertEqual(Path(path).stem,Path(path).stem.rstrip(' .'))

    def test_work_census_covers_every_markdown_and_preserves_all_lines(self):
        actual={p.relative_to(export.ROOT).as_posix() for p in (export.ROOT/'work').rglob('*.md')}
        self.assertEqual(actual,{d['path'] for d in self.enc.corpus.documents})
        for d in self.enc.corpus.documents:
            if not d['included']: continue
            original=(export.ROOT/d['path']).read_text(encoding='utf-8-sig').splitlines()
            addressed=[n for s in d['sections'] for n in range(s['start'],s['end']+1)]
            self.assertEqual(list(range(1,len(original)+1)),addressed,d['path'])
            text=self.enc.files[d['page']]
            for s in d['sections']:
                self.assertEqual('\n'.join(original[s['start']-1:s['end']]),s['text'])
                self.assertIn('## '+s['anchor']+'\n',text)
                self.assertIn('### '+s['title'],text)

    def test_heading_parser_ignores_code_and_partitions_text(self):
        text='# Title\n\n```python\n# code comment\n```\n\n## Next\nbody\n'
        parts=corpus.sections(text)
        self.assertEqual([x['title'] for x in parts],['Title','Next'])
        self.assertEqual([n for s in parts for n in range(s['start'],s['end']+1)],list(range(1,len(text.splitlines())+1)))

    def test_facets_require_exact_source_hash_and_quote(self):
        obj=copy.copy(self.enc.corpus)
        obj.facets=copy.deepcopy(obj.facets)
        self.assertTrue(obj.facets,'Reviewed substantive facets must exist')
        obj.errors=[]; obj.by_entity=__import__('collections').defaultdict(list)
        obj.facets[0]['exact_quote']+=' invented condition'
        obj.validate_facets()
        self.assertTrue(any('Неточный фрагмент' in e for e in obj.errors))

    def test_stale_facet_is_withheld_and_marked_for_review(self):
        obj=copy.copy(self.enc.corpus)
        obj.facets=copy.deepcopy(obj.facets[:1]); obj.stale_facets=[]
        obj.errors=[]; obj.by_entity=__import__('collections').defaultdict(list)
        obj.facets[0]['source_sha256']='changed'
        obj.validate_facets()
        self.assertEqual(obj.errors,[])
        self.assertEqual(obj.stale_facets,obj.facets)
        cid=obj.facets[0]['entity_ids'][0]
        text=obj.render_facets(cid,export.link,export.cell,export.fenced)
        self.assertIn('Требуют пересмотра',text)
        self.assertNotIn(obj.facets[0]['summary_ru'],text)

    def test_question_coverage_does_not_imply_an_answer(self):
        expected=[x for x in (export.ROOT/'work/v14_rebuild/claim_questions/QUESTION_CARDS.jsonl').read_text(encoding='utf-8').splitlines() if x.strip()]
        self.assertEqual(len(self.enc.corpus.questions),len(expected))
        unanswered=[q for q in self.enc.corpus.questions if q.get('answer_status')=='unanswered' and q.get('corpus_coverage')=='covered']
        self.assertTrue(unanswered)
        text=self.enc.page(self.enc.nodes['card_u_00'])
        self.assertIn('Вопросы к сущности',text)
        self.assertIn('unanswered',text)

    def test_all_other_work_formats_have_explicit_inventory_decisions(self):
        expected={p.relative_to(export.ROOT).as_posix() for p in (export.ROOT/'work').rglob('*') if p.is_file() and p.suffix.lower()!='.md'}
        self.assertEqual(expected,{a['path'] for a in self.enc.corpus.assets})
        for a in self.enc.corpus.assets:
            self.assertTrue(a.get('excluded_reason') or (a.get('sha256') and a.get('content_review')))

    def test_asset_review_is_bound_to_current_source_hash(self):
        obj=copy.copy(self.enc.corpus)
        asset=next(a for a in obj.assets if not a.get('excluded_reason'))
        rel=asset['path']
        obj.reviews={rel:{'sha256':asset['sha256'],'review_note':'Проверена конкретная область.'}}
        obj.assets=[]; obj.scan_assets()
        current=next(a for a in obj.assets if a['path']==rel)
        self.assertTrue(current['review'])
        self.assertFalse(current['review_stale'])
        obj.reviews[rel]['sha256']='changed'
        obj.assets=[]; obj.scan_assets()
        changed=next(a for a in obj.assets if a['path']==rel)
        self.assertFalse(changed['review'])
        self.assertTrue(changed['review_stale'])
        self.assertNotIn('Проверена конкретная область.',changed['content_review'])


if __name__=='__main__': unittest.main()
