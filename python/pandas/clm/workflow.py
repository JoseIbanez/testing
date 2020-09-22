#!/usr/bin/python3.7

import luigi
import json
from time import strftime
import datetime

import getNotasDay
import getText
import bqInsert


BQ_TABLE_CLM = "cases_CLM"


class DownloadLastPages(luigi.Task):
    today = strftime("%Y-%m-%d")


    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.today}.lastPages.txt")

    def run(self):
        getNotasDay.getLastPages()
        
        with self.output().open('w') as target:
            target.write(self.today)


class DownloadNotesDay(luigi.Task):

    date = luigi.Parameter()


    def requires(self):
        return DownloadLastPages()

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.date}.notes.txt")

    def run(self):
        getNotasDay.getNotesFromDay(self.date)
        
        with self.output().open('w') as target:
            target.write(self.date)


class ParseNoteDay(luigi.Task):

    date = luigi.Parameter()


    def requires(self):
        return DownloadNotesDay(self.date)

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.date}.data.json")

    def run(self):
        data=getText.parseByDate(self.date)
        
        with self.output().open('w') as target:
            target.write(json.dumps(data))


class CasesUpload(luigi.Task):
    date = luigi.Parameter()

    def requires(self):
        return ParseNoteDay(self.date)

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.date}.uploaded.txt")

    def run(self):
        with self.input().open('r') as infile:
            cases = json.loads(infile.read())

        #print("filename: "+filename)
        result = bqInsert.insert_table(BQ_TABLE_CLM, cases)

        with self.output().open('w') as target:
            target.write(result)




class MasterTask(luigi.Task):
    date = luigi.Parameter()

    def requires(self):
        return [ CasesUpload(self.date) ]

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.date}.master.txt")

    def run(self):

        with self.output().open('w') as target:
            target.write('OK')



class M100Task(luigi.Task):

    numdays = luigi.Parameter()

    def requires(self):

        base = datetime.datetime.today()
        date_list = [base - datetime.timedelta(days=x) for x in range(int(self.numdays))]

        for date in date_list:
            dateiso = date.strftime("%Y-%m-%d")
            print(dateiso)
            yield MasterTask(dateiso)




if __name__ == '__main__':
    luigi.run
