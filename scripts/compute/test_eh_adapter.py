"""Synthetic edge cases for exporting the inherited EH2 row parser."""
from datetime import datetime
import unittest

from eh_adapter import parse_page, to_tidy, validate_rows, window_summaries


class EHExportTests(unittest.TestCase):
    def test_omitted_3cm_triad_stays_blank_and_supersaturated_RH_retained(self):
        rows,errors=parse_page('1 11/28/17 0:00 11/28/17 1:30 -8.20 56.07 59.40 -12.60 86.78 101.23',1)
        self.assertFalse(errors)
        out=to_tidy(rows,{'earth_candidate_id':'FIXTURE','mars_candidate_id':'M'}, {'source_id':'fixture','expected_sha256':'fixture'})[0]
        self.assertEqual(out['T_3cm_C'],'')
        self.assertEqual(out['T_3cm_C__status'],'not_published')
        self.assertEqual(out['RH_49cm_ice_corrected_pct'],101.23)
        self.assertEqual(out['RH_49cm_ice_corrected_pct__status'],'above_100_retained')
        self.assertEqual(out['raw_time_1'],'11/28/17 0:00')
        self.assertEqual(out['raw_time_2'],'11/28/17 1:30')

    def test_malformed_numeric_column_count_is_an_error(self):
        rows,errors=parse_page('1 11/28/17 0:00 11/28/17 1:30 1 2 3 4 5 6 7',1)
        self.assertFalse(rows)
        self.assertEqual(len(errors),1)

    def test_shifted_second_clock_blocks_export(self):
        rows,_=parse_page('1 11/28/17 0:00 11/28/17 2:30 1 2 3 4 5 6',1)
        with self.assertRaisesRegex(ValueError,'relation'):
            validate_rows(rows,{'expected_records':1})

    def test_no_annual_3cm_and_pair_is_same_row(self):
        rows,_=parse_page('1 12/1/17 0:00 12/1/17 1:30 -8 50 60 -12 80 95 -4 70 80\n2 12/1/17 1:00 12/1/17 2:30 -9 50 60 -10 80 95',1)
        result=window_summaries(rows,{'summer_start':'2017-12-01T00:00:00','summer_end_exclusive':'2018-03-01T00:00:00','period_start':'2017-12-01T00:00:00','period_end_exclusive':'2018-12-01T00:00:00'})
        paired=next(r for r in result if r['metric_id']=='T_3cm_minus_49cm_C')
        self.assertEqual(paired['valid_n'],1)
        self.assertEqual(paired['observed_mean'],8)
        self.assertFalse(any(r['window']=='paper_year' and r['metric_id']=='T_3cm_C' for r in result))

    def test_no_valid_pairs_retains_missing_summary(self):
        rows,_=parse_page('1 12/1/17 0:00 12/1/17 1:30 -8 50 60 -12 80 95',1)
        result=window_summaries(rows,{'summer_start':'2017-12-01T00:00:00','summer_end_exclusive':'2018-03-01T00:00:00','period_start':'2017-12-01T00:00:00','period_end_exclusive':'2018-12-01T00:00:00'})
        paired=next(r for r in result if r['metric_id']=='T_3cm_minus_49cm_C')
        self.assertEqual(paired['valid_n'],0)
        self.assertEqual(paired['observed_mean'],'')


if __name__=='__main__':
    unittest.main()
