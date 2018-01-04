from mamba import description, context, it, before
from doublex import Stub, when
from expects import expect, equal

from requirements_finder import RequirementsFinder
from project_requirements import ProjectRequirements
from outdated_packages_reporter import (OutdatedPackagesReporter,
                                        NO_PROJECTS_FOUND_MESSAGE,
                                        NO_REQUIREMENTS_MESSAGE,
                                        ALL_REQUIREMENTS_UP_TO_DATE)

EMPTY_PROJECTS_LIST = []
A_LIST_OF_PROJECTS_WITHOUT_REQUIREMENTS = ['project_without_requirements_1']
A_LIST_OF_PROJECTS_WITH_UP_TO_DATE_REQUIREMENTS = ['project_with_up_to_date_requirements_1']

with description('Outdated packages reporter') as self:
    with before.each:
        self.requirements_finder = Stub(RequirementsFinder)
        self.reporter = OutdatedPackagesReporter(self.requirements_finder)

    with context('when NO projects found'):
        with it('reports no projects found message'):
            when(self.requirements_finder).find_all().returns([])

            report = self.reporter.generate_report()

            expect(report).to(equal(NO_PROJECTS_FOUND_MESSAGE))

    with context('when projects found'):
        with context('without requirements'):
            with it('reports no requirements found message'):
                when(self.requirements_finder).find_all().returns([ProjectRequirements(project_name='fulanito', requirements=[])])

                report = self.reporter.generate_report()

                expect(report).to(equal(NO_REQUIREMENTS_MESSAGE))

        with context('with some requirements'):
            with context('all requirements up to date'):
                with it('reports all requirements up to date message'):
                    requirements_finder = Stub(RequirementsFinder)
                    when(requirements_finder).find_all().returns([ProjectRequirements(project_name='pepito', requirements=['hola'])])
                    reporter = OutdatedPackagesReporter(requirements_finder)
                    report = reporter.generate_report()
                    
                    expect(report).to(equal(ALL_REQUIREMENTS_UP_TO_DATE))
