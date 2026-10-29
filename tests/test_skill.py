import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT/"skills"/"scientific-diagrams"
sys.path.insert(0,str(SKILL/"scripts"))
from vector import Diagram, Port, bloom_pass, exact_probe_counts, sum_to_genes, pack_location
from build_examples import validate_data
from check_exports import check


class ScientificInvariants(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((SKILL/"assets"/"toy-data.json").read_text())

    def test_same_cell_and_umi_stay_separate_across_samples(self):
        counts = exact_probe_counts([("A","x","P1","u1"),("A","x","P1","u1"),("B","x","P1","u1")])
        self.assertEqual(counts,{("A","x","P1"):1,("B","x","P1"):1})

    def test_same_umi_stays_separate_across_probes_before_gene_sum(self):
        counts = exact_probe_counts([("A","x","P1","u1"),("A","x","P2","u1")])
        self.assertEqual(sum_to_genes(counts,{"P1":"G","P2":"G"}),{("A","x","G"):2})

    def test_matrix_conserves_molecules(self):
        counts, genes = validate_data(self.data)
        self.assertEqual([genes[(s,"x","G")] for s in ("A","B")],[3,2])
        self.assertEqual(sum(counts.values()),sum(genes.values()))

    def test_bloom_repeated_positions_and_false_positive(self):
        self.assertTrue(bloom_pass([1,0,1],[0,0,2,2]))
        self.assertFalse(bloom_pass([1,0,1],[0,1,2,2]))
        # Pass establishes no exact membership: the downstream dictionary may miss.
        self.assertIsNone({"present":7}.get("absent") if bloom_pass([1],[0]*4) else "rejected")

    def test_bloom_invalid_query(self):
        for bits,positions in [([1],[1]),([2],[0]),([1],[]),([1],[-1])]:
            with self.assertRaises(ValueError): bloom_pass(bits,positions)

    def test_pack_location_boundaries(self):
        self.assertEqual(pack_location(2**31-1,1,2**32-1),2**64-1)
        value = pack_location(7,1,3)
        self.assertEqual((value >> 33,(value >> 32)&1,value & (2**32-1)),(7,1,3))
        for values in [(2**31,0,0),(0,2,0),(0,0,2**32),(-1,0,0)]:
            with self.assertRaises(ValueError): pack_location(*values)

    def test_wrong_coordinate_and_bit_story_rejected(self):
        self.data["position"] = 2
        with self.assertRaises(ValueError): validate_data(self.data)


class RenderingContracts(unittest.TestCase):
    def diagram(self):
        d = Diagram(width=240,height=100,title="Editable",description="Input to output")
        d.box("a",10,30,60,30); d.text(40,45,"Input",align="center")
        d.box("b",170,30,60,30); d.text(200,45,"Output",align="center")
        return d

    def test_port_and_branch_continuity(self):
        d = self.diagram()
        a,b = d.port("a","e"),d.port("b","w")
        self.assertEqual(a.xy,(70,45)); self.assertEqual(b.xy,(170,45))
        d.fork(a,[b],(120,45))
        self.assertEqual(d.connections[0]["end"],d.connections[1]["start"])
        self.assertEqual(d.connections[1]["end"],b.xy)
        # Internal connectors must be visible above group surfaces, below labels.
        self.assertGreater(d.ax.patches[-2].get_zorder(),d.ax.patches[0].get_zorder())

    def test_round_route_is_continuous_and_attached(self):
        d = self.diagram()
        d.route(d.port("a","n"),d.port("b","n"),[(40,15),(200,15)])
        path = d.connections[-1]
        self.assertEqual(path["vertices"][0],(40,30))
        self.assertEqual(path["vertices"][-1],(200,30))
        with self.assertRaises(ValueError): d.route((1,1),(4,4),[(2,3)])

    def test_layout_failure_blocks_export(self):
        d = self.diagram(); d.text(-10,0,"clipped",size=6)
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaises(ValueError): d.save(temp,"bad")
            self.assertFalse((Path(temp)/"bad.svg").exists())

    def test_overlapping_labels_detected(self):
        d = self.diagram(); d.text(40,45,"collision")
        self.assertTrue(d.review()["text_overlaps"])

    def test_svg_pdf_png_reproduce_and_tamper_detected(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            for directory in (a,b):
                d = self.diagram(); d.connect(d.port("a","e"),d.port("b","w")); d.save(directory,"demo")
            for ext in ("svg","pdf","png"):
                self.assertEqual((Path(a)/f"demo.{ext}").read_bytes(),(Path(b)/f"demo.{ext}").read_bytes())
            self.assertEqual(check(a),[])
            with (Path(a)/"demo.png").open("ab") as f: f.write(b"changed")
            self.assertTrue(any("changed" in e for e in check(a)))

    def test_duplicate_node_and_invalid_port_rejected(self):
        d = self.diagram()
        with self.assertRaises(ValueError): d.box("a",1,1,3,3)
        with self.assertRaises(ValueError): d.port("a","invalid")

    def test_svg_keeps_bold_type_hierarchy(self):
        with tempfile.TemporaryDirectory() as temp:
            d = self.diagram(); d.text(120,15,"Heading",bold=True)
            d.save(temp,"type")
            root = ET.parse(Path(temp)/"type.svg").getroot()
            heading = next(t for t in root.iter() if t.tag.endswith("}text") and t.text == "Heading")
            self.assertIn("700",heading.attrib.get("style",""))


class PackagingContracts(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location("package_skill",ROOT/"tools/package_skill.py")
        self.package = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.package)

    def test_package_round_trip_reproducible_and_isolated(self):
        import zipfile
        with tempfile.TemporaryDirectory() as temp:
            a,b = Path(temp)/"a.zip",Path(temp)/"b.zip"
            self.assertEqual(self.package.build(a),self.package.build(b))
            with zipfile.ZipFile(a) as archive:
                self.assertIn("scientific-diagrams/SKILL.md",archive.namelist())
                self.assertFalse(any("__pycache__" in n or n.endswith(".pdf") for n in archive.namelist()))
                archive.extractall(Path(temp)/"extracted")
            self.package.validate_tree(Path(temp)/"extracted/scientific-diagrams")

    def test_unsafe_archive_rejected(self):
        import zipfile
        with tempfile.TemporaryDirectory() as temp:
            archive_path = Path(temp)/"bad.zip"
            with zipfile.ZipFile(archive_path,"w") as archive:
                archive.writestr("../escape",b"bad")
            with self.assertRaises(ValueError): self.package.verify(archive_path)


if __name__ == "__main__":
    unittest.main()
