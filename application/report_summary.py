class ReportSummary:

    def __init__(self, report):
        self.report = report

    def is_valid(self):
        return self.report['tables'][0]['valid']

    def file_format(self):
        return self.report['tables'][0]['format']

    def total_errors(self):
        return self.report['error-count']

    def errors_by_type(self):
        err_types = {}
        for t in self.report['tables']:
            for e in t['errors']:
                if e['code'] not in err_types:
                    column_name = t['headers'][e['column-number'] - 1]
                    err_types[e['code']] = {'count': 1, 'columns': [column_name]}
                else:
                    column_name = t['headers'][e['column-number'] - 1]
                    err_types[e['code']]['count'] += 1
                    err_types[e['code']]['columns'].append(column_name)
        return err_types