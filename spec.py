from doublex import Stub
from expects import expect, equal

EMPTY_PROJECTS_LIST = []

with describe('Outdated packages reporter'):
    with context('when no projects found'):
        with it('reports no projects found'):
            projects_finder = Stub(ProjectsFinder)
            when(projects_finder.find_all()).returns(EMPTY_PROJECTS_LIST)
            reporter = OutdatedPackagesReporter(projects_finder)

            report = reporter.generate_report()

            expect(report).to(equal('No projects found'))
