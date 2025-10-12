import pandas as pd
from backend.main import ETLProcessor


def test_transform_filters_and_transformations_cover_branches(tmp_path):
  processor = ETLProcessor(data_dir='data', output_dir=str(tmp_path))
  df = pd.DataFrame({
      'num': [1, 2, 3, 4],
      'cat': ['A', 'B', 'A', 'C'],
      'eq': ['x', 'y', 'x', 'z'],
  })
  processor.raw_data = df

  filters = {
      'num': {'min': 2, 'max': 4},
      'cat': ['A', 'B'],
      'eq': 'x',
      'missing': {'min': 0},  # exercise missing column branch
  }
  transformations = ['normalize', 'standardize', 'log_transform']

  processed = processor.transform(filters=filters, transformations=transformations)
  assert processed is not None
  assert len(processed) >= 1

  # Cover chart config branches with existing numeric column
  cfg_bar = processor.generate_apexcharts_config('bar')
  cfg_pie = processor.generate_apexcharts_config('pie')
  assert 'series' in cfg_bar and 'series' in cfg_pie

  # Cover loading to files
  outputs = processor.load('csv')
  assert 'csv' in outputs
