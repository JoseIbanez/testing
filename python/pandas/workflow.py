#!/usr/bin/python3.7

import luigi
import getPdf

class GetId(luigi.Task):
    index = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.getId.txt")

    def run(self):
        with self.output().open('w') as target:
            target.write('OK')


class DownloadPdf(luigi.Task):
    index = luigi.Parameter()

    def requires(self):
        return GetId(self.index)

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.downloadPdf.txt")

    def run(self):
        with self.output().open('w') as target:
            filename = getPdf.getGovPdf(self.index)
            target.write(filename)


class PandasProcess(luigi.Task):
    index = luigi.Parameter()

    def requires(self):
        return DownloadPdf(self.index)

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.pandasProcess.txt")

    def run(self):
        with self.input().open('r') as infile:
            filename = infile.read()
        print("PANDAS: "+filename)

        with self.output().open('w') as target:
            target.write("OK")




class MasterTask(luigi.Task):
    index = luigi.Parameter()

    def requires(self):
        return PandasProcess(self.index)

    def output(self):
        return luigi.LocalTarget(f"./data/task-{self.index}.master.txt")

    def run(self):

        with self.output().open('w') as target:
            target.write('OK')

if __name__ == '__main__':
    luigi.run
