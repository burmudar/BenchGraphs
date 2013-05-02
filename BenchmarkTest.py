import unittest
import numpy as np
import opti_benchmarks

class TestBenchmarkFunctions(unittest.TestCase):

    def testBenchmarkDescriptionBuilderBuild(self):
        builder = opti_benchmarks.BenchmarkDescriptionBuilder()
        description = builder.Build()
        self.assertIsNotNone(description)

    def testBenchmarkDescriptionXPlane(self):
        builder = opti_benchmarks.BenchmarkDescriptionBuilder()
        description = builder.XPlane(-5,5).Build()
        self.assertEqual(description.x_near, -5)
        self.assertEqual(description.x_far, 5)
        self.assertTrue(description.HasXPlane())
        return

    def testBenchmarkDescriptionYPlane(self):
        builder = opti_benchmarks.BenchmarkDescriptionBuilder()
        description = builder.YPlane(-5,5).Build()
        self.assertEqual(description.y_near, -5)
        self.assertEqual(description.y_far, 5)
        self.assertTrue(description.HasYPlane())
        return

    def testBenchmarkDescriptionZPlane(self):
        builder = opti_benchmarks.BenchmarkDescriptionBuilder()
        description = builder.ZPlane(-5,5).Build()
        self.assertEqual(description.z_near, -5)
        self.assertEqual(description.z_far, 5)
        self.assertTrue(description.HasZPlane())
        return

    def testBenchmarkDescriptionAmountOfPoints(self):
        builder = opti_benchmarks.BenchmarkDescriptionBuilder()
        description = builder.AmountOfPoints(150).Build()
        self.assertEqual(description.amount_of_points, 150)
        return

    def testBenchmarkDescriptionBuilderNewInstance(self):
        builder = opti_benchmarks.BenchmarkDescriptionBuilder()
        description = builder.AmountOfPoints(150).NewInstance().XPlane(-10,10).Build()
        self.assertNotEqual(description.amount_of_points, 150)
        self.assertEquals(description.x_near, -10)
        self.assertEquals(description.x_far, 10)
        return

    def testBenchmarkDescriptionWithDeJongF1(self):
        builder = opti_benchmarks.BenchmarkDescriptionBuilder()
        description = builder.DeJongF1().Build()
        self.assertIsNotNone(description.benchFn)
        self.assertIsNotNone(description.benchTitle)
        self.assertEqual(description.benchTitle, opti_benchmarks.DEJONGF1_TITLE)
        self.assertEqual(description.benchFn, opti_benchmarks.DeJongF1)
        return

    def testBenchmarkDescriptionNPLinspaceCreation(self):
        builder = opti_benchmarks.BenchmarkDescriptionBuilder();
        description = builder.DeJongF1().AmountOfPoints(150).XPlane(-5.12,5.12).YPlane(-5.12,5.12).Build()
        self.assertIsNotNone(description.CreateXLinspace())
        self.assertIsNotNone(description.CreateYLinspace())
        self.assertIsInstance(description.CreateXLinspace(), np.ndarray, "Expected created X linspace to be of numpy.darray")
        self.assertIsInstance(description.CreateYLinspace(), np.ndarray, "Expected created Y linsapce to be of numpy.darray")

    def testBenchRunnerIsValidDescription(self):
        runner = opti_benchmarks.BenchmarkRunner()
        self.assertFalse(runner.IsValidDescription(None))
        self.assertFalse(runner.IsValidDescription(opti_benchmarks.BenchmarkDescription()))
        builder = opti_benchmarks.BenchmarkDescriptionBuilder()
        description = builder.DeJongF1().AmountOfPoints(150).XPlane(-5.12,5.12).Build()
        self.assertFalse(runner.IsValidDescription(description))
        description = builder.DeJongF1().AmountOfPoints(150).YPlane(-5.12,5.12).Build()
        self.assertFalse(runner.IsValidDescription(description))
        description = builder.DeJongF1().AmountOfPoints(150).Build()
        self.assertFalse(runner.IsValidDescription(description))
        description = builder.DeJongF1().AmountOfPoints(150).XPlane(-5.12,5.12).YPlane(-5.12,5.12).Build()
        self.assertTrue(runner.IsValidDescription(description))
        return


    def testBenchRunnerRunBenchmark(self):
        runner = opti_benchmarks.BenchmarkRunner()
        self.assertRaises(opti_benchmarks.BenchmarkDescriptionError, runner.RunBenchmark, None)
        builder = opti_benchmarks.BenchmarkDescriptionBuilder()
        description = builder.AmountOfPoints(150).XPlane(-5.12,5.12).YPlane(-5.12,5.12).DeJongF1().Build()
        result = runner.RunBenchmark(description)
        self.assertIsNotNone(result, "Expected a result after the benchmark was executed")
        self.assertTrue(len(result.X) == description.amount_of_points)
        self.assertTrue(len(result.Y) == description.amount_of_points)
        self.assertTrue(len(result.Z) == description.amount_of_points)
        return

    def testBenchmarkPlotter(self):
        runner = opti_benchmarks.BenchmarkRunner();
        builder = opti_benchmarks.BenchmarkDescriptionBuilder();
        description = builder.AmountOfPoints(150).XPlane(-5.12,5.12).YPlane(-5.12,5.12).DeJongF1().Build();
        result = runner.RunBenchmark(description);
        plotter = opti_benchmarks.BenchmarkResultPlotter()
        plotter.PlotResult(result)
        with open(result.BenchTitle + ".pdf", "r") as testFile:
            self.assertTrue(result.BenchTitle, testFile.name)


if __name__ == "__main__":
    unittest.main()
