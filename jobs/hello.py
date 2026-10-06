from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("hello").getOrCreate()
df = spark.range(0, 10_000_000).selectExpr("id % 10 as k", "id as v")
df.groupBy("k").sum("v").show()
input("Press Enter to finish...")  # keeps the driver UI alive so you can look around
spark.stop()