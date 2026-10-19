"""Integration gates for the derived Obsidian vault (no canon changes)."""
import copy
import json
from pathlib import Path
import tempfile
import unittest

import obsidian_fts as export


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


if __name__=='__main__': unittest.main()
