import requests
import json
import yaml
import os

headers = {"Authorization": "bearer {}".format(os.getenv("GITHUB_TOKEN"))}

PATH_PROJECT = os.path.realpath(os.path.dirname(__file__))


class Maven_scanner():
    def __init__(self, appname):
        self.appname = appname
        self.advisory_list = []
        self.query = yaml.safe_load(open(PATH_PROJECT + '/../data/queries.yaml')).get('maven_query')

    def get_advisories(self, package):
        vulndata = []
        hasnext = True
        nextcursor = None
        while hasnext:
            variables = {'package': package, 'after': nextcursor}
            request = requests.post('https://api.github.com/graphql',
                                    json={'query': self.query, 'variables': variables}, headers=headers)
            if request.status_code == 200:
                data = json.loads(request.content)
                vulndata = vulndata + data.get('data').get('securityVulnerabilities').get('nodes')
                hasnext = data.get('data').get('securityVulnerabilities').get('pageInfo').get('hasNextPage')
                nextcursor = data.get('data').get('securityVulnerabilities').get('pageInfo').get('endCursor')
            else:
                raise Exception("Error running the query. Error {}".format(request.status_code))

        return vulndata

    def validate_vulnerable_version(self, advisories, package, version):
        for advisory in advisories:
            major_eq = False
            minor_eq = False
            try:
                bottom, top = advisory.get('vulnerableVersionRange').split(',')
                if '>=' in bottom:
                    major_eq = True
                if '<=' in top:
                    minor_eq = True
                bottomnumber = bottom.replace('>', '').replace('=', '').strip()
                topnumber = top.replace('<', '').replace('=', '').strip()
                if bottomnumber < version < topnumber or (version == bottomnumber and minor_eq) or (
                        version == topnumber and major_eq):
                    advisory = self.parse_identifiers(advisory)
                    self.advisory_list.append({'package': package + ':' + version, 'advisory': advisory.copy()})
            except ValueError:  # no top version
                top = advisory.get('vulnerableVersionRange')
                if '<=' in top:
                    minor_eq = True
                topnumber = top.replace('<', '').replace('=', '').strip()
                if version < topnumber or (version == topnumber and minor_eq):
                    advisory = self.parse_identifiers(advisory)
                    self.advisory_list.append({'package': package + ':' + version, 'advisory': advisory.copy()})

    def parse_identifiers(self, advisory):
        dicts = advisory.get('advisory').get('identifiers')
        advisory.get('advisory')['cve'] = next((id for id in dicts if id.get('type') == "CVE"),
                                               {'type': 'CVE', 'value': ''})
        advisory.get('advisory')['ghsa'] = next((id for id in dicts if id.get('type') == "GHSA"),
                                                {'type': 'GHSA', 'value': ''})
        return advisory
