import argparse
import os
from util import bai

if __name__ == '__main__':
  # set up parser
  parser = argparse.ArgumentParser( \
    description='script for creating a Batch AI cluster.')
  parser.add_argument(
    '--name', 
    dest='cluster_name', 
    help='The name of the cluster you wish to create.'
  )
  parser.set_defaults(upload_data=False)
  args = parser.parse_args()
  
  cluster_name = args.cluster_name or \
    os.getenv('CLUSTER_NAME')

  # setup bai 
  client = bai.setup_bai()

  # create a workspace
  bai.create_workspace(client)

  # create an autoscsale cluster
  bai.create_autoscale_cluster(client, cluster_name)

  # print cluster state
  cluster = bai.get_cluster(client, cluster_name)
  print(('Cluster state: {0}; Allocated: {1}; Idle: {2}; ' +
         'Unusable: {3}; Running: {4}; Preparing: {5}; ' +
         'Leaving: {6}').format(
    cluster.allocation_state,
    cluster.current_node_count,
    cluster.node_state_counts.idle_node_count,
    cluster.node_state_counts.unusable_node_count,
    cluster.node_state_counts.running_node_count,
    cluster.node_state_counts.preparing_node_count,
    cluster.node_state_counts.leaving_node_count))


