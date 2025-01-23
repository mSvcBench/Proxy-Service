from re import M
from prometheus_api_client import PrometheusConnect, MetricsList, Metric
from prometheus_api_client.utils import parse_datetime
import pandas
from datetime import datetime
from pprint import pprint
# import natsort
import csv
import matplotlib.pyplot as plt
from pprint import pprint


def show_metrics(myquery, start, end):
    # Get the list of all the metrics that the Prometheus host scrapes
  start_time = parse_datetime(start)
  end_time = parse_datetime(end)

  # custom_query_range
  custom_query = prom.custom_query_range(query=myquery, start_time=start_time, end_time=end_time, step="30s")
  
  pprint(custom_query)
  # save the results in a csv file
  # f = open(file_path, 'w')
  # writer = csv.writer(f)
  # writer.writerow(["timestamp", "value"])
  # for ts in custom_query[0]["values"]:
    # print(f"{ts[0]} -> {ts[1]}")
    # writer.writerow([ts[0], ts[1]])
  # f.close()

  # print(f":: Results written in {file_path} ::")
  return


def print_metrics(file):
  # open the file in the read mode
  f = open(file, 'r')
  # create the csv reader
  reader = csv.reader(f)
  # read the first row
  header = next(reader)
  # read the remaining rows
  for row in reader:
    print(row)
  # close the file
  f.close()
  return


def plot_metrics(file):
  # plot using matplotlib
  df = pandas.read_csv(file)
  # df['timestamp'] from 1707149100 to timestamp
  timestamp = df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x))
  plt.plot(timestamp, df['value'])
  plt.xlabel('Timestamp')
  plt.ylim(0, 600)
  plt.ylabel('Value')
  plt.show()
  plt
  return


if __name__ == "__main__":
  prom = PrometheusConnect(url ="http://160.80.223.224:30000", disable_ssl=True)
  
  time_range = "1m"
  ## PROXY SERVICE
  print(":: PROXY SERVICE ::")
  start = "2024-02-07 18:00:30"
  end = "2024-02-07 18:12:00"
  
  ## LEAST_REQUEST
  # print(":: LEAST_REQUEST ::")
  # start = "2024-02-08 10:15:30"
  # end = "2024-02-08 10:26:00"

  ## RANDOM
  # print(":: RANDOM ::")
  # start = "2024-02-08 12:16:30"
  # end = "2024-02-08 12:27:30"
  
  print("############################################")
  print(f"start: {start}")
  print(f"end: {end}")
  print("############################################")
  
  print(":: REQUESTS PER SECOND ::")
  query_reqs = 'sum by (destination_workload) (rate(istio_requests_total{namespace="sock-shop", source_workload="istio-ingress", destination_workload="front-end", response_code!~"5.*|4.*", reporter="destination"}[' + time_range + ']))'
  show_metrics(query_reqs, start, end)  

  print("############################################")
  print(":: AVERAGE DELAY ::")
  query_avg = "sum by (destination_workload) (increase(istio_request_duration_milliseconds_sum{namespace='sock-shop', source_workload='istio-ingress', destination_workload='front-end', response_code!~'5.*|4.*', response_flags='-', reporter='destination'}[" + time_range + "]))/sum by (destination_workload) (increase(istio_request_duration_milliseconds_count{namespace='sock-shop', source_workload='istio-ingress', destination_workload='front-end', response_code!~'5.*|4.*', response_flags='-', reporter='destination'}[" + time_range + "]))"
  show_metrics(query_avg, start, end)

  print("############################################")
  print(f":: P95 ::")
  query_p95 = "histogram_quantile(0.95, sum(irate(istio_request_duration_milliseconds_bucket{reporter='source', destination_canonical_service=~'front-end'}["+ time_range +"])) by (destination_canonical_service,destination_workload_namespace,source_canonical_service,source_workload_namespace,le))"
  show_metrics(query_p95, start, end)

  # print("############################################")
  print(f":: CPUS FRONT-END ::")
  query_cpu_order = "(sum by (container) (rate(container_cpu_usage_seconds_total{namespace='sock-shop', container!='istio-proxy', container!='', container='front-end'}["+ time_range +"]))/sum by (container) (kube_pod_container_resource_limits{namespace='sock-shop', resource='cpu', container!='istio-proxy', container='front-end'}))*100"
  show_metrics(query_cpu_order, start, end)
  print(f":: CPUS CARTS ::")
  query_cpu_order = "(sum by (container) (rate(container_cpu_usage_seconds_total{namespace='sock-shop', container!='istio-proxy', container!='', container='carts'}["+ time_range +"]))/sum by (container) (kube_pod_container_resource_limits{namespace='sock-shop', resource='cpu', container!='istio-proxy', container='carts'}))*100"
  show_metrics(query_cpu_order, start, end)
  print(f":: CPUS ORDERS ::")
  query_cpu_order = "(sum by (container) (rate(container_cpu_usage_seconds_total{namespace='sock-shop', container!='istio-proxy', container!='', container='orders'}["+ time_range +"]))/sum by (container) (kube_pod_container_resource_limits{namespace='sock-shop', resource='cpu', container!='istio-proxy', container='orders'}))*100"
  show_metrics(query_cpu_order, start, end)
  print(f":: CPUS USER ::")
  query_cpu_order = "(sum by (container) (rate(container_cpu_usage_seconds_total{namespace='sock-shop', container!='istio-proxy', container!='', container='user'}["+ time_range +"]))/sum by (container) (kube_pod_container_resource_limits{namespace='sock-shop', resource='cpu', container!='istio-proxy', container='user'}))*100"
  show_metrics(query_cpu_order, start, end)
  
  print("############################################")
  print("############################################")

  # print_metrics(file_path)
  # plot_metrics(file_path)

