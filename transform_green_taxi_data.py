import re

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    
    data.columns = [re.sub(r'(?<=[a-z])(?=[A-Z]|\d)', '_', col).title().lower() for col in data.columns]
    
    return data

@test
def test_output(output, *args) -> None:
    
    assert 'vendor_id' in output.columns, 'vendor_id column does not exist'

    assert (output['passenger_count'] > 0).all(), 'There are rows with passenger_count <= 0'

    assert (output['trip_distance'] > 0).all(), 'There are rows with trip_distance <= 0'
