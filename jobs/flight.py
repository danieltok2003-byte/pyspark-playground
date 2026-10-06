from pyspark.sql import SparkSession
from pyspark.sql.functions import desc

spark = SparkSession.builder.appName("flight").getOrCreate()

flightData2015 = spark.read.option("header", "true").option("inferSchema", "true").csv("/opt/spark/data/2015-summary.csv")
flightData2015.take(3)
spark.conf.set("spark.sql.shuffle.partitions", "5")
flightData2015.sort("count").explain()
flightData2015.createOrReplaceTempView("flight_data_2015")
sqlWay = spark.sql("""
SELECT DEST_COUNTRY_NAME, count(1)
FROM flight_data_2015
GROUP BY DEST_COUNTRY_NAME
""")
dataFrameWay = flightData2015.groupBy("DEST_COUNTRY_NAME").count()
sqlWay.explain()
dataFrameWay.explain()


maxSql = spark.sql("""
SELECT DEST_COUNTRY_NAME, sum(count) as destination_total
FROM flight_data_2015
GROUP BY DEST_COUNTRY_NAME
ORDER BY sum(count) DESC
LIMIT 5
""")
maxSql.show()


maxPython = flightData2015.groupBy('DEST_COUNTRY_NAME').sum('count').withColumnRenamed('sum(count)', 'destination_total').sort(desc('destination_total')).limit(5).explain()

input('wait')