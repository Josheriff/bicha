from mamba import description, context, it
from doublex import Stub, when
from expects import expect, equal

from projects_finder import ProjectsFinder
from outdated_packages_reporter import OutdatedPackagesReporter, NO_PROJECTS_FOUND_MESSAGE

EMPTY_PROJECTS_LIST = []

with description('Outdated packages reporter'):
    with context('when no projects found'):
        with it('reports no projects found'):
            projects_finder = Stub(ProjectsFinder)
            when(projects_finder).find_all().returns(EMPTY_PROJECTS_LIST)
            reporter = OutdatedPackagesReporter(projects_finder)

            report = reporter.generate_report()

            expect(report).to(equal(NO_PROJECTS_FOUND_MESSAGE))
