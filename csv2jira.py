#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import unicodecsv as csv

from jira import JIRA, JIRAError

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Creates standardized issues for a Scrum sprint')
    parser.add_argument('-s', action='store', required=True, help='Server')
    parser.add_argument('-u', action='store', required=True, help='Username')
    parser.add_argument('-p', action='store', required=True, help='Password')
    parser.add_argument('-i', action='store', type=argparse.FileType('r'), required=True, help='Input file')

    # -s https://jira.atlassian.com -u username -p 1234 -i issues.csv

    # http://jira.readthedocs.io/en/latest/examples.html#quickstart
    # Required dependencies:
    #   Argparse
    #   sudo apt-get install ipython
    #   sudo pip install jira

    arguments = parser.parse_args()

    server = arguments.s
    username = arguments.u
    password = arguments.p
    input_file = arguments.i

    print server, username, password

    # read csv
    with open(input_file.name, 'rb') as csv_file:
        try:
            reader = csv.DictReader(csv_file, delimiter=';')
            jira = JIRA(server=server, basic_auth=(username, password))

            for row in reader:
                project_key = row['PROJECT_KEY']
                issue_type = row['ISSUE_TYPE']
                summary = row['SUMMARY']
                description = row['DESCRIPTION']
                assignee = row['ASSIGNEE']

                # print project_key, issue_type, summary, description, assignee

                issue_data = {
                    'project': {'id': project_key},
                    'issuetype': {'name': issue_type},
                    'summary': summary,
                    'description': description
                }

                # would be nice to have:
                # duedate='2016-11-11', timeestimate='2.5', sprint (which field ?), component,

                if assignee is not None and assignee.strip() != '':
                    issue_data['assignee'] = {'name': assignee}

                new_issue = jira.create_issue(fields=issue_data)

        except csv.Error as e:
            print e.status_code, e.text
            print 'file %s, line %d: %s' % (csv_file, reader.line_num, e)
        except JIRAError as e:
            print e.status_code, e.text
        finally:
            csv_file.close()
