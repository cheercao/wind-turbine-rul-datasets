"""Validate wind turbine operational and RUL datasets integrity."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def validate():
    manifest = json.loads((ROOT / 'manifest.json').read_text(encoding='utf-8'))
    for item in manifest:
        path = ROOT / item['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], f'Hash mismatch: {path.name}'
        assert path.stat().st_size == item['bytes'], f'Size mismatch: {path.name}'
    rows = []
    for stem, expected in [('rul_blade_load_fatigue', 3600),
                           ('rul_bearing_degradation', 720),
                           ('rul_component_failures', 120)]:
        csv = pd.read_csv(ROOT / 'datasets' / f'{stem}.csv')
        pq = pd.read_parquet(ROOT / 'datasets' / f'{stem}.parquet')
        assert len(csv) == len(pq) == expected
        assert csv.columns.tolist() == pq.columns.tolist()
        for entry in manifest:
            if Path(entry['path']).stem == stem:
                assert entry['rows'] == expected and entry['columns'] == pq.columns.tolist()
        assert not csv.isna().any().any(), f'Missing values: {stem}'
        assert not pq.isna().any().any(), f'Missing values: {stem}'
        if stem == 'rul_component_failures':
            for frame in (csv, pq):
                assert frame.failed_event.isin([0, 1]).all()
                assert frame.failed_event.sum() == 44
                assert (frame.failed_event == 0).sum() == 76
                assert (frame.operating_hours > 0).all()
                for column in frame.select_dtypes(include='number'):
                    assert np.isfinite(frame[column]).all()
            assert csv.component_type.eq('Gearbox_Bearing').all()
            assert pq.groupby('component_type').size().tolist() == [30] * 4
            print('NOTE  lifetime CSV (single component) and Parquet (multi-component) variants verified')
            rows.append((stem, expected))
            continue
        for column in pq:
            if column in ('date', 'timestamp'):
                left, right = pd.to_datetime(csv[column]), pd.to_datetime(pq[column])
                assert (left == right).all(), f'Time mismatch: {column}'
            elif pd.api.types.is_numeric_dtype(pq[column]):
                assert np.isfinite(pq[column]).all()
                np.testing.assert_allclose(csv[column], pq[column], rtol=1e-12, atol=1e-12)
            else:
                np.testing.assert_array_equal(csv[column].astype(str).to_numpy(), pq[column].astype(str).to_numpy())
        if stem == 'rul_blade_load_fatigue':
            assert pq.groupby('turbine_id').size().tolist() == [600] * 6
            for _, sub in pq.groupby('turbine_id'):
                gaps = pd.to_datetime(sub.timestamp).diff().dt.total_seconds().dropna()
                np.testing.assert_allclose(gaps, .1)
        elif stem == 'rul_bearing_degradation':
            assert pq.groupby('turbine_id').size().tolist() == [120] * 6
            assert ((pq.health_index_hi > 0) & (pq.health_index_hi <= 1)).all()
            for _, sub in pq.groupby('turbine_id'):
                np.testing.assert_array_equal(sub.operating_days, np.arange(120))
        else:
            assert pq.failed_event.isin([0, 1]).all()
            assert pq.failed_event.sum() == 44
            assert (pq.failed_event == 0).sum() == 76
            assert (pq.operating_hours > 0).all()
            assert pq.groupby('component_type').size().tolist() == [30] * 4
        rows.append((stem, expected))
    for name, count in rows:
        print(f'PASS  {name}: {count:,} rows per file; documented structure verified')
    print('PASS  all 6 SHA-256 hashes match the original upload')
    return rows


if __name__ == '__main__':
    validate()
