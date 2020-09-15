#!/usr/bin/python3.7

import luigi
import json

import getPdf
import pdf2date
import pdf2cases
import getCases
import bqInsert

class GetId(luigi.Task):
    index = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.getId.txt")

    def run(self):
        with self.output().open('w') as target:
            target.write('OK')


class DownloadPdf(luigi.Task):
    index = luigi.Parameter()

    retry_count = 20
    retry_delay = 60

    def requires(self):
        return GetId(self.index)

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.downloadPdf.txt")

    def run(self):
        with self.output().open('w') as target:
            filename = getPdf.getGovPdf(self.index)
            target.write(filename)


class CasesProcess(luigi.Task):
    index = luigi.Parameter()

    def requires(self):
        return DownloadPdf(self.index)

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.cases.json")

    def run(self):
        with self.input().open('r') as infile:
            filename = infile.read()
        print("filename: "+filename)
        table = pdf2cases.processCasesTable(filename)

        with self.output().open('w') as target:
            target.write(json.dumps(table, sort_keys=True, indent=4))

class DateProcess(luigi.Task):
    index = luigi.Parameter()

    def requires(self):
        return DownloadPdf(self.index)

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.date.json")

    def run(self):
        with self.input().open('r') as infile:
            filename = infile.read()
        print("filename: "+filename)
        date = pdf2date.pdfToken(filename)

        with self.output().open('w') as target:
            target.write(json.dumps(date))


class CasesJson(luigi.Task):
    index = luigi.Parameter()

    def requires(self):
        return { "cases": CasesProcess(self.index), "date": DateProcess(self.index) }

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.cases.format.json")

    def run(self):
        with self.input()['cases'].open('r') as infile:
            cases = json.loads(infile.read())

        with self.input()['date'].open('r') as infile:
            date = json.loads(infile.read())


        #print("filename: "+filename)
        result = getCases.getConfirmedCases(self.index, cases, date)

        with self.output().open('w') as target:
            target.write(json.dumps(result))


class CasesUpload(luigi.Task):
    index = luigi.Parameter()

    def requires(self):
        return CasesJson(self.index)

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.cases.uploaded.txt")

    def run(self):
        with self.input().open('r') as infile:
            cases = json.loads(infile.read())

        #print("filename: "+filename)
        result = bqInsert.insert_table(cases)

        with self.output().open('w') as target:
            target.write(result)



class MasterTask(luigi.Task):
    index = luigi.Parameter()

    def requires(self):
        return [ CasesUpload(self.index) ]

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.master.txt")

    def run(self):

        with self.output().open('w') as target:
            target.write('OK')


class M100Task(luigi.Task):

    def requires(self):
        for index in range(150,210):
            yield MasterTask(index)



if __name__ == '__main__':
    luigi.run
