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
        with context('and project with all requirements up to date'):
            with context('and project with all requirements outdated'):
                with context('and project with some requirements up to date and some outdated'):
                    with it('reports only projects with their outdated requirements'):
                        when(self.projects_finder).find_all().returns([PROJECT_WITH_UP_TO_DATE_REQUIREMENTS,
                                                                       PROJECT_WITH_OUTDATED_REQUIREMENTS,
                                                                       PROJECT_WITH_UP_TO_DATE_AND_OUTDATED_REQUIREMENTS
                                                                       ])

                        report = self.reporter.generate_report()

                        expected_report = Report()
                        project_report_1 = ProjectReport(project_name=PROJECT_WITH_OUTDATED_REQUIREMENTS.project_name,
                                                       outdated_requirements=[OUTDATED_REQUIREMENT])
                        project_report_2 = ProjectReport(project_name=PROJECT_WITH_UP_TO_DATE_AND_OUTDATED_REQUIREMENTS.project_name,
                                                        outdated_requirements=[OUTDATED_REQUIREMENT])
                        expected_report.add_project_report(project_report_1)
                        expected_report.add_project_report(project_report_2)
                        expect(report).to(equal(expected_report))
