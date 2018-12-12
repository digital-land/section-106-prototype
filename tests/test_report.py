from application.report_summary import ReportSummary


def test_error_count(json_data):
    summary = ReportSummary(json_data)
    assert summary.total_errors() == 4


def test_errors_by_type(json_data):
    summary = ReportSummary(json_data)
    errors_by_type = summary.errors_by_type()

    assert errors_by_type['pattern-constraint']['count'] == 2
    assert 'developer-agreement-type' in errors_by_type['pattern-constraint']['columns']
    assert 'organisation' in errors_by_type['pattern-constraint']['columns']

    assert errors_by_type['type-or-format-error']['count'] == 2
    assert 'entry-date' in errors_by_type['type-or-format-error']['columns']
    assert 'document-url' in errors_by_type['type-or-format-error']['columns']


def test_format(json_data):
    summary = ReportSummary(json_data)
    assert 'csv' == summary.file_format()


def test_valid(json_data):
    summary = ReportSummary(json_data)
    assert not summary.is_valid()