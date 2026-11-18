"""Correctness checks use synthetic fixtures only, never research observations."""
import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from pipeline import bind_source, decode_value, read_candidate, read_station, summarize


class ScientificExtractionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.directory = Path(self.tmp.name)
        self.source = {
            "earth_candidate_id": "TEST-A", "mars_candidate_id": "TEST-M", "latitude_deg": -70,
            "longitude_east_deg": 160, "adapter": "campbell_toa5", "path": "fixture.csv",
            "source_id": "synthetic-only", "spatial_support": "synthetic station point", "horizontal_datum": "unknown",
            "sample_interval_minutes": 30, "period_start": "2020-01-01T00:00:00", "period_end_exclusive": "2020-03-01T00:00:00",
            "time_standard": "unknown", "timestamp_formats": ["%m/%d/%Y %H:%M", "%Y-%m-%d %H:%M:%S"],
            "decimal_day_epoch": "2009-01-01T00:00:00", "decimal_day_tolerance_days": .0001,
            "missing_tokens": ["NaN", ""], "dataset_doi": "synthetic", "method_url": "synthetic",
            "variables": [{"column": c, "quantity": "temperature", "unit": "Deg C", "height_above_surface_m": h,
                           "scale_factor": 1, "add_offset": 0, "valid_range": [-50,50]} for c,h in [("a",1),("b",-.42)]],
            "paired_differences": [{"metric_id":"a_minus_b", "columns":["a","b"]}]}
        self.candidate = {"earth_candidate_id":"TEST-A", "mars_candidate_id":"TEST-M", "site_name":"Synthetic fixture",
                          "latitude_deg":-70, "longitude_east_deg":160, "requirements_version":"TEST-v1"}

    def fixture(self, values):
        path = self.directory/"fixture.csv"
        rows = [["TOA5"], ["TIMESTAMP","decimalDaySinceJan1_2009","a","b"], ["TS","days","Deg C","Deg C"], ["","","Smp","Smp"]]
        epoch = datetime(2009,1,1)
        for stamp,a,b in values:
            t = datetime.fromisoformat(stamp)
            rows.append([stamp, f"{(t-epoch).total_seconds()/86400:.4f}", a,b])
        with path.open("w",newline="") as f: csv.writer(f).writerows(rows)
        self.source["expected_md5"] = hashlib.md5(path.read_bytes()).hexdigest()
        return path

    def test_missing_scale_fill_and_range_are_separate(self):
        var = {"scale_factor":.02,"add_offset":-273.15,"fill_values":[0],"valid_range":[-50,50]}
        self.assertEqual(decode_value("0",var,["NaN"]), (None,"fill_value"))
        self.assertEqual(decode_value("NaN",var,["NaN"]), (None,"missing_token"))
        self.assertAlmostEqual(decode_value("14000",var,[])[0], 6.85)
        self.assertEqual(decode_value("10000",var,[])[1], "outside_instrument_range")

    def test_calendar_leap_year_and_single_month_do_not_create_annual_mean(self):
        path = self.fixture([("2020-01-01 00:00:00",-10,-12)])
        records,_ = read_station(path,self.source)
        rows = summarize(records,self.source,self.candidate,"fixturehash","TEST-v1")
        a = [r for r in rows if r['metric_id']=='a']
        self.assertEqual([r['expected_n'] for r in a],[1488,1392])
        self.assertEqual([r['valid_n'] for r in a],[1,0])
        self.assertEqual(a[1]['observed_mean'],"")
        self.assertTrue(all(r['annual_statistic']=='not_computed' for r in rows))
        self.assertTrue(all(r['suitability_threshold_status']=='not_defined' for r in rows))

    def test_pair_uses_only_intersection_of_same_time_observations(self):
        path=self.fixture([("2020-01-01 00:00:00",-10,-12),("2020-01-01 00:30:00",-40,"NaN"),("2020-01-01 01:00:00","NaN",-1)])
        records,_=read_station(path,self.source)
        row=next(r for r in summarize(records,self.source,self.candidate,"h","TEST") if r['metric_id']=='a_minus_b')
        self.assertEqual(row['valid_n'],1)
        self.assertEqual(row['observed_mean'],2)
        self.assertEqual(row['present_but_invalid_n'],2)

    def test_gap_count_and_no_interpolation(self):
        path=self.fixture([("2020-01-01 00:00:00",-10,-12),("2020-01-01 01:30:00",-20,-22)])
        records,qa=read_station(path,self.source)
        self.assertEqual(len(records),2)
        self.assertEqual(qa['timestamp_gaps'][0]['missing_slots'],2)

    def test_identical_duplicate_deduplicated(self):
        row=("2020-01-01 00:00:00",-10,-12)
        records,qa=read_station(self.fixture([row,row]),self.source)
        self.assertEqual(len(records),1)
        self.assertEqual(qa['identical_duplicate_rows_removed'],1)

    def test_conflicting_duplicate_blocks_extraction(self):
        path=self.fixture([("2020-01-01 00:00:00",-10,-12),("2020-01-01 00:00:00",-11,-12)])
        with self.assertRaisesRegex(ValueError,"Conflicting duplicate"):read_station(path,self.source)

    def test_modified_file_fails_checksum(self):
        path=self.fixture([("2020-01-01 00:00:00",-10,-12)])
        path.write_text(path.read_text().replace('-10','-11'))
        with self.assertRaisesRegex(ValueError,"checksum"):read_station(path,self.source)

    def test_decimal_day_disagreement_blocks_time_series(self):
        path=self.fixture([("2020-01-01 00:00:00",-10,-12)])
        path.write_text(path.read_text().replace('4017.0000','4018.0000'))
        self.source['expected_md5']=hashlib.md5(path.read_bytes()).hexdigest()
        with self.assertRaisesRegex(ValueError,"Date encoding"):read_station(path,self.source)

    def test_station_cannot_be_reassigned_to_other_coordinate(self):
        self.candidate['latitude_deg']=-69
        with self.assertRaisesRegex(ValueError,"latitude_deg"):bind_source(self.candidate,self.source)

    def test_next_candidate_via_config_preserves_original_fields(self):
        path=self.directory/'candidates.csv'
        original={'earth_candidate_id':'TEST-NEXT','mars_candidate_id':'TEST-M2','earth_site_name':'Next fixture',
                  'earth_lat_deg':'-60','earth_lon_east_deg':'150','coordinate_basis':'point anchor only',
                  'test_purpose':'synthetic test','source_urls':'https://example.invalid','review_date':'2026-11-14',
                  'custom_original_field':'keep me'}
        with path.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(original));w.writeheader();w.writerow(original)
        candidate=read_candidate(path,'TEST-NEXT')
        for k,v in original.items():self.assertEqual(candidate[k],v)
        self.source.update(earth_candidate_id='TEST-NEXT',mars_candidate_id='TEST-M2',latitude_deg=-60,longitude_east_deg=150)
        bind_source(candidate,self.source)
        records,_=read_station(self.fixture([('2020-01-01 00:00:00',-10,-12)]),self.source)
        rows=summarize(records,self.source,candidate,'h','TEST')
        self.assertTrue(all(r['earth_candidate_id']=='TEST-NEXT' and r['latitude_deg']=='-60' for r in rows))


if __name__ == '__main__':
    unittest.main()
