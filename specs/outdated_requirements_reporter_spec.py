from mamba import description, context, it, before
from doublex import Stub, when
from expects import expect, equal

from model.project import Project
from model.project_report import ProjectReport
from model.report import Report
from services.version_checker import VersionChecker
from services.projects_finder import ProjectsFinder
from services.outdated_requirements_reporter import (OutdatedRequirementsReporter,
                                                     NO_PROJECTS_FOUND_MESSAGE)

EMPTY_PROJECTS_LIST = []
UP_TO_DATE_REQUIREMENT = 'an_up_to_date_requirement'
OUTDATED_REQUIREMENT = 'an_outdated_requirement'
PROJECT_WITH_UP_TO_DATE_REQUIREMENTS = Project(project_name='project_with_up_to_date_requirements', requirements=[UP_TO_DATE_REQUIREMENT])
PROJECT_WITH_OUTDATED_REQUIREMENTS = Project(project_name='project_with_outdated_requirements', requirements=[OUTDATED_REQUIREMENT])
PROJECT_WITH_UP_TO_DATE_AND_OUTDATED_REQUIREMENTS = Project(project_name='project_with_mixed_requirements', requirements=[UP_TO_DATE_REQUIREMENT, OUTDATED_REQUIREMENT])

with description('Outdated requirements reporter') as self:
    with before.each:
        self.projects_finder = Stub(ProjectsFinder)
        self.version_checker = Stub(VersionChecker)
        self.reporter = OutdatedRequirementsReporter(self.projects_finder, self.version_checker)

    with context('when NO projects found'):
        with it('reports no projects found message'):
            when(self.projects_finder).find_all().returns(EMPTY_PROJECTS_LIST)

            report = self.reporter.generate_report()

            expected_report = Report(NO_PROJECTS_FOUND_MESSAGE)
            expect(report).to(equal(expected_report))

    with context('when projects found'):
        with before.each:
            when(self.version_checker).is_outdated(OUTDATED_REQUIREMENT).returns(True)
        with context('all requirements up to date'):
            with it('reports nothing'):
                when(self.projects_finder).find_all().returns([PROJECT_WITH_UP_TO_DATE_REQUIREMENTS])
                report = self.reporter.generate_report()
               
                empty_report = Report()
                expect(report).to(equal(empty_report))

        with context('a requirement is outdated'):
            with it('reports the project outdated and the requirement'):
                when(self.projects_finder).find_all().returns([PROJECT_WITH_OUTDATED_REQUIREMENTS])

                report = self.reporter.generate_report()

                outdated_project_report = ProjectReport(project_name=PROJECT_WITH_OUTDATED_REQUIREMENTS.project_name, outdated_requirements=[OUTDATED_REQUIREMENT])
                expected_report = Report()
                expected_report.add_project_report(outdated_project_report)
                expect(report).to(equal(expected_report))

        with context('some project has up to date and outdated requirements'):
            with it('reports just the outdated requirements'):
                when(self.projects_finder).find_all().returns([PROJECT_WITH_UP_TO_DATE_AND_OUTDATED_REQUIREMENTS])

                report = self.reporter.generate_report()

                project_report = ProjectReport(project_name=PROJECT_WITH_UP_TO_DATE_AND_OUTDATED_REQUIREMENTS.project_name, outdated_requirements=[OUTDATED_REQUIREMENT])
                expected_report = Report()
                expected_report.add_project_report(project_report)
                expect(report).to(equal(expected_report))
