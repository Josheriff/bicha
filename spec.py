from mamba import description, context, it
from doublex import Stub, when
from expects import expect, equal

from projects_finder import ProjectsFinder
from requirements_finder import RequirementsFinder
from outdated_packages_reporter import OutdatedPackagesReporter, NO_PROJECTS_FOUND_MESSAGE, NO_REQUIREMENTS_MESSAGE

EMPTY_PROJECTS_LIST = []
A_PROJECT_LIST = ['first_project_name']

with description('Outdated packages reporter'):
    with context('when no projects found'):
        with it('reports no projects found message'):
            projects_finder = Stub(ProjectsFinder)
            when(projects_finder).find_all().returns(EMPTY_PROJECTS_LIST)
            requirements_finder = RequirementsFinder(projects_finder)
            reporter = OutdatedPackagesReporter(requirements_finder)

            report = reporter.generate_report()

            expect(report).to(equal(NO_PROJECTS_FOUND_MESSAGE))

    with context('when projects found'):
        with context('without requirements'):
            with it('reports no requirements found message'):
                projects_finder = Stub(ProjectsFinder)
                when(projects_finder).find_all().returns(A_PROJECT_LIST)
                requirements_finder = RequirementsFinder(projects_finder) 
                reporter = OutdatedPackagesReporter(requirements_finder)

                report = reporter.generate_report()

                expect(report).to(equal(NO_REQUIREMENTS_MESSAGE))
