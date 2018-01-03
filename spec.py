from mamba import description, context, it, before
from doublex import Stub, when
from expects import expect, equal

from projects_finder import ProjectsFinder
from requirements_finder import RequirementsFinder
from outdated_packages_reporter import (OutdatedPackagesReporter,
                                        NO_PROJECTS_FOUND_MESSAGE,
                                        NO_REQUIREMENTS_MESSAGE)

EMPTY_PROJECTS_LIST = []
A_PROJECT_LIST = ['first_project_name']

with description('Outdated packages reporter') as self:
    with before.each:
        self.projects_finder = Stub(ProjectsFinder)
        self.requirements_finder = RequirementsFinder(self.projects_finder)
        self.reporter = OutdatedPackagesReporter(self.requirements_finder)

    with context('when NO projects found'):
        with it('reports no projects found message'):
            when(self.projects_finder).find_all().returns(EMPTY_PROJECTS_LIST)

            report = self.reporter.generate_report()

            expect(report).to(equal(NO_PROJECTS_FOUND_MESSAGE))

    with context('when projects found'):
        with context('without requirements'):
            with it('reports no requirements found message'):
                when(self.projects_finder).find_all().returns(A_PROJECT_LIST)

                report = self.reporter.generate_report()

                expect(report).to(equal(NO_REQUIREMENTS_MESSAGE))
