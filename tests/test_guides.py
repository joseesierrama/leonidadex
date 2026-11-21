import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from guide_pages import load_guides, page_body

class GuideTests(unittest.TestCase):
    def setUp(self):
        self.data=load_guides(ROOT/'src')

    def validate_copy(self,data):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)
            (path/'guias.json').write_text(json.dumps(data),encoding='utf-8')
            return load_guides(path)

    def test_bad_video_and_missing_related_guide_block_build(self):
        bad=copy.deepcopy(self.data)
        video=next(g for g in bad['guias'] if g.get('video'))
        video['video']['id']='bad"><iframe src=evil'
        with self.assertRaisesRegex(ValueError,'Vídeo'):
            self.validate_copy(bad)
        bad=copy.deepcopy(self.data);bad['guias'][0]['relacionadas']=['no-existe']
        with self.assertRaisesRegex(ValueError,'relacionada'):
            self.validate_copy(bad)

    def test_each_video_belongs_to_a_step_and_starts_unloaded(self):
        for guide in self.data['guias']:
            with self.subTest(guide=guide['id']):
                text=page_body(guide,self.data)
                self.assertNotIn('<iframe',text)
                if guide.get('video'):
                    self.assertEqual(text.count('data-load-video'),1)
                    step_start=text.index('id="paso-'+str(guide['paso_video'])+'"')
                    clip_start=text.index('data-video-block')
                    self.assertGreater(clip_start,step_start)
                    self.assertIn('Abrir original en YouTube',text)
                if guide.get('spoiler'):
                    self.assertIn('<details class="gv-spoilers" data-guide-spoilers>',text)
                    self.assertNotIn('data-guide-spoilers open',text)

    def test_all_map_destinations_exist_and_text_is_escaped(self):
        base=json.loads((ROOT/'src/base.json').read_text('utf-8'))
        dyn=json.loads((ROOT/'src/actualizaciones.json').read_text('utf-8'))
        pins={p['id'] for p in base['mapa_lugares']+dyn['mapa_lugares']}
        for guide in self.data['guias']:
            if guide.get('mapa'):self.assertIn(guide['mapa'],pins)
        guide=copy.deepcopy(self.data['guias'][0]);guide['titulo']='<script>alert(1)</script>'
        rendered=page_body(guide,self.data)
        self.assertNotIn('<script>alert',rendered)
        self.assertIn('&lt;script&gt;',rendered)
